#!/usr/bin/env python3
"""Make the website's webfonts from the free source fonts in tools/fonts/free/.

Inter (Latin) and Vazirmatn (Arabic script: Kurdish Sorani, Arabic, Persian) are both under the
SIL Open Font License 1.1 with no Reserved Font Name, so they may be subset and served.
Each keeps its full weight axis (100-900); Inter also keeps its optical-size axis.

Writes assets/fonts/inter.woff2, assets/fonts/vazirmatn.woff2 and copies both licences next to them.
The unicode ranges below must match the @font-face rules in css/tailwind.src.css.

Needs: fonttools 4.56.0, brotli 1.1.0 (tools/requirements.txt)
"""
import os
import shutil
from fontTools import subset

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "free")
OUT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "assets", "fonts")

LATIN = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,"
         "U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD")
ARABIC = "U+0020,U+00A0,U+0600-06FF,U+0750-077F,U+08A0-08FF,U+200C-200F,U+FB50-FDFF,U+FE70-FEFF"
JOBS = [("Inter.ttf", "inter.woff2", LATIN, "OFL-Inter.txt"),
        ("Vazirmatn.ttf", "vazirmatn.woff2", ARABIC, "OFL-Vazirmatn.txt")]


def unicodes(spec):
    out = []
    for part in spec.split(","):
        a, _, b = part.replace("U+", "").partition("-")
        out += range(int(a, 16), int(b or a, 16) + 1)
    return out


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for src, dst, spec, lic in JOBS:
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["*"]       # keep every OpenType feature: Arabic joining, kerning, ligatures
        opts.name_IDs = ["*"]
        opts.hinting = False               # smaller; modern browsers render these variable fonts unhinted
        opts.notdef_outline = True
        font = subset.load_font(os.path.join(SRC, src), opts)
        sub = subset.Subsetter(opts)
        sub.populate(unicodes=unicodes(spec))
        sub.subset(font)
        subset.save_font(font, os.path.join(OUT, dst), opts)
        shutil.copyfile(os.path.join(SRC, lic), os.path.join(OUT, lic))
        print(f"{dst}: {os.path.getsize(os.path.join(OUT, dst)) // 1024} kB  ({spec[:40]}...)")
