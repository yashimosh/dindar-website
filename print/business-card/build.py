#!/usr/bin/env python3
"""Builds Dindar Ahmed's business card: front.svg and back.svg.

The SVGs are the source of truth; open and edit them in Illustrator or
Figma (install fonts/NotoKufiArabic[wght].ttf first). This script only
exists to regenerate them, mainly the QR code, if the details change.

Needs: pip install segno==1.6.1
Card: 85 x 55 mm trim, 3 mm bleed (91 x 61 mm artboard), 4 mm safe zone.
"""
import os
import segno

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- details (single place to edit) ----
NAME_EN = "DINDAR AHMED"
NAME_KU = "دیندار ئەحمەد"
TITLE_EN = "MARKETING MANAGER AND CONSULTANT"
TITLE_KU = "بەڕێوەبەری مارکێتینگ و ڕاوێژکار"
PHONE = "+964 771 992 2486"
EMAIL = "Dindar.Ahmed@mithra.agency"
WEB = "dindarahmed.com"
INSTAGRAM = "@dindar_ahmad"
# kept short on purpose: every extra field makes the QR denser and harder
# to scan once printed small (aim for modules of 0.45 mm or more)
VCARD = "\n".join([
    "BEGIN:VCARD", "VERSION:3.0",
    "N:Ahmed;Dindar", "FN:Dindar Ahmed",
    "TEL:+9647719922486", "EMAIL:Dindar.Ahmed@mithra.agency",
    "URL:https://dindarahmed.com", "END:VCARD",
])

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
    s = svg_open("Dindar Ahmed business card, front")
    s += f"""<defs>
<radialGradient id="glow" cx="0.08" cy="1.05" r="0.75">
<stop offset="0" stop-color="{VIOLET}" stop-opacity="0.85"/>
<stop offset="0.55" stop-color="{VIOLET}" stop-opacity="0.18"/>
<stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
</radialGradient>
<linearGradient id="yellow" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="{Y1}"/><stop offset="1" stop-color="{Y4}"/>
</linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="{BLACK}"/>
<rect width="{W}" height="{H}" fill="url(#glow)"/>
<g font-weight="900" font-size="12.2" letter-spacing="-0.3">
<text x="{L}" y="18.6" fill="{WHITE}">TELL ME</text>
<text x="{L}" y="31.2" fill="url(#yellow)">WHAT ISN'T</text>
<text x="{L}" y="43.8" fill="{WHITE}">SELLING<tspan fill="{Y1}">.</tspan></text>
</g>
<g font-size="2.3" letter-spacing="0.45">
<path d="M{L + 0.8} {B - 1.95} l0.8 0.8 l-0.8 0.8 l-0.8 -0.8 z" fill="{Y1}"/>
<text x="{L + 2.6}" y="{B - 0.3}" fill="{WHITE}" font-weight="700">{NAME_EN}</text>
<text x="{R}" y="{B - 0.3}" fill="{LAVENDER}" font-weight="600" text-anchor="end">{WEB.upper()}</text>
</g>
</svg>
"""
    return s


def qr_path(size_mm, x0, y0, quiet=2):
    """QR as one black path inside a yellow tile, for crisp print"""
    qr = segno.make(VCARD, error="l", boost_error=False, micro=False)
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
    qx, qy, qs = 61, 22.5, 23
    path, version, n, cell = qr_path(qs, qx, qy)
    rows = [("WHATSAPP", PHONE, True), ("EMAIL", EMAIL, True), ("WEB", WEB, True), ("INSTAGRAM", INSTAGRAM, True)]
    y = 37.2
    contact = ""
    for label, value, ltr in rows:
        contact += (f'<text x="{L}" y="{y:.1f}" font-size="1.75" font-weight="700" letter-spacing="0.35" fill="{Y1}">{label}</text>'
                    f'<text x="{L + 15.5}" y="{y:.1f}" font-size="2.3" font-weight="500" fill="{WHITE}">{value}</text>\n')
        y += 4.6
    s = svg_open("Dindar Ahmed business card, back")
    s += f"""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="{VIOLET}"/>
<stop offset="0.45" stop-color="{VIOLET}" stop-opacity="0.25"/>
<stop offset="0.8" stop-color="{BLACK}" stop-opacity="0"/>
</linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="{BLACK}"/>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<text x="{L}" y="14.6" font-size="6.2" font-weight="900" letter-spacing="-0.1" fill="{WHITE}">{NAME_EN}</text>
<text x="{L}" y="20.6" font-size="3.6" font-weight="700" fill="{Y4}" direction="rtl" unicode-bidi="embed" text-anchor="end">{NAME_KU}</text>
<text x="{L}" y="25.6" font-size="1.85" font-weight="700" letter-spacing="0.38" fill="{WHITE}" fill-opacity="0.85">{TITLE_EN}</text>
<text x="{L}" y="29.6" font-size="2.4" font-weight="500" fill="{WHITE}" fill-opacity="0.85" direction="rtl" unicode-bidi="embed" text-anchor="end">{TITLE_KU}</text>
{contact}<rect x="{qx}" y="{qy}" width="{qs}" height="{qs}" rx="1.2" fill="{Y4}"/>
<path d="{path}" fill="{BLACK}"/>
<text x="{qx + qs / 2}" y="{qy + qs + 3.2}" font-size="1.6" font-weight="700" letter-spacing="0.3" fill="{LAVENDER}" text-anchor="middle">SCAN TO SAVE CONTACT</text>
</svg>
"""
    return s, version, n, cell


def print_page(front_svg, back_svg):
    """two pages at the full bleed size; Brave/Chrome prints this to card-print.pdf"""
    body = lambda svg: svg.split("\n", 1)[1] if svg.startswith("<?xml") else svg
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><title>Dindar Ahmed business card, print</title>
<style>
@page {{ size: {W}mm {H}mm; margin: 0; }}
html, body {{ margin: 0; padding: 0; }}
.page {{ width: {W}mm; height: {H}mm; overflow: hidden; page-break-after: always; break-after: page; }}
.page:last-child {{ page-break-after: auto; break-after: auto; }}
.page svg {{ display: block; width: {W}mm; height: {H}mm; }}
</style></head><body>
<div class="page">{body(front_svg)}</div>
<div class="page">{body(back_svg)}</div>
</body></html>
"""


if __name__ == "__main__":
    f = front()
    open(os.path.join(HERE, "front.svg"), "w", encoding="utf-8").write(f)
    b, version, n, cell = back()
    open(os.path.join(HERE, "back.svg"), "w", encoding="utf-8").write(b)
    open(os.path.join(HERE, "print.html"), "w", encoding="utf-8").write(print_page(f, b))
    print(f"front.svg, back.svg, print.html written. QR version {version}, {n}x{n} modules, module {cell:.3f} mm")
