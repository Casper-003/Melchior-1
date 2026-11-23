"""Slide builders for Slides 6 through 10."""

from __future__ import annotations

from typing import Any

from ppt_helpers import (
    AMBER,
    AMBER_LIGHT,
    CHANNEL,
    COST_COLOR,
    COST_LIGHT,
    DRIFT_HL,
    ELECTRON,
    FONT_MATH,
    FONT_UI,
    GATE_OX,
    GATE_POLY,
    HOLE,
    METAL,
    MSO_ANCHOR_MIDDLE,
    MSO_ANCHOR_TOP,
    MSO_ANIM_DIR_BOTTOM,
    MSO_ANIM_DIR_LEFT,
    MSO_ANIM_DIR_TOP,
    MSO_LINE_DASH,
    MSO_SHAPE_ISOSCELES_TRIANGLE,
    MSO_SHAPE_RIGHT_TRIANGLE,
    N_MINUS,
    N_PLUS,
    PANEL_BG,
    PANEL_BORDER,
    PP_ALIGN_CENTER,
    PP_ALIGN_LEFT,
    PP_ALIGN_RIGHT,
    P_BODY,
    P_PLUS,
    SIC_COLOR,
    SIC_LIGHT,
    SI_COLOR,
    SI_LIGHT,
    TEXT_MAIN,
    TEXT_SUB,
    TRIG_AFTER_PREV,
    TRIG_CLICK,
    TRIG_WITH_PREV,
    WHITE,
    add_box,
    add_bracket,
    add_carrier_legend,
    add_line_seg,
    add_oval,
    add_polyline,
    add_req_badge,
    add_simple_label,
    add_slide_chrome,
    add_table_row_group,
    add_textbox,
    anim_appear,
    anim_exit_fade,
    anim_fade,
    anim_motion_path,
    anim_pulse,
    anim_wipe,
    clean_shape,
    cm,
    group_shapes,
    make_run,
    rgb,
)


def build_slide_6(sld: Any) -> None:
    """Slide 6: Silicon IGBT conductivity modulation & three costs — 4 clicks."""
    add_slide_chrome(sld, 6, "硅 IGBT：电导调制降低导通压降，也带来三项代价", "硅 IGBT")

    # Left Panel background frame (x=1.5..19.5, y=3.6..14.6)
    add_box(sld, "p6_left_frame", 1.45, 3.55, 18.1, 10.9, fill=WHITE, line=PANEL_BORDER, line_pt=0.75)

    # 1. N- Drift region
    add_box(sld, "p6_drift_1", 1.5, 5.5, 18.0, 7.1, fill=N_MINUS, line=WHITE, line_pt=1.0)

    # 2. Drift highlight (initially hidden, layered above drift_1, below P-body & carriers)
    drift_hl = add_box(sld, "p6_drift_hl", 1.5, 5.5, 18.0, 7.1, fill=DRIFT_HL, line=None, transp=0.65)

    # 3. P-body (Left & Right)
    add_box(sld, "p6_pbody_L", 1.5, 5.5, 6.0, 2.5, fill=P_BODY, line=WHITE, line_pt=1.0)
    add_box(sld, "p6_pbody_R", 13.5, 5.5, 6.0, 2.5, fill=P_BODY, line=WHITE, line_pt=1.0)
    add_simple_label(sld, "p6_pbody_lbl_L", 1.7, 7.25, 2.4, 0.60, "P 体区", size=14, color=TEXT_MAIN)
    add_simple_label(sld, "p6_pbody_lbl_R", 16.9, 7.25, 2.4, 0.60, "P 体区", size=14, color=TEXT_MAIN, align=PP_ALIGN_RIGHT)

    # 4. N+ source (Left & Right)
    add_box(sld, "p6_nsrc_L", 2.5, 5.5, 3.0, 1.0, fill=N_PLUS, line=WHITE, line_pt=1.0)
    add_box(sld, "p6_nsrc_R", 15.5, 5.5, 3.0, 1.0, fill=N_PLUS, line=WHITE, line_pt=1.0)
    add_textbox(
        sld,
        "p6_nsrc_lbl_L",
        2.55,
        5.55,
        2.9,
        0.9,
        [{"runs": [make_run("N", size=14, color=TEXT_MAIN, bold=True), make_run("+", size=14, color=TEXT_MAIN, bold=True, sup=True)], "align": PP_ALIGN_CENTER}],
    )
    add_textbox(
        sld,
        "p6_nsrc_lbl_R",
        15.55,
        5.55,
        2.9,
        0.9,
        [{"runs": [make_run("N", size=14, color=TEXT_MAIN, bold=True), make_run("+", size=14, color=TEXT_MAIN, bold=True, sup=True)], "align": PP_ALIGN_CENTER}],
    )

    # 5. Channels (initially hidden, 60% opacity -> transp=0.40)
    ch_L = add_box(sld, "p6_channel_L", 5.5, 5.5, 2.0, 0.30, fill=CHANNEL, line=None, transp=0.40)
    ch_R = add_box(sld, "p6_channel_R", 13.5, 5.5, 2.0, 0.30, fill=CHANNEL, line=None, transp=0.40)

    # 6. Gate oxide & Gate polysilicon
    add_box(sld, "p6_oxide_1", 4.5, 5.1, 12.0, 0.4, fill=GATE_OX, line=WHITE, line_pt=1.0)
    add_simple_label(
        sld, "p6_gate_1", 6.5, 4.5, 8.0, 0.6, "栅极 G", size=14, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=GATE_POLY, line=WHITE, line_pt=1.0, line_spacing=1.0
    )

    # 7. Emitter contacts & Emitter E bar
    add_box(sld, "p6_econt_L", 2.5, 4.2, 2.0, 1.3, fill=METAL, line=WHITE, line_pt=1.0)
    add_box(sld, "p6_econt_R", 16.5, 4.2, 2.0, 1.3, fill=METAL, line=WHITE, line_pt=1.0)
    add_box(sld, "p6_emitter_1", 1.5, 3.6, 18.0, 0.6, fill=METAL, line=WHITE, line_pt=1.0)
    add_simple_label(sld, "p6_emitter_lbl", 1.8, 3.56, 4.5, 0.68, "发射极 E", size=14, color=WHITE, bold=True, align=PP_ALIGN_LEFT, line_spacing=1.0)

    # 8. P+ collector & Collector C
    add_box(sld, "p6_pcol_1", 1.5, 12.6, 18.0, 1.2, fill=P_PLUS, line=WHITE, line_pt=1.0)
    add_textbox(
        sld,
        "p6_pcol_lbl",
        1.7,
        12.6,
        4.0,
        1.2,
        [{"runs": [make_run("P", size=14, color=TEXT_MAIN, bold=True), make_run("+", size=14, color=TEXT_MAIN, bold=True, sup=True), make_run(" 集电区", size=14, color=TEXT_MAIN, bold=True)]}],
    )
    add_simple_label(
        sld, "p6_collector_1", 1.5, 13.8, 18.0, 0.6, "集电极 C", size=14, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=METAL, line=WHITE, line_pt=1.0, line_spacing=1.0
    )

    # N- drift region label
    add_textbox(
        sld,
        "p6_drift_lbl",
        1.7,
        11.65,
        4.2,
        0.75,
        [{"runs": [make_run("N", size=14, color=TEXT_MAIN, bold=True), make_run("−", size=14, color=TEXT_MAIN, bold=True, sup=True), make_run(" 漂移区", size=14, color=TEXT_MAIN, bold=True)]}],
    )

    # Gate voltage labels (initially hidden, centered above gate at x=8.7, y=3.75)
    gate_on = add_simple_label(
        sld,
        "p6_gate_on",
        8.7,
        3.75,
        3.6,
        0.65,
        "栅极 +15 V",
        size=14,
        color=TEXT_MAIN,
        bold=True,
        align=PP_ALIGN_CENTER,
        fill=AMBER,
        line=WHITE,
        line_pt=1.0,
        round_cm=0.18,
    )
    gate_off = add_simple_label(
        sld,
        "p6_gate_off",
        8.7,
        3.75,
        3.6,
        0.65,
        "栅极 0 V",
        size=14,
        color=WHITE,
        bold=True,
        align=PP_ALIGN_CENTER,
        fill=METAL,
        line=WHITE,
        line_pt=1.0,
        round_cm=0.18,
    )

    # Modulation badge (initially hidden)
    mod_badge = add_textbox(
        sld,
        "p6_mod_badge",
        6.7,
        9.45,
        7.6,
        0.95,
        [
            {
                "runs": [
                    make_run("n ≈ p ≫ N", size=16, color=TEXT_MAIN, bold=True, font=FONT_MATH),
                    make_run("D", size=16, color=TEXT_MAIN, bold=True, font=FONT_MATH, sub=True),
                    make_run("　电导调制", size=16, color=TEXT_MAIN, bold=True),
                ],
                "align": PP_ALIGN_CENTER,
            }
        ],
        fill=WHITE,
        line=DRIFT_HL,
        line_pt=1.25,
        round_cm=0.18,
    )

    # 12 static plasma pairs (4 top y < 8.5 grouped as p6_plasma_top; 8 deep y >= 8.5)
    top_coords = [(4.2, 8.2), (8.2, 7.3), (12.6, 7.6), (16.8, 8.2)]
    top_shapes = []
    for idx, (px, py) in enumerate(top_coords, start=1):
        top_shapes.append(add_oval(sld, f"p6_ptop_e{idx}", px, py, 0.28, fill=ELECTRON, line=None))
        top_shapes.append(add_oval(sld, f"p6_ptop_h{idx}", px + 0.36, py + 0.14, 0.28, fill=WHITE, line=HOLE, line_pt=1.5))
    plasma_top = group_shapes(sld, top_shapes, "p6_plasma_top")

    deep_coords = [
        (3.4, 9.6),
        (5.4, 10.9),
        (7.5, 11.7),
        (10.3, 11.4),
        (13.4, 11.8),
        (15.6, 10.6),
        (17.5, 9.5),
        (17.6, 11.6),
    ]
    plasma_deeps = []
    for idx, (px, py) in enumerate(deep_coords, start=1):
        pe = add_oval(sld, f"p6_pdeep_{idx}_e", px, py, 0.28, fill=ELECTRON, line=None)
        ph = add_oval(sld, f"p6_pdeep_{idx}_h", px + 0.36, py + 0.14, 0.28, fill=WHITE, line=HOLE, line_pt=1.5)
        plasma_deeps.append(group_shapes(sld, [pe, ph], f"p6_plasma_deep_{idx}"))

    # Moving carriers (4 points per path, delay step 0.3 s, duration 2.2 s, repeat 2)
    e_path_L = [(4.0, 6.0), (6.5, 5.75), (8.3, 6.8), (8.3, 12.4)]
    e_path_R = [(17.0, 6.0), (14.5, 5.75), (12.7, 6.8), (12.7, 12.4)]
    h_paths = [
        ("L1", [(5.5, 13.2), (5.5, 8.2), (4.0, 6.8)]),
        ("L2", [(9.6, 13.2), (9.6, 9.0), (7.0, 6.9)]),
        ("R1", [(15.5, 13.2), (15.5, 8.2), (17.0, 6.8)]),
        ("R2", [(11.4, 13.2), (11.4, 9.0), (14.0, 6.9)]),
    ]
    carrier_specs: list[tuple[Any, list[tuple[float, float]], float]] = []
    for side, pts in (("L", e_path_L), ("R", e_path_R)):
        for k in range(4):
            dot = add_oval(sld, f"p6_electron_{side}{k + 1}", pts[0][0], pts[0][1], 0.28, fill=ELECTRON, line=None)
            carrier_specs.append((dot, pts, k * 0.3))
    for tag, pts in h_paths:
        for k in range(4):
            ring = add_oval(sld, f"p6_hole_{tag}_{k + 1}", pts[0][0], pts[0][1], 0.28, fill=WHITE, line=HOLE, line_pt=1.5)
            carrier_specs.append((ring, pts, k * 0.3))

    # Carrier legend below cross-section
    add_carrier_legend(sld, 6, x=1.5, y=14.85)

    # ---------------- Right Panel (x=20.5..32.4) ----------------
    # Chart A: Output I-V (y=3.6..9.1)
    add_box(sld, "p6_chartA_bg", 20.5, 3.6, 11.9, 5.5, fill=WHITE, line=PANEL_BORDER, line_pt=0.75, round_cm=0.18)
    add_simple_label(sld, "p6_chartA_t", 20.8, 3.72, 6.5, 0.55, "输出特性 I–V", size=14, color=TEXT_MAIN, bold=True)
    # Axes
    axA_x0, axA_y0, axA_w, axA_h = 21.6, 8.55, 9.8, 3.95
    add_line_seg(sld, "p6_chartA_y", axA_x0, axA_y0, axA_x0, axA_y0 - axA_h, color=TEXT_MAIN, weight_pt=1.25, arrow_end=True)
    add_line_seg(sld, "p6_chartA_x", axA_x0, axA_y0, axA_x0 + axA_w, axA_y0, color=TEXT_MAIN, weight_pt=1.25, arrow_end=True)
    add_simple_label(sld, "p6_chartA_ylbl", axA_x0 - 0.55, axA_y0 - axA_h, 0.5, 0.55, "I", size=14, color=TEXT_MAIN, italic=True, font=FONT_MATH, align=PP_ALIGN_RIGHT)
    add_textbox(
        sld,
        "p6_chartA_xlbl",
        axA_x0 + axA_w - 1.2,
        axA_y0 + 0.02,
        1.5,
        0.52,
        [{"runs": [make_run("V", size=14, color=TEXT_MAIN, italic=True, font=FONT_MATH), make_run("CE", size=14, color=TEXT_MAIN, font=FONT_MATH, sub=True)], "align": PP_ALIGN_RIGHT}],
    )
    # Curves (initially hidden)
    igbt_pts = [(axA_x0, axA_y0), (axA_x0 + 2.1, axA_y0), (axA_x0 + 2.6, axA_y0 - 0.55), (axA_x0 + 3.4, axA_y0 - 1.9), (axA_x0 + 4.3, axA_y0 - 3.65)]
    iv_igbt = add_polyline(sld, "p6_iv_igbt", igbt_pts, color=SI_COLOR, weight_pt=2.5)
    mos_pts = [(axA_x0, axA_y0), (axA_x0 + 4.5, axA_y0 - 1.15), (axA_x0 + 9.0, axA_y0 - 2.30)]
    iv_mos = add_polyline(sld, "p6_iv_mos", mos_pts, color=METAL, weight_pt=2.0, dash=MSO_LINE_DASH)
    iv_igbt_lbl = add_simple_label(sld, "p6_iv_igbt_lbl", axA_x0 + 4.45, axA_y0 - 3.65, 3.2, 0.55, "硅 IGBT", size=14, color=SI_COLOR, bold=True)
    iv_mos_lbl = add_simple_label(sld, "p6_iv_mos_lbl", axA_x0 + 6.4, axA_y0 - 2.95, 3.4, 0.55, "硅 MOSFET", size=14, color=TEXT_SUB)
    iv_vce_lbl = add_simple_label(
        sld,
        "p6_iv_vce_lbl",
        axA_x0 + 1.4,
        axA_y0 - 1.35,
        3.9,
        0.60,
        "≈ 0.7 V 结压降",
        size=14,
        color=COST_COLOR,
        bold=True,
        fill=COST_LIGHT,
        line=COST_COLOR,
        line_pt=0.75,
        round_cm=0.14,
        align=PP_ALIGN_CENTER,
    )

    # Chart B: Turn-off & Turn-on Waveforms (y=9.6..15.2)
    add_box(sld, "p6_chartB_bg", 20.5, 9.6, 11.9, 5.6, fill=WHITE, line=PANEL_BORDER, line_pt=0.75, round_cm=0.18)
    add_simple_label(sld, "p6_chartB_t", 20.8, 9.72, 6.8, 0.55, "关断与开通波形", size=14, color=TEXT_MAIN, bold=True)
    axB_x0, axB_y0, axB_w, axB_h = 21.3, 14.55, 10.6, 3.9
    add_line_seg(sld, "p6_chartB_y", axB_x0, axB_y0, axB_x0, axB_y0 - axB_h, color=TEXT_MAIN, weight_pt=1.25, arrow_end=True)
    add_line_seg(sld, "p6_chartB_x", axB_x0, axB_y0, axB_x0 + axB_w, axB_y0, color=TEXT_MAIN, weight_pt=1.25, arrow_end=True)
    add_line_seg(sld, "p6_chartB_div", axB_x0 + 5.5, axB_y0, axB_x0 + 5.5, axB_y0 - axB_h + 0.2, color=PANEL_BORDER, weight_pt=1.0, dash=MSO_LINE_DASH)
    add_simple_label(sld, "p6_chartB_subL", axB_x0 + 0.15, axB_y0 - 3.92, 2.6, 0.60, "关断阶段", size=14, color=TEXT_SUB, bold=True)
    add_simple_label(sld, "p6_chartB_subR", axB_x0 + 5.85, axB_y0 - 3.92, 2.6, 0.60, "开通阶段", size=14, color=TEXT_SUB, bold=True)

    # Left half: Turn-off V_CE + I_C fast drop + tail
    vce_pts = [(axB_x0 + 0.2, axB_y0 - 0.15), (axB_x0 + 1.0, axB_y0 - 0.15), (axB_x0 + 1.8, axB_y0 - 2.95), (axB_x0 + 5.0, axB_y0 - 2.95)]
    wf_vce_off = add_polyline(sld, "p6_wf_vce_off", vce_pts, color=COST_COLOR, weight_pt=2.25)
    wf_vce_lbl = add_textbox(
        sld,
        "p6_wf_vce_lbl",
        axB_x0 + 3.0,
        axB_y0 - 3.65,
        1.8,
        0.58,
        [{"runs": [make_run("V", size=14, color=COST_COLOR, bold=True, italic=True, font=FONT_MATH), make_run("CE", size=14, color=COST_COLOR, bold=True, font=FONT_MATH, sub=True)]}],
    )
    ic_fast_pts = [(axB_x0 + 0.2, axB_y0 - 2.65), (axB_x0 + 1.1, axB_y0 - 2.65), (axB_x0 + 1.85, axB_y0 - 0.95)]
    wf_ic_fast = add_polyline(sld, "p6_wf_ic_fast", ic_fast_pts, color=SI_COLOR, weight_pt=2.5)
    ic_tail_pts = [(axB_x0 + 1.85, axB_y0 - 0.95), (axB_x0 + 2.4, axB_y0 - 0.58), (axB_x0 + 3.2, axB_y0 - 0.30), (axB_x0 + 4.3, axB_y0 - 0.12), (axB_x0 + 5.0, axB_y0)]
    tail_poly_pts = ic_tail_pts + [(axB_x0 + 1.85, axB_y0)]
    wf_tail_fill = add_polyline(sld, "p6_wf_tail_fill", tail_poly_pts, color=None, fill_color=COST_LIGHT, fill_transp=0.1, closed=True)
    wf_ic_tail = add_polyline(sld, "p6_wf_ic_tail", ic_tail_pts, color=SI_COLOR, weight_pt=2.5)
    wf_tail_lbl = add_simple_label(sld, "p6_wf_tail_lbl", axB_x0 + 2.25, axB_y0 - 1.38, 2.8, 0.60, "拖尾电流", size=14, color=COST_COLOR, bold=True)

    # Right half: Turn-on I_C + I_rr spike
    ic_on_pts = [
        (axB_x0 + 5.9, axB_y0),
        (axB_x0 + 6.5, axB_y0),
        (axB_x0 + 7.1, axB_y0 - 2.65),
        (axB_x0 + 7.65, axB_y0 - 3.65),
        (axB_x0 + 8.3, axB_y0 - 2.55),
        (axB_x0 + 10.0, axB_y0 - 2.55),
    ]
    wf_ic_on = add_polyline(sld, "p6_wf_ic_on", ic_on_pts, color=SI_COLOR, weight_pt=2.5)
    wf_irr_lbl = add_textbox(
        sld,
        "p6_wf_irr_lbl",
        axB_x0 + 6.2,
        axB_y0 - 2.28,
        4.4,
        1.30,
        [
            {
                "runs": [
                    make_run("I", size=14, color=COST_COLOR, bold=True, italic=True, font=FONT_MATH),
                    make_run("rr", size=14, color=COST_COLOR, bold=True, font=FONT_MATH, sub=True),
                    make_run(" 尖峰\n（FRD 反向恢复）", size=14, color=COST_COLOR, bold=True),
                ],
                "align": PP_ALIGN_CENTER,
            }
        ],
        fill=COST_LIGHT,
        line=COST_COLOR,
        line_pt=0.75,
        round_cm=0.14,
    )

    # ---------------- Bottom 3 Cost Tags (y=15.80..18.00) ----------------
    cost_specs = [
        (
            2,
            1.5,
            [
                make_run("0.7 V 结压降：\n", size=18, color=COST_COLOR, bold=True),
                make_run("轻载导通损耗偏高", size=18, color=TEXT_MAIN),
            ],
        ),
        (
            3,
            12.0,
            [
                make_run("拖尾电流：\n", size=18, color=COST_COLOR, bold=True),
                make_run("E", size=18, color=TEXT_MAIN, italic=True, font=FONT_MATH),
                make_run("off", size=18, color=TEXT_MAIN, font=FONT_MATH, sub=True),
                make_run(" 升高，频率约 10 kHz", size=18, color=TEXT_MAIN),
            ],
        ),
        (
            4,
            22.5,
            [
                make_run("需并联 FRD：\n", size=18, color=COST_COLOR, bold=True),
                make_run("Q", size=18, color=TEXT_MAIN, italic=True, font=FONT_MATH),
                make_run("rr", size=18, color=TEXT_MAIN, font=FONT_MATH, sub=True),
                make_run(" 使 ", size=18, color=TEXT_MAIN),
                make_run("E", size=18, color=TEXT_MAIN, italic=True, font=FONT_MATH),
                make_run("on", size=18, color=TEXT_MAIN, font=FONT_MATH, sub=True),
                make_run(" 升高", size=18, color=TEXT_MAIN),
            ],
        ),
    ]
    cost_cards = []
    for num, cx, runs in cost_specs:
        bg = add_box(sld, f"p6_cost_{num}_bg", cx, 15.80, 9.9, 2.20, fill=COST_LIGHT, line=COST_COLOR, line_pt=1.25, round_cm=0.2)
        badge = add_req_badge(sld, f"p6_cost_{num}_badge", num, cx + 0.35, 16.50)
        txt = add_textbox(sld, f"p6_cost_{num}_txt", cx + 1.35, 15.90, 8.35, 2.00, [{"runs": runs}], valign=MSO_ANCHOR_MIDDLE)
        cost_cards.append(group_shapes(sld, [bg, badge, txt], f"p6_cost_{num}"))

    # ---------------- Animations: Exact 4 Clicks ----------------
    # Click 1: Turn-on + conductivity modulation
    anim_fade(sld, gate_on, trigger=TRIG_CLICK, duration=0.4)
    anim_fade(sld, ch_L, trigger=TRIG_WITH_PREV, duration=0.4)
    anim_fade(sld, ch_R, trigger=TRIG_WITH_PREV, duration=0.4)
    for shp, pts, dly in carrier_specs:
        anim_appear(sld, shp, trigger=TRIG_WITH_PREV, delay=dly)
        anim_motion_path(sld, shp, pts, trigger=TRIG_WITH_PREV, duration=2.2, delay=dly, repeat=2)
        anim_exit_fade(sld, shp, trigger=TRIG_WITH_PREV, duration=0.25, delay=dly + 4.15)
    # After first wave (~2.2 s), drift highlight + badge + plasma dots fade in
    anim_fade(sld, drift_hl, trigger=TRIG_WITH_PREV, duration=0.4, delay=2.2)
    anim_fade(sld, mod_badge, trigger=TRIG_WITH_PREV, duration=0.4, delay=2.2)
    anim_fade(sld, plasma_top, trigger=TRIG_WITH_PREV, duration=0.4, delay=2.2)
    for pd in plasma_deeps:
        anim_fade(sld, pd, trigger=TRIG_WITH_PREV, duration=0.4, delay=2.2)

    # Click 2: Output I-V curves + 0.7 V pulse + Cost tag 2
    anim_wipe(sld, iv_igbt, direction=MSO_ANIM_DIR_LEFT, trigger=TRIG_CLICK, duration=0.6)
    anim_fade(sld, iv_igbt_lbl, trigger=TRIG_WITH_PREV, duration=0.3)
    anim_wipe(sld, iv_mos, direction=MSO_ANIM_DIR_LEFT, trigger=TRIG_AFTER_PREV, duration=0.5)
    anim_fade(sld, iv_mos_lbl, trigger=TRIG_WITH_PREV, duration=0.3)
    anim_fade(sld, iv_vce_lbl, trigger=TRIG_AFTER_PREV, duration=0.35)
    anim_pulse(sld, iv_vce_lbl, trigger=TRIG_AFTER_PREV, duration=0.5)
    anim_fade(sld, cost_cards[0], trigger=TRIG_WITH_PREV, duration=0.4)

    # Click 3: Turn-off tail current synced with slow deep plasma recombination + Cost tag 3
    anim_exit_fade(sld, gate_on, trigger=TRIG_CLICK, duration=0.3)
    anim_fade(sld, gate_off, trigger=TRIG_WITH_PREV, duration=0.3)
    anim_exit_fade(sld, ch_L, trigger=TRIG_WITH_PREV, duration=0.3)
    anim_exit_fade(sld, ch_R, trigger=TRIG_WITH_PREV, duration=0.3)
    anim_exit_fade(sld, plasma_top, trigger=TRIG_WITH_PREV, duration=0.3, delay=0.0)
    # 8 deep plasma pairs fade out evenly from 0.6 s to 2.4 s
    for idx, pd in enumerate(plasma_deeps):
        dly = 0.6 + (1.8 / 7.0) * idx
        anim_exit_fade(sld, pd, trigger=TRIG_WITH_PREV, duration=0.35, delay=dly)
    anim_exit_fade(sld, drift_hl, trigger=TRIG_WITH_PREV, duration=0.5, delay=1.8)
    anim_exit_fade(sld, mod_badge, trigger=TRIG_WITH_PREV, duration=0.4, delay=1.8)

    anim_wipe(sld, wf_vce_off, direction=MSO_ANIM_DIR_LEFT, trigger=TRIG_WITH_PREV, duration=0.8, delay=0.0)
    anim_fade(sld, wf_vce_lbl, trigger=TRIG_WITH_PREV, duration=0.3, delay=0.4)
    anim_wipe(sld, wf_ic_fast, direction=MSO_ANIM_DIR_LEFT, trigger=TRIG_WITH_PREV, duration=0.5, delay=0.1)
    anim_wipe(sld, wf_ic_tail, direction=MSO_ANIM_DIR_LEFT, trigger=TRIG_WITH_PREV, duration=2.0, delay=0.5)
    anim_fade(sld, wf_tail_fill, trigger=TRIG_WITH_PREV, duration=1.5, delay=0.7)
    anim_fade(sld, wf_tail_lbl, trigger=TRIG_WITH_PREV, duration=0.4, delay=1.2)
    anim_fade(sld, cost_cards[1], trigger=TRIG_WITH_PREV, duration=0.4, delay=2.4)

    # Click 4: Turn-on I_rr spike + Cost tag 4
    anim_wipe(sld, wf_ic_on, direction=MSO_ANIM_DIR_LEFT, trigger=TRIG_CLICK, duration=0.65)
    anim_fade(sld, wf_irr_lbl, trigger=TRIG_AFTER_PREV, duration=0.35)
    anim_pulse(sld, wf_irr_lbl, trigger=TRIG_AFTER_PREV, duration=0.5)
    anim_fade(sld, cost_cards[2], trigger=TRIG_WITH_PREV, duration=0.4)


def build_slide_7(sld: Any) -> None:
    """Slide 7: 4H-SiC material advantage & equal-area E-field triangle comparison — 4 clicks."""
    add_slide_chrome(sld, 7, "4H-SiC：击穿场强高约 10 倍，漂移区薄到约 1/10", "SiC", rule_y=2.92)

    # Top capsule (x=1.5, y=3.08, h=0.82)
    add_simple_label(
        sld,
        "p7_cap_1",
        1.5,
        3.08,
        9.4,
        0.80,
        "800 V 平台 → 1200 V 器件",
        size=18,
        color=TEXT_MAIN,
        bold=True,
        align=PP_ALIGN_CENTER,
        fill=PANEL_BG,
        line=PANEL_BORDER,
        line_pt=0.75,
        round_cm=0.40,
    )

    # Parameter Table (x=1.5..32.4, y=4.02..8.12, 5 rows x 4 cols, row h=0.82)
    col_w = [11.5, 6.8, 7.6, 5.0]
    add_table_row_group(
        sld,
        "p7_tbl_hdr",
        1.5,
        4.02,
        col_w,
        0.82,
        [
            [make_run("关键材料 / 器件参数", size=16, color=TEXT_MAIN, bold=True)],
            [make_run("硅 (Si)", size=16, color=SI_COLOR, bold=True)],
            [make_run("4H-SiC", size=16, color=SIC_COLOR, bold=True)],
            [make_run("倍数对比", size=16, color=SIC_COLOR, bold=True)],
        ],
        default_fill=PANEL_BG,
        aligns=[PP_ALIGN_LEFT, PP_ALIGN_CENTER, PP_ALIGN_CENTER, PP_ALIGN_CENTER],
    )
    rows_data = [
        ("禁带宽度", "1.12 eV", "3.26 eV", "≈ 3×"),
        ("临界击穿场强", "0.3 MV/cm", "≈ 3 MV/cm", "≈ 10×"),
        ("1200 V 所需漂移区厚度（理想估算）", "≈ 80 μm", "≈ 8 μm", "≈ 1/10"),
        ("漂移区掺杂浓度", "1×", "≈ 100×", "≈ 100×"),
    ]
    tbl_rows = []
    for idx, (c0, c1, c2, c3) in enumerate(rows_data, start=1):
        row = add_table_row_group(
            sld,
            f"p7_tbl_row_{idx}",
            1.5,
            4.02 + idx * 0.82,
            col_w,
            0.82,
            [
                [make_run(c0, size=16, color=TEXT_MAIN, bold=True)],
                [make_run(c1, size=16, color=SI_COLOR)],
                [make_run(c2, size=16, color=SIC_COLOR, bold=True)],
                [make_run(c3, size=16, color=SIC_COLOR, bold=True)],
            ],
            default_fill=WHITE,
            aligns=[PP_ALIGN_LEFT, PP_ALIGN_CENTER, PP_ALIGN_CENTER, PP_ALIGN_CENTER],
        )
        tbl_rows.append(row)

    # Lower two panels (y=8.40..17.85): Left Silicon x=1.5..16.2, Right 4H-SiC x=17.7..32.4
    add_box(sld, "p7_si_panel", 1.5, 8.40, 14.7, 9.45, fill=WHITE, line=PANEL_BORDER, line_pt=0.75, round_cm=0.2)
    add_simple_label(sld, "p7_si_hdr", 1.85, 8.48, 8.0, 0.65, "硅（IGBT）", size=16, color=SI_COLOR, bold=True)

    add_box(sld, "p7_sic_panel", 17.7, 8.40, 14.7, 9.45, fill=WHITE, line=PANEL_BORDER, line_pt=0.75, round_cm=0.2)
    add_simple_label(sld, "p7_sic_hdr", 18.05, 8.48, 8.0, 0.65, "4H-SiC MOSFET", size=16, color=SIC_COLOR, bold=True)

    # Scale label in top-right of right panel
    add_simple_label(
        sld,
        "p7_scale_note",
        24.2,
        8.48,
        7.9,
        0.90,
        "同比例尺：横 1 cm = 10 μm\n纵 1 cm = 0.6 MV/cm",
        size=14,
        color=TEXT_SUB,
        align=PP_ALIGN_RIGHT,
        valign=MSO_ANCHOR_TOP,
    )

    # Baseline y = 14.25 cm (5.0 cm tall SiC triangle reaches y = 9.25, cleanly below header at 8.48..9.13!)
    base_y = 14.25

    # --- Silicon Panel (Click 2) ---
    si_x0 = 3.1
    si_axes = group_shapes(
        sld,
        [
            add_line_seg(sld, "p7_si_ay", si_x0, base_y, si_x0, 9.25, color=TEXT_MAIN, weight_pt=1.5, arrow_end=True),
            add_line_seg(sld, "p7_si_ax", 2.0, base_y, 14.6, base_y, color=TEXT_MAIN, weight_pt=1.5, arrow_end=True),
            add_simple_label(sld, "p7_si_ey_lbl", si_x0 + 0.18, 9.05, 2.5, 0.62, "电场 E", size=14, color=TEXT_MAIN, bold=True, align=PP_ALIGN_LEFT, word_wrap=False),
            add_simple_label(sld, "p7_si_dx_lbl", 13.7, base_y - 0.65, 1.6, 0.60, "深度", size=14, color=TEXT_MAIN, align=PP_ALIGN_CENTER),
        ],
        "p7_si_axes",
    )
    # Triangle: x 3.0..11.0 (8.0 cm = 80 um), h = 0.5 cm (0.3 MV/cm)
    si_tri = add_polyline(
        sld,
        "p7_si_tri",
        [(si_x0, base_y), (si_x0, base_y - 0.50), (si_x0 + 8.0, base_y)],
        color=SI_COLOR,
        weight_pt=1.75,
        fill_color=SI_COLOR,
        fill_transp=0.65,
        closed=True,
    )
    si_epeak = add_textbox(
        sld,
        "p7_si_epeak",
        5.5,
        12.70,
        5.5,
        0.65,
        [
            {
                "runs": [
                    make_run("E", size=14, color=SI_COLOR, bold=True, italic=True, font=FONT_MATH),
                    make_run("peak", size=14, color=SI_COLOR, bold=True, font=FONT_MATH, sub=True),
                    make_run(" ≈ 0.3 MV/cm", size=14, color=SI_COLOR, bold=True),
                ]
            }
        ],
    )
    si_w_br = add_bracket(sld, "p7_si_w_br", si_x0, si_x0 + 8.0, base_y + 0.16, h_tick=0.12, up=True, color=SI_COLOR, weight_pt=1.25)
    si_w_lbl = add_simple_label(sld, "p7_si_w_lbl", si_x0, base_y + 0.18, 8.0, 0.58, "W ≈ 80 μm", size=14, color=SI_COLOR, bold=True, align=PP_ALIGN_CENTER)

    # Silicon unfolded cross-section strip (y=15.38..16.22)
    si_pbody = add_simple_label(sld, "p7_si_pbody", 1.9, 15.38, 1.2, 0.84, "P", size=14, color=TEXT_MAIN, bold=True, align=PP_ALIGN_CENTER, fill=P_BODY, line=WHITE, line_pt=1.0)
    si_drift = add_textbox(
        sld,
        "p7_si_drift",
        3.1,
        15.38,
        8.0,
        0.84,
        [{"runs": [make_run("N", size=14, color=TEXT_MAIN, bold=True), make_run("−", size=14, color=TEXT_MAIN, bold=True, sup=True), make_run(" 漂移区 (80 μm)", size=14, color=TEXT_MAIN, bold=True)], "align": PP_ALIGN_CENTER}],
        fill=N_MINUS,
        line=WHITE,
        line_pt=1.0,
    )
    si_pplus = add_textbox(
        sld,
        "p7_si_pplus",
        11.1,
        15.38,
        1.4,
        0.84,
        [{"runs": [make_run("P", size=14, color=TEXT_MAIN, bold=True), make_run("+", size=14, color=TEXT_MAIN, bold=True, sup=True)], "align": PP_ALIGN_CENTER}],
        fill=P_PLUS,
        line=WHITE,
        line_pt=1.0,
    )
    si_e_arr = add_line_seg(sld, "p7_si_e_arr", 3.4, 15.14, 8.6, 15.14, color=ELECTRON, weight_pt=2.0, arrow_end=True)
    si_h_arr = add_line_seg(sld, "p7_si_h_arr", 10.7, 16.46, 4.4, 16.46, color=HOLE, weight_pt=2.0, arrow_end=True)
    si_strip = group_shapes(sld, [si_pbody, si_drift], "p7_si_strip_base")
    si_bot_lbl = add_simple_label(sld, "p7_si_bot_lbl", 1.8, 16.82, 13.8, 0.72, "空穴注入 → 少子拖尾", size=16, color=COST_COLOR, bold=True, align=PP_ALIGN_CENTER)

    # --- 4H-SiC Panel (Click 3) ---
    sic_x0 = 19.6
    sic_axes = group_shapes(
        sld,
        [
            add_line_seg(sld, "p7_sic_ay", sic_x0, base_y, sic_x0, 9.15, color=TEXT_MAIN, weight_pt=1.5, arrow_end=True),
            add_line_seg(sld, "p7_sic_ax", 18.4, base_y, 31.0, base_y, color=TEXT_MAIN, weight_pt=1.5, arrow_end=True),
            add_simple_label(sld, "p7_sic_ey_lbl", sic_x0 + 0.18, 9.02, 2.5, 0.62, "电场 E", size=14, color=TEXT_MAIN, bold=True, align=PP_ALIGN_LEFT, word_wrap=False),
            add_simple_label(sld, "p7_sic_dx_lbl", 30.1, base_y - 0.65, 1.6, 0.60, "深度", size=14, color=TEXT_MAIN, align=PP_ALIGN_CENTER),
        ],
        "p7_sic_axes",
    )
    # Triangle: x 19.6..20.4 (0.8 cm = 8 um), h = 5.0 cm (3 MV/cm -> apex y = 9.25)
    sic_tri = add_polyline(
        sld,
        "p7_sic_tri",
        [(sic_x0, base_y), (sic_x0, base_y - 5.00), (sic_x0 + 0.80, base_y)],
        color=SIC_COLOR,
        weight_pt=1.75,
        fill_color=SIC_COLOR,
        fill_transp=0.65,
        closed=True,
    )
    sic_epeak = add_textbox(
        sld,
        "p7_sic_epeak",
        20.6,
        9.72,
        5.8,
        0.65,
        [
            {
                "runs": [
                    make_run("E", size=14, color=SIC_COLOR, bold=True, italic=True, font=FONT_MATH),
                    make_run("peak", size=14, color=SIC_COLOR, bold=True, font=FONT_MATH, sub=True),
                    make_run(" ≈ 3 MV/cm (10×)", size=14, color=SIC_COLOR, bold=True),
                ]
            }
        ],
    )
    sic_w_br = add_bracket(sld, "p7_sic_w_br", sic_x0, sic_x0 + 0.80, base_y + 0.16, h_tick=0.12, up=True, color=SIC_COLOR, weight_pt=1.25)
    sic_w_lbl = add_simple_label(sld, "p7_sic_w_lbl", sic_x0 + 0.90, base_y + 0.16, 4.2, 0.58, "W ≈ 8 μm (1/10)", size=14, color=SIC_COLOR, bold=True)

    # SiC unfolded strip (y=15.38..16.22): P body + narrow N- + N+ substrate (NO P+!)
    sic_pbody = add_simple_label(sld, "p7_sic_pbody", 18.4, 15.38, 1.2, 0.84, "P", size=14, color=TEXT_MAIN, bold=True, align=PP_ALIGN_CENTER, fill=P_BODY, line=WHITE, line_pt=1.0)
    sic_drift = add_box(sld, "p7_sic_drift", 19.6, 15.38, 0.8, 0.84, fill=N_MINUS, line=WHITE, line_pt=1.0)
    sic_sub = add_textbox(
        sld,
        "p7_sic_sub",
        20.4,
        15.38,
        2.3,
        0.84,
        [{"runs": [make_run("N", size=14, color=TEXT_MAIN, bold=True), make_run("+", size=14, color=TEXT_MAIN, bold=True, sup=True), make_run(" 衬底", size=14, color=TEXT_MAIN, bold=True)], "align": PP_ALIGN_CENTER}],
        fill=N_PLUS,
        line=WHITE,
        line_pt=1.0,
    )
    sic_e_arr = add_line_seg(sld, "p7_sic_e_arr", 19.6, 15.14, 22.6, 15.14, color=ELECTRON, weight_pt=2.0, arrow_end=True)
    sic_strip = group_shapes(sld, [sic_pbody, sic_drift, sic_sub, sic_e_arr], "p7_sic_strip")
    sic_bot_lbl = add_simple_label(sld, "p7_sic_bot_lbl", 18.1, 16.82, 13.8, 0.72, "仅电子导电 → 无拖尾", size=16, color=SIC_COLOR, bold=True, align=PP_ALIGN_CENTER)

    # Center annotation between panels (floating cleanly in open area left of SiC axis)
    area_note = add_simple_label(
        sld,
        "p7_area_note",
        11.2,
        10.70,
        5.8,
        1.48,
        "三角形面积相等\n= 同为 1200 V 耐压",
        size=14,
        color=TEXT_SUB,
        bold=True,
        align=PP_ALIGN_CENTER,
        fill=PANEL_BG,
        line=PANEL_BORDER,
        line_pt=0.75,
        round_cm=0.18,
    )

    add_carrier_legend(sld, 7, x=1.5, y=18.02)

    # ---------------- Animations: Exact 4 Clicks ----------------
    # Click 1: Table rows 1 & 2
    anim_fade(sld, tbl_rows[0], trigger=TRIG_CLICK, duration=0.4)
    anim_fade(sld, tbl_rows[1], trigger=TRIG_AFTER_PREV, duration=0.4)

    # Click 2: Silicon panel sequence
    anim_fade(sld, si_axes, trigger=TRIG_CLICK, duration=0.3)
    anim_wipe(sld, si_tri, direction=MSO_ANIM_DIR_TOP, trigger=TRIG_AFTER_PREV, duration=0.6)
    anim_fade(sld, si_epeak, trigger=TRIG_AFTER_PREV, duration=0.3)
    anim_wipe(sld, si_w_br, direction=MSO_ANIM_DIR_LEFT, trigger=TRIG_AFTER_PREV, duration=0.4)
    anim_fade(sld, si_w_lbl, trigger=TRIG_WITH_PREV, duration=0.3)
    anim_fade(sld, si_strip, trigger=TRIG_AFTER_PREV, duration=0.35)
    anim_fade(sld, si_pplus, trigger=TRIG_WITH_PREV, duration=0.35)
    anim_fade(sld, si_e_arr, trigger=TRIG_WITH_PREV, duration=0.35)
    anim_fade(sld, si_h_arr, trigger=TRIG_WITH_PREV, duration=0.35)
    anim_fade(sld, si_bot_lbl, trigger=TRIG_WITH_PREV, duration=0.35)

    # Click 3: SiC panel + area note + Table rows 3 & 4
    anim_fade(sld, sic_axes, trigger=TRIG_CLICK, duration=0.3)
    anim_wipe(sld, sic_tri, direction=MSO_ANIM_DIR_TOP, trigger=TRIG_AFTER_PREV, duration=0.6)
    anim_fade(sld, sic_epeak, trigger=TRIG_AFTER_PREV, duration=0.3)
    anim_wipe(sld, sic_w_br, direction=MSO_ANIM_DIR_LEFT, trigger=TRIG_AFTER_PREV, duration=0.4)
    anim_fade(sld, sic_w_lbl, trigger=TRIG_WITH_PREV, duration=0.3)
    anim_fade(sld, sic_strip, trigger=TRIG_AFTER_PREV, duration=0.35)
    anim_fade(sld, area_note, trigger=TRIG_AFTER_PREV, duration=0.4)
    anim_fade(sld, tbl_rows[2], trigger=TRIG_AFTER_PREV, duration=0.4)
    anim_fade(sld, tbl_rows[3], trigger=TRIG_AFTER_PREV, duration=0.4)

    # Click 4: Pulse Si P+ and hole arrow -> Fade SiC "仅电子导电 → 无拖尾"
    anim_pulse(sld, si_pplus, trigger=TRIG_CLICK, duration=0.5)
    anim_pulse(sld, si_h_arr, trigger=TRIG_WITH_PREV, duration=0.5)
    anim_fade(sld, sic_bot_lbl, trigger=TRIG_AFTER_PREV, duration=0.4)


def build_slide_8(sld: Any) -> None:
    """Slide 8: SiC circuit-level improvements across conduction, switching & freewheeling — 4 clicks."""
    add_slide_chrome(sld, 8, "SiC 在导通、开关、续流上都明显改善", "SiC")

    # Three panels: x=1.5..11.4, 12.0..21.9, 22.5..32.4; y=3.6..15.0 (w=9.9, h=11.4)
    panel_xs = [1.5, 12.0, 22.5]
    panel_meta = [(2, "导通特性"), (3, "开关损耗（双脉冲）"), (4, "续流与反向恢复")]
    for px, (bnum, bttl) in zip(panel_xs, panel_meta):
        add_box(sld, f"p8_panel_{bnum}_bg", px, 3.6, 9.9, 11.4, fill=WHITE, line=PANEL_BORDER, line_pt=0.75, round_cm=0.2)
        add_req_badge(sld, f"p8_panel_{bnum}_badge", bnum, px + 0.4, 3.88)
        add_simple_label(sld, f"p8_panel_{bnum}_hdr", px + 1.4, 3.85, 8.1, 0.85, bttl, size=16, color=TEXT_MAIN, bold=True)

    # ---------------- Panel 1: Output I-V ----------------
    p1_x0, p1_y0, p1_w, p1_h = 2.65, 12.55, 7.9, 6.9
    add_line_seg(sld, "p8_p1_ay", p1_x0, p1_y0, p1_x0, p1_y0 - p1_h, color=TEXT_MAIN, weight_pt=1.5, arrow_end=True)
    add_line_seg(sld, "p8_p1_ax", p1_x0, p1_y0, p1_x0 + p1_w, p1_y0, color=TEXT_MAIN, weight_pt=1.5, arrow_end=True)
    add_simple_label(sld, "p8_p1_ilbl", p1_x0 - 0.55, p1_y0 - p1_h, 0.5, 0.55, "I", size=14, color=TEXT_MAIN, italic=True, font=FONT_MATH, align=PP_ALIGN_RIGHT)
    add_textbox(
        sld,
        "p8_p1_vlbl",
        p1_x0 + p1_w - 0.8,
        p1_y0 + 0.05,
        1.1,
        0.55,
        [{"runs": [make_run("V", size=14, color=TEXT_MAIN, italic=True, font=FONT_MATH), make_run("on", size=14, color=TEXT_MAIN, font=FONT_MATH, sub=True)]}],
    )

    # Shaded advantage region (x from 0 to crossing x_cross = p1_x0 + 4.9, y_cross = p1_y0 - 4.7)
    xc, yc = p1_x0 + 4.9, p1_y0 - 4.7
    p8_p1_fill = add_polyline(
        sld,
        "p8_p1_fill",
        [(p1_x0, p1_y0), (p1_x0 + 1.45, p1_y0), (p1_x0 + 2.2, p1_y0 - 0.6), (xc, yc)],
        color=None,
        fill_color=SIC_LIGHT,
        fill_transp=0.15,
        closed=True,
    )
    p8_p1_si = add_polyline(
        sld,
        "p8_p1_si",
        [(p1_x0, p1_y0), (p1_x0 + 1.45, p1_y0), (p1_x0 + 2.2, p1_y0 - 0.6), (xc, yc), (p1_x0 + 6.4, p1_y0 - 6.7)],
        color=SI_COLOR,
        weight_pt=2.5,
    )
    p8_p1_sic = add_polyline(
        sld,
        "p8_p1_sic",
        [(p1_x0, p1_y0), (xc, yc), (p1_x0 + 7.1, p1_y0 - 6.6)],
        color=SIC_COLOR,
        weight_pt=2.5,
    )
    p8_p1_cross = add_oval(sld, "p8_p1_cross", xc, yc, 0.24, fill=TEXT_MAIN, line=WHITE, line_pt=1.0)
    p8_p1_notes = group_shapes(
        sld,
        [
            add_simple_label(sld, "p8_p1_sic_lbl", p1_x0 + 0.35, p1_y0 - 4.75, 3.6, 0.60, "SiC MOSFET", size=14, color=SIC_COLOR, bold=True),
            add_simple_label(sld, "p8_p1_si_lbl", p1_x0 + 4.35, p1_y0 - 6.85, 2.8, 0.60, "硅 IGBT", size=14, color=SI_COLOR, bold=True),
            add_simple_label(
                sld,
                "p8_p1_adv",
                p1_x0 + 0.25,
                p1_y0 - 2.40,
                3.5,
                1.25,
                "中小电流：\nSiC 压降更低",
                size=14,
                color=SIC_COLOR,
                bold=True,
                align=PP_ALIGN_CENTER,
                fill=WHITE,
                line=SIC_COLOR,
                line_pt=0.75,
                round_cm=0.14,
            ),
            add_simple_label(sld, "p8_p1_note", 1.85, 13.25, 9.2, 1.35, "交点取决于芯片面积与结温\n无 0.7 V 门槛压降", size=14, color=TEXT_SUB, align=PP_ALIGN_CENTER),
        ],
        "p8_p1_notes",
    )

    # ---------------- Panel 2: Double-Pulse Bar Chart ----------------
    p2_x0, p2_y0, p2_w = 13.0, 11.85, 8.2
    add_line_seg(sld, "p8_p2_ay", p2_x0, p2_y0, p2_x0, 5.4, color=TEXT_MAIN, weight_pt=1.5, arrow_end=True)
    add_line_seg(sld, "p8_p2_ax", p2_x0, p2_y0, p2_x0 + p2_w, p2_y0, color=TEXT_MAIN, weight_pt=1.5)
    add_simple_label(sld, "p8_p2_ylbl", 13.15, 4.88, 2.6, 0.55, "能量 (mJ)", size=14, color=TEXT_SUB, align=PP_ALIGN_LEFT, word_wrap=False)
    add_box(sld, "p8_p2_lg1_sq", 16.8, 5.00, 0.30, 0.30, fill=SI_COLOR, line=None)
    add_simple_label(sld, "p8_p2_lg1_tx", 17.15, 4.86, 1.3, 0.58, "硅", size=14, color=SI_COLOR, bold=True)
    add_box(sld, "p8_p2_lg2_sq", 18.5, 5.00, 0.30, 0.30, fill=SIC_COLOR, line=None)
    add_simple_label(sld, "p8_p2_lg2_tx", 18.85, 4.86, 2.3, 0.58, "4H-SiC", size=14, color=SIC_COLOR, bold=True, word_wrap=False)

    # Scale: max 8.78 mJ -> 5.4 cm height
    sc = 5.4 / 8.78
    bar_w = 1.25
    # Group 1: E_off (8.78 vs 1.28)
    b1_si_h, b1_sic_h = 8.78 * sc, 1.28 * sc
    b1_si = add_box(sld, "p8_p2_b1_si", 13.55, p2_y0 - b1_si_h, bar_w, b1_si_h, fill=SI_COLOR, line=None)
    b1_sic = add_box(sld, "p8_p2_b1_sic", 15.05, p2_y0 - b1_sic_h, bar_w, b1_sic_h, fill=SIC_COLOR, line=None)
    # Group 2: E_rr (5.93 vs 0.53)
    b2_si_h, b2_sic_h = 5.93 * sc, 0.53 * sc
    b2_si = add_box(sld, "p8_p2_b2_si", 17.55, p2_y0 - b2_si_h, bar_w, b2_si_h, fill=SI_COLOR, line=None)
    b2_sic = add_box(sld, "p8_p2_b2_sic", 19.05, p2_y0 - b2_sic_h, bar_w, b2_sic_h, fill=SIC_COLOR, line=None)

    add_textbox(sld, "p8_p2_g1_lbl", 13.3, 11.95, 3.2, 0.65, [{"runs": [make_run("E", size=15, color=TEXT_MAIN, bold=True, italic=True, font=FONT_MATH), make_run("off", size=15, color=TEXT_MAIN, bold=True, font=FONT_MATH, sub=True)], "align": PP_ALIGN_CENTER}])
    add_textbox(sld, "p8_p2_g2_lbl", 17.3, 11.95, 3.2, 0.65, [{"runs": [make_run("E", size=15, color=TEXT_MAIN, bold=True, italic=True, font=FONT_MATH), make_run("rr", size=15, color=TEXT_MAIN, bold=True, font=FONT_MATH, sub=True)], "align": PP_ALIGN_CENTER}])

    p8_p2_vals_si = group_shapes(
        sld,
        [
            add_simple_label(sld, "p8_p2_v1_si", 13.35, p2_y0 - b1_si_h - 0.65, 1.65, 0.60, "8.78", size=14, color=SI_COLOR, bold=True, align=PP_ALIGN_CENTER),
            add_simple_label(sld, "p8_p2_v2_si", 17.35, p2_y0 - b2_si_h - 0.65, 1.65, 0.60, "5.93", size=14, color=SI_COLOR, bold=True, align=PP_ALIGN_CENTER),
        ],
        "p8_p2_vals_si",
    )
    p8_p2_vals_sic = group_shapes(
        sld,
        [
            add_simple_label(sld, "p8_p2_v1_sic", 14.85, p2_y0 - b1_sic_h - 0.65, 1.65, 0.60, "1.28", size=14, color=SIC_COLOR, bold=True, align=PP_ALIGN_CENTER),
            add_simple_label(sld, "p8_p2_v2_sic", 18.85, p2_y0 - b2_sic_h - 0.65, 1.65, 0.60, "0.53", size=14, color=SIC_COLOR, bold=True, align=PP_ALIGN_CENTER),
        ],
        "p8_p2_vals_sic",
    )
    p8_p2_deltas = group_shapes(
        sld,
        [
            add_simple_label(sld, "p8_p2_d1", 14.70, 7.35, 2.75, 0.95, "−85%", size=24, color=SIC_COLOR, bold=True, align=PP_ALIGN_CENTER, word_wrap=False),
            add_simple_label(sld, "p8_p2_d2", 18.82, 8.45, 2.75, 0.95, "−91%", size=24, color=SIC_COLOR, bold=True, align=PP_ALIGN_CENTER, word_wrap=False),
        ],
        "p8_p2_deltas",
    )
    add_textbox(
        sld,
        "p8_p2_foot",
        12.3,
        12.75,
        9.3,
        1.95,
        [
            {
                "runs": [
                    make_run("1200 V / 100 A 模块（600 V、100 A、125 ℃ 双脉冲）；", size=14, color=TEXT_SUB),
                    make_run("E", size=14, color=TEXT_SUB, italic=True, font=FONT_MATH),
                    make_run("rr", size=14, color=TEXT_SUB, font=FONT_MATH, sub=True),
                    make_run(" 的 SiC 为外并肖特基二极管", size=14, color=TEXT_SUB),
                ]
            }
        ],
    )

    # ---------------- Panel 3: Freewheeling Half-Bridge ----------------
    # Static half-bridge schematic (banner at y=4.85..5.60; rails y=5.95..12.65)
    hx = 25.0
    dx = hx + 1.55
    add_line_seg(sld, "p8_p3_rail_t", hx - 1.2, 5.95, hx + 1.8, 5.95, color=TEXT_MAIN, weight_pt=2.0)
    add_line_seg(sld, "p8_p3_rail_b", hx - 1.2, 12.65, hx + 1.8, 12.65, color=TEXT_MAIN, weight_pt=2.0)
    add_simple_label(sld, "p8_p3_vdc", hx - 1.9, 5.65, 1.4, 0.55, "+U", size=14, color=TEXT_MAIN, bold=True, font=FONT_MATH)
    add_simple_label(sld, "p8_p3_gnd", hx - 1.9, 12.35, 1.4, 0.55, "0 V", size=14, color=TEXT_MAIN, bold=True, font=FONT_MATH)

    # Upper MOSFET Q1 (y=6.55..8.05) & Lower MOSFET Q2 (y=9.90..11.40)
    add_line_seg(sld, "p8_p3_leg_t", hx, 5.95, hx, 6.55, color=TEXT_MAIN, weight_pt=1.75)
    add_box(sld, "p8_p3_qu", hx - 0.75, 6.55, 1.5, 1.50, fill=PANEL_BG, line=TEXT_MAIN, line_pt=1.5, round_cm=0.14)
    add_simple_label(sld, "p8_p3_qu_lbl", hx - 0.75, 6.55, 1.5, 1.50, "Q₁", size=14, color=TEXT_MAIN, bold=True, align=PP_ALIGN_CENTER)

    add_line_seg(sld, "p8_p3_leg_m", hx, 8.05, hx, 9.90, color=TEXT_MAIN, weight_pt=1.75)
    add_box(sld, "p8_p3_ql", hx - 0.75, 9.90, 1.5, 1.50, fill=PANEL_BG, line=SIC_COLOR, line_pt=1.75, round_cm=0.14)
    add_simple_label(sld, "p8_p3_ql_lbl", hx - 0.75, 9.90, 1.5, 1.50, "Q₂", size=14, color=SIC_COLOR, bold=True, align=PP_ALIGN_CENTER)
    add_line_seg(sld, "p8_p3_leg_b", hx, 11.40, hx, 12.65, color=TEXT_MAIN, weight_pt=1.75)

    # Upper body diode branch on right of Q1 (dx = hx + 1.55)
    add_line_seg(sld, "p8_p3_bdu_t", hx, 6.22, dx, 6.22, color=TEXT_SUB, weight_pt=1.25)
    add_line_seg(sld, "p8_p3_bdu_v1", dx, 6.22, dx, 7.05, color=TEXT_SUB, weight_pt=1.25)
    add_line_seg(sld, "p8_p3_bdu_v2", dx, 7.55, dx, 8.38, color=TEXT_SUB, weight_pt=1.25)
    add_line_seg(sld, "p8_p3_bdu_b", dx, 8.38, hx, 8.38, color=TEXT_SUB, weight_pt=1.25)
    diode_tri_u = sld.Shapes.AddShape(MSO_SHAPE_ISOSCELES_TRIANGLE, cm(dx - 0.23), cm(7.07), cm(0.46), cm(0.46))
    clean_shape(diode_tri_u)
    diode_tri_u.Name = "p8_p3_bdu_tri"
    diode_tri_u.Fill.Visible = -1
    diode_tri_u.Fill.Solid()
    diode_tri_u.Fill.ForeColor.RGB = rgb(WHITE)
    diode_tri_u.Line.Visible = -1
    diode_tri_u.Line.ForeColor.RGB = rgb(TEXT_MAIN)
    diode_tri_u.Line.Weight = 1.5
    add_line_seg(sld, "p8_p3_bdu_bar", dx - 0.26, 7.05, dx + 0.26, 7.05, color=TEXT_MAIN, weight_pt=1.75)

    # Lower body diode branch on right of Q2 (dx = hx + 1.55)
    add_line_seg(sld, "p8_p3_bd_t", hx, 9.55, dx, 9.55, color=TEXT_SUB, weight_pt=1.25)
    add_line_seg(sld, "p8_p3_bd_v1", dx, 9.55, dx, 10.42, color=TEXT_SUB, weight_pt=1.25)
    add_line_seg(sld, "p8_p3_bd_v2", dx, 10.92, dx, 11.78, color=TEXT_SUB, weight_pt=1.25)
    add_line_seg(sld, "p8_p3_bd_b", dx, 11.78, hx, 11.78, color=TEXT_SUB, weight_pt=1.25)
    diode_tri = sld.Shapes.AddShape(MSO_SHAPE_ISOSCELES_TRIANGLE, cm(dx - 0.23), cm(10.44), cm(0.46), cm(0.46))
    clean_shape(diode_tri)
    diode_tri.Name = "p8_p3_bd_tri"
    diode_tri.Fill.Visible = -1
    diode_tri.Fill.Solid()
    diode_tri.Fill.ForeColor.RGB = rgb(WHITE)
    diode_tri.Line.Visible = -1
    diode_tri.Line.ForeColor.RGB = rgb(TEXT_MAIN)
    diode_tri.Line.Weight = 1.5
    add_line_seg(sld, "p8_p3_bd_bar", dx - 0.26, 10.42, dx + 0.26, 10.42, color=TEXT_MAIN, weight_pt=1.75)

    # Midpoint -> Inductive load L
    add_line_seg(sld, "p8_p3_out_wire", hx, 8.95, 29.0, 8.95, color=TEXT_MAIN, weight_pt=2.0)
    add_box(sld, "p8_p3_load", 29.0, 8.40, 2.9, 1.10, fill=PANEL_BG, line=TEXT_MAIN, line_pt=1.5, round_cm=0.14)
    add_simple_label(sld, "p8_p3_load_lbl", 29.0, 8.40, 2.9, 1.10, "感性负载 L", size=14, color=TEXT_MAIN, bold=True, align=PP_ALIGN_CENTER, word_wrap=False)

    # Click 3: Deadtime body-diode path (orange dashed, clean forward route without back-step)
    dt_path = add_polyline(
        sld,
        "p8_p3_dt_arr",
        [(hx + 0.15, 12.35), (dx + 0.35, 12.35), (dx + 0.35, 9.20), (28.9, 9.20)],
        color=COST_COLOR,
        weight_pt=2.5,
        dash=MSO_LINE_DASH,
        arrow_end=True,
    )
    dt_lbl = add_simple_label(
        sld,
        "p8_p3_dt_lbl",
        23.0,
        4.85,
        8.9,
        0.72,
        "死区：经体二极管续流（压降 2–3 V）",
        size=14,
        color=COST_COLOR,
        bold=True,
        align=PP_ALIGN_CENTER,
        fill=COST_LIGHT,
        line=COST_COLOR,
        line_pt=0.75,
        round_cm=0.14,
    )
    p8_p3_deadtime = group_shapes(sld, [dt_path, dt_lbl], "p8_p3_deadtime")

    # Click 4: Sync-rectification channel path (teal solid)
    sr_path = add_polyline(
        sld,
        "p8_p3_sr_arr",
        [(hx - 0.18, 12.35), (hx - 0.18, 8.70), (28.9, 8.70)],
        color=SIC_COLOR,
        weight_pt=3.0,
        arrow_end=True,
    )
    sr_lbl = add_simple_label(
        sld,
        "p8_p3_sr_lbl",
        23.0,
        4.85,
        8.9,
        0.72,
        "同步整流：经沟道双向导通（低阻）",
        size=14,
        color=SIC_COLOR,
        bold=True,
        align=PP_ALIGN_CENTER,
        fill=SIC_LIGHT,
        line=SIC_COLOR,
        line_pt=0.75,
        round_cm=0.14,
    )
    p8_p3_syncrec = group_shapes(sld, [sr_path, sr_lbl], "p8_p3_syncrec")

    add_textbox(
        sld,
        "p8_p3_foot",
        22.9,
        13.35,
        9.1,
        1.30,
        [
            {
                "runs": [
                    make_run("外并 SiC 肖特基二极管：", size=14, color=TEXT_SUB, bold=True),
                    make_run("E", size=14, color=SIC_COLOR, bold=True, italic=True, font=FONT_MATH),
                    make_run("rr", size=14, color=SIC_COLOR, bold=True, font=FONT_MATH, sub=True),
                    make_run(" −91%", size=14, color=SIC_COLOR, bold=True),
                ],
                "align": PP_ALIGN_CENTER,
            }
        ],
    )

    # ---------------- Bottom Conclusion Strip (y=15.55..17.85) ----------------
    bot_specs = [
        (2, 1.5, [make_run("中小电流压降更低", size=18, color=TEXT_MAIN, bold=True)]),
        (
            3,
            12.0,
            [
                make_run("E", size=18, color=SIC_COLOR, bold=True, italic=True, font=FONT_MATH),
                make_run("off", size=18, color=SIC_COLOR, bold=True, font=FONT_MATH, sub=True),
                make_run(" −85%，频率 > 20 kHz", size=18, color=TEXT_MAIN, bold=True),
            ],
        ),
        (4, 22.5, [make_run("同步整流 + 外并肖特基", size=18, color=TEXT_MAIN, bold=True)]),
    ]
    bot_cards = []
    for num, cx, runs in bot_specs:
        bg = add_box(sld, f"p8_bot_{num}_bg", cx, 15.55, 9.9, 2.25, fill=SIC_LIGHT, line=SIC_COLOR, line_pt=1.25, round_cm=0.2)
        bd = add_req_badge(sld, f"p8_bot_{num}_badge", num, cx + 0.35, 16.28)
        tx = add_textbox(sld, f"p8_bot_{num}_txt", cx + 1.35, 15.65, 8.35, 2.05, [{"runs": runs}], valign=MSO_ANCHOR_MIDDLE)
        bot_cards.append(group_shapes(sld, [bg, bd, tx], f"p8_bot_{num}"))

    # ---------------- Animations: Exact 4 Clicks ----------------
    # Click 1: Panel 1 I-V + bottom badge 2
    anim_wipe(sld, p8_p1_si, direction=MSO_ANIM_DIR_LEFT, trigger=TRIG_CLICK, duration=0.55)
    anim_wipe(sld, p8_p1_sic, direction=MSO_ANIM_DIR_LEFT, trigger=TRIG_AFTER_PREV, duration=0.55)
    anim_fade(sld, p8_p1_fill, trigger=TRIG_WITH_PREV, duration=0.4)
    anim_fade(sld, p8_p1_cross, trigger=TRIG_WITH_PREV, duration=0.3)
    anim_fade(sld, p8_p1_notes, trigger=TRIG_WITH_PREV, duration=0.4)
    anim_fade(sld, bot_cards[0], trigger=TRIG_WITH_PREV, duration=0.4)

    # Click 2: Panel 2 Bars bottom->up + deltas + bottom badge 3
    anim_wipe(sld, b1_si, direction=MSO_ANIM_DIR_BOTTOM, trigger=TRIG_CLICK, duration=0.5)
    anim_wipe(sld, b2_si, direction=MSO_ANIM_DIR_BOTTOM, trigger=TRIG_WITH_PREV, duration=0.5)
    anim_fade(sld, p8_p2_vals_si, trigger=TRIG_WITH_PREV, duration=0.3)
    anim_wipe(sld, b1_sic, direction=MSO_ANIM_DIR_BOTTOM, trigger=TRIG_AFTER_PREV, duration=0.5)
    anim_wipe(sld, b2_sic, direction=MSO_ANIM_DIR_BOTTOM, trigger=TRIG_WITH_PREV, duration=0.5)
    anim_fade(sld, p8_p2_vals_sic, trigger=TRIG_WITH_PREV, duration=0.3)
    anim_fade(sld, p8_p2_deltas, trigger=TRIG_AFTER_PREV, duration=0.4)
    anim_fade(sld, bot_cards[1], trigger=TRIG_WITH_PREV, duration=0.4)

    # Click 3: Panel 3 Dead-time path
    anim_wipe(sld, p8_p3_deadtime, direction=MSO_ANIM_DIR_BOTTOM, trigger=TRIG_CLICK, duration=0.6)

    # Click 4: Dead-time fades out, Sync-rectification wipes in + bottom badge 4
    anim_exit_fade(sld, p8_p3_deadtime, trigger=TRIG_CLICK, duration=0.3)
    anim_wipe(sld, p8_p3_syncrec, direction=MSO_ANIM_DIR_BOTTOM, trigger=TRIG_WITH_PREV, duration=0.6)
    anim_fade(sld, bot_cards[2], trigger=TRIG_WITH_PREV, duration=0.4)


def build_slide_9(sld: Any) -> None:
    """Slide 9: Four new SiC costs & engineering countermeasures — 4 clicks."""
    add_slide_chrome(sld, 9, "SiC 的新代价：更快、更小、更难制造", "SiC")

    card_xs = [1.50, 9.37, 17.24, 25.11]
    w = 7.30

    # --- Card 1: Overshoot & false turn-on ---
    x1 = card_xs[0]
    c1_prob_parts = [
        add_box(sld, "p9_c1_bg", x1, 3.6, w, 11.55, fill=WHITE, line=PANEL_BORDER, line_pt=0.75, round_cm=0.2),
        add_simple_label(sld, "p9_c1_hdr", x1, 3.6, w, 0.90, "1. 过冲与误导通", size=16, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=COST_COLOR, line=None),
        # Mini schematic: C_gd coupling + turn-off spike
        add_box(sld, "p9_c1_diag", x1 + 0.35, 4.72, w - 0.7, 5.45, fill=PANEL_BG, line=PANEL_BORDER, line_pt=0.75, round_cm=0.14),
        # Drain/Gate nodes & capacitor
        add_simple_label(sld, "p9_c1_d_lbl", x1 + 0.45, 4.88, 1.50, 0.62, "D (漏)", size=14, color=TEXT_MAIN, bold=True, word_wrap=False),
        add_line_seg(sld, "p9_c1_w1", x1 + 1.92, 5.20, x1 + 2.35, 5.20, color=TEXT_MAIN, weight_pt=1.5),
        add_line_seg(sld, "p9_c1_cap1", x1 + 2.35, 4.92, x1 + 2.35, 5.48, color=COST_COLOR, weight_pt=2.5),
        add_line_seg(sld, "p9_c1_cap2", x1 + 2.60, 4.92, x1 + 2.60, 5.48, color=COST_COLOR, weight_pt=2.5),
        add_line_seg(sld, "p9_c1_w2", x1 + 2.60, 5.20, x1 + 3.05, 5.20, color=TEXT_MAIN, weight_pt=1.5),
        add_simple_label(sld, "p9_c1_g_lbl", x1 + 3.08, 4.88, 1.55, 0.62, "G (栅)", size=14, color=TEXT_MAIN, bold=True, word_wrap=False),
        add_textbox(sld, "p9_c1_cgd", x1 + 1.72, 5.52, 1.5, 0.55, [{"runs": [make_run("C", size=14, color=COST_COLOR, bold=True, italic=True, font=FONT_MATH), make_run("gd", size=14, color=COST_COLOR, bold=True, font=FONT_MATH, sub=True)], "align": PP_ALIGN_CENTER}]),
        add_line_seg(sld, "p9_c1_coup_arr", x1 + 1.75, 6.16, x1 + 3.45, 6.16, color=COST_COLOR, weight_pt=2.0, arrow_end=True),
        add_simple_label(sld, "p9_c1_dvdt", x1 + 4.95, 4.88, 1.95, 0.62, "高 dv/dt", size=14, color=COST_COLOR, bold=True, word_wrap=False),
        # Voltage spike waveform below
        add_line_seg(sld, "p9_c1_wx", x1 + 0.7, 9.65, x1 + 6.5, 9.65, color=TEXT_SUB, weight_pt=1.0),
        add_polyline(
            sld,
            "p9_c1_spike",
            [(x1 + 0.8, 9.55), (x1 + 1.7, 9.55), (x1 + 2.15, 7.25), (x1 + 2.50, 6.60), (x1 + 2.85, 8.25), (x1 + 3.25, 7.65), (x1 + 3.70, 7.95), (x1 + 6.2, 7.95)],
            color=COST_COLOR,
            weight_pt=2.25,
        ),
        add_textbox(
            sld,
            "p9_c1_vos",
            x1 + 3.45,
            6.55,
            3.35,
            1.15,
            [
                {
                    "runs": [
                        make_run("过冲\nV", size=14, color=COST_COLOR, bold=True),
                        make_run("os", size=14, color=COST_COLOR, bold=True, sub=True),
                        make_run(" = L", size=14, color=COST_COLOR, bold=True, font=FONT_MATH),
                        make_run("σ", size=14, color=COST_COLOR, bold=True, font=FONT_MATH, sub=True),
                        make_run("·di/dt", size=14, color=COST_COLOR, bold=True, font=FONT_MATH),
                    ]
                }
            ],
        ),
        # KPI & Note
        add_textbox(
            sld,
            "p9_c1_kpi",
            x1 + 0.3,
            10.45,
            w - 0.6,
            1.45,
            [
                {
                    "runs": [
                        make_run("V", size=28, color=COST_COLOR, bold=True, italic=True, font=FONT_MATH),
                        make_run("th", size=28, color=COST_COLOR, bold=True, font=FONT_MATH, sub=True),
                        make_run(" ≈ 2–4.5 V", size=26, color=COST_COLOR, bold=True),
                    ],
                    "align": PP_ALIGN_CENTER,
                }
            ],
        ),
        add_simple_label(
            sld,
            "p9_c1_desc",
            x1 + 0.35,
            12.00,
            w - 0.7,
            3.1,
            "阈值低于 IGBT（约 5–6.5 V），高温更低；高 di/dt、dv/dt 下易电压过冲与寄生导通。",
            size=14,
            color=TEXT_MAIN,
            valign=MSO_ANCHOR_TOP,
        ),
    ]
    c1_prob = group_shapes(sld, c1_prob_parts, "p9_card_1_prob")
    c1_fix = add_textbox(
        sld,
        "p9_card_1_fix",
        x1,
        15.35,
        w,
        2.25,
        [
            {"runs": [make_run("对策", size=14, color=SIC_COLOR, bold=True)], "space_after": 1, "line_spacing": 1.08},
            {"runs": [make_run("降寄生电感 · 开尔文源极 · −2～−5 V 负压关断", size=14, color=TEXT_MAIN, bold=True)], "line_spacing": 1.08},
        ],
        fill=SIC_LIGHT,
        line=SIC_COLOR,
        line_pt=1.25,
        round_cm=0.18,
        margin_cm=(0.20, 0.16, 0.08, 0.08),
    )

    # --- Card 2: Body diode ---
    x2 = card_xs[1]
    c2_prob_parts = [
        add_box(sld, "p9_c2_bg", x2, 3.6, w, 11.55, fill=WHITE, line=PANEL_BORDER, line_pt=0.75, round_cm=0.2),
        add_simple_label(sld, "p9_c2_hdr", x2, 3.6, w, 0.90, "2. 体二极管特性", size=16, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=COST_COLOR, line=None),
        add_box(sld, "p9_c2_diag", x2 + 0.35, 4.75, w - 0.7, 5.45, fill=PANEL_BG, line=PANEL_BORDER, line_pt=0.75, round_cm=0.14),
        # Reverse I-V diagram
        add_line_seg(sld, "p9_c2_ay", x2 + 1.25, 9.65, x2 + 1.25, 5.10, color=TEXT_MAIN, weight_pt=1.25, arrow_end=True),
        add_line_seg(sld, "p9_c2_ax", x2 + 1.25, 9.65, x2 + 6.45, 9.65, color=TEXT_MAIN, weight_pt=1.25, arrow_end=True),
        add_textbox(sld, "p9_c2_ilbl", x2 + 0.36, 4.95, 0.85, 0.58, [{"runs": [make_run("I", size=14, color=TEXT_MAIN, italic=True, font=FONT_MATH), make_run("sd", size=14, color=TEXT_MAIN, font=FONT_MATH, sub=True)]}]),
        add_textbox(sld, "p9_c2_vlbl", x2 + 5.2, 9.68, 1.4, 0.48, [{"runs": [make_run("V", size=14, color=TEXT_MAIN, italic=True, font=FONT_MATH), make_run("sd", size=14, color=TEXT_MAIN, font=FONT_MATH, sub=True)]}]),
        add_polyline(sld, "p9_c2_ch", [(x2 + 1.25, 9.65), (x2 + 3.4, 5.45)], color=SIC_COLOR, weight_pt=2.5),
        add_polyline(sld, "p9_c2_bd", [(x2 + 1.25, 9.65), (x2 + 3.85, 9.65), (x2 + 4.5, 8.6), (x2 + 5.6, 5.65)], color=COST_COLOR, weight_pt=2.5),
        add_simple_label(sld, "p9_c2_ch_l", x2 + 1.4, 5.85, 2.2, 0.55, "沟道", size=14, color=SIC_COLOR, bold=True),
        add_simple_label(sld, "p9_c2_bd_l", x2 + 4.3, 6.75, 2.2, 0.60, "体二极管", size=14, color=COST_COLOR, bold=True),
        add_simple_label(sld, "p9_c2_kpi", x2 + 0.3, 10.45, w - 0.6, 1.45, "2–3 V", size=28, color=COST_COLOR, bold=True, align=PP_ALIGN_CENTER),
        add_simple_label(
            sld,
            "p9_c2_desc",
            x2 + 0.35,
            12.00,
            w - 0.7,
            3.1,
            "宽禁带导致 PN 体二极管开启压降偏高（2–3 V）；长期导通易引发双极退化，使导通电阻增大。",
            size=14,
            color=TEXT_MAIN,
            valign=MSO_ANCHOR_TOP,
        ),
    ]
    c2_prob = group_shapes(sld, c2_prob_parts, "p9_card_2_prob")
    c2_fix = add_textbox(
        sld,
        "p9_card_2_fix",
        x2,
        15.35,
        w,
        2.25,
        [
            {"runs": [make_run("对策", size=14, color=SIC_COLOR, bold=True)], "space_after": 1, "line_spacing": 1.08},
            {"runs": [make_run("同步整流缩短导通 · 外并 SiC 肖特基二极管", size=14, color=TEXT_MAIN, bold=True)], "line_spacing": 1.08},
        ],
        fill=SIC_LIGHT,
        line=SIC_COLOR,
        line_pt=1.25,
        round_cm=0.18,
        margin_cm=(0.20, 0.16, 0.08, 0.08),
    )

    # --- Card 3: Thermal & Short Circuit ---
    x3 = card_xs[2]
    c3_prob_parts = [
        add_box(sld, "p9_c3_bg", x3, 3.6, w, 11.55, fill=WHITE, line=PANEL_BORDER, line_pt=0.75, round_cm=0.2),
        add_simple_label(sld, "p9_c3_hdr", x3, 3.6, w, 0.90, "3. 热集中与短路耐受", size=16, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=COST_COLOR, line=None),
        add_box(sld, "p9_c3_diag", x3 + 0.35, 4.75, w - 0.7, 5.45, fill=PANEL_BG, line=PANEL_BORDER, line_pt=0.75, round_cm=0.14),
        # Area comparison squares
        add_simple_label(sld, "p9_c3_a_hdr", x3 + 0.55, 4.86, 6.2, 0.58, "同电流芯片面积对比", size=14, color=TEXT_SUB, bold=True),
        add_simple_label(sld, "p9_c3_igbt_sq", x3 + 1.0, 5.56, 2.0, 1.95, "IGBT\n面积大", size=14, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=SI_COLOR, line=None, round_cm=0.12),
        add_simple_label(sld, "p9_c3_sic_sq", x3 + 4.3, 5.95, 1.25, 1.25, "SiC\n小", size=14, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=COST_COLOR, line=None, round_cm=0.10),
        # Short-circuit bars
        add_simple_label(sld, "p9_c3_sc_hdr", x3 + 0.55, 7.72, 6.2, 0.58, "短路耐受时间对比", size=14, color=TEXT_SUB, bold=True),
        add_simple_label(sld, "p9_c3_sc1", x3 + 0.65, 8.42, 5.2, 0.60, "IGBT ≈ 10 μs", size=14, color=WHITE, bold=True, align=PP_ALIGN_LEFT, fill=SI_COLOR, line=None),
        add_box(sld, "p9_c3_sc2_bar", x3 + 0.65, 9.22, 1.95, 0.60, fill=COST_COLOR, line=None),
        add_simple_label(sld, "p9_c3_sc2", x3 + 2.75, 9.22, 3.8, 0.60, "SiC 2–5 μs", size=14, color=COST_COLOR, bold=True, align=PP_ALIGN_LEFT),
        add_simple_label(sld, "p9_c3_kpi", x3 + 0.3, 10.45, w - 0.6, 1.45, "2–5 μs", size=28, color=COST_COLOR, bold=True, align=PP_ALIGN_CENTER),
        add_simple_label(
            sld,
            "p9_c3_desc",
            x3 + 0.35,
            12.00,
            w - 0.7,
            3.1,
            "SiC 芯片面积小、热容低：热量高度集中，短路时温升极快，耐受时间明显短于硅 IGBT。",
            size=14,
            color=TEXT_MAIN,
            valign=MSO_ANCHOR_TOP,
        ),
    ]
    c3_prob = group_shapes(sld, c3_prob_parts, "p9_card_3_prob")
    c3_fix = add_textbox(
        sld,
        "p9_card_3_fix",
        x3,
        15.35,
        w,
        2.25,
        [
            {"runs": [make_run("对策", size=14, color=SIC_COLOR, bold=True)], "space_after": 1, "line_spacing": 1.08},
            {"runs": [make_run("银烧结 · 液冷散热 · 更快的过流保护", size=14, color=TEXT_MAIN, bold=True)], "line_spacing": 1.08},
        ],
        fill=SIC_LIGHT,
        line=SIC_COLOR,
        line_pt=1.25,
        round_cm=0.18,
        margin_cm=(0.20, 0.16, 0.08, 0.08),
    )

    # --- Card 4: Interface & Crystal Growth ---
    x4 = card_xs[3]
    c4_prob_parts = [
        add_box(sld, "p9_c4_bg", x4, 3.6, w, 11.55, fill=WHITE, line=PANEL_BORDER, line_pt=0.75, round_cm=0.2),
        add_simple_label(sld, "p9_c4_hdr", x4, 3.6, w, 0.90, "4. 界面与长晶成本", size=16, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=COST_COLOR, line=None),
        add_box(sld, "p9_c4_diag", x4 + 0.35, 4.75, w - 0.7, 5.45, fill=PANEL_BG, line=PANEL_BORDER, line_pt=0.75, round_cm=0.14),
        # PVT furnace using basic geometric shapes
        add_simple_label(sld, "p9_c4_f_hdr", x4 + 0.55, 4.84, 6.2, 0.58, "PVT 气相长晶炉示意", size=14, color=TEXT_SUB, bold=True),
        add_box(sld, "p9_c4_cruc", x4 + 2.0, 5.58, 2.8, 2.95, fill=WHITE, line=SI_COLOR, line_pt=1.5, round_cm=0.12),
        add_simple_label(sld, "p9_c4_seed", x4 + 2.35, 5.78, 2.1, 0.58, "籽晶", size=14, color=SIC_COLOR, bold=True, align=PP_ALIGN_CENTER, fill=SIC_LIGHT, line=SIC_COLOR, line_pt=0.75),
        add_simple_label(sld, "p9_c4_powd", x4 + 2.25, 7.72, 2.3, 0.65, "SiC 粉料", size=14, color=TEXT_MAIN, align=PP_ALIGN_CENTER, fill=AMBER_LIGHT, line=AMBER, line_pt=0.75),
        add_line_seg(sld, "p9_c4_subl1", x4 + 2.9, 7.62, x4 + 2.9, 6.48, color=COST_COLOR, weight_pt=1.5, dash=MSO_LINE_DASH, arrow_end=True),
        add_line_seg(sld, "p9_c4_subl2", x4 + 3.9, 7.62, x4 + 3.9, 6.48, color=COST_COLOR, weight_pt=1.5, dash=MSO_LINE_DASH, arrow_end=True),
        # Heating coils on left/right
        *[add_oval(sld, f"p9_c4_coilL_{k}", x4 + 1.55, 5.98 + k * 0.58, 0.34, fill=COST_COLOR, line=None) for k in range(4)],
        *[add_oval(sld, f"p9_c4_coilR_{k}", x4 + 5.25, 5.98 + k * 0.58, 0.34, fill=COST_COLOR, line=None) for k in range(4)],
        # Cost share bar at bottom of schematic
        add_box(sld, "p9_c4_costbar_bg", x4 + 0.55, 8.98, 6.2, 0.78, fill=WHITE, line=PANEL_BORDER, line_pt=0.75, round_cm=0.10),
        add_simple_label(sld, "p9_c4_costbar", x4 + 0.55, 8.98, 4.65, 0.78, "衬底+外延 ≥ 50%", size=14, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=COST_COLOR, line=None, word_wrap=False),
        add_simple_label(sld, "p9_c4_costrest", x4 + 5.22, 8.98, 1.50, 0.78, "其他", size=14, color=TEXT_SUB, align=PP_ALIGN_CENTER),
        add_simple_label(sld, "p9_c4_kpi", x4 + 0.25, 10.45, w - 0.5, 1.45, "2200–2400 ℃", size=24, color=COST_COLOR, bold=True, align=PP_ALIGN_CENTER, word_wrap=False),
        add_simple_label(
            sld,
            "p9_c4_desc",
            x4 + 0.35,
            12.00,
            w - 0.7,
            3.1,
            "界面缺陷多 → 需 +15～+18 V 栅压；常压升华生长慢、切片损耗大；150/200 mm 晶圆已量产。",
            size=14,
            color=TEXT_MAIN,
            valign=MSO_ANCHOR_TOP,
        ),
    ]
    c4_prob = group_shapes(sld, c4_prob_parts, "p9_card_4_prob")
    c4_fix = add_textbox(
        sld,
        "p9_card_4_fix",
        x4,
        15.35,
        w,
        2.25,
        [
            {"runs": [make_run("对策", size=14, color=SIC_COLOR, bold=True)], "space_after": 1, "line_spacing": 1.08},
            {"runs": [make_run("扩大晶圆尺寸（200 mm）降本 · 优化栅氧工艺", size=14, color=TEXT_MAIN, bold=True)], "line_spacing": 1.08},
        ],
        fill=SIC_LIGHT,
        line=SIC_COLOR,
        line_pt=1.25,
        round_cm=0.18,
        margin_cm=(0.20, 0.16, 0.08, 0.08),
    )

    # Exact 4 Clicks: Click k fades problem card (0.5 s), then after 1.0 s wipes countermeasure L->R
    for prob, fix in ((c1_prob, c1_fix), (c2_prob, c2_fix), (c3_prob, c3_fix), (c4_prob, c4_fix)):
        anim_fade(sld, prob, trigger=TRIG_CLICK, duration=0.5)
        anim_wipe(sld, fix, direction=MSO_ANIM_DIR_LEFT, trigger=TRIG_AFTER_PREV, duration=0.5, delay=1.0)


def build_slide_10(sld: Any) -> None:
    """Slide 10: Three future directions -> switch to 3x6 summary matrix — 4 clicks."""
    add_slide_chrome(sld, 10, "三个发展方向，与一条演进主线", "展望")

    # ---------------- State 1: 3 Direction Cards (x=1.5..11.4, 12.0..21.9, 22.5..32.4; y=3.6..16.2) ----------------
    # Card 1: Trench vs Planar gate
    x1 = 1.5
    d1_parts = [
        add_box(sld, "p10_d1_bg", x1, 3.6, 9.9, 12.4, fill=PANEL_BG, line=PANEL_BORDER, line_pt=0.75, round_cm=0.2),
        add_simple_label(sld, "p10_d1_tag", x1 + 0.45, 3.88, 4.5, 0.74, "方向一 · 器件结构", size=15, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=SIC_COLOR, line=None, round_cm=0.16, word_wrap=False),
        add_simple_label(sld, "p10_d1_hdr", x1 + 0.45, 4.76, 9.0, 0.72, "沟槽栅 vs 平面栅并行", size=20, color=TEXT_MAIN, bold=True),
        # Visual comparison frame
        add_box(sld, "p10_d1_vis", x1 + 0.45, 5.62, 9.0, 5.15, fill=WHITE, line=PANEL_BORDER, line_pt=0.75, round_cm=0.16),
        # Planar (left)
        add_simple_label(sld, "p10_d1_pl_t", x1 + 0.65, 5.72, 4.0, 0.58, "平面栅", size=14, color=TEXT_SUB, bold=True, align=PP_ALIGN_CENTER),
        add_box(sld, "p10_d1_pl_n", x1 + 0.85, 6.82, 3.6, 2.7, fill=N_MINUS, line=WHITE, line_pt=0.75),
        add_box(sld, "p10_d1_pl_p1", x1 + 0.85, 6.82, 1.2, 0.95, fill=P_BODY, line=WHITE, line_pt=0.75),
        add_box(sld, "p10_d1_pl_p2", x1 + 3.25, 6.82, 1.2, 0.95, fill=P_BODY, line=WHITE, line_pt=0.75),
        add_box(sld, "p10_d1_pl_g", x1 + 1.65, 6.38, 2.0, 0.40, fill=GATE_POLY, line=WHITE, line_pt=0.75),
        # Trench (right)
        add_simple_label(sld, "p10_d1_tr_t", x1 + 4.85, 5.72, 4.4, 0.58, "沟槽栅（竖直沟道）", size=14, color=SIC_COLOR, bold=True, align=PP_ALIGN_CENTER, word_wrap=False),
        add_box(sld, "p10_d1_tr_n", x1 + 5.35, 6.82, 3.6, 2.7, fill=N_MINUS, line=WHITE, line_pt=0.75),
        add_box(sld, "p10_d1_tr_p1", x1 + 5.35, 6.82, 1.3, 1.35, fill=P_BODY, line=WHITE, line_pt=0.75),
        add_box(sld, "p10_d1_tr_p2", x1 + 7.65, 6.82, 1.3, 1.35, fill=P_BODY, line=WHITE, line_pt=0.75),
        add_box(sld, "p10_d1_tr_ox", x1 + 6.55, 6.55, 1.2, 2.10, fill=GATE_OX, line=WHITE, line_pt=0.75),
        add_box(sld, "p10_d1_tr_g", x1 + 6.75, 6.55, 0.8, 1.85, fill=GATE_POLY, line=WHITE, line_pt=0.75),
        # Highlighted vertical channels along trench walls
        add_box(sld, "p10_d1_tr_ch1", x1 + 6.40, 6.90, 0.18, 1.25, fill=SIC_COLOR, line=None),
        add_box(sld, "p10_d1_tr_ch2", x1 + 7.72, 6.90, 0.18, 1.25, fill=SIC_COLOR, line=None),
        add_simple_label(sld, "p10_d1_note_c", x1 + 0.6, 9.85, 8.7, 0.65, "元胞更密 · 导通电阻更低", size=14, color=SIC_COLOR, bold=True, align=PP_ALIGN_CENTER, word_wrap=False),
        add_textbox(
            sld,
            "p10_d1_body",
            x1 + 0.45,
            11.05,
            9.0,
            4.5,
            [
                {"runs": [make_run("• 元胞密度 ↑，比导通电阻 ↓", size=18, color=TEXT_MAIN, bold=True)], "space_after": 10},
                {"runs": [make_run("• 芯片面积缩小，降低器件成本", size=18, color=TEXT_MAIN)], "space_after": 10},
                {"runs": [make_run("• 注意：需防止槽底栅氧高电场击穿", size=16, color=COST_COLOR, bold=True)]},
            ],
            valign=MSO_ANCHOR_TOP,
        ),
    ]
    dir_1 = group_shapes(sld, d1_parts, "p10_dir_1")

    # Card 2: Hybrid SiC || Si IGBT
    x2 = 12.0
    d2_parts = [
        add_box(sld, "p10_d2_bg", x2, 3.6, 9.9, 12.4, fill=PANEL_BG, line=PANEL_BORDER, line_pt=0.75, round_cm=0.2),
        add_simple_label(sld, "p10_d2_tag", x2 + 0.45, 3.88, 4.5, 0.74, "方向二 · 模块层面", size=15, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=SIC_COLOR, line=None, round_cm=0.16, word_wrap=False),
        add_simple_label(sld, "p10_d2_hdr", x2 + 0.45, 4.76, 9.0, 0.72, "SiC 与硅 IGBT 混合并联", size=20, color=TEXT_MAIN, bold=True),
        add_box(sld, "p10_d2_vis", x2 + 0.45, 5.62, 9.0, 5.15, fill=WHITE, line=PANEL_BORDER, line_pt=0.75, round_cm=0.16),
        # Parallel schematic
        add_line_seg(sld, "p10_d2_top", x2 + 1.4, 6.20, x2 + 4.1, 6.20, color=TEXT_MAIN, weight_pt=1.5),
        add_line_seg(sld, "p10_d2_bot", x2 + 1.4, 8.85, x2 + 4.1, 8.85, color=TEXT_MAIN, weight_pt=1.5),
        add_line_seg(sld, "p10_d2_l1", x2 + 1.7, 6.20, x2 + 1.7, 8.85, color=SIC_COLOR, weight_pt=1.5),
        add_line_seg(sld, "p10_d2_l2", x2 + 3.8, 6.20, x2 + 3.8, 8.85, color=SI_COLOR, weight_pt=1.5),
        add_simple_label(sld, "p10_d2_sic_b", x2 + 0.9, 6.92, 1.65, 1.20, "SiC\nMOS", size=14, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=SIC_COLOR, line=None, round_cm=0.12),
        add_simple_label(sld, "p10_d2_ig_b", x2 + 3.0, 6.92, 1.65, 1.20, "硅\nIGBT", size=14, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=SI_COLOR, line=None, round_cm=0.12),
        # Area comparison bars
        add_simple_label(sld, "p10_d2_ar_t", x2 + 5.1, 5.85, 4.1, 0.60, "SiC 芯片面积", size=14, color=TEXT_SUB, bold=True),
        add_simple_label(sld, "p10_d2_ar1", x2 + 5.1, 6.62, 3.8, 0.76, "全 SiC = 1", size=14, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=SI_COLOR, line=None, round_cm=0.10),
        add_simple_label(sld, "p10_d2_ar2", x2 + 5.1, 7.68, 1.4, 0.76, "≈1/3", size=14, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=SIC_COLOR, line=None, round_cm=0.10),
        add_simple_label(sld, "p10_d2_ar2t", x2 + 6.65, 7.68, 2.4, 0.76, "混合方案", size=14, color=SIC_COLOR, bold=True),
        add_simple_label(sld, "p10_d2_eff", x2 + 0.7, 9.68, 8.5, 0.78, "CLTC 效率 ≈ 98.7%（与全 SiC 相当）", size=14, color=SIC_COLOR, bold=True, align=PP_ALIGN_CENTER),
        add_textbox(
            sld,
            "p10_d2_body",
            x2 + 0.45,
            11.05,
            9.0,
            4.5,
            [
                {"runs": [make_run("• SiC 承担中小负载与开关过程", size=18, color=TEXT_MAIN, bold=True)], "space_after": 10},
                {"runs": [make_run("• 硅 IGBT 分担稳态大电流", size=18, color=TEXT_MAIN)], "space_after": 10},
                {"runs": [make_run("• 小鹏 X9 公开方案：兼顾效率与成本", size=16, color=TEXT_SUB)]},
            ],
            valign=MSO_ANCHOR_TOP,
        ),
    ]
    dir_2 = group_shapes(sld, d2_parts, "p10_dir_2")

    # Card 3: 1000 V platform evolution
    x3 = 22.5
    d3_parts = [
        add_box(sld, "p10_d3_bg", x3, 3.6, 9.9, 12.4, fill=PANEL_BG, line=PANEL_BORDER, line_pt=0.75, round_cm=0.2),
        add_simple_label(sld, "p10_d3_tag", x3 + 0.45, 3.88, 4.5, 0.74, "方向三 · 系统层面", size=15, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=SIC_COLOR, line=None, round_cm=0.16, word_wrap=False),
        add_simple_label(sld, "p10_d3_hdr", x3 + 0.45, 4.76, 9.0, 0.72, "平台电压向千伏级演进", size=20, color=TEXT_MAIN, bold=True),
        add_box(sld, "p10_d3_vis", x3 + 0.45, 5.62, 9.0, 5.15, fill=WHITE, line=PANEL_BORDER, line_pt=0.75, round_cm=0.16),
        # 3-step staircase
        add_simple_label(sld, "p10_d3_s1", x3 + 0.9, 8.04, 2.5, 1.38, "400 V\n平台", size=14, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=SI_COLOR, line=None, round_cm=0.12, line_spacing=1.05),
        add_box(sld, "p10_d3_s2_bg", x3 + 3.7, 7.12, 2.5, 2.30, fill=SIC_COLOR, line=None, round_cm=0.12, transp=0.30),
        add_simple_label(sld, "p10_d3_s2", x3 + 3.7, 7.12, 2.5, 2.30, "800 V\n平台", size=14, color=WHITE, bold=True, align=PP_ALIGN_CENTER),
        add_simple_label(sld, "p10_d3_s3", x3 + 6.5, 5.95, 2.5, 3.47, "1000 V\n左右", size=14, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=SIC_COLOR, line=None, round_cm=0.12),
        # Device breakdown ratings below steps
        add_simple_label(sld, "p10_d3_r1", x3 + 0.7, 9.65, 2.9, 0.78, "650/750 V", size=14, color=SI_COLOR, bold=True, align=PP_ALIGN_CENTER),
        add_simple_label(sld, "p10_d3_r2", x3 + 3.6, 9.65, 2.7, 0.78, "1200 V", size=14, color=TEXT_MAIN, bold=True, align=PP_ALIGN_CENTER),
        add_simple_label(sld, "p10_d3_r3", x3 + 6.4, 9.65, 2.8, 0.78, "1500 V+", size=14, color=SIC_COLOR, bold=True, align=PP_ALIGN_CENTER),
        add_textbox(
            sld,
            "p10_d3_body",
            x3 + 0.45,
            11.05,
            9.0,
            4.5,
            [
                {"runs": [make_run("• 整车母线向 1000 V 左右升级", size=18, color=TEXT_MAIN, bold=True)], "space_after": 10},
                {"runs": [make_run("• 对应器件耐压提升至 1500 V 以上", size=18, color=TEXT_MAIN)], "space_after": 10},
                {"runs": [make_run("• 比亚迪千伏平台已采用 1500 V 级 SiC 器件", size=16, color=TEXT_SUB)]},
            ],
            valign=MSO_ANCHOR_TOP,
        ),
    ]
    dir_3 = group_shapes(sld, d3_parts, "p10_dir_3")

    # ---------------- State 2: 3x6 Summary Matrix (replaces dir cards on Click 4) ----------------
    # Cols: 器件 (4.0), ①耐压 (4.8), ②导通 (5.7), ③开关 (5.0), ④续流 (5.1), 新代价 (6.3) -> total = 30.9 cm
    col_w = [4.0, 4.8, 5.7, 5.0, 5.1, 6.3]
    col_xs = [1.5]
    for w_c in col_w[:-1]:
        col_xs.append(col_xs[-1] + w_c)

    mat_hdr = add_table_row_group(
        sld,
        "p10_mat_hdr",
        1.5,
        3.65,
        col_w,
        1.20,
        [
            [make_run("器件路线", size=16, color=WHITE, bold=True)],
            [make_run("① 耐压", size=16, color=WHITE, bold=True)],
            [make_run("② 导通损耗", size=16, color=WHITE, bold=True)],
            [make_run("③ 开关损耗", size=16, color=WHITE, bold=True)],
            [make_run("④ 续流与 Q", size=16, color=WHITE, bold=True), make_run("rr", size=16, color=WHITE, bold=True, sub=True)],
            [make_run("核心代价", size=16, color=WHITE, bold=True)],
        ],
        default_fill=TEXT_MAIN,
        border_color=WHITE,
        aligns=[PP_ALIGN_CENTER] * 6,
    )

    def make_matrix_row(r_idx: int, y_row: float, dev_name: str, dev_color: str, dev_bg: str, cells_spec: list[tuple[str | None, str]]) -> Any:
        row_h = 2.95
        parts = []
        # Col 0: Device name
        parts.append(
            add_simple_label(
                sld,
                f"p10_m{r_idx}_c0",
                col_xs[0],
                y_row,
                col_w[0],
                row_h,
                dev_name,
                size=18,
                color=dev_color,
                bold=True,
                align=PP_ALIGN_CENTER,
                fill=dev_bg,
                line=PANEL_BORDER,
                line_pt=0.75,
            )
        )
        for c_i, (dot_col, txt_spec) in enumerate(cells_spec, start=1):
            cx = col_xs[c_i]
            cw = col_w[c_i]
            is_cost = c_i == 5 and txt_spec != "—"
            cell_bg = COST_LIGHT if is_cost else WHITE
            cell_box = add_box(sld, f"p10_m{r_idx}_c{c_i}_bg", cx, y_row, cw, row_h, fill=cell_bg, line=PANEL_BORDER, line_pt=0.75)
            parts.append(cell_box)
            if dot_col is not None:
                parts.append(add_oval(sld, f"p10_m{r_idx}_c{c_i}_dot", cx + 0.42, y_row + row_h / 2.0, 0.34, fill=dot_col, line=None))
                tx_x, tx_w = cx + 0.72, cw - 0.85
                al = PP_ALIGN_LEFT
            else:
                tx_x, tx_w = cx + 0.12, cw - 0.24
                al = PP_ALIGN_CENTER if txt_spec == "—" else PP_ALIGN_LEFT
            if isinstance(txt_spec, list):
                runs = txt_spec
            else:
                runs = [make_run(txt_spec, size=16, color=COST_COLOR if is_cost else TEXT_MAIN, bold=is_cost)]
            parts.append(
                add_textbox(
                    sld,
                    f"p10_m{r_idx}_c{c_i}_txt",
                    tx_x,
                    y_row + 0.15,
                    tx_w,
                    row_h - 0.30,
                    [{"runs": runs, "align": al}],
                    align=al,
                    valign=MSO_ANCHOR_MIDDLE,
                )
            )
        return group_shapes(sld, parts, f"p10_mat_row_{r_idx}")

    # Dot semantics: SIC_COLOR = 满足, AMBER = 折中, COST_COLOR = 不足
    mat_row_1 = make_matrix_row(
        1,
        4.85,
        "硅\nMOSFET",
        TEXT_SUB,
        PANEL_BG,
        [
            (AMBER, "漂移区厚"),
            (COST_COLOR, "随耐压急增"),
            (SIC_COLOR, "开关快"),
            (None, "—"),
            (None, "—"),
        ],
    )
    mat_row_2 = make_matrix_row(
        2,
        7.80,
        "硅\nIGBT",
        SI_COLOR,
        SI_LIGHT,
        [
            (SIC_COLOR, "1200 V 可做"),
            (AMBER, "大流低、轻载 0.7 V"),
            (COST_COLOR, "拖尾，约 10 kHz"),
            (COST_COLOR, "需 FRD，反向恢复大"),
            (None, "拖尾电流\n需外并 FRD"),
        ],
    )
    mat_row_3 = make_matrix_row(
        3,
        10.75,
        "4H-SiC\nMOSFET",
        SIC_COLOR,
        SIC_LIGHT,
        [
            (SIC_COLOR, "漂移区薄 1/10"),
            (SIC_COLOR, "过原点电阻"),
            (
                SIC_COLOR,
                [
                    make_run("E", size=16, color=TEXT_MAIN, italic=True, font=FONT_MATH),
                    make_run("off", size=16, color=TEXT_MAIN, font=FONT_MATH, sub=True),
                    make_run(" −85%", size=16, color=TEXT_MAIN),
                ],
            ),
            (SIC_COLOR, "同步整流 + SBD"),
            (None, "过冲/误导通 · 体二极管\n热与短路 · 长晶成本"),
        ],
    )

    # Legend + Core Takeaway bar below matrix
    mat_takeaway = add_textbox(
        sld,
        "p10_mat_takeaway",
        1.5,
        14.15,
        30.9,
        3.25,
        [
            {
                "runs": [
                    make_run("图例：", size=15, color=TEXT_SUB, bold=True),
                    make_run("● 满足", size=15, color=SIC_COLOR, bold=True),
                    make_run("　　", size=15, color=TEXT_SUB),
                    make_run("● 折中", size=15, color=AMBER, bold=True),
                    make_run("　　", size=15, color=TEXT_SUB),
                    make_run("● 不足", size=15, color=COST_COLOR, bold=True),
                ],
                "align": PP_ALIGN_LEFT,
                "space_after": 8,
            },
            {
                "runs": [
                    make_run("演进主线：", size=18, color=SIC_COLOR, bold=True),
                    make_run("围绕耐压、导通、开关和续流四项要求，不断解决旧矛盾，同时承担新代价。", size=18, color=TEXT_MAIN, bold=True),
                ],
                "align": PP_ALIGN_LEFT,
            },
        ],
        fill=PANEL_BG,
        line=PANEL_BORDER,
        line_pt=0.75,
        round_cm=0.2,
        margin_cm=(0.45, 0.45, 0.25, 0.25),
    )

    # ---------------- Animations: Exact 4 Clicks ----------------
    # Clicks 1-3: 3 direction cards fade in
    anim_fade(sld, dir_1, trigger=TRIG_CLICK, duration=0.4)
    anim_fade(sld, dir_2, trigger=TRIG_CLICK, duration=0.4)
    anim_fade(sld, dir_3, trigger=TRIG_CLICK, duration=0.4)

    # Click 4: Cards fade out; Matrix fades in row by row top-to-bottom + takeaway
    anim_exit_fade(sld, dir_1, trigger=TRIG_CLICK, duration=0.35)
    anim_exit_fade(sld, dir_2, trigger=TRIG_WITH_PREV, duration=0.35)
    anim_exit_fade(sld, dir_3, trigger=TRIG_WITH_PREV, duration=0.35)
    anim_fade(sld, mat_hdr, trigger=TRIG_WITH_PREV, duration=0.4)
    anim_fade(sld, mat_row_1, trigger=TRIG_AFTER_PREV, duration=0.4)
    anim_fade(sld, mat_row_2, trigger=TRIG_AFTER_PREV, duration=0.4)
    anim_fade(sld, mat_row_3, trigger=TRIG_AFTER_PREV, duration=0.4)
    anim_fade(sld, mat_takeaway, trigger=TRIG_AFTER_PREV, duration=0.4)
