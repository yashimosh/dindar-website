#!/usr/bin/env python3
"""Extend 29LT Zawi with the five Kurdish Sorani letters it lacks: ڕ ڵ ە ۆ ێ.

Same terms as the UA Neo build (29Letters, in writing): the fonts may be
modified and used in any medium, but not redistributed. The extended files
stay on the build machine (tools/fonts/dist/, git-ignored) and the website only
ever receives SVG outlines made from them.

Zawi differs from UA Neo in four ways, all handled here:
  - the archive's static files are CFF, so we instantiate Regular / Bold /
    Black from the variable TrueType file and extend those
  - positional forms are named after Unicode presentation forms (uniFEDF,
    uniFEAE ...) instead of ".init/.fina" suffixes
  - ە is missing as well, so it is derived from ة by removing the two dots
  - it already has a full Latin alphabet, so no fallback font is needed

Needs: fonttools 4.56.0
"""
import os
import sys

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.ttLib.tables.otTables import SingleSubst, Lookup, Ligature
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.ttLib.tables.ttProgram import Program
from array import array

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from extend_uaneo import topmost_x, bottommost_x  # noqa: E402

VAR = os.path.join(HERE, "src_zawi_var", "29LTZawi-Variable.ttf")
OUT = os.path.join(HERE, "dist")
WEIGHTS = {"Regular": 400, "Bold": 700, "Black": 900}

# The small V is the font's own Arabic-Indic seven (٧, U+0667) shrunk to width w, so its
# strokes and corners match the letters. A shrunk glyph gets thin, so the seven is taken
# from a heavier instance (dw = extra weight) to keep the stroke in line with the stems.
# Units: 1000-unit em (Zawi is 1000 upem already).
MARK = {
    "Regular": dict(w=190, dw=250, gap_above=50, gap_below=40),
    "Bold":    dict(w=200, dw=200, gap_above=50, gap_below=40),
    "Black":   dict(w=215, dw=0,   gap_above=55, gap_below=45),
}

# new codepoint -> (base codepoint, mark, {new suffix: base glyph name})
# base glyph names are the font's own (presentation-form names for joined forms)
LETTERS = {
    0x0695: (0x0631, "below", {"": "uni0631", ".fina": "uniFEAE"}),
    0x06B5: (0x0644, "above", {"": "uni0644", ".init": "uniFEDF", ".medi": "uniFEE0", ".fina": "uniFEDE"}),
    0x06C6: (0x0648, "above", {"": "uni0648", ".fina": "uniFEEE"}),
    0x06CE: (0x06CC, "above", {"": "uni06CC", ".init": "uniFBFE", ".medi": "uniFBFF", ".fina": "uniFBFD"}),
}
# ە: ة without its two dots (the last two contours)
AE = {"": "uni0629", ".fina": "uniFE94"}
LIGS = [  # ڵ + alef ligatures, built from the font's own لا glyphs
    ("uniFEFB", "uni06B50627", "uni06B5.init"),
    ("uniFEFC", "uni06B50627.fina", "uni06B5.medi"),
]


def _outline(glyf, name):
    g = glyf[name]
    coords, ends, flags = g.getCoordinates(glyf)
    return list(coords), list(ends), list(flags), g


def _compose(coords, ends, flags, extra_pts=(), extra_flags=()):
    all_coords = list(coords) + list(extra_pts)
    all_flags = [f & 1 for f in flags] + list(extra_flags)  # outlines only; keep on/off-curve bit
    new_ends = list(ends)
    if extra_pts:
        new_ends.append(len(all_coords) - 1)
    g = Glyph()
    g.numberOfContours = len(new_ends)
    g.endPtsOfContours = new_ends
    g.coordinates = GlyphCoordinates(all_coords)
    g.flags = array("B", all_flags)
    prog = Program()
    prog.fromBytecode(b"")
    g.program = prog
    xs = [x for x, _ in all_coords]
    ys = [y for _, y in all_coords]
    g.xMin, g.xMax, g.yMin, g.yMax = int(min(xs)), int(max(xs)), int(min(ys)), int(max(ys))
    return g


def _add(font, name, glyph, advance):
    font["glyf"][name] = glyph
    font["hmtx"][name] = (advance, glyph.xMin)  # lsb must equal xMin for glyf fonts


def extend(style, wght):
    var = TTFont(VAR)
    font = instancer.instantiateVariableFont(var, {"wght": wght}, inplace=False)
    P = dict(MARK[style])
    sev = instancer.instantiateVariableFont(TTFont(VAR), {"wght": min(900, wght + P["dw"])}, inplace=False)
    sc, _, sf, _ = _outline(sev["glyf"], "uni0667")
    xs_, ys_ = [x for x, _ in sc], [y for _, y in sc]
    k = P["w"] / (max(xs_) - min(xs_))
    P["h"] = (max(ys_) - min(ys_)) * k
    mx, my = (max(xs_) + min(xs_)) / 2, (max(ys_) + min(ys_)) / 2

    def mark(cx, cy):
        return [((x - mx) * k + cx, (y - my) * k + cy) for x, y in sc], [f & 1 for f in sf]

    glyf, hmtx = font["glyf"], font["hmtx"]
    cmap_tables = [t for t in font["cmap"].tables if t.isUnicode()]
    print(f"\n== Zawi {style} (wght {wght})")

    added = {"init": {}, "medi": {}, "fina": {}}

    for new_cp, (_, pos, forms) in LETTERS.items():
        iso = f"uni{new_cp:04X}"
        for suffix, base_name in forms.items():
            coords, ends, flags, src = _outline(glyf, base_name)
            ref = glyf[base_name]
            if pos == "above":
                cx = topmost_x(ref)
                cy = ref.yMax + P["gap_above"] + P["h"] / 2
                pts, fl = mark(cx, cy)
            else:
                cx = bottommost_x(ref)
                cy = ref.yMin - P["gap_below"] - P["h"] / 2
                pts, fl = mark(cx, cy)
            name = iso + suffix
            _add(font, name, _compose(coords, ends, flags, pts, fl), hmtx[base_name][0])
            if suffix:
                added[suffix.strip(".")][iso] = name
            print(f"   + {name:16} from {base_name:8} mark at x={cx:.0f}")

    for suffix, base_name in AE.items():
        coords, ends, flags, _ = _outline(glyf, base_name)
        assert len(ends) == 3, f"expected body + 2 dots in {base_name}, got {len(ends)} contours"
        keep = ends[0] + 1
        name = "uni06D5" + suffix
        _add(font, name, _compose(coords[:keep], ends[:1], flags[:keep]), hmtx[base_name][0])
        if suffix:
            added["fina"]["uni06D5"] = name
        print(f"   + {name:16} from {base_name:8} dots removed")

    # the font's own lam-alef ligature glyphs, with the V added above the lam
    for lig_src, lig_new, _ in LIGS:
        coords, ends, flags, _ = _outline(glyf, lig_src)
        ref = glyf[lig_src]
        tops = [x for x, y in ref.coordinates if y >= ref.yMax - 40]
        right = max(tops)
        cl = [x for x in tops if x >= right - 120]
        cx = sum(cl) / len(cl)
        cy = ref.yMax + P["gap_above"] + P["h"] / 2
        pts, fl = mark(cx, cy)
        _add(font, lig_new, _compose(coords, ends, flags, pts, fl), hmtx[lig_src][0])
        print(f"   + {lig_new:16} from {lig_src}")

    order = list(glyf.glyphOrder)
    assert len(order) == len(set(order))
    font.setGlyphOrder(order)

    for cp in [0x0695, 0x06B5, 0x06C6, 0x06CE, 0x06D5]:
        for t in cmap_tables:
            t.cmap[cp] = f"uni{cp:04X}"

    gsub = font["GSUB"].table
    for tag, mapping in added.items():
        if not mapping:
            continue
        sub = SingleSubst()
        sub.mapping = dict(mapping)
        lk = Lookup()
        lk.LookupType, lk.LookupFlag, lk.SubTable, lk.SubTableCount = 1, 0, [sub], 1
        gsub.LookupList.Lookup.append(lk)
        gsub.LookupList.LookupCount = len(gsub.LookupList.Lookup)
        idx = gsub.LookupList.LookupCount - 1
        for rec in gsub.FeatureList.FeatureRecord:
            if rec.FeatureTag == tag and idx not in rec.Feature.LookupListIndex:
                rec.Feature.LookupListIndex.append(idx)
                rec.Feature.LookupCount = len(rec.Feature.LookupListIndex)

    done = 0
    for rec in gsub.FeatureList.FeatureRecord:
        if rec.FeatureTag != "rlig":
            continue
        for li in rec.Feature.LookupListIndex:
            for st in gsub.LookupList.Lookup[li].SubTable:
                ligs = getattr(st, "ligatures", None)
                if not ligs or "uniFEDF" not in ligs:
                    continue
                for _, lig_new, first in LIGS:
                    if first not in ligs:
                        L = Ligature()
                        L.Component, L.LigGlyph, L.CompCount = ["uniFE8E"], lig_new, 2
                        ligs[first] = [L]
                        done += 1
    assert done >= 2, "ligature rules were not registered"

    cd = font["GDEF"].table.GlyphClassDef.classDefs
    for n in order:
        if n.startswith(("uni0695", "uni06B5", "uni06C6", "uni06CE", "uni06D5")):
            cd[n] = 2 if n.startswith("uni06B50627") else 1

    nm = font["name"]
    fam = nm.getBestFamilyName() + " KU"
    for rec in nm.names:
        if rec.nameID in (1, 4, 16):
            rec.string = fam.encode(rec.getEncoding())
        if rec.nameID == 6:
            rec.string = (fam.replace(" ", "") + "-" + style).encode(rec.getEncoding())
    font["maxp"].numGlyphs = len(order)

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"29LT_Zawi_KU_{style}.ttf")
    font.save(path)
    chk = TTFont(path).getBestCmap()
    assert all(cp in chk for cp in (0x0695, 0x06B5, 0x06C6, 0x06CE, 0x06D5))
    print(f"   wrote {os.path.relpath(path, HERE)} ({os.path.getsize(path) // 1024} kB); ڕ ڵ ە ۆ ێ verified")


if __name__ == "__main__":
    for style, wght in WEIGHTS.items():
        extend(style, wght)
    print("\nDone. Build-only files: never publish them.")
