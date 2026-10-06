#!/usr/bin/env python3
"""Draw the site icon: a black Kurdish "د" (Vazirmatn Black) on the brand yellow, as outlines.

Writes assets/favicon.svg (the editable source, open it in Illustrator or Figma),
and, when Brave/Chrome is available, the raster files made from it:
assets/favicon.ico (16, 32, 48), assets/apple-touch-icon.png (180),
assets/icon-192.png, assets/icon-512.png. Also copies favicon.ico to the site root,
where browsers look first.

Vazirmatn is free (SIL OFL, tools/fonts/free/); the letter is drawn as an outline so the icon needs no font.
Needs fonttools and Pillow (tools/requirements.txt).
"""
import os
import shutil
import subprocess
import sys
import tempfile

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
VARIABLE = os.path.join(ROOT, "tools", "fonts", "free", "Vazirmatn.ttf")
WEIGHT = 900
OUT = os.path.join(ROOT, "assets")
LETTER = "\u062f"   # د, the first letter of دیندار (try "D" for the Latin version)
Y1, Y2, INK = "#ffc300", "#ffea00", "#000000"
SIZE = 64            # viewBox
RADIUS = 14          # tile corner radius
LETTER_H = 46        # cap height of the letter inside the tile, same units
NUDGE = 0.0          # optical vertical nudge (down is positive)


def letter_path():
    from fontTools.varLib import instancer
    tt = instancer.instantiateVariableFont(TTFont(VARIABLE), {"wght": WEIGHT}, inplace=False)
    gs = tt.getGlyphSet()
    name = tt.getBestCmap()[ord(LETTER)]
    bp = BoundsPen(gs)
    gs[name].draw(bp)
    x0, y0, x1, y1 = bp.bounds
    k = LETTER_H / (y1 - y0)
    # centre the glyph's ink box in the tile; font y goes up, SVG y goes down
    tx = (SIZE - (x1 - x0) * k) / 2 - x0 * k
    ty = (SIZE + LETTER_H) / 2 + y0 * k + NUDGE
    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
    gs[name].draw(TransformPen(pen, (k, 0, 0, -k, tx, ty)))
    return pen.getCommands()


def svg(rounded=True):
    r = RADIUS if rounded else 0
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}" width="{SIZE}" height="{SIZE}">\n'
            f'<title>Dindar Ahmed</title>\n'
            f'<defs><linearGradient id="y" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{Y1}"/><stop offset="1" stop-color="{Y2}"/></linearGradient></defs>\n'
            f'<rect width="{SIZE}" height="{SIZE}" rx="{r}" fill="url(#y)"/>\n'
            f'<path fill="{INK}" d="{letter_path()}"/>\n</svg>\n')


def browser():
    for p in ("/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"):
        if os.path.exists(p):
            return p
    return shutil.which("chromium") or shutil.which("google-chrome")


def render(svg_text, px, path, transparent):
    """Rasterise one SVG with headless Chrome/Brave at px x px."""
    html = (f'<!doctype html><meta charset="utf-8"><style>html,body{{margin:0;background:transparent}}'
            f'svg{{display:block;width:{px}px;height:{px}px}}</style>{svg_text}')
    with tempfile.TemporaryDirectory() as d:
        page = os.path.join(d, "i.html")
        open(page, "w", encoding="utf-8").write(html)
        args = [browser(), "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={px},{px}",
                f"--screenshot={path}", "--virtual-time-budget=2000"]
        if transparent:
            args.append("--default-background-color=00000000")
        subprocess.run(args + [f"file://{page}"], check=True, capture_output=True)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8").write(svg(True))
    print("assets/favicon.svg written")
    if not browser():
        sys.exit("no Brave/Chrome found: SVG written, PNG and ICO skipped")
    from PIL import Image
    big = os.path.join(OUT, "icon-512.png")
    render(svg(True), 512, big, True)
    render(svg(False), 180, os.path.join(OUT, "apple-touch-icon.png"), False)  # iOS rounds it itself
    render(svg(True), 192, os.path.join(OUT, "icon-192.png"), True)
    im = Image.open(big).convert("RGBA")
    ico = os.path.join(OUT, "favicon.ico")
    im.save(ico, sizes=[(16, 16), (32, 32), (48, 48)])
    shutil.copyfile(ico, os.path.join(ROOT, "favicon.ico"))
    print("favicon.ico (16/32/48), apple-touch-icon.png, icon-192.png, icon-512.png written")
