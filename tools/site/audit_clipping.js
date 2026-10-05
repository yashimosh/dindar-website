// Run in the browser console (or via the preview tools) on a built page.
// Reports text that is cut off by a clipping ancestor (overflow hidden/clip/auto),
// or that runs past the right/left edge of the page. Marquees clip on purpose and
// are ignored. Returns [] when nothing is cropped.
(() => {
  document.documentElement.style.scrollBehavior = "auto";
  document.querySelectorAll(".rv,.reveal").forEach((e) => e.classList.add("in"));
  // measure the finished layout: no pending reveal animations (they freeze in hidden tabs)
  if (!document.getElementById("audit-style")) {
    const st = document.createElement("style");
    st.id = "audit-style";
    st.textContent = ".hl>span,.rv{transform:none!important;opacity:1!important}*{transition:none!important;animation:none!important}";
    document.head.appendChild(st);
  }
  const out = [];
  const clips = (el) => {
    const cs = getComputedStyle(el);
    return [cs.overflowX, cs.overflowY].some((v) => v !== "visible");
  };
  const items = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const n = walker.currentNode;
    const t = n.textContent.trim();
    if (!t) continue;
    const pe = n.parentElement;
    if (!pe || pe.closest(".sr-only, script, style, svg, [hidden], .kw-line > .sr-only")) continue;
    if (pe.closest("svg")) continue;
    const r = document.createRange();
    r.selectNodeContents(n);
    for (const b of r.getClientRects()) if (b.width > 0 && b.height > 0) items.push([pe, b, t.slice(0, 32), 0]);
  }
  document.querySelectorAll("svg.kw").forEach((s) => {
    const fs = parseFloat(getComputedStyle(s).fontSize) || 16;
    const b = s.getBoundingClientRect();
    if (!b.width || !b.height) return;
    // the V marks and tall letters reach about 0.2em above the glyph box
    const label = (s.closest(".kw-line")?.querySelector(".sr-only")?.textContent || "").trim().slice(0, 32);
    // the drawing box is 1.2 em above / .62 em below the baseline so nothing is ever shaved off, but
    // ordinary ink only reaches about .9 em above and .45 em below: test that, V marks get 0.2em more
    const ink = { top: b.top + 0.3 * fs, bottom: b.bottom - 0.17 * fs, left: b.left, right: b.right, width: b.width, height: b.height };
    items.push([s, ink, label, fs * 0.2]);
  });
  for (const [el, b, label, lift] of items) {
    if (el.closest(".marquee, .wa")) continue; // marquee and the WhatsApp hover label clip on purpose
    const top = b.top - lift;
    for (let p = el.parentElement; p && p !== document.documentElement; p = p.parentElement) {
      if (!clips(p) || p.closest(".marquee, .wa") || p === document.body) continue;
      const pb = p.getBoundingClientRect();
      const scroller = ["auto", "scroll"].includes(getComputedStyle(p).overflowX); // carousels scroll sideways
      const dx = scroller ? 0 : Math.max(pb.left - b.left, b.right - pb.right, 0);
      const dy = Math.max(pb.top - top, b.bottom - pb.bottom, 0);
      if (dx > 1.5 || dy > 1.5)
        out.push({ text: label, by: p.tagName.toLowerCase() + "." + String(p.className).split(" ").slice(0, 3).join("."), dx: Math.round(dx), dy: Math.round(dy) });
    }
    // headline masks (.hl) are clip-paths reaching 0.4em above and 0.55em below their box
    const hl = el.closest(".hl");
    if (hl) {
      const pb = hl.getBoundingClientRect();
      const fs = parseFloat(getComputedStyle(hl).fontSize) || 16;
      const dy = Math.max(pb.top - 0.4 * fs - top, b.bottom - (pb.bottom + 0.55 * fs), 0);
      if (dy > 1.5) out.push({ text: label, by: "clip-path on .hl", dx: 0, dy: Math.round(dy) });
    }
    const sw = document.documentElement.clientWidth;
    if (!el.closest('[class*="overflow-x-auto"]') && (b.right > sw + 1 || b.left < -1)) out.push({ text: label, by: "page edge", dx: Math.round(Math.max(b.right - sw, -b.left)), dy: 0 });
  }
  const seen = new Set();
  return out.filter((o) => { const k = o.text + o.by + o.dx + o.dy; if (seen.has(k)) return false; seen.add(k); return true; });
})();
