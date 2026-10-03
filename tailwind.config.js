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
        // TEST PALETTE (branch palette-violet-yellow), refined roles:
        //   deep violet  #1c1550  ground + text on yellow (white on it 15:1)
        //   violet       #7161ef  accent blocks, glows
        //   lavender     #957fef  secondary text (5:1 on deep), hairlines
        //   school bus   #ffc300  main accent (buttons)
        //   sunbeam      #ffea00  highlights; bright amber / gold are gradient steps
        // Token names kept from the fire palette so no markup changes.
        ink: "#1c1550",
        deep: "#1c1550",
        violet: "#7161ef",
        lavender: "#957fef",
        night: "#7161ef",
        cherry: "#7161ef",
        oxblood: "#7161ef",
        brick: "#7161ef",
        ochre: "#ffc300",
        cayenne: "#ffc300",
        saffron: "#ffd000",
        orange: "#ffdd00",
        amber: "#ffea00",
        accent: "#ffea00",
        dark: "#1c1550",
        muted: "#957fef",
        faint: "rgb(149 127 239 / 0.75)",
        line: "rgb(149 127 239 / 0.22)",
        card: "rgb(149 127 239 / 0.40)",
        edge: "rgb(149 127 239 / 0.40)",
      },
      // Tailwind's own fallbacks (blue ring, grey border) pointed at the palette
      borderColor: { DEFAULT: "rgb(149 127 239 / 0.40)" },
      ringColor: { DEFAULT: "#ffea00" },
      fontFamily: {
        sans: ["Noto Kufi Arabic", "Tahoma", "sans-serif"],
        display: ["Noto Kufi Arabic", "Tahoma", "sans-serif"],
      },
    },
  },
  plugins: [],
};
