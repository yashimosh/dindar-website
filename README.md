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

- **Home:** headline, featured TVC, info + numbers, core expertise, case study
  preview, client logo marquee, contact footer.
- **Work:** approach, case studies, campaigns (YouTube), reels (Instagram).
- **About:** belief, info, quote, experience, certificates, in the field
  (photos), clients by category.

The same sentence lives in up to 4 files (one per language). Change all four
when you change one.

## Client logos: one file

All client logos on every page and in every language come from
`assets/data/clients.json`. To add a logo:

1. Put a 256x256 PNG in `assets/img/clients/<category>/`.
2. Add `{"name": "Brand", "file": "<category>/<file>.png"}` to that category in
   `clients.json`. List order is display order.

Category names, subtitles and alt text for all four languages are in the same
file. No HTML edit is needed.

## Design system

- Tokens (colours, font, widths): `tailwind.config.js`
- Shared CSS (headline reveal, image shimmer, marquee, RTL font): `css/tailwind.src.css`
- `css/tailwind.css` is generated. Do not edit it.
- Fonts: Geist (English), IBM Plex Sans Arabic (Kurdish, Arabic, Persian).
- Behaviour: `js/scripts.js` (headline reveal, scroll
  reveal, mobile menu, click-to-load YouTube, client logos).

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
