/** Tailwind config — the design system for dindarahmed.com.
 *  Edit these tokens, then run:  npm run build:css
 */
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        /* ---- Mithra-brand navy + amber, sampled from the actual
           Mithra Production logo (assets/img/hero.jpg). "secondary"
           (amber) is reserved for interactive fills — buttons, dots,
           decorative glows — never for small text, since bright amber
           can't clear 4.5:1 on a light background. Everywhere amber
           would otherwise be read as text, "primary" (navy ink) is
           used instead. See README for the contrast rationale. ---- */
        "on-secondary-fixed-variant": "#d99a2c",
        "secondary": "#f4ae37",
        "on-secondary-container": "#efefff",
        "surface-bright": "#f7f9fc",
        "surface-container-high": "#e7e2d8",
        "tertiary-fixed-dim": "#ffb4a4",
        "surface-dim": "#d8dadd",
        "surface-variant": "#e3ddd0",
        "on-secondary-fixed": "#001356",
        "on-background": "#242220",
        "outline": "#79746a",
        "inverse-on-surface": "#eff1f4",
        "on-tertiary-container": "#13294b",
        "surface-container-low": "#f1ede4",
        "inverse-primary": "#c8c6c5",
        "secondary-fixed-dim": "#b8c3ff",
        "primary-container": "#13294b",
        "error": "#ba1a1a",
        "secondary-fixed": "#dde1ff",
        "inverse-surface": "#2d3133",
        "tertiary-container": "#13294b",
        "primary": "#13294b",
        "on-tertiary-fixed-variant": "#13294b",
        "outline-variant": "#d9d3c6",
        "primary-fixed-dim": "#c8c6c5",
        "error-container": "#ffdad6",
        "surface": "#faf9f5",
        "on-primary-fixed-variant": "#474746",
        "on-error-container": "#93000a",
        "primary-fixed": "#e5e2e1",
        "on-primary-fixed": "#1c1b1b",
        "on-error": "#ffffff",
        "on-primary-container": "#858383",
        "surface-tint": "#5f5e5e",
        "surface-container-lowest": "#ffffff",
        "on-secondary": "#13294b",
        "on-primary": "#ffffff",
        "on-tertiary-fixed": "#3d0600",
        "background": "#faf9f5",
        "tertiary-fixed": "#ffdad3",
        "secondary-container": "#f4ae37",
        "on-surface": "#242220",
        "on-surface-variant": "#615c50",
        "tertiary": "#000000",
        "surface-container-highest": "#ded8c9",
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
        "headline-lg": ["IBM Plex Sans"],
        "headline-md": ["IBM Plex Sans"],
        "display-lg": ["IBM Plex Sans"],
        "headline-lg-mobile": ["IBM Plex Sans"],
        "body-lg": ["IBM Plex Sans"],
        "body-md": ["IBM Plex Sans"],
        "label-bold": ["IBM Plex Sans"]
      },
      fontSize: {
        "headline-lg": ["48px", { "lineHeight": "56px", "letterSpacing": "-0.01em", "fontWeight": "700" }],
        "headline-md": ["32px", { "lineHeight": "40px", "fontWeight": "600" }],
        "display-lg": ["72px", { "lineHeight": "80px", "letterSpacing": "-0.02em", "fontWeight": "700" }],
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
