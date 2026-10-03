# Dindar Ahmed business card

| File | What it is |
|---|---|
| `front.svg`, `back.svg` | The editable design. Open in Illustrator or Figma. |
| `card-print.pdf` | Send this to the printer. 2 pages: front, back. |
| `front.png`, `back.png` | 600 dpi images of each side, cut to size (for sharing, mockups). |
| `preview.png`, `preview.html` | Both sides side by side, for a quick look. |
| `fonts/` | Noto Kufi Arabic (free, SIL Open Font License, see `OFL.txt`). |
| `build.py`, `print.html` | Regenerate the SVGs and the PDF (only needed if details change). |

## Layout

One grid, few elements, a lot of empty black. Everything hangs off the safe-zone
corners (7 mm in from the cut on every side) and the middle of each side is left
clear on purpose:

- Front: name small top-left; "Tell me what isn't selling." in the bottom-left
  corner; a faint violet glow in the empty top-right.
- Back: identity block top-left (name, Kurdish name, title); phone, email and
  website bottom-left; QR bottom-right, its bottom edge level with the last line.

Keep that empty space when editing. Adding lines or enlarging type is what made
the first version feel crowded.

## Print spec

- Size: 85 x 55 mm trimmed. Artboard and PDF are 91 x 61 mm: 3 mm bleed on every side.
- Keep text inside the 4 mm safe zone (everything already is).
- Colours are RGB from the website palette: black, violet `#7161ef`, lavender
  `#957fef`, yellows `#ffc300` to `#ffea00`. Ask the printer to convert to CMYK and
  send a proof: bright violet and sunbeam yellow shift a little in CMYK.
- Suggested stock: 400 gsm or heavier, matte or soft-touch lamination. A spot UV or
  foil on the yellow "WHAT ISN'T" line is the place to spend extra if budget allows.
- If the printer uses 90 x 50 mm cards instead, the layout needs a small redesign,
  not just a resize.

## Editing

- Install `fonts/NotoKufiArabic[wght].ttf` first, otherwise Illustrator substitutes
  another font. Weights used: 500, 600, 700, 900.
- Change text directly in the SVGs, or edit the details at the top of `build.py` and
  run it (`pip install segno==1.6.1`, then `python build.py`). The script is the
  easiest way to change the QR code.
- The QR code opens https://dindarahmed.com, where WhatsApp, Instagram and LinkedIn
  are one tap away. A plain web address keeps the code small and coarse (25 x 25
  modules, 0.5 mm each at 14.5 mm), so it scans easily. It was checked to decode.
- PDF from `print.html`:
  `"/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" --headless=new --no-pdf-header-footer --virtual-time-budget=8000 --print-to-pdf=card-print.pdf print.html`
  (Chrome works the same way.)
