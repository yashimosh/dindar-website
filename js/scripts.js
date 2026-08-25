document.addEventListener("DOMContentLoaded", function () {
  // Mobile menu toggle
  var toggle = document.getElementById("nav-toggle");
  var mobileNav = document.getElementById("mobile-nav");

  if (toggle && mobileNav) {
    var icon = toggle.querySelector(".material-symbols-outlined");

    toggle.addEventListener("click", function () {
      var isOpen = mobileNav.classList.toggle("hidden") === false;
      mobileNav.classList.toggle("flex", isOpen);
      toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
      if (icon) icon.textContent = isOpen ? "close" : "menu";
    });

    mobileNav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        mobileNav.classList.add("hidden");
        mobileNav.classList.remove("flex");
        toggle.setAttribute("aria-expanded", "false");
        if (icon) icon.textContent = "menu";
      });
    });
  }

  // Contact form -> composes a mailto: so it works with no backend
  var form = document.getElementById("contact-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var get = function (id) {
        var el = form.querySelector("#" + id);
        return el ? el.value.trim() : "";
      };
      var name = get("name"), email = get("email"),
          subject = get("subject"), message = get("message");
      var body = "Name: " + name + "\nEmail: " + email + "\n\n" + message;
      window.location.href =
        "mailto:" + form.dataset.mailto +
        "?subject=" + encodeURIComponent(subject ? "Website enquiry - " + subject : "Website enquiry") +
        "&body=" + encodeURIComponent(body);
    });
  }

  // Click-to-load YouTube facade: no YouTube request until the visitor presses play
  document.querySelectorAll("[data-yt]").forEach(function (box) {
    var btn = box.querySelector(".yt-play");
    if (!btn) return;
    btn.addEventListener("click", function () {
      var id = box.getAttribute("data-yt");
      var frame = document.createElement("iframe");
      frame.src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0";
      frame.title = box.getAttribute("data-yt-title") || "Video";
      frame.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
      frame.allowFullscreen = true;
      frame.className = "absolute inset-0 w-full h-full";
      frame.setAttribute("frameborder", "0");
      box.innerHTML = "";
      box.appendChild(frame);
    });
  });

  // Nav shadow on scroll
  var nav = document.getElementById("main-nav");
  if (nav) {
    window.addEventListener("scroll", function () {
      if (window.scrollY > 50) {
        nav.classList.add("shadow-md");
        nav.classList.remove("shadow-sm");
      } else {
        nav.classList.remove("shadow-md");
        nav.classList.add("shadow-sm");
      }
    });
  }
});
