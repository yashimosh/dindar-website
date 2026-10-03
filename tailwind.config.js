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
        // TEST PALETTE (branch palette-violet-yellow): two violets, four yellows.
        // Token names kept from the fire palette so no markup changes.
        ink: "#7161ef",        // violet: page ground, text on yellow fills
        night: "#957fef",      // lavender
        cherry: "#957fef",
        oxblood: "#957fef",
        brick: "#957fef",
        ochre: "#ffc300",      // school bus yellow
        cayenne: "#ffc300",
        saffron: "#ffd000",    // bright amber
        orange: "#ffdd00",     // bright gold
        amber: "#ffea00",      // sunbeam yellow
        accent: "#ffea00",
        dark: "#7161ef",
        // white is the only text colour that clears 4.5:1 on the violet,
        // so secondary text stays near-solid white
        muted: "rgb(255 255 255 / 0.9)",
        faint: "rgb(255 255 255 / 0.7)",
        line: "rgb(255 234 0 / 0.22)",
        card: "rgb(255 234 0 / 0.35)",
        edge: "rgb(255 234 0 / 0.35)",
      },
      // Tailwind's own fallbacks (blue ring, grey border) pointed at the palette
      borderColor: { DEFAULT: "rgb(255 234 0 / 0.35)" },
      ringColor: { DEFAULT: "#ffea00" },
      fontFamily: {
        sans: ["Noto Kufi Arabic", "Tahoma", "sans-serif"],
        display: ["Noto Kufi Arabic", "Tahoma", "sans-serif"],
      },
    },
  },
  plugins: [],
};
