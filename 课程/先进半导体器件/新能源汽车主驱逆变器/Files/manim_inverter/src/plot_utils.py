"""Shared waveform plotting utilities and exact cross-scene state builders."""

from __future__ import annotations

import math
import numpy as np
from manim import *

from style import (
    INK,
    INK_MUTED,
    GRID_LIGHT,
    RULE_COLOR,
    RED_POS,
    BLUE_NEG,
    AMBER_BAND,
    TEAL_CUR,
    VIOLET_MOD,
    GATE_S1_POS,
    GATE_S3_POS,
    PLOT_RIGHT_W,
    math_tnr,
    zh_label,
)
from physics import (
    square_u,
    triangle_i,
    bipolar_period_duty,
    gate_states_deadtime,
    triangle_carrier,
    spwm_pulses_from_mod,
    solve_rl_current,
)


def make_clean_axes(
    center: np.ndarray,
    width: float,
    height: float,
    x_range: tuple[float, float, float],
    y_range: tuple[float, float, float],
    x_tip: bool = True,
    y_tip: bool = True,
) -> Axes:
    """Create crisp editorial axes with subtle ink lines and slim arrowheads."""
    ax = Axes(
        x_range=list(x_range),
        y_range=list(y_range),
        x_length=width,
        y_length=height,
        tips=True,
        axis_config={
            "color": INK,
            "stroke_width": 2.0,
            "include_ticks": False,
            "include_numbers": False,
            "tip_width": 0.11,
            "tip_height": 0.13,
        },
        x_axis_config={"include_tip": x_tip},
        y_axis_config={"include_tip": y_tip},
    )
    ax.move_to(center)
    return ax


def build_ut_plot_group(center: np.ndarray, width: float = PLOT_RIGHT_W, height: float = 3.2, t_max: float = 3.0) -> tuple[Axes, VGroup]:
    """Build u(t) axes + +U/0/-U reference dashed lines and labels."""
    ax = make_clean_axes(center, width, height, (0, t_max, 0.5), (-1.35, 1.35, 1.0))
    dash_p = DashedLine(ax.c2p(0, 1), ax.c2p(t_max, 1), color=GRID_LIGHT, stroke_width=1.4, dash_length=0.09)
    dash_m = DashedLine(ax.c2p(0, -1), ax.c2p(t_max, -1), color=GRID_LIGHT, stroke_width=1.4, dash_length=0.09)
    lbl_y = math_tnr("u(t)", font_size=26, color=INK).next_to(ax.y_axis.get_top(), RIGHT, buff=0.10).shift(DOWN * 0.05)
    lbl_t = math_tnr("t", font_size=24, color=INK).next_to(ax.x_axis.get_right(), DOWN, buff=0.10)
    lbl_up = math_tnr("+U", font_size=22, color=RED_POS).next_to(ax.c2p(0, 1), LEFT, buff=0.10)
    lbl_zero = math_tnr("0", font_size=20, color=INK_MUTED).next_to(ax.c2p(0, 0), LEFT, buff=0.10)
    lbl_dn = math_tnr("-U", font_size=22, color=BLUE_NEG).next_to(ax.c2p(0, -1), LEFT, buff=0.10)
    decos = VGroup(dash_p, dash_m, lbl_y, lbl_t, lbl_up, lbl_zero, lbl_dn)
    return ax, decos


def build_it_plot_group(center: np.ndarray, width: float = PLOT_RIGHT_W, height: float = 2.25, t_max: float = 3.0) -> tuple[Axes, VGroup]:
    """Build i(t) axes aligned with u(t) axes."""
    ax = make_clean_axes(center, width, height, (0, t_max, 0.5), (-1.35, 1.35, 1.0))
    dash_p = DashedLine(ax.c2p(0, 1), ax.c2p(t_max, 1), color=GRID_LIGHT, stroke_width=1.1, dash_length=0.09)
    dash_m = DashedLine(ax.c2p(0, -1), ax.c2p(t_max, -1), color=GRID_LIGHT, stroke_width=1.1, dash_length=0.09)
    lbl_y = math_tnr("i(t)", font_size=26, color=TEAL_CUR).next_to(ax.y_axis.get_top(), RIGHT, buff=0.10).shift(DOWN * 0.05)
    lbl_t = math_tnr("t", font_size=24, color=INK).next_to(ax.x_axis.get_right(), DOWN, buff=0.10)
    lbl_zero = math_tnr("0", font_size=20, color=INK_MUTED).next_to(ax.c2p(0, 0), LEFT, buff=0.10)
    decos = VGroup(dash_p, dash_m, lbl_y, lbl_t, lbl_zero)
    return ax, decos


def build_alignment_guides(ut_ax: Axes, it_ax: Axes, t_vals: list[float]) -> VGroup:
    """Delicate vertical dashed guides linking voltage reversal instants from u(t) to i(t)."""
    guides = VGroup()
    y_top = ut_ax.c2p(0, -1.15)[1]
    y_bot = it_ax.c2p(0, +1.15)[1]
    for tv in t_vals:
        x_pos = ut_ax.c2p(tv, 0)[0]
        guides.add(
            DashedLine(
                [x_pos, y_top, 0],
                [x_pos, y_bot, 0],
                color="#B8B3A6",
                stroke_width=1.3,
                dash_length=0.08,
            )
        )
    return guides


def build_square_u_waveform(ax: Axes, t_end: float, period: float = 1.0, stroke_w: float = 3.0) -> VGroup:
    """Build colored bipolar square wave u(t) up to t_end with live tip dot."""
    t_end = max(0.0, float(t_end))
    pos_vm = VMobject(color=RED_POS, stroke_width=stroke_w)
    neg_vm = VMobject(color=BLUE_NEG, stroke_width=stroke_w)
    vert_vm = VMobject(color="#4B5563", stroke_width=1.8)

    half = 0.5 * period
    t_cur = 0.0
    prev_val = None
    while t_cur < t_end - 1e-6:
        idx = int(math.floor(t_cur / half + 1e-9))
        t_next = min(t_end, (idx + 1) * half)
        val = 1.0 if (idx % 2 == 0) else -1.0
        p0 = ax.c2p(t_cur, val)
        p1 = ax.c2p(t_next, val)
        if prev_val is not None:
            pv0 = ax.c2p(t_cur, prev_val)
            vert_vm.start_new_path(pv0)
            vert_vm.add_line_to(p0)
        target = pos_vm if val > 0 else neg_vm
        target.start_new_path(p0)
        target.add_line_to(p1)
        prev_val = val
        t_cur = t_next

    tip_val = square_u(max(0.0, t_end - 1e-5), period) if t_end > 1e-4 else 1.0
    tip_col = RED_POS if tip_val > 0 else BLUE_NEG
    tip_dot = Dot(ax.c2p(t_end, tip_val), radius=0.065, color=tip_col, stroke_color="#FFFFFF", stroke_width=1.4)
    return VGroup(vert_vm, pos_vm, neg_vm, tip_dot)


def build_triangle_i_waveform(ax: Axes, t_end: float, period: float = 1.0, stroke_w: float = 3.0) -> VGroup:
    """Build steady-state triangular inductive current i(t) up to t_end."""
    t_end = max(0.0, float(t_end))
    half = 0.5 * period
    knots = [0.0]
    k = 1
    while k * half < t_end - 1e-6:
        knots.append(k * half)
        k += 1
    knots.append(t_end)
    pts = [ax.c2p(t_val, triangle_i(t_val if t_val < t_end else max(0.0, t_end - 1e-7), period) if abs((t_val % period) - 0.0) > 1e-7 or t_val == 0 else -1.0) for t_val in knots]
    # Exact corner evaluation avoiding modulo wrap at integer periods
    pts = []
    for tv in knots:
        phase = (tv / period) % 1.0
        if tv > 1e-6 and abs(phase) < 1e-7:
            # exact end of period -> value is -1.0
            val = -1.0
        else:
            val = triangle_i(tv, period)
        pts.append(ax.c2p(tv, val))

    curve = VMobject(color=TEAL_CUR, stroke_width=stroke_w)
    if len(pts) >= 2:
        curve.set_points_as_corners(pts)
    tip_dot = Dot(pts[-1], radius=0.065, color=TEAL_CUR, stroke_color="#FFFFFF", stroke_width=1.4)
    return VGroup(curve, tip_dot)


def build_freewheeling_bands(it_ax: Axes, t_max: float = 3.0, period: float = 1.0) -> VGroup:
    """Translucent amber bands highlighting every quarter-period where u and i oppose."""
    bands = VGroup()
    y_bot = it_ax.c2p(0, -1.25)[1]
    y_top = it_ax.c2p(0, +1.25)[1]
    h = y_top - y_bot
    yc = 0.5 * (y_top + y_bot)

    starts = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5]
    for idx, t0 in enumerate(starts):
        t1 = min(t_max, t0 + 0.25 * period)
        if t1 <= t0:
            continue
        x0 = it_ax.c2p(t0, 0)[0]
        x1 = it_ax.c2p(t1, 0)[0]
        rect = Rectangle(
            width=x1 - x0,
            height=h,
            fill_color=AMBER_BAND,
            fill_opacity=0.16,
            stroke_width=0,
        ).move_to([0.5 * (x0 + x1), yc, 0])
        bands.add(rect)
        if idx == 1:
            tag = zh_label("续流", font_size=15, color="#B45309").move_to([0.5 * (x0 + x1), y_bot + 0.22, 0])
            bands.add(tag)
    return bands


def build_p1b_end_state(hbridge_cls) -> dict:
    """Canonical end state of P1B (and exact start state of P1C)."""
    from style import HBRIDGE_TOPLEFT_POS, HBRIDGE_TOPLEFT_SCALE, UT_UPPER_POS, IT_LOWER_POS

    hb = hbridge_cls(rl_mode=True)
    hb.scale(HBRIDGE_TOPLEFT_SCALE)
    hb.move_to(HBRIDGE_TOPLEFT_POS)

    rule = Line([-6.05, 0.34, 0], [-0.75, 0.34, 0], color=RULE_COLOR, stroke_width=1.6)

    eq1 = math_tnr(r"u = R\,i + L\,\frac{di}{dt}", font_size=30, color=INK).move_to([-3.55, -0.22, 0])
    # Dim Ri subtly and add gentle strike
    eq2_note = math_tnr(r"R\,i \ll L\,\frac{di}{dt}", font_size=24, color=INK_MUTED).move_to([-3.55, -0.96, 0])
    eq3 = math_tnr(r"\frac{di}{dt} \approx \frac{u}{L}", font_size=30, color=INK).move_to([-3.55, -1.78, 0])
    eq4 = math_tnr(r"i(t) \approx \frac{1}{L}\int u(t)\,dt", font_size=31, color=TEAL_CUR).move_to([-3.55, -2.72, 0])
    eq4_box = RoundedRectangle(
        width=eq4.width + 0.36,
        height=eq4.height + 0.24,
        corner_radius=0.10,
        fill_color="#FFFFFF",
        fill_opacity=0.75,
        stroke_color=TEAL_CUR,
        stroke_width=1.6,
    ).move_to(eq4.get_center())
    eq4_grp = VGroup(eq4_box, eq4)

    ut_ax, ut_decos = build_ut_plot_group(UT_UPPER_POS, width=PLOT_RIGHT_W, height=2.25, t_max=3.0)
    ut_wave = build_square_u_waveform(ut_ax, t_end=3.0, stroke_w=2.8)
    ut_wave.remove(ut_wave[-1])  # remove moving tip dot at static end state

    it_ax, it_decos = build_it_plot_group(IT_LOWER_POS, width=PLOT_RIGHT_W, height=2.25, t_max=3.0)
    it_wave = build_triangle_i_waveform(it_ax, t_end=3.0, stroke_w=2.8)
    it_wave.remove(it_wave[-1])

    guides = build_alignment_guides(ut_ax, it_ax, [0.5, 1.0, 1.5, 2.0, 2.5])

    return {
        "hb": hb,
        "rule": rule,
        "eq1": eq1,
        "eq2_note": eq2_note,
        "eq3": eq3,
        "eq4_grp": eq4_grp,
        "ut_ax": ut_ax,
        "ut_decos": ut_decos,
        "ut_wave": ut_wave,
        "it_ax": it_ax,
        "it_decos": it_decos,
        "it_wave": it_wave,
        "guides": guides,
    }


def _build_digital_gate_wave(ax: Axes, is_upper: bool, t_max: float = 2.0, td: float = 0.08, color: str = RED_POS) -> VMobject:
    """Step waveform in {0, 1} for S1 (upper) or S3 (lower) with symmetric dead-time td."""
    pts = []
    # Sample step vertices densely enough per half-period
    edges = []
    for k in range(int(round(t_max))):
        edges.extend([
            (k + 0.0, 0.0),
            (k + td, 1.0 if is_upper else 0.0),
            (k + 0.5 - td, 0.0),
            (k + 0.5 + td, 0.0 if is_upper else 1.0),
            (k + 1.0 - td, 0.0),
        ])
    edges.append((t_max, 0.0))

    prev_y = 0.0
    for t_val, level in edges:
        if len(pts) > 0 and abs(level - prev_y) > 0.1:
            pts.append(ax.c2p(t_val, prev_y))
        pts.append(ax.c2p(t_val, level))
        prev_y = level

    vm = VMobject(color=color, stroke_width=2.8)
    vm.set_points_as_corners(pts)
    return vm


def build_deadtime_plots_group(td: float = 0.08, t_max: float = 2.0) -> dict:
    """Build stacked asynchronous S1 & S3 gate plots with amber dead-time bands (P1C end / P2A start)."""
    w = PLOT_RIGHT_W
    h = 1.90
    ax_s1 = make_clean_axes(GATE_S1_POS, w, h, (0, t_max, 0.5), (-0.25, 1.35, 1.0))
    ax_s3 = make_clean_axes(GATE_S3_POS, w, h, (0, t_max, 0.5), (-0.25, 1.35, 1.0))

    # Labels
    lbl_s1 = math_tnr("S_1", font_size=28, color=RED_POS).next_to(ax_s1.y_axis.get_top(), RIGHT, buff=0.12).shift(DOWN * 0.06)
    lbl_s3 = math_tnr("S_3", font_size=28, color=BLUE_NEG).next_to(ax_s3.y_axis.get_top(), RIGHT, buff=0.12).shift(DOWN * 0.06)
    t1 = math_tnr("t", font_size=22, color=INK).next_to(ax_s1.x_axis.get_right(), DOWN, buff=0.08)
    t3 = math_tnr("t", font_size=22, color=INK).next_to(ax_s3.x_axis.get_right(), DOWN, buff=0.08)
    on1 = math_tnr("1", font_size=18, color=INK_MUTED).next_to(ax_s1.c2p(0, 1), LEFT, buff=0.09)
    off1 = math_tnr("0", font_size=18, color=INK_MUTED).next_to(ax_s1.c2p(0, 0), LEFT, buff=0.09)
    on3 = math_tnr("1", font_size=18, color=INK_MUTED).next_to(ax_s3.c2p(0, 1), LEFT, buff=0.09)
    off3 = math_tnr("0", font_size=18, color=INK_MUTED).next_to(ax_s3.c2p(0, 0), LEFT, buff=0.09)

    dash1 = DashedLine(ax_s1.c2p(0, 1), ax_s1.c2p(t_max, 1), color=GRID_LIGHT, stroke_width=1.2, dash_length=0.08)
    dash3 = DashedLine(ax_s3.c2p(0, 1), ax_s3.c2p(t_max, 1), color=GRID_LIGHT, stroke_width=1.2, dash_length=0.08)

    wave_s1 = _build_digital_gate_wave(ax_s1, is_upper=True, t_max=t_max, td=td, color=RED_POS)
    wave_s3 = _build_digital_gate_wave(ax_s3, is_upper=False, t_max=t_max, td=td, color=BLUE_NEG)

    # Dead-time bands spanning both plots
    y_top = ax_s1.c2p(0, 1.18)[1]
    y_bot = ax_s3.c2p(0, -0.10)[1]
    yc = 0.5 * (y_top + y_bot)
    bh = y_top - y_bot

    intervals = [
        (0.0, td),
        (0.5 - td, 0.5 + td),
        (1.0 - td, 1.0 + td),
        (1.5 - td, 1.5 + td),
        (2.0 - td, 2.0),
    ]
    bands = VGroup()
    for a, b in intervals:
        xa = ax_s1.c2p(a, 0)[0]
        xb = ax_s1.c2p(b, 0)[0]
        bands.add(
            Rectangle(
                width=max(0.02, xb - xa),
                height=bh,
                fill_color=AMBER_BAND,
                fill_opacity=0.20,
                stroke_width=0,
            ).move_to([0.5 * (xa + xb), yc, 0])
        )

    # Double-arrow callout on the central dead-time gap [0.5 - td, 0.5 + td]
    xa = ax_s1.c2p(0.5 - td, 0)[0]
    xb = ax_s1.c2p(0.5 + td, 0)[0]
    y_mid_gap = 0.5 * (ax_s1.c2p(0, -0.25)[1] + ax_s3.c2p(0, 1.25)[1])
    arr_l = Line([xa - 0.25, y_mid_gap, 0], [xa, y_mid_gap, 0], color="#B45309", stroke_width=2.0).add_tip(tip_length=0.10, tip_width=0.09)
    arr_r = Line([xb + 0.25, y_mid_gap, 0], [xb, y_mid_gap, 0], color="#B45309", stroke_width=2.0).add_tip(tip_length=0.10, tip_width=0.09)
    td_lbl = math_tnr("t_d", font_size=24, color="#B45309").move_to([0.5 * (xa + xb), y_mid_gap + 0.28, 0])
    zh_dt = zh_label("死区", font_size=17, color="#B45309").move_to([0.5 * (xa + xb), y_mid_gap - 0.28, 0])

    axes_decos = VGroup(dash1, dash3, lbl_s1, lbl_s3, t1, t3, on1, off1, on3, off3)
    full_group = VGroup(
        bands,
        axes_decos,
        ax_s1, ax_s3,
        wave_s1, wave_s3,
        arr_l, arr_r, td_lbl, zh_dt,
    )
    return {
        "group": full_group,
        "ax_s1": ax_s1,
        "ax_s3": ax_s3,
        "axes_decos": axes_decos,
        "bands": bands,
        "wave_s1": wave_s1,
        "wave_s3": wave_s3,
        "td_callout": VGroup(arr_l, arr_r, td_lbl, zh_dt),
    }


def build_p1c_end_state(hbridge_cls) -> dict:
    """Exact end state of P1C (and exact Frame 0 of P2A)."""
    from style import HBRIDGE_LEFT_POS, HBRIDGE_LEFT_SCALE

    hb = hbridge_cls(rl_mode=True)
    hb.scale(HBRIDGE_LEFT_SCALE)
    hb.move_to(HBRIDGE_LEFT_POS)

    dt_plots = build_deadtime_plots_group(td=0.08, t_max=2.0)
    return {"hb": hb, **dt_plots}


def build_spwm_window_mobjects(
    ax: Axes,
    t_start: float,
    t_span: float,
    n_sw: int = 24,
    amp: float = 0.88,
    show_areas: bool = True,
    show_sine_guide: bool = False,
) -> VGroup:
    """Render bipolar PWM pulses + period average dots on normalized axes x in [0, 1]."""
    pos_line = VMobject(color=RED_POS)
    neg_line = VMobject(color=BLUE_NEG)
    vert_line = VMobject(color="#4B5563")

    stroke_w = float(np.interp(t_span, [1.0, 24.0], [3.0, 1.5]))
    vert_w = float(np.interp(t_span, [1.0, 24.0], [1.8, 0.9]))
    pos_line.set_stroke(width=stroke_w)
    neg_line.set_stroke(width=stroke_w)
    vert_line.set_stroke(width=vert_w, opacity=float(np.interp(t_span, [1.0, 24.0], [0.85, 0.45])))

    area_op = float(np.interp(t_span, [1.0, 10.0], [0.15, 0.0])) if show_areas else 0.0
    bar_op = float(np.interp(t_span, [1.0, 12.0], [0.90, 0.0]))
    div_op = float(np.interp(t_span, [1.0, 14.0], [0.50, 0.0]))
    dot_r = float(np.interp(t_span, [1.0, 24.0], [0.085, 0.052]))

    areas = VGroup()
    dividers = VGroup()
    avg_bars = VGroup()
    avg_dots = VGroup()

    t_end = t_start + t_span
    k_min = int(math.floor(t_start))
    k_max = int(math.ceil(t_end))

    prev_end_val = None
    for k in range(k_min, k_max):
        duty, u_bar = bipolar_period_duty(k, n_sw=n_sw, amp=amp)
        t_sw = k + duty

        # Period divider line at k > t_start
        if div_op > 0.02 and t_start + 0.02 < k < t_end - 0.02:
            x_div = (k - t_start) / t_span
            dividers.add(
                DashedLine(
                    ax.c2p(x_div, -1.12),
                    ax.c2p(x_div, +1.12),
                    color="#B8B3A6",
                    stroke_width=1.2,
                    stroke_opacity=div_op,
                    dash_length=0.07,
                )
            )

        # Positive segment [k, t_sw] clipped to [t_start, t_end]
        a_pos = max(float(k), t_start)
        b_pos = min(t_sw, t_end)
        if b_pos > a_pos + 1e-6:
            xa = (a_pos - t_start) / t_span
            xb = (b_pos - t_start) / t_span
            p0 = ax.c2p(xa, 1.0)
            p1 = ax.c2p(xb, 1.0)
            if prev_end_val is not None and abs(prev_end_val - 1.0) > 0.1 and a_pos > t_start + 1e-5:
                vert_line.start_new_path(ax.c2p(xa, prev_end_val))
                vert_line.add_line_to(p0)
            pos_line.start_new_path(p0)
            pos_line.add_line_to(p1)
            prev_end_val = 1.0
            if area_op > 0.01:
                bl = ax.c2p(xa, 0.0)
                tr = ax.c2p(xb, 1.0)
                areas.add(
                    Rectangle(
                        width=max(0.005, tr[0] - bl[0]),
                        height=tr[1] - bl[1],
                        fill_color=RED_POS,
                        fill_opacity=area_op,
                        stroke_width=0,
                    ).move_to([0.5 * (bl[0] + tr[0]), 0.5 * (bl[1] + tr[1]), 0])
                )

        # Negative segment [t_sw, k + 1] clipped to [t_start, t_end]
        a_neg = max(t_sw, t_start)
        b_neg = min(float(k + 1), t_end)
        if b_neg > a_neg + 1e-6:
            xa = (a_neg - t_start) / t_span
            xb = (b_neg - t_start) / t_span
            p0 = ax.c2p(xa, -1.0)
            p1 = ax.c2p(xb, -1.0)
            if prev_end_val is not None and abs(prev_end_val - (-1.0)) > 0.1 and a_neg > t_start + 1e-5:
                vert_line.start_new_path(ax.c2p(xa, prev_end_val))
                vert_line.add_line_to(p0)
            neg_line.start_new_path(p0)
            neg_line.add_line_to(p1)
            prev_end_val = -1.0
            if area_op > 0.01:
                tl = ax.c2p(xa, 0.0)
                br = ax.c2p(xb, -1.0)
                areas.add(
                    Rectangle(
                        width=max(0.005, br[0] - tl[0]),
                        height=tl[1] - br[1],
                        fill_color=BLUE_NEG,
                        fill_opacity=area_op,
                        stroke_width=0,
                    ).move_to([0.5 * (tl[0] + br[0]), 0.5 * (tl[1] + br[1]), 0])
                )

        # Period average bar & violet dot at k + 0.5
        if bar_op > 0.02:
            ba = max(float(k), t_start)
            bb = min(float(k + 1), t_end)
            if bb > ba + 0.05:
                xba = (ba - t_start) / t_span
                xbb = (bb - t_start) / t_span
                avg_bars.add(
                    Line(
                        ax.c2p(xba, u_bar),
                        ax.c2p(xbb, u_bar),
                        color=VIOLET_MOD,
                        stroke_width=2.8,
                        stroke_opacity=bar_op,
                    )
                )

        t_mid = k + 0.5
        if t_start <= t_mid <= t_end:
            xm = (t_mid - t_start) / t_span
            avg_dots.add(
                Dot(
                    ax.c2p(xm, u_bar),
                    radius=dot_r,
                    color=VIOLET_MOD,
                    stroke_color="#FFFFFF",
                    stroke_width=1.0,
                )
            )

    guide = VGroup()
    if show_sine_guide:
        ts = np.linspace(t_start, t_end, 160)
        pts = [ax.c2p((tv - t_start) / t_span, amp * math.sin(2.0 * math.pi * tv / n_sw)) for tv in ts]
        s_curve = VMobject(color=VIOLET_MOD, stroke_width=2.0, stroke_opacity=0.65)
        s_curve.set_points_as_corners(pts)
        guide.add(DashedVMobject(s_curve, num_dashes=48, dashed_ratio=0.55))

    return VGroup(areas, dividers, vert_line, pos_line, neg_line, avg_bars, guide, avg_dots)


def build_p2a_end_state() -> dict:
    """Exact end frame of P2A (and Frame 0 of P2B)."""
    ax = make_clean_axes(np.array([0.0, -0.10, 0.0]), width=9.4, height=4.1, x_range=(0, 1, 0.25), y_range=(-1.35, 1.35, 1.0))
    dash_p = DashedLine(ax.c2p(0, 1), ax.c2p(1, 1), color=GRID_LIGHT, stroke_width=1.3, dash_length=0.09)
    dash_m = DashedLine(ax.c2p(0, -1), ax.c2p(1, -1), color=GRID_LIGHT, stroke_width=1.3, dash_length=0.09)
    lbl_up = math_tnr("+U", font_size=22, color=RED_POS).next_to(ax.c2p(0, 1), LEFT, buff=0.12)
    lbl_z = math_tnr("0", font_size=20, color=INK_MUTED).next_to(ax.c2p(0, 0), LEFT, buff=0.12)
    lbl_dn = math_tnr("-U", font_size=22, color=BLUE_NEG).next_to(ax.c2p(0, -1), LEFT, buff=0.12)
    lbl_y = math_tnr("u(t)", font_size=26, color=INK).next_to(ax.y_axis.get_top(), RIGHT, buff=0.12).shift(DOWN * 0.05)
    lbl_t = math_tnr("t", font_size=24, color=INK).next_to(ax.x_axis.get_right(), DOWN, buff=0.10)
    decos = VGroup(dash_p, dash_m, lbl_up, lbl_z, lbl_dn, lbl_y, lbl_t)
    wave = build_spwm_window_mobjects(ax, t_start=0.0, t_span=24.0, n_sw=24, amp=0.88, show_areas=False, show_sine_guide=True)
    return {"ax": ax, "decos": decos, "wave": wave}


def build_three_tier_scope_static() -> dict:
    """Shared static axes & labels for the 3-tier SPWM modulation parameter explorer (P2B end / P2C start)."""
    cx = -0.68
    w = 8.65
    h = 1.62
    ys = (2.38, 0.0, -2.38)

    ax_ref = make_clean_axes(np.array([cx, ys[0], 0.0]), w, h, (0, 1, 0.25), (-1.25, 1.25, 1.0))
    ax_pwm = make_clean_axes(np.array([cx, ys[1], 0.0]), w, h, (0, 1, 0.25), (-1.25, 1.25, 1.0))
    ax_cur = make_clean_axes(np.array([cx, ys[2], 0.0]), w, h, (0, 1, 0.25), (-1.10, 1.10, 1.0))

    d_ref_p = DashedLine(ax_ref.c2p(0, 1), ax_ref.c2p(1, 1), color=GRID_LIGHT, stroke_width=1.0, dash_length=0.08)
    d_ref_m = DashedLine(ax_ref.c2p(0, -1), ax_ref.c2p(1, -1), color=GRID_LIGHT, stroke_width=1.0, dash_length=0.08)
    d_pwm_p = DashedLine(ax_pwm.c2p(0, 1), ax_pwm.c2p(1, 1), color=GRID_LIGHT, stroke_width=1.0, dash_length=0.08)
    d_pwm_m = DashedLine(ax_pwm.c2p(0, -1), ax_pwm.c2p(1, -1), color=GRID_LIGHT, stroke_width=1.0, dash_length=0.08)

    tag_ref = VGroup(
        zh_label("调制波", font_size=17, color=VIOLET_MOD),
        math_tnr("u_{\\mathrm{ref}}", font_size=21, color=VIOLET_MOD),
    ).arrange(RIGHT, buff=0.06).next_to(ax_ref.c2p(0, 0), LEFT, buff=0.16)

    tag_pwm = math_tnr("u(t)", font_size=22, color=INK).next_to(ax_pwm.c2p(0, 0), LEFT, buff=0.48)

    tag_cur = VGroup(
        zh_label("电流", font_size=17, color=TEAL_CUR),
        math_tnr("i(t)", font_size=21, color=TEAL_CUR),
    ).arrange(RIGHT, buff=0.06).next_to(ax_cur.c2p(0, 0), LEFT, buff=0.16)

    lbl_up = math_tnr("+U", font_size=18, color=RED_POS).next_to(ax_pwm.c2p(0, 1), LEFT, buff=0.08)
    lbl_dn = math_tnr("-U", font_size=18, color=BLUE_NEG).next_to(ax_pwm.c2p(0, -1), LEFT, buff=0.08)
    t_lbl = math_tnr("t", font_size=20, color=INK).next_to(ax_cur.x_axis.get_right(), RIGHT, buff=0.08)

    static_grp = VGroup(
        d_ref_p, d_ref_m, d_pwm_p, d_pwm_m,
        ax_ref, ax_pwm, ax_cur,
        tag_ref, tag_pwm, tag_cur, lbl_up, lbl_dn, t_lbl,
    )
    return {
        "ax_ref": ax_ref,
        "ax_pwm": ax_pwm,
        "ax_cur": ax_cur,
        "static_grp": static_grp,
    }


def build_three_tier_waveforms(
    ax_ref: Axes,
    ax_pwm: Axes,
    ax_cur: Axes,
    amp: float,
    freq: float,
    phase: float,
    f_sw: float,
) -> VGroup:
    """Fast 60fps generator of carrier + u_ref + bipolar PWM + RL current waveforms."""
    # 1. Faint triangle carrier + u_ref
    t_car = np.linspace(0.0, 1.0, int(round(4 * f_sw)) + 1)
    u_car = triangle_carrier(t_car, f_sw)
    car_vm = VMobject(color="#9CA3AF", stroke_width=1.0, stroke_opacity=0.35)
    car_vm.set_points_as_corners([ax_ref.c2p(float(t_car[i]), float(u_car[i])) for i in range(len(t_car))])

    t_ref = np.linspace(0.0, 1.0, 140)
    u_ref = amp * np.sin(2.0 * np.pi * freq * t_ref + phase)
    ref_vm = VMobject(color=VIOLET_MOD, stroke_width=2.6)
    ref_vm.set_points_as_corners([ax_ref.c2p(float(t_ref[i]), float(u_ref[i])) for i in range(len(t_ref))])

    # 2. Bipolar PWM via 3 batched VMobjects (instantaneous!)
    edges, levels = spwm_pulses_from_mod(amp=amp, freq=freq, phase=phase, f_sw=f_sw, t_start=0.0, t_max=1.0, n_grid=2000)
    pos_vm = VMobject(color=RED_POS, stroke_width=2.2)
    neg_vm = VMobject(color=BLUE_NEG, stroke_width=2.2)
    vert_vm = VMobject(color="#4B5563", stroke_width=1.1, stroke_opacity=0.65)
    for k in range(len(levels)):
        t0 = float(edges[k])
        t1 = float(edges[k + 1])
        lv = float(levels[k])
        p0 = ax_pwm.c2p(t0, lv)
        p1 = ax_pwm.c2p(t1, lv)
        if k > 0:
            prev_lv = float(levels[k - 1])
            vert_vm.start_new_path(ax_pwm.c2p(t0, prev_lv))
            vert_vm.add_line_to(p0)
        tgt = pos_vm if lv > 0 else neg_vm
        tgt.start_new_path(p0)
        tgt.add_line_to(p1)

    # 3. RL filtered current i(t)
    t_cur, i_cur = solve_rl_current(amp=amp, freq=freq, phase=phase, f_sw=f_sw, tau=0.14, r_val=1.0, t_max=1.0)
    # Normalize comfortably inside [-0.95, 0.95] at nominal amplitude
    i_scaled = np.clip(i_cur * 1.18, -1.05, 1.05)
    cur_vm = VMobject(color=TEAL_CUR, stroke_width=2.7)
    cur_vm.set_points_as_corners([ax_cur.c2p(float(t_cur[j]), float(i_scaled[j])) for j in range(len(t_cur))])

    return VGroup(car_vm, ref_vm, vert_vm, pos_vm, neg_vm, cur_vm)


class ModulationHUD(VGroup):
    """Static-compiled Times New Roman HUD cards updated via DecimalNumber.set_value (zero per-frame TeX)."""

    def __init__(self, amp: float = 0.80, freq: float = 1.00, phase_deg: float = 0.0, f_sw: float = 44.0, active_idx: int = -1):
        super().__init__()
        self.cards: list[RoundedRectangle] = []
        self.sym_mobs: list[Mobject] = []

        sym_specs = [
            ("A", 0),
            ("f / f_0", 1),
            (r"\varphi", 2),
            ("f_s / f_0", 3),
        ]

        self.num_amp = DecimalNumber(amp, num_decimal_places=2, font_size=26, color=INK)
        self.num_freq = DecimalNumber(freq, num_decimal_places=2, font_size=26, color=INK)
        self.num_phase = DecimalNumber(phase_deg, num_decimal_places=0, include_sign=True, unit=r"^\circ", font_size=26, color=INK)
        self.num_fsw = DecimalNumber(f_sw, num_decimal_places=0, font_size=26, color=INK)
        self.nums = [self.num_amp, self.num_freq, self.num_phase, self.num_fsw]

        rows = VGroup()
        for sym, idx in sym_specs:
            box = RoundedRectangle(
                width=2.16,
                height=0.92,
                corner_radius=0.12,
                fill_color="#FFFFFF",
                fill_opacity=0.98,
                stroke_color="#D1CEC4",
                stroke_width=1.5,
            )
            sym_mob = math_tnr(sym, font_size=24, color=INK_MUTED)
            sym_mob.move_to(box.get_left() + RIGHT * 0.48)
            num_mob = self.nums[idx]
            num_mob.move_to(box.get_right() + LEFT * 0.56)
            self.cards.append(box)
            self.sym_mobs.append(sym_mob)
            rows.add(VGroup(box, sym_mob, num_mob))

        rows.arrange(DOWN, buff=0.22)
        rows.move_to([5.25, 0.0, 0.0])
        self.add(rows)
        self.set_active(active_idx)
        self._last_strs = (None, None, None, None)

    def set_active(self, active_idx: int) -> None:
        for idx, (box, sym_mob) in enumerate(zip(self.cards, self.sym_mobs)):
            is_act = idx == active_idx
            box.set_stroke(VIOLET_MOD if is_act else "#D1CEC4", width=2.3 if is_act else 1.5)
            box.set_fill("#F5F3FF" if is_act else "#FFFFFF", opacity=0.98)
            sym_mob.set_color(VIOLET_MOD if is_act else INK_MUTED)

    def update_values(self, amp: float, freq: float, phase_deg: float, f_sw: float, active_idx: int = -1) -> None:
        s_amp = f"{amp:.2f}"
        s_freq = f"{freq:.2f}"
        s_phase = f"{int(round(phase_deg))}"
        s_fsw = f"{int(round(f_sw))}"
        if s_amp != self._last_strs[0]:
            self.num_amp.set_value(float(s_amp))
            self.num_amp.move_to(self.cards[0].get_right() + LEFT * 0.54)
        if s_freq != self._last_strs[1]:
            self.num_freq.set_value(float(s_freq))
            self.num_freq.move_to(self.cards[1].get_right() + LEFT * 0.54)
        if s_phase != self._last_strs[2]:
            self.num_phase.set_value(int(s_phase))
            self.num_phase.move_to(self.cards[2].get_right() + LEFT * 0.54)
        if s_fsw != self._last_strs[3]:
            self.num_fsw.set_value(int(s_fsw))
            self.num_fsw.move_to(self.cards[3].get_right() + LEFT * 0.54)
        self._last_strs = (s_amp, s_freq, s_phase, s_fsw)
        self.set_active(active_idx)


def build_p2b_end_state() -> dict:
    """Exact end frame of P2B (and Frame 0 of P2C)."""
    scope = build_three_tier_scope_static()
    waves = build_three_tier_waveforms(
        scope["ax_ref"], scope["ax_pwm"], scope["ax_cur"],
        amp=0.80, freq=1.00, phase=0.0, f_sw=44.0,
    )
    hud = ModulationHUD(amp=0.80, freq=1.00, phase_deg=0.0, f_sw=44.0, active_idx=-1)
    return {**scope, "waves": waves, "hud": hud}
