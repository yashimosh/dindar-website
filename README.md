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
- Fonts: **Inter** for Latin and **Vazirmatn** for Arabic script (Kurdish Sorani,
  Arabic, Persian). Both are free under the SIL Open Font License 1.1 with no
  Reserved Font Name, so they are self-hosted: the sources live in
  `tools/fonts/free/` (with their licences) and `tools/fonts/make_webfonts.py`
  subsets them into `assets/fonts/inter.woff2` (Latin) and
  `assets/fonts/vazirmatn.woff2` (Arabic script), each with its full 100-900 weight
  axis. The `@font-face` rules in `css/tailwind.src.css` use matching
  `unicode-range`s, and each page lists its own script's font first (English:
  Inter, then Vazirmatn; Kurdish/Arabic/Persian: the reverse) and preloads it.
- Vazirmatn covers every Sorani letter (ڕ ڵ ە ۆ ێ ڤ گ چ ژ پ). Kufam, Alexandria,
  Cairo, Reem Kufi and Readex Pro were tested and rejected (missing letters or broken
  Kurdish joining).
- The big footer name is sized to fill its row: `generate.py` measures it with
  HarfBuzz in the real font and writes `--fit` (see `.fit` in the CSS).
- Audit: `tools/site/audit_clipping.js` finds cropped or cut text; run every page
  and width with `tools/site/audit_all.js` (copy `audit_clipping.js` to
  `assets/audit.js` temporarily, run `audit_all.js` in the browser console on the
  dev server, delete the copy before committing). It should return `{}`.
- Icon: a black Vazirmatn Black Kurdish "د" (first letter of دیندار) on the brand yellow. `assets/favicon.svg` is the editable
  source (outlined, open it in Illustrator or Figma); `tools/site/make_favicon.py`
  redraws it and makes `favicon.ico` (16/32/48, also copied to the site root),
  `apple-touch-icon.png` and `icon-192/512.png`.
- Behaviour: `js/scripts.js` (headline and scroll reveals, count-up numbers,
  mobile menu, click-to-load YouTube, client logos).

## Build and deploy

```bash
npm ci
```

Regenerate the pages (and, after changing a font, `tools/venv/bin/python tools/fonts/make_webfonts.py`):

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
ignores `.assetsignore`, so deploying the repo root would publish `tools/`
(build scripts, source fonts, and the 29LT files kept locally for other work).
The script stages only the public site and refuses to run if any `.ttf`/`.otf`
or tool file is in it; the woff2 webfonts in `assets/fonts/` are deployed.

New pages also go in `sitemap.xml`.
