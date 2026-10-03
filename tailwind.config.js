/** Tailwind config: the design system for dindarahmed.com.
 *  Edit these tokens, then run:  npm run build:css
 *
 *  Fire palette on ink black: dark grounds, ember-to-amber gradients,
 *  frosted glass panels and blurred glows (see css/tailwind.src.css).
 *  Fonts: Archivo Expanded for big Latin headlines, Geist for Latin
 *  text, Noto Kufi Arabic for all Kurdish, Arabic and Persian text.
 */
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./*.html", "./{about,work}/*.html", "./{ku,ar,fa}/**/*.html", "./js/*.js"],
  theme: {
    extend: {
      colors: {
        // the palette, darkest to brightest
        ink: "#03071e",        // ink black: page ground, text on bright fills
        night: "#370617",      // night bordeaux
        cherry: "#6a040f",     // black cherry
        oxblood: "#9d0208",
        brick: "#d00000",      // brick ember
        ochre: "#dc2f02",      // red ochre
        cayenne: "#e85d04",    // cayenne red
        saffron: "#f48c06",    // deep saffron
        orange: "#faa307",
        amber: "#ffba08",      // amber flame
        // roles
        accent: "#ffba08",                 // small highlights on dark
        dark: "#03071e",
        muted: "#a7a9be",                  // secondary text on ink (7:1)
        faint: "#6e7191",
        line: "rgb(255 255 255 / 0.08)",   // hairlines, faint grounds
        card: "rgb(255 255 255 / 0.14)",   // card and glass borders
        edge: "rgb(255 255 255 / 0.14)",
      },
      fontFamily: {
        sans: ["Geist", "ui-sans-serif", "system-ui", "sans-serif"],
        display: ["Archivo", "Geist", "sans-serif"],
      },
    },
  },
  plugins: [],
};
