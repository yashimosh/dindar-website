# Dindar Ahmed — website

Plain HTML/CSS/JS. No build step, no framework, no Claude dependency —
open any `index.html` in a text editor and edit it directly.

Template base: [Start Bootstrap "Agency"](https://startbootstrap.com/theme/agency)
(MIT licensed, free for commercial use).

## Structure

```
index.html      English (default, site root)
fa/index.html   Persian
ku/index.html   Kurdish (Sorani)
ar/index.html   Arabic
css/styles.css  shared theme (from the template, untouched)
css/rtl.css     small overrides for the fa/ku/ar (right-to-left) pages
js/scripts.js   shared theme JS
assets/         shared images/icons — reused across all 4 languages
```

Each language is a full, independent HTML file — there's no templating
engine. To change a sentence, open that language's `index.html` and edit
the text in place.

## Before this goes live — please review

1. **Translations.** The Kurdish `about` text is Dindar's own original
   bio (pulled from his beacons.ai page). The English is written fresh
   from that bio. **The Persian and Arabic pages are AI-translated
   drafts** — have Dindar or a native speaker read them over before
   publishing; tone/idiom in a couple of spots may want adjusting.
2. **"Areas of Work" / "Work" section.** There's no real case-study
   data yet, so that grid is placeholder — generic marketing categories
   (Social Media Campaigns, Paid Advertising, etc.) with stock photos,
   not real client work. Swap in actual campaigns when you have them
   (image path: `assets/img/portfolio/1.jpg` through `6.jpg`, one per
   language file, same filenames referenced in each).
3. **Contact section.** It's a plain `mailto:` link to
   `Dindar.Ahmed@mithra.agency` — works with zero setup, but it's not a
   form with validation/spam-filtering. If you want a real contact
   form later, the two easy no-backend options are Cloudflare Pages
   Functions or a free [Formspree](https://formspree.io) endpoint.
4. **Headshot photo.** The hero currently uses a generic stock flat-lay
   image (`assets/img/header-bg.jpg`) — swap in a real photo of Dindar
   if you have one.

## Deploying to Cloudflare Pages (domain already in your account)

Easiest path, no GitHub required:

1. Cloudflare dashboard → **Workers & Pages** → **Create** → **Pages** →
   **Upload assets**.
2. Drag this whole folder in (or zip it first — either works).
3. Give the project a name, deploy.
4. **Workers & Pages** → your project → **Custom domains** → add the
   domain you already own in this Cloudflare account. Cloudflare wires
   the DNS automatically since it's in the same account.

Every time you edit a file locally, re-upload via the same **Upload
assets** flow (or connect a GitHub repo instead, if you'd rather push
to deploy — Cloudflare Pages supports both).
