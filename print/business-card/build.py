#!/usr/bin/env python3
"""Builds Dindar Ahmed's business card: front.svg (bilingual), back.svg (bilingual),
the print pages and a grid guide. One card for everyone: English and Kurdish side by side.

The SVGs are the source of truth; open and edit them in Illustrator or
Figma. All text is set in 29LT Zawi (extended with the Sorani letters, see
tools/fonts/extend_zawi.py) and drawn as outlines, so no font has to be
installed and no font file is ever handed to the printer (the 29Letters
licence forbids redistributing the fonts). To change wording, edit the
details below and run this script; text in the SVGs is shapes, not live type.

Needs: tools/venv with tools/requirements.txt (segno, uharfbuzz, fonttools)
and the built fonts in tools/fonts/dist.
Card: 85 x 55 mm trim, 3 mm bleed (91 x 61 mm artboard).

LAYOUT: a Swiss modular grid, 6 columns x 4 rows, on a live area inset 7 mm from the sides and
6 mm from top and bottom of the trim (so everything is at least 6 mm inside the cut), 3 mm gutters.
  - flush-left English hangs from the left margin, flush-right Kurdish from the right margin
  - top and bottom margins are the two baselines everything is set on
  - the back's text blocks hang from the margin and row lines; the QR is exactly two rows tall and sits on the
    bottom-right corner of the grid
  - one size scale, a few weights, no decoration except one hairline rule
python3 build.py also writes grid.svg, the grid drawn over the card, for checking.
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

W, H, BLEED = 91, 61, 3

# ---- the grid (all values in mm on the 91 x 61 artboard; trim starts at BLEED) ----
MX, MY, GUT = 7.0, 6.0, 3.0           # side margin, top/bottom margin, gutter
COLS, ROWS = 6, 4
GL, GR = BLEED + MX, W - BLEED - MX    # live area left / right edge  (10 .. 81)
GT, GB = BLEED + MY, H - BLEED - MY    # live area top / bottom edge  (9 .. 52)
CW = (GR - GL - (COLS - 1) * GUT) / COLS   # column width
RH = (GB - GT - (ROWS - 1) * GUT) / ROWS   # row height


def col(i):
    """left edge of column i (0-based)"""
    return GL + i * (CW + GUT)


def row(j):
    """top edge of row j (0-based)"""
    return GT + j * (RH + GUT)


CAP = 0.70   # cap height of Zawi in em, to hang caps from a line

# type scale (mm): small caps, text, KU name on the back, slogan / name
XS, S, M, XL = 1.6, 2.2, 2.8, 4.7
KU_OPTICAL = 1.04   # Arabic script reads smaller than Latin at the same size

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
    """English slogan flush left, Kurdish slogan flush right, both on the same three baselines that end on the
    bottom margin; each name on the top margin line; one hairline under the header row."""
    step = 6.6                                   # baseline step, shared by both languages
    b1, b2, b3 = GB - 2 * step, GB - step, GB
    top = GT + CAP * XS                          # cap-top of the small name sits on the top margin
    rule = row(0) + RH + GUT / 2                 # hairline between header row and the rest
    sk = XL * KU_OPTICAL
    s = svg_open("Dindar Ahmed business card, front")
    s += f"""<defs>
<radialGradient id="glow" cx="0.5" cy="0" r="0.8">
<stop offset="0" stop-color="{VIOLET}" stop-opacity="0.32"/>
<stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
</radialGradient>
<linearGradient id="yellow" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="{Y1}"/><stop offset="1" stop-color="{Y4}"/>
</linearGradient>
<linearGradient id="yellowk" x1="1" y1="0" x2="0" y2="0">
<stop offset="0" stop-color="{Y1}"/><stop offset="1" stop-color="{Y4}"/>
</linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="{BLACK}"/>
<rect width="{W}" height="{H}" fill="url(#glow)"/>
{line(NAME_EN, XS, 700, GL, top, SOFT, tracking=0.5)}{line(NAME_KU, S, 700, GR, top, SOFT, rtl=True)}<path d="M{GL} {rule:.3f}H{GR}" stroke="{WHITE}" stroke-opacity="0.22" stroke-width="0.12" fill="none"/>
{line("TELL ME", XL, 900, GL, b1, WHITE, tracking=-0.1)}{line("WHAT ISN'T", XL, 900, GL, b2, "url(#yellow)", tracking=-0.1)}{line("SELLING", XL, 900, GL, b3, WHITE, tracking=-0.1, tail=(".", Y1))}{line(STATEMENT_KU[0], sk, 900, GR, b1, WHITE, rtl=True)}{line(STATEMENT_KU[1], sk, 900, GR, b2, "url(#yellowk)", rtl=True)}{line(STATEMENT_KU[2], sk, 900, GR, b3, WHITE, rtl=True, tail=(".", Y1))}</svg>
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
    """names and titles hang from the top and from row 1; contacts end on the bottom margin with their first
    cap-line on row 3; the QR is two rows tall and fills the bottom-right corner of the grid."""
    qs = 2 * RH + GUT                            # two rows tall (20 mm)
    qx, qy = GR - qs, GB - qs                    # right margin, bottom margin; its top lands on row 2
    path, version, n, cell = qr_path(qs, qx, qy)
    lines = [PHONE, EMAIL, WEB]
    first = row(3) + CAP * S                     # first contact line: cap-top on row 3
    step = (GB - first) / (len(lines) - 1)       # last line on the bottom margin
    contact = "".join(line(v, S, 400, GL, first + k * step, SOFT) for k, v in enumerate(lines))
    ty = row(1) + GUT + CAP * XS                 # titles hang one gutter below row 1, clear of the names above
    s = svg_open("Dindar Ahmed business card, back")
    s += f"""<rect width="{W}" height="{H}" fill="{BLACK}"/>
{line(NAME_EN, XL, 900, GL, GT + CAP * XL, WHITE, tracking=-0.05)}{line(NAME_KU, M, 700, GL, GT + CAP * XL + 6.0, LAVENDER, rtl=True, anchor_left=True)}{line(TITLE_EN, XS, 700, GL, ty, Y1, tracking=0.45)}{line(TITLE_KU, S, 700, GL, ty + 4.6, Y1, rtl=True, anchor_left=True)}{contact}<rect x="{qx:.3f}" y="{qy:.3f}" width="{qs:.3f}" height="{qs:.3f}" rx="0.8" fill="{Y4}"/>
<path d="{path}" fill="{BLACK}"/>
</svg>
"""
    return s, version, n, cell


def grid_guide():
    """the grid drawn over the artboard: columns cyan, rows magenta, trim and live area outlined"""
    g = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">']
    for i in range(COLS):
        g.append(f'<rect x="{col(i):.3f}" y="{GT}" width="{CW:.3f}" height="{GB - GT}" fill="#00c8ff" fill-opacity="0.16"/>')
    for j in range(ROWS):
        g.append(f'<rect x="{GL}" y="{row(j):.3f}" width="{GR - GL}" height="{RH:.3f}" fill="#ff3b8d" fill-opacity="0.13"/>')
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
    f = front()
    open(os.path.join(HERE, "front.svg"), "w", encoding="utf-8").write(f)
    b, version, n, cell = back()
    open(os.path.join(HERE, "back.svg"), "w", encoding="utf-8").write(b)
    open(os.path.join(HERE, "grid.svg"), "w", encoding="utf-8").write(grid_guide())
    open(os.path.join(HERE, "print.html"), "w", encoding="utf-8").write(print_page(f, b))
    open(os.path.join(HERE, "print-marks.html"), "w", encoding="utf-8").write(print_page_marks(f, b))
    print(f"front.svg, back.svg, grid.svg, print.html, print-marks.html written. QR version {version}, {n}x{n} modules, module {cell:.3f} mm")
