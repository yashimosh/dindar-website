# Dindar Ahmed business card

One card for everyone: English and Kurdish side by side on the front, bilingual back. Printed once, both sides.

| File | What it is |
|---|---|
| `FINAL/` | **The print-ready package for the printer**: PDF with bleed (TrimBox/BleedBox set), the same with crop marks, a proof image and `PRINTER-INSTRUCTIONS.md`. Made by `make_final.py`. |
| `front.svg`, `back.svg` | The editable design. Open in Illustrator or Figma. All text is 29LT Zawi drawn as outlines (no font to install). |
| `grid.svg` | The grid drawn over the artboard, for checking alignment (open `preview.html?grid` to see it on the card). |
| `preview.png`, `preview.html` | Both sides, cut to the trim, for a quick look. |
| `build.py` | Regenerates the SVGs, `grid.svg` and the print pages. Edit the details at its top (names, titles, phone, e-mail, slogan) and run it. |
| `make_final.py` | Turns the print pages into the PDFs in `FINAL/` and checks them. |
| `PRINTER-INSTRUCTIONS.md` | The text that goes to the printer (copied into `FINAL/`). |
| `fonts/` | Noto Kufi Arabic, no longer used by the card (kept for reference; SIL OFL, see `OFL.txt`). |

## The grid (Swiss modular grid)

Everything sits on one grid, defined at the top of `build.py`:

- Live area: inset **7 mm from the sides** and **6 mm from the top and bottom** of the trim.
- **6 columns x 4 rows**, **3 mm gutters** (column 9.33 mm, row 8.5 mm).
- Flush-left English hangs from the left margin, flush-right Kurdish from the right margin.
- The bottom margin is the baseline of the slogans (English and Kurdish share three baselines) and of the last contact line. The top margin is the cap line of the names.
- Back: the QR is exactly two rows tall (20 mm) and fills the bottom-right corner; the contact block's first cap line sits on row 3; the titles hang one gutter under the row-1 line.
- Type scale (mm): 1.6, 2.2, 2.8, 4.7. Weights: Black for the slogan and the name, Bold for names and titles, Medium-light Regular for contacts. One hairline rule under the header row on the front. The Kurdish slogan is set 4% larger than the English one because Arabic script reads smaller at the same size.

Change a margin, the gutter or the column count in `build.py` and everything re-flows to the new grid.

## Print spec

- Size: 85 x 55 mm trimmed. Artboard and PDF are 91 x 61 mm: 3 mm bleed on every side.
- All text and the QR are at least 6 mm inside the trim (a few Kurdish tails come within 4.5 mm).
- Colours are RGB from the website palette: black, violet `#7161ef`, lavender `#957fef`, yellows `#ffc300` to `#ffea00`. Ask the printer to convert to CMYK and send a proof: bright violet and sunbeam yellow shift a little in CMYK.
- Suggested stock: 400 gsm or heavier, matte or soft-touch lamination. A spot UV or foil on the yellow "WHAT ISN'T" line is the place to spend extra if budget allows.
- If the printer uses 90 x 50 mm cards instead, the layout needs a small redesign, not just a resize.
- The QR opens https://dindarahmed.com, where WhatsApp, Instagram and LinkedIn are one tap away. Its modules are 0.69 mm, so it scans easily.

## Editing

- All text is outlined Zawi (extended with the Sorani letters), so nothing needs installing and the PDFs embed no fonts. The 29Letters licence allows using and modifying the fonts but not handing the files to anyone, which is why only outlines go to the printer. Never send `tools/fonts/` to the printer. Layers are named (`aria-label`) after the text they draw.
- Because the text is shapes, change wording in the details at the top of `build.py` and run it; editing the SVG text directly is not possible.
- Run it with `tools/venv/bin/python build.py` (needs `tools/requirements.txt` installed and the extended fonts in `tools/fonts/dist`, see the main README).
- PDF check: `make_final.py` needs Brave or Chrome and poppler; with `pypdf` and `opencv-python-headless` it also sets TrimBox/BleedBox and verifies the QR decodes to the site (both optional).
