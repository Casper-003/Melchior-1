"""Semiconductor device physics & parameter animations for Slides 14, 16, 18, 19, 20.

Rendered on pure #FFFFFF white background with STZhongsong + Times New Roman so every clip
blends seamlessly onto the PowerPoint slide canvas without visible borders.
"""

from __future__ import annotations

import numpy as np
from manim import *

from style import get_times_tex_template

# Unified semiconductor palette (consistent across IGBT & 4H-SiC MOSFET)
BG_WHITE = "#FFFFFF"
NAVY = "#0E2841"
STEEL = "#1F4E79"
ICE = "#DCEAF7"
SLATE = "#64748B"
MUTED = "#595959"
INK = "#16191F"
TEAL = "#0F766E"
TEAL_LIGHT = "#DDF3F0"
CRIMSON = "#C00000"

# Semiconductor doping-concentration colors:
# N-type = Blue family (saturation proportional to donor concentration)
COL_N_PLUS = "#3A8FD6"     # High doping N+ (source wells, field-stop buffer, 4H-SiC substrate)
COL_N_SIC = "#A4D8FA"      # Medium-low doping N- (4H-SiC thin drift ~100x Si doping)
COL_N_MINUS = "#D8F0FF"    # Low doping N- (thick Si drift layer)
COL_N_PLASMA = "#C7E2F7"   # Modulated electron-hole plasma state in IGBT N- drift

# P-type = Rose-Pink family (saturation proportional to acceptor concentration)
COL_P_PLUS = "#D96288"     # High doping P+ (IGBT back-side collector)
COL_P_BODY = "#F5C4D4"     # Medium doping P (P-body / P-well)

# Insulator & Channel
COL_SIO2 = "#CBE6DC"
COL_SIO2_STROKE = "#2C7A68"
COL_CHANNEL = "#1D70B8"
COL_E_DOT = "#1D63B8"      # Electron solid blue sphere
COL_H_RING = "#C82855"     # Hole hollow rose-red ring
COL_GOLD = "#D98A00"       # Electric field indicator


def smootherstep(t: float) -> float:
    """Quintic ease-in-out: zero 1st & 2nd derivatives at t=0 and t=1."""
    t = max(0.0, min(1.0, float(t)))
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)


def cn_text(text: str, font_size: float = 22, color: str = INK, bold: bool = False) -> Text:
    return Text(
        text,
        font="STZhongsong",
        font_size=font_size,
        color=color,
        weight=BOLD if bold else NORMAL,
    )


def en_text(text: str, font_size: float = 22, color: str = INK, bold: bool = False) -> Text:
    return Text(
        text,
        font="Times New Roman",
        font_size=font_size,
        color=color,
        weight=BOLD if bold else NORMAL,
    )


def mtex(tex: str, font_size: float = 32, color: str = INK) -> MathTex:
    return MathTex(tex, tex_template=get_times_tex_template(), font_size=font_size, color=color)


def make_electron(pos: np.ndarray, r: float = 0.095) -> VGroup:
    dot = Circle(radius=r, fill_color=COL_E_DOT, fill_opacity=1.0, stroke_color="#FFFFFF", stroke_width=1.0)
    minus = Line(LEFT * (r * 0.52), RIGHT * (r * 0.52), color="#FFFFFF", stroke_width=1.8)
    g = VGroup(dot, minus)
    g.move_to(pos)
    return g


def make_hole(pos: np.ndarray, r: float = 0.095) -> VGroup:
    ring = Circle(radius=r, fill_color="#FFFFFF", fill_opacity=0.96, stroke_color=COL_H_RING, stroke_width=2.4)
    h_bar = Line(LEFT * (r * 0.48), RIGHT * (r * 0.48), color=COL_H_RING, stroke_width=1.6)
    v_bar = Line(DOWN * (r * 0.48), UP * (r * 0.48), color=COL_H_RING, stroke_width=1.6)
    g = VGroup(ring, h_bar, v_bar)
    g.move_to(pos)
    return g


def build_igbt_cell(center_x: float = -1.65, scale_f: float = 0.90) -> dict[str, Mobject]:
    """Construct a textbook-grade planar IGBT cross-section with consistent P-pink / N-blue shading."""
    w = 5.4 * scale_f
    y_em_top = 2.60 * scale_f
    y_top = 1.95 * scale_f
    y_nplus_bot = 1.45 * scale_f
    y_p_bot = 0.90 * scale_f
    y_drift_bot = -1.45 * scale_f
    y_buf_bot = -1.88 * scale_f
    y_pplus_bot = -2.45 * scale_f
    y_col_bot = -2.82 * scale_f

    n_drift = Rectangle(
        width=w,
        height=(y_top - y_drift_bot),
        fill_color=COL_N_MINUS,
        fill_opacity=1.0,
        stroke_color=NAVY,
        stroke_width=1.8,
    ).move_to([center_x, (y_top + y_drift_bot) / 2.0, 0])

    n_buf = Rectangle(
        width=w,
        height=(y_drift_bot - y_buf_bot),
        fill_color=COL_N_PLUS,
        fill_opacity=1.0,
        stroke_color=NAVY,
        stroke_width=1.5,
    ).move_to([center_x, (y_drift_bot + y_buf_bot) / 2.0, 0])

    p_plus = Rectangle(
        width=w,
        height=(y_buf_bot - y_pplus_bot),
        fill_color=COL_P_PLUS,
        fill_opacity=1.0,
        stroke_color=NAVY,
        stroke_width=1.8,
    ).move_to([center_x, (y_buf_bot + y_pplus_bot) / 2.0, 0])

    col_metal = Rectangle(
        width=w,
        height=(y_pplus_bot - y_col_bot),
        fill_color=NAVY,
        fill_opacity=1.0,
        stroke_color=NAVY,
        stroke_width=1.5,
    ).move_to([center_x, (y_pplus_bot + y_col_bot) / 2.0, 0])

    pw = 1.90 * scale_f
    ph = y_top - y_p_bot
    p_left = Rectangle(
        width=pw,
        height=ph,
        fill_color=COL_P_BODY,
        fill_opacity=1.0,
        stroke_color=NAVY,
        stroke_width=1.5,
    ).move_to([center_x - w / 2.0 + pw / 2.0, (y_top + y_p_bot) / 2.0, 0])
    p_right = p_left.copy().move_to([center_x + w / 2.0 - pw / 2.0, (y_top + y_p_bot) / 2.0, 0])

    nw = 0.85 * scale_f
    nh = y_top - y_nplus_bot
    n_left = Rectangle(
        width=nw,
        height=nh,
        fill_color=COL_N_PLUS,
        fill_opacity=1.0,
        stroke_color=NAVY,
        stroke_width=1.5,
    ).move_to([center_x - w / 2.0 + 1.15 * scale_f, (y_top + y_nplus_bot) / 2.0, 0])
    n_right = n_left.copy().move_to([center_x + w / 2.0 - 1.15 * scale_f, (y_top + y_nplus_bot) / 2.0, 0])

    ox_w = 2.68 * scale_f
    ox_h = 0.56 * scale_f
    sio2 = Rectangle(
        width=ox_w,
        height=ox_h,
        fill_color=COL_SIO2,
        fill_opacity=1.0,
        stroke_color=COL_SIO2_STROKE,
        stroke_width=1.8,
    ).move_to([center_x, y_top + ox_h / 2.0, 0])

    gate_w = 2.16 * scale_f
    gate_h = 0.30 * scale_f
    gate_metal = Rectangle(
        width=gate_w,
        height=gate_h,
        fill_color=STEEL,
        fill_opacity=1.0,
        stroke_color=NAVY,
        stroke_width=1.4,
    ).move_to([center_x, y_top + 0.36 * scale_f, 0])

    em_w = 1.25 * scale_f
    em_h = 0.34 * scale_f
    em_left = Rectangle(
        width=em_w,
        height=em_h,
        fill_color=NAVY,
        fill_opacity=1.0,
        stroke_color=NAVY,
        stroke_width=1.4,
    ).move_to([center_x - w / 2.0 + em_w / 2.0, y_top + em_h / 2.0, 0])
    em_right = em_left.copy().move_to([center_x + w / 2.0 - em_w / 2.0, y_top + em_h / 2.0, 0])

    em_bar = VMobject(stroke_color=NAVY, stroke_width=2.6)
    em_bar.set_points_as_corners([
        [center_x - w / 2.0 + 0.55 * scale_f, y_top + em_h, 0],
        [center_x - w / 2.0 + 0.55 * scale_f, y_em_top + 0.25 * scale_f, 0],
        [center_x + w / 2.0 - 0.55 * scale_f, y_em_top + 0.25 * scale_f, 0],
        [center_x + w / 2.0 - 0.55 * scale_f, y_top + em_h, 0],
    ])

    fs_s = 18 * scale_f
    lbl_nl = mtex(r"\mathrm{N^+}", font_size=fs_s, color="#FFFFFF").move_to(n_left)
    lbl_nr = mtex(r"\mathrm{N^+}", font_size=fs_s, color="#FFFFFF").move_to(n_right)
    lbl_pl = mtex(r"\mathrm{P}", font_size=fs_s, color=NAVY).move_to([p_left.get_left()[0] + 0.35 * scale_f, p_left.get_center()[1], 0])
    lbl_pr = mtex(r"\mathrm{P}", font_size=fs_s, color=NAVY).move_to([p_right.get_right()[0] - 0.35 * scale_f, p_right.get_center()[1], 0])
    lbl_drift = VGroup(
        mtex(r"\mathrm{N^-}", font_size=26 * scale_f, color=STEEL),
        cn_text("漂移区（低浓度）", font_size=17 * scale_f, color=STEEL),
    ).arrange(RIGHT, buff=0.12 * scale_f).move_to([center_x, -0.25 * scale_f, 0])
    lbl_buf = VGroup(
        mtex(r"\mathrm{N^+}", font_size=19 * scale_f, color="#FFFFFF"),
        cn_text("缓冲层", font_size=15 * scale_f, color="#FFFFFF"),
    ).arrange(RIGHT, buff=0.10 * scale_f).move_to(n_buf)
    lbl_pplus = VGroup(
        mtex(r"\mathrm{P^+}", font_size=21 * scale_f, color="#FFFFFF"),
        cn_text("背面集电区（高浓度）", font_size=16 * scale_f, color="#FFFFFF"),
    ).arrange(RIGHT, buff=0.10 * scale_f).move_to(p_plus)
    lbl_col = cn_text("集电极 C", font_size=16 * scale_f, color="#FFFFFF", bold=True).move_to(col_metal)
    lbl_gate = cn_text("栅极 G", font_size=15 * scale_f, color="#FFFFFF", bold=True).move_to(gate_metal)
    lbl_sio2 = mtex(r"\mathrm{SiO_2}", font_size=14 * scale_f, color=COL_SIO2_STROKE).move_to([center_x, y_top + 0.11 * scale_f, 0])
    lbl_em = cn_text("发射极 E", font_size=16 * scale_f, color=NAVY, bold=True).next_to(em_bar, UP, buff=0.06 * scale_f)

    ch_h = 0.13 * scale_f
    ch_left = Rectangle(
        width=0.33 * scale_f,
        height=ch_h,
        fill_color=COL_CHANNEL,
        fill_opacity=0.95,
        stroke_width=0,
    ).move_to([center_x - w / 2.0 + 1.735 * scale_f, y_top - ch_h / 2.0, 0])
    ch_right = ch_left.copy().move_to([center_x + w / 2.0 - 1.735 * scale_f, y_top - ch_h / 2.0, 0])

    all_static = VGroup(
        n_drift, n_buf, p_plus, col_metal,
        p_left, p_right, n_left, n_right,
        sio2, gate_metal, em_left, em_right, em_bar,
        lbl_nl, lbl_nr, lbl_pl, lbl_pr, lbl_drift, lbl_buf, lbl_pplus, lbl_col, lbl_gate, lbl_sio2, lbl_em,
    )

    return {
        "static": all_static,
        "n_drift": n_drift,
        "lbl_drift": lbl_drift,
        "p_plus": p_plus,
        "gate_metal": gate_metal,
        "sio2": sio2,
        "ch_left": ch_left,
        "ch_right": ch_right,
        "cx": center_x,
        "w": w,
        "y_top": y_top,
        "y_drift_bot": y_drift_bot,
        "y_buf_bot": y_buf_bot,
        "scale": scale_f,
    }


def build_doping_legend(x_left: float = 1.65, y_top: float = 3.05) -> VGroup:
    """Clean color-concentration legend for P/N regions & carriers."""
    title = cn_text("掺杂浓度与载流子图例", font_size=17, color=NAVY, bold=True)
    items = [
        (COL_P_PLUS, NAVY, r"\mathrm{P^+}", "高浓度 P 型"),
        (COL_P_BODY, NAVY, r"\mathrm{P}", "中浓度 P 型"),
        (COL_N_PLUS, NAVY, r"\mathrm{N^+}", "高浓度 N 型"),
        (COL_N_MINUS, NAVY, r"\mathrm{N^-}", "低浓度 N 型"),
    ]
    rows = VGroup()
    for fill_c, strk, sym, desc in items:
        sw = Rectangle(width=0.44, height=0.25, fill_color=fill_c, fill_opacity=1.0, stroke_color=strk, stroke_width=1.2)
        t_sym = mtex(sym, font_size=20, color=NAVY)
        t_desc = cn_text(desc, font_size=15.5, color=INK)
        row = VGroup(sw, t_sym, t_desc).arrange(RIGHT, buff=0.14)
        rows.add(row)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12)

    e_row = VGroup(make_electron(ORIGIN, r=0.095), mtex(r"e^-", font_size=20, color=COL_E_DOT), cn_text("电子", font_size=15.5, color=COL_E_DOT, bold=True)).arrange(RIGHT, buff=0.12)
    h_row = VGroup(make_hole(ORIGIN, r=0.095), mtex(r"h^+", font_size=20, color=COL_H_RING), cn_text("空穴", font_size=15.5, color=COL_H_RING, bold=True)).arrange(RIGHT, buff=0.12)
    car_row = VGroup(e_row, h_row).arrange(RIGHT, buff=0.42)

    content = VGroup(title, rows, car_row).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    box = Rectangle(
        width=4.45,
        height=content.height + 0.34,
        fill_color="#F8FAFC",
        fill_opacity=1.0,
        stroke_color=ICE,
        stroke_width=1.6,
    )
    content.move_to(box.get_center())
    grp = VGroup(box, content)
    grp.move_to([x_left + box.width / 2.0, y_top - box.height / 2.0, 0])
    return grp


# ==============================================================================
# SCENE 1 (Slide 14): IGBT Structure & Conductivity Modulation
# ==============================================================================
class IGBTConductionScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG_WHITE

        hdr = cn_text("硅 IGBT 纵向结构与电导调制导通原理", font_size=24, color=NAVY, bold=True)
        hdr.to_corner(UL, buff=0.32).shift(RIGHT * 0.15)
        rule = Line(hdr.get_left() + DOWN * 0.26, hdr.get_left() + RIGHT * 12.6 + DOWN * 0.26, color=ICE, stroke_width=2.0)

        cell = build_igbt_cell(center_x=-1.65, scale_f=0.90)
        legend = build_doping_legend(x_left=1.65, y_top=3.00)

        cx = cell["cx"]
        sc = cell["scale"]
        vge_pill = VGroup(
            Rectangle(width=1.80, height=0.44, fill_color=ICE, fill_opacity=1.0, stroke_color=STEEL, stroke_width=1.4),
            mtex(r"V_{\mathrm{GE}} > V_{\mathrm{th}}", font_size=21, color=NAVY),
        )
        vge_pill[1].move_to(vge_pill[0])
        vge_pill.move_to([cx - 3.65, 2.05, 0])
        vge_arr = Arrow(vge_pill.get_right(), [cx - 0.98, 2.08, 0], buff=0.06, color=STEEL, stroke_width=2.4, tip_length=0.15)

        vce_lbl = mtex(r"+V_{\mathrm{CE}}", font_size=24, color=CRIMSON).move_to([cx - 3.65, -1.95, 0])
        vce_wire = VMobject(stroke_color=NAVY, stroke_width=1.8)
        vce_wire.set_points_as_corners([
            [cx - 2.43, -2.35, 0],
            [cx - 3.65, -2.35, 0],
            [cx - 3.65, -2.20, 0],
        ])

        s1_txt = cn_text("① 栅极加正压，P 区表面形成反型沟道", font_size=16, color=MUTED)
        s2_txt = VGroup(cn_text("② 电子经沟道注入", font_size=16, color=MUTED), mtex(r"\mathrm{N^-}", font_size=18, color=MUTED), cn_text("漂移区", font_size=16, color=MUTED)).arrange(RIGHT, buff=0.06)
        s3_txt = VGroup(cn_text("③ 背面", font_size=16, color=MUTED), mtex(r"\mathrm{P^+/N^-}", font_size=18, color=MUTED), cn_text("结正偏，空穴向上注入", font_size=16, color=MUTED)).arrange(RIGHT, buff=0.06)
        steps_grp = VGroup(s1_txt, s2_txt, s3_txt).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        steps_grp.move_to([3.88, -0.38, 0])

        eq_box = Rectangle(width=4.45, height=1.35, fill_color=NAVY, fill_opacity=1.0, stroke_width=0)
        eq_top = cn_text("电导调制 · 漂移区电中性条件", font_size=15, color=ICE)
        eq_math = mtex(r"n \approx p \gg N_D", font_size=38, color="#FFFFFF")
        eq_sub = cn_text("降低厚漂移区电阻，兼顾耐压与低导通压降", font_size=13.5, color=ICE)
        eq_inner = VGroup(eq_top, eq_math, eq_sub).arrange(DOWN, buff=0.10)
        eq_inner.move_to(eq_box)
        eq_grp = VGroup(eq_box, eq_inner).move_to([3.88, -2.18, 0])

        self.add(hdr, rule, cell["static"], legend, steps_grp)
        self.wait(1.0)

        # Stage 1: +V_GE -> positive gate charges + E-field across SiO2 + inversion channels
        plus_charges = VGroup(*[
            en_text("+", font_size=17, color=CRIMSON, bold=True).move_to([cx + dx, cell["y_top"] + 0.24 * sc, 0])
            for dx in np.linspace(-0.78, 0.78, 7)
        ])
        efield_arrows = VGroup(*[
            Arrow(
                [cx + dx, cell["y_top"] + 0.15 * sc, 0],
                [cx + dx, cell["y_top"] - 0.02 * sc, 0],
                buff=0,
                color=COL_GOLD,
                stroke_width=2.0,
                tip_length=0.08,
            )
            for dx in [-0.66, -0.33, 0.0, 0.33, 0.66]
        ])

        self.play(
            FadeIn(vge_pill, shift=RIGHT * 0.15),
            GrowArrow(vge_arr),
            FadeIn(vce_lbl),
            Create(vce_wire),
            s1_txt.animate.set_color(NAVY),
            run_time=0.8,
        )
        self.play(FadeIn(plus_charges), FadeIn(efield_arrows), run_time=0.6)
        self.play(
            GrowFromEdge(cell["ch_left"], LEFT),
            GrowFromEdge(cell["ch_right"], RIGHT),
            run_time=0.9,
            rate_func=smootherstep,
        )
        ch_lbl = cn_text("N 型反型沟道", font_size=13.5, color=COL_CHANNEL, bold=True).move_to([cx, cell["y_top"] - 0.32 * sc, 0])
        self.play(FadeIn(ch_lbl), run_time=0.4)
        self.wait(0.4)

        # Stage 2: Curved electron streams flowing from N+ through surface channel down into N- drift
        self.play(s2_txt.animate.set_color(COL_E_DOT), run_time=0.4)

        def make_e_path(side: int, x_end_offset: float) -> VMobject:
            p = VMobject()
            x_start = cx + side * 1.35 * sc
            x_ch = cx + side * 0.85 * sc
            x_neck = cx + side * 0.45 * sc
            x_end = cx + x_end_offset * sc
            y_ch = cell["y_top"] - 0.08 * sc
            p.set_points_smoothly([
                [x_start, y_ch - 0.08 * sc, 0],
                [x_ch, y_ch, 0],
                [x_neck, cell["y_top"] - 0.50 * sc, 0],
                [x_end, -0.25 * sc, 0],
                [x_end, -1.25 * sc, 0],
            ])
            return p

        e_paths = [
            make_e_path(-1, -1.55),
            make_e_path(-1, -0.75),
            make_e_path(-1, -0.20),
            make_e_path(+1, +0.20),
            make_e_path(+1, +0.75),
            make_e_path(+1, +1.55),
        ]
        e_guides = VGroup(*[
            DashedVMobject(p, num_dashes=10, dashed_ratio=0.55).set_stroke(COL_E_DOT, width=1.4, opacity=0.45)
            for p in e_paths
        ])
        e_dots = [make_electron(p.get_start(), r=0.085) for p in e_paths]
        self.play(FadeIn(e_guides), *[FadeIn(d) for d in e_dots], run_time=0.4)
        self.play(*[MoveAlongPath(d, p, rate_func=smootherstep) for d, p in zip(e_dots, e_paths)], run_time=2.1)

        # Stage 3: Back-side P+/N- junction forward bias -> hole injection upward + plasma modulation
        self.play(s3_txt.animate.set_color(COL_H_RING), run_time=0.4)
        junc_line = Line(
            [cx - cell["w"] / 2.0, cell["y_buf_bot"], 0],
            [cx + cell["w"] / 2.0, cell["y_buf_bot"], 0],
            color=CRIMSON,
            stroke_width=3.5,
        )
        junc_tag = VGroup(mtex(r"\mathrm{P^+/N^-}", font_size=18, color=CRIMSON), cn_text("结正偏", font_size=14, color=CRIMSON, bold=True)).arrange(RIGHT, buff=0.05)
        junc_tag.move_to([cx - 3.65, cell["y_buf_bot"] + 0.16, 0])
        junc_ptr = Arrow(junc_tag.get_right(), [cx - cell["w"] / 2.0 + 0.05, cell["y_buf_bot"], 0], buff=0.06, color=CRIMSON, stroke_width=2.0, tip_length=0.12)
        self.play(Create(junc_line), FadeIn(junc_tag), GrowArrow(junc_ptr), run_time=0.5)

        h_x_list = [-1.85, -1.10, -0.38, 0.38, 1.10, 1.85]
        h_paths = []
        h_dots = []
        for idx, hx in enumerate(h_x_list):
            hp = Line([cx + hx * sc, -1.95 * sc, 0], [cx + hx * sc, (0.50 - (idx % 2) * 0.42) * sc, 0])
            h_paths.append(hp)
            h_dots.append(make_hole(hp.get_start(), r=0.085))

        e_wave2 = [make_electron(p.get_start(), r=0.085) for p in e_paths]
        self.play(*[FadeIn(h) for h in h_dots], *[FadeIn(e) for e in e_wave2], run_time=0.35)
        self.play(
            *[MoveAlongPath(h, hp, rate_func=smootherstep) for h, hp in zip(h_dots, h_paths)],
            *[MoveAlongPath(e, ep, rate_func=smootherstep) for e, ep in zip(e_wave2, e_paths)],
            cell["n_drift"].animate.set_fill(COL_N_PLASMA, opacity=1.0),
            run_time=2.3,
        )

        plasma_lbl = cn_text("高浓度电子–空穴等离子体", font_size=15.5, color=NAVY, bold=True).move_to([cx, -0.22 * sc, 0])
        plasma_bg = Rectangle(
            width=plasma_lbl.width + 0.34,
            height=0.42,
            fill_color="#FFFFFF",
            fill_opacity=0.92,
            stroke_color=COL_H_RING,
            stroke_width=1.3,
        ).move_to(plasma_lbl)

        self.play(
            FadeOut(cell["lbl_drift"]),
            FadeIn(plasma_bg),
            FadeIn(plasma_lbl),
            FadeIn(eq_grp, shift=UP * 0.16),
            run_time=0.9,
        )
        self.wait(1.5)


# ==============================================================================
# SCENE 2 (Slide 16): IGBT Turn-Off Process & Tail Current
# ==============================================================================
class IGBTTurnOffTailScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG_WHITE

        hdr = cn_text("IGBT 关断过程：沟道关断、载流子扫出与少子复合拖尾", font_size=23, color=NAVY, bold=True)
        hdr.to_corner(UL, buff=0.32).shift(RIGHT * 0.15)
        rule = Line(hdr.get_left() + DOWN * 0.26, hdr.get_left() + RIGHT * 12.6 + DOWN * 0.26, color=ICE, stroke_width=2.0)

        cell = build_igbt_cell(center_x=-3.25, scale_f=0.78)
        cell["n_drift"].set_fill(COL_N_PLASMA, opacity=1.0)
        cell["lbl_drift"].set_opacity(0.0)
        cx = cell["cx"]
        sc = cell["scale"]

        shallow_pos = [(-1.4, 0.45), (-0.7, 0.30), (0.0, 0.48), (0.7, 0.32), (1.4, 0.45)]
        deep_pos = [(-1.5, -0.35), (-0.8, -0.75), (-0.1, -0.25), (0.6, -0.70), (1.3, -0.30), (-1.1, -0.90), (0.3, -0.92), (1.4, -0.82)]

        shallow_e = VGroup(*[make_electron([cx + dx * sc, dy * sc, 0], r=0.072) for dx, dy in shallow_pos])
        shallow_h = VGroup(*[make_hole([cx + (dx + 0.18) * sc, (dy - 0.16) * sc, 0], r=0.072) for dx, dy in shallow_pos])
        deep_e = VGroup(*[make_electron([cx + dx * sc, dy * sc, 0], r=0.072) for dx, dy in deep_pos])
        deep_h = VGroup(*[make_hole([cx + (dx + 0.18) * sc, (dy - 0.14) * sc, 0], r=0.072) for dx, dy in deep_pos])

        ax_orig = np.array([0.45, -0.45, 0.0])
        ax_x_end = np.array([6.25, -0.45, 0.0])
        ax_y_end = np.array([0.45, 2.55, 0.0])

        ax_x = Arrow(ax_orig, ax_x_end, buff=0, color=NAVY, stroke_width=2.0, tip_length=0.16)
        ax_y = Arrow(ax_orig, ax_y_end, buff=0, color=NAVY, stroke_width=2.0, tip_length=0.16)
        lbl_t = mtex("t", font_size=24, color=NAVY).next_to(ax_x_end, DOWN, buff=0.08)
        lbl_y = mtex(r"V_{\mathrm{CE}},\ I_{\mathrm{C}}", font_size=22, color=NAVY).next_to(ax_y_end, RIGHT, buff=0.10)

        y_u = 2.05
        u_dash = DashedLine([ax_orig[0], y_u, 0], [6.05, y_u, 0], color=SLATE, stroke_width=1.2)
        u_lbl = mtex("U", font_size=22, color=NAVY).next_to(u_dash.get_left(), LEFT, buff=0.10)

        vce_p0 = Line([0.50, -0.32, 0], [1.45, -0.32, 0], color=NAVY, stroke_width=3.0)
        vce_p1 = Line([1.45, -0.32, 0], [2.15, y_u, 0], color=NAVY, stroke_width=3.0)
        vce_p2 = Line([2.15, y_u, 0], [5.85, y_u, 0], color=NAVY, stroke_width=3.0)

        ic_p0 = Line([0.50, 1.80, 0], [1.80, 1.80, 0], color=CRIMSON, stroke_width=3.2)
        ic_p1 = Line([1.80, 1.80, 0], [2.55, 0.56, 0], color=CRIMSON, stroke_width=3.2)
        tail_pts = []
        for s in np.linspace(0.0, 1.0, 28):
            tx = 2.55 + s * 3.25
            ty = -0.43 + 0.99 * np.exp(-3.1 * s)
            tail_pts.append([tx, ty, 0.0])
        ic_p2 = VMobject(stroke_color=CRIMSON, stroke_width=3.2)
        ic_p2.set_points_smoothly(tail_pts)

        eoff_poly_pts = [[1.55, -0.45, 0.0], [1.80, 1.80, 0.0], [2.55, 0.56, 0.0]] + tail_pts + [[5.80, -0.45, 0.0]]
        eoff_area = Polygon(*eoff_poly_pts, fill_color=CRIMSON, fill_opacity=0.16, stroke_width=0)

        leg_vce = VGroup(Line(ORIGIN, RIGHT * 0.35, color=NAVY, stroke_width=3.0), mtex(r"V_{\mathrm{CE}}(t)", font_size=20, color=NAVY)).arrange(RIGHT, buff=0.08)
        leg_ic = VGroup(Line(ORIGIN, RIGHT * 0.35, color=CRIMSON, stroke_width=3.2), mtex(r"I_{\mathrm{C}}(t)", font_size=20, color=CRIMSON)).arrange(RIGHT, buff=0.08)
        wf_leg = VGroup(leg_vce, leg_ic).arrange(RIGHT, buff=0.36).move_to([4.55, 2.46, 0])

        n1 = cn_text("① 撤除栅压：反型沟道关闭，电子停止注入", font_size=15.5, color=MUTED)
        n2 = cn_text("② 浅层扫出：电流速降，端电压升至母线电压 U", font_size=15.5, color=MUTED)
        n3 = VGroup(cn_text("③ 少子复合：残余载流子缓慢衰减，产生拖尾与", font_size=15.5, color=MUTED), mtex(r"E_{\mathrm{off}}", font_size=20, color=MUTED)).arrange(RIGHT, buff=0.06)
        n4 = cn_text("   温度升高使载流子寿命延长，拖尾加重（约 10 kHz 上限）", font_size=14, color=SLATE)
        notes = VGroup(n1, n2, n3, n4).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.20, -2.02, 0])

        self.add(
            hdr, rule, cell["static"], cell["ch_left"], cell["ch_right"],
            shallow_e, shallow_h, deep_e, deep_h,
            ax_x, ax_y, lbl_t, lbl_y, u_dash, u_lbl, wf_leg, notes,
        )
        self.play(Create(vce_p0), Create(ic_p0), run_time=0.8)
        self.wait(0.4)

        cross_l = VGroup(
            Line([-0.11, -0.11, 0], [0.11, 0.11, 0], color=CRIMSON, stroke_width=3.0),
            Line([-0.11, 0.11, 0], [0.11, -0.11, 0], color=CRIMSON, stroke_width=3.0),
        ).move_to(cell["ch_left"])
        cross_r = cross_l.copy().move_to(cell["ch_right"])
        vge0_tag = VGroup(
            Rectangle(width=1.28, height=0.40, fill_color=ICE, fill_opacity=1.0, stroke_color=CRIMSON, stroke_width=1.3),
            mtex(r"V_{\mathrm{GE}} = 0", font_size=18.5, color=CRIMSON),
        )
        vge0_tag[1].move_to(vge0_tag[0])
        vge0_tag.move_to([cx - 2.82, 1.55, 0])

        self.play(
            FadeOut(cell["ch_left"]),
            FadeOut(cell["ch_right"]),
            FadeIn(cross_l),
            FadeIn(cross_r),
            FadeIn(vge0_tag),
            n1.animate.set_color(NAVY),
            run_time=0.8,
        )

        self.play(
            Create(vce_p1),
            Create(ic_p1),
            shallow_e.animate.shift(DOWN * 0.40).set_opacity(0.0),
            shallow_h.animate.shift(UP * 0.40).set_opacity(0.0),
            n2.animate.set_color(NAVY),
            run_time=1.7,
            rate_func=smootherstep,
        )

        tail_tag = VGroup(
            cn_text("拖尾电流", font_size=16, color=CRIMSON, bold=True),
            mtex(r"E_{\mathrm{off}}", font_size=25, color=CRIMSON),
        ).arrange(DOWN, buff=0.05).move_to([3.55, 0.68, 0])

        recomb_anims = []
        for e_dot, h_dot in zip(deep_e, deep_h):
            mid = (e_dot.get_center() + h_dot.get_center()) / 2.0
            recomb_anims.append(e_dot.animate.move_to(mid).set_opacity(0.0))
            recomb_anims.append(h_dot.animate.move_to(mid).set_opacity(0.0))

        self.play(
            Create(vce_p2),
            Create(ic_p2, rate_func=smootherstep),
            FadeIn(eoff_area, rate_func=smootherstep),
            *recomb_anims,
            cell["n_drift"].animate.set_fill(COL_N_MINUS, opacity=1.0),
            n3.animate.set_color(CRIMSON),
            run_time=3.5,
        )
        self.play(FadeIn(tail_tag), n4.animate.set_color(INK), run_time=0.6)
        self.wait(1.6)


# ==============================================================================
# SCENE 3 (Slide 18): 4H-SiC & Si Core Material Parameters (Nonlinear Rising Bars)
# ==============================================================================
class SiCParamsBarsScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG_WHITE

        hdr = cn_text("硅与 4H-SiC 核心材料参数对比", font_size=25, color=NAVY, bold=True)
        hdr.to_corner(UL, buff=0.34).shift(RIGHT * 0.20)
        rule = Line(hdr.get_left() + DOWN * 0.28, hdr.get_left() + RIGHT * 12.5 + DOWN * 0.28, color=ICE, stroke_width=2.0)

        sw_si = Rectangle(width=0.38, height=0.22, fill_color=SLATE, fill_opacity=1.0, stroke_width=0)
        t_si = cn_text("硅 Si", font_size=18, color=SLATE, bold=True)
        sw_sic = Rectangle(width=0.38, height=0.22, fill_color=NAVY, fill_opacity=1.0, stroke_width=0)
        t_sic = cn_text("4H-SiC", font_size=18, color=NAVY, bold=True)
        leg = VGroup(VGroup(sw_si, t_si).arrange(RIGHT, buff=0.10), VGroup(sw_sic, t_sic).arrange(RIGHT, buff=0.10)).arrange(RIGHT, buff=0.45)
        leg.to_corner(UR, buff=0.38).shift(LEFT * 0.25)

        self.add(hdr, rule, leg)

        groups = [
            {
                "cx": -4.25,
                "title": "禁带宽度",
                "sym": r"E_g\ (\mathrm{eV})",
                "si_val": 1.12,
                "sic_val": 3.26,
                "max_val": 3.80,
                "fmt": "{:.2f}",
                "ratio": "约 3 倍",
                "sic_col": NAVY,
                "note": "宽禁带抑制本征载流子热激发",
            },
            {
                "cx": 0.0,
                "title": "临界击穿场强",
                "sym": r"E_c\ (\mathrm{MV/cm})",
                "si_val": 0.30,
                "sic_val": 3.00,
                "max_val": 3.50,
                "fmt": "{:.1f}",
                "ratio": "约 10 倍",
                "sic_col": TEAL,
                "note": "同耐压下所需漂移层明显更薄",
            },
            {
                "cx": 4.25,
                "title": "1200 V 理想漂移层厚度",
                "sym": r"W\ (\mu\mathrm{m})",
                "si_val": 80.0,
                "sic_val": 8.0,
                "max_val": 92.0,
                "fmt": "{:.0f}",
                "ratio": "约 1/10",
                "sic_col": STEEL,
                "note": "实际器件约 10 μm · 掺杂提高约百倍",
            },
        ]

        y_base = -2.10
        max_h = 3.20
        bar_w = 0.86
        gap = 0.44

        for g in groups:
            cx = g["cx"]
            base_ln = Line([cx - 1.55, y_base, 0], [cx + 1.55, y_base, 0], color=NAVY, stroke_width=2.0)
            t_main = cn_text(g["title"], font_size=19.5, color=NAVY, bold=True)
            t_sym = mtex(g["sym"], font_size=21, color=STEEL)
            g_hdr = VGroup(t_main, t_sym).arrange(DOWN, buff=0.06).move_to([cx, 2.38, 0])
            l_si = cn_text("硅 Si", font_size=16, color=SLATE, bold=True).move_to([cx - (bar_w + gap) / 2.0, y_base - 0.30, 0])
            l_sic = en_text("4H-SiC", font_size=16, color=NAVY, bold=True).move_to([cx + (bar_w + gap) / 2.0, y_base - 0.30, 0])
            note = cn_text(g["note"], font_size=14, color=MUTED).move_to([cx, y_base - 0.78, 0])
            self.add(base_ln, g_hdr, l_si, l_sic, note)

        self.add(
            Line([-2.12, -2.95, 0], [-2.12, 2.65, 0], color=ICE, stroke_width=1.4),
            Line([2.12, -2.95, 0], [2.12, 2.65, 0], color=ICE, stroke_width=1.4),
        )
        self.wait(0.4)

        for g in groups:
            cx = g["cx"]
            x_si = cx - (bar_w + gap) / 2.0
            x_sic = cx + (bar_w + gap) / 2.0
            h_si_target = max_h * (g["si_val"] / g["max_val"])
            h_sic_target = max_h * (g["sic_val"] / g["max_val"])
            fmt = g["fmt"]

            prog = ValueTracker(0.0)

            def make_bar_updater(x_pos: float, target_h: float, col: str, trk: ValueTracker = prog) -> Mobject:
                def _build() -> Rectangle:
                    h = max(0.02, target_h * trk.get_value())
                    r = Rectangle(
                        width=bar_w,
                        height=h,
                        fill_color=col,
                        fill_opacity=1.0,
                        stroke_color=NAVY,
                        stroke_width=1.0,
                    )
                    r.move_to([x_pos, y_base + h / 2.0, 0])
                    return r
                return always_redraw(_build)

            def make_val_updater(x_pos: float, target_h: float, target_v: float, col: str, trk: ValueTracker = prog, f_str: str = fmt) -> Mobject:
                def _build() -> Text:
                    p = trk.get_value()
                    h = max(0.02, target_h * p)
                    v = target_v * p
                    t = en_text(f_str.format(v), font_size=22, color=col, bold=True)
                    t.move_to([x_pos, y_base + h + 0.24, 0])
                    return t
                return always_redraw(_build)

            b_si = make_bar_updater(x_si, h_si_target, SLATE)
            b_sic = make_bar_updater(x_sic, h_sic_target, g["sic_col"])
            v_si = make_val_updater(x_si, h_si_target, g["si_val"], SLATE)
            v_sic = make_val_updater(x_sic, h_sic_target, g["sic_val"], g["sic_col"])

            self.add(b_si, b_sic, v_si, v_sic)
            self.play(prog.animate.set_value(1.0), run_time=2.2, rate_func=smootherstep)

            pill_bg = Rectangle(width=1.45, height=0.40, fill_color=ICE, fill_opacity=1.0, stroke_color=g["sic_col"], stroke_width=1.4)
            pill_t = cn_text(g["ratio"], font_size=17, color=g["sic_col"], bold=True)
            pill = VGroup(pill_bg, pill_t)
            pill_t.move_to(pill_bg)
            pill.move_to([cx, 1.45, 0])
            self.play(FadeIn(pill, shift=UP * 0.10), run_time=0.45)

        self.wait(1.6)


# ==============================================================================
# SCENE 4 (Slide 19): 1D Triangular Electric Field & Depletion Width (1200 V)
# ==============================================================================
class SiCEFieldTriangleScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG_WHITE

        hdr = cn_text("一维近似下的三角形电场分布（以 1200 V 耐压为例）", font_size=24, color=NAVY, bold=True)
        hdr.to_corner(UL, buff=0.32).shift(RIGHT * 0.15)
        rule = Line(hdr.get_left() + DOWN * 0.26, hdr.get_left() + RIGHT * 12.6 + DOWN * 0.26, color=ICE, stroke_width=2.0)

        x0 = -4.55
        scale_x = 0.11
        w80 = 80.0 * scale_x
        w8 = 8.0 * scale_x

        y_geo_mid = 1.98
        geo_h = 0.70
        p_zone = Rectangle(width=0.76, height=geo_h, fill_color=COL_P_BODY, fill_opacity=1.0, stroke_color=NAVY, stroke_width=1.4)
        p_zone.move_to([x0 - 0.38, y_geo_mid, 0])
        p_lbl = mtex(r"\mathrm{P}", font_size=22, color=NAVY).move_to(p_zone)

        si_drift_bar = Rectangle(width=w80, height=geo_h, fill_color=COL_N_MINUS, fill_opacity=1.0, stroke_color=NAVY, stroke_width=1.4)
        si_drift_bar.move_to([x0 + w80 / 2.0, y_geo_mid, 0])
        si_drift_lbl = VGroup(
            cn_text("硅", font_size=16, color=STEEL, bold=True),
            mtex(r"\mathrm{N^-}", font_size=20, color=STEEL),
            cn_text("漂移区：", font_size=16, color=STEEL, bold=True),
            mtex(r"W \approx 80\,\mu\mathrm{m}", font_size=20, color=STEEL),
            cn_text("（低掺杂）", font_size=15, color=STEEL),
        ).arrange(RIGHT, buff=0.06).move_to(si_drift_bar)

        nplus_si = Rectangle(width=0.70, height=geo_h, fill_color=COL_N_PLUS, fill_opacity=1.0, stroke_color=NAVY, stroke_width=1.4)
        nplus_si.move_to([x0 + w80 + 0.35, y_geo_mid, 0])
        nplus_si_lbl = mtex(r"\mathrm{N^+}", font_size=18, color="#FFFFFF").move_to(nplus_si)

        junc_dash = DashedLine([x0, y_geo_mid - geo_h / 2.0, 0], [x0, -2.55, 0], color=SLATE, stroke_width=1.2)
        junc_lbl = cn_text("PN 结界面 x = 0", font_size=13.5, color=SLATE, bold=True).move_to([x0 - 0.65, y_geo_mid + 0.56, 0])

        y0 = -2.35
        scale_e = 1.12
        h03 = 0.3 * scale_e
        h30 = 3.0 * scale_e

        ax_x = Arrow([x0, y0, 0], [x0 + w80 + 0.80, y0, 0], buff=0, color=NAVY, stroke_width=2.0, tip_length=0.16)
        ax_y = Arrow([x0, y0, 0], [x0, y0 + h30 + 0.32, 0], buff=0, color=NAVY, stroke_width=2.0, tip_length=0.16)
        lbl_ax_x = VGroup(cn_text("漂移区位置", font_size=16, color=NAVY, bold=True), mtex(r"x\ (\mu\mathrm{m})", font_size=20, color=NAVY)).arrange(RIGHT, buff=0.08)
        lbl_ax_x.move_to([x0 + w80 / 2.0, y0 - 0.52, 0])
        lbl_ax_y = VGroup(mtex(r"E(x)", font_size=21, color=NAVY), cn_text("(MV/cm)", font_size=13.5, color=STEEL, bold=True)).arrange(RIGHT, buff=0.08)
        lbl_ax_y.move_to([x0 + 1.05, y0 + h30 + 0.22, 0])

        t_03 = en_text("0.3", font_size=18, color=SLATE, bold=True).move_to([x0 - 0.42, y0 + h03, 0])
        t_30 = en_text("3.0", font_size=18, color=TEAL, bold=True).move_to([x0 - 0.42, y0 + h30, 0])
        t_80 = en_text("80 μm", font_size=17, color=SLATE, bold=True).move_to([x0 + w80, y0 - 0.24, 0])
        t_8 = en_text("8 μm", font_size=17, color=TEAL, bold=True).move_to([x0 + w8 + 0.15, y0 - 0.24, 0])

        eq_box = Rectangle(width=5.15, height=1.50, fill_color="#F8FAFC", fill_opacity=1.0, stroke_color=NAVY, stroke_width=1.4)
        eq_f = mtex(r"V_{\mathrm{BR}} = \int_0^W E(x)\,\mathrm{d}x = \frac{1}{2} E_{\mathrm{peak}} \cdot W", font_size=26, color=NAVY)
        eq_sub = cn_text("三角形面积 = 器件阻断电压（均按 1200 V 计算）", font_size=14.5, color=STEEL, bold=True)
        eq_inner = VGroup(eq_f, eq_sub).arrange(DOWN, buff=0.14).move_to(eq_box)
        eq_grp = VGroup(eq_box, eq_inner).move_to([3.08, 0.35, 0])

        tri_si = Polygon(
            [x0, y0, 0],
            [x0, y0 + h03, 0],
            [x0 + w80, y0, 0],
            fill_color=SLATE,
            fill_opacity=0.25,
            stroke_color=SLATE,
            stroke_width=2.4,
        )
        si_tri_tag = cn_text("硅 Si：峰值 0.3 MV/cm × 厚度 80 μm → 面积 = 1200 V", font_size=16, color=SLATE, bold=True)
        si_tri_tag.move_to([x0 + w80 * 0.56, y0 + h03 + 0.32, 0])

        self.add(hdr, rule, ax_x, ax_y, lbl_ax_x, lbl_ax_y, p_zone, p_lbl, junc_dash, junc_lbl)
        self.play(FadeIn(eq_grp), run_time=0.8)
        self.play(
            FadeIn(si_drift_bar), FadeIn(si_drift_lbl), FadeIn(nplus_si), FadeIn(nplus_si_lbl),
            Create(tri_si), FadeIn(t_03), FadeIn(t_80), FadeIn(si_tri_tag),
            run_time=1.8,
            rate_func=smootherstep,
        )
        self.wait(1.0)

        sic_drift_bar = Rectangle(width=w8, height=geo_h, fill_color=COL_N_SIC, fill_opacity=1.0, stroke_color=TEAL, stroke_width=2.2)
        sic_drift_bar.move_to([x0 + w8 / 2.0, y_geo_mid, 0])
        sic_bar_note = cn_text("4H-SiC 漂移层：约 8–10 μm（掺杂提高约百倍）", font_size=15.0, color=TEAL, bold=True)
        sic_bar_note.move_to([x0 + w8 + 3.05, y_geo_mid + 0.56, 0])
        sic_bar_ptr = Arrow(sic_bar_note.get_left(), [x0 + w8 / 2.0, y_geo_mid + 0.34, 0], buff=0.06, color=TEAL, stroke_width=1.8, tip_length=0.11)

        prog = ValueTracker(0.0)
        tri_sic = always_redraw(lambda: Polygon(
            [x0, y0, 0],
            [x0, y0 + max(0.02, h30 * prog.get_value()), 0],
            [x0 + w8, y0, 0],
            fill_color=TEAL,
            fill_opacity=0.30,
            stroke_color=TEAL,
            stroke_width=2.8,
        ))

        self.play(
            si_drift_bar.animate.set_fill(opacity=0.32),
            si_drift_lbl.animate.set_opacity(0.40),
            FadeIn(sic_drift_bar),
            FadeIn(sic_bar_note),
            GrowArrow(sic_bar_ptr),
            run_time=0.9,
        )
        self.add(tri_sic)
        self.play(prog.animate.set_value(1.0), FadeIn(t_30), FadeIn(t_8), run_time=2.2, rate_func=smootherstep)

        sic_tri_tag = VGroup(
            cn_text("4H-SiC（等面积 = 1200 V）", font_size=16.5, color=TEAL, bold=True),
            cn_text("峰值电场 3.0 MV/cm（10 倍）", font_size=14.5, color=INK),
            cn_text("漂移区厚度 8 μm（1/10）", font_size=14.5, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        sic_tag_bg = Rectangle(width=sic_tri_tag.width + 0.32, height=sic_tri_tag.height + 0.24, fill_color=TEAL_LIGHT, fill_opacity=0.96, stroke_color=TEAL, stroke_width=1.4)
        sic_tri_tag.move_to(sic_tag_bg)
        sic_call = VGroup(sic_tag_bg, sic_tri_tag).move_to([-1.95, -0.45, 0])
        ptr = Arrow(sic_call.get_left(), [x0 + w8 * 0.45, y0 + h30 * 0.55, 0], buff=0.06, color=TEAL, stroke_width=2.2, tip_length=0.14)

        self.play(FadeIn(sic_call), GrowArrow(ptr), run_time=0.8)
        self.wait(1.8)


# ==============================================================================
# SCENE 5 (Slide 20): 4H-SiC MOSFET Structure & Unipolar Working Principle
# ==============================================================================
class SiCMOSFETPrincipleScene(Scene):
    def construct(self) -> None:
        self.camera.background_color = BG_WHITE

        hdr = cn_text("4H-SiC MOSFET 纵向结构与单极导通/关断原理", font_size=24, color=NAVY, bold=True)
        hdr.to_corner(UL, buff=0.32).shift(RIGHT * 0.15)
        rule = Line(hdr.get_left() + DOWN * 0.26, hdr.get_left() + RIGHT * 12.5 + DOWN * 0.26, color=ICE, stroke_width=2.0)

        cx = -2.25
        w = 5.30
        y_top = 1.70
        y_nplus_bot = 1.24
        y_p_bot = 0.72
        y_drift_bot = -0.52    # Thin 4H-SiC drift (~10 um)
        y_sub_bot = -2.10      # N+ SiC substrate (no P+ collector)
        y_drn_bot = -2.48

        n_drift = Rectangle(width=w, height=(y_top - y_drift_bot), fill_color=COL_N_SIC, fill_opacity=1.0, stroke_color=NAVY, stroke_width=1.8)
        n_drift.move_to([cx, (y_top + y_drift_bot) / 2.0, 0])

        n_sub = Rectangle(width=w, height=(y_drift_bot - y_sub_bot), fill_color=COL_N_PLUS, fill_opacity=1.0, stroke_color=NAVY, stroke_width=1.8)
        n_sub.move_to([cx, (y_drift_bot + y_sub_bot) / 2.0, 0])

        drn_metal = Rectangle(width=w, height=(y_sub_bot - y_drn_bot), fill_color=NAVY, fill_opacity=1.0, stroke_color=NAVY, stroke_width=1.5)
        drn_metal.move_to([cx, (y_sub_bot + y_drn_bot) / 2.0, 0])

        pw = 1.88
        p_left = Rectangle(width=pw, height=(y_top - y_p_bot), fill_color=COL_P_BODY, fill_opacity=1.0, stroke_color=NAVY, stroke_width=1.5)
        p_left.move_to([cx - w / 2.0 + pw / 2.0, (y_top + y_p_bot) / 2.0, 0])
        p_right = p_left.copy().move_to([cx + w / 2.0 - pw / 2.0, (y_top + y_p_bot) / 2.0, 0])

        nw = 0.84
        n_left = Rectangle(width=nw, height=(y_top - y_nplus_bot), fill_color=COL_N_PLUS, fill_opacity=1.0, stroke_color=NAVY, stroke_width=1.5)
        n_left.move_to([cx - w / 2.0 + 1.12, (y_top + y_nplus_bot) / 2.0, 0])
        n_right = n_left.copy().move_to([cx + w / 2.0 - 1.12, (y_top + y_nplus_bot) / 2.0, 0])

        sio2 = Rectangle(width=2.64, height=0.52, fill_color=COL_SIO2, fill_opacity=1.0, stroke_color=COL_SIO2_STROKE, stroke_width=1.8)
        sio2.move_to([cx, y_top + 0.26, 0])
        gate_m = Rectangle(width=2.12, height=0.27, fill_color=STEEL, fill_opacity=1.0, stroke_color=NAVY, stroke_width=1.4)
        gate_m.move_to([cx, y_top + 0.34, 0])
        src_l = Rectangle(width=1.22, height=0.33, fill_color=NAVY, fill_opacity=1.0, stroke_color=NAVY, stroke_width=1.4)
        src_l.move_to([cx - w / 2.0 + 0.61, y_top + 0.165, 0])
        src_r = src_l.copy().move_to([cx + w / 2.0 - 0.61, y_top + 0.165, 0])
        src_bar = VMobject(stroke_color=NAVY, stroke_width=2.6)
        src_bar.set_points_as_corners([
            [cx - w / 2.0 + 0.55, y_top + 0.33, 0],
            [cx - w / 2.0 + 0.55, y_top + 0.82, 0],
            [cx + w / 2.0 - 0.55, y_top + 0.82, 0],
            [cx + w / 2.0 - 0.55, y_top + 0.33, 0],
        ])

        lbls = VGroup(
            mtex(r"\mathrm{N^+}", font_size=18, color="#FFFFFF").move_to(n_left),
            mtex(r"\mathrm{N^+}", font_size=18, color="#FFFFFF").move_to(n_right),
            mtex(r"\mathrm{P}", font_size=18, color=NAVY).move_to([p_left.get_left()[0] + 0.35, p_left.get_center()[1], 0]),
            mtex(r"\mathrm{P}", font_size=18, color=NAVY).move_to([p_right.get_right()[0] - 0.35, p_right.get_center()[1], 0]),
            VGroup(mtex(r"\mathrm{N^-}", font_size=23, color=NAVY), cn_text("4H-SiC 薄漂移区（约 10 μm，较高掺杂）", font_size=15, color=NAVY, bold=True)).arrange(RIGHT, buff=0.10).move_to([cx, 0.05, 0]),
            VGroup(mtex(r"\mathrm{N^+}", font_size=23, color="#FFFFFF"), cn_text("4H-SiC 衬底（无背面", font_size=15.5, color="#FFFFFF", bold=True), mtex(r"\mathrm{P^+}", font_size=19, color="#FFFFFF"), cn_text("区）", font_size=15.5, color="#FFFFFF", bold=True)).arrange(RIGHT, buff=0.06).move_to(n_sub),
            cn_text("漏极 D", font_size=16, color="#FFFFFF", bold=True).move_to(drn_metal),
            cn_text("栅极 G", font_size=14.5, color="#FFFFFF", bold=True).move_to(gate_m),
            mtex(r"\mathrm{SiO_2}", font_size=13.5, color=COL_SIO2_STROKE).move_to([cx, y_top + 0.10, 0]),
            cn_text("源极 S", font_size=16, color=NAVY, bold=True).next_to(src_bar, UP, buff=0.06),
        )

        ch_l = Rectangle(width=0.34, height=0.13, fill_color=COL_CHANNEL, fill_opacity=0.95, stroke_width=0).move_to([cx - w / 2.0 + 1.71, y_top - 0.065, 0])
        ch_r = ch_l.copy().move_to([cx + w / 2.0 - 1.71, y_top - 0.065, 0])

        r_x = 1.65
        rw = 4.75
        cards_spec = [
            (
                VGroup(cn_text("① 结构特点：去掉背面", font_size=17.5, color=NAVY, bold=True), mtex(r"\mathrm{P^+}", font_size=20, color=NAVY), cn_text("区", font_size=17.5, color=NAVY, bold=True)).arrange(RIGHT, buff=0.05),
                ["高击穿场强使 1200 V 漂移层减薄至约 10 μm", "掺杂提高约百倍，无需空穴注入电导调制"],
                NAVY,
            ),
            (
                cn_text("② 导通：单极电子导电", font_size=17.5, color=TEAL, bold=True),
                ["栅极加正压形成 N 型反型沟道", "仅靠电子经沟道与薄 N 型漂移区流向漏极"],
                TEAL,
            ),
            (
                cn_text("③ 关断：无少子复合拖尾", font_size=17.5, color=STEEL, bold=True),
                ["撤除栅压后沟道关闭，无存储少子复合", "过程，单次关断损耗较低"],
                STEEL,
            ),
        ]
        card_objs = []
        for idx, (ct_mob, lines_txt, ccol) in enumerate(cards_spec):
            cy = 1.65 - idx * 1.92
            bg = Rectangle(width=rw, height=1.55, fill_color="#F8FAFC", fill_opacity=1.0, stroke_color=ICE, stroke_width=1.5)
            bar = Rectangle(width=0.10, height=1.55, fill_color=ccol, fill_opacity=1.0, stroke_width=0).align_to(bg, LEFT)
            body = VGroup(*[cn_text(ln, font_size=13.5, color=INK) for ln in lines_txt]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            txt = VGroup(ct_mob, body).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            txt.move_to(bg).align_to(bg, LEFT).shift(RIGHT * 0.26)
            g = VGroup(bg, bar, txt).move_to([r_x + rw / 2.0, cy, 0])
            g.set_opacity(0.30)
            card_objs.append(g)

        static_cell = VGroup(n_drift, n_sub, drn_metal, p_left, p_right, n_left, n_right, sio2, gate_m, src_l, src_r, src_bar, lbls)
        self.add(hdr, rule, static_cell, *card_objs)

        # Stage 1: Structure difference
        self.play(card_objs[0].animate.set_opacity(1.0), Indicate(n_sub, color=ICE, scale_factor=1.02), run_time=1.3)
        self.wait(0.6)

        # Stage 2: Unipolar Turn-on
        vgs_on = mtex(r"+V_{\mathrm{GS}}", font_size=22, color=TEAL).move_to([cx - 3.35, y_top + 0.34, 0])
        plus_ch = VGroup(*[
            en_text("+", font_size=17, color=CRIMSON, bold=True).move_to([cx + dx, y_top + 0.24, 0])
            for dx in np.linspace(-0.80, 0.80, 7)
        ])
        self.play(
            card_objs[1].animate.set_opacity(1.0),
            FadeIn(vgs_on),
            FadeIn(plus_ch),
            GrowFromEdge(ch_l, LEFT),
            GrowFromEdge(ch_r, RIGHT),
            run_time=1.0,
            rate_func=smootherstep,
        )

        def make_sic_epath(side: int, x_off: float) -> VMobject:
            p = VMobject()
            p.set_points_smoothly([
                [cx + side * 1.45, y_top - 0.16, 0],
                [cx + side * 0.88, y_top - 0.07, 0],
                [cx + side * 0.48, y_top - 0.45, 0],
                [cx + x_off, -0.50, 0],
                [cx + x_off, -1.95, 0],
            ])
            return p

        e_paths = [
            make_sic_epath(-1, -1.45),
            make_sic_epath(-1, -0.75),
            make_sic_epath(-1, -0.22),
            make_sic_epath(+1, +0.22),
            make_sic_epath(+1, +0.75),
            make_sic_epath(+1, +1.45),
        ]
        e_guides = VGroup(*[
            DashedVMobject(p, num_dashes=10, dashed_ratio=0.55).set_stroke(COL_E_DOT, width=1.4, opacity=0.45)
            for p in e_paths
        ])
        e_dots_1 = [make_electron(p.get_start(), r=0.09) for p in e_paths]
        e_dots_2 = [make_electron(p.get_start(), r=0.09) for p in e_paths]
        self.play(FadeIn(e_guides), *[FadeIn(d) for d in e_dots_1], run_time=0.35)
        self.play(*[MoveAlongPath(d, p, rate_func=smootherstep) for d, p in zip(e_dots_1, e_paths)], run_time=1.8)
        self.play(*[FadeOut(d) for d in e_dots_1], *[FadeIn(d) for d in e_dots_2], run_time=0.25)
        self.play(*[MoveAlongPath(d, p, rate_func=smootherstep) for d, p in zip(e_dots_2, e_paths)], run_time=1.8)

        # Stage 3: Clean Turn-off
        vgs_off = mtex(r"V_{\mathrm{GS}} \le 0", font_size=22, color=CRIMSON).move_to(vgs_on)
        cross_l = VGroup(
            Line([-0.12, -0.12, 0], [0.12, 0.12, 0], color=CRIMSON, stroke_width=3.0),
            Line([-0.12, 0.12, 0], [0.12, -0.12, 0], color=CRIMSON, stroke_width=3.0),
        ).move_to(ch_l)
        cross_r = cross_l.copy().move_to(ch_r)

        self.play(
            card_objs[2].animate.set_opacity(1.0),
            Transform(vgs_on, vgs_off),
            FadeOut(plus_ch),
            FadeOut(ch_l),
            FadeOut(ch_r),
            FadeIn(cross_l),
            FadeIn(cross_r),
            FadeOut(e_guides),
            *[d.animate.shift(DOWN * 0.40).set_opacity(0.0) for d in e_dots_2],
            run_time=1.2,
            rate_func=smootherstep,
        )
        self.wait(1.8)
