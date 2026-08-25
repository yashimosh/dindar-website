/** Tailwind config — the design system for dindarahmed.com.
 *  Edit these tokens, then run:  npm run build:css
 */
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "on-secondary-fixed-variant": "#0035be",
        "secondary": "#0040e0",
        "on-secondary-container": "#efefff",
        "surface-bright": "#f7f9fc",
        "surface-container-high": "#e6e8eb",
        "tertiary-fixed-dim": "#ffb4a4",
        "surface-dim": "#d8dadd",
        "surface-variant": "#e0e3e6",
        "on-secondary-fixed": "#001356",
        "on-background": "#191c1e",
        "outline": "#747878",
        "inverse-on-surface": "#eff1f4",
        "on-tertiary-container": "#ec4a27",
        "surface-container-low": "#f2f4f7",
        "inverse-primary": "#c8c6c5",
        "secondary-fixed-dim": "#b8c3ff",
        "primary-container": "#1c1b1b",
        "error": "#ba1a1a",
        "secondary-fixed": "#dde1ff",
        "inverse-surface": "#2d3133",
        "tertiary-container": "#3d0600",
        "primary": "#000000",
        "on-tertiary-fixed-variant": "#8c1800",
        "outline-variant": "#c4c7c7",
        "primary-fixed-dim": "#c8c6c5",
        "error-container": "#ffdad6",
        "surface": "#f7f9fc",
        "on-primary-fixed-variant": "#474746",
        "on-error-container": "#93000a",
        "primary-fixed": "#e5e2e1",
        "on-primary-fixed": "#1c1b1b",
        "on-error": "#ffffff",
        "on-primary-container": "#858383",
        "surface-tint": "#5f5e5e",
        "surface-container-lowest": "#ffffff",
        "on-secondary": "#ffffff",
        "on-primary": "#ffffff",
        "on-tertiary-fixed": "#3d0600",
        "background": "#f7f9fc",
        "tertiary-fixed": "#ffdad3",
        "secondary-container": "#2e5bff",
        "on-surface": "#191c1e",
        "on-surface-variant": "#444748",
        "tertiary": "#000000",
        "surface-container-highest": "#e0e3e6",
        "on-tertiary": "#ffffff",
        "surface-container": "#eceef1"
      },
      borderRadius: {
        "DEFAULT": "0.25rem",
        "lg": "0.5rem",
        "xl": "0.75rem",
        "full": "9999px"
      },
      spacing: {
        "container-max": "1280px",
        "gutter": "24px",
        "margin-desktop": "64px",
        "margin-mobile": "20px",
        "unit": "8px"
      },
      fontFamily: {
        "headline-lg": ["Montserrat"],
        "headline-md": ["Montserrat"],
        "display-lg": ["Montserrat"],
        "headline-lg-mobile": ["Montserrat"],
        "body-lg": ["Inter"],
        "body-md": ["Inter"],
        "label-bold": ["Inter"]
      },
      fontSize: {
        "headline-lg": ["48px", { "lineHeight": "56px", "letterSpacing": "-0.01em", "fontWeight": "700" }],
        "headline-md": ["32px", { "lineHeight": "40px", "fontWeight": "600" }],
        "display-lg": ["72px", { "lineHeight": "80px", "letterSpacing": "-0.02em", "fontWeight": "800" }],
        "headline-lg-mobile": ["32px", { "lineHeight": "40px", "fontWeight": "700" }],
        "body-lg": ["18px", { "lineHeight": "28px", "fontWeight": "400" }],
        "body-md": ["16px", { "lineHeight": "24px", "fontWeight": "400" }],
        "label-bold": ["14px", { "lineHeight": "20px", "letterSpacing": "0.05em", "fontWeight": "600" }]
      }
    }
  }
}

module.exports.content = [
  "./index.html",
  "./404.html",
  "./fa/index.html",
  "./ku/index.html",
  "./ar/index.html",
  "./js/**/*.js"
];
