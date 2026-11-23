"""Slide builders for Slides 1 through 5."""

from __future__ import annotations

import math
import pathlib
from typing import Any

from ppt_helpers import (
    AMBER,
    AMBER_LIGHT,
    COST_COLOR,
    COST_LIGHT,
    FONT_MATH,
    FONT_UI,
    MSO_ANCHOR_MIDDLE,
    MSO_ANCHOR_TOP,
    MSO_ANIM_DIR_BOTTOM,
    MSO_ANIM_DIR_LEFT,
    MSO_LINE_DASH,
    MSO_SHAPE_OVAL,
    MSO_SHAPE_RIGHT_ARROW,
    PANEL_BG,
    PANEL_BORDER,
    PP_ALIGN_CENTER,
    PP_ALIGN_LEFT,
    PP_ALIGN_RIGHT,
    PP_EFFECT_FADE_SMOOTHLY,
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
    add_line_seg,
    add_oval,
    add_polyline,
    add_req_badge,
    add_simple_label,
    add_slide_chrome,
    add_table_row_group,
    add_textbox,
    anim_appear,
    anim_fade,
    anim_media_play,
    anim_pulse,
    anim_wipe,
    clean_shape,
    cm,
    CM_TO_PT,
    group_shapes,
    make_run,
    rgb,
    set_slide_white_bg,
)

CLIPS_DIR = pathlib.Path(r"c:\Users\Casper\Documents\Proj\manim_videos\clips")


def build_slide_1(sld: Any) -> None:
    """Slide 1: Cover — 0 clicks."""
    set_slide_white_bg(sld)

    # Kicker pill
    add_simple_label(
        sld,
        "p1_kicker_1",
        1.5,
        1.65,
        8.6,
        0.72,
        "课堂专题汇报 · 电气 / 微电子方向",
        size=14,
        color=SIC_COLOR,
        bold=True,
        align=PP_ALIGN_CENTER,
        fill=SIC_LIGHT,
        line=SIC_COLOR,
        line_pt=0.75,
        round_cm=0.36,
    )

    # Main Title
    add_simple_label(
        sld,
        "p1_title_1",
        1.5,
        2.75,
        15.8,
        3.9,
        "先进半导体器件在\n新能源汽车主驱逆变器\n中的应用",
        size=32,
        color=TEXT_MAIN,
        bold=True,
        align=PP_ALIGN_LEFT,
        valign=MSO_ANCHOR_TOP,
        margin_cm=(0.0, 0.1, 0.0, 0.0),
        line_spacing=1.20,
    )

    # Subtitle
    add_simple_label(
        sld,
        "p1_subtitle_1",
        1.5,
        7.55,
        15.5,
        2.2,
        "从 H 桥换流与 PWM 调制出发，围绕耐压、导通、开关、续流四项核心要求，对比硅 IGBT 与 4H-SiC MOSFET 的技术演进与新代价。",
        size=18,
        color=TEXT_SUB,
        align=PP_ALIGN_LEFT,
        valign=MSO_ANCHOR_TOP,
        margin_cm=(0.0, 0.1, 0.0, 0.0),
        line_spacing=1.30,
    )

    # Presenter / Meta strip
    add_line_seg(sld, "p1_meta_rule", 1.5, 10.45, 16.5, 10.45, color=PANEL_BORDER, weight_pt=0.75)
    add_textbox(
        sld,
        "p1_meta_1",
        1.5,
        10.75,
        15.2,
        1.5,
        [
            {"runs": [make_run("汇报人：【待补】　　学号 / 班级：【待补】", size=16, color=TEXT_MAIN, bold=True)], "space_after": 6},
            {"runs": [make_run("汇报时长：约 14 分钟　·　共 10 页", size=15, color=TEXT_SUB)]},
        ],
        align=PP_ALIGN_LEFT,
        valign=MSO_ANCHOR_TOP,
        margin_cm=(0.0, 0.0, 0.0, 0.0),
    )

    # Right schematic panel: Battery -> Inverter -> Motor (x 17.8..32.4, y 1.65..12.35)
    add_box(sld, "p1_diag_panel", 17.8, 1.65, 14.6, 10.7, fill=PANEL_BG, line=PANEL_BORDER, line_pt=0.75, round_cm=0.25)
    add_simple_label(
        sld,
        "p1_diag_hdr",
        18.3,
        1.90,
        13.6,
        0.70,
        "核心能量变换链路示意",
        size=15,
        color=TEXT_SUB,
        bold=True,
        align=PP_ALIGN_LEFT,
    )

    # 1) Battery block
    add_box(sld, "p1_bat_box", 18.1, 4.15, 3.45, 4.9, fill=WHITE, line=SI_COLOR, line_pt=1.5, round_cm=0.2)
    # Battery icon bars inside
    add_line_seg(sld, "p1_bat_lead_t", 19.82, 4.70, 19.82, 5.25, color=SI_COLOR, weight_pt=1.75)
    add_line_seg(sld, "p1_bat_p1", 19.12, 5.25, 20.52, 5.25, color=SI_COLOR, weight_pt=2.5)
    add_line_seg(sld, "p1_bat_n1", 19.42, 5.60, 20.22, 5.60, color=SI_COLOR, weight_pt=4.0)
    add_line_seg(sld, "p1_bat_p2", 19.12, 5.95, 20.52, 5.95, color=SI_COLOR, weight_pt=2.5)
    add_line_seg(sld, "p1_bat_n2", 19.42, 6.30, 20.22, 6.30, color=SI_COLOR, weight_pt=4.0)
    add_line_seg(sld, "p1_bat_lead_b", 19.82, 6.30, 19.82, 6.85, color=SI_COLOR, weight_pt=1.75)
    add_simple_label(sld, "p1_bat_lbl1", 18.15, 7.10, 3.35, 0.72, "动力电池", size=16, color=TEXT_MAIN, bold=True, align=PP_ALIGN_CENTER)
    add_simple_label(sld, "p1_bat_lbl2", 18.15, 7.82, 3.35, 0.72, "400/800 V DC", size=14, color=TEXT_SUB, align=PP_ALIGN_CENTER, word_wrap=False)

    # Arrow Battery -> Inverter
    add_line_seg(sld, "p1_arr_1a", 21.60, 6.00, 22.40, 6.00, color=TEXT_MAIN, weight_pt=2.5, arrow_end=True)
    add_line_seg(sld, "p1_arr_1b", 21.60, 7.30, 22.40, 7.30, color=TEXT_MAIN, weight_pt=2.5, arrow_end=True)
    add_simple_label(sld, "p1_dc_tag", 21.45, 5.05, 1.10, 0.68, "DC", size=14, color=SI_COLOR, bold=True, align=PP_ALIGN_CENTER, word_wrap=False)

    # 2) Inverter block (highlighted)
    add_box(sld, "p1_inv_box", 22.45, 3.45, 3.95, 6.3, fill=WHITE, line=SIC_COLOR, line_pt=2.0, round_cm=0.22)
    add_simple_label(
        sld, "p1_inv_top_tag", 22.65, 3.70, 3.55, 0.78, "主驱逆变器", size=16, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=SIC_COLOR, line=None, round_cm=0.16, word_wrap=False
    )
    # 3-phase bridge mini wireframe inside inverter box
    add_line_seg(sld, "p1_inv_rail_t", 22.90, 4.90, 25.95, 4.90, color=TEXT_MAIN, weight_pt=1.5)
    add_line_seg(sld, "p1_inv_rail_b", 22.90, 7.90, 25.95, 7.90, color=TEXT_MAIN, weight_pt=1.5)
    for leg_i, lx in enumerate((23.40, 24.42, 25.45), start=1):
        add_line_seg(sld, f"p1_inv_leg_{leg_i}", lx, 4.90, lx, 7.90, color=TEXT_SUB, weight_pt=1.2)
        add_box(sld, f"p1_inv_sw_u{leg_i}", lx - 0.24, 5.35, 0.48, 0.72, fill=SI_LIGHT, line=SI_COLOR, line_pt=1.2, round_cm=0.06)
        add_box(sld, f"p1_inv_sw_d{leg_i}", lx - 0.24, 6.73, 0.48, 0.72, fill=SIC_LIGHT, line=SIC_COLOR, line_pt=1.2, round_cm=0.06)
    add_simple_label(sld, "p1_inv_sub", 22.55, 8.20, 3.75, 1.3, "6 开关管器件\n高频斩波调制", size=14, color=TEXT_MAIN, align=PP_ALIGN_CENTER)

    # 3-phase arrows Inverter -> Motor
    for idx, yy in enumerate((5.85, 6.65, 7.45), start=1):
        add_line_seg(sld, f"p1_arr_2_{idx}", 26.45, yy, 28.25, yy, color=SIC_COLOR, weight_pt=2.2, arrow_end=True)
    add_simple_label(sld, "p1_ac_tag", 26.52, 4.92, 1.65, 0.68, "3φ AC", size=14, color=SIC_COLOR, bold=True, align=PP_ALIGN_CENTER, word_wrap=False)

    # 3) PMSM Motor block
    add_box(sld, "p1_mot_box", 28.3, 4.15, 3.7, 4.9, fill=WHITE, line=TEXT_MAIN, line_pt=1.5, round_cm=0.2)
    add_oval(sld, "p1_mot_circle", 30.15, 5.80, 1.85, fill=SIC_LIGHT, line=SIC_COLOR, line_pt=2.0)
    add_simple_label(sld, "p1_mot_m", 29.22, 4.88, 1.85, 1.85, "M", size=22, color=SIC_COLOR, bold=True, align=PP_ALIGN_CENTER)
    add_simple_label(sld, "p1_mot_lbl1", 28.35, 7.10, 3.6, 0.72, "永磁同步电机", size=15, color=TEXT_MAIN, bold=True, align=PP_ALIGN_CENTER, word_wrap=False)
    add_simple_label(sld, "p1_mot_lbl2", 28.35, 7.82, 3.6, 0.72, "100–300 kW", size=14, color=TEXT_SUB, align=PP_ALIGN_CENTER, word_wrap=False)

    # Semantic color preview strip inside right panel bottom
    add_box(sld, "p1_sem_strip", 18.2, 10.35, 13.8, 1.45, fill=WHITE, line=PANEL_BORDER, line_pt=0.75, round_cm=0.15)
    add_oval(sld, "p1_sem_dot_si", 19.0, 11.08, 0.36, fill=SI_COLOR, line=None)
    add_simple_label(sld, "p1_sem_txt_si", 19.35, 10.72, 3.4, 0.72, "硅 / IGBT", size=14, color=SI_COLOR, bold=True)
    add_oval(sld, "p1_sem_dot_sic", 23.2, 11.08, 0.36, fill=SIC_COLOR, line=None)
    add_simple_label(sld, "p1_sem_txt_sic", 23.55, 10.72, 3.8, 0.72, "4H-SiC", size=14, color=SIC_COLOR, bold=True)
    add_oval(sld, "p1_sem_dot_cost", 27.5, 11.08, 0.36, fill=COST_COLOR, line=None)
    add_simple_label(sld, "p1_sem_txt_cost", 27.85, 10.72, 3.6, 0.72, "代价与挑战", size=14, color=COST_COLOR, bold=True)

    # Bottom 5-segment report roadmap (x 1.5..32.4, y 14.0..17.2)
    add_simple_label(sld, "p1_road_hdr", 1.5, 13.10, 10.0, 0.75, "汇报路线（5 部分）", size=16, color=TEXT_SUB, bold=True)
    road_items = [
        ("01 原理", "系统框图 · H 桥 · PWM", TEXT_MAIN, WHITE),
        ("02 要求", "耐压 · 导通 · 开关 · 续流", TEXT_MAIN, WHITE),
        ("03 硅 IGBT", "电导调制与三项代价", SI_COLOR, SI_LIGHT),
        ("04 4H-SiC", "材料优势 · 性能 · 新代价", SIC_COLOR, SIC_LIGHT),
        ("05 展望", "沟槽 · 混合并联 · 千伏平台", TEXT_MAIN, PANEL_BG),
    ]
    card_w = 5.7
    gap = (30.9 - 5 * card_w) / 4.0  # 0.6 cm
    for idx, (r_title, r_sub, accent, bg) in enumerate(road_items):
        rx = 1.5 + idx * (card_w + gap)
        add_box(sld, f"p1_road_card_{idx + 1}", rx, 14.05, card_w, 2.95, fill=bg, line=accent, line_pt=1.25, round_cm=0.2)
        add_simple_label(
            sld, f"p1_road_tag_{idx + 1}", rx + 0.3, 14.32, 3.10, 0.76, r_title, size=15, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=accent, line=None, round_cm=0.18, word_wrap=False
        )
        add_simple_label(sld, f"p1_road_s_{idx + 1}", rx + 0.30, 15.32, card_w - 0.60, 1.45, r_sub, size=14, color=TEXT_MAIN, align=PP_ALIGN_LEFT, valign=MSO_ANCHOR_TOP)
        if idx < 4:
            add_line_seg(sld, f"p1_road_arr_{idx + 1}", rx + card_w + 0.08, 15.52, rx + card_w + gap - 0.08, 15.52, color=TEXT_SUB, weight_pt=1.75, arrow_end=True)

    add_simple_label(sld, "p1_pagenum_1", 29.4, 18.20, 3.0, 0.55, "01 / 10", size=12, color=TEXT_SUB, align=PP_ALIGN_RIGHT)


def build_slide_2(sld: Any) -> None:
    """Slide 2: Inverter power + control topology & linear vs switch mode — 3 clicks."""
    add_slide_chrome(sld, 2, "逆变器用开关态，把直流电变成可控的三相交流", "原理")

    # Static layout frames
    add_box(sld, "p2_top_panel", 1.5, 3.30, 30.9, 8.95, fill=PANEL_BG, line=PANEL_BORDER, line_pt=0.75, round_cm=0.2)
    add_simple_label(sld, "p2_pwr_hdr", 1.9, 3.42, 8.5, 0.68, "功率流（100–300 kW）", size=15, color=TEXT_MAIN, bold=True)
    add_simple_label(sld, "p2_ctl_hdr", 1.9, 7.52, 8.5, 0.68, "控制与采样反馈（FOC）", size=15, color=TEXT_SUB, bold=True)

    add_box(sld, "p2_bot_left_frame", 1.5, 12.60, 13.2, 5.20, fill=PANEL_BG, line=PANEL_BORDER, line_pt=0.75, round_cm=0.2)
    add_simple_label(sld, "p2_bot_left_hdr", 1.9, 12.74, 12.4, 0.72, "电流三要素 → 电机运行状态", size=16, color=TEXT_MAIN, bold=True)

    add_box(sld, "p2_bot_right_frame", 15.3, 12.60, 17.1, 5.20, fill=PANEL_BG, line=PANEL_BORDER, line_pt=0.75, round_cm=0.2)
    add_simple_label(sld, "p2_bot_right_hdr", 15.7, 12.74, 16.3, 0.72, "器件工作状态对比：为何只用开关态？", size=16, color=TEXT_MAIN, bold=True)

    # --- Click 1 objects: 6 power-flow blocks + 5 thick arrows ---
    blocks_spec = [
        ("动力电池", "400 V / 800 V 直流", 1.95, 4.10, WHITE, TEXT_MAIN, TEXT_MAIN, TEXT_SUB),
        ("母线电容", "稳压 · 吸收纹波", 7.15, 3.70, WHITE, TEXT_MAIN, TEXT_MAIN, TEXT_SUB),
        ("逆变器", "六个开关管（DC → 3φ AC）", 11.95, 5.10, SI_COLOR, SI_COLOR, WHITE, "#E2E8F0"),
        ("永磁同步电机", "定子旋转磁场", 18.15, 4.40, WHITE, SIC_COLOR, TEXT_MAIN, TEXT_SUB),
        ("减速器", "减速增扭", 23.65, 3.35, WHITE, TEXT_MAIN, TEXT_MAIN, TEXT_SUB),
        ("车轮", "驱动行驶", 28.10, 3.85, WHITE, TEXT_MAIN, TEXT_MAIN, TEXT_SUB),
    ]
    power_objs: list[tuple[str, Any]] = []
    box_edges: list[tuple[float, float]] = []
    for idx, (title, sub, bx, bw, bg, ln, tcol, scol) in enumerate(blocks_spec, start=1):
        shp = add_textbox(
            sld,
            f"p2_pwr_box_{idx}",
            bx,
            4.25,
            bw,
            2.45,
            [
                {"runs": [make_run(title, size=18, color=tcol, bold=True)], "align": PP_ALIGN_CENTER, "space_after": 4},
                {"runs": [make_run(sub, size=14, color=scol)], "align": PP_ALIGN_CENTER},
            ],
            align=PP_ALIGN_CENTER,
            valign=MSO_ANCHOR_MIDDLE,
            fill=bg,
            line=ln,
            line_pt=1.75 if idx == 3 else 1.25,
            round_cm=0.2,
            margin_cm=(0.10, 0.10, 0.08, 0.08),
        )
        power_objs.append(("box", shp))
        box_edges.append((bx, bx + bw))

    arrows: list[Any] = []
    for idx in range(5):
        x_start = box_edges[idx][1] + 0.08
        x_end = box_edges[idx + 1][0] - 0.08
        arr = add_line_seg(sld, f"p2_pwr_arr_{idx + 1}", x_start, 5.48, x_end, 5.48, color=TEXT_MAIN, weight_pt=3.0, arrow_end=True)
        arrows.append(arr)

    # Interleave box & arrow wipes in left-to-right flow
    for idx in range(6):
        trig = TRIG_CLICK if idx == 0 else TRIG_AFTER_PREV
        anim_wipe(sld, power_objs[idx][1], direction=MSO_ANIM_DIR_LEFT, trigger=trig, duration=0.35)
        if idx < 5:
            anim_wipe(sld, arrows[idx], direction=MSO_ANIM_DIR_LEFT, trigger=TRIG_AFTER_PREV, duration=0.25)

    # --- Click 2 objects: Control chain + feedback dashed lines ---
    ctl_parts: list[Any] = []
    ctl_parts.append(
        add_textbox(
            sld,
            "p2_ctl_cmd",
            2.0,
            8.45,
            3.3,
            1.45,
            [{"runs": [make_run("扭矩指令", size=16, color=TEXT_MAIN, bold=True)], "align": PP_ALIGN_CENTER}],
            fill=WHITE,
            line=TEXT_SUB,
            line_pt=1.0,
            round_cm=0.18,
        )
    )
    ctl_parts.append(
        add_textbox(
            sld,
            "p2_ctl_mcu",
            6.5,
            8.35,
            4.2,
            1.65,
            [
                {"runs": [make_run("主控芯片", size=16, color=TEXT_MAIN, bold=True)], "align": PP_ALIGN_CENTER, "space_after": 2},
                {"runs": [make_run("FOC + PWM", size=14, color=SIC_COLOR, bold=True)], "align": PP_ALIGN_CENTER},
            ],
            fill=WHITE,
            line=SIC_COLOR,
            line_pt=1.25,
            round_cm=0.18,
        )
    )
    ctl_parts.append(
        add_textbox(
            sld,
            "p2_ctl_drv",
            11.95,
            8.45,
            3.3,
            1.45,
            [
                {"runs": [make_run("隔离驱动", size=16, color=TEXT_MAIN, bold=True)], "align": PP_ALIGN_CENTER, "space_after": 2},
                {"runs": [make_run("6 路通断时序", size=14, color=TEXT_SUB)], "align": PP_ALIGN_CENTER},
            ],
            fill=WHITE,
            line=SI_COLOR,
            line_pt=1.25,
            round_cm=0.18,
        )
    )
    # Dashed control arrows
    ctl_parts.append(add_line_seg(sld, "p2_ctl_arr1", 5.35, 9.18, 6.45, 9.18, color=TEXT_MAIN, weight_pt=1.75, dash=MSO_LINE_DASH, arrow_end=True))
    ctl_parts.append(add_line_seg(sld, "p2_ctl_arr2", 10.75, 9.18, 11.90, 9.18, color=TEXT_MAIN, weight_pt=1.75, dash=MSO_LINE_DASH, arrow_end=True))
    ctl_parts.append(add_line_seg(sld, "p2_ctl_arr3", 13.60, 8.40, 13.60, 6.75, color=SI_COLOR, weight_pt=2.0, dash=MSO_LINE_DASH, arrow_end=True))
    ctl_parts.append(add_simple_label(sld, "p2_ctl_up_lbl", 13.80, 7.15, 3.8, 0.65, "PWM 驱动信号", size=14, color=SI_COLOR, bold=True, word_wrap=False))

    # Feedback paths from Bus Cap (x=9.0, y=6.7) and Motor (x=20.35, y=6.7) back to MCU
    ctl_parts.append(add_polyline(sld, "p2_fb_vdc", [(9.0, 6.75), (9.0, 8.30)], color=TEXT_SUB, weight_pt=1.5, dash=MSO_LINE_DASH, arrow_end=True))
    ctl_parts.append(add_simple_label(sld, "p2_fb_vdc_lbl", 9.15, 7.15, 2.8, 0.65, "母线电压", size=14, color=TEXT_SUB, word_wrap=False))

    ctl_parts.append(
        add_polyline(
            sld,
            "p2_fb_mot",
            [(20.35, 6.75), (20.35, 11.40), (8.60, 11.40), (8.60, 10.05)],
            color=TEXT_SUB,
            weight_pt=1.5,
            dash=MSO_LINE_DASH,
            arrow_end=True,
        )
    )
    ctl_parts.append(
        add_simple_label(
            sld,
            "p2_fb_mot_lbl",
            10.8,
            10.98,
            8.0,
            0.68,
            "采样反馈：相电流、转子位置",
            size=14,
            color=TEXT_SUB,
            align=PP_ALIGN_CENTER,
            fill=PANEL_BG,
            line=None,
            word_wrap=False,
        )
    )
    ctl_grp = group_shapes(sld, ctl_parts, "p2_ctl_grp_1")
    anim_fade(sld, ctl_grp, trigger=TRIG_CLICK, duration=0.45)

    # --- Click 3 objects: Bottom-left table & Bottom-right V-I comparison ---
    row_specs = [
        ("基波频率", "→", "电机转速", "n = 60f / p"),
        ("电流幅值", "→", "电磁扭矩", "幅值 ↑ 扭矩 ↑"),
        ("电流相位（夹角）", "→", "电磁扭矩", "FOC 定向控制"),
    ]
    tbl_rows = []
    for r_i, (c1, c2, c3, c4) in enumerate(row_specs, start=1):
        row = add_table_row_group(
            sld,
            f"p2_tbl_row_{r_i}",
            1.9,
            13.55 + (r_i - 1) * 1.28,
            [4.5, 0.9, 3.2, 3.8],
            1.16,
            [
                [make_run(c1, size=16, color=TEXT_MAIN, bold=True)],
                [make_run(c2, size=16, color=SIC_COLOR, bold=True)],
                [make_run(c3, size=16, color=SIC_COLOR, bold=True)],
                [make_run(c4, size=14, color=TEXT_SUB)],
            ],
            aligns=[PP_ALIGN_LEFT, PP_ALIGN_CENTER, PP_ALIGN_LEFT, PP_ALIGN_LEFT],
            margin_cm=(0.14, 0.10, 0.02, 0.02),
        )
        tbl_rows.append(row)
    bot_left_grp = group_shapes(sld, tbl_rows, "p2_bot_left_1")

    # Right V-I subplots (x=15.7..32.0, y=13.45..17.65)
    vi_parts: list[Any] = []
    # Subplot A: Linear active region
    ax_a_x, ax_a_y, ax_w, ax_h = 16.4, 16.62, 6.2, 2.22
    vi_parts.append(add_simple_label(sld, "p2_vi_a_t", 15.7, 13.42, 7.5, 0.65, "线性放大区（同时承高压与大流）", size=14, color=COST_COLOR, bold=True, align=PP_ALIGN_CENTER))
    vi_parts.append(add_box(sld, "p2_vi_a_rect", ax_a_x + 0.5, ax_a_y - 1.82, 4.5, 1.35, fill=COST_COLOR, line=COST_COLOR, line_pt=1.25, transp=0.65))
    vi_parts.append(add_line_seg(sld, "p2_vi_a_y", ax_a_x, ax_a_y, ax_a_x, ax_a_y - ax_h, color=TEXT_MAIN, weight_pt=1.25, arrow_end=True))
    vi_parts.append(add_line_seg(sld, "p2_vi_a_x", ax_a_x, ax_a_y, ax_a_x + ax_w, ax_a_y, color=TEXT_MAIN, weight_pt=1.25, arrow_end=True))
    vi_parts.append(add_simple_label(sld, "p2_vi_a_ilbl", ax_a_x - 0.55, ax_a_y - ax_h, 0.5, 0.55, "I", size=14, color=TEXT_MAIN, italic=True, font=FONT_MATH, align=PP_ALIGN_RIGHT))
    vi_parts.append(add_simple_label(sld, "p2_vi_a_vlbl", ax_a_x + ax_w - 0.4, ax_a_y + 0.02, 0.6, 0.55, "V", size=14, color=TEXT_MAIN, italic=True, font=FONT_MATH))
    vi_parts.append(add_simple_label(sld, "p2_vi_a_in", ax_a_x + 0.65, ax_a_y - 1.75, 4.2, 1.25, "P = V · I\n数十千瓦（烧毁）", size=14, color=COST_COLOR, bold=True, align=PP_ALIGN_CENTER))
    vi_parts.append(add_simple_label(sld, "p2_vi_a_foot", 16.0, 17.02, 7.0, 0.68, "功耗极高 ✗", size=16, color=COST_COLOR, bold=True, align=PP_ALIGN_CENTER))

    # Subplot B: Switch mode
    ax_b_x = 24.8
    vi_parts.append(add_simple_label(sld, "p2_vi_b_t", 24.0, 13.42, 7.8, 0.65, "开关态（只用导通 / 关断两端）", size=14, color=SIC_COLOR, bold=True, align=PP_ALIGN_CENTER))
    vi_parts.append(add_box(sld, "p2_vi_b_on", ax_b_x, ax_a_y - 1.95, 0.36, 1.95, fill=SIC_COLOR, line=SIC_COLOR, line_pt=1.0, transp=0.35))
    vi_parts.append(add_box(sld, "p2_vi_b_off", ax_b_x, ax_a_y - 0.30, 5.20, 0.30, fill=SIC_COLOR, line=SIC_COLOR, line_pt=1.0, transp=0.35))
    vi_parts.append(add_line_seg(sld, "p2_vi_b_y", ax_b_x, ax_a_y, ax_b_x, ax_a_y - ax_h, color=TEXT_MAIN, weight_pt=1.25, arrow_end=True))
    vi_parts.append(add_line_seg(sld, "p2_vi_b_x", ax_b_x, ax_a_y, ax_b_x + ax_w, ax_a_y, color=TEXT_MAIN, weight_pt=1.25, arrow_end=True))
    vi_parts.append(add_simple_label(sld, "p2_vi_b_ilbl", ax_b_x - 0.55, ax_a_y - ax_h, 0.5, 0.55, "I", size=14, color=TEXT_MAIN, italic=True, font=FONT_MATH, align=PP_ALIGN_RIGHT))
    vi_parts.append(add_simple_label(sld, "p2_vi_b_vlbl", ax_b_x + ax_w - 0.4, ax_a_y + 0.02, 0.6, 0.55, "V", size=14, color=TEXT_MAIN, italic=True, font=FONT_MATH))
    vi_parts.append(add_simple_label(sld, "p2_vi_b_lbl1", ax_b_x + 0.55, ax_a_y - 1.95, 4.2, 0.65, "导通态：V ≈ 0", size=14, color=SIC_COLOR, bold=True))
    vi_parts.append(add_simple_label(sld, "p2_vi_b_lbl2", ax_b_x + 1.85, ax_a_y - 1.05, 4.2, 0.65, "关断态：I ≈ 0", size=14, color=SIC_COLOR, bold=True))
    vi_parts.append(add_simple_label(sld, "p2_vi_b_foot", 24.4, 17.02, 7.0, 0.68, "功耗很小 ✓", size=16, color=SIC_COLOR, bold=True, align=PP_ALIGN_CENTER))

    bot_right_grp = group_shapes(sld, vi_parts, "p2_bot_right_1")

    anim_fade(sld, bot_left_grp, trigger=TRIG_CLICK, duration=0.4)
    anim_fade(sld, bot_right_grp, trigger=TRIG_WITH_PREV, duration=0.4)


def _add_video_clips(sld: Any, page_num: int, prefix: str) -> list[Any]:
    """Embed 4 seamless 1080p60 MP4 clips at exact same position, clearing auto InteractiveSequences."""
    clips = []
    # Slight hairline frame behind video
    add_box(sld, f"p{page_num}_vid_frame", 1.48, 3.38, 24.04, 13.54, fill=WHITE, line=PANEL_BORDER, line_pt=0.75)
    for i in range(1, 5):
        clip_path = str(CLIPS_DIR / f"{prefix}_clip{i}.mp4")
        vid = sld.Shapes.AddMediaObject2(clip_path, 0, -1, cm(1.5), cm(3.4), cm(24.0), cm(13.5))
        clean_shape(vid)
        vid.Name = f"p{page_num}_vid_{i}"
        vid.MediaFormat.Muted = -1
        clips.append(vid)

    # Clear automatic click-on-video InteractiveSequences so MainSequence advances smoothly anywhere
    iseq = sld.TimeLine.InteractiveSequences
    for s_i in range(iseq.Count, 0, -1):
        seq = iseq.Item(s_i)
        for e_i in range(seq.Count, 0, -1):
            seq.Item(e_i).Delete()
    return clips


def build_slide_3(sld: Any) -> None:
    """Slide 3: Single-phase H-bridge, freewheeling & dead-time (Manim clips) — 4 clicks."""
    add_slide_chrome(sld, 3, "电流不能突变：开关必须配续流二极管", "原理")
    clips = _add_video_clips(sld, 3, "p3")

    # Right beat checklist panel (x=26.1..32.4, y=3.4..16.9)
    add_box(sld, "p3_beat_panel", 26.1, 3.4, 6.3, 13.5, fill=PANEL_BG, line=PANEL_BORDER, line_pt=0.75, round_cm=0.2)
    add_simple_label(sld, "p3_beat_hdr", 26.4, 3.55, 5.7, 0.72, "动画节拍导览", size=18, color=TEXT_MAIN, bold=True)

    beats = [
        ("① 开关与方波", "S₁/S₄ (+U) 与 S₂/S₃ (−U) 交替切换"),
        ("② 绕组电流", "感性负载：电流为电压的积分（三角波）"),
        ("③ 续流路径", "电压翻转时电流经反并二极管回流"),
        ("④ 死区与反向恢复", "防母线直通留死区；反向恢复增 E_on"),
    ]
    beat_cards = []
    for idx, (bt, bs) in enumerate(beats, start=1):
        cy = 4.45 + (idx - 1) * 3.05
        runs_sub = (
            [
                make_run("防母线直通留死区；反向恢复增 ", size=14, color=TEXT_SUB),
                make_run("E", size=14, color=TEXT_SUB, italic=True, font=FONT_MATH),
                make_run("on", size=14, color=TEXT_SUB, font=FONT_MATH, sub=True),
            ]
            if idx == 4
            else [make_run(bs, size=14, color=TEXT_SUB)]
        )
        card = add_textbox(
            sld,
            f"p3_beat_{idx}",
            26.35,
            cy,
            5.8,
            2.80,
            [
                {"runs": [make_run(bt, size=16, color=TEXT_MAIN, bold=True)], "space_after": 6},
                {"runs": runs_sub},
            ],
            align=PP_ALIGN_LEFT,
            valign=MSO_ANCHOR_MIDDLE,
            fill=WHITE,
            line=PANEL_BORDER,
            line_pt=0.75,
            round_cm=0.18,
            margin_cm=(0.20, 0.16, 0.10, 0.10),
        )
        beat_cards.append(card)

    # Bottom formula strip (x=1.5..25.5, y=17.15..18.45)
    formula_bar = add_textbox(
        sld,
        "p3_formula_1",
        1.5,
        17.15,
        24.0,
        1.30,
        [
            {
                "runs": [
                    make_run("感性回路： ", size=16, color=TEXT_SUB, bold=True),
                    make_run("u", size=18, color=TEXT_MAIN, italic=True, font=FONT_MATH),
                    make_run(" = ", size=18, color=TEXT_MAIN, font=FONT_MATH),
                    make_run("Ri", size=18, color=TEXT_MAIN, italic=True, font=FONT_MATH),
                    make_run(" + ", size=18, color=TEXT_MAIN, font=FONT_MATH),
                    make_run("L", size=18, color=TEXT_MAIN, italic=True, font=FONT_MATH),
                    make_run(" d", size=18, color=TEXT_MAIN, font=FONT_MATH),
                    make_run("i", size=18, color=TEXT_MAIN, italic=True, font=FONT_MATH),
                    make_run("/d", size=18, color=TEXT_MAIN, font=FONT_MATH),
                    make_run("t", size=18, color=TEXT_MAIN, italic=True, font=FONT_MATH),
                    make_run("  ≈  ", size=18, color=SIC_COLOR, bold=True, font=FONT_MATH),
                    make_run("L", size=18, color=SIC_COLOR, italic=True, bold=True, font=FONT_MATH),
                    make_run(" d", size=18, color=SIC_COLOR, bold=True, font=FONT_MATH),
                    make_run("i", size=18, color=SIC_COLOR, italic=True, bold=True, font=FONT_MATH),
                    make_run("/d", size=18, color=SIC_COLOR, bold=True, font=FONT_MATH),
                    make_run("t", size=18, color=SIC_COLOR, italic=True, bold=True, font=FONT_MATH),
                    make_run("　（电流不能突变）", size=16, color=TEXT_MAIN, bold=True),
                ],
                "align": PP_ALIGN_CENTER,
            }
        ],
        fill=PANEL_BG,
        line=PANEL_BORDER,
        line_pt=0.75,
        round_cm=0.18,
    )

    # 4 clicks: video clips + beat cards + formula bar on Click 2
    for i in range(4):
        if i == 0:
            anim_media_play(sld, clips[0], trigger=TRIG_CLICK)
        else:
            anim_appear(sld, clips[i], trigger=TRIG_CLICK)
            anim_media_play(sld, clips[i], trigger=TRIG_WITH_PREV)
        anim_fade(sld, beat_cards[i], trigger=TRIG_WITH_PREV, duration=0.4)
        if i == 1:
            anim_fade(sld, formula_bar, trigger=TRIG_WITH_PREV, duration=0.4)


def build_slide_4(sld: Any) -> None:
    """Slide 4: PWM duty-cycle averaging & SPWM 3-phase motor (Manim clips) — 4 clicks."""
    add_slide_chrome(sld, 4, "改变占空比，就能得到正弦电流", "原理")
    clips = _add_video_clips(sld, 4, "p4")

    # Right panel (x=26.1..32.4, y=3.4..16.9)
    add_box(sld, "p4_right_panel", 26.1, 3.4, 6.3, 13.5, fill=PANEL_BG, line=PANEL_BORDER, line_pt=0.75, round_cm=0.2)

    # Top formula & D -> u_bar table (synced to Click 1, where Clip 1 animates 75% -> 50% -> 25%)
    duty_hdr = add_textbox(
        sld,
        "p4_duty_formula",
        26.35,
        3.52,
        5.8,
        1.38,
        [
            {
                "runs": [
                    make_run("ū = (2D − 1)U", size=18, color=TEXT_MAIN, bold=True, font=FONT_MATH),
                ],
                "align": PP_ALIGN_CENTER,
                "space_after": 1,
                "line_spacing": 1.05,
            },
            {"runs": [make_run("算例：U = 400 V", size=14, color=TEXT_SUB)], "align": PP_ALIGN_CENTER, "line_spacing": 1.05},
        ],
        fill=WHITE,
        line=PANEL_BORDER,
        line_pt=0.75,
        round_cm=0.16,
        margin_cm=(0.06, 0.06, 0.02, 0.02),
    )
    tbl_rows = [duty_hdr]
    tbl_specs = [
        ("占空比 D", "平均电压 ū", PANEL_BG, TEXT_MAIN, TEXT_MAIN, True),
        ("75%", "+200 V", WHITE, TEXT_MAIN, COST_COLOR, False),
        ("50%", "0 V", WHITE, TEXT_MAIN, TEXT_SUB, False),
        ("25%", "−200 V", WHITE, TEXT_MAIN, SI_COLOR, False),
    ]
    for r_i, (d_s, u_s, bg, c_d, c_u, is_hdr) in enumerate(tbl_specs):
        row = add_table_row_group(
            sld,
            f"p4_duty_row_{r_i + 1}",
            26.35,
            5.00 + r_i * 0.84,
            [2.65, 3.15],
            0.84,
            [
                [make_run(d_s, size=16, color=c_d, bold=True)],
                [make_run(u_s, size=16, color=c_u, bold=True)],
            ],
            default_fill=bg,
            aligns=[PP_ALIGN_CENTER, PP_ALIGN_CENTER],
            margin_cm=(0.06, 0.06, 0.0, 0.0),
        )
        tbl_rows.append(row)
    duty_grp = group_shapes(sld, tbl_rows, "p4_duty_grp_1")

    # Lower 4 beat cards (y=8.52..16.72)
    beats = [
        ("① 占空比与伏秒面积", "平均电压随 D 线性变化"),
        ("② SPWM 正弦包络", "占空比按正弦规律变化"),
        ("③ 滤波正弦电流", "幅值/频率/相位独立可控"),
        ("④ 三相全桥与电机", "三相 120° → 旋转磁场"),
    ]
    beat_cards = []
    for idx, (bt, bs) in enumerate(beats, start=1):
        cy = 8.52 + (idx - 1) * 2.06
        card = add_textbox(
            sld,
            f"p4_beat_{idx}",
            26.35,
            cy,
            5.8,
            1.96,
            [
                {"runs": [make_run(bt, size=15, color=TEXT_MAIN, bold=True)], "space_after": 1, "line_spacing": 1.05},
                {"runs": [make_run(bs, size=14, color=TEXT_SUB)], "line_spacing": 1.05},
            ],
            fill=WHITE,
            line=PANEL_BORDER,
            line_pt=0.75,
            round_cm=0.16,
            margin_cm=(0.14, 0.10, 0.02, 0.02),
        )
        beat_cards.append(card)

    # Bottom strip (x=1.5..25.5, y=17.15..18.45)
    bottom_bar = add_textbox(
        sld,
        "p4_bottom_note",
        1.5,
        17.15,
        24.0,
        1.30,
        [
            {
                "runs": [
                    make_run("一阶低通特性： ", size=16, color=TEXT_SUB, bold=True),
                    make_run("τ = L/R ≫ T", size=17, color=TEXT_MAIN, bold=True, font=FONT_MATH),
                    make_run("s", size=17, color=TEXT_MAIN, bold=True, font=FONT_MATH, sub=True),
                    make_run("　|　开关频率越高纹波越小（", size=16, color=TEXT_MAIN),
                    make_run("10 kHz / 50 Hz = 200 脉冲/周期", size=16, color=SIC_COLOR, bold=True),
                    make_run("）", size=16, color=TEXT_MAIN),
                ],
                "align": PP_ALIGN_CENTER,
            }
        ],
        fill=PANEL_BG,
        line=PANEL_BORDER,
        line_pt=0.75,
        round_cm=0.18,
    )

    # 4 clicks
    for i in range(4):
        if i == 0:
            anim_media_play(sld, clips[0], trigger=TRIG_CLICK)
            anim_fade(sld, duty_grp, trigger=TRIG_WITH_PREV, duration=0.4)
        else:
            anim_appear(sld, clips[i], trigger=TRIG_CLICK)
            anim_media_play(sld, clips[i], trigger=TRIG_WITH_PREV)
        anim_fade(sld, beat_cards[i], trigger=TRIG_WITH_PREV, duration=0.4)
        if i == 2:
            anim_fade(sld, bottom_bar, trigger=TRIG_WITH_PREV, duration=0.4)


def build_slide_5(sld: Any) -> None:
    """Slide 5: Four device requirements + native log-log R_on,sp vs BV chart — 5 clicks."""
    add_slide_chrome(sld, 5, "对开关器件的四项要求", "要求")

    # Left 2x2 cards (x=1.5..17.5, y=3.6..16.2, each 7.8 x 5.9 cm, gap 0.4)
    cards_spec = [
        (
            1,
            1.5,
            3.6,
            "耐压",
            [
                make_run("V", size=16, color=TEXT_MAIN, italic=True, font=FONT_MATH),
                make_run("os", size=16, color=TEXT_MAIN, font=FONT_MATH, sub=True),
                make_run(" = ", size=16, color=TEXT_MAIN, font=FONT_MATH),
                make_run("L", size=16, color=TEXT_MAIN, italic=True, font=FONT_MATH),
                make_run("σ", size=16, color=TEXT_MAIN, font=FONT_MATH, sub=True),
                make_run(" · d", size=16, color=TEXT_MAIN, font=FONT_MATH),
                make_run("i", size=16, color=TEXT_MAIN, italic=True, font=FONT_MATH),
                make_run("/d", size=16, color=TEXT_MAIN, font=FONT_MATH),
                make_run("t", size=16, color=TEXT_MAIN, italic=True, font=FONT_MATH),
            ],
            "400 V 平台：650/750V\n800 V 平台：1200 V",
        ),
        (
            2,
            9.7,
            3.6,
            "导通损耗",
            [
                make_run("P", size=16, color=TEXT_MAIN, italic=True, font=FONT_MATH),
                make_run("cond", size=16, color=TEXT_MAIN, font=FONT_MATH, sub=True),
                make_run(" = ", size=16, color=TEXT_MAIN, font=FONT_MATH),
                make_run("V", size=16, color=TEXT_MAIN, italic=True, font=FONT_MATH),
                make_run("on", size=16, color=TEXT_MAIN, font=FONT_MATH, sub=True),
                make_run(" · ", size=16, color=TEXT_MAIN, font=FONT_MATH),
                make_run("I", size=16, color=TEXT_MAIN, italic=True, font=FONT_MATH),
            ],
            "导通压降要小\nMOSFET 看导通电阻",
        ),
        (
            3,
            1.5,
            9.8,
            "开关损耗",
            [
                make_run("P", size=16, color=TEXT_MAIN, italic=True, font=FONT_MATH),
                make_run("sw", size=16, color=TEXT_MAIN, font=FONT_MATH, sub=True),
                make_run(" = ", size=16, color=TEXT_MAIN, font=FONT_MATH),
                make_run("f", size=16, color=TEXT_MAIN, italic=True, font=FONT_MATH),
                make_run("sw", size=16, color=TEXT_MAIN, font=FONT_MATH, sub=True),
                make_run("(", size=16, color=TEXT_MAIN, font=FONT_MATH),
                make_run("E", size=16, color=TEXT_MAIN, italic=True, font=FONT_MATH),
                make_run("on", size=16, color=TEXT_MAIN, font=FONT_MATH, sub=True),
                make_run(" + ", size=16, color=TEXT_MAIN, font=FONT_MATH),
                make_run("E", size=16, color=TEXT_MAIN, italic=True, font=FONT_MATH),
                make_run("off", size=16, color=TEXT_MAIN, font=FONT_MATH, sub=True),
                make_run(")", size=16, color=TEXT_MAIN, font=FONT_MATH),
            ],
            "单次能量越低\n开关频率可越高",
        ),
        (
            4,
            9.7,
            9.8,
            "续流与反向恢复",
            [
                make_run("Q", size=16, color=TEXT_MAIN, italic=True, font=FONT_MATH),
                make_run("rr", size=16, color=TEXT_MAIN, font=FONT_MATH, sub=True),
                make_run(" = ∫ ", size=16, color=TEXT_MAIN, font=FONT_MATH),
                make_run("I", size=16, color=TEXT_MAIN, italic=True, font=FONT_MATH),
                make_run("rr", size=16, color=TEXT_MAIN, font=FONT_MATH, sub=True),
                make_run(" d", size=16, color=TEXT_MAIN, font=FONT_MATH),
                make_run("t", size=16, color=TEXT_MAIN, italic=True, font=FONT_MATH),
            ],
            "续流压降低\n反向恢复电荷 Q_rr 小",
        ),
    ]

    card_groups = []
    for num, cx, cy, title, eq_runs, body_txt in cards_spec:
        parts = [
            add_box(sld, f"p5_card_{num}_bg", cx, cy, 7.8, 5.8, fill=PANEL_BG, line=PANEL_BORDER, line_pt=0.75, round_cm=0.2),
            add_req_badge(sld, f"p5_badge_{num}", num, cx + 0.45, cy + 0.42),
            add_simple_label(sld, f"p5_card_{num}_t", cx + 1.45, cy + 0.36, 6.0, 0.90, title, size=18, color=TEXT_MAIN, bold=True),
            add_textbox(
                sld,
                f"p5_card_{num}_eq",
                cx + 0.45,
                cy + 1.45,
                6.9,
                1.10,
                [{"runs": eq_runs, "align": PP_ALIGN_CENTER}],
                fill=WHITE,
                line=PANEL_BORDER,
                line_pt=0.75,
                round_cm=0.15,
            ),
        ]
        # Format body text cleanly (replace Q_rr in card 4 with subscript)
        if num == 4:
            body_paras = [
                {"runs": [make_run("续流压降低", size=18, color=TEXT_MAIN)], "space_after": 6},
                {
                    "runs": [
                        make_run("反向恢复电荷 ", size=18, color=TEXT_MAIN),
                        make_run("Q", size=18, color=TEXT_MAIN, italic=True, font=FONT_MATH),
                        make_run("rr", size=18, color=TEXT_MAIN, font=FONT_MATH, sub=True),
                        make_run(" 小", size=18, color=TEXT_MAIN),
                    ]
                },
            ]
        else:
            lines = body_txt.split("\n")
            body_paras = [{"runs": [make_run(ln, size=18, color=TEXT_MAIN)], "space_after": 6 if idx == 0 else 0} for idx, ln in enumerate(lines)]
        parts.append(
            add_textbox(
                sld,
                f"p5_card_{num}_body",
                cx + 0.35,
                cy + 2.85,
                7.1,
                2.55,
                body_paras,
                align=PP_ALIGN_LEFT,
                valign=MSO_ANCHOR_TOP,
                margin_cm=(0.04, 0.04, 0.04, 0.04),
            )
        )
        card_groups.append(group_shapes(sld, parts, f"p5_card_{num}"))

    # Clicks 1-4: Cards 1..4 fade in one by one
    for grp in card_groups:
        anim_fade(sld, grp, trigger=TRIG_CLICK, duration=0.4)

    # Right Panel (x=18.3..32.4, y=3.6..17.4): Real PowerPoint log-log Chart + aligned vector curve
    add_box(sld, "p5_chart_panel", 18.3, 3.6, 14.1, 12.15, fill=WHITE, line=PANEL_BORDER, line_pt=0.75, round_cm=0.2)
    add_textbox(
        sld,
        "p5_chart_hdr",
        18.7,
        3.80,
        13.3,
        0.75,
        [
            {
                "runs": [
                    make_run("传统硅 MOSFET：比导通电阻 vs 击穿电压（对数坐标）", size=15, color=TEXT_MAIN, bold=True),
                ],
                "align": PP_ALIGN_LEFT,
            }
        ],
    )

    # Native PowerPoint Scatter Chart (xlXYScatter = -4169) for true log-log grid & axes
    cht_shp = sld.Shapes.AddChart2(-1, -4169, cm(18.6), cm(4.55), cm(13.4), cm(10.8))
    clean_shape(cht_shp)
    cht_shp.Name = "p5_log_chart"
    cht = cht_shp.Chart
    cht.HasTitle = 0
    cht.HasLegend = 0
    cd = cht.ChartData
    cd.Activate()
    wb = cd.Workbook
    ws = wb.Worksheets(1)
    ws.Cells.Clear()
    ws.Range("A1").Value = "BV (V)"
    ws.Range("B1").Value = "R_on,sp (mΩ·cm²)"
    # Keep invisible anchor points spanning [100..2000] x [0.1..1000] so PlotArea grid is calibrated
    ws.Range("A2").Value = 100
    ws.Range("B2").Value = 0.1
    ws.Range("A3").Value = 2000
    ws.Range("B3").Value = 1000
    cht.SetSourceData("='Sheet1'!$A$1:$B$3")
    ser = cht.SeriesCollection(1)
    ser.Format.Line.Visible = 0
    ser.MarkerStyle = -4142  # xlMarkerStyleNone
    wb.Close(True)

    # Configure log-log axes BEFORE reading PlotArea.Inside*
    ax_x = cht.Axes(1)  # xlCategory = 1
    ax_y = cht.Axes(2)  # xlValue = 2
    for ax, mn, mx, ttl in (
        (ax_x, 100.0, 2000.0, "击穿电压 BV (V)"),
        (ax_y, 0.1, 1000.0, "比导通电阻 (mΩ·cm²)"),
    ):
        ax.ScaleType = -4133  # xlScaleLogarithmic
        ax.MinimumScale = mn
        ax.MaximumScale = mx
        ax.HasMajorGridlines = -1
        ax.MajorGridlines.Format.Line.ForeColor.RGB = rgb(PANEL_BORDER)
        ax.MajorGridlines.Format.Line.Weight = 0.5
        ax.Format.Line.ForeColor.RGB = rgb(TEXT_SUB)
        ax.Format.Line.Weight = 1.0
        ax.TickLabels.Font.Name = FONT_UI
        ax.TickLabels.Font.Size = 14
        ax.TickLabels.Font.Color = rgb(TEXT_SUB)
        ax.HasTitle = -1
        ax.AxisTitle.Text = ttl
        ax.AxisTitle.Font.Name = FONT_UI
        ax.AxisTitle.Font.Size = 14
        ax.AxisTitle.Font.Color = rgb(TEXT_MAIN)
        ax.AxisTitle.Font.Bold = -1

    # Map log coordinates directly onto the chart's actual PlotArea
    pa = cht.PlotArea
    pa_x = cht_shp.Left / CM_TO_PT + pa.InsideLeft / CM_TO_PT
    pa_y = cht_shp.Top / CM_TO_PT + pa.InsideTop / CM_TO_PT
    pa_w = pa.InsideWidth / CM_TO_PT
    pa_h = pa.InsideHeight / CM_TO_PT

    def map_log(bv: float, ron: float) -> tuple[float, float]:
        fx = (math.log10(bv) - math.log10(100.0)) / (math.log10(2000.0) - math.log10(100.0))
        fy = (math.log10(ron) - math.log10(0.1)) / (math.log10(1000.0) - math.log10(0.1))
        return pa_x + fx * pa_w, pa_y + (1.0 - fy) * pa_h

    # Silicon 1D limit R_on,sp = 1e-6 * BV^2.5 (mOhm*cm^2)
    bvs = [120, 200, 300, 450, 650, 900, 1200, 1600]
    pts_si = [map_log(b, 1e-6 * (b**2.5)) for b in bvs]
    si_curve = add_polyline(sld, "p5_curve_si_1", pts_si, color=SI_COLOR, weight_pt=3.0)

    x650, y650 = map_log(650.0, 1e-6 * (650.0**2.5))
    dot_650 = add_oval(sld, "p5_dot_650v", x650, y650, 0.42, fill=COST_COLOR, line=WHITE, line_pt=1.5)

    slope_lbl = add_textbox(
        sld,
        "p5_slope_lbl",
        pa_x + pa_w * 0.48,
        pa_y + 0.25,
        4.6,
        0.75,
        [
            {
                "runs": [
                    make_run("R", size=14, color=SI_COLOR, italic=True, bold=True, font=FONT_MATH),
                    make_run("on,sp", size=14, color=SI_COLOR, bold=True, font=FONT_MATH, sub=True),
                    make_run(" ∝ BV", size=14, color=SI_COLOR, bold=True, font=FONT_MATH),
                    make_run("2.5", size=14, color=SI_COLOR, bold=True, font=FONT_MATH, sup=True),
                ],
                "align": PP_ALIGN_CENTER,
            }
        ],
        fill=WHITE,
        line=SI_COLOR,
        line_pt=0.75,
        round_cm=0.14,
    )

    callout_box = add_textbox(
        sld,
        "p5_callout_box",
        21.4,
        5.85,
        8.1,
        2.15,
        [
            {"runs": [make_run("650 V 起步：", size=14, color=COST_COLOR, bold=True)], "space_after": 2, "line_spacing": 1.08},
            {"runs": [make_run("耐压 ↑ → 漂移区加厚、掺杂降低\n→ 导通电阻急剧上升", size=14, color=TEXT_MAIN)], "line_spacing": 1.08},
        ],
        fill=COST_LIGHT,
        line=COST_COLOR,
        line_pt=1.0,
        round_cm=0.16,
        margin_cm=(0.18, 0.14, 0.10, 0.10),
    )
    callout_ptr = add_line_seg(sld, "p5_callout_ptr", 25.8, 8.00, x650 - 0.12, y650 - 0.12, color=COST_COLOR, weight_pt=1.5, arrow_end=True)
    callout = group_shapes(sld, [callout_box, callout_ptr], "p5_callout_si")

    verdict = add_textbox(
        sld,
        "p5_verdict_1",
        18.3,
        16.05,
        14.1,
        1.35,
        [
            {
                "runs": [
                    make_run("硅 MOSFET：", size=16, color=TEXT_MAIN, bold=True),
                    make_run("开关快 ✓", size=16, color=SIC_COLOR, bold=True),
                    make_run("　　", size=16, color=TEXT_MAIN),
                    make_run("耐压与导通难兼得 ✗", size=16, color=COST_COLOR, bold=True),
                ],
                "align": PP_ALIGN_CENTER,
            }
        ],
        fill=PANEL_BG,
        line=PANEL_BORDER,
        line_pt=0.75,
        round_cm=0.18,
    )

    # Click 5: Wipe curve L->R -> Appear + Pulse dot -> Fade callout, slope tag & verdict
    anim_wipe(sld, si_curve, direction=MSO_ANIM_DIR_LEFT, trigger=TRIG_CLICK, duration=0.75)
    anim_appear(sld, dot_650, trigger=TRIG_AFTER_PREV)
    anim_pulse(sld, dot_650, trigger=TRIG_WITH_PREV, duration=0.5)
    anim_fade(sld, slope_lbl, trigger=TRIG_WITH_PREV, duration=0.4)
    anim_fade(sld, callout, trigger=TRIG_WITH_PREV, duration=0.4)
    anim_fade(sld, verdict, trigger=TRIG_WITH_PREV, duration=0.4)
