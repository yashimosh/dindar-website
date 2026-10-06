#!/usr/bin/env python3
"""One-shot generator for the redesigned dindarahmed.com.
Reads content_{loc}.json + ui_strings.json, writes plain static HTML
(12 pages + 404) and assets/data/clients.json into the repo.
After this runs, the HTML in the repo is the source of truth."""
import json, re, os, html as H
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))  # repo root (this file lives in tools/site/)
SITE = "https://dindarahmed.com"
LOCS = ["en", "ku", "ar", "fa"]
PREFIX = {"en": "/", "ku": "/ku/", "ar": "/ar/", "fa": "/fa/"}
HREFLANG = {"en": "en", "ku": "ckb", "ar": "ar", "fa": "fa"}
LANG_ATTR = {"en": "en", "ku": "ckb", "ar": "ar", "fa": "fa"}
LANG_NAME = {"en": "EN", "ku": "کوردی", "ar": "العربية", "fa": "فارسی"}
EMAIL = "Dindar.Ahmed@mithra.agency"
WA = "https://wa.me/9647719922486"
PHONE = "+964 771 992 2486"
IG = "https://www.instagram.com/dindar_ahmad/"
LI = "https://www.linkedin.com/in/dindar-ahmad-36ba57205/"
YT = "https://www.youtube.com/@mithra.production/videos"

C = {l: json.load(open(f"{HERE}/content_{l}.json")) for l in LOCS}
UI = json.load(open(f"{HERE}/ui_strings.json"))
# Kurdish uses the same phrase for "Featured Work" and "Case Studies"; where the
# two headings would repeat back to back, use the menu's own case-studies term
for _l in LOCS:
    if C[_l]["cases"]["h2"] == C[_l]["featured"]["h2"]:
        C[_l]["cases"]["h2"] = C[_l]["nav_mobile"]["#case-studies"]

e = lambda s: H.escape(s, quote=False)
a = lambda s: H.escape(s, quote=True)

# H1 emphasis: (text, gray?) segments per locale; must rebuild hero.h1 exactly
H1 = {
    "en": [("Tell Me", 0), ("What Isn't", 1), ("Selling", 0), (".", 1)],
    "ku": [("پێم بڵێ", 0), ("چی", 1), ("نافرۆشرێت", 0), (".", 1)],
    "ar": [("قل لي", 0), ("ما الذي", 1), ("لا يُباع", 0), (".", 1)],
    "fa": [("به من بگویید", 0), ("چه چیزی", 1), ("فروش نمی‌رود", 0), (".", 1)],
}

ICONS = {
    "troubleshoot": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/><path d="M8 11h1.5l1-2 2 4 1-2H15"/>',
    "campaign": '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
    "hub": '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/>',
    "movie": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 3v18M17 3v18M3 7.5h4M3 12h18M3 16.5h4M17 7.5h4M17 16.5h4"/>',
    "trending_up": '<path d="m22 7-8.5 8.5-5-5L2 17"/><path d="M16 7h6v6"/>',
}
def icon(name, cls="w-6 h-6"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

ARROW = '<svg class="w-4 h-4 rtl:-scale-x-100" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ARROW_UR = '<svg class="w-4 h-4 rtl:-scale-x-100" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>'
PLAY = '<svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13l11-6.5z"/></svg>'

def digits(loc, s):
    n = C[loc]["stats"][0]["n"]
    if "١" in n or "٠" in n:
        return s.translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩"))
    if "۱" in n or "۰" in n:
        return s.translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))
    return s

SIZES = {}
def size(img):
    if img not in SIZES:
        SIZES[img] = Image.open(f"{REPO}/assets/img/{img}").size
    return SIZES[img]

def pic(img, alt, cls="", box="", eager=False, wh=True):
    """image inside a shimmer skeleton box"""
    w, h = size(img)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    dims = f' width="{w}" height="{h}"' if wh else ""
    return (f'<div class="sk overflow-hidden {box}">'
            f'<img src="/assets/img/{img}" alt="{a(alt)}"{dims} {load} decoding="async" class="block w-full {cls}"/></div>')

def sentences(p):
    return re.split(r"(?<=[.!?؟])\s+", p.strip())

def name_of(loc):
    return C[loc]["quote"]["name"]

# ------------------------------------------------------------------ chrome

PAGES = {"home": "", "work": "work/", "about": "about/"}

def url(loc, page):
    return PREFIX[loc] + PAGES[page]

# a drawn diamond: Zawi has no ◆ glyph, and no text should fall back to another font
DIA = '<svg class="dia" viewBox="0 0 10 10" aria-hidden="true"><path d="M5 0l5 5-5 5-5-5z"/></svg>'
DIAMOND = f'<span class="text-accent" aria-hidden="true">{DIA}</span>'

def pause_btn(loc, target, cls=""):
    """pause/play button for a moving band (WCAG 2.2.2); the page script wires it to the band with id `target`"""
    u = UI[loc]
    return (f'<button type="button" class="marq-ctl {cls}" data-marquee="#{target}" aria-pressed="false" '
            f'aria-label="{a(u["anim_pause"])}" data-pause="{a(u["anim_pause"])}" data-play="{a(u["anim_play"])}">'
            '<svg class="mc-pause" viewBox="0 0 12 12" aria-hidden="true"><path d="M2.5 1.5h2.6v9H2.5zM6.9 1.5h2.6v9H6.9z"/></svg>'
            '<svg class="mc-play" viewBox="0 0 12 12" aria-hidden="true"><path d="M3 1.5l7 4.5-7 4.5z"/></svg></button>')

def head(loc, page, title, desc):
    c = C[loc]
    canon = SITE + url(loc, page)
    alts = "\n".join(f'<link rel="alternate" hreflang="{HREFLANG[l]}" href="{SITE}{url(l, page)}"/>' for l in LOCS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{SITE}{url("en", page)}"/>'
    font = "family=Noto+Kufi+Arabic:wght@300..900"
    return f"""<!DOCTYPE html>
<html lang="{LANG_ATTR[loc]}" dir="{'ltr' if loc == 'en' else 'rtl'}">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{e(title)}</title>
<meta name="description" content="{a(desc)}"/>
<meta name="author" content="{a(name_of(loc))}"/>
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg"/>
<link rel="icon" type="image/x-icon" sizes="48x48" href="/assets/favicon.ico"/>
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png"/>
<link rel="canonical" href="{canon}"/>
{alts}
<meta name="theme-color" content="#000000"/>
<meta property="og:type" content="profile"/>
<meta property="og:site_name" content="{a(name_of(loc))}"/>
<meta property="og:locale" content="{c['meta']['og_locale']}"/>
<meta property="og:url" content="{canon}"/>
<meta property="og:title" content="{a(title)}"/>
<meta property="og:description" content="{a(c['meta']['og_description'] if page == 'home' else desc)}"/>
<meta property="og:image" content="{SITE}/assets/img/portrait.jpg"/>
<meta property="og:image:width" content="900"/>
<meta property="og:image:height" content="900"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{a(title)}"/>
<meta name="twitter:description" content="{a(c['meta']['tw_description'] if page == 'home' else desc)}"/>
<meta name="twitter:image" content="{SITE}/assets/img/portrait.jpg"/>
<link href="/css/tailwind.css" rel="stylesheet"/>
<script>/* reveal animations only when the page opens in a visible tab: a hidden tab freezes CSS transitions half way, which leaves headlines cut off */if(document.visibilityState!=="hidden")document.documentElement.classList.add("js")</script>
</head>
<body data-loc="{loc}" class="bg-ink text-white antialiased overflow-x-hidden">
<a href="#main" class="sr-only focus:not-sr-only focus:absolute focus:top-3 focus:start-3 focus:z-[60] focus:btn-fire focus:px-4 focus:py-2">{e(UI[loc]['skip'])}</a>
"""

def nav_items(loc):
    c = C[loc]
    return [
        ("home", url(loc, "home"), UI[loc]["nav_home"]),
        ("work", url(loc, "work"), c["nav_mobile"]["#work"]),
        ("about", url(loc, "about"), c["nav_mobile"]["#about"]),
        ("contact", "#contact", c["nav_mobile"]["#contact"]),
    ]

def lang_links(loc, page, cls_on, cls_off):
    out = []
    for l in LOCS:
        cls = cls_on if l == loc else cls_off
        cur = ' aria-current="true"' if l == loc else ""
        out.append(f'<a href="{url(l, page)}" lang="{LANG_ATTR[l]}" hreflang="{HREFLANG[l]}" class="{cls}" data-kw{cur}>{LANG_NAME[l]}</a>')
    return "\n".join(out)

def header(loc, page):
    """white + difference blend: reads white over the dark hero, black over white pages"""
    u = UI[loc]
    links, mlinks = [], []
    for key, href, label in nav_items(loc):
        on = key == page
        cur = ' aria-current="page"' if on else ""
        links.append(f'<a href="{href}" class="{"fire-text" if on else "opacity-60 hover:opacity-100"} transition-opacity"{cur}>{e(label)}</a>')
        mlinks.append(f'<a href="{href}" class="block py-1 {"fire-text" if on else "text-white"}"{cur}>{e(label)}</a>')
    return f"""<header class="absolute inset-x-0 top-0 z-50">
<div class="wrap">
<div class="h-20 md:h-24 flex items-center justify-between gap-6 border-b border-white/10">
<a href="{url(loc, 'home')}" class="display text-[16px] md:text-[18px]">{e(name_of(loc))}</a>
<nav class="hidden md:flex items-center gap-8 lbl" aria-label="Main">
{chr(10).join(links)}
</nav>
<div class="lang hidden md:flex items-center gap-4 text-[14px]" aria-label="{a(u['label_language'])}">
{lang_links(loc, page, 'text-accent', 'opacity-60 hover:opacity-100 transition-opacity')}
</div>
<button id="menu-toggle" type="button" class="md:hidden lbl inline-flex items-center gap-2 min-h-[44px] px-4 btn-fire" aria-controls="menu" aria-expanded="false" data-open="{a(u['menu_open'])}" data-close="{a(u['menu_close'])}"><span data-state="open">{e(u['menu_open'])}</span><span data-state="close" hidden>{e(u['menu_close'])}</span></button>
</div>
</div>
</header>
<div id="menu" hidden class="md:hidden fixed inset-0 z-[60] bg-ink text-white overflow-y-auto">
<div class="wrap h-20 flex items-center justify-between border-b border-white/10">
<span class="display text-[16px]">{e(name_of(loc))}</span>
<button type="button" data-menu-close class="lbl inline-flex items-center min-h-[44px] px-4 btn-fire">{e(u['menu_close'])}</button>
</div>
<nav class="wrap pt-10 display text-[40px]" aria-label="Main">
{chr(10).join(mlinks)}
</nav>
<div class="lang wrap mt-12 flex flex-wrap gap-5 text-[17px]">
{lang_links(loc, page, 'text-accent', 'text-white/75')}
</div>
</div>
"""

def hl(text_html, cls=""):
    return f'<span class="hl"><span class="{cls}">{text_html}</span></span>'

def footer(loc, page):
    c = C[loc]; u = UI[loc]
    soc = [
        ("WhatsApp", WA, f'<span dir="ltr">{PHONE}</span>'),
        ("Instagram", IG, '<span dir="ltr">@dindar_ahmad</span>'),
        ("LinkedIn", LI, e(name_of(loc))),
        ("YouTube", YT, e(c["campaigns"]["channel"]["text"])),
    ]
    rows = "\n".join(
        f'<li><a href="{h}" target="_blank" rel="noopener" class="group flex items-baseline justify-between gap-4 py-4 border-t border-edge first:border-t-0">'
        f'<span class="lbl">{n}</span><span class="text-white/75 group-hover:text-accent transition-colors inline-flex flex-1 min-w-0 justify-end text-end items-baseline gap-2">{v} {ARROW_UR}</span></a></li>'
        for n, h, v in soc)
    return f"""<footer id="contact" class="relative overflow-hidden border-t border-line grad-up">
<div class="wrap above pt-24 md:pt-36 pb-10">
<p class="rv lbl text-accent mb-8">{DIA} {e(c['contact']['h2'])}</p>
<h2 class="reveal display text-[40px] sm:text-[64px] lg:text-[96px] max-w-6xl">{hl(e(c['cta']['h2']), 'fire-text')}</h2>
<p class="rv mt-10 text-[18px] leading-[1.6] md:text-[20px] text-white/75 max-w-2xl">{e(c['contact']['sub'])}</p>
<div class="mt-16 md:mt-24 grid gap-6 md:grid-cols-2">
<div class="rv border border-edge p-6 md:p-10">
<p class="lbl text-white/70 mb-4">{e(c['contact']['email_title'])}</p>
<a href="mailto:{EMAIL}" class="block text-[22px] sm:text-[30px] lg:text-[38px] leading-tight tracking-[-0.02em] text-white hover:text-accent transition-colors break-words rtl:text-right" dir="ltr">{EMAIL}</a>
<p class="mt-5 text-[17px] leading-[1.6] text-white/75 max-w-md">{e(c['contact']['email_body'])}</p>
<a href="mailto:{EMAIL}" class="mt-8 lbl inline-flex items-center gap-3 btn-fire px-7 py-4">{e(c['footer']['start_project'])} {ARROW}</a>
</div>
<div class="rv border border-edge p-6 md:p-10">
<p class="lbl text-white/70 mb-4">{e(c['contact']['direct_title'])}</p>
<ul class="text-[17px]">
{rows}
</ul>
</div>
</div>
<p class="display fire-text fit leading-[0.95] mt-24 md:mt-36 text-center whitespace-nowrap select-none" data-fit="0.96" aria-hidden="true">{e(name_of(loc))}.</p>
<div class="mt-12 pt-6 pb-16 sm:pb-0 sm:pe-20 border-t border-edge flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between text-[15px] text-white/90">
<p data-kw>{e(c['footer']['copyright'])}</p>
<div class="lang flex flex-wrap gap-4" aria-label="{a(u['label_language'])}">
{lang_links(loc, page, 'text-accent', 'hover:text-white transition-colors')}
</div>
</div>
</div>
</footer>
<a href="{WA}" target="_blank" rel="noopener" class="wa fixed bottom-5 end-5 z-40 inline-flex items-center gap-2 h-12 md:h-14 ps-3.5 pe-3.5 md:ps-4 md:pe-4 rounded-full btn-fire" aria-label="WhatsApp {PHONE}">
<svg class="w-6 h-6 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 11.5a8.5 8.5 0 0 1-12.6 7.4L3 20l1.2-4.2A8.5 8.5 0 1 1 20 11.5z"/><path d="M9 9.5c0 2.8 2.2 5 5 5l1-1.5-2-1-1 1a3 3 0 0 1-1.5-1.5l1-1-1-2L9 9.5z"/></svg>
<span class="lbl">WhatsApp</span>
</a>
<script src="/js/scripts.js" defer></script>
</body>
</html>
"""

def sec_head(title, sub=None, dark=False, extra=""):
    subc = "text-white/75" if dark else "text-muted"
    s = f'<p class="rv md:col-span-5 md:justify-self-end text-[18px] leading-[1.6] {subc} md:max-w-md">{e(sub)}</p>' if sub else ""
    return f"""<div class="grid gap-6 md:grid-cols-12 md:items-end mb-10 md:mb-14">
<h2 class="reveal display text-[36px] sm:text-[48px] lg:text-[68px] md:col-span-7">{hl(e(title))}</h2>
{s}{extra}
</div>"""

def section(sid, title, body, sub=None, dark=False):
    idattr = f' id="{sid}"' if sid else ""
    if dark:
        return f"""<section{idattr} class="relative overflow-hidden grad-diag">
<div class="wrap above py-16 md:py-24">
{sec_head(title, sub, dark=True)}
{body}
</div>
</section>
"""
    return f"""<section{idattr} class="wrap">
<div class="border-t border-line py-16 md:py-24">
{sec_head(title, sub)}
{body}
</div>
</section>
"""

def yt_box(loc, item, cls="aspect-video", eager=False):
    w, h = size(item["thumb"])
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f"""<div class="sk relative overflow-hidden {cls}" data-yt="{item['yt']}" data-yt-title="{a(item['yt_title'])}">
<img src="/assets/img/{item['thumb']}" alt="" width="{w}" height="{h}" {load} decoding="async" class="absolute inset-0 w-full h-full object-cover"/>
<button type="button" class="yt-play group absolute inset-0 flex items-end p-4 md:p-6 text-start" aria-label="{a(item['aria'])}">
<span class="inline-flex items-stretch bg-ink/85 text-white group-hover:bg-ink transition-colors"><span class="w-11 h-11 btn-fire flex items-center justify-center">{PLAY}</span><span class="flex items-center gap-3 px-4"><span class="lbl">{e(UI[loc]['watch'])}</span><span class="text-[14px] text-white/75" dir="ltr">{e(item['dur'])}</span></span></span>
</button>
</div>"""

CASE_IMG = {0: "tvc-06.jpg", 1: "tvc-01.jpg", 2: "tvc-07.jpg"}  # Kiasa, Banu, Runaki
CASE_SLUG = {0: "kiasa", 1: "banu", 2: "runaki"}

def page_intro(label, title, sub=None, jumps=None):
    s = f'<p class="rv mt-10 text-[18px] leading-[1.6] md:text-[20px] text-muted max-w-2xl">{e(sub)}</p>' if sub else ""
    if jumps:
        s += ('<nav class="rv mt-12 flex flex-wrap gap-2.5" aria-label="' + a(title) + '">'
              + "".join(f'<a href="#{sid}" class="lbl border border-white/30 px-4 py-2.5 hover:border-amber hover:text-amber transition-colors">{e(t)}</a>' for sid, t in jumps)
              + '</nav>')
    return f"""<section class="relative overflow-hidden grad-down">
<div class="wrap above pt-36 md:pt-52 pb-16 md:pb-24">
<p class="rv lbl text-muted mb-8">{DIAMOND} {e(label)}</p>
<h1 class="reveal display text-[44px] sm:text-[72px] lg:text-[112px] max-w-6xl">{hl(e(title), 'fire-text')}</h1>
{s}
</div>
</section>
"""

def h1_lines(loc):
    c = C[loc]
    segs = H1[loc]
    joined = re.sub(r"\s+\.", ".", " ".join(t for t, _ in segs))
    assert joined == c["hero"]["h1"], (loc, joined, c["hero"]["h1"])
    return (hl(e(segs[0][0])) + hl(e(segs[1][0]), "fire-text")
            + hl(e(segs[2][0]) + f'<span class="fire-text">{e(segs[3][0])}</span>'))

# ------------------------------------------------------------------ pages

def home(loc):
    c = C[loc]; u = UI[loc]; car = c["career"]
    sents = sentences(c["hero"]["p"])
    assert len(sents) == 5, (loc, len(sents))
    lead, info = " ".join(sents[:3]), " ".join(sents[3:])
    feat = next(i for i in c["campaigns"]["items"] if i["thumb"] == "tvc-02.jpg")


    stats = "\n".join(f"""<div class="rv py-12 md:py-16 sm:px-8 border-t border-ink/20 first:border-t-0 sm:border-t-0 sm:border-s sm:first:border-s-0 sm:first:ps-0">
<p class="display text-[56px] md:text-[80px]" data-count>{e(s['n'])}</p>
<p class="lbl mt-5">{e(s['label'])}</p>
<p class="mt-3 text-[16px] leading-[1.6] text-deep/75 max-w-xs">{e(s['body'])}</p>
</div>""" for s in c["stats"])

    rows = []
    for i, it in enumerate(c["expertise"]["items"]):
        rows.append(f"""<div class="svc rv border-t border-edge py-7 md:py-9 flex items-start md:items-center gap-5 md:gap-10">
<span class="svc-n shrink-0 w-11 h-11 md:w-14 md:h-14 rounded-full border border-edge flex items-center justify-center text-[14px] text-white/70">{digits(loc, f'{i+1:02d}')}</span>
<div class="flex-1 min-w-0">
<h3 class="svc-name display text-[24px] sm:text-[34px] lg:text-[46px]">{e(it['h3'])}</h3>
<p class="mt-3 text-[17px] leading-[1.6] text-white/75 max-w-xl">{e(it['p'])}</p>
</div>
<span class="hidden md:block text-white/60">{icon(it['icon'], 'w-8 h-8')}</span>
</div>""")

    cards = []
    for i, it in enumerate(c["cases"]["items"]):
        cards.append(f"""<a href="{url(loc, 'work')}#case-{CASE_SLUG[i]}" class="rv group block w-[82vw] sm:w-[60vw] shrink-0 snap-start md:w-auto">
<div class="relative">
{pic(CASE_IMG[i], '', 'aspect-[16/10] object-cover group-hover:scale-[1.04] transition-transform duration-700')}
<span class="absolute top-0 end-0 w-11 h-11 btn-fire flex items-center justify-center">{ARROW_UR}</span>
</div>
<p class="mt-6 display fire-text text-[28px] md:text-[34px] leading-[1.05] md:min-h-[2.1em]">{e(it['metric'])}</p>
<div class="mt-4 pt-4 border-t border-line flex items-baseline justify-between gap-4">
<h3 class="display text-[18px] md:text-[20px]">{e(it['name'])}</h3>
<span class="lbl text-muted">{e(it['tag'])}</span>
</div>
</a>""")

    tag = c["footer"]["tagline"]
    vals = "".join(
        f'<span class="display text-[44px] md:text-[96px] px-6 md:px-10 {"ol text-white/70" if k % 2 else "fire-text"}">{e(tag)}</span><span class="text-accent text-[18px]" aria-hidden="true">{DIA}</span>'
        for k in range(4))

    body = f"""<main id="main">
<section class="relative min-h-[100svh] flex flex-col justify-end overflow-hidden">
<div class="absolute top-0 end-0 h-[66%] w-full lg:inset-y-0 lg:h-auto lg:w-[68%]">
<img src="/assets/img/hero-portrait.jpg" alt="{a(c['hero']['portrait_alt'])}" width="2000" height="1250" fetchpriority="high" decoding="async" class="absolute inset-0 w-full h-full object-cover object-[50%_10%] lg:object-[50%_30%]"/>
<div class="hero-side absolute inset-0 hidden lg:block" aria-hidden="true"></div>
</div>
<div class="hero-shade absolute inset-0" aria-hidden="true"></div>
<div class="orb orb-a" style="width:640px;height:640px;bottom:-300px;inset-inline-start:-220px;opacity:.4" aria-hidden="true"></div>
<div class="wrap above pt-36 pb-24 md:pb-14">
<p class="rv lbl text-white/70 mb-6">{e(c['hero']['eyebrow'])}</p>
<h1 class="reveal display text-[40px] sm:text-[68px] lg:text-[88px] xl:text-[104px]">{h1_lines(loc)}</h1>
<div class="rv mt-10 md:mt-14 flex flex-wrap items-end justify-between gap-6">
<div class="flex flex-wrap gap-3">
<a href="{url(loc, 'work')}" class="lbl inline-flex items-center gap-3 btn-fire px-7 py-4">{e(c['hero']['btn_work'])} {ARROW}</a>
<a href="#contact" class="lbl inline-flex items-center gap-3 border border-white/30 text-white px-7 py-4 hover:border-amber hover:text-amber transition-colors">{e(c['cta']['btn'])}</a>
</div>
</div>
</div>
</section>
<section id="clients" class="border-b border-line">
<div class="wrap pt-10 md:pt-12 pb-6 flex flex-wrap items-baseline justify-between gap-x-6 gap-y-2">
<p class="lbl text-muted">{DIAMOND} {e(c['clients']['h2'])}</p>
<div class="flex items-center gap-5">{pause_btn(loc, 'marquee-clients')}<a href="{url(loc, 'about')}#clients" class="lbl inline-flex items-center gap-3 ul">{e(u['discover_more'])} {ARROW}</a></div>
</div>
<div id="marquee-clients" class="marquee marquee-fade pb-10 md:pb-12" data-clients="marquee"></div>
</section>
<section id="info" class="wrap">
<div class="py-16 md:py-24">
<p class="rv lbl text-muted mb-8">{DIAMOND} {e(u['label_info'])}</p>
<p data-kw class="rv text-[26px] sm:text-[36px] lg:text-[52px] font-semibold leading-[1.4] lg:leading-[1.3] tracking-[-0.02em] max-w-[1250px]">{e(lead)} <em class="hi not-italic">{e(car['belief_title'])}</em></p>
<div class="mt-14 grid gap-8 md:grid-cols-12">
<p class="rv md:col-start-6 md:col-span-7 text-[18px] leading-[1.65] md:text-[20px] text-muted">{e(info)}</p>
<a href="{url(loc, 'about')}" class="rv md:col-start-6 md:col-span-7 lbl inline-flex items-center gap-3 ul">{e(c['hero']['btn_about'])} {ARROW}</a>
</div>
</div>
</section>
<section class="wrap pb-16 md:pb-24">
<div class="rv flex flex-wrap items-baseline justify-between gap-x-6 gap-y-2 mb-5">
<p class="lbl text-muted">{DIAMOND} {e(c['campaigns']['h2'])}</p>
<a href="{url(loc, 'work')}#campaigns" class="lbl inline-flex items-center gap-3 ul">{e(u['view_all'])} {ARROW}</a>
</div>
<div class="rv">
{yt_box(loc, feat, 'aspect-video')}
<div class="mt-5 flex flex-wrap items-baseline justify-between gap-x-6 gap-y-1"><p class="lbl">{e(feat['h3'])}</p><p class="text-[16px] text-muted">{e(feat['p'])}</p></div>
</div>
</section>
<section class="band-fire text-deep">
<div class="wrap grid sm:grid-cols-3">
{stats}
</div>
</section>
{section('expertise', c['expertise']['h2'], f'<div class="border-b border-edge">{chr(10)}{chr(10).join(rows)}{chr(10)}</div>', sub=c['expertise']['sub'], dark=True)}
{section('work', c['cases']['h2'], f'''<div class="flex md:grid md:grid-cols-3 gap-4 md:gap-6 overflow-x-auto md:overflow-visible snap-x snap-mandatory scroll-px-4 md:scroll-px-0 [scrollbar-width:none] -mx-4 px-4 py-3 -my-3 md:mx-0 md:px-0 md:py-0 md:my-0">
{chr(10).join(cards)}
</div>
<a href="{url(loc, 'work')}" class="rv mt-12 lbl inline-flex items-center gap-3 ul">{e(u['view_all'])} {ARROW}</a>''', sub=c['cases']['sub'])}
<div class="relative">
<div id="marquee-slogan" class="marquee border-t border-line py-10 md:py-16" aria-hidden="true"><div class="marquee-track fast">{vals}{vals}</div></div>
{pause_btn(loc, 'marquee-slogan', 'absolute top-3 end-4 z-10')}
</div>
</main>
"""
    return head(loc, "home", c["meta"]["title"], c["meta"]["description"]) + header(loc, "home") + body + footer(loc, "home")


def about(loc):
    c = C[loc]; u = UI[loc]; car = c["career"]
    title = f"{c['nav_mobile']['#about']} | {name_of(loc)}"
    st = c["stats"][0]

    tags = "".join(f'<span class="lbl border border-edge px-4 py-2.5">{e(it["h3"])}</span>' for it in c["expertise"]["items"])

    exp = []
    for key in ("mithra", "sales"):
        exp.append(f"""<div class="rv border-t border-edge py-10 md:py-12 grid gap-4 md:grid-cols-12 md:gap-6">
<p class="md:col-span-3 display fire-text text-[28px] md:text-[34px] leading-[1.05]">{e(car[f'{key}_years'])}</p>
<div class="md:col-span-4"><h3 class="display text-[28px] md:text-[36px]">{e(car[f'{key}_title'])}</h3><p class="mt-3 text-[16px] text-muted">{e(car[f'{key}_org'])}</p></div>
<p class="md:col-span-5 text-[18px] leading-[1.65] text-white/80">{e(car[f'{key}_body'])}</p>
</div>""")

    certs = "\n".join(f"""<figure class="rv">
<a href="/assets/img/{it['img']}" target="_blank" rel="noopener" class="group block">
{pic(it['img'], it['alt'], 'aspect-[4/3] object-contain p-5 group-hover:scale-[1.03] transition-transform duration-500', box='border border-edge bg-night/40 group-hover:border-amber transition-colors')}
</a>
<figcaption class="mt-5"><p class="lbl text-muted">{e(it['issuer'])}</p><p data-kw class="mt-2 text-[18px] leading-snug font-medium">{e(it['title'])}</p><p class="mt-1 text-[15px] text-muted">{e(it['meta'])}</p></figcaption>
</figure>""" for it in c["certs"]["items"])

    gallery = "\n".join(f'<div class="rv mb-4 break-inside-avoid">{pic(it["img"], it["alt"], "h-auto")}</div>' for it in c["gallery"]["items"])

    q = c["quote"]["text"].strip().strip('"“”«»')
    body = f"""<main id="main">
{page_intro(car['belief_label'], car['belief_title'], jumps=[('experience', u['label_experience']), ('certificates', c['certs']['h2']), ('field', c['gallery']['h2']), ('clients', c['clients']['h2'])])}
<section class="wrap pb-20 md:pb-32">
<div class="grid gap-12 lg:grid-cols-12 lg:gap-16 items-start">
<div class="rv relative lg:col-span-5">
{pic('portrait-square.jpg', c['hero']['portrait_alt'], 'aspect-square object-cover', eager=True)}
<div class="absolute bottom-0 end-0 bg-amber text-deep px-6 py-5"><p class="display text-[44px]" data-count>{e(st['n'])}</p><p class="lbl mt-2 max-w-[11rem]">{e(st['label'])}</p></div>
</div>
<div class="lg:col-span-7">
<p class="rv lbl text-muted mb-6">{DIAMOND} {e(u['label_info'])}</p>
<p class="rv text-[22px] leading-[1.5] md:text-[28px] md:leading-[1.45] font-medium tracking-[-0.01em]">{e(c['hero']['p'])}</p>
<p class="rv mt-8 text-[18px] leading-[1.65] md:text-[20px] text-muted">{e(car['belief_body'])}</p>
<div class="rv mt-10 flex flex-wrap gap-2.5">{tags}</div>
</div>
</div>
</section>
<section class="relative overflow-hidden border-y border-line grad-diag">
<div class="wrap above py-24 md:py-36">
<blockquote class="rv max-w-6xl">
<p class="fire-text display text-[64px] md:text-[96px] leading-none" aria-hidden="true">“</p>
<p data-kw class="text-[28px] leading-[1.25] md:text-[48px] md:leading-[1.15] font-semibold tracking-[-0.02em]">{e(q)}</p>
<footer class="mt-10 flex flex-wrap gap-x-4 gap-y-1"><span class="lbl text-accent">{e(c['quote']['name'])}</span><span data-kw class="text-[16px] text-white/75">{e(c['quote']['role'])}</span></footer>
</blockquote>
</div>
</section>
{section('experience', u['label_experience'], f'<div class="border-b border-edge">{chr(10)}{chr(10).join(exp)}{chr(10)}</div>')}
{section('certificates', c['certs']['h2'], f'<div class="grid gap-x-6 gap-y-14 sm:grid-cols-2 lg:grid-cols-3">{chr(10)}{certs}{chr(10)}</div>', sub=c['certs']['sub'])}
{section('field', c['gallery']['h2'], f'<div class="columns-1 sm:columns-2 lg:columns-3 gap-4">{chr(10)}{gallery}{chr(10)}</div>', sub=c['gallery']['sub'])}
{section('clients', c['clients']['h2'], '<div data-clients="grid">' + ''.join(f'<div class="rv border-t border-line pt-8 pb-12 first:border-0 first:pt-0" data-cat="{cid}"><div class="flex flex-wrap items-baseline justify-between gap-x-6 gap-y-1 mb-6"><h3 class="display text-[22px] md:text-[26px]">{e(cat["h3"])}</h3><p class="lbl text-muted">{e(cat["sub"])}</p></div><div class="grid grid-cols-4 sm:grid-cols-6 lg:grid-cols-8 gap-2 sm:gap-3" data-cat-grid></div></div>' for cid, cat in zip(CLIENT_IDS, c['clients']['cats'])) + '</div>', sub=c['clients']['sub'])}
</main>
"""
    return head(loc, "about", title, car["belief_body"]) + header(loc, "about") + body + footer(loc, "about")


def work(loc):
    c = C[loc]; u = UI[loc]
    title = f"{c['nav_mobile']['#work']} | {name_of(loc)}"

    approach = "\n".join(f"""<article class="rv">
{pic(it['img'], it['alt'], 'aspect-[4/3] object-cover')}
<p class="mt-6 lbl text-muted">{f' {DIAMOND} '.join(e(t) for t in it['tags'])}</p>
<h3 class="mt-3 display text-[26px] md:text-[34px]">{e(it['h3'])}</h3>
<p class="mt-4 text-[18px] leading-[1.65] text-muted">{e(it['p'])}</p>
</article>""" for it in c["featured"]["items"])

    cases = []
    for i, it in enumerate(c["cases"]["items"]):
        cases.append(f"""<article id="case-{CASE_SLUG[i]}" class="rv scroll-mt-8 border-t border-card py-12 md:py-16 grid gap-8 lg:grid-cols-12 lg:gap-12">
<div class="lg:col-span-7">{yt_box(loc, next(v for v in c["campaigns"]["items"] if v["thumb"] == CASE_IMG[i]))}</div>
<div class="lg:col-span-5">
<p class="display text-[56px] md:text-[80px] ol text-amber/80" aria-hidden="true">{digits(loc, f'{i+1:02d}')}</p>
<p class="mt-4 display fire-text text-[32px] md:text-[44px] leading-[1.05]">{e(it['metric'])}</p>
<h3 class="mt-5 display text-[22px] md:text-[26px]">{e(it['name'])}</h3>
<p class="mt-2 lbl text-muted">{e(it['tag'])} {DIAMOND} {e(it['period'])}</p>
<p class="mt-5 text-[18px] leading-[1.65] text-white/80">{e(it['body'])}</p>
</div>
</article>""")

    camps = "\n".join(f"""<article class="rv{' md:col-span-2' if k == 0 else ''}">
{yt_box(loc, it, 'aspect-video md:aspect-[2.2/1]' if k == 0 else 'aspect-video')}
<p class="mt-5 lbl text-accent">{e(it['tag'])}</p>
<h3 class="mt-2 text-[22px] leading-snug font-semibold">{e(it['h3'])}</h3>
<p class="mt-2 text-[16px] leading-[1.6] text-white/75">{e(it['p'])}</p>
</article>""" for k, it in enumerate(c["campaigns"]["items"]))
    cp = c["campaigns"]
    note = f'<p class="rv mt-14 text-[16px] text-white/75">{e(cp["note_pre"])} <a href="{cp["channel"]["href"]}" target="_blank" rel="noopener" class="ul text-white">{e(cp["channel"]["text"])}</a>{e(cp["note_post"])}</p>'

    reels = "\n".join(f"""<a href="{it['href']}" target="_blank" rel="noopener" class="rv group block">
{pic(it['img'], it['alt'], 'aspect-[9/16] object-cover group-hover:scale-[1.03] transition-transform duration-700')}
<h3 class="mt-3 text-[14px] sm:text-[16px] leading-snug font-medium">{e(it['h3'])}</h3>
<p class="hidden sm:block mt-1 text-[15px] leading-[1.5] text-muted line-clamp-3">{e(it['p'])}</p>
</a>""" for it in c["reels"]["items"])

    body = f"""<main id="main">
{page_intro(c['nav_mobile']['#work'], c['featured']['h2'], c['cases']['sub'], jumps=[('case-studies', c['cases']['h2']), ('campaigns', cp['h2']), ('reels', c['reels']['h2']), ('approach', u['label_approach'])])}
{section('case-studies', c['cases']['h2'], f'<div class="border-b border-card">{chr(10)}{chr(10).join(cases)}{chr(10)}</div>')}
{section('campaigns', cp['h2'], f'<div class="grid gap-x-6 gap-y-14 md:grid-cols-2">{chr(10)}{camps}{chr(10)}</div>{chr(10)}{note}', sub=cp['sub'], dark=True)}
{section('reels', c['reels']['h2'], f'<div class="max-w-[960px] mx-auto grid grid-cols-3 gap-x-2 gap-y-8 sm:gap-x-4 sm:gap-y-10">{chr(10)}{reels}{chr(10)}</div>{chr(10)}<p class="rv mt-14 text-center"><a href="{IG}" target="_blank" rel="noopener" class="lbl inline-flex items-center gap-3 ul">Instagram <span dir="ltr">@dindar_ahmad</span> {ARROW_UR}</a></p>', sub=c['reels']['sub'])}
{section('approach', u['label_approach'], f'<div class="grid gap-x-6 gap-y-14 md:grid-cols-2">{chr(10)}{approach}{chr(10)}</div>')}
</main>
"""
    return head(loc, "work", title, c["campaigns"]["sub"]) + header(loc, "work") + body + footer(loc, "work")


def not_found():
    langs = " ".join(f'<a href="{PREFIX[l]}" lang="{LANG_ATTR[l]}" class="text-white/75 hover:text-accent">{LANG_NAME[l]}</a>' for l in LOCS)
    return f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="robots" content="noindex"/>
<title>Page not found | Dindar Ahmed</title>
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg"/>
<link rel="icon" type="image/x-icon" sizes="48x48" href="/assets/favicon.ico"/>
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png"/>
<link href="/css/tailwind.css" rel="stylesheet"/>
</head>
<body class="bg-ink text-white antialiased">
<main class="wrap min-h-screen flex flex-col justify-center py-24">
<p class="lbl text-accent mb-8">{DIA} 404</p>
<h1 class="display fire-text text-[48px] sm:text-[96px]">Page not found.</h1>
<p class="mt-10 text-[20px] leading-[1.6] text-white/75 max-w-xl">That page doesn&rsquo;t exist. Head back to the homepage, or write to <a class="ul text-white" href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<div class="mt-12 flex flex-wrap items-center gap-x-8 gap-y-4">
<a href="/" class="lbl inline-flex items-center gap-3 btn-fire px-7 py-4">Homepage {ARROW}</a>
<span class="lang flex gap-4 text-[16px]">{langs}</span>
</div>
</main>
</body>
</html>
"""

# ------------------------------------------------------------------ clients.json

CLIENT_IDS = ["food", "cleaning", "cosmetics", "education", "other"]

def clients_json():
    cats = []
    ids = CLIENT_IDS
    alt_tpl = {}
    unnamed = {}
    en = C["en"]["clients"]["cats"]
    for ci, cat in enumerate(en):
        logos = []
        for li, lg in enumerate(cat["logos"]):
            m = re.fullmatch(r"(.+) logo", lg["alt"])
            assert m, lg
            name = m.group(1)
            if name == "Client":  # logo with no known brand name
                for l in LOCS:
                    unnamed[l] = C[l]["clients"]["cats"][ci]["logos"][li]["alt"]
                logos.append({"name": "", "file": lg["file"].rsplit(".", 1)[0] + ".webp"})
                continue
            for l in LOCS:
                other = C[l]["clients"]["cats"][ci]["logos"][li]
                assert other["file"] == lg["file"], (l, other, lg)
                tpl = other["alt"].replace(name, "{name}")
                assert "{name}" in tpl, (l, other["alt"], name)
                alt_tpl.setdefault(l, tpl)
                assert alt_tpl[l] == tpl, (l, tpl, alt_tpl[l])
            logos.append({"name": name, "file": lg["file"].rsplit(".", 1)[0] + ".webp"})
        cats.append({
            "id": ids[ci],
            "label": {l: C[l]["clients"]["cats"][ci]["h3"] for l in LOCS},
            "sub": {l: C[l]["clients"]["cats"][ci]["sub"] for l in LOCS},
            "logos": logos,
        })
    return {
        "_readme": "Client logos for every page and language. To add a logo: drop a 256x256 image (WebP or PNG) in assets/img/clients/<category>/ and add {\"name\", \"file\"} to that category below. Order here is display order. Alt text is built from the 'alt' template per language; a logo with an empty name uses 'alt_unnamed'.",
        "alt": alt_tpl,
        "alt_unnamed": unnamed,
        "categories": cats,
    }

# ------------------------------------------------------------------ write

OUT = os.environ.get("GEN_OUT", REPO)

import display_svg

def write(rel, text):
    # Headings, labels, buttons, menus and numbers are set in 29LT Zawi as SVG
    # shapes (the font file itself is never served; see display_svg.py)
    if rel.endswith(".html"):
        if display_svg.available():
            lang = {"ku": "ckb", "ar": "ar", "fa": "fa"}.get(rel.split("/")[0], "en")
            text, n = display_svg.apply(text, lang)
            print(f"   Zawi: {n} unique words in {rel}")
        else:
            print(f"   WARNING: Zawi build fonts missing (tools/fonts/dist); {rel} falls back to Noto Kufi")
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", rel, len(text))

for loc in LOCS:
    base = "" if loc == "en" else f"{loc}/"
    write(f"{base}index.html", home(loc))
    write(f"{base}about/index.html", about(loc))
    write(f"{base}work/index.html", work(loc))
write("404.html", not_found())
write("assets/data/clients.json", json.dumps(clients_json(), ensure_ascii=False, indent=1) + "\n")
