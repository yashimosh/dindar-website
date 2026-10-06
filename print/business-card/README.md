# Dindar Ahmed business card

One card for everyone, printed both sides: **one side per language**, each complete on its own. English side black, Kurdish side brand yellow.

| File | What it is |
|---|---|
| `FINAL/` | **The print-ready package for the printer**: PDF with bleed (TrimBox/BleedBox set), the same with crop marks, a proof image and `PRINTER-INSTRUCTIONS.md`. Made by `make_final.py`. |
| `front.svg`, `back.svg` | The editable design: English side, Kurdish side. Open in Illustrator or Figma. Latin text is Inter, Kurdish is Vazirmatn (free, SIL OFL; same fonts as the website), drawn as outlines (no font to install). |
| `grid.svg` | The grid drawn over the artboard, for checking alignment (open `preview.html?grid` to see it on the card). |
| `preview.png`, `preview.html` | Both sides, cut to the trim, for a quick look. |
| `build.py` | Regenerates the SVGs, `grid.svg` and the print pages. Edit the details at its top (names, titles, phone, e-mail, slogans) and run it. |
| `make_final.py` | Turns the print pages into the PDFs in `FINAL/` and checks them. |
| `PRINTER-INSTRUCTIONS.md` | The text that goes to the printer (copied into `FINAL/`). |

## The grid (Swiss)

Defined at the top of `build.py`; every size and position is derived from it:

- Live area **6 mm inside the trim on all four sides**, **6 columns**, **3 mm gutters**.
- A **3.2 mm baseline grid** for the small text; the bottom margin is its last baseline.
- Each side has one dominant element, the slogan, and one information band:
  - **Slogan**: hangs from the top margin by its real ink (the Kurdish V marks touch the margin, not the cut). The English one is sized so its longest line spans exactly **4 columns**; the Kurdish one gets the **same letter height**, made smaller only if it would come within one gutter of the information band.
  - **Information band**: three baselines ending on the bottom margin. English side: name and title in columns 1-3, contacts in columns 4-6. Kurdish side mirrored: name and title flush right in columns 4-6, contacts (left to right) in columns 1-3.
- One size for all small text (the e-mail fills three columns, at most 2.2 mm); the name is 15-25% larger.
- Colours: English side black with the website's violet glow, yellow accent line. Kurdish side brand yellow, black type, a deeper violet accent (`#4b3bd0`) for contrast on yellow.

Change the margin, gutter, columns or baseline step in `build.py` and the whole card re-flows.

## Print spec

- Size: 85 x 55 mm trimmed. Artboard and PDF are 91 x 61 mm: 3 mm bleed on every side.
- All ink is at least 6 mm inside the trim.
- Colours are RGB from the website palette: black, violet `#7161ef`, lavender `#957fef`, yellows `#ffc300` to `#ffea00`. Ask the printer to convert to CMYK and send a proof: bright violet and sunbeam yellow shift a little in CMYK.
- Suggested stock: 400 gsm or heavier, matte or soft-touch lamination. A spot UV or foil on the yellow "WHAT ISN'T" line is the place to spend extra if budget allows.
- If the printer uses 90 x 50 mm cards instead, the layout needs a small redesign, not just a resize.

## Editing

- All text is outlined Inter and Vazirmatn (in `tools/fonts/free/`, SIL OFL), so the printer needs no fonts and the PDFs embed none. `build.py` makes fixed-weight instances of the two variable fonts into `tools/fonts/free/build/` the first time it runs.
- Because the text is shapes, change wording in the details at the top of `build.py` and run it; editing the SVG text directly is not possible.
- Run it with `tools/venv/bin/python build.py` (needs `tools/requirements.txt` installed and the extended fonts in `tools/fonts/dist`, see the main README).
- PDF check: `make_final.py` needs Brave or Chrome and poppler; with `pypdf` it also sets TrimBox/BleedBox (optional).
