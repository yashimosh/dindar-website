/* dindarahmed.com: small, dependency-free page behaviour.
   Everything here is progressive: the pages read fine without it. */
(function () {
  var loc = document.body.getAttribute("data-loc") || "en";
  var calm = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---- Count-up numbers (keeps the page's own digit set: 0-9, Arabic-Indic or Persian) ----
  var SETS = ["0123456789", "\u0660\u0661\u0662\u0663\u0664\u0665\u0666\u0667\u0668\u0669", "\u06f0\u06f1\u06f2\u06f3\u06f4\u06f5\u06f6\u06f7\u06f8\u06f9"];
  // Numbers are drawn from the page's glyph sprite (Zawi, shaped at build time):
  // each character is an inline SVG that points at a <path id="kc{codepoint}">.
  var drawCount = function (el, str) {
    var host = el.querySelector(".kw-count"), sp = document.getElementById("kwsprite");
    if (!host || !sp) { el.textContent = str; return; }
    var asc = +sp.getAttribute("data-asc"), desc = +sp.getAttribute("data-desc");
    var chars = str.split("");
    if (document.documentElement.dir === "rtl" && chars[chars.length - 1] === "+") chars.unshift(chars.pop());
    host.innerHTML = chars.map(function (ch) {
      var id = "kc" + ch.charCodeAt(0), p = document.getElementById(id);
      if (!p) return "";
      var w = +p.getAttribute("data-w");
      return '<svg class="kw" viewBox="0 ' + (-asc) + " " + w + " " + (asc + desc) + '"><use href="#' + id + '"/></svg>';
    }).join("");
  };
  var countUp = function (el) {
    var text = el.getAttribute("data-count-text") || el.textContent, set = SETS[0];
    SETS.forEach(function (s) { if (s.split("").some(function (d) { return text.indexOf(d) > -1; })) set = s; });
    var digits = text.split("").filter(function (ch) { return set.indexOf(ch) > -1; });
    // a hidden tab pauses animation frames, which would leave the number stuck at 0
    if (!digits.length || calm || document.visibilityState === "hidden") return;
    var target = parseInt(digits.map(function (d) { return set.indexOf(d); }).join(""), 10);
    var render = function (n) {
      var str = String(n).split("").map(function (d) { return set[+d]; }).join("");
      drawCount(el, text.replace(digits.join(""), str));
    };
    var t0 = null;
    var step = function (t) {
      if (t0 === null) t0 = t;
      var k = Math.min(1, (t - t0) / 1400);
      render(Math.round(target * (1 - Math.pow(1 - k, 3))));
      if (k < 1) requestAnimationFrame(step);
    };
    render(0);
    requestAnimationFrame(step);
  };

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

  // ---- WhatsApp button: step aside while the contact section (which has WhatsApp in it) is on screen ----
  var wa = document.querySelector(".wa"), contact = document.getElementById("contact");
  if (wa && contact && "IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      wa.classList.toggle("wa-off", entries[0].isIntersecting);
    }, { rootMargin: "0px 0px -25% 0px" }).observe(contact);
  }

  // ---- Pause / play for the moving bands ----
  document.querySelectorAll("[data-marquee]").forEach(function (btn) {
    var band = document.querySelector(btn.getAttribute("data-marquee"));
    if (!band) return;
    btn.addEventListener("click", function () {
      var paused = band.classList.toggle("paused");
      btn.setAttribute("aria-pressed", paused ? "true" : "false");
      btn.setAttribute("aria-label", btn.getAttribute(paused ? "data-play" : "data-pause"));
    });
  });

  // ---- Scroll reveal ----
  var observe = function (root) {
    var items = root.querySelectorAll(".rv:not(.in), .reveal:not(.in), [data-count]");
    if (!("IntersectionObserver" in window) || calm) {
      items.forEach(function (el) { el.classList.add("in"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add("in");
        if (e.target.hasAttribute("data-count")) countUp(e.target);
        io.unobserve(e.target);
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
      toggle.querySelectorAll("[data-state]").forEach(function (s) {
        s.hidden = (s.getAttribute("data-state") === "close") !== open;
      });
    };
    toggle.addEventListener("click", function () { setOpen(menu.hidden); });
    menu.querySelectorAll("a, [data-menu-close]").forEach(function (a) {
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
      var logoImg = function (l, cls, eager) {
        var img = document.createElement("img");
        img.src = "/assets/img/clients/" + l.file;
        img.alt = altFor(l.name);
        // the marquee slides logos in sideways, which lazy-loading misses
        img.loading = eager ? "eager" : "lazy";
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
                cell.className = "shrink-0 w-24 h-24 md:w-32 md:h-32 mx-2 md:mx-3 overflow-hidden bg-white";
                var img = logoImg(l, "w-full h-full object-contain", true);
                if (run) { img.alt = ""; cell.setAttribute("aria-hidden", "true"); }
                cell.appendChild(img);
                track.appendChild(cell);
              });
            });
          }
          t.appendChild(track);
        } else {
          // category headings are in the HTML (set in Zawi at build time); fill each grid
          data.categories.forEach(function (cat) {
            var block = t.querySelector('[data-cat="' + cat.id + '"]');
            var grid = block && block.querySelector("[data-cat-grid]");
            if (!grid) return;
            cat.logos.forEach(function (l) {
              var cell = document.createElement("div");
              cell.className = "aspect-square overflow-hidden bg-white";
              cell.appendChild(logoImg(l, "w-full h-full object-contain"));
              grid.appendChild(cell);
            });
          });
          observe(t);
        }
      });
    })
    .catch(function () { /* logos are a bonus; the page stands without them */ });
})();
