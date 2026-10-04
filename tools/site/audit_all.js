// Runs audit_clipping.js on every page at phone, tablet and desktop widths, using hidden same-origin
// frames, and returns a summary. Needs the dev server running and audit_clipping.js reachable at
// /assets/audit.js (copy it there temporarily; do not commit that copy).
(async () => {
  const js = await (await fetch("/assets/audit.js?" + Date.now())).text();
  const pages = ["/", "/about/", "/work/", "/ku/", "/ku/about/", "/ku/work/", "/ar/", "/ar/about/", "/ar/work/", "/fa/", "/fa/about/", "/fa/work/", "/404.html"];
  const widths = [375, 768, 1440];
  const report = {};
  for (const w of widths) {
    for (const p of pages) {
      const f = document.createElement("iframe");
      f.style.cssText = `position:fixed;left:0;top:0;width:${w}px;height:900px;opacity:0;pointer-events:none;border:0`;
      document.body.appendChild(f);
      await new Promise((res) => { f.onload = res; f.src = p; });
      try { await f.contentDocument.fonts.ready; } catch (e) {}
      await new Promise((r) => setTimeout(r, 500));
      const out = f.contentWindow.eval(js);
      if (out.length) report[`${p} @${w}`] = out.slice(0, 12).map((o) => `${o.text} | ${o.by} | dx${o.dx} dy${o.dy}`);
      f.remove();
    }
  }
  return report;
})();
