# Dindar Ahmed business card

| File | What it is |
|---|---|
| `FINAL/` | **The print-ready package for the printer**: EN and KU PDFs (bleed, boxes set), the same with crop marks, a proof image and `PRINTER-INSTRUCTIONS.md`. Made by `make_final.py`. |
| `front.svg`, `front-ku.svg`, `back.svg` | The editable design: English front, Kurdish front, bilingual back. Open in Illustrator or Figma. All text is 29LT Zawi drawn as outlines (no font to install). |
| `card-print.pdf` | English card for the printer. 2 pages: front, back. |
| `card-print-ku.pdf` | Kurdish card for the printer. 2 pages: Kurdish front, the same back. |
| `front.png`, `front-ku.png`, `back.png` | 600 dpi images of each side, cut to size (for sharing, mockups). |
| `preview.png`, `preview.html` | Both sides side by side, for a quick look. |
| `fonts/` | Noto Kufi Arabic, no longer used by the card (kept for reference; free, SIL OFL, see `OFL.txt`). |
| `build.py`, `print.html`, `print-ku.html` | Regenerate the SVGs and the PDFs (only needed if details change). |

## Layout

One grid, few elements, a lot of empty black. Everything hangs off the safe-zone
corners (7 mm in from the cut on every side) and the middle of each side is left
clear on purpose:

- Front: name small top-left; "Tell me what isn't selling." in the bottom-left
  corner; a faint violet glow in the empty top-right.
- Kurdish front: the same layout mirrored for right-to-left reading: Kurdish name
  small top-right, "پێم بڵێ / چی / فرۆشی نییە." bottom-right, glow top-left.
  Arabic-script lines are spaced a little wider than the English ones.
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

- All text is outlined 29LT Zawi (extended with the Sorani letters), so nothing needs
  installing and the PDFs embed no fonts. The 29Letters licence allows using and
  modifying the fonts but not handing the files to anyone, which is why only outlines
  go to the printer. Never send `tools/fonts/` to the printer. Layers are named
  (`aria-label`) after the text they draw.
- Because the text is shapes, change wording in the details at the top of `build.py`
  and run it; editing the SVG text directly is not possible. Weights used: Regular
  (contacts), Bold (name, labels), Black (headlines).
- Run it with `tools/venv/bin/python build.py` (needs `tools/requirements.txt` installed
  and the extended fonts in `tools/fonts/dist`, see the main README). It is also the
  easiest way to change the QR code.
- The QR code opens https://dindarahmed.com, where WhatsApp, Instagram and LinkedIn
  are one tap away. A plain web address keeps the code small and coarse (25 x 25
  modules, 0.5 mm each at 14.5 mm), so it scans easily. It was checked to decode.
- PDF from `print.html`:
  `"/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" --headless=new --no-pdf-header-footer --virtual-time-budget=8000 --print-to-pdf=card-print.pdf print.html`
  (Chrome works the same way.) For the Kurdish card use `print-ku.html` and
  `card-print-ku.pdf`.
- Printing both: most printers can split one order across two front designs with the
  same back; otherwise order them as two jobs.

## Final print files

`build.py` writes the pages, then `make_final.py` prints them to `FINAL/`, sets TrimBox/BleedBox, checks that
no fonts are embedded and that the QR on the back still decodes to the site. Run it with Python that has
`pypdf` and `opencv-python-headless` (both optional; without them those two steps are skipped).
