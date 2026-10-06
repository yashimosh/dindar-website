#!/usr/bin/env python3
"""Builds Dindar Ahmed's business card: front.svg (English), front-ku.svg
(Kurdish), back.svg (bilingual) and the print pages.

The SVGs are the source of truth; open and edit them in Illustrator or
Figma. All text is set in 29LT Zawi (extended with the Sorani letters, see
tools/fonts/extend_zawi.py) and drawn as outlines, so no font has to be
installed and no font file is ever handed to the printer (the 29Letters
licence forbids redistributing the fonts). To change wording, edit the
details below and run this script; text in the SVGs is shapes, not live type.

Needs: tools/venv with tools/requirements.txt (segno, uharfbuzz, fonttools)
and the built fonts in tools/fonts/dist.
Card: 85 x 55 mm trim, 3 mm bleed (91 x 61 mm artboard), 4 mm safe zone.

Layout rule: one grid, few elements, lots of empty black. Everything
hangs off the safe-zone corners (left 7, right 84, top 7, bottom 54 mm)
and the middle of each side is left clear on purpose.
"""
import os
import sys
import segno

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "fonts"))
from shape_svg import shape_to_path  # noqa: E402

DIST = os.path.join(ROOT, "tools", "fonts", "dist")
ZAWI = {w: os.path.join(DIST, f"29LT_Zawi_KU_{n}.ttf") for w, n in
        {400: "Regular", 700: "Bold", 900: "Black"}.items()}

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- details (single place to edit) ----
NAME_EN = "DINDAR AHMED"
NAME_KU = "دیندار ئەحمەد"
TITLE_EN = "MARKETING MANAGER AND CONSULTANT"
TITLE_KU = "بەڕێوەبەر و ڕاوێژکاری مارکێتینگ"   # as in the website's page title
PHONE = "+964 771 992 2486"
EMAIL = "Dindar.Ahmed@mithra.agency"
WEB = "dindarahmed.com"
# the website's Kurdish headline, split the same way as the English one
STATEMENT_KU = ("پێم بڵێ", "چی", "نافرۆشرێت")
QR_DATA = "https://dindarahmed.com"     # the site carries WhatsApp, Instagram, LinkedIn

# ---- palette (same as the website) ----
BLACK, VIOLET, LAVENDER = "#000000", "#7161ef", "#957fef"
Y1, Y4 = "#ffc300", "#ffea00"
WHITE = "#ffffff"
SOFT = "#e6e6e6"   # white at 90%, as a flat colour (safer in Illustrator and for print)

W, H, BLEED, SAFE = 91, 61, 3, 4
L, R = BLEED + SAFE, W - BLEED - SAFE          # 7 .. 84 mm
T, B = BLEED + SAFE, H - BLEED - SAFE          # 7 .. 54 mm

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


def front():
    """black field; name small in the top corner, the statement small in the
    bottom corner, everything between left empty"""
    size, step = 5.4, 6.0
    s = svg_open("Dindar Ahmed business card, front")
    s += f"""<defs>
<radialGradient id="glow" cx="1" cy="0" r="0.9">
<stop offset="0" stop-color="{VIOLET}" stop-opacity="0.38"/>
<stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
</radialGradient>
<linearGradient id="yellow" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="{Y1}"/><stop offset="1" stop-color="{Y4}"/>
</linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="{BLACK}"/>
<rect width="{W}" height="{H}" fill="url(#glow)"/>
{line(NAME_EN, 1.7, 700, L, T + 1.6, SOFT, tracking=0.55)}{line("TELL ME", size, 900, L, B - 2 * step, WHITE, tracking=-0.12)}{line("WHAT ISN'T", size, 900, L, B - step, "url(#yellow)", tracking=-0.12)}{line("SELLING", size, 900, L, B, WHITE, tracking=-0.12, tail=(".", Y1))}</svg>
"""
    return s


def front_ku():
    """Kurdish front: the English layout mirrored for right-to-left reading.
    Name small top-right, the website's Kurdish line bottom-right, glow top-left.
    Arabic-script letters run taller and deeper than Latin capitals, so the
    lines are spaced wider and the last baseline sits a little higher to keep
    descenders inside the safe zone."""
    size, step, base = 5.6, 7.4, B - 1.4
    s = svg_open("Dindar Ahmed business card, Kurdish front")
    s += f"""<defs>
<radialGradient id="glow" cx="0" cy="0" r="0.9">
<stop offset="0" stop-color="{VIOLET}" stop-opacity="0.38"/>
<stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
</radialGradient>
<linearGradient id="yellow" x1="1" y1="0" x2="0" y2="0">
<stop offset="0" stop-color="{Y1}"/><stop offset="1" stop-color="{Y4}"/>
</linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="{BLACK}"/>
<rect width="{W}" height="{H}" fill="url(#glow)"/>
{line(NAME_KU, 2.3, 700, R, T + 2.4, SOFT, rtl=True)}{line(TITLE_KU, 1.9, 700, R, T + 6.6, LAVENDER, rtl=True)}{line(STATEMENT_KU[0], size, 900, R, base - 2 * step, WHITE, rtl=True)}{line(STATEMENT_KU[1], size, 900, R, base - step, "url(#yellow)", rtl=True)}{line(STATEMENT_KU[2], size, 900, R, base, WHITE, rtl=True, tail=(".", Y1))}</svg>
"""
    return s


def qr_path(size_mm, x0, y0, quiet=2):
    """QR as one black path inside a yellow tile, for crisp print"""
    qr = segno.make(QR_DATA, error="m", boost_error=False, micro=False)
    rows = [list(r) for r in qr.matrix]
    n = len(rows)
    cell = size_mm / (n + 2 * quiet)
    d = []
    for yy, row in enumerate(rows):
        xx = 0
        while xx < n:
            if row[xx]:
                start = xx
                while xx < n and row[xx]:
                    xx += 1
                d.append(f"M{x0 + (start + quiet) * cell:.3f} {y0 + (yy + quiet) * cell:.3f}h{(xx - start) * cell:.3f}v{cell:.3f}h{-(xx - start) * cell:.3f}z")
            else:
                xx += 1
    return "".join(d), qr.version, n, cell


def back():
    """identity top-left, contacts bottom-left, QR bottom-right, clear middle"""
    qs = 14.5
    qx, qy = R - qs, B - qs
    path, version, n, cell = qr_path(qs, qx, qy)
    lines = [PHONE, EMAIL, WEB]
    step = 3.9
    contact = "".join(line(v, 2.15, 400, L, B - (len(lines) - 1 - k) * step, SOFT) for k, v in enumerate(lines))
    s = svg_open("Dindar Ahmed business card, back")
    s += f"""<rect width="{W}" height="{H}" fill="{BLACK}"/>
{line(NAME_EN, 4.6, 900, L, T + 3.9, WHITE, tracking=-0.05)}{line(NAME_KU, 2.7, 700, L, T + 9.1, LAVENDER, rtl=True, anchor_left=True)}{line(TITLE_EN, 1.55, 700, L, T + 13.4, Y1, tracking=0.45)}{line(TITLE_KU, 2.0, 700, L, T + 17.9, Y1, rtl=True, anchor_left=True)}{contact}<rect x="{qx}" y="{qy}" width="{qs}" height="{qs}" rx="0.8" fill="{Y4}"/>
<path d="{path}" fill="{BLACK}"/>
</svg>
"""
    return s, version, n, cell


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
    f = front()
    open(os.path.join(HERE, "front.svg"), "w", encoding="utf-8").write(f)
    fk = front_ku()
    open(os.path.join(HERE, "front-ku.svg"), "w", encoding="utf-8").write(fk)
    b, version, n, cell = back()
    open(os.path.join(HERE, "back.svg"), "w", encoding="utf-8").write(b)
    open(os.path.join(HERE, "print.html"), "w", encoding="utf-8").write(print_page(f, b))
    open(os.path.join(HERE, "print-ku.html"), "w", encoding="utf-8").write(print_page(fk, b))
    open(os.path.join(HERE, "print-marks.html"), "w", encoding="utf-8").write(print_page_marks(f, b))
    open(os.path.join(HERE, "print-ku-marks.html"), "w", encoding="utf-8").write(print_page_marks(fk, b))
    print(f"front.svg, front-ku.svg, back.svg, print.html, print-ku.html written. QR version {version}, {n}x{n} modules, module {cell:.3f} mm")
