/* dindarahmed.com: small, dependency-free page behaviour.
   Everything here is progressive: the pages read fine without it. */
(function () {
  var html = document.documentElement;
  var loc = document.body.getAttribute("data-loc") || "en";
  var rtl = html.dir === "rtl";
  var calm = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---- Hero headline: letter (Latin) or word (Arabic script) reveal ----
  document.querySelectorAll("[data-split]").forEach(function (h) {
    if (calm) return;
    h.setAttribute("aria-label", h.textContent.replace(/\s+/g, " ").trim());
    var i = 0;
    var walk = function (node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 1) { walk(n); return; }
        if (n.nodeType !== 3) return;
        var frag = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(function (part) {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(" ")); return; }
          var w = document.createElement("span");
          w.className = "w";
          w.setAttribute("aria-hidden", "true");
          if (rtl) {
            w.className = "w c";
            w.style.animationDelay = (i++ * 0.08) + "s";
            w.textContent = part;
          } else {
            part.split("").forEach(function (ch) {
              var c = document.createElement("span");
              c.className = "c";
              c.style.animationDelay = (i++ * 0.025) + "s";
              c.textContent = ch;
              w.appendChild(c);
            });
          }
          frag.appendChild(w);
        });
        node.replaceChild(frag, n);
      });
    };
    walk(h);
    h.classList.add("split");
  });

  // ---- Image skeletons: fade images in once loaded ----
  var settle = function (img) {
    var box = img.closest(".sk");
    if (box) box.classList.add("ld");
  };
  var watchImages = function (root) {
    root.querySelectorAll(".sk img").forEach(function (img) {
      if (img.complete && img.naturalWidth) settle(img);
      else {
        img.addEventListener("load", function () { settle(img); });
        img.addEventListener("error", function () { settle(img); });
      }
    });
  };
  watchImages(document);

  // ---- Scroll reveal ----
  var observe = function (root) {
    var items = root.querySelectorAll(".rv:not(.in)");
    if (!("IntersectionObserver" in window) || calm) {
      items.forEach(function (el) { el.classList.add("in"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    items.forEach(function (el) { io.observe(el); });
  };
  observe(document);

  // ---- Mobile menu ----
  var toggle = document.getElementById("menu-toggle");
  var menu = document.getElementById("menu");
  if (toggle && menu) {
    var setOpen = function (open) {
      menu.hidden = !open;
      document.body.classList.toggle("menu-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.textContent = open ? toggle.getAttribute("data-close") : toggle.getAttribute("data-open");
    };
    toggle.addEventListener("click", function () { setOpen(menu.hidden); });
    menu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { setOpen(false); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !menu.hidden) { setOpen(false); toggle.focus(); }
    });
  }

  // ---- Click-to-load YouTube: nothing loads from YouTube until play ----
  document.querySelectorAll("[data-yt]").forEach(function (box) {
    var btn = box.querySelector(".yt-play");
    if (!btn) return;
    btn.addEventListener("click", function () {
      var frame = document.createElement("iframe");
      frame.src = "https://www.youtube-nocookie.com/embed/" + box.getAttribute("data-yt") + "?autoplay=1&rel=0";
      frame.title = box.getAttribute("data-yt-title") || "Video";
      frame.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
      frame.allowFullscreen = true;
      frame.className = "absolute inset-0 w-full h-full";
      frame.setAttribute("frameborder", "0");
      box.innerHTML = "";
      box.appendChild(frame);
    });
  });

  // ---- Client logos: one list (assets/data/clients.json) feeds every page ----
  var targets = document.querySelectorAll("[data-clients]");
  if (!targets.length) return;
  fetch("/assets/data/clients.json")
    .then(function (r) { return r.json(); })
    .then(function (data) {
      var altFor = function (name) {
        if (!name) return data.alt_unnamed[loc] || data.alt_unnamed.en;
        return (data.alt[loc] || data.alt.en).replace("{name}", name);
      };
      var logoImg = function (l, cls) {
        var img = document.createElement("img");
        img.src = "/assets/img/clients/" + l.file;
        img.alt = altFor(l.name);
        img.loading = "lazy";
        img.decoding = "async";
        img.width = 256;
        img.height = 256;
        img.className = cls;
        return img;
      };
      targets.forEach(function (t) {
        if (t.getAttribute("data-clients") === "marquee") {
          var track = document.createElement("div");
          track.className = "marquee-track";
          // two identical runs so the loop is seamless; the copy is hidden from AT
          for (var run = 0; run < 2; run++) {
            data.categories.forEach(function (cat) {
              cat.logos.forEach(function (l) {
                var cell = document.createElement("div");
                cell.className = "shrink-0 w-28 h-28 md:w-36 md:h-36 mx-2 md:mx-4 flex items-center justify-center";
                var img = logoImg(l, "max-w-full max-h-full object-contain grayscale opacity-70 hover:grayscale-0 hover:opacity-100 transition");
                if (run) { img.alt = ""; cell.setAttribute("aria-hidden", "true"); }
                cell.appendChild(img);
                track.appendChild(cell);
              });
            });
          }
          t.appendChild(track);
        } else {
          data.categories.forEach(function (cat) {
            var block = document.createElement("div");
            block.className = "rv border-t border-line pt-8 pb-12 first:border-0 first:pt-0";
            var head = document.createElement("div");
            head.className = "flex flex-wrap items-baseline justify-between gap-x-6 gap-y-1 mb-6";
            var h3 = document.createElement("h3");
            h3.className = "text-[20px] font-medium tracking-tight";
            h3.textContent = cat.label[loc] || cat.label.en;
            var sub = document.createElement("p");
            sub.className = "text-[15px] text-muted";
            sub.textContent = cat.sub[loc] || cat.sub.en;
            head.appendChild(h3);
            head.appendChild(sub);
            var grid = document.createElement("div");
            grid.className = "grid grid-cols-3 sm:grid-cols-4 lg:grid-cols-6 gap-3";
            cat.logos.forEach(function (l) {
              var cell = document.createElement("div");
              cell.className = "aspect-square border border-card rounded-lg flex items-center justify-center p-3 bg-white";
              cell.appendChild(logoImg(l, "max-w-full max-h-full object-contain"));
              grid.appendChild(cell);
            });
            block.appendChild(head);
            block.appendChild(grid);
            t.appendChild(block);
          });
          observe(t);
        }
      });
    })
    .catch(function () { /* logos are a bonus; the page stands without them */ });
})();
