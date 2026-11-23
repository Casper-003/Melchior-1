"""Part 1 (Slide 3): Single-phase H-bridge, bipolar square wave, derivation, freewheeling, and dead-time."""

from __future__ import annotations

import math
from pathlib import Path
import numpy as np
from PIL import Image
from manim import *

from style import (
    INK,
    INK_MUTED,
    RULE_COLOR,
    RED_POS,
    BLUE_NEG,
    AMBER_FW,
    AMBER_BAND,
    TEAL_CUR,
    SHORT_RED,
    HBRIDGE_CENTER_SCALE,
    HBRIDGE_CENTER_POS,
    HBRIDGE_LEFT_SCALE,
    HBRIDGE_LEFT_POS,
    HBRIDGE_TOPLEFT_SCALE,
    HBRIDGE_TOPLEFT_POS,
    UT_CENTER_POS,
    UT_UPPER_POS,
    IT_LOWER_POS,
    PLOT_RIGHT_W,
    get_times_tex_template,
    math_tnr,
    zh_label,
    setup_canvas_scene,
    make_status_pill,
)
from physics import square_u, triangle_i, hbridge_mode_at, gate_states_deadtime
from hbridge import HBridgeCircuit
from plot_utils import (
    build_ut_plot_group,
    build_it_plot_group,
    build_alignment_guides,
    build_square_u_waveform,
    build_triangle_i_waveform,
    build_freewheeling_bands,
    build_p1b_end_state,
    build_deadtime_plots_group,
    build_p1c_end_state,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXPLOSION_DIR = PROJECT_ROOT / "assets" / "explosion"


def _load_explosion_arrays() -> tuple[list[np.ndarray], np.ndarray]:
    frames = []
    for idx in range(24):
        arr = np.array(Image.open(EXPLOSION_DIR / f"exp_{idx:02d}.png").convert("RGBA"), dtype=np.uint8)
        frames.append(arr)
    soot = np.array(Image.open(EXPLOSION_DIR / "soot.png").convert("RGBA"), dtype=np.uint8)
    return frames, soot


class P1A_CanvasAndHBridge(Scene):
    """Shots 2-3: Draw H-bridge with parallel diodes & RL load directly on canvas, flash legs/load, show red/blue conduction."""

    def construct(self) -> None:
        config.tex_template = get_times_tex_template()
        setup_canvas_scene(self)

        # --- Draw black-ink H-bridge directly with RL load & clear parallel diodes ---
        hb = HBridgeCircuit(rl_mode=True)
        hb.scale(HBRIDGE_CENTER_SCALE)
        hb.move_to(HBRIDGE_CENTER_POS)

        self.play(Create(hb.bus_group), run_time=1.6)
        self.play(Create(hb.left_sw_group), run_time=1.4)
        self.play(Create(hb.left_diode_group), run_time=1.2)
        self.play(Create(hb.right_sw_group), run_time=1.4)
        self.play(Create(hb.right_diode_group), run_time=1.2)
        self.play(Create(hb.load_leads_group), Create(hb.active_load), run_time=1.2)
        self.add(hb)

        # Exact 1.0s pause after completing circuit drawing
        self.wait(1.0)

        def flash_capsules(mobs: list[Mobject], color: str, flashes: int = 2) -> None:
            glows = VGroup()
            for mb in mobs:
                cap = SurroundingRectangle(
                    mb,
                    buff=0.18,
                    corner_radius=0.16,
                    color=color,
                    fill_color=color,
                    fill_opacity=0.16,
                    stroke_width=2.6,
                )
                glows.add(cap)
            for _ in range(flashes):
                self.play(FadeIn(glows, run_time=0.28), *[Indicate(m, color=color, scale_factor=1.08, run_time=0.28) for m in mobs])
                self.play(FadeOut(glows, run_time=0.32))

        # Flash left leg switches (S1, S3)
        flash_capsules([hb.switches["S1"]["blade"], hb.switches["S3"]["blade"]], RED_POS, flashes=2)

        # Exact 0.5s pause before right leg
        self.wait(0.5)

        # Flash right leg switches (S2, S4)
        flash_capsules([hb.switches["S2"]["blade"], hb.switches["S4"]["blade"]], BLUE_NEG, flashes=2)

        # Matching 0.5s pause before RL load
        self.wait(0.5)

        # Flash central RL load
        flash_capsules([hb.active_load], AMBER_FW, flashes=2)

        # --- Red loop (S1, S4) with +U polarity, then Blue loop (S2, S3) with -U polarity ---
        flow_t = ValueTracker(0.0)
        mode_state = {"mode": "S1_S4"}

        overlay = always_redraw(
            lambda: hb.build_current_overlay(
                mode_state["mode"],
                phase=flow_t.get_value(),
                n_markers=16,
                stroke_scale=HBRIDGE_CENTER_SCALE,
            )
        )

        # Conduct S1, S4 -> Red loop + (+U) polarity
        self.play(*hb.animate_switch_state(s1=True, s4=True), run_time=0.45)
        hb.set_polarity(+1)
        self.add(overlay)
        self.play(flow_t.animate.set_value(2.0), run_time=3.8, rate_func=linear)

        # Swap to S2, S3 -> Blue loop + (-U) polarity
        self.remove(overlay)
        hb.set_polarity(0)
        self.play(*hb.animate_switch_state(s1=False, s4=False, s2=True, s3=True), run_time=0.50)
        mode_state["mode"] = "S2_S3"
        hb.set_polarity(-1)
        self.add(overlay)
        self.play(flow_t.animate.set_value(4.0), run_time=3.8, rate_func=linear)

        # Return cleanly to neutral open H-bridge (exact start state of P1B)
        self.remove(overlay)
        hb.set_polarity(0)
        sw_rst = hb.animate_switch_state(s1=False, s2=False, s3=False, s4=False)
        if sw_rst:
            self.play(*sw_rst, run_time=0.45)
        self.wait(0.4)


class P1B_SquareWaveAndDerivation(Scene):
    """Shots 4-7: Shrink circuit left + alternating u(t), shrink & lift + Times New Roman derivation, lift u(t) + draw i(t)."""

    def construct(self) -> None:
        config.tex_template = get_times_tex_template()
        setup_canvas_scene(self)

        # Exact final frame of P1A (already RL mode!)
        hb = HBridgeCircuit(rl_mode=True)
        hb.scale(HBRIDGE_CENTER_SCALE)
        hb.move_to(HBRIDGE_CENTER_POS)
        self.add(hb)

        # --- Shot 4: Shrink left + alternate switches & polarity in lockstep with u(t) ---
        ut_ax, ut_decos = build_ut_plot_group(UT_CENTER_POS, width=PLOT_RIGHT_W, height=3.15, t_max=3.0)
        self.play(
            hb.animate.scale(HBRIDGE_LEFT_SCALE / HBRIDGE_CENTER_SCALE).move_to(HBRIDGE_LEFT_POS),
            Create(ut_ax),
            FadeIn(ut_decos),
            run_time=1.3,
        )

        t_sweep = ValueTracker(0.0)
        flow_t = ValueTracker(0.0)

        # Direct updater ON hb prevents Manim static-background freeze!
        def sync_hb_shot4(mob: HBridgeCircuit) -> None:
            t_cur = min(2.999, t_sweep.get_value())
            is_pos = square_u(t_cur, period=1.0) > 0
            mob.set_switch_state(s1=is_pos, s4=is_pos, s2=not is_pos, s3=not is_pos)
            mob.set_polarity(+1 if is_pos else -1)

        hb.add_updater(sync_hb_shot4)

        hb_ov = always_redraw(
            lambda: hb.build_current_overlay(
                "S1_S4" if square_u(min(2.999, t_sweep.get_value()), period=1.0) > 0 else "S2_S3",
                phase=flow_t.get_value(),
                n_markers=14,
                stroke_scale=HBRIDGE_LEFT_SCALE,
            )
        )
        ut_wave_dyn = always_redraw(lambda: build_square_u_waveform(ut_ax, t_end=t_sweep.get_value(), stroke_w=3.0))
        self.add(hb_ov, ut_wave_dyn)

        self.play(
            t_sweep.animate.set_value(3.0),
            flow_t.animate.set_value(4.5),
            run_time=10.5,
            rate_func=linear,
        )

        hb.remove_updater(sync_hb_shot4)
        self.remove(hb_ov, ut_wave_dyn)
        ut_wave_static = build_square_u_waveform(ut_ax, t_end=3.0, stroke_w=3.0)
        ut_wave_static.remove(ut_wave_static[-1])
        self.add(ut_wave_static)
        hb.set_polarity(0)
        sw_rst = hb.animate_switch_state(False, False, False, False)
        if sw_rst:
            self.play(*sw_rst, run_time=0.4)

        # --- Shot 5: Shrink further & lift top-left to make room for RL formula derivation ---
        rule = Line([-6.05, 0.34, 0], [-0.75, 0.34, 0], color=RULE_COLOR, stroke_width=1.6)
        self.play(
            hb.animate.scale(HBRIDGE_TOPLEFT_SCALE / HBRIDGE_LEFT_SCALE).move_to(HBRIDGE_TOPLEFT_POS),
            Create(rule),
            run_time=1.2,
        )
        self.play(Indicate(hb.active_load, color=TEAL_CUR, scale_factor=1.10), run_time=0.8)

        # --- Shot 6: Times New Roman derivation in bottom-left ---
        eq1 = math_tnr(r"u = R\,i + L\,\frac{di}{dt}", font_size=30, color=INK).move_to([-3.55, -0.22, 0])
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

        self.play(Write(eq1), run_time=1.8)
        self.wait(1.8)
        self.play(FadeIn(eq2_note, shift=UP * 0.08), run_time=1.0)
        self.wait(1.8)
        self.play(Write(eq3), run_time=1.6)
        self.wait(1.8)
        self.play(Create(eq4_box), Write(eq4), run_time=2.0)
        self.wait(1.8)

        # --- Shot 7: Lift u(t) to upper half, draw i(t) below ---
        ut_upper_ax, ut_upper_decos = build_ut_plot_group(UT_UPPER_POS, width=PLOT_RIGHT_W, height=2.25, t_max=3.0)
        ut_upper_wave = build_square_u_waveform(ut_upper_ax, t_end=3.0, stroke_w=2.8)
        ut_upper_wave.remove(ut_upper_wave[-1])

        it_ax, it_decos = build_it_plot_group(IT_LOWER_POS, width=PLOT_RIGHT_W, height=2.25, t_max=3.0)
        guides = build_alignment_guides(ut_upper_ax, it_ax, [0.5, 1.0, 1.5, 2.0, 2.5])

        self.play(
            Transform(ut_ax, ut_upper_ax),
            Transform(ut_decos, ut_upper_decos),
            Transform(ut_wave_static, ut_upper_wave),
            Create(it_ax),
            FadeIn(it_decos),
            Create(guides),
            run_time=1.6,
        )

        t_i = ValueTracker(0.0)
        it_wave_dyn = always_redraw(lambda: build_triangle_i_waveform(it_ax, t_end=t_i.get_value(), stroke_w=2.8))
        self.add(it_wave_dyn)
        self.play(t_i.animate.set_value(3.0), run_time=7.8, rate_func=linear)

        self.remove(it_wave_dyn)
        it_wave_static = build_triangle_i_waveform(it_ax, t_end=3.0, stroke_w=2.8)
        it_wave_static.remove(it_wave_static[-1])
        self.add(it_wave_static)
        self.wait(1.4)


class P1C_FreewheelingAndDeadtime(Scene):
    """Shots 8-11: Time-aligned freewheeling demo, nonlinear slide-out, centered shoot-through boom, synchronized dead-time."""

    def construct(self) -> None:
        config.tex_template = get_times_tex_template()
        setup_canvas_scene(self)

        # Exact end state of P1B
        st = build_p1b_end_state(HBridgeCircuit)
        hb: HBridgeCircuit = st["hb"]
        rule = st["rule"]
        eq1, eq2_note, eq3, eq4_grp = st["eq1"], st["eq2_note"], st["eq3"], st["eq4_grp"]
        ut_ax, ut_decos, ut_wave = st["ut_ax"], st["ut_decos"], st["ut_wave"]
        it_ax, it_decos, it_wave = st["it_ax"], st["it_decos"], st["it_wave"]
        guides = st["guides"]
        self.add(hb, rule, eq1, eq2_note, eq3, eq4_grp, ut_ax, ut_decos, ut_wave, it_ax, it_decos, it_wave, guides)

        # --- Shot 8: Time-synced freewheeling demonstration across cycles ---
        fw_bands = build_freewheeling_bands(it_ax, t_max=3.0, period=1.0)
        self.play(FadeIn(fw_bands), run_time=1.0)

        pills = {
            "S1_S4": make_status_pill(math_tnr(r"S_1, S_4\ (u=+U,\, i>0)", font_size=19, color=RED_POS), RED_POS),
            "S2_S3": make_status_pill(math_tnr(r"S_2, S_3\ (u=-U,\, i<0)", font_size=19, color=BLUE_NEG), BLUE_NEG),
            "D2_D3": make_status_pill(
                VGroup(math_tnr("D_2, D_3", font_size=19, color=AMBER_FW), zh_label("续流", font_size=16, color=AMBER_FW)).arrange(RIGHT, buff=0.08),
                AMBER_FW,
            ),
            "D1_D4": make_status_pill(
                VGroup(math_tnr("D_1, D_4", font_size=19, color=AMBER_FW), zh_label("续流", font_size=16, color=AMBER_FW)).arrange(RIGHT, buff=0.08),
                AMBER_FW,
            ),
        }
        pill_pos = np.array([-3.45, 3.24, 0.0])
        pill_group = VGroup(*pills.values())
        for p in pills.values():
            p.move_to(pill_pos)
            p.set_opacity(0.0)
        self.add(pill_group)

        t_cur = ValueTracker(0.26)
        flow_t = ValueTracker(0.0)
        last_pill_mode = [None]

        y_top_cursor = ut_ax.c2p(0, 1.24)[1]
        y_bot_cursor = it_ax.c2p(0, -1.24)[1]

        def sync_hb_shot8(mob: HBridgeCircuit) -> None:
            tv = min(2.999, max(0.0, t_cur.get_value()))
            mode = hbridge_mode_at(tv)
            if mode == "S1_S4":
                mob.set_switch_state(s1=True, s4=True, s2=False, s3=False)
                mob.set_polarity(+1)
            elif mode == "S2_S3":
                mob.set_switch_state(s1=False, s4=False, s2=True, s3=True)
                mob.set_polarity(-1)
            else:
                mob.set_switch_state(s1=False, s2=False, s3=False, s4=False)
                mob.set_polarity(+1 if mode == "D1_D4" else -1)

        def sync_pill_shot8(_mob: VGroup) -> None:
            tv = min(2.999, max(0.0, t_cur.get_value()))
            mode = hbridge_mode_at(tv)
            if mode != last_pill_mode[0]:
                for k_m, p_mob in pills.items():
                    p_mob.set_opacity(1.0 if k_m == mode else 0.0)
                last_pill_mode[0] = mode

        hb.add_updater(sync_hb_shot8)
        pill_group.add_updater(sync_pill_shot8)

        def build_sync_cursor() -> VGroup:
            tv = min(2.999, max(0.0, t_cur.get_value()))
            xc = ut_ax.c2p(tv, 0)[0]
            line = Line([xc, y_top_cursor, 0], [xc, y_bot_cursor, 0], color=INK, stroke_width=1.8, stroke_opacity=0.65)
            uv = square_u(tv)
            iv = triangle_i(tv)
            mode = hbridge_mode_at(tv)
            dot_col = AMBER_FW if mode.startswith("D") else (RED_POS if uv > 0 else BLUE_NEG)
            du = Dot(ut_ax.c2p(tv, uv), radius=0.075, color=dot_col, stroke_color="#FFFFFF", stroke_width=1.4)
            di = Dot(it_ax.c2p(tv, iv), radius=0.075, color=dot_col, stroke_color="#FFFFFF", stroke_width=1.4)
            return VGroup(line, du, di)

        fw_overlay = always_redraw(
            lambda: hb.build_current_overlay(
                hbridge_mode_at(min(2.999, max(0.0, t_cur.get_value()))),
                phase=flow_t.get_value(),
                n_markers=14,
                stroke_scale=HBRIDGE_TOPLEFT_SCALE,
            )
        )
        sync_cursor = always_redraw(build_sync_cursor)
        self.add(sync_cursor, fw_overlay)

        # Cycle 1 paced thoughtfully with slow-beat during D2, D3 freewheeling
        self.play(t_cur.animate.set_value(0.49), flow_t.animate.set_value(1.1), run_time=2.2, rate_func=linear)
        self.play(t_cur.animate.set_value(0.56), flow_t.animate.set_value(1.6), run_time=1.0, rate_func=linear)
        self.play(t_cur.animate.set_value(0.68), flow_t.animate.set_value(3.0), run_time=3.2, rate_func=linear)
        self.play(t_cur.animate.set_value(0.75), flow_t.animate.set_value(3.5), run_time=1.0, rate_func=linear)
        self.play(t_cur.animate.set_value(1.00), flow_t.animate.set_value(4.7), run_time=2.6, rate_func=linear)
        self.play(t_cur.animate.set_value(1.25), flow_t.animate.set_value(6.1), run_time=3.0, rate_func=linear)
        self.play(t_cur.animate.set_value(3.00), flow_t.animate.set_value(12.6), run_time=11.0, rate_func=linear)

        hb.remove_updater(sync_hb_shot8)
        pill_group.remove_updater(sync_pill_shot8)
        self.remove(sync_cursor, fw_overlay, pill_group)
        hb.set_polarity(0)
        sw_rst = hb.animate_switch_state(False, False, False, False)
        if sw_rst:
            self.play(*sw_rst, run_time=0.4)

        # --- Shot 9: Nonlinear slide-out right of both plots + bring H-bridge to CENTER for explosion ---
        BOOM_SCALE = 0.90
        right_plots = VGroup(ut_ax, ut_decos, ut_wave, it_ax, it_decos, it_wave, guides, fw_bands)
        self.play(
            right_plots.animate(rate_func=rate_functions.rush_into).shift(RIGHT * 13.0),
            FadeOut(VGroup(rule, eq1, eq2_note, eq3, eq4_grp)),
            hb.animate.scale(BOOM_SCALE / HBRIDGE_TOPLEFT_SCALE).move_to(HBRIDGE_CENTER_POS),
            run_time=1.7,
        )
        self.remove(right_plots)

        # --- Shot 10: Simultaneous S1 & S3 shoot-through short + centered cheap meme explosions ---
        self.play(*hb.animate_switch_state(s1=True, s3=True, s2=False, s4=False, short_left=True), run_time=0.40)

        short_flow = ValueTracker(0.0)
        short_ov = always_redraw(
            lambda: hb.build_current_overlay(
                "SHORT_LEFT",
                phase=short_flow.get_value(),
                n_markers=14,
                stroke_scale=BOOM_SCALE * 1.12,
            )
        )
        self.add(short_ov)
        self.play(short_flow.animate.set_value(3.2), run_time=1.8, rate_func=linear)

        # Nervous warning jitter before boom
        base_hb_pos = hb.get_center().copy()
        jitter_t = ValueTracker(0.0)

        def jitter_updater(mob: Mobject) -> None:
            jv = jitter_t.get_value()
            dx = 0.055 * math.sin(65.0 * jv)
            dy = 0.045 * math.cos(83.0 * jv)
            mob.move_to(base_hb_pos + np.array([dx, dy, 0.0]))

        hb.add_updater(jitter_updater)
        self.play(jitter_t.animate.set_value(0.6), short_flow.animate.set_value(4.5), run_time=0.6, rate_func=linear)
        hb.remove_updater(jitter_updater)
        hb.move_to(base_hb_pos)

        exp_frames, soot_arr = _load_explosion_arrays()
        pt_s1 = hb.get_anchor("s1_center")
        pt_s3 = hb.get_anchor("s3_center")
        pt_dc = hb.get_anchor("dc_center")

        boom_t = ValueTracker(0.0)
        boom_specs = [
            (pt_s1, 0.00, 1.95),
            (pt_s3, 0.14, 1.95),
            (pt_dc, 0.28, 2.20),
        ]

        empty_frame = np.zeros((224, 224, 4), dtype=np.uint8)
        boom_mobs = []
        for pos, delay, size_w in boom_specs:
            im = ImageMobject(empty_frame)
            im.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
            im.set(width=size_w)
            im.move_to(pos)
            im.set_z_index(25)

            def make_sprite_upd(d_sec: float):
                def _upd(mob: ImageMobject) -> None:
                    dt = boom_t.get_value() - d_sec
                    if dt < 0.0:
                        mob.pixel_array[:] = empty_frame
                        return
                    f_idx = int(dt * 18.0)
                    if f_idx >= len(exp_frames):
                        mob.pixel_array[:] = empty_frame
                    else:
                        mob.pixel_array[:] = exp_frames[f_idx]
                return _upd

            im.add_updater(make_sprite_upd(delay))
            boom_mobs.append(im)
            self.add(im)

        def boom_shake(mob: Mobject) -> None:
            bt = boom_t.get_value()
            if bt < 0.55:
                amp = 0.11 * math.exp(-5.0 * bt)
                mob.move_to(base_hb_pos + np.array([amp * math.sin(52.0 * bt), amp * 0.7 * math.cos(68.0 * bt), 0.0]))
            else:
                mob.move_to(base_hb_pos)

        hb.add_updater(boom_shake)
        self.play(boom_t.animate.set_value(1.65), short_flow.animate.set_value(6.5), run_time=1.65, rate_func=linear)
        hb.remove_updater(boom_shake)
        hb.move_to(base_hb_pos)
        for bm in boom_mobs:
            bm.clear_updaters()
            self.remove(bm)

        soots = Group()
        for pos, _delay, size_w in boom_specs:
            sm = ImageMobject(soot_arr)
            sm.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
            sm.set(width=size_w * 0.72)
            sm.move_to(pos)
            sm.set_z_index(15)
            soots.add(sm)
        self.add(soots)
        self.wait(1.0)

        # --- Shot 11: Restore normal circuit, move H-bridge LEFT, draw right S1/S3 gate plots, sync switches ---
        self.remove(short_ov)
        self.play(
            FadeOut(soots),
            *hb.animate_switch_state(False, False, False, False),
            run_time=0.7,
        )

        dt = build_deadtime_plots_group(td=0.08, t_max=2.0)
        self.play(
            hb.animate.scale(HBRIDGE_LEFT_SCALE / BOOM_SCALE).move_to(HBRIDGE_LEFT_POS),
            Create(dt["ax_s1"]),
            Create(dt["ax_s3"]),
            FadeIn(dt["axes_decos"]),
            run_time=1.2,
        )
        self.play(Create(dt["wave_s1"]), Create(dt["wave_s3"]), run_time=1.4)
        self.play(FadeIn(dt["bands"]), FadeIn(dt["td_callout"]), run_time=1.0)

        # Synchronized gate timing sweep showing S1 & S3 blades & capsule indicators in real time!
        gate_t = ValueTracker(0.0)
        y_top_g = dt["ax_s1"].c2p(0, 1.18)[1]
        y_bot_g = dt["ax_s3"].c2p(0, -0.15)[1]

        dt_pills = {
            "S1": make_status_pill(VGroup(math_tnr("S_1", font_size=20, color=RED_POS), zh_label("导通", font_size=17, color=RED_POS)).arrange(RIGHT, buff=0.08), RED_POS),
            "S3": make_status_pill(VGroup(math_tnr("S_3", font_size=20, color=BLUE_NEG), zh_label("导通", font_size=17, color=BLUE_NEG)).arrange(RIGHT, buff=0.08), BLUE_NEG),
            "DT": make_status_pill(VGroup(zh_label("死区：", font_size=17, color="#B45309"), math_tnr("S_1, S_3", font_size=20, color="#B45309"), zh_label("全断", font_size=17, color="#B45309")).arrange(RIGHT, buff=0.06), "#B45309"),
        }
        dt_pill_pos = np.array([-3.45, 2.35, 0.0])
        dt_pill_grp = VGroup(*dt_pills.values())
        for p in dt_pills.values():
            p.move_to(dt_pill_pos)
            p.set_opacity(0.0)
        self.add(dt_pill_grp)
        last_dt_state = [None]

        def sync_hb_shot11(mob: HBridgeCircuit) -> None:
            tv = min(1.999, max(0.0, gate_t.get_value()))
            s1_on, s3_on = gate_states_deadtime(tv, period=1.0, td=0.08)
            mob.set_switch_state(s1=s1_on, s3=s3_on, s2=False, s4=False)

        def sync_dt_pill(_mob: VGroup) -> None:
            tv = min(1.999, max(0.0, gate_t.get_value()))
            s1_on, s3_on = gate_states_deadtime(tv, period=1.0, td=0.08)
            st_key = "S1" if s1_on else ("S3" if s3_on else "DT")
            if st_key != last_dt_state[0]:
                for k_s, pm in dt_pills.items():
                    pm.set_opacity(1.0 if k_s == st_key else 0.0)
                last_dt_state[0] = st_key

        hb.add_updater(sync_hb_shot11)
        dt_pill_grp.add_updater(sync_dt_pill)

        def build_gate_cursor_and_sw_glow() -> VGroup:
            tv = min(1.999, max(0.0, gate_t.get_value()))
            xc = dt["ax_s1"].c2p(tv, 0)[0]
            s1_on, s3_on = gate_states_deadtime(tv, period=1.0, td=0.08)
            col = RED_POS if s1_on else (BLUE_NEG if s3_on else "#B45309")
            ln = Line([xc, y_top_g, 0], [xc, y_bot_g, 0], color=col, stroke_width=2.0, stroke_opacity=0.8)
            d1 = Dot(dt["ax_s1"].c2p(tv, 1.0 if s1_on else 0.0), radius=0.075, color=RED_POS if s1_on else INK_MUTED, stroke_color="#FFFFFF", stroke_width=1.4)
            d3 = Dot(dt["ax_s3"].c2p(tv, 1.0 if s3_on else 0.0), radius=0.075, color=BLUE_NEG if s3_on else INK_MUTED, stroke_color="#FFFFFF", stroke_width=1.4)

            # Left circuit switch highlight capsules
            c_s1 = hb.get_anchor("s1_center")
            c_s3 = hb.get_anchor("s3_center")
            glows = VGroup()
            if s1_on:
                glows.add(RoundedRectangle(width=0.52, height=0.64, corner_radius=0.12, color=RED_POS, fill_color=RED_POS, fill_opacity=0.14, stroke_width=2.4).move_to(c_s1))
            elif s3_on:
                glows.add(RoundedRectangle(width=0.52, height=0.64, corner_radius=0.12, color=BLUE_NEG, fill_color=BLUE_NEG, fill_opacity=0.14, stroke_width=2.4).move_to(c_s3))
            else:
                glows.add(RoundedRectangle(width=0.54, height=0.66, corner_radius=0.12, color=AMBER_BAND, fill_color=AMBER_BAND, fill_opacity=0.16, stroke_width=2.2).move_to(c_s1))
                glows.add(RoundedRectangle(width=0.54, height=0.66, corner_radius=0.12, color=AMBER_BAND, fill_color=AMBER_BAND, fill_opacity=0.16, stroke_width=2.2).move_to(c_s3))
            return VGroup(ln, d1, d3, glows)

        g_cursor = always_redraw(build_gate_cursor_and_sw_glow)
        self.add(g_cursor)
        self.play(gate_t.animate.set_value(2.0), run_time=8.5, rate_func=linear)

        hb.remove_updater(sync_hb_shot11)
        dt_pill_grp.remove_updater(sync_dt_pill)
        self.remove(g_cursor, dt_pill_grp)
        hb.set_switch_state(False, False, False, False)
        # Verify exact match with build_p1c_end_state()
        self.wait(1.4)
