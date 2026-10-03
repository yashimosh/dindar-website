/** Tailwind config: the design system for dindarahmed.com.
 *  Edit these tokens, then run:  npm run build:css
 *
 *  Fire palette on ink black: dark grounds, ember-to-amber gradients,
 *  frosted glass panels and blurred glows (see css/tailwind.src.css).
 *  Font: Noto Kufi Arabic for every language (Latin, Arabic, Persian,
 *  Kurdish Sorani).
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
        // neutrals: only white text over the palette, plus amber-flame
        // hairlines. No greys or blues of their own.
        muted: "rgb(255 255 255 / 0.68)",  // secondary text (8:1 on ink)
        faint: "rgb(255 255 255 / 0.45)",
        line: "rgb(255 186 8 / 0.10)",     // hairlines (amber flame)
        card: "rgb(255 186 8 / 0.18)",     // card borders (amber flame)
        edge: "rgb(255 186 8 / 0.18)",
      },
      // Tailwind's own fallbacks (blue ring, grey border) pointed at the palette
      borderColor: { DEFAULT: "rgb(255 186 8 / 0.18)" },
      ringColor: { DEFAULT: "#ffba08" },
      fontFamily: {
        sans: ["Noto Kufi Arabic", "Tahoma", "sans-serif"],
        display: ["Noto Kufi Arabic", "Tahoma", "sans-serif"],
      },
    },
  },
  plugins: [],
};
