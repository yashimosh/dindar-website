#!/usr/bin/env python3
"""Shape a line of text with HarfBuzz and return it as SVG path data.

The build machine shapes the text (with proper Arabic joining) and emits plain
vector outlines, so print files and pages carry shapes, not the font.

    from shape_svg import shape_to_path
    d, width, ascent, descent = shape_to_path(font_path, "پێم بڵێ", size=100)

Needs: fonttools 4.56.0, uharfbuzz 0.39.5
"""
import functools
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen


@functools.lru_cache(maxsize=8)
def _load(font_path):
    blob = hb.Blob.from_file_path(font_path)
    face = hb.Face(blob)
    font = hb.Font(face)
    tt = TTFont(font_path)
    return font, tt, tt.getGlyphSet(), tt["head"].unitsPerEm


def shape_to_path(font_path, text, size=100.0, direction="rtl", script="Arab",
                  language="ckb", tracking=0.0):
    """Return (svg_path_d, advance_width, ascent, descent) in output units.

    The path's origin is the start of the baseline at the LEFT edge, with y
    pointing down (SVG convention), so it can be dropped straight into an
    <svg viewBox="0 -ascent width ascent+descent">.
    """
    hb_font, tt, glyphset, upem = _load(font_path)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.direction = direction
    buf.script = script
    buf.language = language
    hb.shape(hb_font, buf, {"kern": True, "liga": True})

    scale = size / upem
    pen = SVGPathPen(glyphset)
    x = 0.0
    order = tt.getGlyphOrder()
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = order[info.codepoint]
        # flip y and scale; HarfBuzz output is already visual (left to right)
        t = TransformPen(pen, (scale, 0, 0, -scale,
                               (x + pos.x_offset) * scale,
                               -pos.y_offset * scale))
        glyphset[name].draw(t)
        x += pos.x_advance + tracking * upem / size if tracking else pos.x_advance
    hhea = tt["hhea"]
    return pen.getCommands(), x * scale, hhea.ascent * scale, -hhea.descent * scale


def missing_glyphs(font_path, text):
    """Codepoints in text that the font maps to .notdef."""
    _, tt, _, _ = _load(font_path)
    cmap = tt.getBestCmap()
    return sorted({c for c in text if not c.isspace() and ord(c) not in cmap})


def svg_line(font_path, text, size=100.0, fill="currentColor", **kw):
    """A complete standalone <svg> for one line of text."""
    d, w, asc, desc = shape_to_path(font_path, text, size, **kw)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {-asc:.1f} {w:.1f} {asc + desc:.1f}" '
            f'width="{w:.1f}" height="{asc + desc:.1f}"><path fill="{fill}" d="{d}"/></svg>')
