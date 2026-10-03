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
- Font: Noto Kufi Arabic for every language (English, Kurdish, Arabic, Persian;
  covers every Sorani letter). Loaded from Google Fonts.
- 29LT Bukra was requested but its licence forbids modifying the font and needs
  a separate 29LT web licence (WOFF files from 29LT) for any website use. If that
  licence is bought, swap the `font-family` in `css/tailwind.src.css` and `tailwind.config.js`.
- Behaviour: `js/scripts.js` (headline and scroll reveals, count-up numbers,
  mobile menu, click-to-load YouTube, client logos).

## Build and deploy

```bash
npm ci
```

```bash
npm run build
```

`build` regenerates `css/tailwind.css` and stamps a content hash on the CSS/JS
links in every page (`build.js`) so browsers never serve a stale copy. Add any
new page to the `PAGES` list in `build.js`.

```bash
npx wrangler pages deploy . --project-name dindar-ahmed --branch main
```

New pages also go in `sitemap.xml`.
