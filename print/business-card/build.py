#!/usr/bin/env python3
"""Builds Dindar Ahmed's business card: front.svg (bilingual), back.svg (bilingual),
the print pages and a grid guide. One card for everyone: English and Kurdish side by side.

The SVGs are the source of truth; open and edit them in Illustrator or
Figma. All text is set in 29LT Zawi (extended with the Sorani letters, see
tools/fonts/extend_zawi.py) and drawn as outlines, so no font has to be
installed and no font file is ever handed to the printer (the 29Letters
licence forbids redistributing the fonts). To change wording, edit the
details below and run this script; text in the SVGs is shapes, not live type.

Needs: tools/venv with tools/requirements.txt (uharfbuzz, fonttools)
and the built fonts in tools/fonts/dist.
Card: 85 x 55 mm trim, 3 mm bleed (91 x 61 mm artboard).

LAYOUT: a Swiss modular grid, 6 columns x 4 rows, on a live area inset 7 mm from the sides and
6 mm from top and bottom of the trim (so everything is at least 6 mm inside the cut), 3 mm gutters.
  - flush-left English hangs from the left margin, flush-right Kurdish from the right margin
  - top and bottom margins are the two baselines everything is set on
  - the back mirrors the front: names on the top margin, titles on row 1, the same hairline, contacts ending on
    the bottom margin
  - one size scale, a few weights, no decoration except one hairline rule
python3 build.py also writes grid.svg, the grid drawn over the card, for checking.
"""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "fonts"))
from shape_svg import shape_to_path, _load  # noqa: E402

DIST = os.path.join(ROOT, "tools", "fonts", "dist")
ZAWI = {w: os.path.join(DIST, f"29LT_Zawi_KU_{n}.ttf") for w, n in
        {400: "Regular", 500: "Medium", 700: "Bold", 900: "Black"}.items()}

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- details (single place to edit) ----
NAME_EN = "Dindar Ahmed"
NAME_KU = "دیندار ئەحمەد"
TITLE_EN = ("Marketing Manager", "and Consultant")          # two lines, set under the name
TITLE_KU = "بەڕێوەبەر و ڕاوێژکاری مارکێتینگ"                # as in the website's page title
PHONE = "+964 771 992 2486"
EMAIL = "Dindar.Ahmed@mithra.agency"
WEB = "dindarahmed.com"
SLOGAN_EN = ("TELL ME", "WHAT ISN'T", "SELLING")            # the website's headline; the middle line is the accent
SLOGAN_KU = ("پێم بڵێ", "چی", "نافرۆشرێت")

# ---- palette (same as the website) ----
BLACK, VIOLET, LAVENDER = "#000000", "#7161ef", "#957fef"
Y1, Y4 = "#ffc300", "#ffea00"
WHITE = "#ffffff"
SOFT = "#e6e6e6"   # white at 90%, as a flat colour (safer in Illustrator and for print)

W, H, BLEED = 91, 61, 3

# ---- the grid (all values in mm on the 91 x 61 artboard; the trim starts at BLEED) ----
M, GUT, COLS = 6.0, 3.0, 6             # margin on all four sides of the trim, gutter, columns
GL, GR = BLEED + M, W - BLEED - M      # live area left / right edge   (9 .. 82)
GT, GB = BLEED + M, H - BLEED - M      # live area top / bottom edge   (9 .. 52)
CW = (GR - GL - (COLS - 1) * GUT) / COLS   # column width (9.67)
LEAD = 3.2                             # baseline step of the small text; the bottom margin is its last baseline


def col(i):
    """left edge of column i (0-based)"""
    return GL + i * (CW + GUT)


def span(n):
    """width of n columns with their gutters"""
    return n * CW + (n - 1) * GUT


CAP = 0.70     # cap height of Zawi, in em
ARAB = 0.78    # height of the Arabic letters above the baseline (without the V marks), in em; used to match sizes

def line(text, size, weight, x, y, fill, rtl=False, tracking=0.0, label=None, tail=None, anchor_left=False):
    """One line of text as a filled outline path (mm units), named for the layer panel.
    x is the left edge for left-to-right text and the right edge for right-to-left.
    tail=(text, fill) adds a trailing character in a second colour (the full stop)."""
    kw = dict(direction="rtl", script="Arab", language="ckb") if rtl else dict(direction="ltr", script="Latn", language="en")
    d, w, _, _ = shape_to_path(ZAWI[weight], text, size, tracking=tracking, **kw)
    w -= tracking  # no trailing space after the last letter
    ox = x if (not rtl or anchor_left) else x - w
    out = f'<path transform="translate({ox:.3f} {y:.3f})" fill="{fill}" d="{d}"/>'
    if tail:
        t, tfill = tail
        td, tw, _, _ = shape_to_path(ZAWI[weight], t, size, direction="ltr", script="Latn", language="en", tracking=tracking)
        tx = ox - tw + 0.5 if rtl else ox + w + tracking  # RTL: pull the dot in; the Arabic joining leaves it looser
        out += f'\n<path transform="translate({tx:.3f} {y:.3f})" fill="{tfill}" d="{td}"/>'
    return f'<g aria-label="{label or text}">{out}</g>\n'


def svg_open(title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">\n'
            f'<title>{title}</title>\n')


def width(text, size, weight, rtl=False, tracking=0.0):
    kw = dict(direction="rtl", script="Arab", language="ckb") if rtl else dict(direction="ltr", script="Latn", language="en")
    return shape_to_path(ZAWI[weight], text, size, tracking=tracking, **kw)[1] - tracking


def fit(lines, weight, target, rtl=False, tracking_em=0.0):
    """the size (mm) at which the longest line is exactly `target` mm wide"""
    w1 = max(width(t, 1.0, weight, rtl, tracking_em) for t in lines)
    return target / w1


def ink(text, size, weight, rtl=False):
    """(top, bottom) of the drawn letters relative to the baseline, in mm (SVG y-down: top is negative)"""
    import uharfbuzz as hb
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.pens.transformPen import TransformPen
    font, tt, gs, upem = _load(ZAWI[weight])
    buf = hb.Buffer()
    buf.add_str(text)
    buf.direction, buf.script, buf.language = ("rtl", "Arab", "ckb") if rtl else ("ltr", "Latn", "en")
    hb.shape(font, buf, {"kern": True, "liga": True})
    bp, x, order = BoundsPen(gs), 0, tt.getGlyphOrder()
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        gs[order[info.codepoint]].draw(TransformPen(bp, (1, 0, 0, 1, x + pos.x_offset, pos.y_offset)))
        x += pos.x_advance
    _, y0, _, y1 = bp.bounds
    k = size / upem
    return -y1 * k, -y0 * k


def small_size():
    """one size for all the small text: the e-mail fills three columns exactly, never larger than 2.2 mm"""
    return min(2.2, span(3) / width(EMAIL, 1.0, 500))


def side_en():
    """English side, black. Slogan hangs from the top margin across four columns; under it, on the bottom
    margin, two blocks on one baseline grid: name and title in columns 1-3, contacts in columns 4-6."""
    s_slogan = fit(SLOGAN_EN, 900, span(4), tracking_em=-0.02)
    step = s_slogan * 1.0
    b1 = GT - ink(SLOGAN_EN[0], s_slogan, 900)[0]       # the ink of the first line touches the top margin
    t = small_size()
    rows = [GB - 2 * LEAD, GB - LEAD, GB]
    out = svg_open("Dindar Ahmed business card, English side")
    out += f"""<defs>
<radialGradient id="glow" cx="1" cy="0" r="1">
<stop offset="0" stop-color="{VIOLET}" stop-opacity="0.30"/>
<stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
</radialGradient>
</defs>
<rect width="{W}" height="{H}" fill="{BLACK}"/>
<rect width="{W}" height="{H}" fill="url(#glow)"/>
{line(SLOGAN_EN[0], s_slogan, 900, GL, b1, WHITE, tracking=-0.02 * s_slogan)}{line(SLOGAN_EN[1], s_slogan, 900, GL, b1 + step, Y1, tracking=-0.02 * s_slogan)}{line(SLOGAN_EN[2], s_slogan, 900, GL, b1 + 2 * step, WHITE, tracking=-0.02 * s_slogan, tail=(".", Y1))}{line(NAME_EN, t * 1.15, 700, GL, rows[0], WHITE)}{line(TITLE_EN[0], t, 500, GL, rows[1], LAVENDER)}{line(TITLE_EN[1], t, 500, GL, rows[2], LAVENDER)}{line(PHONE, t, 500, col(3), rows[0], SOFT)}{line(EMAIL, t, 500, col(3), rows[1], SOFT)}{line(WEB, t, 500, col(3), rows[2], SOFT)}</svg>
"""
    return out


def side_ku():
    """Kurdish side, brand yellow: the English side mirrored for right-to-left reading. Slogan flush right from the
    top margin across four columns; name and title flush right in columns 4-6; contacts (left to right) in 1-3."""
    t = small_size()
    rows = [GB - 2 * LEAD, GB - LEAD, GB]
    s_en = fit(SLOGAN_EN, 900, span(4), tracking_em=-0.02)
    s_slogan = min(CAP * s_en / ARAB, fit(SLOGAN_KU, 900, span(4), rtl=True))   # same letter height as the English
    floor = rows[0] - CAP * t - GUT                     # the slogan's ink must end one gutter above the info block
    while True:
        step = s_slogan * 1.3
        b1 = GT - ink(SLOGAN_KU[0], s_slogan, 900, rtl=True)[0]     # V marks of line 1 touch the top margin
        bottom = b1 + 2 * step + ink(SLOGAN_KU[2], s_slogan, 900, rtl=True)[1]
        if bottom <= floor:
            break
        s_slogan -= 0.1
    fg, accent = BLACK, "#4b3bd0"         # a deeper violet than the website's, for contrast on yellow
    out = svg_open("Dindar Ahmed business card, Kurdish side")
    out += f"""<defs>
<linearGradient id="yellow" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="{Y1}"/><stop offset="1" stop-color="{Y4}"/>
</linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="url(#yellow)"/>
{line(SLOGAN_KU[0], s_slogan, 900, GR, b1, fg, rtl=True)}{line(SLOGAN_KU[1], s_slogan, 900, GR, b1 + step, accent, rtl=True)}{line(SLOGAN_KU[2], s_slogan, 900, GR, b1 + 2 * step, fg, rtl=True, tail=(".", accent))}{line(NAME_KU, t * 1.25, 700, GR, rows[1], fg, rtl=True)}{line(TITLE_KU, t * 1.1, 500, GR, rows[2], fg, rtl=True)}{line(PHONE, t, 500, GL, rows[0], fg)}{line(EMAIL, t, 500, GL, rows[1], fg)}{line(WEB, t, 500, GL, rows[2], fg)}</svg>
"""
    return out


def grid_guide():
    """the grid drawn over the artboard: columns, the small-text baselines, trim outlined"""
    g = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">']
    for i in range(COLS):
        g.append(f'<rect x="{col(i):.3f}" y="{GT}" width="{CW:.3f}" height="{GB - GT}" fill="#00c8ff" fill-opacity="0.16"/>')
    y = GB
    while y > GT:
        g.append(f'<path d="M{GL} {y:.3f}H{GR}" stroke="#ff3b8d" stroke-opacity="0.45" stroke-width="0.08"/>')
        y -= LEAD
    g.append(f'<rect x="{GL}" y="{GT}" width="{GR - GL}" height="{GB - GT}" fill="none" stroke="#ff3b8d" stroke-width="0.12"/>')
    g.append(f'<rect x="{BLEED}" y="{BLEED}" width="{W - 2 * BLEED}" height="{H - 2 * BLEED}" fill="none" stroke="#ffffff" stroke-width="0.15" stroke-dasharray="1 0.6"/>')
    g.append('</svg>')
    return "\n".join(g)


def print_page(front_svg, back_svg):
    """two pages at the full bleed size; Brave/Chrome prints this to card-print.pdf"""
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><title>Dindar Ahmed business card, print</title>
<style>
@page {{ size: {W}mm {H}mm; margin: 0; }}
html, body {{ margin: 0; padding: 0; }}
.page {{ width: {W}mm; height: {H}mm; overflow: hidden; page-break-after: always; break-after: page; }}
.page:last-child {{ page-break-after: auto; break-after: auto; }}
.page svg {{ display: block; width: {W}mm; height: {H}mm; }}
</style></head><body>
<div class="page">{front_svg}</div>
<div class="page">{back_svg}</div>
</body></html>
"""


SLUG = 6   # mm of white around the bleed on the crop-mark pages


def marks_svg():
    """crop marks at the four trim corners, outside the bleed: black hairlines, 1 mm clear of the bleed"""
    pw, ph = W + 2 * SLUG, H + 2 * SLUG
    x0, x1 = SLUG + BLEED, SLUG + W - BLEED          # trim edges on the page
    y0, y1 = SLUG + BLEED, SLUG + H - BLEED
    gap, ln = 1.0, 3.5                                 # clear of the bleed, mark length (mm)
    lines = []
    for y in (y0, y1):                                 # horizontal marks, left and right of the card
        lines.append(f'M{SLUG - gap - ln:.2f} {y}H{SLUG - gap:.2f}M{pw - SLUG + gap:.2f} {y}H{pw - SLUG + gap + ln:.2f}')
    for x in (x0, x1):                                 # vertical marks, above and below
        lines.append(f'M{x} {SLUG - gap - ln:.2f}V{SLUG - gap:.2f}M{x} {ph - SLUG + gap:.2f}V{ph - SLUG + gap + ln:.2f}')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {pw} {ph}" width="{pw}mm" height="{ph}mm" '
            f'style="position:absolute;left:0;top:0"><path d="{"".join(lines)}" fill="none" stroke="#000" stroke-width="0.09"/></svg>')


def print_page_marks(front_svg, back_svg):
    """two pages with crop marks: the card (with bleed) centred on a page 6 mm larger on every side"""
    pw, ph = W + 2 * SLUG, H + 2 * SLUG
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><title>Dindar Ahmed business card, print with crop marks</title>
<style>
@page {{ size: {pw}mm {ph}mm; margin: 0; }}
html, body {{ margin: 0; padding: 0; }}
.page {{ position: relative; width: {pw}mm; height: {ph}mm; overflow: hidden; page-break-after: always; break-after: page; }}
.page:last-child {{ page-break-after: auto; break-after: auto; }}
.card {{ position: absolute; left: {SLUG}mm; top: {SLUG}mm; width: {W}mm; height: {H}mm; }}
.card svg {{ display: block; width: {W}mm; height: {H}mm; }}
</style></head><body>
<div class="page"><div class="card">{front_svg}</div>{marks_svg()}</div>
<div class="page"><div class="card">{back_svg}</div>{marks_svg()}</div>
</body></html>
"""


if __name__ == "__main__":
    f, b = side_en(), side_ku()
    open(os.path.join(HERE, "front.svg"), "w", encoding="utf-8").write(f)
    open(os.path.join(HERE, "back.svg"), "w", encoding="utf-8").write(b)
    open(os.path.join(HERE, "grid.svg"), "w", encoding="utf-8").write(grid_guide())
    open(os.path.join(HERE, "print.html"), "w", encoding="utf-8").write(print_page(f, b))
    open(os.path.join(HERE, "print-marks.html"), "w", encoding="utf-8").write(print_page_marks(f, b))
    print(f"front.svg (English side), back.svg (Kurdish side), grid.svg, print pages written; small text {small_size():.2f} mm")
