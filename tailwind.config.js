/** Tailwind config: the design system for dindarahmed.com.
 *  Edit these tokens, then run:  npm run build:css
 *
 *  Fire palette on ink black: dark grounds, ember-to-amber gradients,
 *  frosted glass panels and blurred glows (see css/tailwind.src.css).
 *  Font: all text is 29LT Zawi drawn as SVG outlines at build time
 *  (tools/site/display_svg.py); the families below are only a fallback.
 */
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./*.html", "./{about,work}/*.html", "./{ku,ar,fa}/**/*.html", "./js/*.js"],
  theme: {
    extend: {
      colors: {
        // TEST PALETTE (branch palette-violet-yellow), roles:
        //   black        #000000  ground + text on yellow
        //   violet       #7161ef  gradients into black (.grad-*), glows
        //   lavender     #957fef  secondary text (5:1 on deep), hairlines
        //   school bus   #ffc300  main accent (buttons)
        //   sunbeam      #ffea00  highlights; bright amber / gold are gradient steps
        // Token names kept from the fire palette so no markup changes.
        ink: "#000000",        // black: page ground
        deep: "#000000",       // black: text on yellow
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
        dark: "#000000",
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
