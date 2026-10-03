/** Tailwind config: the design system for dindarahmed.com.
 *  Edit these tokens, then run:  npm run build:css
 *
 *  Ink on white for reading sections, near-black bands for rhythm,
 *  and one acid-lime accent. The accent is only ever used as text on
 *  dark grounds, or as a fill with ink text on top (it is too light
 *  to read as text on white). Change it here and everything follows.
 *  Fonts: Archivo Expanded for display type, Geist for text,
 *  IBM Plex Sans Arabic on the RTL pages (see css/tailwind.src.css).
 */
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./*.html", "./{about,work}/*.html", "./{ku,ar,fa}/**/*.html", "./js/*.js"],
  theme: {
    extend: {
      colors: {
        ink: "#111111",        // text on light
        dark: "#141414",       // dark bands, footer
        accent: "#c5f04a",     // signal colour (fills, text on dark only)
        muted: "#6a7282",      // secondary text on light (4.8:1)
        faint: "#99a1af",      // large display text only
        line: "#f3f4f6",       // light rules and grounds
        card: "#e5e7eb",       // card borders
        edge: "#2a2a2a",       // rules on dark
      },
      fontFamily: {
        sans: ["Geist", "ui-sans-serif", "system-ui", "sans-serif"],
        display: ["Archivo", "Geist", "sans-serif"],
      },
    },
  },
  plugins: [],
};
