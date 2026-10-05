"""Set all of the site's text in 29LT Zawi.

29Letters lets us modify and use their fonts in any medium, but not
redistribute them. A webfont would put a copy of the font in every visitor's
browser, so the font is never served. Instead, at build time, every word of
text is shaped with HarfBuzz (proper Arabic joining and Latin
kerning) and replaced by an inline SVG of its outlines. Visitors receive
shapes, not the font.

What is converted: every piece of visible text on the page (headings, labels,
buttons, menus, numbers and running paragraphs). Headings, .display, .lbl and
data-kw text use the heavy weights; everything else uses Regular, or Bold when
its Tailwind classes ask for font-semibold/bold. Only text inside <script>,
<style>, form fields and data-nokw elements is left alone.

For every converted text node:
  - the original text stays in the page as .sr-only, so screen readers, search
    engines and translation tools still read it
  - words are separate inline SVGs joined by real spaces, so lines wrap
    naturally at every width
  - each unique word is drawn once in a sprite at the top of <body> and reused
  - characters Zawi lacks fall back to ordinary text (.kw-txt)
Count-up numbers (data-count) get a per-digit sprite so the script can keep
animating them.
"""
import html as H
import os
import re
import sys

from bs4 import BeautifulSoup, NavigableString, Comment
from bs4.formatter import HTMLFormatter
from fontTools.pens.basePen import BasePen

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "fonts"))
from shape_svg import _load  # noqa: E402

DIST = os.path.join(os.path.dirname(HERE), "fonts", "dist")
FONTS = {"black": os.path.join(DIST, "29LT_Zawi_KU_Black.ttf"),
         "bold": os.path.join(DIST, "29LT_Zawi_KU_Bold.ttf"),
         "regular": os.path.join(DIST, "29LT_Zawi_KU_Regular.ttf")}
# Each word is drawn in a box that covers the font's whole ink (tall V marks reach 1.18 em above
# the baseline, tails go 0.6 em below), so no container with overflow hidden can shave them off.
# All weights share these numbers, so the box height, baseline shift and the negative margins that
# keep line spacing as it was live in CSS (svg.kw) instead of in every tag.
ASC, DESC = 1200, 620
HHEA = (840, 360)  # the font's own ascent/descent; the line layout was tuned to these
FIRE = ("#ffc300", "#ffea00")  # the yellow gradient behind .fire-text
HB_LANG = {"en": "en", "ckb": "ckb", "ar": "ar", "fa": "fa"}
IGNORABLE = "‌‍‎‏"
SKIP_TAGS = {"script", "style", "svg", "noscript", "head", "title", "textarea", "option", "select", "code", "pre"}
HEADINGS = {"h1", "h2", "h3", "h4"}
DIGIT_SETS = ["0123456789", "٠١٢٣٤٥٦٧٨٩",
              "۰۱۲۳۴۵۶۷۸۹"]
_AD = "\u0660-\u0669\u06f0-\u06f9"  # Arabic-Indic and Persian digits
# runs that read left to right inside right-to-left text (Unicode bidi: Latin letters, and numbers)
RUN_RE = re.compile(
    r"(?P<latin>[A-Za-z0-9](?:[A-Za-z0-9.,'\u2019:/&+%@_-]*[A-Za-z0-9%])?)"
    rf"|(?P<num>[{_AD}]+(?:[.,:/\u066b\u066c][{_AD}]+)*)")
LATIN_ONLY = re.compile(r"[+@]?[A-Za-z0-9](?:[\x21-\x7e]*[A-Za-z0-9])?")  # no trailing punctuation
OUTLINE_STROKE = 24  # font units; scales with the text


class _KeepOrder(HTMLFormatter):
    """Serialise without bs4's default alphabetical attribute sorting."""
    def attributes(self, tag):
        return list(tag.attrs.items())


_FMT = _KeepOrder(entity_substitution=HTMLFormatter.REGISTRY["minimal"].entity_substitution,
                  void_element_close_prefix="/")


def available():
    return all(os.path.exists(p) for p in FONTS.values())


def _classes(el):
    return el.get("class", []) if hasattr(el, "get") else []


def _covered(font, token):
    _, tt, _, _ = _load(FONTS[font])
    cmap = tt.getBestCmap()
    return all(ord(c) in cmap or c in IGNORABLE for c in token)


def _runs(token):
    """Split into (text, kind) runs; kind is 'latin' or 'num' (both left to right) or 'arab'."""
    runs, i = [], 0
    for m in RUN_RE.finditer(token):
        if m.start() > i:
            runs.append((token[i:m.start()], "arab"))
        runs.append((m.group(), m.lastgroup))
        i = m.end()
    if i < len(token):
        runs.append((token[i:], "arab"))
    return runs


class _CompactPen(BasePen):
    """SVG path data in whole units with relative commands and no wasted separators. The pages carry
    hundreds of word outlines, so this is about a third smaller than absolute coordinates."""

    def __init__(self, glyphset=None):
        super().__init__(glyphset)
        self.buf, self.cur, self.start, self.last, self.after_letter = [], (0, 0), (0, 0), "", True

    def _emit(self, cmd, nums):
        if not (cmd == self.last and cmd not in "mz"):   # a repeated command needs no letter
            self.buf.append(cmd)
            self.after_letter = True
        for n in nums:
            self.buf.append(str(n) if (n < 0 or self.after_letter) else " " + str(n))
            self.after_letter = False
        self.last = cmd

    def _moveTo(self, pt):
        pt = (round(pt[0]), round(pt[1]))
        self._emit("m", [pt[0] - self.cur[0], pt[1] - self.cur[1]])
        self.cur = self.start = pt

    def _lineTo(self, pt):
        pt = (round(pt[0]), round(pt[1]))
        dx, dy = pt[0] - self.cur[0], pt[1] - self.cur[1]
        if dx == 0 and dy == 0:
            return
        if dy == 0:
            self._emit("h", [dx])
        elif dx == 0:
            self._emit("v", [dy])
        else:
            self._emit("l", [dx, dy])
        self.cur = pt

    def _qCurveToOne(self, p1, p2):
        p1, p2 = (round(p1[0]), round(p1[1])), (round(p2[0]), round(p2[1]))
        if p1 == self.cur and p2 == self.cur:
            return
        cx, cy = self.cur
        self._emit("q", [p1[0] - cx, p1[1] - cy, p2[0] - cx, p2[1] - cy])
        self.cur = p2

    def _curveToOne(self, p1, p2, p3):
        pts = [(round(p[0]), round(p[1])) for p in (p1, p2, p3)]
        cx, cy = self.cur
        self._emit("c", [v for p in pts for v in (p[0] - cx, p[1] - cy)])
        self.cur = pts[2]

    def _closePath(self):
        self._emit("z", [])
        self.cur = self.start

    def _endPath(self):
        pass

    def path(self):
        return "".join(self.buf)


def _shape(font, token, base_dir, lang, tracking):
    """Outline of one word in font units (y down, origin at left of baseline)."""
    import uharfbuzz as hb
    from fontTools.pens.transformPen import TransformPen
    hb_font, tt, glyphset, upem = _load(FONTS[font])
    order = tt.getGlyphOrder()
    import pathops
    # draw every glyph into one path, then union it: connected Arabic letters overlap at their
    # joins, which an outlined (stroke-only) word would show as stray inner lines
    merged = pathops.Path()
    pen = merged.getPen(glyphSet=glyphset)
    x = 0.0
    runs = _runs(token)
    if base_dir == "rtl":
        runs = list(reversed(runs))  # first run is drawn rightmost
    for text, kind in runs:
        buf = hb.Buffer()
        buf.add_str(text)
        if kind == "latin":
            buf.direction, buf.script, buf.language = "ltr", "Latn", "en"
        elif kind == "num":
            buf.direction, buf.script, buf.language = "ltr", "Arab", HB_LANG.get(lang, "ar")
        else:
            buf.direction, buf.script, buf.language = "rtl", "Arab", HB_LANG.get(lang, "ar")
        hb.shape(hb_font, buf, {"kern": True, "liga": True})
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            glyphset[order[info.codepoint]].draw(
                TransformPen(pen, (1, 0, 0, -1, x + pos.x_offset, -pos.y_offset)))
            x += pos.x_advance + (tracking * upem if kind == "latin" else 0)
    merged.simplify(fix_winding=True, keep_starting_points=False)
    out = _CompactPen(glyphset)
    merged.draw(out)
    hhea = tt["hhea"]
    return out.path(), x, hhea.ascent, -hhea.descent, upem


def _px_size(el):
    """Base font size in px from a Tailwind arbitrary class (text-[44px]), if any."""
    node = el
    while node is not None and hasattr(node, "get"):
        for c in _classes(node):
            m = re.fullmatch(r"text-\[(\d+)px\]", c)
            if m:
                return int(m.group(1))
        node = node.parent
    return None


TRACKING = {"tracking-tighter": -0.05, "tracking-tight": -0.025, "tracking-wide": 0.025,
            "tracking-wider": 0.05, "tracking-widest": 0.1}


def _style_for(trigger, node, body=False):
    """(font, caps, kind, outline, fire, tracking_class) for a text node under `trigger`."""
    chain, p = [], node.parent
    while p is not None and hasattr(p, "get"):
        chain.append(p)
        p = p.parent
    classes = set()
    for el in chain:
        classes.update(_classes(el))
    is_display = "display" in classes or trigger.name in ("h1", "h2")
    is_lbl = "lbl" in classes
    size = _px_size(trigger) or 0
    if body and not (is_display or is_lbl or trigger.name in HEADINGS):
        if "font-black" in classes:
            font = "black"
        elif classes & {"font-bold", "font-semibold", "font-extrabold"}:
            font = "bold"
        else:
            font = "regular"
    else:
        font = "black" if (is_display and (size == 0 or size > 24)) else "bold"
    track = None
    for c in classes:
        m = re.fullmatch(r"tracking-\[(-?[\d.]+)em\]", c)
        if m:
            track = float(m.group(1))
        elif c in TRACKING:
            track = TRACKING[c]
    return font, ("display" in classes or is_lbl or "uppercase" in classes), \
        ("lbl" if is_lbl else "display" if "display" in classes else ""), "ol" in classes, "fire-text" in classes, track


def _find_trigger(node):
    p = node.parent
    while p is not None and hasattr(p, "get"):
        if p.name in SKIP_TAGS or "sr-only" in _classes(p) or "kw-line" in _classes(p) or p.has_attr("data-nokw"):
            return None
        if p.name in HEADINGS or "display" in _classes(p) or "lbl" in _classes(p) or p.has_attr("data-kw"):
            return p
        p = p.parent
    return None


def _body_parent(node):
    """The element to style ordinary text by, or None if this text must stay as it is."""
    p = node.parent
    while p is not None and hasattr(p, "get"):
        if p.name in SKIP_TAGS or "sr-only" in _classes(p) or "kw-line" in _classes(p) or p.has_attr("data-nokw") \
                or p.has_attr("hidden") or p.has_attr("data-count"):
            return None
        p = p.parent
    return node.parent


def apply(html, lang="en"):
    soup = BeautifulSoup(html, "html.parser")
    rtl = soup.html is not None and soup.html.get("dir") == "rtl"
    base_dir = "rtl" if rtl else "ltr"
    sprite, ids, count_chars = [], {}, {}
    meta = {}
    fit_em = {}  # element -> total width in em, for data-fit headings

    def word_ref(font, token, tracking, bdir=None):
        bdir = bdir or base_dir
        key = (font, token, tracking, bdir)
        if key not in ids:
            d, w, asc, desc, upem = _shape(font, token, bdir, lang, tracking)
            meta.update(asc=asc, desc=desc, upem=upem)
            ids[key] = (f"kw{len(ids)}", w)
            sprite.append(f'<path id="kw{len(ids) - 1}" d="{d}"/>')
        return ids[key]

    def svg_for(font, token, tracking, fill, outline, bdir=None):
        kid, w = word_ref(font, token, tracking, bdir)
        asc, desc, upem = meta["asc"], meta["desc"], meta["upem"]
        assert (asc, desc, upem) == (*HHEA, 1000), "Zawi metrics changed: update ASC/DESC/HHEA and svg.kw in the CSS"
        paint = (f' fill="none" stroke="currentColor" stroke-width="{OUTLINE_STROKE}" stroke-linejoin="round"'
                 if outline else (f' fill="{fill}"' if fill != "currentColor" else ""))
        return f'<svg class="kw" viewBox="0 -{ASC} {w:.0f} {ASC + DESC}"><use href="#{kid}"{paint}/></svg>'

    # ---- numbers that count up: one sprite glyph per character --------------
    for el in soup.select("[data-count]"):
        text = el.get_text().strip()
        dset = next((s for s in DIGIT_SETS[1:] if any(d in text for d in s)), DIGIT_SETS[0])
        for ch in dset + "+":
            if ch not in count_chars:
                d, w, asc, desc, upem = _shape("black", ch, "ltr", lang, 0)
                meta.update(asc=asc, desc=desc, upem=upem)
                count_chars[ch] = (d, w)
        shown = list(text)
        if rtl and shown and shown[-1] == "+":
            shown.insert(0, shown.pop())
        parts = []
        for ch in shown:
            if ch in count_chars:
                w = count_chars[ch][1]
                parts.append(
                    f'<svg class="kw" viewBox="0 {-ASC} {w:.0f} {ASC + DESC}" '
                    f'style="width:{w / meta["upem"]:.3f}em;height:{(ASC + DESC) / meta["upem"]:.3f}em;'
                    f'vertical-align:{-DESC / meta["upem"]:.3f}em"><use href="#kc{ord(ch)}" fill="currentColor"/></svg>')
        el["data-count-text"] = text
        el.clear()
        el.append(BeautifulSoup(
            f'<span class="sr-only">{H.escape(text)}</span>'
            f'<span class="kw-count" dir="ltr" aria-hidden="true">{"".join(parts)}</span>', "html.parser"))

    # ---- everything else ----------------------------------------------------
    for node in list(soup.find_all(string=True)):
        # exact type: Doctype, comments, CDATA etc. are NavigableString subclasses and must stay untouched
        if type(node) is not NavigableString:
            continue
        text = str(node)
        if not text.strip():
            continue
        if any(p.has_attr("data-count") for p in node.parents if hasattr(p, "has_attr")):
            continue
        trigger = _find_trigger(node)
        body = trigger is None
        if body:
            trigger = _body_parent(node)
            if trigger is None:
                continue
        font, caps, kind, outline, fire, track = _style_for(trigger, node, body)
        tracking = 0.0
        if not rtl and lang == "en":
            tracking = 0.2 if kind == "lbl" else -0.01 if kind == "display" else 0.0
            if track is not None:
                tracking = track
        fill = "url(#kwfire)" if fire else "currentColor"
        shown = text.upper() if (caps and lang == "en") else text
        parts, ltr = [], []   # `ltr` = Latin words being collected into one left-to-right group
        prev_latin = False

        def flush():
            if ltr:
                parts.append('<span dir="ltr" class="kw-ltr">' + "".join(ltr) + "</span>")
                ltr.clear()

        for tok in re.split(r"(\s+)", shown):
            if not tok:
                continue
            if tok.isspace():
                _, tt, _, upem_ = _load(FONTS[font])
                fit_em[id(trigger)] = fit_em.get(id(trigger), 0) + tt["hmtx"]["space"][0] / upem_ * len(tok)
                (ltr if ltr else parts).append(" ")
                continue
            # Unicode bidi keeps Latin words (and numbers after them) in left-to-right order
            # inside right-to-left text: "Strap Iraq" must not become "Iraq Strap"
            is_latin = bool(re.search("[A-Za-z]", tok)) or bool(LATIN_ONLY.fullmatch(tok)) or (prev_latin and bool(re.fullmatch(r"[0-9.,:%+-]+", tok)))
            if rtl and not is_latin and ltr and ltr[-1] == " ":
                ltr.pop()
                flush()
                parts.append(" ")
            elif rtl and not is_latin:
                flush()
            prev_latin = is_latin
            if _covered(font, tok):
                # an e-mail address is one long word: let it break before the @ on narrow columns
                bits = [tok] if ("@" not in tok or len(tok) < 14) else [tok.split("@")[0], "@" + tok.split("@", 1)[1]]
                # e-mails, phone numbers, handles and web addresses read left to right even on a
                # right-to-left page (their @ and + must not be flipped to the wrong end)
                bdir = "ltr" if (rtl and all(LATIN_ONLY.fullmatch(b) for b in bits)) else None
                piece = "<wbr/>".join(svg_for(font, b, tracking, fill, outline, bdir) for b in bits)
                fit_em[id(trigger)] = fit_em.get(id(trigger), 0) + sum(word_ref(font, b, tracking, bdir)[1] for b in bits) / meta["upem"]
            else:
                piece = f'<span class="kw-txt">{H.escape(tok)}</span>'
            (ltr if (rtl and is_latin) else parts).append(piece)
        if ltr and ltr[-1] == " ":
            ltr.pop()
            flush()
            parts.append(" ")
        else:
            flush()
        new = BeautifulSoup(
            f'<span class="kw-line"><span class="sr-only">{H.escape(text)}</span>'
            f'<span aria-hidden="true">{"".join(parts)}</span></span>', "html.parser")
        node.replace_with(new)

    # headings that must fill their row (the footer name): size = share of the row / measured width
    for el in soup.select("[data-fit]"):
        if fit_em.get(id(el)):
            el["style"] = f"--fit:{float(el['data-fit']) / fit_em[id(el)]:.4f}"
        del el["data-fit"]

    if sprite or count_chars:
        counts = "".join(f'<path id="kc{ord(ch)}" data-w="{w:.0f}" d="{d}"/>' for ch, (d, w) in count_chars.items())
        defs = BeautifulSoup(
            f'<svg id="kwsprite" width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false" '
            f'data-asc="{ASC}" data-desc="{DESC}" data-upem="{meta["upem"]}"><defs>'
            f'<linearGradient id="kwfire" x1="0" x2="1"><stop offset="0" stop-color="{FIRE[0]}"/>'
            f'<stop offset="1" stop-color="{FIRE[1]}"/></linearGradient>'
            + "".join(sprite) + counts + "</defs></svg>", "html.parser")
        soup.body.insert(0, defs)
    out = soup.decode(formatter=_FMT)
    out = re.sub(r"^(<!DOCTYPE html>)\n+", r"\1\n", out)
    return out, len(ids)
