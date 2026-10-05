# Dindar Ahmed website

Plain HTML, one Tailwind stylesheet, one small JS file. No framework, no
templating engine: open any `index.html` in a text editor and edit the text
in place.

Live: https://dindarahmed.com (Cloudflare Pages project `dindar-ahmed`).

## Structure

Three pages in four languages, each a full, independent HTML file:

| Page  | English            | Kurdish (Sorani)      | Arabic                | Persian               |
|-------|--------------------|-----------------------|-----------------------|-----------------------|
| Home  | `index.html`       | `ku/index.html`       | `ar/index.html`       | `fa/index.html`       |
| Work  | `work/index.html`  | `ku/work/index.html`  | `ar/work/index.html`  | `fa/work/index.html`  |
| About | `about/index.html` | `ku/about/index.html` | `ar/about/index.html` | `fa/about/index.html` |

`404.html` is the not-found page.

- **Home:** full-screen hero, services ticker, statement, featured TVC, numbers
  band, core expertise rows, case studies, client logo marquee, tagline ticker.
- **Work:** approach, case studies, campaigns (YouTube), reels (Instagram).
- **About:** belief, portrait + info, quote, experience, certificates, in the
  field (photos), clients by category.

The same sentence lives in up to 4 files (one per language). Change all four
when you change one.

## Client logos: one file

All client logos on every page and in every language come from
`assets/data/clients.json`. To add a logo:

1. Put a 256x256 image in `assets/img/clients/<category>/`. WebP keeps the page
   light (the current logos are WebP); PNG also works.
2. Add `{"name": "Brand", "file": "<category>/<file>.webp"}` to that category in
   `clients.json`. List order is display order.

Category names, subtitles and alt text for all four languages are in the same
file. No HTML edit is needed.

## Design system

- Palette: black ground and black text on yellow; bright violet `#7161ef`
  (gradients into black, glows); lavender `#957fef` (secondary text, hairlines);
  yellows `#ffc300` `#ffd000` `#ffdd00` `#ffea00` (buttons, highlights, numbers
  band). Values live in `tailwind.config.js` and `css/tailwind.src.css`. Token
  names (`ink`, `amber`, `night`...) are left over from an earlier fire palette;
  the comments in the config say what each one holds now.
- Shared CSS: `css/tailwind.src.css`. Gradients (`.fire`, `.fire-text`,
  `.btn-fire`, `.band-fire`, `.hi`), violet-to-black section gradients
  (`.grad-down`, `.grad-up`, `.grad-diag`), soft glows (`.orb`), headline reveal,
  marquees, service rows, RTL font rules. Layout follows lircle.co: square
  corners, flat ruled rows, solid fills, no frosted glass.
- `css/tailwind.css` is generated. Do not edit it.
- Fonts: **all text on the site is 29LT Zawi** (headlines, labels, buttons, menus,
  numbers and running paragraphs), drawn as inline SVG outlines at build time so no
  font file is ever served. No Google Fonts or other font request is made. The real
  text is kept next to each shape as `.sr-only`, so screen readers, search and
  translation still work. Zawi has no ◆, so that is a drawn SVG diamond (`.dia`).
- 29Letters licence (confirmed in writing by 29Letters): the fonts may be
  modified and used in any medium, but **never redistributed**. This repo is
  public, so no font file is ever committed (`.gitignore`: `tools/fonts/src*`,
  `tools/fonts/dist`, `*.ttf`, `*.otf`) and none is deployed. Only SVG paths
  made from them are published.
- Zawi (and UA Neo) lack five Sorani letters (ڕ ڵ ە ۆ ێ).
  `tools/fonts/extend_zawi.py` / `extend_uaneo.py` add them (base letter plus a
  drawn "small V" mark, with joining and the ڵ+ا ligature) into `tools/fonts/dist/`.
  Source fonts go in `tools/fonts/src_zawi_var/` (Zawi variable) and
  `tools/fonts/src/` (UA Neo); get them from 29LT.
- Build chain: `tools/site/generate.py` writes the pages, then
  `tools/site/display_svg.py` swaps every visible text node for SVG word shapes
  (HarfBuzz shaping, glyph overlaps merged, bidi handled for Latin/number runs and
  e-mail/phone tokens in RTL; unique words drawn once in a sprite with compact
  relative path data). Weights: Black for display headings, Bold for
  `font-semibold/bold`, Regular for the rest. Without `tools/fonts/dist` it leaves
  plain text and prints a WARNING (the page then uses the system font).
- Audit: `tools/site/audit_clipping.js` finds cropped or cut text; run every page
  and width with `tools/site/audit_all.js` (copy `audit_clipping.js` to
  `assets/audit.js` temporarily, run `audit_all.js` in the browser console on the
  dev server, delete the copy before committing). It should return `{}`.
- Icon: a black Zawi Kurdish "د" (first letter of دیندار) on the brand yellow. `assets/favicon.svg` is the editable
  source (outlined, open it in Illustrator or Figma); `tools/site/make_favicon.py`
  redraws it and makes `favicon.ico` (16/32/48, also copied to the site root),
  `apple-touch-icon.png` and `icon-192/512.png`.
- Behaviour: `js/scripts.js` (headline and scroll reveals, count-up numbers,
  mobile menu, click-to-load YouTube, client logos).

## Build and deploy

```bash
npm ci
```

Regenerate the pages (needs the extended fonts in `tools/fonts/dist`):

```bash
python3 -m venv tools/venv && tools/venv/bin/pip install -r tools/requirements.txt
```

```bash
tools/venv/bin/python tools/site/generate.py
```

```bash
npm run build
```

`build` regenerates `css/tailwind.css` and stamps a content hash on the CSS/JS
links in every page (`build.js`) so browsers never serve a stale copy. Add any
new page to the `PAGES` list in `build.js`.

```bash
tools/deploy.sh
```

Always deploy with `tools/deploy.sh`, never `wrangler pages deploy .`: Pages
ignores `.assetsignore`, so deploying the repo root would publish `tools/` and
the licensed 29LT font files. The script stages only the public site and refuses
to run if any font or tool file is in it.

New pages also go in `sitemap.xml`.
