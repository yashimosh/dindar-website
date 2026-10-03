#!/usr/bin/env python3
"""Builds Dindar Ahmed's business card: front.svg (English), front-ku.svg
(Kurdish), back.svg (bilingual) and the print pages.

The SVGs are the source of truth; open and edit them in Illustrator or
Figma (install fonts/NotoKufiArabic[wght].ttf first). This script only
exists to regenerate them, mainly the QR code, if the details change.

Needs: pip install segno==1.6.1
Card: 85 x 55 mm trim, 3 mm bleed (91 x 61 mm artboard), 4 mm safe zone.

Layout rule: one grid, few elements, lots of empty black. Everything
hangs off the safe-zone corners (left 7, right 84, top 7, bottom 54 mm)
and the middle of each side is left clear on purpose.
"""
import os
import segno

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- details (single place to edit) ----
NAME_EN = "DINDAR AHMED"
NAME_KU = "دیندار ئەحمەد"
TITLE_EN = "MARKETING MANAGER AND CONSULTANT"
PHONE = "+964 771 992 2486"
EMAIL = "Dindar.Ahmed@mithra.agency"
WEB = "dindarahmed.com"
# the website's Kurdish headline, split the same way as the English one
STATEMENT_KU = ("پێم بڵێ", "چی", "فرۆشی نییە")
QR_DATA = "https://dindarahmed.com"     # the site carries WhatsApp, Instagram, LinkedIn

# ---- palette (same as the website) ----
BLACK, VIOLET, LAVENDER = "#000000", "#7161ef", "#957fef"
Y1, Y4 = "#ffc300", "#ffea00"
WHITE = "#ffffff"

W, H, BLEED, SAFE = 91, 61, 3, 4
L, R = BLEED + SAFE, W - BLEED - SAFE          # 7 .. 84 mm
T, B = BLEED + SAFE, H - BLEED - SAFE          # 7 .. 54 mm

FONT = """<style>
@font-face { font-family: "Noto Kufi Arabic"; src: url("fonts/NotoKufiArabic[wght].ttf") format("truetype"); font-weight: 100 900; }
text { font-family: "Noto Kufi Arabic", sans-serif; }
</style>"""


def svg_open(title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">\n'
            f'<title>{title}</title>\n{FONT}\n')


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
<text x="{L}" y="{T + 1.6}" font-size="1.7" font-weight="700" letter-spacing="0.55" fill="{WHITE}" fill-opacity="0.9">{NAME_EN}</text>
<g font-weight="900" font-size="{size}" letter-spacing="-0.12">
<text x="{L}" y="{B - 2 * step:.2f}" fill="{WHITE}">TELL ME</text>
<text x="{L}" y="{B - step:.2f}" fill="url(#yellow)">WHAT ISN'T</text>
<text x="{L}" y="{B:.2f}" fill="{WHITE}">SELLING<tspan fill="{Y1}">.</tspan></text>
</g>
</svg>
"""
    return s


def front_ku():
    """Kurdish front: the English layout mirrored for right-to-left reading.
    Name small top-right, the website's Kurdish line bottom-right, glow top-left.
    Arabic-script letters run taller and deeper than Latin capitals, so the
    lines are spaced wider and the last baseline sits a little higher to keep
    descenders inside the safe zone."""
    size, step, base = 5.6, 7.4, B - 1.4
    rtl = 'direction="rtl" unicode-bidi="embed" text-anchor="start"'
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
<text x="{R}" y="{T + 2.4}" font-size="2.3" font-weight="700" fill="{WHITE}" fill-opacity="0.9" {rtl}>{NAME_KU}</text>
<g font-weight="900" font-size="{size}">
<text x="{R}" y="{base - 2 * step:.2f}" fill="{WHITE}" {rtl}>{STATEMENT_KU[0]}</text>
<text x="{R}" y="{base - step:.2f}" fill="url(#yellow)" {rtl}>{STATEMENT_KU[1]}</text>
<text x="{R}" y="{base:.2f}" fill="{WHITE}" {rtl}>{STATEMENT_KU[2]}<tspan fill="{Y1}">.</tspan></text>
</g>
</svg>
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
    contact = "".join(
        f'<text x="{L}" y="{B - (len(lines) - 1 - k) * step:.2f}" font-size="2.15" font-weight="500" fill="{WHITE}" fill-opacity="0.9">{v}</text>\n'
        for k, v in enumerate(lines))
    s = svg_open("Dindar Ahmed business card, back")
    s += f"""<rect width="{W}" height="{H}" fill="{BLACK}"/>
<text x="{L}" y="{T + 3.9}" font-size="4.6" font-weight="900" letter-spacing="-0.05" fill="{WHITE}">{NAME_EN}</text>
<text x="{L}" y="{T + 9.1}" font-size="2.7" font-weight="700" fill="{LAVENDER}" direction="rtl" unicode-bidi="embed" text-anchor="end">{NAME_KU}</text>
<text x="{L}" y="{T + 13.4}" font-size="1.55" font-weight="700" letter-spacing="0.45" fill="{Y1}">{TITLE_EN}</text>
{contact}<rect x="{qx}" y="{qy}" width="{qs}" height="{qs}" rx="0.8" fill="{Y4}"/>
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


if __name__ == "__main__":
    f = front()
    open(os.path.join(HERE, "front.svg"), "w", encoding="utf-8").write(f)
    fk = front_ku()
    open(os.path.join(HERE, "front-ku.svg"), "w", encoding="utf-8").write(fk)
    b, version, n, cell = back()
    open(os.path.join(HERE, "back.svg"), "w", encoding="utf-8").write(b)
    open(os.path.join(HERE, "print.html"), "w", encoding="utf-8").write(print_page(f, b))
    open(os.path.join(HERE, "print-ku.html"), "w", encoding="utf-8").write(print_page(fk, b))
    print(f"front.svg, front-ku.svg, back.svg, print.html, print-ku.html written. QR version {version}, {n}x{n} modules, module {cell:.3f} mm")
