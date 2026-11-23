"""Shared visual design system, fonts, canvas framing, and layout anchors."""

from __future__ import annotations

import numpy as np
from manim import *

# Editorial warm whiteboard palette
BG_OUTER = "#E6E3DC"
BG_CANVAS = "#FCFBF8"
INK = "#16191F"
INK_MUTED = "#6B7280"
GRID_LIGHT = "#DDDAD0"
RULE_COLOR = "#D1CEC4"

# Semantic engineering colors
RED_POS = "#D9383A"
BLUE_NEG = "#2563EB"
AMBER_FW = "#E67E00"
AMBER_BAND = "#F59E0B"
TEAL_CUR = "#0D8A72"
VIOLET_MOD = "#7C3AED"
SHORT_RED = "#FF1A1A"

PHASE_U = "#D9383A"
PHASE_V = "#0D8A72"
PHASE_W = "#2563EB"

# 16:9 Artboard inside Manim's 14.222 x 8.0 frame
CANVAS_W = 13.44
CANVAS_H = 7.56
CANVAS_TL = np.array([-CANVAS_W / 2.0, CANVAS_H / 2.0, 0.0])

# Canonical layout coordinates shared across all stitched scenes
HBRIDGE_CENTER_SCALE = 0.96
HBRIDGE_CENTER_POS = np.array([0.0, 0.0, 0.0])

HBRIDGE_LEFT_SCALE = 0.62
HBRIDGE_LEFT_POS = np.array([-3.45, 0.0, 0.0])

HBRIDGE_TOPLEFT_SCALE = 0.50
HBRIDGE_TOPLEFT_POS = np.array([-3.45, 1.72, 0.0])

DERIV_CENTER = np.array([-3.45, -1.78, 0.0])

PLOT_RIGHT_X = 3.10
PLOT_RIGHT_W = 5.40

UT_CENTER_POS = np.array([PLOT_RIGHT_X, 0.0, 0.0])
UT_UPPER_POS = np.array([PLOT_RIGHT_X, 1.68, 0.0])
IT_LOWER_POS = np.array([PLOT_RIGHT_X, -1.68, 0.0])

GATE_S1_POS = np.array([PLOT_RIGHT_X, 1.55, 0.0])
GATE_S3_POS = np.array([PLOT_RIGHT_X, -1.45, 0.0])

# Global toggle configured after smoke test (xelatex vs latex/newtx)
TEX_BACKEND = "xelatex"


def get_times_tex_template() -> TexTemplate:
    """Return a Times New Roman LaTeX template for Manim MathTex."""
    if TEX_BACKEND == "xelatex":
        tpl = TexTemplate(tex_compiler="xelatex", output_format=".xdv")
        tpl.add_to_preamble(r"\usepackage{amsmath}")
        tpl.add_to_preamble(r"\usepackage{amssymb}")
        tpl.add_to_preamble(r"\usepackage{fontspec}")
        tpl.add_to_preamble(r"\usepackage{mathspec}")
        tpl.add_to_preamble(r"\setmainfont{Times New Roman}")
        tpl.add_to_preamble(r"\setmathsfont(Digits,Latin,Greek){Times New Roman}")
        return tpl

    tpl = TexTemplate(tex_compiler="latex", output_format=".dvi")
    tpl.add_to_preamble(r"\usepackage{amsmath}")
    tpl.add_to_preamble(r"\usepackage{amssymb}")
    tpl.add_to_preamble(r"\usepackage{newtxtext}")
    tpl.add_to_preamble(r"\usepackage{newtxmath}")
    return tpl


def math_tnr(tex: str, font_size: float = 34, color: str = INK) -> MathTex:
    """Create a MathTex equation rendered in Times New Roman."""
    return MathTex(tex, tex_template=get_times_tex_template(), font_size=font_size, color=color)


def zh_label(
    text: str,
    font_size: float = 22,
    color: str = INK,
    weight: str = MEDIUM,
) -> Text:
    """Create crisp Noto Sans SC Chinese annotation text."""
    return Text(text, font="Noto Sans SC", font_size=font_size, color=color, weight=weight)


def setup_canvas_scene(scene: Scene) -> None:
    """Set clean full-bleed warm-ivory drafting background with no frame or border."""
    scene.camera.background_color = BG_CANVAS


def sample_polyline_chevrons(
    points: list[np.ndarray],
    phase: float,
    color: str,
    n_markers: int = 14,
    size: float = 0.105,
) -> VGroup:
    """Return crisp directional chevrons evenly spaced and animated along EVERY segment of a polyline."""
    pts = [np.asarray(p, dtype=float) for p in points]
    segs = []
    total_len = 0.0
    for i in range(len(pts) - 1):
        d = pts[i + 1] - pts[i]
        ln = float(np.linalg.norm(d))
        if ln > 1e-6:
            segs.append((pts[i], pts[i + 1], d / ln, ln))
            total_len += ln
    if total_len < 1e-5:
        return VGroup()

    group = VGroup()
    n_segs = len(segs)
    for idx in range(n_markers):
        s_target = ((idx / n_markers + phase) % 1.0) * total_len
        acc = 0.0
        for seg_idx, (p0, _p1, tangent, seg_len) in enumerate(segs):
            if acc + seg_len >= s_target or seg_idx == n_segs - 1:
                local_s = max(0.0, min(seg_len, s_target - acc))
                pos = p0 + tangent * local_s
                ang = float(np.arctan2(tangent[1], tangent[0]))
                tri = Triangle(fill_color=color, fill_opacity=0.98, stroke_color="#FFFFFF", stroke_width=1.0)
                tri.scale(size)
                tri.rotate(ang - PI / 2.0)
                tri.move_to(pos)
                group.add(tri)
                break
            acc += seg_len
    return group


def make_status_pill(content: Mobject, accent_color: str, pad_x: float = 0.18, pad_y: float = 0.10) -> VGroup:
    """Create a sleek white pill badge with colored border around content."""
    box = RoundedRectangle(
        width=content.width + 2 * pad_x,
        height=content.height + 2 * pad_y,
        corner_radius=0.14,
        fill_color="#FFFFFF",
        fill_opacity=0.96,
        stroke_color=accent_color,
        stroke_width=1.8,
    )
    content.move_to(box.get_center())
    return VGroup(box, content)
