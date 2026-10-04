#!/usr/bin/env python3
"""Extend 29LT UA Neo with the four Kurdish Sorani letters it lacks: ڕ ڵ ۆ ێ.

Rules for use (per 29Letters' direct confirmation):
  - You may modify the font.
  - You may use it in any medium (web, print, apps).
  - You may NOT redistribute the font file. On the web this means the TTF/OTF
    is never served to visitors; it is used only on the build machine to
    render display text to SVG paths, which are then embedded in the HTML.

What this script does:
  For each of ڕ ڵ ۆ ێ it adds one glyph per positional form (isolated, final,
  and where applicable initial and medial). Each new glyph is drawn as the
  outline of its base letter (reh, lam, waw, farsi yeh) plus a small V mark —
  above for ڵ ۆ ێ, below for ڕ. Unicode cmap entries, GSUB joining rules and
  advance widths are all registered.

Output lives under /print/build-fonts/dist/ and is excluded from the Pages
deploy via .assetsignore (which already covers /print).

Needs: fonttools 4.56.0
Run:   venv/bin/python extend_uaneo.py
"""
import os
import sys
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates, flagOnCurve
from fontTools.ttLib.tables.otTables import (
    SingleSubst,
    Lookup,
    FeatureRecord,
    LookupList,
)
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.tables.ttProgram import Program
from array import array

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(HERE, "src")
OUT_DIR = os.path.join(HERE, "dist")

STYLES = {
    "Regular": "29LT UA Neo N.ttf",
    "Bold": "29LT UA Neo N Bold.ttf",
    "Light": "29LT UA Neo N Light.ttf",
    "B": "29LT_UA_Neo_B.ttf",
}


def copy_outline(src_glyph: Glyph) -> tuple[list[tuple[float, float]], list[int], list[int]]:
    """Return the base glyph's coords, flags and endPts, so we can compose."""
    if src_glyph.numberOfContours == 0:
        return [], [], []
    coords = [(x, y) for x, y in src_glyph.coordinates]
    flags = list(src_glyph.flags)
    ends = list(src_glyph.endPtsOfContours)
    return coords, flags, ends


def chevron(cx: float, cy: float, width: float, height: float, stroke: float,
            pointing: str) -> tuple[list[tuple[float, float]], list[int]]:
    """Draw a small V (chevron) centred on (cx, cy).

    pointing="down": vertex at the bottom, used as a mark ABOVE a letter.
    pointing="up":   vertex at the top, used as a mark BELOW a letter (for ڕ).

    The mark is a filled, closed shape — not a stroke — so it rasterises
    cleanly at any size. All points are on-curve (flag = 1).
    """
    hw, hh, s = width / 2, height / 2, stroke / 2
    if pointing == "down":
        pts = [
            (cx - hw, cy + hh),      # outer top-left
            (cx, cy - hh),            # outer bottom tip
            (cx + hw, cy + hh),      # outer top-right
            (cx + hw - s, cy + hh - s * 0.6),
            (cx, cy - hh + s * 1.9),
            (cx - hw + s, cy + hh - s * 0.6),
        ]
    else:
        pts = [
            (cx - hw, cy - hh),
            (cx, cy + hh),
            (cx + hw, cy - hh),
            (cx + hw - s, cy - hh + s * 0.6),
            (cx, cy + hh - s * 1.9),
            (cx - hw + s, cy - hh + s * 0.6),
        ]
    return pts, [1] * len(pts)


def topmost_x(glyph: Glyph) -> float:
    """Return x of the highest point in the glyph — where the ascender is."""
    if glyph.numberOfContours == 0:
        return 0.0
    pts = list(glyph.coordinates)
    ymax = max(y for _, y in pts)
    xs_at_top = [x for x, y in pts if y >= ymax - 20]
    return sum(xs_at_top) / len(xs_at_top)


def lam_top_x(glyph: Glyph) -> float:
    """In a lam-alef ligature both strokes rise; the lam is the right-hand one."""
    pts = list(glyph.coordinates)
    ymax = max(y for _, y in pts)
    tops = [x for x, y in pts if y >= ymax - 40]
    right = max(tops)
    cluster = [x for x in tops if x >= right - 120]
    return sum(cluster) / len(cluster)


def bottommost_x(glyph: Glyph) -> float:
    if glyph.numberOfContours == 0:
        return 0.0
    pts = list(glyph.coordinates)
    ymin = min(y for _, y in pts)
    xs_at_bot = [x for x, y in pts if y <= ymin + 20]
    return sum(xs_at_bot) / len(xs_at_bot)


def compose_glyph(base: Glyph, mark_pts, mark_flags) -> Glyph:
    """Return a new simple glyph: base outline + mark, both as contours."""
    base_coords, base_flags, base_ends = copy_outline(base)
    all_coords = base_coords + list(mark_pts)
    all_flags = base_flags + list(mark_flags)
    if base_ends:
        new_ends = list(base_ends) + [base_ends[-1] + len(mark_pts)]
    else:
        new_ends = [len(mark_pts) - 1]

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
    g.xMin, g.xMax = int(min(xs)), int(max(xs))
    g.yMin, g.yMax = int(min(ys)), int(max(ys))
    return g


# codepoint -> (base_cp, mark_pos, variants)
# variants map Unicode-form suffix to the base glyph's suffix; '' is isolated.
NEW_LETTERS = {
    0x0695: (0x0631, "above_below_reh", {"": "", ".fina": ".fina"}),           # ڕ reh+V below
    0x06B5: (0x0644, "above",            {"": "", ".init": ".init", ".medi": ".medi", ".fina": ".fina"}),  # ڵ
    0x06C6: (0x0648, "above",            {"": "", ".fina": ".fina"}),           # ۆ
    0x06CE: (0x06CC, "above",            {"": "", ".init": ".init", ".medi": ".medi", ".fina": ".fina"}),  # ێ
}

# V mark size per weight, in units of a 1000-unit em (scaled to each font's
# own unitsPerEm: Regular is 1000, Bold and Light are 2048)
MARK_PARAMS = {
    "Light":    dict(w=260, h=140, s=60,  gap_above=70, gap_below=45),
    "Regular":  dict(w=280, h=160, s=90,  gap_above=70, gap_below=50),
    "Bold":     dict(w=300, h=180, s=130, gap_above=80, gap_below=55),
    "B":        dict(w=280, h=160, s=100, gap_above=70, gap_below=50),
}


def extend(style: str, src_path: str, out_path: str) -> None:
    print(f"\n== {style}: {os.path.basename(src_path)}")
    font = TTFont(src_path)
    k = font["head"].unitsPerEm / 1000
    params = {key: v * k for key, v in MARK_PARAMS[style].items()}
    glyf = font["glyf"]
    hmtx = font["hmtx"]
    cmap_table = font["cmap"]
    best_cmap = font.getBestCmap()
    glyph_order = font.getGlyphOrder()

    # 1. Build the new glyphs
    added = []
    for new_cp, (base_cp, pos, variants) in NEW_LETTERS.items():
        base_name = best_cmap[base_cp]
        for suffix_new, suffix_base in variants.items():
            src_name = base_name + suffix_base
            new_name = f"uni{new_cp:04X}{suffix_new}"
            if new_name in glyph_order:
                continue
            src_glyph = glyf[src_name]
            # expand phantom points
            src_glyph.expand(glyf)

            if pos == "above":
                cx = topmost_x(src_glyph)
                cy = src_glyph.yMax + params["gap_above"] + params["h"] / 2
                mark_pts, mark_flags = chevron(cx, cy, params["w"], params["h"], params["s"], "down")
            else:  # ڕ: a normal v (vertex down) tucked under the reh's tail
                cx = bottommost_x(src_glyph)
                cy = src_glyph.yMin - params["gap_below"] - params["h"] / 2
                mark_pts, mark_flags = chevron(cx, cy, params["w"], params["h"], params["s"], "down")

            new_glyph = compose_glyph(src_glyph, mark_pts, mark_flags)
            glyf[new_name] = new_glyph  # fontTools also appends the name to the glyph order
            hmtx[new_name] = hmtx[src_name]  # same advance as the base
            added.append((new_cp, suffix_new, new_name, src_name))
            print(f"   + {new_name:18}  (from {src_name})  cx={cx:.0f} cy={cy:.0f}")

    # ڵ + ا: the font joins ل + ا into one ligature glyph, so ڵ needs the same
    for lig_src, lig_new in [("uni06440627", "uni06B50627"), ("uni06440627.fina", "uni06B50627.fina")]:
        if lig_src not in glyf.glyphs or lig_new in glyf.glyphs:
            continue
        src_glyph = glyf[lig_src]
        src_glyph.expand(glyf)
        cx = lam_top_x(src_glyph)
        cy = src_glyph.yMax + params["gap_above"] + params["h"] / 2
        mark_pts, mark_flags = chevron(cx, cy, params["w"], params["h"], params["s"], "down")
        glyf[lig_new] = compose_glyph(src_glyph, mark_pts, mark_flags)
        hmtx[lig_new] = hmtx[lig_src]
        print(f"   + {lig_new:18}  (from {lig_src})  cx={cx:.0f} cy={cy:.0f}")

    glyph_order = list(glyf.glyphOrder)
    assert len(glyph_order) == len(set(glyph_order)), "duplicate glyph names"
    font.setGlyphOrder(glyph_order)

    # 2. cmap: add the four new codepoints -> isolated glyph
    for new_cp in NEW_LETTERS:
        iso_name = f"uni{new_cp:04X}"
        for sub in cmap_table.tables:
            if sub.isUnicode():
                sub.cmap[new_cp] = iso_name

    # 3. GSUB: register positional substitutions for the new letters
    gsub = font["GSUB"].table
    added_by_feat = {"init": {}, "medi": {}, "fina": {}}
    for new_cp, (_, _, variants) in NEW_LETTERS.items():
        iso = f"uni{new_cp:04X}"
        for suf in variants:
            if suf == "":
                continue
            feat = suf.strip(".")
            added_by_feat[feat][iso] = iso + suf

    for feat_tag, mapping in added_by_feat.items():
        if not mapping:
            continue
        # Add a new SingleSubst lookup
        sub = SingleSubst()
        sub.mapping = dict(mapping)
        lk = Lookup()
        lk.LookupType = 1
        lk.LookupFlag = 0
        lk.SubTable = [sub]
        lk.SubTableCount = 1
        gsub.LookupList.Lookup.append(lk)
        gsub.LookupList.LookupCount = len(gsub.LookupList.Lookup)
        new_lookup_idx = gsub.LookupList.LookupCount - 1

        # Point every matching feature record at the new lookup too
        for rec in gsub.FeatureList.FeatureRecord:
            if rec.FeatureTag == feat_tag:
                if new_lookup_idx not in rec.Feature.LookupListIndex:
                    rec.Feature.LookupListIndex.append(new_lookup_idx)
                    rec.Feature.LookupCount = len(rec.Feature.LookupListIndex)

    # 3b. rlig: ڵ.init/medi + ا.fina -> ڵا ligature, alongside the font's own لا rules
    from fontTools.ttLib.tables.otTables import Ligature
    for rec in gsub.FeatureList.FeatureRecord:
        if rec.FeatureTag != "rlig":
            continue
        for li in rec.Feature.LookupListIndex:
            for st in gsub.LookupList.Lookup[li].SubTable:
                ligs = getattr(st, "ligatures", None)
                if not ligs or "uni0644.init" not in ligs:
                    continue
                for first, lig in [("uni06B5.init", "uni06B50627"), ("uni06B5.medi", "uni06B50627.fina")]:
                    if lig in glyf.glyphs and first not in ligs:
                        L = Ligature(); L.Component = ["uni0627.fina"]; L.LigGlyph = lig; L.CompCount = 2
                        ligs[first] = [L]

    # 3c. GDEF: new letters are base glyphs (1), the ligatures are ligatures (2)
    if "GDEF" in font and font["GDEF"].table.GlyphClassDef:
        cd = font["GDEF"].table.GlyphClassDef.classDefs
        for name in glyph_order:
            if name.startswith(("uni0695", "uni06B5", "uni06C6", "uni06CE")):
                cd[name] = 2 if name.startswith("uni06B50627") else 1

    # 4. Family and version — mark the file as the extended version
    name_tbl = font["name"]
    def set_name(nid, val):
        for rec in name_tbl.names:
            if rec.nameID == nid:
                rec.string = val.encode(rec.getEncoding()) if isinstance(val, str) else val

    orig_family = name_tbl.getBestFamilyName()
    new_family = orig_family + " KU"
    set_name(1, new_family)
    set_name(4, new_family)
    set_name(16, new_family)
    # Version string
    for rec in name_tbl.names:
        if rec.nameID == 5:
            try:
                old = rec.toUnicode()
            except Exception:
                old = ""
            rec.string = (old + " + ku-ext build").encode(rec.getEncoding())

    # 5. maxp numGlyphs
    font["maxp"].numGlyphs = len(glyph_order)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    font.save(out_path)
    size = os.path.getsize(out_path)
    print(f"   wrote {os.path.relpath(out_path, HERE)} ({size // 1024} kB)")

    # Verify
    t2 = TTFont(out_path)
    cm = t2.getBestCmap()
    missing = [cp for cp in NEW_LETTERS if cp not in cm]
    assert not missing, f"missing cmap: {missing}"
    print(f"   verified: all four Sorani letters present (ڕ ڵ ۆ ێ)")


if __name__ == "__main__":
    for style, fname in STYLES.items():
        src = os.path.join(SRC_DIR, fname)
        out = os.path.join(OUT_DIR, f"29LT_UA_Neo_{'B_KU' if style == 'B' else 'N_KU_' + style}.ttf")
        extend(style, src, out)
    print("\nDone. Extended fonts in build-fonts/dist/.")
    print("Reminder: these files are build-only and must NOT be published to the web.")
