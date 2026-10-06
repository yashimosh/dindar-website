#!/usr/bin/env python3
"""Make the print-ready package in FINAL/ from the pages build.py wrote.

One card for everyone (English side, Kurdish side):
  - *_print-ready.pdf     2 pages, 91 x 61 mm = 85 x 55 trim + 3 mm bleed, TrimBox/BleedBox set
  - *_with-crop-marks.pdf same, on a 103 x 73 mm page with crop marks
Checks: no embedded fonts (all text is outlines) and the page sizes.

Needs Brave or Chrome and poppler (pdfinfo, pdffonts). pypdf (sets TrimBox/BleedBox) is optional:
without it the PDFs are still made and the boxes are not set.
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "FINAL")
MM = 72 / 25.4
BLEED, SLUG, W, H = 3, 6, 91, 61
BROWSER = next((p for p in ("/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
                            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome") if os.path.exists(p)), None)
JOBS = [  # (source page, output name, has marks)
    ("print.html", "Dindar-Ahmed_business-card_print-ready.pdf", False),
    ("print-marks.html", "Dindar-Ahmed_business-card_with-crop-marks.pdf", True),
]


def to_pdf(src, dst):
    subprocess.run([BROWSER, "--headless=new", "--no-pdf-header-footer", "--virtual-time-budget=8000",
                    f"--print-to-pdf={dst}", f"file://{os.path.join(HERE, src)}"], check=True, capture_output=True)


def set_boxes(path, marks):
    try:
        from pypdf import PdfReader, PdfWriter
        from pypdf.generic import RectangleObject
    except ImportError:
        return False
    r, w = PdfReader(path), PdfWriter()
    off = SLUG if marks else 0
    pw, ph = (W + 2 * off) * MM, (H + 2 * off) * MM
    for page in r.pages:
        page.mediabox = RectangleObject((0, 0, pw, ph))
        page.bleedbox = RectangleObject((off * MM, off * MM, pw - off * MM, ph - off * MM))
        page.trimbox = RectangleObject(((off + BLEED) * MM, (off + BLEED) * MM, pw - (off + BLEED) * MM, ph - (off + BLEED) * MM))
        page.cropbox = page.mediabox
        w.add_page(page)
    w.add_metadata({"/Title": "Dindar Ahmed business card", "/Author": "Dindar Ahmed"})
    with open(path, "wb") as fh:
        w.write(fh)
    return True


if __name__ == "__main__":
    if not BROWSER:
        sys.exit("needs Brave or Chrome")
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT)
    for src, name, marks in JOBS:
        dst = os.path.join(OUT, name)
        to_pdf(src, dst)
        boxed = set_boxes(dst, marks)
        info = subprocess.run(["pdfinfo", "-box", dst], capture_output=True, text=True).stdout
        size = next(l for l in info.splitlines() if l.startswith("Page size")).split(":")[1].strip()
        fonts = subprocess.run(["pdffonts", dst], capture_output=True, text=True).stdout.strip().splitlines()[2:]
        print(f"{name}: {size}, {'boxes set' if boxed else 'boxes NOT set (no pypdf)'}, embedded fonts: {len(fonts)}")
    shutil.copyfile(os.path.join(HERE, "preview.png"), os.path.join(OUT, "Dindar-Ahmed_business-card_proof.png"))
    shutil.copyfile(os.path.join(HERE, "PRINTER-INSTRUCTIONS.md"), os.path.join(OUT, "PRINTER-INSTRUCTIONS.md"))   # the text lives next to this script
