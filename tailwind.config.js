/** Tailwind config: the design system for dindarahmed.com.
 *  Edit these tokens, then run:  npm run build:css
 *
 *  Monochrome system: near-black ink on white, a gray ramp for
 *  secondary text, hairline borders. Geist for Latin pages,
 *  IBM Plex Sans Arabic for the RTL pages (see css/tailwind.src.css).
 */
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./*.html", "./{about,work}/*.html", "./{ku,ar,fa}/**/*.html", "./js/*.js"],
  theme: {
    extend: {
      colors: {
        ink: "#111111",        // headings, body, active nav
        muted: "#6a7282",      // secondary text (4.8:1 on white)
        faint: "#99a1af",      // large display text only (email, numbers)
        emph: "#8b8b8b",       // gray words inside the hero headline
        line: "#f3f4f6",       // section rules, footer ground
        card: "#e5e7eb",       // card borders
      },
      fontFamily: {
        sans: ["Geist", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      maxWidth: {
        site: "1440px",
      },
    },
  },
  plugins: [],
};
