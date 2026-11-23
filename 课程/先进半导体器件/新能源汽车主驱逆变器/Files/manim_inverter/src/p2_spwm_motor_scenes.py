"""Part 2 (Slide 4): Bipolar PWM averaging, scrolling, dotted sine wave, RL current, parameter sweeps, and 3-phase PMSM."""

from __future__ import annotations

import math
import numpy as np
from manim import *

from style import (
    INK,
    INK_MUTED,
    GRID_LIGHT,
    RED_POS,
    BLUE_NEG,
    TEAL_CUR,
    VIOLET_MOD,
    PHASE_U,
    PHASE_V,
    PHASE_W,
    get_times_tex_template,
    math_tnr,
    zh_label,
    setup_canvas_scene,
)
from physics import bipolar_period_duty, solve_rl_periodic_edges
from hbridge import HBridgeCircuit
from plot_utils import (
    make_clean_axes,
    build_p1c_end_state,
    build_spwm_window_mobjects,
    build_p2a_end_state,
    build_three_tier_scope_static,
    build_three_tier_waveforms,
    ModulationHUD,
    build_p2b_end_state,
)


class P2A_BipolarAvgToDottedSine(Scene):
    """Part 2 Shot 1: Push out P1C, single-period bipolar avg calculation, leftward scroll, zoom out to dotted sine."""

    def construct(self) -> None:
        config.tex_template = get_times_tex_template()
        setup_canvas_scene(self)

        # --- Exact Frame 0 matching end of P1C ---
        st = build_p1c_end_state(HBridgeCircuit)
        self.add(st["hb"], st["group"])

        # Push H-bridge left and S1/S3 dead-time plots right cleanly out of full 16:9 viewport
        self.play(
            st["hb"].animate(rate_func=rate_functions.rush_into).shift(LEFT * 13.0),
            st["group"].animate(rate_func=rate_functions.rush_into).shift(RIGHT * 13.0),
            run_time=1.5,
        )
        self.remove(st["hb"], st["group"])

        # --- 1b. Single-Period Bipolar Square Wave Average Calculation ---
        ax = make_clean_axes(np.array([0.0, -0.10, 0.0]), width=9.4, height=4.1, x_range=(0, 1, 0.25), y_range=(-1.35, 1.35, 1.0))
        dash_p = DashedLine(ax.c2p(0, 1), ax.c2p(1, 1), color=GRID_LIGHT, stroke_width=1.3, dash_length=0.09)
        dash_m = DashedLine(ax.c2p(0, -1), ax.c2p(1, -1), color=GRID_LIGHT, stroke_width=1.3, dash_length=0.09)
        lbl_up = math_tnr("+U", font_size=22, color=RED_POS).next_to(ax.c2p(0, 1), LEFT, buff=0.12)
        lbl_z = math_tnr("0", font_size=20, color=INK_MUTED).next_to(ax.c2p(0, 0), LEFT, buff=0.12)
        lbl_dn = math_tnr("-U", font_size=22, color=BLUE_NEG).next_to(ax.c2p(0, -1), LEFT, buff=0.12)
        lbl_y = math_tnr("u(t)", font_size=26, color=INK).next_to(ax.y_axis.get_top(), RIGHT, buff=0.12).shift(DOWN * 0.05)
        lbl_t = math_tnr("t", font_size=24, color=INK).next_to(ax.x_axis.get_right(), RIGHT, buff=0.08)
        decos = VGroup(dash_p, dash_m, lbl_up, lbl_z, lbl_dn, lbl_y, lbl_t)

        # Single-period end tick Ts (0 already labeled by lbl_z)
        tick_ts = math_tnr("T_s", font_size=20, color=INK_MUTED).next_to(ax.c2p(1, 0), DOWN, buff=0.16)
        ts_mark = Line(ax.c2p(1, -0.06), ax.c2p(1, 0.06), color=INK, stroke_width=1.8)
        single_ticks = VGroup(tick_ts, ts_mark)

        # Formula & live D / u_bar header card
        hdr_bg = RoundedRectangle(
            width=8.8,
            height=0.82,
            corner_radius=0.12,
            fill_color="#FFFFFF",
            fill_opacity=0.96,
            stroke_color="#D1CEC4",
            stroke_width=1.5,
        ).move_to([0.0, 2.86, 0.0])

        eq_avg = math_tnr(r"\bar{u} = (2D - 1)U", font_size=30, color=INK)
        d_sym = math_tnr(r"D =", font_size=26, color=INK_MUTED)
        d_num = DecimalNumber(75, num_decimal_places=0, unit=r"\%", font_size=26, color=INK)
        u_sym = math_tnr(r"\bar{u} =", font_size=26, color=VIOLET_MOD)
        u_num = DecimalNumber(0.50, num_decimal_places=2, include_sign=True, unit=r"U", font_size=26, color=VIOLET_MOD)

        hdr_content = VGroup(
            eq_avg,
            VGroup(d_sym, d_num).arrange(RIGHT, buff=0.10),
            VGroup(u_sym, u_num).arrange(RIGHT, buff=0.10),
        ).arrange(RIGHT, buff=0.72).move_to(hdr_bg.get_center())
        header_grp = VGroup(hdr_bg, hdr_content)

        d_val = ValueTracker(0.75)
        dts_lbl = math_tnr("D T_s", font_size=20, color=INK_MUTED)

        def build_single_period() -> VGroup:
            d = float(np.clip(d_val.get_value(), 0.02, 0.98))
            u_bar = 2.0 * d - 1.0

            # Shaded positive & negative areas
            bl_p = ax.c2p(0.0, 0.0)
            tr_p = ax.c2p(d, 1.0)
            area_p = Rectangle(
                width=max(0.01, tr_p[0] - bl_p[0]),
                height=tr_p[1] - bl_p[1],
                fill_color=RED_POS,
                fill_opacity=0.15,
                stroke_width=0,
            ).move_to([0.5 * (bl_p[0] + tr_p[0]), 0.5 * (bl_p[1] + tr_p[1]), 0])

            tl_n = ax.c2p(d, 0.0)
            br_n = ax.c2p(1.0, -1.0)
            area_n = Rectangle(
                width=max(0.01, br_n[0] - tl_n[0]),
                height=tl_n[1] - br_n[1],
                fill_color=BLUE_NEG,
                fill_opacity=0.15,
                stroke_width=0,
            ).move_to([0.5 * (tl_n[0] + br_n[0]), 0.5 * (tl_n[1] + br_n[1]), 0])

            # Step waveform
            pos_ln = Line(ax.c2p(0.0, 1.0), ax.c2p(d, 1.0), color=RED_POS, stroke_width=3.2)
            vert_ln = Line(ax.c2p(d, 1.0), ax.c2p(d, -1.0), color="#4B5563", stroke_width=1.8)
            neg_ln = Line(ax.c2p(d, -1.0), ax.c2p(1.0, -1.0), color=BLUE_NEG, stroke_width=3.2)

            # Moving D*Ts marker on axis
            tick_d = Line(ax.c2p(d, -0.06), ax.c2p(d, 0.06), color=INK, stroke_width=1.6)
            dts_lbl.next_to(ax.c2p(d, 0.0), DOWN, buff=0.16)

            # Violet average bar & midpoint sample dot
            avg_bar = Line(ax.c2p(0.0, u_bar), ax.c2p(1.0, u_bar), color=VIOLET_MOD, stroke_width=3.2)
            avg_dash = DashedLine(ax.c2p(0.5, 0.0), ax.c2p(0.5, u_bar), color=VIOLET_MOD, stroke_width=1.5, dash_length=0.07)
            avg_dot = Dot(ax.c2p(0.5, u_bar), radius=0.095, color=VIOLET_MOD, stroke_color="#FFFFFF", stroke_width=1.4)

            return VGroup(area_p, area_n, pos_ln, vert_ln, neg_ln, tick_d, dts_lbl.copy(), avg_dash, avg_bar, avg_dot)

        last_hdr = [None, None]

        def update_hdr_nums(_mob: Mobject) -> None:
            d = d_val.get_value()
            d_pct = int(round(d * 100.0))
            u_str = f"{2.0 * d - 1.0:.2f}"
            if d_pct != last_hdr[0]:
                d_num.set_value(d_pct)
                d_num.next_to(d_sym, RIGHT, buff=0.10)
                last_hdr[0] = d_pct
            if u_str != last_hdr[1]:
                u_num.set_value(float(u_str))
                u_num.next_to(u_sym, RIGHT, buff=0.10)
                last_hdr[1] = u_str

        single_wave = always_redraw(build_single_period)
        self.play(Create(ax), FadeIn(decos), FadeIn(single_ticks), FadeIn(header_grp), run_time=1.3)
        self.add(single_wave)
        header_grp.add_updater(update_hdr_nums)

        self.wait(3.2)
        self.play(d_val.animate.set_value(0.50), run_time=2.2, rate_func=smooth)
        self.wait(2.8)
        self.play(d_val.animate.set_value(0.25), run_time=2.2, rate_func=smooth)
        self.wait(2.8)

        d_k0, _ = bipolar_period_duty(0, n_sw=24, amp=0.88)
        self.play(d_val.animate.set_value(d_k0), run_time=1.6, rate_func=smooth)

        header_grp.remove_updater(update_hdr_nums)
        self.remove(single_wave)

        # --- 1c. Expand & Scroll Continuously Leftward Through Subsequent Periods ---
        t_start = ValueTracker(0.0)
        t_span = ValueTracker(1.0)

        spwm_dyn = always_redraw(
            lambda: build_spwm_window_mobjects(
                ax,
                t_start=t_start.get_value(),
                t_span=t_span.get_value(),
                n_sw=24,
                amp=0.88,
                show_areas=True,
                show_sine_guide=False,
            )
        )
        self.add(spwm_dyn)

        # Expand window from 1 period -> 3.6 periods
        self.play(
            FadeOut(single_ticks),
            t_span.animate.set_value(3.6),
            run_time=3.2,
            rate_func=smooth,
        )

        # Scroll leftward continuously showing subsequent periods' changing duty & average dots
        last_scroll_hdr = [None, None]

        def update_scroll_hdr(_mob: Mobject) -> None:
            k_center = int(math.floor(t_start.get_value() + 0.5 * t_span.get_value()))
            d_k, u_k = bipolar_period_duty(k_center, n_sw=24, amp=0.88)
            d_pct = int(round(d_k * 100.0))
            u_str = f"{u_k:.2f}"
            if d_pct != last_scroll_hdr[0]:
                d_num.set_value(d_pct)
                d_num.next_to(d_sym, RIGHT, buff=0.10)
                last_scroll_hdr[0] = d_pct
            if u_str != last_scroll_hdr[1]:
                u_num.set_value(float(u_str))
                u_num.next_to(u_sym, RIGHT, buff=0.10)
                last_scroll_hdr[1] = u_str

        header_grp.add_updater(update_scroll_hdr)
        self.play(t_start.animate.set_value(12.0), run_time=10.5, rate_func=linear)
        header_grp.remove_updater(update_scroll_hdr)

        # --- 1d. Zoom Out Time Scale -> Dotted Sine Wave ---
        self.play(
            FadeOut(header_grp, shift=UP * 0.25),
            t_start.animate.set_value(0.0),
            t_span.animate.set_value(24.0),
            run_time=5.5,
            rate_func=smooth,
        )
        self.wait(2.8)

        # Trace faint dashed sine guide through the 24 violet average dots
        ts_g = np.linspace(0.0, 1.0, 160)
        pts_g = [ax.c2p(float(tv), 0.88 * math.sin(2.0 * math.pi * tv)) for tv in ts_g]
        s_curve = VMobject(color=VIOLET_MOD, stroke_width=2.0, stroke_opacity=0.65).set_points_as_corners(pts_g)
        guide_dashed = DashedVMobject(s_curve, num_dashes=48, dashed_ratio=0.55)
        self.play(Create(guide_dashed), run_time=2.4)

        # Match exact build_p2a_end_state() cleanly
        self.remove(spwm_dyn, guide_dashed)
        p2a_end = build_p2a_end_state()
        self.remove(ax, decos)
        self.add(p2a_end["ax"], p2a_end["decos"], p2a_end["wave"])
        self.wait(1.4)


class P2B_SPWMCurrentAndParams(Scene):
    """Part 2 Shots 2-3: Lift dotted-sine SPWM up + draw filtered i(t) below; 3-tier live parameter modulation explorer."""

    def construct(self) -> None:
        config.tex_template = get_times_tex_template()
        setup_canvas_scene(self)

        # Exact end frame of P2A
        p2a = build_p2a_end_state()
        ax_u = p2a["ax"]
        decos_u = p2a["decos"]
        wave_u = p2a["wave"]
        self.add(ax_u, decos_u, wave_u)

        # --- Shot 2: Lift SPWM plot to upper half + draw RL filtered i(t) below ---
        ax_u_up = make_clean_axes(np.array([0.0, 1.68, 0.0]), width=9.4, height=2.25, x_range=(0, 1, 0.25), y_range=(-1.35, 1.35, 1.0))
        dash_p = DashedLine(ax_u_up.c2p(0, 1), ax_u_up.c2p(1, 1), color=GRID_LIGHT, stroke_width=1.2, dash_length=0.09)
        dash_m = DashedLine(ax_u_up.c2p(0, -1), ax_u_up.c2p(1, -1), color=GRID_LIGHT, stroke_width=1.2, dash_length=0.09)
        lbl_up = math_tnr("+U", font_size=20, color=RED_POS).next_to(ax_u_up.c2p(0, 1), LEFT, buff=0.10)
        lbl_z = math_tnr("0", font_size=18, color=INK_MUTED).next_to(ax_u_up.c2p(0, 0), LEFT, buff=0.10)
        lbl_dn = math_tnr("-U", font_size=20, color=BLUE_NEG).next_to(ax_u_up.c2p(0, -1), LEFT, buff=0.10)
        lbl_yu = math_tnr("u(t)", font_size=24, color=INK).next_to(ax_u_up.y_axis.get_top(), RIGHT, buff=0.10).shift(DOWN * 0.05)
        lbl_tu = math_tnr("t", font_size=22, color=INK).next_to(ax_u_up.x_axis.get_right(), DOWN, buff=0.08)
        decos_u_up = VGroup(dash_p, dash_m, lbl_up, lbl_z, lbl_dn, lbl_yu, lbl_tu)
        wave_u_up = build_spwm_window_mobjects(ax_u_up, 0.0, 24.0, n_sw=24, amp=0.88, show_areas=False, show_sine_guide=True)

        ax_i = make_clean_axes(np.array([0.0, -1.70, 0.0]), width=9.4, height=2.25, x_range=(0, 1, 0.25), y_range=(-1.15, 1.15, 1.0))
        lbl_yi = math_tnr("i(t)", font_size=26, color=TEAL_CUR).next_to(ax_i.y_axis.get_top(), RIGHT, buff=0.10).shift(DOWN * 0.05)
        lbl_zi = math_tnr("0", font_size=18, color=INK_MUTED).next_to(ax_i.c2p(0, 0), LEFT, buff=0.10)
        lbl_ti = math_tnr("t", font_size=22, color=INK).next_to(ax_i.x_axis.get_right(), DOWN, buff=0.08)
        decos_i = VGroup(lbl_yi, lbl_zi, lbl_ti)

        self.play(
            Transform(ax_u, ax_u_up),
            Transform(decos_u, decos_u_up),
            Transform(wave_u, wave_u_up),
            Create(ax_i),
            FadeIn(decos_i),
            run_time=1.6,
        )

        # Compute exact periodic RL current from the 24-period bipolar pulses
        edges_24 = [0.0]
        levels_24 = []
        n_sw = 24
        for k in range(n_sw):
            duty, _ = bipolar_period_duty(k, n_sw=n_sw, amp=0.88)
            t0 = k / n_sw
            t_sw = (k + duty) / n_sw
            t1 = (k + 1) / n_sw
            edges_24.extend([t_sw, t1])
            levels_24.extend([1.0, -1.0])
        t_cur_24, i_cur_24 = solve_rl_periodic_edges(np.asarray(edges_24), np.asarray(levels_24), tau=0.14, r_val=1.0)
        i_cur_scaled = np.clip(i_cur_24 * 1.15, -1.05, 1.05)

        t_sweep = ValueTracker(0.0)

        def build_swept_i() -> VGroup:
            t_end = max(0.005, t_sweep.get_value())
            mask = t_cur_24 <= t_end
            ts = t_cur_24[mask]
            ys = i_cur_scaled[mask]
            if len(ts) < 2:
                return VGroup()
            pts = [ax_i.c2p(float(ts[j]), float(ys[j])) for j in range(len(ts))]
            vm = VMobject(color=TEAL_CUR, stroke_width=3.0).set_points_as_corners(pts)
            dot = Dot(pts[-1], radius=0.07, color=TEAL_CUR, stroke_color="#FFFFFF", stroke_width=1.4)
            return VGroup(vm, dot)

        i_dyn = always_redraw(build_swept_i)
        self.add(i_dyn)
        self.play(t_sweep.animate.set_value(1.0), run_time=6.5, rate_func=linear)

        self.remove(i_dyn)
        i_full = VMobject(color=TEAL_CUR, stroke_width=3.0).set_points_as_corners(
            [ax_i.c2p(float(t_cur_24[j]), float(i_cur_scaled[j])) for j in range(len(t_cur_24))]
        )
        self.add(i_full)
        self.wait(2.8)

        # --- Shot 3: 3-Tier Real-Time Modulation Parameter Explorer ---
        scope = build_three_tier_scope_static()
        amp_tr = ValueTracker(0.80)
        freq_tr = ValueTracker(1.00)
        phase_tr = ValueTracker(0.0)
        fsw_tr = ValueTracker(20.0)
        active_card = {"idx": -1}

        hud = ModulationHUD(amp=0.80, freq=1.00, phase_deg=0.0, f_sw=20.0, active_idx=-1)
        init_waves = build_three_tier_waveforms(
            scope["ax_ref"], scope["ax_pwm"], scope["ax_cur"],
            amp=0.80, freq=1.00, phase=0.0, f_sw=20.0,
        )

        # Morph neatly from 2-tier view into 3-tier scope + HUD
        self.play(
            FadeOut(VGroup(ax_u, decos_u, wave_u, ax_i, decos_i, i_full), shift=LEFT * 0.4),
            FadeIn(scope["static_grp"]),
            FadeIn(init_waves),
            FadeIn(hud, shift=LEFT * 0.25),
            run_time=1.8,
        )
        self.remove(init_waves)

        live_waves = always_redraw(
            lambda: build_three_tier_waveforms(
                scope["ax_ref"],
                scope["ax_pwm"],
                scope["ax_cur"],
                amp=amp_tr.get_value(),
                freq=freq_tr.get_value(),
                phase=phase_tr.get_value() * DEGREES,
                f_sw=fsw_tr.get_value(),
            )
        )

        def hud_upd(mob: ModulationHUD) -> None:
            mob.update_values(
                amp=amp_tr.get_value(),
                freq=freq_tr.get_value(),
                phase_deg=phase_tr.get_value(),
                f_sw=fsw_tr.get_value(),
                active_idx=active_card["idx"],
            )

        hud.add_updater(hud_upd)
        self.add(live_waves)

        # 1) Amplitude A variation
        active_card["idx"] = 0
        self.play(amp_tr.animate.set_value(0.35), run_time=2.5, rate_func=smooth)
        self.wait(0.7)
        self.play(amp_tr.animate.set_value(0.95), run_time=2.8, rate_func=smooth)
        self.wait(0.7)
        self.play(amp_tr.animate.set_value(0.80), run_time=1.8, rate_func=smooth)

        # 2) Frequency f variation
        active_card["idx"] = 1
        self.play(freq_tr.animate.set_value(1.80), run_time=2.8, rate_func=smooth)
        self.wait(0.7)
        self.play(freq_tr.animate.set_value(0.65), run_time=3.0, rate_func=smooth)
        self.wait(0.7)
        self.play(freq_tr.animate.set_value(1.00), run_time=2.0, rate_func=smooth)

        # 3) Phase phi variation
        active_card["idx"] = 2
        self.play(phase_tr.animate.set_value(120.0), run_time=2.8, rate_func=smooth)
        self.wait(0.7)
        self.play(phase_tr.animate.set_value(-60.0), run_time=3.2, rate_func=smooth)
        self.wait(0.7)
        self.play(phase_tr.animate.set_value(0.0), run_time=2.0, rate_func=smooth)

        # 4) Switching frequency f_s variation (ripple drops sharply)
        active_card["idx"] = 3
        self.play(fsw_tr.animate.set_value(44.0), run_time=5.2, rate_func=linear)
        self.wait(1.2)

        active_card["idx"] = -1
        hud.remove_updater(hud_upd)
        self.remove(live_waves)
        p2b_end = build_p2b_end_state()
        self.remove(scope["static_grp"], hud)
        self.add(p2b_end["static_grp"], p2b_end["waves"], p2b_end["hud"])
        self.wait(1.4)


def _build_three_phase_assembly() -> dict:
    """Build centered full-size 3-phase inverter + dead-straight horizontal leads + PMSM stator/coils."""
    x_dc = -5.75
    x_legs = [-4.40, -3.05, -1.70]
    y_top = 1.78
    y_bot = -1.78
    y_mid = 0.0

    # Invisible anchor dots so dynamic rotor/flux/dots track scaling & lifting cleanly
    mc_init = np.array([3.20, 0.0, 0.0])
    mc_dot = Dot(mc_init, radius=0.001, fill_opacity=0.0, stroke_opacity=0.0)

    bus = VGroup(
        Line([x_dc, 0.16, 0], [x_dc, y_top, 0], color=INK, stroke_width=2.4),
        Line([x_dc, -0.16, 0], [x_dc, y_bot, 0], color=INK, stroke_width=2.4),
        Line([x_dc - 0.24, 0.16, 0], [x_dc + 0.24, 0.16, 0], color=INK, stroke_width=2.6),
        Line([x_dc - 0.14, -0.16, 0], [x_dc + 0.14, -0.16, 0], color=INK, stroke_width=4.6),
        math_tnr("U", font_size=26, color=INK).move_to([x_dc - 0.44, 0.0, 0]),
        Line([x_dc, y_top, 0], [x_legs[-1], y_top, 0], color=INK, stroke_width=2.5),
        Line([x_dc, y_bot, 0], [x_legs[-1], y_bot, 0], color=INK, stroke_width=2.5),
    )

    legs = VGroup()
    phase_colors = [PHASE_U, PHASE_V, PHASE_W]
    tap_ys = [0.44, 0.00, -0.44]

    for xl, p_col, yt in zip(x_legs, phase_colors, tap_ys):
        # Upper switch: [0.80, 1.32], Lower switch: [-1.32, -0.80]
        w_u1 = Line([xl, y_top, 0], [xl, 1.32, 0], color=INK, stroke_width=2.2)
        b_u = Line([xl, 0.80, 0], [xl, 1.32, 0], color=INK, stroke_width=2.6).rotate(-28 * DEGREES, about_point=np.array([xl, 0.80, 0]))
        w_u2 = Line([xl, 0.80, 0], [xl, -0.80, 0], color=INK, stroke_width=2.2)

        w_d2 = Line([xl, -1.32, 0], [xl, y_bot, 0], color=INK, stroke_width=2.2)
        b_d = Line([xl, -1.32, 0], [xl, -0.80, 0], color=INK, stroke_width=2.6).rotate(-28 * DEGREES, about_point=np.array([xl, -1.32, 0]))

        dots = VGroup(
            Dot([xl, y_top, 0], radius=0.042, color=INK),
            Dot([xl, y_bot, 0], radius=0.042, color=INK),
            Dot([xl, 1.32, 0], radius=0.040, color=INK),
            Dot([xl, 0.80, 0], radius=0.040, color=INK),
            Dot([xl, -0.80, 0], radius=0.040, color=INK),
            Dot([xl, -1.32, 0], radius=0.040, color=INK),
        )

        # Clearly separated parallel diodes (offset -0.46 left, inside [0.64, 1.54] and [-1.54, -0.64])
        xd = xl - 0.46
        d_syms = VGroup()
        for yc in (1.06, -1.06):
            yt_h = yc + 0.46
            yb_h = yc - 0.46
            d_syms.add(
                Dot([xl, yt_h, 0], radius=0.032, color=INK),
                Dot([xl, yb_h, 0], radius=0.032, color=INK),
                Line([xl, yt_h, 0], [xd, yt_h, 0], color=INK, stroke_width=1.6),
                Line([xd, yt_h, 0], [xd, yc + 0.09, 0], color=INK, stroke_width=1.6),
                Line([xd, yc - 0.09, 0], [xd, yb_h, 0], color=INK, stroke_width=1.6),
                Line([xd, yb_h, 0], [xl, yb_h, 0], color=INK, stroke_width=1.6),
                Polygon(
                    [xd, yc + 0.09, 0], [xd - 0.09, yc - 0.09, 0], [xd + 0.09, yc - 0.09, 0],
                    fill_color="#FFFFFF", fill_opacity=1.0, stroke_color=INK, stroke_width=1.8,
                ),
                Line([xd - 0.10, yc + 0.09, 0], [xd + 0.10, yc + 0.09, 0], color=INK, stroke_width=2.0),
            )

        tap_dot = Dot([xl, yt, 0], radius=0.055, color=p_col)
        legs.add(VGroup(w_u1, b_u, w_u2, b_d, w_d2, dots, d_syms, tap_dot))

    # Dead-straight horizontal phase leads from each leg directly to stator outer rim
    r_stator_out = 2.22
    feeders = VGroup()
    feeder_dots: list[tuple[Dot, Dot]] = []
    phase_names = ["U", "V", "W"]
    for xl, yt, p_col, pname in zip(x_legs, tap_ys, phase_colors, phase_names):
        x_port = float(mc_init[0] - math.sqrt(r_stator_out ** 2 - yt ** 2))
        p0 = np.array([xl, yt, 0.0])
        p1 = np.array([x_port, yt, 0.0])
        # Subtle background knockout halo where straight leads cross subsequent vertical legs
        halo = Line(p0 + RIGHT * 0.14, p1, color="#FCFBF8", stroke_width=7.0)
        wire = Line(p0, p1, color=p_col, stroke_width=2.8)
        port_dot = Dot(p1, radius=0.052, color=p_col)
        lbl = math_tnr(pname, font_size=22, color=p_col).move_to([-0.28, yt + 0.20, 0.0])
        d_start = Dot(p0, radius=0.001, fill_opacity=0.0, stroke_opacity=0.0)
        d_end = Dot(p1, radius=0.001, fill_opacity=0.0, stroke_opacity=0.0)
        feeder_dots.append((d_start, d_end))
        feeders.add(VGroup(halo, wire, port_dot, lbl, d_start, d_end))

    inv_tag = zh_label("三相全桥", font_size=22, color=INK).move_to([-3.25, -2.28, 0.0])

    # Stator & coils on right centered at y = 0.0
    stator_ring = Annulus(
        inner_radius=1.45,
        outer_radius=r_stator_out,
        fill_color="#EAE7DF",
        fill_opacity=1.0,
        stroke_color=INK,
        stroke_width=2.4,
    ).move_to(mc_init)

    coil_specs = [
        (90 * DEGREES, PHASE_U, "U+"),
        (270 * DEGREES, PHASE_U, "U-"),
        (210 * DEGREES, PHASE_V, "V+"),
        (30 * DEGREES, PHASE_V, "V-"),
        (330 * DEGREES, PHASE_W, "W+"),
        (150 * DEGREES, PHASE_W, "W-"),
    ]
    coil_bases = VGroup()
    coil_labels = VGroup()
    for ang, col, name in coil_specs:
        pos = mc_init + np.array([1.72 * math.cos(ang), 1.72 * math.sin(ang), 0.0])
        c_ring = Circle(radius=0.23, fill_color="#FFFFFF", fill_opacity=1.0, stroke_color=col, stroke_width=2.4).move_to(pos)
        coil_bases.add(c_ring)
        lbl_pos = mc_init + np.array([2.48 * math.cos(ang), 2.48 * math.sin(ang), 0.0])
        coil_labels.add(math_tnr(name, font_size=19, color=col).move_to(lbl_pos))

    motor_tag = zh_label("永磁同步电机", font_size=22, color=INK).move_to(mc_init + DOWN * 2.92)

    return {
        "inv_grp": VGroup(bus, legs, inv_tag),
        "feeders": feeders,
        "stator_grp": VGroup(stator_ring, coil_bases, coil_labels, motor_tag),
        "mc_dot": mc_dot,
        "feeder_dots": feeder_dots,
        "coil_specs": coil_specs,
    }


class P2C_ThreePhaseMotor(Scene):
    """Part 2 Shot 4: Clear all plots, draw centered 3-phase bridge with straight leads + PMSM, shrink to top & show full-width lower 3-phase currents."""

    def construct(self) -> None:
        config.tex_template = get_times_tex_template()
        setup_canvas_scene(self)

        # Exact end frame of P2B
        p2b = build_p2b_end_state()
        all_prev = VGroup(p2b["static_grp"], p2b["waves"], p2b["hud"])
        self.add(all_prev)

        # Clear all previous plots cleanly
        self.play(FadeOut(all_prev, scale=0.96), run_time=1.3)
        self.remove(all_prev)

        # --- Stage 1: Full-size centered 3-phase inverter + straight horizontal leads + PMSM ---
        asm = _build_three_phase_assembly()
        mc_dot: Dot = asm["mc_dot"]
        coil_specs = asm["coil_specs"]

        n_txt_base = math_tnr(r"\mathbf{N}", font_size=26, color="#FFFFFF")
        s_txt_base = math_tnr(r"\mathbf{S}", font_size=26, color="#FFFFFF")
        bs_lbl_base = math_tnr(r"\vec{B}_s", font_size=24, color=VIOLET_MOD)

        def make_rotor(center_pt: np.ndarray, scale_f: float, theta_rad: float) -> VGroup:
            r_rot = 0.86 * scale_f
            n_half = Sector(
                radius=r_rot,
                start_angle=theta_rad - PI / 2,
                angle=PI,
                fill_color=RED_POS,
                fill_opacity=0.92,
                stroke_color=INK,
                stroke_width=2.0,
            ).shift(center_pt)
            s_half = Sector(
                radius=r_rot,
                start_angle=theta_rad + PI / 2,
                angle=PI,
                fill_color=BLUE_NEG,
                fill_opacity=0.92,
                stroke_color=INK,
                stroke_width=2.0,
            ).shift(center_pt)
            shaft = Circle(radius=0.16 * scale_f, fill_color="#FFFFFF", fill_opacity=1.0, stroke_color=INK, stroke_width=2.0).move_to(center_pt)
            n_txt = n_txt_base.copy().scale(scale_f).move_to(
                center_pt + np.array([0.46 * scale_f * math.cos(theta_rad), 0.46 * scale_f * math.sin(theta_rad), 0.0])
            )
            s_txt = s_txt_base.copy().scale(scale_f).move_to(
                center_pt + np.array([-0.46 * scale_f * math.cos(theta_rad), -0.46 * scale_f * math.sin(theta_rad), 0.0])
            )
            return VGroup(n_half, s_half, shaft, n_txt, s_txt)

        rotor_static = make_rotor(mc_dot.get_center(), scale_f=1.0, theta_rad=0.0)

        self.play(Create(asm["inv_grp"]), run_time=2.2)
        self.play(Create(asm["feeders"]), run_time=1.3)
        self.play(Create(asm["stator_grp"]), FadeIn(rotor_static, scale=0.88), run_time=2.2)
        self.wait(0.8)

        # --- Stage 2: Shrink & lift entire 3-phase assembly to upper half; full-width 3-phase waveform below ---
        UPPER_SCALE = 0.58
        top_assembly = VGroup(asm["inv_grp"], asm["feeders"], asm["stator_grp"], rotor_static, mc_dot)

        ax_3ph = make_clean_axes(
            np.array([0.0, -2.02, 0.0]),
            width=11.2,
            height=2.45,
            x_range=(0, 2 * PI, PI / 2),
            y_range=(-1.32, 1.32, 1.0),
        )
        ts_3 = np.linspace(0.0, 2.0 * PI, 180)
        w_u = VMobject(color=PHASE_U, stroke_width=2.6).set_points_as_corners([ax_3ph.c2p(float(t), math.sin(t)) for t in ts_3])
        w_v = VMobject(color=PHASE_V, stroke_width=2.6).set_points_as_corners([ax_3ph.c2p(float(t), math.sin(t - 2 * PI / 3)) for t in ts_3])
        w_w = VMobject(color=PHASE_W, stroke_width=2.6).set_points_as_corners([ax_3ph.c2p(float(t), math.sin(t + 2 * PI / 3)) for t in ts_3])
        lbl_3ph = VGroup(
            math_tnr("i_u,", font_size=22, color=PHASE_U),
            math_tnr("i_v,", font_size=22, color=PHASE_V),
            math_tnr("i_w", font_size=22, color=PHASE_W),
            math_tnr("(120^\\circ)", font_size=20, color=INK_MUTED),
        ).arrange(RIGHT, buff=0.07).next_to(ax_3ph, UP, buff=0.10, aligned_edge=LEFT)
        t_lbl = math_tnr("t", font_size=22, color=INK).next_to(ax_3ph.x_axis.get_right(), RIGHT, buff=0.08)

        self.play(
            top_assembly.animate.scale(UPPER_SCALE).move_to(np.array([0.0, 1.72, 0.0])),
            Create(ax_3ph),
            FadeIn(lbl_3ph, t_lbl),
            run_time=1.5,
        )
        self.play(Create(w_u), Create(w_v), Create(w_w), run_time=1.4)

        # --- Stage 3: Synchronized 2-Rotation Finale ---
        top_assembly.remove(rotor_static)
        self.remove(rotor_static)
        theta_tr = ValueTracker(0.0)

        def build_dynamic_motor() -> VGroup:
            th = theta_tr.get_value()
            mc = mc_dot.get_center()
            rotor = make_rotor(mc, scale_f=UPPER_SCALE, theta_rad=th)

            # Rotating Stator Flux Arrow Bs
            bs_end = mc + np.array([1.30 * UPPER_SCALE * math.cos(th), 1.30 * UPPER_SCALE * math.sin(th), 0.0])
            bs_arr = Arrow(mc, bs_end, buff=0.0, color=VIOLET_MOD, stroke_width=3.8, max_tip_length_to_length_ratio=0.20)
            bs_lbl = bs_lbl_base.copy().scale(0.82).move_to(
                mc + np.array([1.14 * UPPER_SCALE * math.cos(th + 0.34), 1.14 * UPPER_SCALE * math.sin(th + 0.34), 0.0])
            )

            iu = math.sin(th)
            iv = math.sin(th - 2 * PI / 3)
            iw = math.sin(th + 2 * PI / 3)
            phase_vals = [iu, -iu, iv, -iv, iw, -iw]
            coil_glows = VGroup()
            for (ang, col, _nm), pval in zip(coil_specs, phase_vals):
                pos = mc + np.array([1.72 * UPPER_SCALE * math.cos(ang), 1.72 * UPPER_SCALE * math.sin(ang), 0.0])
                op = max(0.08, 0.80 * abs(pval))
                c_fill = Circle(radius=0.21 * UPPER_SCALE, fill_color=col, fill_opacity=op, stroke_width=0).move_to(pos)
                coil_glows.add(c_fill)

            # Animated current pulses along the dead-straight U, V, W horizontal wires
            feeder_dots_vis = VGroup()
            for (d0, d1), col, cur in zip(asm["feeder_dots"], [PHASE_U, PHASE_V, PHASE_W], [iu, iv, iw]):
                p0 = d0.get_center()
                p1 = d1.get_center()
                for k_dot in range(4):
                    s = (k_dot / 4.0 + (0.35 * th if cur >= 0 else -0.35 * th)) % 1.0
                    d_pos = (1.0 - s) * p0 + s * p1
                    r_dot = (0.025 + 0.036 * abs(cur))
                    feeder_dots_vis.add(Dot(d_pos, radius=r_dot, color=col, fill_opacity=0.35 + 0.60 * abs(cur)))

            # Wide lower sync cursor across full-width 3-phase plot
            t_mod = th % (2 * PI)
            xc = ax_3ph.c2p(t_mod, 0)[0]
            y_hi = ax_3ph.c2p(0, 1.15)[1]
            y_lo = ax_3ph.c2p(0, -1.15)[1]
            cur_line = Line([xc, y_lo, 0], [xc, y_hi, 0], color=INK, stroke_width=1.8, stroke_opacity=0.65)
            du = Dot(ax_3ph.c2p(t_mod, iu), radius=0.075, color=PHASE_U, stroke_color="#FFFFFF", stroke_width=1.2)
            dv = Dot(ax_3ph.c2p(t_mod, iv), radius=0.075, color=PHASE_V, stroke_color="#FFFFFF", stroke_width=1.2)
            dw = Dot(ax_3ph.c2p(t_mod, iw), radius=0.075, color=PHASE_W, stroke_color="#FFFFFF", stroke_width=1.2)

            return VGroup(coil_glows, rotor, bs_arr, bs_lbl, feeder_dots_vis, cur_line, du, dv, dw)

        dyn_motor = always_redraw(build_dynamic_motor)
        self.add(dyn_motor)
        self.play(theta_tr.animate.set_value(4.0 * PI), run_time=11.0, rate_func=linear)
        self.wait(1.8)
