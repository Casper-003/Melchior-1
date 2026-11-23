"""Build the expanded 28-slide presentation matching the user's style and all physics/data feedback."""

from __future__ import annotations

import math
from pathlib import Path
import re
import shutil
from typing import Any

import win32com.client as win32

from inject_notes import inject_notes_into_presentation, unwrap_notes_alternate_content
from user_style_helpers import (
    BLACK,
    BORDER_GRAY,
    COL_N_MINUS,
    COL_N_PLUS,
    COL_N_SIC,
    COL_P_BODY,
    COL_P_PLUS,
    COL_SIO2,
    COL_SIO2_STROKE,
    EFF_FADE,
    FONT_CN,
    FONT_LATIN,
    FONT_MATH,
    ICE_BLUE,
    ICE_LIGHT,
    INK_DARK,
    LINE_BLUE,
    MSO_LINE_DASH,
    MUTED,
    NAVY,
    PP_ALIGN_CENTER,
    PP_ALIGN_LEFT,
    PP_ALIGN_RIGHT,
    PP_LAYOUT_BLANK,
    RED,
    RED_LIGHT,
    STEEL_BLUE,
    TEAL,
    TEAL_LIGHT,
    TRIG_ON_CLICK,
    WHITE,
    add_embedded_video,
    add_label,
    add_left_sidebar,
    add_line,
    add_oval,
    add_poly,
    add_rect,
    add_rich_box,
    add_right_sidebar,
    add_top_nav_bar,
    anim_group,
    make_run,
    rgb,
    set_no_transition,
)

ROOT_DIR = Path(r"c:\Users\Casper\Documents\Proj")
BACKUP_PPTX = ROOT_DIR / "ppt_builder" / "backup" / "advanced semiconductor device course pre_original.pptx"
TI_IMG = ROOT_DIR / "TI-Debuts-New-Approach-to-Current-Sensing-for-Unprecedented-Accuracy-in-HEV-and-EV-Traction-Inverter-Designs-1920x1080.png"
CLIP_DIR = ROOT_DIR / "manim_videos" / "clips"
OUT_USER_PPTX = ROOT_DIR / "advanced semiconductor device course pre.pptx"
OUT_CN_PPTX = ROOT_DIR / "新能源汽车主驱逆变器_课堂汇报.pptx"
PREVIEW_DIR = ROOT_DIR / "ppt_builder" / "preview_v4"

REQ_STEPS = ["1.四项核心要求", "2.硅MOSFET\n特性"]
IGBT_STEPS = ["1.结构与\n电导调制", "2.结压降与\n轻载损耗", "3.关断拖尾电流", "4.外并FRD与\n反向恢复"]
SIC_RIGHT_STEPS = ["1.材料参数对比", "2.一维电场分布", "3.结构与\n工作原理"]
SIC_LEFT_STEPS = ["1.导通与\n开关对比", "2.续流与\n同步整流", "3.量产与\n成本瓶颈"]
FUT_STEPS = ["1.器件：\n沟槽栅", "2.模块：\n混合并联", "3.系统：\n千伏平台", "4.器件演进总结"]

BANNED_WORDS = ("VS", "vs", "激增", "剧增", "飙升", "暴增", "大幅", "显著", "质变", "媲美", "主力")


def patch_slides_1_to_11(pres: Any) -> None:
    """Preserve Original Slides 1-11 intact and fix only the off-screen top-bar typo on Original Slides 2-11."""
    for s_idx in range(2, 12):
        sld = pres.Slides(s_idx)
        for sh_i in range(1, sld.Shapes.Count + 1):
            sh = sld.Shapes(sh_i)
            if sh.HasTextFrame and sh.TextFrame.HasText:
                txt = sh.TextFrame.TextRange.Text
                if "对开关电路的要求" in txt:
                    sh.TextFrame.TextRange.Text = "对开关器件的要求"
                    sh.Name = "TextBox 9"


# ==============================================================================
# SLIDE 2 (NEW): 主驱逆变器整车实景与开关态工作模式 (Embedded TI 3D Image)
# ==============================================================================
def build_slide_2_ti_photo(sld: Any) -> None:
    """Build new Slide 2 on a duplicate of Original Slide 2 so the top nav bar Morph stays seamless."""
    if not TI_IMG.is_file():
        raise FileNotFoundError(f"TI traction inverter image not found: {TI_IMG}")

    # Remove all body shapes from duplicated Slide 2 while preserving the 5 top-bar shapes (Top < 30 pt)
    for sh_i in range(sld.Shapes.Count, 0, -1):
        sh = sld.Shapes(sh_i)
        if float(sh.Top) >= 30.0:
            sh.Delete()

    mseq = sld.TimeLine.MainSequence
    for e_idx in range(mseq.Count, 0, -1):
        mseq.Item(e_idx).Delete()

    add_label(
        sld, "s2_hdr", 34.0, 46.0, 892.0, 34.0,
        "  主驱逆变器在整车电驱动系统中的位置与工作模式",
        size=15.5, color=NAVY, bold=True, align=PP_ALIGN_LEFT, fill=ICE_BLUE,
    )

    # Left: 1920x1080 EV traction inverter 3D hardware image (exact 16:9 at 576x324 pt)
    pic = sld.Shapes.AddPicture(str(TI_IMG), 0, -1, 34.0, 98.0, 576.0, 324.0)
    pic.Name = "s2_ti_photo"
    add_rect(sld, "s2_ti_border", 34.0, 98.0, 576.0, 324.0, fill=None, line=NAVY, line_pt=1.2)

    # Crisp hardware callout pills anchored on dark areas without hiding the inverter cables/housing
    add_label(
        sld, "s2_tag_inv", 432.0, 112.0, 166.0, 26.0,
        "主驱逆变器（DC → 三相 AC）", size=10.5, color=NAVY, bold=True, align=PP_ALIGN_CENTER,
        fill=WHITE, line=ICE_BLUE, line_pt=1.2,
    )
    add_line(sld, "s2_ptr_inv", 432.0, 125.0, 392.0, 184.0, color=WHITE, weight_pt=1.6, arrow_end=True)

    add_label(
        sld, "s2_tag_mot", 464.0, 278.0, 128.0, 26.0,
        "永磁同步电机", size=10.5, color=NAVY, bold=True, align=PP_ALIGN_CENTER,
        fill=WHITE, line=ICE_BLUE, line_pt=1.2,
    )
    add_line(sld, "s2_ptr_mot", 464.0, 291.0, 398.0, 314.0, color=WHITE, weight_pt=1.6, arrow_end=True)

    add_label(
        sld, "s2_tag_bat", 48.0, 382.0, 168.0, 26.0,
        "动力电池（400 / 800 V DC）", size=10.5, color=NAVY, bold=True, align=PP_ALIGN_CENTER,
        fill=WHITE, line=ICE_BLUE, line_pt=1.2,
    )

    add_label(
        sld, "s2_flow", 34.0, 426.0, 456.0, 22.0,
        "能量流向：动力电池 → 母线电容 → 主驱逆变器 → 永磁同步电机 → 减速器与车轮",
        size=10.5, color=MUTED, align=PP_ALIGN_LEFT,
    )
    add_label(
        sld, "s2_src", 490.0, 426.0, 120.0, 22.0,
        "图源：Texas Instruments",
        size=9.5, color=MUTED, align=PP_ALIGN_RIGHT,
    )
    add_label(
        sld, "s2_cap_note", 34.0, 456.0, 576.0, 32.0,
        "母线电容并联在直流侧，用于稳定母线电压并吸收高频开关纹波",
        size=11.5, color=NAVY, bold=True, align=PP_ALIGN_CENTER, fill=ICE_LIGHT, line=ICE_BLUE, line_pt=1.0,
    )

    # Right structured panel (x=630..926, top=98..488 aligned cleanly with left visual column)
    rx, rw = 630.0, 296.0
    add_rect(sld, "s2_c1_bg", rx, 98.0, rw, 110.0, fill=ICE_LIGHT, line=ICE_BLUE, line_pt=1.0)
    add_rect(sld, "s2_c1_bar", rx, 98.0, 5.0, 110.0, fill=NAVY, line=None)
    add_rich_box(
        sld, "s2_c1_txt", rx + 14.0, 104.0, rw - 22.0, 98.0,
        [
            {"runs": [make_run("乘用车主驱功率量级", size=11.5, color=STEEL_BLUE, bold=True)], "space_after": 4},
            {"runs": [make_run("100–300 kW", size=24.0, color=NAVY, bold=True)], "space_after": 4},
            {"runs": [make_run("对应 400 V / 800 V 直流母线与数百安相电流", size=11.0, color=INK_DARK)]},
        ],
        margins=(0, 0, 0, 0),
    )

    add_rect(sld, "s2_c2_bg", rx, 222.0, rw, 124.0, fill=WHITE, line=RED, line_pt=1.0)
    add_rect(sld, "s2_c2_bar", rx, 222.0, 5.0, 124.0, fill=RED, line=None)
    add_rich_box(
        sld, "s2_c2_txt", rx + 14.0, 228.0, rw - 22.0, 112.0,
        [
            {"runs": [make_run("为何不能工作在线性放大区？", size=12.0, color=RED, bold=True)], "space_after": 4},
            {"runs": [make_run("P = V · I", size=19.0, color=NAVY, bold=True, italic=True, font_latin=FONT_MATH)], "space_after": 4},
            {"runs": [make_run("同时承受高电压与大电流，功耗可达数十千瓦量级，芯片无法承受。", size=11.0, color=INK_DARK)]},
        ],
        margins=(0, 0, 0, 0),
    )

    add_rect(sld, "s2_c3_bg", rx, 360.0, rw, 128.0, fill=TEAL_LIGHT, line=TEAL, line_pt=1.0)
    add_rect(sld, "s2_c3_bar", rx, 360.0, 5.0, 128.0, fill=TEAL, line=None)
    add_rich_box(
        sld, "s2_c3_txt", rx + 14.0, 366.0, rw - 22.0, 116.0,
        [
            {"runs": [make_run("核心工作模式：高低损耗开关态", size=12.0, color=TEAL, bold=True)], "space_after": 5},
            {"runs": [make_run("• 导通态：", size=11.0, color=NAVY, bold=True), make_run("压降极小，损耗低", size=11.0, color=INK_DARK)], "space_after": 3},
            {"runs": [make_run("• 关断态：", size=11.0, color=NAVY, bold=True), make_run("电流近零，损耗低", size=11.0, color=INK_DARK)], "space_after": 4},
            {"runs": [make_run("通过高频切换两种状态合成交流电压。", size=11.0, color=INK_DARK, bold=True)]},
        ],
        margins=(0, 0, 0, 0),
    )


# ==============================================================================
# SLIDE 12: 对开关器件的要求 -> 1.四项核心要求 (Formulas + variable definitions ONLY)
# ==============================================================================
def build_slide_12(sld: Any) -> None:
    set_no_transition(sld)
    add_top_nav_bar(sld, active_tab=2)
    add_left_sidebar(sld, "req", REQ_STEPS, active_step=1, x_pos=0.0)

    add_line(sld, "s12_cross_v", 561.5, 58.0, 561.5, 504.0, color=ICE_BLUE, weight_pt=1.5)
    add_line(sld, "s12_cross_h", 201.0, 282.0, 922.0, 282.0, color=ICE_BLUE, weight_pt=1.5)

    quads = [
        {
            "idx": "01",
            "title": "耐压",
            "x": 204.0,
            "y": 58.0,
            "eq_meaning": "关断瞬间电压过冲公式",
            "formula": [
                make_run("V", size=30, color=NAVY, bold=True, italic=True, font_latin=FONT_MATH),
                make_run("os", size=19, color=NAVY, bold=True, font_latin=FONT_MATH, sub=True),
                make_run(" = ", size=30, color=NAVY, bold=True, font_latin=FONT_MATH),
                make_run("L", size=30, color=NAVY, bold=True, italic=True, font_latin=FONT_MATH),
                make_run("σ", size=19, color=NAVY, bold=True, italic=True, font_latin=FONT_MATH, sub=True),
                make_run(" · d", size=30, color=NAVY, bold=True, font_latin=FONT_MATH),
                make_run("i", size=30, color=NAVY, bold=True, italic=True, font_latin=FONT_MATH),
                make_run(" / d", size=30, color=NAVY, bold=True, font_latin=FONT_MATH),
                make_run("t", size=30, color=NAVY, bold=True, italic=True, font_latin=FONT_MATH),
            ],
            "vars": [
                [make_run("V", size=12.5, color=STEEL_BLUE, bold=True, italic=True), make_run("os", size=9.5, color=STEEL_BLUE, bold=True, sub=True), make_run("：关断感应电压过冲量", size=12.5, color=INK_DARK)],
                [make_run("L", size=12.5, color=STEEL_BLUE, bold=True, italic=True), make_run("σ", size=9.5, color=STEEL_BLUE, bold=True, sub=True), make_run("：母线与封装寄生电感", size=12.5, color=INK_DARK)],
                [make_run("di/dt", size=12.5, color=STEEL_BLUE, bold=True, italic=True), make_run("：关断时的电流变化率", size=12.5, color=INK_DARK)],
            ],
        },
        {
            "idx": "02",
            "title": "导通损耗",
            "x": 582.0,
            "y": 58.0,
            "eq_meaning": "器件导通稳态损耗功率公式",
            "formula": [
                make_run("P", size=30, color=NAVY, bold=True, italic=True, font_latin=FONT_MATH),
                make_run("cond", size=19, color=NAVY, bold=True, font_latin=FONT_MATH, sub=True),
                make_run(" = ", size=30, color=NAVY, bold=True, font_latin=FONT_MATH),
                make_run("V", size=30, color=NAVY, bold=True, italic=True, font_latin=FONT_MATH),
                make_run("on", size=19, color=NAVY, bold=True, font_latin=FONT_MATH, sub=True),
                make_run(" · ", size=30, color=NAVY, bold=True, font_latin=FONT_MATH),
                make_run("I", size=30, color=NAVY, bold=True, italic=True, font_latin=FONT_MATH),
            ],
            "vars": [
                [make_run("P", size=12.5, color=STEEL_BLUE, bold=True, italic=True), make_run("cond", size=9.5, color=STEEL_BLUE, bold=True, sub=True), make_run("：导通损耗功率", size=12.5, color=INK_DARK)],
                [make_run("V", size=12.5, color=STEEL_BLUE, bold=True, italic=True), make_run("on", size=9.5, color=STEEL_BLUE, bold=True, sub=True), make_run("：器件导通压降（MOSFET 为 I·R", size=12.5, color=INK_DARK), make_run("on", size=9.5, color=INK_DARK, sub=True), make_run("）", size=12.5, color=INK_DARK)],
                [make_run("I", size=12.5, color=STEEL_BLUE, bold=True, italic=True), make_run("：流过器件的导通电流", size=12.5, color=INK_DARK)],
            ],
        },
        {
            "idx": "03",
            "title": "开关损耗",
            "x": 204.0,
            "y": 296.0,
            "eq_meaning": "周期高频切换损耗功率公式",
            "formula": [
                make_run("P", size=30, color=NAVY, bold=True, italic=True, font_latin=FONT_MATH),
                make_run("sw", size=19, color=NAVY, bold=True, font_latin=FONT_MATH, sub=True),
                make_run(" = ", size=30, color=NAVY, bold=True, font_latin=FONT_MATH),
                make_run("f", size=30, color=NAVY, bold=True, italic=True, font_latin=FONT_MATH),
                make_run("sw", size=19, color=NAVY, bold=True, font_latin=FONT_MATH, sub=True),
                make_run(" (", size=30, color=NAVY, bold=True, font_latin=FONT_MATH),
                make_run("E", size=30, color=NAVY, bold=True, italic=True, font_latin=FONT_MATH),
                make_run("on", size=19, color=NAVY, bold=True, font_latin=FONT_MATH, sub=True),
                make_run(" + ", size=30, color=NAVY, bold=True, font_latin=FONT_MATH),
                make_run("E", size=30, color=NAVY, bold=True, italic=True, font_latin=FONT_MATH),
                make_run("off", size=19, color=NAVY, bold=True, font_latin=FONT_MATH, sub=True),
                make_run(")", size=30, color=NAVY, bold=True, font_latin=FONT_MATH),
            ],
            "vars": [
                [make_run("P", size=12.5, color=STEEL_BLUE, bold=True, italic=True), make_run("sw", size=9.5, color=STEEL_BLUE, bold=True, sub=True), make_run("：开关损耗功率", size=12.5, color=INK_DARK)],
                [make_run("f", size=12.5, color=STEEL_BLUE, bold=True, italic=True), make_run("sw", size=9.5, color=STEEL_BLUE, bold=True, sub=True), make_run("：器件开关频率", size=12.5, color=INK_DARK)],
                [make_run("E", size=12.5, color=STEEL_BLUE, bold=True, italic=True), make_run("on", size=9.5, color=STEEL_BLUE, bold=True, sub=True), make_run(" , E", size=12.5, color=STEEL_BLUE, bold=True, italic=True), make_run("off", size=9.5, color=STEEL_BLUE, bold=True, sub=True), make_run("：单次开通能量与单次关断能量", size=12.5, color=INK_DARK)],
            ],
        },
        {
            "idx": "04",
            "title": "续流与反向恢复",
            "x": 582.0,
            "y": 296.0,
            "eq_meaning": "二极管反向恢复电荷定义式",
            "formula": [
                make_run("Q", size=30, color=NAVY, bold=True, italic=True, font_latin=FONT_MATH),
                make_run("rr", size=19, color=NAVY, bold=True, font_latin=FONT_MATH, sub=True),
                make_run(" = ∫ ", size=30, color=NAVY, bold=True, font_latin=FONT_MATH),
                make_run("I", size=30, color=NAVY, bold=True, italic=True, font_latin=FONT_MATH),
                make_run("rr", size=19, color=NAVY, bold=True, font_latin=FONT_MATH, sub=True),
                make_run(" d", size=30, color=NAVY, bold=True, font_latin=FONT_MATH),
                make_run("t", size=30, color=NAVY, bold=True, italic=True, font_latin=FONT_MATH),
            ],
            "vars": [
                [make_run("Q", size=12.5, color=STEEL_BLUE, bold=True, italic=True), make_run("rr", size=9.5, color=STEEL_BLUE, bold=True, sub=True), make_run("：反向恢复电荷量（反向恢复电流对时间的积分）", size=12.5, color=INK_DARK)],
                [make_run("I", size=12.5, color=STEEL_BLUE, bold=True, italic=True), make_run("rr", size=9.5, color=STEEL_BLUE, bold=True, sub=True), make_run("：二极管由续流转为截止时抽走少子的反向恢复电流", size=12.5, color=INK_DARK)],
            ],
        },
    ]

    qw = 338.0
    for q in quads:
        x, y = q["x"], q["y"]
        idx = q["idx"]
        grp: list[Any] = []
        grp.append(add_label(sld, f"s12_num_{idx}", x, y, 36.0, 28.0, idx, size=14.0, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=NAVY))
        grp.append(add_label(sld, f"s12_ttl_{idx}", x + 36.0, y, qw - 36.0, 28.0, f"  {q['title']}  ·  {q['eq_meaning']}", size=14.0, color=NAVY, bold=True, align=PP_ALIGN_LEFT, fill=ICE_BLUE))
        grp.append(
            add_rich_box(
                sld, f"s12_eq_{idx}", x, y + 36.0, qw, 68.0,
                [{"runs": q["formula"], "align": PP_ALIGN_CENTER}],
                fill=None, line=None, default_align=PP_ALIGN_CENTER,
            )
        )
        var_paras = [{"runs": vr, "space_after": 4} for vr in q["vars"]]
        grp.append(
            add_rich_box(
                sld, f"s12_vars_{idx}", x + 8.0, y + 110.0, qw - 16.0, 88.0,
                var_paras, fill=ICE_LIGHT, line=ICE_BLUE, line_pt=0.75, margins=(10, 8, 6, 4),
            )
        )
        anim_group(sld, grp, effect=EFF_FADE, duration=0.4, first_trigger=TRIG_ON_CLICK)


# ==============================================================================
# SLIDE 13: 对开关器件的要求 -> 2.硅MOSFET特性 (Objective facts ONLY, no VS/hype)
# ==============================================================================
def build_slide_13(sld: Any) -> None:
    set_no_transition(sld)
    add_top_nav_bar(sld, active_tab=2)
    add_left_sidebar(sld, "req", REQ_STEPS, active_step=2, x_pos=0.0)

    add_label(
        sld, "s13_plot_ttl", 205.0, 56.0, 440.0, 30.0,
        "  硅功率 MOSFET 比导通电阻与击穿电压关系（对数坐标）",
        size=13.8, color=NAVY, bold=True, align=PP_ALIGN_LEFT, fill=ICE_BLUE,
    )

    cht_shp = sld.Shapes.AddChart2(-1, -4169, 205.0, 92.0, 435.0, 405.0)
    cht_shp.Name = "s13_log_chart"
    cht = cht_shp.Chart
    cd = cht.ChartData
    cd.Activate()
    wb = cd.Workbook
    ws = wb.Worksheets(1)
    ws.Cells.Clear()
    ws.Range("A1").Value = ""
    ws.Range("B1").Value = ""
    ws.Range("A2").Value = 100
    ws.Range("B2").Value = 0.1
    ws.Range("A3").Value = 2000
    ws.Range("B3").Value = 1000
    sheet_name = ws.Name
    cht.SetSourceData(f"='{sheet_name}'!$A$1:$B$3")
    ser = cht.SeriesCollection(1)
    ser.Format.Line.Visible = 0
    ser.MarkerStyle = -4142
    wb.Close(True)

    ax_x = cht.Axes(1)
    ax_y = cht.Axes(2)
    for ax, mn, mx, ttl in (
        (ax_x, 100.0, 2000.0, "击穿电压 BV (V)"),
        (ax_y, 0.1, 1000.0, "比导通电阻 (mΩ·cm²)"),
    ):
        ax.ScaleType = -4133
        ax.MinimumScale = mn
        ax.MaximumScale = mx
        ax.HasMajorGridlines = -1
        ax.MajorGridlines.Format.Line.ForeColor.RGB = rgb(ICE_BLUE)
        ax.MajorGridlines.Format.Line.Weight = 0.75
        ax.Format.Line.ForeColor.RGB = rgb(NAVY)
        ax.Format.Line.Weight = 1.2
        ax.TickLabels.Font.Name = FONT_LATIN
        ax.TickLabels.Font.Size = 11
        ax.TickLabels.Font.Color = rgb(INK_DARK)
        ax.HasTitle = -1
        ax.AxisTitle.Text = ttl
        ax.AxisTitle.Font.Name = FONT_CN
        ax.AxisTitle.Font.Size = 12
        ax.AxisTitle.Font.Color = rgb(NAVY)
        ax.AxisTitle.Font.Bold = -1

    try:
        if cht.HasTitle:
            cht.ChartTitle.Delete()
    except Exception:
        pass
    cht.HasTitle = 0
    cht.HasLegend = 0
    cht.ChartArea.Format.Fill.Visible = 0
    cht.ChartArea.Format.Line.Visible = 0
    cht.PlotArea.Format.Fill.Visible = 0
    cht.PlotArea.Format.Line.Visible = 0

    pa = cht.PlotArea
    pa_x = cht_shp.Left + pa.InsideLeft
    pa_y = cht_shp.Top + pa.InsideTop
    pa_w = pa.InsideWidth
    pa_h = pa.InsideHeight

    def map_log_pt(bv_val: float, ron_val: float) -> tuple[float, float]:
        fx = (math.log10(bv_val) - math.log10(100.0)) / (math.log10(2000.0) - math.log10(100.0))
        fy = (math.log10(ron_val) - math.log10(0.1)) / (math.log10(1000.0) - math.log10(0.1))
        return pa_x + fx * pa_w, pa_y + (1.0 - fy) * pa_h

    bvs = [120.0, 200.0, 350.0, 650.0, 900.0, 1200.0, 1600.0]
    pts_si = [map_log_pt(b, 1e-6 * (b ** 2.5)) for b in bvs]
    add_poly(sld, "s13_si_line", pts_si, fill=None, line=NAVY, line_pt=2.8, closed=False)

    eq_badge = add_rich_box(
        sld, "s13_eq_badge", pa_x + 16.0, pa_y + 14.0, 182.0, 46.0,
        [
            {
                "runs": [
                    make_run("R", size=22, color=NAVY, bold=True, italic=True, font_latin=FONT_MATH),
                    make_run("on,sp", size=14, color=NAVY, bold=True, font_latin=FONT_MATH, sub=True),
                    make_run(" ∝ ", size=22, color=NAVY, bold=True, font_latin=FONT_MATH),
                    make_run("BV", size=22, color=NAVY, bold=True, italic=True, font_latin=FONT_MATH),
                    make_run("2.5", size=15, color=NAVY, bold=True, font_latin=FONT_MATH, sup=True),
                ],
                "align": PP_ALIGN_CENTER,
            }
        ],
        fill=ICE_BLUE, line=NAVY, line_pt=1.0, default_align=PP_ALIGN_CENTER,
    )

    x650, y650 = map_log_pt(650.0, 1e-6 * (650.0 ** 2.5))
    x1200, y1200 = map_log_pt(1200.0, 1e-6 * (1200.0 ** 2.5))
    dot650 = add_oval(sld, "s13_dot_650", x650 - 5.5, y650 - 5.5, 11.0, 11.0, fill=RED, line=WHITE, line_pt=1.5)
    dot1200 = add_oval(sld, "s13_dot_1200", x1200 - 5.5, y1200 - 5.5, 11.0, 11.0, fill=RED, line=WHITE, line_pt=1.5)
    lbl650 = add_label(
        sld, "s13_lbl_650", x650 - 122.0, y650 - 26.0, 116.0, 22.0,
        "650 V (400V平台)", size=11.0, color=RED, bold=True, align=PP_ALIGN_RIGHT,
    )
    lbl1200 = add_label(
        sld, "s13_lbl_1200", x1200 - 128.0, y1200 - 26.0, 122.0, 22.0,
        "1200 V (800V平台)", size=11.0, color=RED, bold=True, align=PP_ALIGN_RIGHT,
    )

    add_line(sld, "s13_v_div", 654.0, 58.0, 654.0, 500.0, color=ICE_BLUE, weight_pt=1.5)

    # Right Zone: Pure basic objective parameters/facts (no evaluative boxes, no hype words, no gray walls)
    facts = [
        ("导电载流子", [make_run("仅靠电子导电", size=19, color=NAVY, bold=True)]),
        ("硅临界击穿场强", [make_run("约 0.3 MV/cm", size=24, color=NAVY, bold=True)]),
        (
            "比导通电阻关系",
            [
                make_run("R", size=22, color=NAVY, bold=True, italic=True, font_latin=FONT_MATH),
                make_run("on,sp", size=14, color=NAVY, bold=True, font_latin=FONT_MATH, sub=True),
                make_run(" ∝ BV", size=22, color=NAVY, bold=True, font_latin=FONT_LATIN),
                make_run("2.5", size=14, color=NAVY, bold=True, font_latin=FONT_LATIN, sup=True),
            ],
        ),
        ("高压器件结构特征", [make_run("漂移区厚度增加、掺杂浓度降低", size=15.5, color=STEEL_BLUE, bold=True)]),
        ("主驱平台耐压等级", [make_run("400 V 平台：650 / 750 V\n800 V 平台：1200 V", size=14.0, color=RED, bold=True)]),
    ]
    fact_grp: list[Any] = []
    for i, (f_lbl, f_val) in enumerate(facts):
        fy = 62.0 + i * 88.0
        fact_grp.append(add_rect(sld, f"s13_fbar_{i}", 672.0, fy, 4.5, 68.0, fill=STEEL_BLUE if i < 4 else RED, line=None))
        fact_grp.append(add_label(sld, f"s13_flbl_{i}", 686.0, fy, 235.0, 22.0, f_lbl, size=12.5, color=STEEL_BLUE, bold=True))
        fact_grp.append(
            add_rich_box(
                sld, f"s13_fval_{i}", 686.0, fy + 24.0, 236.0, 42.0,
                [{"runs": f_val, "align": PP_ALIGN_LEFT}],
                margins=(0, 0, 0, 0),
            )
        )
        if i < 4:
            fact_grp.append(add_line(sld, f"s13_fsep_{i}", 672.0, fy + 76.0, 920.0, fy + 76.0, color=ICE_BLUE, weight_pt=0.75))

    anim_group(sld, [eq_badge, dot650, lbl650, dot1200, lbl1200] + fact_grp, effect=EFF_FADE, duration=0.4, first_trigger=TRIG_ON_CLICK)


# ==============================================================================
# SLIDE 14: IGBT -> 1.结构与电导调制 (Manim Video Clip)
# ==============================================================================
def build_slide_14(sld: Any) -> None:
    set_no_transition(sld)
    add_top_nav_bar(sld, active_tab=3)
    add_left_sidebar(sld, "igbt", IGBT_STEPS, active_step=1, x_pos=0.0)
    add_embedded_video(sld, "igbt_conduction", CLIP_DIR / "igbt_conduction.mp4", 163.2, 57.5, 796.8, 448.2)


# ==============================================================================
# SLIDE 15: IGBT -> 2.结压降与轻载损耗 (No big red headline; clear I-V chart explanation)
# ==============================================================================
def build_slide_15(sld: Any) -> None:
    set_no_transition(sld)
    add_top_nav_bar(sld, active_tab=3)
    add_left_sidebar(sld, "igbt", IGBT_STEPS, active_step=2, x_pos=0.0)

    add_label(
        sld, "s15_hdr", 201.0, 52.0, 721.0, 32.0,
        "  硅 IGBT 输出特性曲线：背面 P+/N− 结开启压降与轻载损耗",
        size=15.0, color=NAVY, bold=True, align=PP_ALIGN_LEFT, fill=ICE_BLUE,
    )

    # Left: Large Vector I_C - V_CE Curve (x=205..575, y=104..496)
    ox, oy = 256.0, 442.0
    add_line(sld, "s15_ax_x", ox, oy, 560.0, oy, color=NAVY, weight_pt=1.8, arrow_end=True)
    add_line(sld, "s15_ax_y", ox, oy, ox, 114.0, color=NAVY, weight_pt=1.8, arrow_end=True)

    add_rich_box(
        sld, "s15_xlbl", 455.0, oy + 8.0, 112.0, 26.0,
        [{"runs": [make_run("导通压降 V", size=12, color=NAVY, bold=True), make_run("CE", size=9, color=NAVY, bold=True, sub=True), make_run(" (V)", size=12, color=NAVY, bold=True)], "align": PP_ALIGN_RIGHT}],
        margins=(0, 0, 0, 0),
    )
    add_rich_box(
        sld, "s15_ylbl", ox + 8.0, 112.0, 125.0, 26.0,
        [{"runs": [make_run("集电极电流 I", size=12, color=NAVY, bold=True), make_run("C", size=9, color=NAVY, bold=True, sub=True), make_run(" (A)", size=12, color=NAVY, bold=True)]}],
        margins=(0, 0, 0, 0),
    )

    # Dead zone shading (0 -> 0.7 V)
    kx = ox + 115.0  # 0.7 V knee
    add_rect(sld, "s15_kzone", ox, 150.0, kx - ox, oy - 150.0, fill=RED_LIGHT, line=None)
    add_line(sld, "s15_kdash", kx, oy, kx, 146.0, color=RED, weight_pt=1.5, dash=MSO_LINE_DASH)
    add_label(sld, "s15_tick0", ox - 12.0, oy + 6.0, 24.0, 22.0, "0", size=12.0, color=NAVY, bold=True, align=PP_ALIGN_CENTER)
    add_label(sld, "s15_tick07", kx - 30.0, oy + 6.0, 60.0, 22.0, "~0.7 V", size=12.0, color=RED, bold=True, align=PP_ALIGN_CENTER)

    # Light-load horizontal band (lower portion of IC)
    add_rect(sld, "s15_llband", ox, oy - 88.0, 290.0, 88.0, fill=ICE_LIGHT, line=ICE_BLUE, line_pt=0.75)
    add_label(sld, "s15_llbl", kx + 102.0, oy - 74.0, 130.0, 38.0, "车辆日常多处于\n中小负载电流区间", size=11.0, color=STEEL_BLUE, bold=True)

    # IGBT I_C(V_CE) curve
    add_poly(
        sld, "s15_iv_curve",
        [(ox, oy), (kx - 10.0, oy), (kx + 18.0, oy - 22.0), (kx + 56.0, oy - 86.0), (kx + 118.0, oy - 210.0), (kx + 160.0, oy - 296.0)],
        fill=None, line=RED, line_pt=3.0, closed=False,
    )
    add_label(
        sld, "s15_ktag", ox + 8.0, 174.0, 100.0, 48.0,
        "内建结开启门槛\n（约 0.7 V）", size=11.0, color=RED, bold=True, align=PP_ALIGN_CENTER, fill=WHITE, line=RED, line_pt=0.75,
    )
    add_label(
        sld, "s15_ctag", kx + 18.0, 128.0, 118.0, 42.0,
        "电导调制导通区\n（大电流压降较缓）", size=10.5, color=NAVY, bold=True, align=PP_ALIGN_CENTER, fill=WHITE, line=NAVY, line_pt=0.75,
    )

    add_line(sld, "s15_vdiv", 584.0, 104.0, 584.0, 496.0, color=ICE_BLUE, weight_pt=1.5)

    # Right: Clear chart-reading explanation blocks (x=602..922)
    exps = [
        (
            "01  坐标与曲线含义",
            [
                make_run("横轴为集射极导通压降 V", size=12.5, color=INK_DARK),
                make_run("CE", size=9.5, color=INK_DARK, sub=True),
                make_run("，纵轴为集电极电流 I", size=12.5, color=INK_DARK),
                make_run("C", size=9.5, color=INK_DARK, sub=True),
                make_run("；曲线斜率对应器件导通后的等效电阻。", size=12.5, color=INK_DARK),
            ],
        ),
        (
            "02  约 0.7 V 门槛来源",
            [
                make_run("IGBT 背面引入的 P", size=12.5, color=INK_DARK),
                make_run("+", size=9.5, color=INK_DARK, sup=True),
                make_run("/N", size=12.5, color=INK_DARK),
                make_run("−", size=9.5, color=INK_DARK, sup=True),
                make_run(" 结本身存在约 0.7 V 的开启压降；当外加压降超过该门槛后电流才迅速上升。", size=12.5, color=INK_DARK),
            ],
        ),
        (
            "03  轻载导通损耗偏高",
            [
                make_run("即使工作电流很小时，该约 0.7 V 的结压降依然存在；而乘用车大部分运行时间位于中小负载区，因此轻载导通损耗相对偏高。", size=12.5, color=INK_DARK),
            ],
        ),
    ]
    exp_grp: list[Any] = []
    for i, (e_ttl, e_runs) in enumerate(exps):
        ey = 108.0 + i * 130.0
        exp_grp.append(add_rect(sld, f"s15_ebg_{i}", 602.0, ey, 320.0, 114.0, fill=ICE_LIGHT, line=ICE_BLUE, line_pt=1.0))
        exp_grp.append(add_rect(sld, f"s15_ebar_{i}", 602.0, ey, 5.0, 114.0, fill=STEEL_BLUE if i < 2 else RED, line=None))
        exp_grp.append(add_label(sld, f"s15_ettl_{i}", 616.0, ey + 6.0, 296.0, 24.0, e_ttl, size=14.5, color=NAVY, bold=True))
        exp_grp.append(
            add_rich_box(
                sld, f"s15_etxt_{i}", 616.0, ey + 32.0, 298.0, 76.0,
                [{"runs": e_runs, "line_spacing": 1.15}],
                margins=(0, 0, 0, 0),
            )
        )
    anim_group(sld, exp_grp, effect=EFF_FADE, duration=0.45, first_trigger=TRIG_ON_CLICK)


# ==============================================================================
# SLIDE 16: IGBT -> 3.关断拖尾电流 (Manim Video Clip)
# ==============================================================================
def build_slide_16(sld: Any) -> None:
    set_no_transition(sld)
    add_top_nav_bar(sld, active_tab=3)
    add_left_sidebar(sld, "igbt", IGBT_STEPS, active_step=3, x_pos=0.0)
    add_embedded_video(sld, "igbt_turnoff_tail", CLIP_DIR / "igbt_turnoff_tail.mp4", 163.2, 57.5, 796.8, 448.2)


# ==============================================================================
# SLIDE 17: IGBT -> 4.外并FRD与反向恢复 (No big red headline; circuit + annotated iD(t) chart)
# ==============================================================================
def build_slide_17(sld: Any) -> None:
    set_no_transition(sld)
    add_top_nav_bar(sld, active_tab=3)
    add_left_sidebar(sld, "igbt", IGBT_STEPS, active_step=4, x_pos=0.0)

    add_rich_box(
        sld, "s17_hdr", 201.0, 52.0, 721.0, 32.0,
        [{"runs": [make_run("  失去反向导通能力：外并硅快恢复二极管（FRD）与反向恢复电荷 Q", size=15.0, color=NAVY, bold=True), make_run("rr", size=11.0, color=NAVY, bold=True, sub=True)]}],
        fill=ICE_BLUE, margins=(0, 0, 0, 0),
    )

    # Left: Circuit Schematic (x=201..495, y=104..496)
    add_rect(sld, "s17_cir_bg", 201.0, 104.0, 294.0, 392.0, fill=ICE_LIGHT, line=ICE_BLUE, line_pt=1.0)
    add_label(sld, "s17_cir_ttl", 213.0, 112.0, 270.0, 24.0, "单个开关模块内部电流路径", size=13.5, color=NAVY, bold=True, align=PP_ALIGN_CENTER)

    # Main vertical nodes: Top node (348, 160), Bot node (348, 355)
    add_line(sld, "s17_top_stub", 348.0, 144.0, 348.0, 174.0, color=NAVY, weight_pt=2.0)
    add_line(sld, "s17_bot_stub", 348.0, 322.0, 348.0, 355.0, color=NAVY, weight_pt=2.0)
    add_line(sld, "s17_top_bus", 268.0, 174.0, 428.0, 174.0, color=NAVY, weight_pt=2.0)
    add_line(sld, "s17_bot_bus", 268.0, 322.0, 428.0, 322.0, color=NAVY, weight_pt=2.0)

    # Left branch: IGBT symbol block (268)
    add_line(sld, "s17_igbt_v", 268.0, 174.0, 268.0, 322.0, color=NAVY, weight_pt=2.0)
    add_label(
        sld, "s17_igbt_box", 220.0, 218.0, 96.0, 62.0,
        "硅 IGBT\n（仅正向导通）", size=11.5, color=NAVY, bold=True, align=PP_ALIGN_CENTER, fill=WHITE, line=NAVY, line_pt=1.5,
    )
    add_line(sld, "s17_arr_fwd", 268.0, 286.0, 268.0, 316.0, color=NAVY, weight_pt=2.4, arrow_end=True)

    # Right branch: Anti-parallel Si FRD (428)
    add_line(sld, "s17_frd_v", 428.0, 174.0, 428.0, 322.0, color=RED, weight_pt=2.0)
    add_label(
        sld, "s17_frd_box", 374.0, 218.0, 108.0, 62.0,
        "外并硅 FRD\n（反并联续流）", size=11.5, color=RED, bold=True, align=PP_ALIGN_CENTER, fill=RED_LIGHT, line=RED, line_pt=1.5,
    )
    add_line(sld, "s17_arr_rev", 428.0, 212.0, 428.0, 180.0, color=RED, weight_pt=2.4, arrow_end=True)

    add_rich_box(
        sld, "s17_cir_note", 214.0, 368.0, 268.0, 118.0,
        [
            {
                "runs": [
                    make_run("结构原因：", size=12, color=NAVY, bold=True),
                    make_run("背面 P", size=12, color=INK_DARK),
                    make_run("+", size=9, color=INK_DARK, sup=True),
                    make_run(" 集电区使 IGBT 无法从发射极向集电极反向导通；电感负载死区续流必须依靠外部反并联硅 FRD。", size=12, color=INK_DARK),
                ],
                "line_spacing": 1.18,
            }
        ],
        fill=WHITE, line=ICE_BLUE, line_pt=1.0, margins=(8, 8, 6, 6),
    )

    # Right: Large Annotated i_D(t) Reverse Recovery Waveform + Chart Explanation (x=518..922)
    ox, oy = 548.0, 224.0  # zero current axis
    add_line(sld, "s17_ax_x", ox, oy, 912.0, oy, color=NAVY, weight_pt=1.5, arrow_end=True)
    add_line(sld, "s17_ax_y", ox, 332.0, ox, 114.0, color=NAVY, weight_pt=1.5, arrow_end=True)
    add_label(sld, "s17_xlbl", 872.0, oy + 4.0, 38.0, 20.0, "t", size=12.0, color=NAVY, bold=True, italic=True, align=PP_ALIGN_RIGHT)
    add_rich_box(
        sld, "s17_ylbl", ox + 6.0, 110.0, 150.0, 22.0,
        [{"runs": [make_run("二极管电流 i", size=11.5, color=NAVY, bold=True), make_run("D", size=9, color=NAVY, bold=True, sub=True), make_run("(t)", size=11.5, color=NAVY, bold=True)]}],
        margins=(0, 0, 0, 0),
    )

    # Negative Qrr area polygon
    add_poly(
        sld, "s17_qrr_fill",
        [(ox + 126.0, oy), (ox + 178.0, oy + 92.0), (ox + 266.0, oy)],
        fill=RED_LIGHT, line=None, closed=True,
    )
    # Reverse recovery current curve
    add_poly(
        sld, "s17_id_curve",
        [(ox + 10.0, oy - 76.0), (ox + 84.0, oy - 76.0), (ox + 126.0, oy), (ox + 178.0, oy + 92.0), (ox + 266.0, oy), (ox + 332.0, oy)],
        fill=None, line=RED, line_pt=2.8, closed=False,
    )
    add_label(sld, "s17_ph1", ox + 20.0, oy - 102.0, 80.0, 20.0, "正向续流区", size=10.5, color=STEEL_BLUE, bold=True)
    add_label(sld, "s17_ph0", ox + 110.0, oy - 22.0, 48.0, 20.0, "过零", size=10.0, color=MUTED, bold=True)
    add_rich_box(
        sld, "s17_irr_lbl", ox + 10.0, oy + 32.0, 132.0, 50.0,
        [
            {"runs": [make_run("阴影面积 Q", size=11, color=RED, bold=True), make_run("rr", size=8.5, color=RED, bold=True, sub=True), make_run(" = ∫ I", size=11, color=RED, bold=True), make_run("rr", size=8.5, color=RED, bold=True, sub=True), make_run(" dt", size=11, color=RED, bold=True)]},
            {"runs": [make_run("峰值 I", size=10.5, color=RED, bold=True), make_run("rr", size=8, color=RED, bold=True, sub=True), make_run("（少子被抽走）", size=10.5, color=INK_DARK)]},
        ],
        fill=WHITE, line=RED, line_pt=0.75, margins=(6, 6, 4, 4),
    )
    add_line(sld, "s17_irr_ptr", ox + 142.0, oy + 52.0, ox + 168.0, oy + 52.0, color=RED, weight_pt=1.5, arrow_end=True)

    # Chart reading notes below waveform (y=350..496)
    ex_grp = [
        add_rect(sld, "s17_ex_bg", 518.0, 350.0, 404.0, 146.0, fill=ICE_LIGHT, line=ICE_BLUE, line_pt=1.0),
        add_rect(sld, "s17_ex_bar", 518.0, 350.0, 5.0, 146.0, fill=NAVY, line=None),
        add_rich_box(
            sld, "s17_ex_txt", 532.0, 358.0, 382.0, 132.0,
            [
                {"runs": [make_run("1. 曲线解读：", size=12, color=NAVY, bold=True), make_run("死区期间 i", size=12, color=INK_DARK), make_run("D", size=9, color=INK_DARK, sub=True), make_run(" > 0 为正，二极管持续续流。", size=12, color=INK_DARK)], "space_after": 5},
                {"runs": [make_run("2. 反向恢复：", size=12, color=NAVY, bold=True), make_run("续流转截止时，内部存储的少数载流子需要被抽走，形成负向尖峰电流 I", size=12, color=INK_DARK), make_run("rr", size=9, color=INK_DARK, sub=True), make_run("。", size=12, color=INK_DARK)], "space_after": 5},
                {"runs": [make_run("3. 电路影响：", size=12, color=NAVY, bold=True), make_run("硅 FRD 的反向恢复电荷 Q", size=12, color=INK_DARK), make_run("rr", size=9, color=INK_DARK, sub=True), make_run(" 较大；死区结束对管开通时，该尖峰叠加于对管电流，增大开通能量 E", size=12, color=INK_DARK), make_run("on", size=9, color=INK_DARK, sub=True), make_run("。", size=12, color=INK_DARK)]},
            ],
            margins=(0, 0, 0, 0),
        ),
    ]
    anim_group(sld, ex_grp, effect=EFF_FADE, duration=0.45, first_trigger=TRIG_ON_CLICK)


# ==============================================================================
# SLIDES 18, 19, 20: SiC MOSFET Material & Principle (Manim Video Clips)
# ==============================================================================
def build_slide_18(sld: Any) -> None:
    set_no_transition(sld)
    add_top_nav_bar(sld, active_tab=4)
    add_right_sidebar(sld, "sic_r", SIC_RIGHT_STEPS, active_step=1, x_pos=797.1)
    add_embedded_video(sld, "sic_params_bars", CLIP_DIR / "sic_params_bars.mp4", 0.0, 57.5, 796.8, 448.2)


def build_slide_19(sld: Any) -> None:
    set_no_transition(sld)
    add_top_nav_bar(sld, active_tab=4)
    add_right_sidebar(sld, "sic_r", SIC_RIGHT_STEPS, active_step=2, x_pos=797.1)
    add_embedded_video(sld, "sic_efield_triangle", CLIP_DIR / "sic_efield_triangle.mp4", 0.0, 57.5, 796.8, 448.2)


def build_slide_20(sld: Any) -> None:
    set_no_transition(sld)
    add_top_nav_bar(sld, active_tab=4)
    add_right_sidebar(sld, "sic_r", SIC_RIGHT_STEPS, active_step=3, x_pos=797.1)
    add_embedded_video(sld, "sic_mosfet_principle", CLIP_DIR / "sic_mosfet_principle.mp4", 0.0, 57.5, 796.8, 448.2)


# ==============================================================================
# SLIDE 21: SiC MOSFET -> Left Sidebar Step 1: 导通与开关对比 (2 spacious columns)
# ==============================================================================
def build_slide_21(sld: Any) -> None:
    set_no_transition(sld)
    add_top_nav_bar(sld, active_tab=4)
    add_left_sidebar(sld, "sic_l", SIC_LEFT_STEPS, active_step=1, x_pos=0.0)

    add_line(sld, "s21_vdiv", 561.5, 58.0, 561.5, 502.0, color=ICE_BLUE, weight_pt=1.5)

    # --- Left Column (x=201..546): I-V Conduction Curve Comparison ---
    x1, cw = 201.0, 345.0
    add_label(sld, "s21_c1_h", x1, 56.0, cw, 30.0, "  01  导通损耗对比（输出特性曲线）", size=14.5, color=NAVY, bold=True, fill=ICE_BLUE)

    ox, oy = x1 + 42.0, 344.0
    add_line(sld, "s21_ax_x", ox, oy, x1 + cw - 12.0, oy, color=NAVY, weight_pt=1.6, arrow_end=True)
    add_line(sld, "s21_ax_y", ox, oy, ox, 108.0, color=NAVY, weight_pt=1.6, arrow_end=True)
    add_rich_box(
        sld, "s21_xl", x1 + 205.0, oy + 6.0, 130.0, 22.0,
        [{"runs": [make_run("V", size=11, color=NAVY, bold=True, italic=True), make_run("DS", size=8.5, color=NAVY, bold=True, sub=True), make_run(" / V", size=11, color=NAVY, bold=True, italic=True), make_run("CE", size=8.5, color=NAVY, bold=True, sub=True), make_run(" (V)", size=11, color=NAVY, bold=True)], "align": PP_ALIGN_RIGHT}],
        margins=(0, 0, 0, 0),
    )
    add_rich_box(
        sld, "s21_yl", ox + 8.0, 104.0, 105.0, 22.0,
        [{"runs": [make_run("I", size=11, color=NAVY, bold=True, italic=True), make_run("D", size=8.5, color=NAVY, bold=True, sub=True), make_run(" / I", size=11, color=NAVY, bold=True, italic=True), make_run("C", size=8.5, color=NAVY, bold=True, sub=True), make_run(" (A)", size=11, color=NAVY, bold=True)]}],
        margins=(0, 0, 0, 0),
    )
    # Shaded SiC lower-drop advantage region
    add_poly(sld, "s21_adv", [(ox, oy), (ox + 92.0, oy), (ox + 158.0, oy - 135.0)], fill=TEAL_LIGHT, line=None, closed=True)
    add_poly(
        sld, "s21_igbt_iv",
        [(ox, oy), (ox + 92.0, oy), (ox + 124.0, oy - 50.0), (ox + 158.0, oy - 135.0), (ox + 190.0, oy - 218.0)],
        fill=None, line=MUTED, line_pt=2.5, closed=False,
    )
    add_line(sld, "s21_sic_iv", ox, oy, ox + 225.0, oy - 192.0, color=TEAL, weight_pt=3.0)
    add_label(sld, "s21_lbl_sic", ox + 16.0, 198.0, 125.0, 36.0, "4H-SiC MOSFET\n（过原点近似电阻）", size=11.0, color=TEAL, bold=True)
    add_label(sld, "s21_lbl_igbt", ox + 132.0, 294.0, 115.0, 36.0, "硅 IGBT\n（约 0.7 V 结压降）", size=11.0, color=MUTED, bold=True)

    add_rect(sld, "s21_c1_nbg", x1, 382.0, cw, 118.0, fill=ICE_LIGHT, line=ICE_BLUE, line_pt=1.0)
    add_rect(sld, "s21_c1_nbar", x1, 382.0, 5.0, 118.0, fill=TEAL, line=None)
    add_rich_box(
        sld, "s21_c1_ntxt", x1 + 14.0, 388.0, cw - 22.0, 106.0,
        [
            {"runs": [make_run("• 过原点特性：", size=12, color=NAVY, bold=True), make_run("无约 0.7 V 结压降，中小电流区导通压降低于硅 IGBT。", size=12, color=INK_DARK)], "space_after": 6},
            {"runs": [make_run("• 大电流交点：", size=12, color=NAVY, bold=True), make_run("电流很大时两曲线可能相交，具体交点位置取决于芯片面积与结温。", size=12, color=INK_DARK)]},
        ],
        margins=(0, 0, 0, 0),
    )

    # --- Right Column (x=577..922): Double-Pulse Test Data & Frequency ---
    x2 = 577.0
    add_label(sld, "s21_c2_h", x2, 56.0, cw, 30.0, "  02  开关损耗对比（双脉冲测试）", size=14.5, color=NAVY, bold=True, fill=ICE_BLUE)

    by0 = 316.0
    add_line(sld, "s21_base", x2 + 24.0, by0, x2 + cw - 20.0, by0, color=NAVY, weight_pt=1.6)
    h_878, h_128 = 166.0, 24.2
    add_rect(sld, "s21_b1_si", x2 + 46.0, by0 - h_878, 38.0, h_878, fill=MUTED, line=NAVY, line_pt=0.75)
    add_label(sld, "s21_v1_si", x2 + 34.0, by0 - h_878 - 22.0, 62.0, 20.0, "8.78 mJ", size=11.0, color=MUTED, bold=True, align=PP_ALIGN_CENTER)
    add_rect(sld, "s21_b1_sic", x2 + 92.0, by0 - h_128, 38.0, h_128, fill=TEAL, line=NAVY, line_pt=0.75)
    add_label(sld, "s21_v1_sic", x2 + 80.0, by0 - h_128 - 22.0, 62.0, 20.0, "1.28 mJ", size=11.0, color=TEAL, bold=True, align=PP_ALIGN_CENTER)
    add_label(sld, "s21_d1", x2 + 78.0, by0 - 115.0, 64.0, 26.0, "−85%", size=13.5, color=RED, bold=True, align=PP_ALIGN_CENTER, fill=RED_LIGHT, line=RED, line_pt=0.75)
    add_rich_box(
        sld, "s21_l1", x2 + 34.0, by0 + 4.0, 108.0, 38.0,
        [{"runs": [make_run("关断能量 E", size=11, color=NAVY, bold=True), make_run("off", size=8.5, color=NAVY, bold=True, sub=True)], "align": PP_ALIGN_CENTER}, {"runs": [make_run("（Si IGBT / SiC）", size=10, color=MUTED)], "align": PP_ALIGN_CENTER}],
        default_align=PP_ALIGN_CENTER, margins=(0, 0, 0, 0),
    )

    h_593, h_053 = 112.1, 10.0
    add_rect(sld, "s21_b2_si", x2 + 198.0, by0 - h_593, 38.0, h_593, fill=MUTED, line=NAVY, line_pt=0.75)
    add_label(sld, "s21_v2_si", x2 + 186.0, by0 - h_593 - 22.0, 62.0, 20.0, "5.93 mJ", size=11.0, color=MUTED, bold=True, align=PP_ALIGN_CENTER)
    add_rect(sld, "s21_b2_sic", x2 + 244.0, by0 - h_053, 38.0, h_053, fill=TEAL, line=NAVY, line_pt=0.75)
    add_label(sld, "s21_v2_sic", x2 + 232.0, by0 - h_053 - 22.0, 62.0, 20.0, "0.53 mJ", size=11.0, color=TEAL, bold=True, align=PP_ALIGN_CENTER)
    add_label(sld, "s21_d2", x2 + 230.0, by0 - 82.0, 64.0, 26.0, "−91%", size=13.5, color=RED, bold=True, align=PP_ALIGN_CENTER, fill=RED_LIGHT, line=RED, line_pt=0.75)
    add_rich_box(
        sld, "s21_l2", x2 + 184.0, by0 + 4.0, 114.0, 38.0,
        [{"runs": [make_run("反向恢复 E", size=11, color=NAVY, bold=True), make_run("rr", size=8.5, color=NAVY, bold=True, sub=True)], "align": PP_ALIGN_CENTER}, {"runs": [make_run("（Si FRD / SiC SBD）", size=10, color=MUTED)], "align": PP_ALIGN_CENTER}],
        default_align=PP_ALIGN_CENTER, margins=(0, 0, 0, 0),
    )

    add_rect(sld, "s21_c2_nbg", x2, 382.0, cw, 118.0, fill=ICE_LIGHT, line=ICE_BLUE, line_pt=1.0)
    add_rect(sld, "s21_c2_nbar", x2, 382.0, 5.0, 118.0, fill=RED, line=None)
    add_rich_box(
        sld, "s21_c2_ntxt", x2 + 14.0, 388.0, cw - 22.0, 106.0,
        [
            {"runs": [make_run("• 测试条件：", size=12, color=NAVY, bold=True), make_run("1200 V / 100 A 模块（600 V · 100 A · 125 ℃ 双脉冲测试），关断能量低约 85% 且受温度影响小。", size=12, color=INK_DARK)], "space_after": 6},
            {"runs": [make_run("• 频率提升：", size=12, color=NAVY, bold=True), make_run("开关频率可提至 20 kHz 以上，减小电机谐波损耗与母线电容容量。", size=12, color=INK_DARK)]},
        ],
        margins=(0, 0, 0, 0),
    )


# ==============================================================================
# SLIDE 22: SiC MOSFET -> Left Sidebar Step 2: 续流与同步整流
# ==============================================================================
def build_slide_22(sld: Any) -> None:
    set_no_transition(sld)
    add_top_nav_bar(sld, active_tab=4)
    add_left_sidebar(sld, "sic_l", SIC_LEFT_STEPS, active_step=2, x_pos=0.0)

    add_label(
        sld, "s22_hdr", 201.0, 52.0, 721.0, 32.0,
        "  SiC MOSFET 续流改进路径：死区体二极管 → 同步整流与外并 SiC 肖特基二极管",
        size=14.5, color=NAVY, bold=True, align=PP_ALIGN_LEFT, fill=ICE_BLUE,
    )

    def draw_stage(tag: str, x0: float, hdr_txt: str, hdr_col: tuple[int, int, int], body_bg: tuple[int, int, int], path_col: tuple[int, int, int], chan_on: bool, desc_lines: list[list[dict[str, Any]]]) -> list[Any]:
        w = 344.0
        objs: list[Any] = []
        objs.append(add_rect(sld, f"s22_{tag}_bg", x0, 102.0, w, 304.0, fill=body_bg, line=hdr_col, line_pt=1.2))
        objs.append(add_label(sld, f"s22_{tag}_h", x0, 102.0, w, 32.0, hdr_txt, size=14.0, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=hdr_col))

        # Half-bridge MOSFET schematic inside x0+20..x0+324, y=148..320
        cx_hb = x0 + 172.0
        # Top OFF switch
        objs.append(add_line(sld, f"s22_{tag}_dc1", cx_hb - 60.0, 152.0, cx_hb + 60.0, 152.0, color=NAVY, weight_pt=2.0))
        objs.append(add_label(sld, f"s22_{tag}_tmos", cx_hb - 42.0, 162.0, 84.0, 26.0, "上管 (关断)", size=10.5, color=MUTED, bold=True, align=PP_ALIGN_CENTER, fill=WHITE, line=BORDER_GRAY))
        objs.append(add_line(sld, f"s22_{tag}_mid_v", cx_hb, 188.0, cx_hb, 224.0, color=NAVY, weight_pt=1.8))
        # Load phase arrow out to right
        objs.append(add_line(sld, f"s22_{tag}_out", cx_hb, 206.0, cx_hb + 108.0, 206.0, color=path_col, weight_pt=2.8, arrow_end=True))
        objs.append(add_label(sld, f"s22_{tag}_load", cx_hb + 68.0, 180.0, 68.0, 22.0, "感性负载", size=10.5, color=NAVY, bold=True, align=PP_ALIGN_CENTER))

        # Lower switch parallel paths: left branch = MOS channel, right branch = PN Body Diode
        objs.append(add_line(sld, f"s22_{tag}_bus_t", cx_hb - 68.0, 224.0, cx_hb + 68.0, 224.0, color=NAVY, weight_pt=1.8))
        objs.append(add_line(sld, f"s22_{tag}_bus_b", cx_hb - 68.0, 304.0, cx_hb + 68.0, 304.0, color=NAVY, weight_pt=1.8))
        objs.append(add_line(sld, f"s22_{tag}_bot_dc", cx_hb - 60.0, 314.0, cx_hb + 60.0, 314.0, color=NAVY, weight_pt=2.0))
        objs.append(add_line(sld, f"s22_{tag}_bot_st", cx_hb, 304.0, cx_hb, 314.0, color=NAVY, weight_pt=1.8))

        ch_fill = TEAL_LIGHT if chan_on else WHITE
        ch_line = TEAL if chan_on else BORDER_GRAY
        ch_txt_col = TEAL if chan_on else MUTED
        ch_lbl = "下管 MOS 沟道\n（正栅压开通）" if chan_on else "下管 MOS 沟道\n（死区关断）"
        objs.append(add_line(sld, f"s22_{tag}_l1a", cx_hb - 68.0, 224.0, cx_hb - 68.0, 240.0, color=ch_line, weight_pt=2.2 if chan_on else 1.2))
        objs.append(add_line(sld, f"s22_{tag}_l1b", cx_hb - 68.0, 288.0, cx_hb - 68.0, 304.0, color=ch_line, weight_pt=2.2 if chan_on else 1.2))
        objs.append(add_label(sld, f"s22_{tag}_ch", cx_hb - 134.0, 240.0, 126.0, 48.0, ch_lbl, size=10.5, color=ch_txt_col, bold=chan_on, align=PP_ALIGN_CENTER, fill=ch_fill, line=ch_line, line_pt=1.5 if chan_on else 1.0))

        bd_active = not chan_on
        bd_fill = RED_LIGHT if bd_active else WHITE
        bd_line = RED if bd_active else BORDER_GRAY
        bd_txt_col = RED if bd_active else MUTED
        objs.append(add_line(sld, f"s22_{tag}_l2a", cx_hb + 68.0, 224.0, cx_hb + 68.0, 240.0, color=bd_line, weight_pt=2.2 if bd_active else 1.2))
        objs.append(add_line(sld, f"s22_{tag}_l2b", cx_hb + 68.0, 288.0, cx_hb + 68.0, 304.0, color=bd_line, weight_pt=2.2 if bd_active else 1.2))
        objs.append(add_label(sld, f"s22_{tag}_bd", cx_hb + 8.0, 240.0, 126.0, 48.0, "内部 PN 体二极管\n（开启压降 ~2–3 V）", size=10.5, color=bd_txt_col, bold=bd_active, align=PP_ALIGN_CENTER, fill=bd_fill, line=bd_line, line_pt=1.5 if bd_active else 1.0))

        # External bypass flow indicator arrow outside the box so it never crosses text
        arr_x = cx_hb - 144.0 if chan_on else cx_hb + 144.0
        objs.append(add_line(sld, f"s22_{tag}_flow", arr_x, 294.0, arr_x, 232.0, color=path_col, weight_pt=2.6, arrow_end=True))
        objs.append(add_label(sld, f"s22_{tag}_flbl", arr_x - 16.0 if chan_on else arr_x + 4.0, 252.0, 24.0, 22.0, "I", size=11.0, color=path_col, bold=True, italic=True, align=PP_ALIGN_CENTER))

        objs.append(
            add_rich_box(
                sld, f"s22_{tag}_desc", x0 + 14.0, 326.0, w - 28.0, 70.0,
                [{"runs": ln, "space_after": 3} for ln in desc_lines],
                margins=(0, 0, 0, 0),
            )
        )
        return objs

    g1 = draw_stage(
        "dead", 201.0,
        "阶段 1｜死区时间（上下管均关断）", MUTED, WHITE, RED, False,
        [
            [make_run("为防直通，上下管均关断；续流电流被迫流经高压降 PN 体二极管（或外并 SiC SBD）。", size=12, color=INK_DARK)],
        ],
    )
    add_line(sld, "s22_arrow_mid", 550.0, 254.0, 572.0, 254.0, color=TEAL, weight_pt=3.0, arrow_end=True)
    g2 = draw_stage(
        "sync", 578.0,
        "阶段 2｜死区结束 · 同步整流（双向沟道导电）", TEAL, ICE_LIGHT, TEAL, True,
        [
            [make_run("MOSFET 沟道支持双向导电；给正在续流的下管施加正栅压，电流改走低阻沟道（I·R", size=12, color=INK_DARK), make_run("on", size=9, color=INK_DARK, sub=True), make_run("），避开体二极管压降。", size=12, color=INK_DARK)],
        ],
    )

    # Bottom factual card on External SiC Schottky Diode
    bot = [
        add_rect(sld, "s22_bot_bg", 201.0, 422.0, 721.0, 82.0, fill=TEAL_LIGHT, line=TEAL, line_pt=1.2),
        add_rect(sld, "s22_bot_bar", 201.0, 422.0, 6.0, 82.0, fill=TEAL, line=None),
        add_rich_box(
            sld, "s22_bot_txt", 218.0, 428.0, 694.0, 70.0,
            [
                {"runs": [make_run("途径二｜外并 SiC 肖特基二极管（SBD）", size=14.0, color=NAVY, bold=True)], "space_after": 4},
                {"runs": [make_run("若模块外并 SiC 肖特基二极管承担续流，其反向恢复能量相比硅 FRD 低约 91%，可同步降低对管的开通能量 E", size=12.5, color=INK_DARK), make_run("on", size=9.5, color=INK_DARK, sub=True), make_run("。", size=12.5, color=INK_DARK)]},
            ],
            margins=(0, 0, 0, 0),
        ),
    ]
    anim_group(sld, g2, effect=EFF_FADE, duration=0.45, first_trigger=TRIG_ON_CLICK)
    anim_group(sld, bot, effect=EFF_FADE, duration=0.45, first_trigger=TRIG_ON_CLICK)


# ==============================================================================
# SLIDE 24: SiC MOSFET -> Left Sidebar Step 3: 量产与成本瓶颈 (Safe, crystal-focused)
# ==============================================================================
def build_slide_24_sic_cost_limits(sld: Any) -> None:
    set_no_transition(sld)
    add_top_nav_bar(sld, active_tab=4)
    add_left_sidebar(sld, "sic_l", SIC_LEFT_STEPS, active_step=3, x_pos=0.0)

    add_label(
        sld, "s24_hdr", 201.0, 52.0, 721.0, 32.0,
        "  4H-SiC MOSFET 普及受限的主要原因：制造门槛与成本",
        size=14.5, color=NAVY, bold=True, align=PP_ALIGN_LEFT, fill=ICE_BLUE,
    )

    # Top: Three crisp manufacturing / yield / cost bottleneck cards (y=102..386)
    cards = [
        (
            "01｜长晶极慢、能耗高",
            "2200–2400 ℃",
            "物理气相传输法（PVT）气相生长",
            "SiC 在常压下不熔化而直接升华，无法像硅一样从熔体快速拉晶；单根晶锭生长耗时可达百余小时，产能与良率均受限制。",
            STEEL_BLUE,
            22.0,
        ),
        (
            "02｜晶锭极硬、切片损耗大",
            "接近金刚石",
            "莫氏硬度约 9.2–9.5",
            "SiC 晶锭硬度远高于单晶硅，切片、研磨与抛光周期长，金刚线切割损耗比例高，单根晶锭可切出的有效晶圆数量有限。",
            NAVY,
            22.0,
        ),
        (
            "03｜衬底与外延成本占比高",
            "> 50%",
            "占芯片总成本一半以上",
            "上游材料成本直接推高整车电控模块价格，因此目前多优先用于中高端 800 V 车型；行业正从 6 英寸向 8 英寸（200 mm）晶圆扩产以摊薄单片成本。",
            RED,
            26.0,
        ),
    ]
    for i, (title, big_val, sub_lbl, body, acc_col, big_sz) in enumerate(cards):
        cx0 = 201.0 + i * (228.0 + 18.5)
        cw = 228.0
        add_rect(sld, f"s24_card_{i}", cx0, 102.0, cw, 284.0, fill=ICE_LIGHT, line=ICE_BLUE, line_pt=1.0)
        add_rect(sld, f"s24_cbar_{i}", cx0, 102.0, cw, 5.0, fill=acc_col, line=None)
        add_label(sld, f"s24_ct_{i}", cx0 + 12.0, 114.0, cw - 24.0, 26.0, title, size=13.5, color=NAVY, bold=True, align=PP_ALIGN_LEFT)
        add_label(sld, f"s24_cv_{i}", cx0 + 12.0, 148.0, cw - 24.0, 44.0, big_val, size=big_sz, color=acc_col, bold=True, align=PP_ALIGN_CENTER)
        add_label(
            sld, f"s24_cs_{i}", cx0 + 14.0, 196.0, cw - 28.0, 24.0, sub_lbl,
            size=10.5, color=MUTED, bold=True, align=PP_ALIGN_CENTER, fill=WHITE, line=ICE_BLUE, line_pt=0.75,
        )
        add_rich_box(
            sld, f"s24_cb_{i}", cx0 + 12.0, 230.0, cw - 24.0, 146.0,
            [{"runs": [make_run(body, size=11.5, color=INK_DARK)], "line_spacing": 1.18}],
            margins=(2, 2, 2, 2),
        )

    # Bottom: High-level summary of engineering support requirements (concise, no deep jargon bait)
    add_rect(sld, "s24_bot_bg", 201.0, 406.0, 721.0, 92.0, fill=WHITE, line=BORDER_GRAY, line_pt=1.0)
    add_rect(sld, "s24_bot_bar", 201.0, 406.0, 5.0, 92.0, fill=NAVY, line=None)
    add_rich_box(
        sld, "s24_bot_txt", 216.0, 412.0, 694.0, 80.0,
        [
            {"runs": [make_run("工程应用层面的配套要求（简要概览）", size=13.0, color=NAVY, bold=True)], "space_after": 5},
            {"runs": [make_run("• 开关速度很快，对功率回路布局、门极驱动与散热封装的工程要求高于硅 IGBT。", size=11.5, color=INK_DARK)], "space_after": 3},
            {"runs": [make_run("• 芯片面积较小，热集中更明显且短路耐受窗口相对更短，需要配套更快的过流保护与散热方案。", size=11.5, color=INK_DARK)]},
        ],
        margins=(0, 0, 0, 0),
    )


# ==============================================================================
# SLIDE 25: 未来发展趋势 -> Right Sidebar Step 1: 1.器件：沟槽栅
# ==============================================================================
def build_slide_25(sld: Any) -> None:
    set_no_transition(sld)
    add_top_nav_bar(sld, active_tab=5)
    add_right_sidebar(sld, "fut", FUT_STEPS, active_step=1, x_pos=797.1)

    add_label(
        sld, "s25_hdr", 38.0, 52.0, 721.0, 32.0,
        "  器件结构演进：平面栅与沟槽栅 SiC MOSFET 并行发展",
        size=15.0, color=NAVY, bold=True, align=PP_ALIGN_LEFT, fill=ICE_BLUE,
    )

    # Left half: Planar Gate vs Trench Gate Cross-Sections (consistent P-pink / N-blue doping colors!)
    # Planar Cell (x=38..380)
    add_label(sld, "s25_pl_h", 38.0, 98.0, 342.0, 26.0, "平面栅结构（横向沟道）", size=14.0, color=NAVY, bold=True, align=PP_ALIGN_CENTER)
    px, pw = 64.0, 290.0
    add_rect(sld, "s25_pl_nd", px, 174.0, pw, 128.0, fill=COL_N_SIC, line=NAVY, line_pt=1.4)
    add_label(sld, "s25_pl_ns", px, 302.0, pw, 36.0, "N+ 碳化硅衬底", size=11.0, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=COL_N_PLUS, line=NAVY)
    add_rect(sld, "s25_pl_pl", px, 174.0, 102.0, 56.0, fill=COL_P_BODY, line=NAVY, line_pt=1.0)
    add_rect(sld, "s25_pl_pr", px + 188.0, 174.0, 102.0, 56.0, fill=COL_P_BODY, line=NAVY, line_pt=1.0)
    add_label(sld, "s25_pl_ptl", px, 200.0, 102.0, 28.0, "P 区", size=11.0, color=NAVY, bold=True, align=PP_ALIGN_CENTER)
    add_label(sld, "s25_pl_ptr", px + 188.0, 200.0, 102.0, 28.0, "P 区", size=11.0, color=NAVY, bold=True, align=PP_ALIGN_CENTER)
    add_label(sld, "s25_pl_nl", px + 34.0, 174.0, 46.0, 24.0, "N+", size=10.0, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=COL_N_PLUS, line=NAVY)
    add_label(sld, "s25_pl_nr", px + 210.0, 174.0, 46.0, 24.0, "N+", size=10.0, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=COL_N_PLUS, line=NAVY)
    add_rect(sld, "s25_pl_ox", px + 76.0, 144.0, 138.0, 30.0, fill=COL_SIO2, line=COL_SIO2_STROKE, line_pt=1.4)
    add_label(sld, "s25_pl_g", px + 92.0, 148.0, 106.0, 20.0, "平面栅 G", size=10.5, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=STEEL_BLUE, line=NAVY)
    add_poly(sld, "s25_pl_arr1", [(px + 66.0, 184.0), (px + 108.0, 184.0), (px + 118.0, 224.0), (px + 118.0, 294.0)], fill=None, line=LINE_BLUE, line_pt=2.2, closed=False)
    add_poly(sld, "s25_pl_arr2", [(px + 224.0, 184.0), (px + 182.0, 184.0), (px + 172.0, 224.0), (px + 172.0, 294.0)], fill=None, line=LINE_BLUE, line_pt=2.2, closed=False)
    add_label(sld, "s25_pl_ndl", px + 70.0, 250.0, 150.0, 26.0, "N− 漂移区（电子路径）", size=10.5, color=NAVY, bold=True, align=PP_ALIGN_CENTER, fill=WHITE, line=ICE_BLUE, line_pt=0.75)

    # Right half: Trench Gate Cell (x=416..759)
    add_label(sld, "s25_tr_h", 416.0, 98.0, 342.0, 26.0, "沟槽栅结构（竖直沟道 · 元胞更紧凑）", size=14.0, color=TEAL, bold=True, align=PP_ALIGN_CENTER)
    tx, tw = 442.0, 290.0
    add_rect(sld, "s25_tr_nd", tx, 160.0, tw, 142.0, fill=COL_N_SIC, line=NAVY, line_pt=1.4)
    add_label(sld, "s25_tr_ns", tx, 302.0, tw, 36.0, "N+ 碳化硅衬底", size=11.0, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=COL_N_PLUS, line=NAVY)
    add_rect(sld, "s25_tr_pl", tx, 160.0, 96.0, 62.0, fill=COL_P_BODY, line=NAVY, line_pt=1.0)
    add_rect(sld, "s25_tr_pr", tx + 194.0, 160.0, 96.0, 62.0, fill=COL_P_BODY, line=NAVY, line_pt=1.0)
    add_label(sld, "s25_tr_ptl", tx, 190.0, 96.0, 30.0, "P 区", size=11.0, color=NAVY, bold=True, align=PP_ALIGN_CENTER)
    add_label(sld, "s25_tr_ptr", tx + 194.0, 190.0, 96.0, 30.0, "P 区", size=11.0, color=NAVY, bold=True, align=PP_ALIGN_CENTER)
    add_label(sld, "s25_tr_nl", tx + 46.0, 160.0, 50.0, 24.0, "N+", size=10.0, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=COL_N_PLUS, line=NAVY)
    add_label(sld, "s25_tr_nr", tx + 194.0, 160.0, 50.0, 24.0, "N+", size=10.0, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=COL_N_PLUS, line=NAVY)
    # Etched Trench with SiO2 liner & Gate inside
    add_rect(sld, "s25_tr_ox", tx + 96.0, 152.0, 98.0, 98.0, fill=COL_SIO2, line=COL_SIO2_STROKE, line_pt=1.6)
    add_label(sld, "s25_tr_g", tx + 110.0, 152.0, 70.0, 82.0, "刻蚀\n沟槽栅\nG", size=11.0, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=STEEL_BLUE, line=NAVY)
    # Buried P+ shield at trench bottom
    add_label(sld, "s25_tr_sh", tx + 90.0, 254.0, 110.0, 24.0, "槽底 P+ 电场屏蔽", size=10.0, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=COL_P_PLUS, line=NAVY)
    # Vertical channels along trench side walls
    add_line(sld, "s25_tr_a1", tx + 90.0, 168.0, tx + 90.0, 296.0, color=LINE_BLUE, weight_pt=2.5, arrow_end=True)
    add_line(sld, "s25_tr_a2", tx + 200.0, 168.0, tx + 200.0, 296.0, color=LINE_BLUE, weight_pt=2.5, arrow_end=True)

    # Bottom structured comparison takeaways (y=360..496)
    cards = [
        ("空间利用率提升", [make_run("栅极做入刻蚀沟槽内部，沟道沿槽壁竖直分布，元胞横向宽度缩小、单位面积元胞数量增加。", size=11.5, color=INK_DARK)], STEEL_BLUE),
        ("降低比导通电阻与成本", [make_run("消除了平面栅的 JFET 夹断颈区并缩短导电路径，直接降低 R", size=11.5, color=INK_DARK), make_run("on,sp", size=8.5, color=INK_DARK, sub=True), make_run(" 与芯片面积，进而降低器件成本。", size=11.5, color=INK_DARK)], TEAL),
        ("核心工程挑战", [make_run("沟槽拐角与槽底栅氧极易发生电场集中，必须结合非对称屏蔽或底部 P", size=11.5, color=INK_DARK), make_run("+", size=8.5, color=INK_DARK, sup=True), make_run(" 屏蔽保护防止栅氧击穿。", size=11.5, color=INK_DARK)], RED),
    ]
    for i, (ct, cb_runs, cc) in enumerate(cards):
        cx0 = 38.0 + i * 246.0
        add_rect(sld, f"s25_cb_{i}", cx0, 362.0, 228.0, 134.0, fill=ICE_LIGHT, line=ICE_BLUE, line_pt=1.0)
        add_rect(sld, f"s25_cbar_{i}", cx0, 362.0, 228.0, 4.5, fill=cc, line=None)
        add_label(sld, f"s25_ct_{i}", cx0 + 10.0, 374.0, 208.0, 24.0, ct, size=13.5, color=NAVY, bold=True, align=PP_ALIGN_LEFT)
        add_rich_box(sld, f"s25_cx_{i}", cx0 + 10.0, 402.0, 208.0, 86.0, [{"runs": cb_runs}], margins=(0, 0, 0, 0))


# ==============================================================================
# SLIDE 26: 未来发展趋势 -> Right Sidebar Step 2: 2.模块：混合并联
# ==============================================================================
def build_slide_26(sld: Any) -> None:
    set_no_transition(sld)
    add_top_nav_bar(sld, active_tab=5)
    add_right_sidebar(sld, "fut", FUT_STEPS, active_step=2, x_pos=797.1)

    add_label(
        sld, "s26_hdr", 38.0, 52.0, 721.0, 32.0,
        "  模块层面演进：4H-SiC MOSFET 与硅 IGBT 芯片混合并联",
        size=15.0, color=NAVY, bold=True, align=PP_ALIGN_LEFT, fill=ICE_BLUE,
    )

    # Left: Hybrid Parallel Circuit Schematic (x=38..365, y=104..496)
    add_rect(sld, "s26_cbg", 38.0, 104.0, 327.0, 392.0, fill=ICE_LIGHT, line=ICE_BLUE, line_pt=1.0)
    add_label(sld, "s26_cttl", 50.0, 114.0, 303.0, 26.0, "混合开关单元并联拓扑示意", size=14.0, color=NAVY, bold=True, align=PP_ALIGN_CENTER)

    add_line(sld, "s26_st_t", 201.5, 148.0, 201.5, 178.0, color=NAVY, weight_pt=2.2)
    add_line(sld, "s26_st_b", 201.5, 344.0, 201.5, 374.0, color=NAVY, weight_pt=2.2)
    add_line(sld, "s26_bus_t", 120.0, 178.0, 283.0, 178.0, color=NAVY, weight_pt=2.2)
    add_line(sld, "s26_bus_b", 120.0, 344.0, 283.0, 344.0, color=NAVY, weight_pt=2.2)
    add_line(sld, "s26_br_l", 120.0, 178.0, 120.0, 344.0, color=TEAL, weight_pt=2.5)
    add_line(sld, "s26_br_r", 283.0, 178.0, 283.0, 344.0, color=STEEL_BLUE, weight_pt=2.5)

    add_label(
        sld, "s26_dev_sic", 56.0, 212.0, 128.0, 98.0,
        "4H-SiC MOSFET\n\n开关边沿 + 中小负载\n（芯片面积更小）",
        size=11.5, color=TEAL, bold=True, align=PP_ALIGN_CENTER, fill=TEAL_LIGHT, line=TEAL, line_pt=1.6,
    )
    add_label(
        sld, "s26_dev_igbt", 219.0, 212.0, 128.0, 98.0,
        "硅 IGBT\n\n稳态大电流分流\n（芯片成本更低）",
        size=11.5, color=NAVY, bold=True, align=PP_ALIGN_CENTER, fill=ICE_BLUE, line=NAVY, line_pt=1.6,
    )
    add_label(
        sld, "s26_cnote", 54.0, 386.0, 295.0, 92.0,
        "独立门极控制协同：先开 SiC 承担开通、再开 IGBT 分担稳态电流；关断前先关 IGBT，由 SiC 承担最终关断过程。",
        size=11.5, color=INK_DARK, align=PP_ALIGN_CENTER, fill=WHITE, line=ICE_BLUE,
    )

    # Right: Working Logic & Public Case Data (x=386..759)
    add_rect(sld, "s26_r1_bg", 386.0, 104.0, 373.0, 180.0, fill=WHITE, line=NAVY, line_pt=1.2)
    add_label(sld, "s26_r1_h", 386.0, 104.0, 373.0, 32.0, "  分区协同机制（效率与成本折中）", size=14.0, color=WHITE, bold=True, fill=NAVY)
    add_rich_box(
        sld, "s26_r1_t", 400.0, 146.0, 345.0, 130.0,
        [
            {"runs": [make_run("• 轻中载与开关过程 → 4H-SiC MOSFET 承担", size=13, color=TEAL, bold=True)], "space_after": 4},
            {"runs": [make_run("  发挥无 0.7 V 结压降与低开关损耗优势。", size=12, color=INK_DARK)], "space_after": 12},
            {"runs": [make_run("• 重载稳态大电流 → 硅 IGBT 并联分担", size=13, color=STEEL_BLUE, bold=True)], "space_after": 4},
            {"runs": [make_run("  减小高价 SiC 总芯片面积，在轻载效率、开关效率与成本之间取得平衡。", size=12, color=INK_DARK)]},
        ],
        margins=(0, 0, 0, 0),
    )

    add_rect(sld, "s26_r2_bg", 386.0, 304.0, 373.0, 192.0, fill=ICE_LIGHT, line=STEEL_BLUE, line_pt=1.2)
    add_label(sld, "s26_r2_h", 386.0, 304.0, 373.0, 32.0, "  公开工程方案参考（小鹏 X9）", size=14.0, color=NAVY, bold=True, fill=ICE_BLUE)
    add_label(sld, "s26_d_area", 404.0, 352.0, 160.0, 44.0, "约 1/3", size=30.0, color=RED, bold=True, align=PP_ALIGN_CENTER)
    add_label(sld, "s26_l_area", 404.0, 398.0, 160.0, 38.0, "SiC MOSFET 芯片面积\n占全 SiC 方案比例", size=11.5, color=INK_DARK, align=PP_ALIGN_CENTER)
    add_line(sld, "s26_mdiv", 572.0, 352.0, 572.0, 434.0, color=ICE_BLUE, weight_pt=1.5)
    add_label(sld, "s26_d_eff", 582.0, 352.0, 160.0, 44.0, "约 98.7%", size=30.0, color=TEAL, bold=True, align=PP_ALIGN_CENTER)
    add_label(sld, "s26_l_eff", 582.0, 398.0, 160.0, 38.0, "CLTC 工况逆变器效率\n与全 SiC 方案基本相当", size=11.5, color=INK_DARK, align=PP_ALIGN_CENTER)
    add_label(sld, "s26_r2_sub", 400.0, 452.0, 345.0, 32.0, "注：全硅方案同条件下效率参考约 96.3%。", size=11.0, color=MUTED, align=PP_ALIGN_CENTER)


# ==============================================================================
# SLIDE 27: 未来发展趋势 -> Right Sidebar Step 3: 3.系统：千伏平台
# ==============================================================================
def build_slide_27(sld: Any) -> None:
    set_no_transition(sld)
    add_top_nav_bar(sld, active_tab=5)
    add_right_sidebar(sld, "fut", FUT_STEPS, active_step=3, x_pos=797.1)

    add_label(
        sld, "s27_hdr", 38.0, 52.0, 721.0, 32.0,
        "  系统层面演进：电池平台电压迈向 1000 V 与 1500 V 级及以上器件",
        size=15.0, color=NAVY, bold=True, align=PP_ALIGN_LEFT, fill=ICE_BLUE,
    )

    # Three crisp horizontal architectural tiers ascending left-to-right (x=38..759)
    tiers = [
        (
            38.0, 290.0, 152.0,
            "第一代｜400 V 平台",
            "650 / 750 V",
            "常见器件耐压等级",
            "硅 IGBT 为主流方案\n受限于充电电流，快充功率提升遇瓶颈",
            ICE_LIGHT, ICE_BLUE, NAVY, STEEL_BLUE,
        ),
        (
            286.0, 210.0, 232.0,
            "第二代｜800 V 平台",
            "1200 V",
            "常见器件耐压等级",
            "4H-SiC MOSFET 成为优选\n缩短充电时间、降低线束与系统电流",
            WHITE, STEEL_BLUE, STEEL_BLUE, TEAL,
        ),
        (
            534.0, 124.0, 318.0,
            "下一代｜1000 V 千伏平台",
            "1500 V+",
            "对应器件耐压等级",
            "耐压要求提升至 1500 V 左右及以上\n\n工程实例：比亚迪千伏平台已采用 1500 V 级 SiC 器件",
            ICE_LIGHT, NAVY, NAVY, RED,
        ),
    ]
    for i, (tx, ty, th, t_gen, t_v, t_vl, t_sub, c_bg, c_hdr, c_htxt, c_v) in enumerate(tiers):
        tw = 225.0
        add_rect(sld, f"s27_box_{i}", tx, ty, tw, th, fill=c_bg, line=c_hdr, line_pt=1.5)
        h_tc = WHITE if c_hdr != ICE_BLUE else NAVY
        add_label(sld, f"s27_h_{i}", tx, ty, tw, 34.0, t_gen, size=14.0, color=h_tc, bold=True, align=PP_ALIGN_CENTER, fill=c_hdr)
        add_label(sld, f"s27_v_{i}", tx + 10.0, ty + 44.0, tw - 20.0, 42.0, t_v, size=30.0, color=c_v, bold=True, align=PP_ALIGN_CENTER)
        add_label(sld, f"s27_vl_{i}", tx + 10.0, ty + 84.0, tw - 20.0, 20.0, t_vl, size=11.0, color=MUTED, align=PP_ALIGN_CENTER)
        add_label(sld, f"s27_sub_{i}", tx + 14.0, ty + 108.0, tw - 28.0, th - 116.0, t_sub, size=11.5, color=INK_DARK, align=PP_ALIGN_CENTER)

    # Trend connecting arrows between top edges
    add_line(sld, "s27_a1", 266.0, 348.0, 282.0, 318.0, color=STEEL_BLUE, weight_pt=2.4, arrow_end=True)
    add_line(sld, "s27_a2", 514.0, 268.0, 530.0, 238.0, color=NAVY, weight_pt=2.4, arrow_end=True)

    # Bottom Engineering Note
    add_rect(sld, "s27_foot_bg", 38.0, 456.0, 721.0, 44.0, fill=NAVY, line=None)
    add_label(
        sld, "s27_foot_t", 52.0, 456.0, 694.0, 44.0,
        "电压提升驱动力：同等充电与驱动功率下提高母线电压可直接减小电流与焦耳热损耗，推动 SiC 器件向更高耐压演进。",
        size=12.5, color=WHITE, bold=True, align=PP_ALIGN_CENTER,
    )


# ==============================================================================
# SLIDE 28: 未来发展趋势 -> Right Sidebar Step 4: 4.器件演进总结 (Clean matrix, zero hype/sub errors)
# ==============================================================================
def build_slide_28(sld: Any) -> None:
    set_no_transition(sld)
    add_top_nav_bar(sld, active_tab=5)
    add_right_sidebar(sld, "fut", FUT_STEPS, active_step=4, x_pos=797.1)

    col_x = [38.0, 162.0, 332.0, 540.0]
    col_w = [124.0, 170.0, 208.0, 219.0]

    headers = ["对比维度", "传统硅功率 MOSFET", "硅 IGBT（配 Si FRD）", "4H-SiC MOSFET"]
    hdr_fills = [NAVY, MUTED, STEEL_BLUE, NAVY]
    for j in range(4):
        add_label(
            sld, f"s28_th_{j}", col_x[j], 54.0, col_w[j], 36.0, headers[j],
            size=13.0, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=hdr_fills[j], line=WHITE, line_pt=1.0,
        )

    rows = [
        (
            "导电方式",
            [make_run("仅电子（单极型）", size=11.5, color=MUTED)],
            [make_run("电子 + 空穴（电导调制）", size=11.5, color=INK_DARK)],
            [make_run("仅电子（宽禁带单极型）", size=11.5, color=NAVY, bold=True)],
        ),
        (
            "场强与漂移区",
            [make_run("约 0.3 MV/cm · 高压漂移区较厚", size=11.2, color=MUTED)],
            [make_run("约 0.3 MV/cm · 1200V 理想约 80 μm", size=11.2, color=INK_DARK, bold=True)],
            [make_run("约 3.0 MV/cm (10×) · 约 8–10 μm", size=11.2, color=TEAL, bold=True)],
        ),
        (
            "导通特性",
            [
                make_run("R", size=11.5, color=MUTED, italic=True),
                make_run("on,sp", size=8.5, color=MUTED, sub=True),
                make_run(" ∝ BV", size=11.5, color=MUTED),
                make_run("2.5", size=8.5, color=MUTED, sup=True),
                make_run("，随耐压上升", size=11.5, color=MUTED),
            ],
            [make_run("含约 0.7 V 结压降，大电流压降低", size=11.5, color=INK_DARK, bold=True)],
            [make_run("过原点近似电阻，中小载损耗低", size=11.5, color=TEAL, bold=True)],
        ),
        (
            "关断与开关损耗",
            [make_run("无拖尾电流，开关较快", size=11.5, color=MUTED)],
            [
                make_run("少子复合拖尾，E", size=11.5, color=INK_DARK),
                make_run("off", size=8.5, color=INK_DARK, sub=True),
                make_run(" 随温度增大", size=11.5, color=INK_DARK),
            ],
            [
                make_run("无拖尾电流，E", size=11.5, color=RED, bold=True),
                make_run("off", size=8.5, color=RED, bold=True, sub=True),
                make_run(" 比 IGBT 低约 85%", size=11.5, color=RED, bold=True),
            ],
        ),
        (
            "续流与反向恢复",
            [
                make_run("体二极管 Q", size=11.5, color=MUTED),
                make_run("rr", size=8.5, color=MUTED, sub=True),
                make_run(" 较大", size=11.5, color=MUTED),
            ],
            [
                make_run("外并硅 FRD，Q", size=11.5, color=INK_DARK),
                make_run("rr", size=8.5, color=INK_DARK, sub=True),
                make_run(" 较大", size=11.5, color=INK_DARK),
            ],
            [
                make_run("同步整流；外并 SBD 时 E", size=11.5, color=RED, bold=True),
                make_run("rr", size=8.5, color=RED, bold=True, sub=True),
                make_run(" 低约 91%", size=11.5, color=RED, bold=True),
            ],
        ),
        (
            "频率与工程配套",
            [make_run("多用于低压高频场合", size=11.5, color=MUTED)],
            [make_run("约 10 kHz · 工艺与驱动成熟", size=11.0, color=INK_DARK)],
            [make_run("20 kHz 以上 · 对驱动与散热要求更高", size=11.0, color=NAVY, bold=True)],
        ),
        (
            "工程适用区间",
            [make_run("高压下耐压与低导通难兼得", size=11.2, color=MUTED)],
            [make_run("400 V 平台常见 / 成本优势明显", size=11.2, color=INK_DARK, bold=True)],
            [make_run("800–1000 V 平台 / 随 8 英寸扩产降本", size=11.2, color=NAVY, bold=True)],
        ),
    ]

    rh = 50.0
    for i, (dim, r_mos, r_igbt, r_sic) in enumerate(rows):
        ry = 90.0 + i * rh
        bg = WHITE if i % 2 == 0 else ICE_LIGHT
        add_label(
            sld, f"s28_r{i}_c0", col_x[0], ry, col_w[0], rh, dim,
            size=12.0, color=NAVY, bold=True, align=PP_ALIGN_CENTER, fill=ICE_BLUE, line=BORDER_GRAY, line_pt=0.75,
        )
        add_rich_box(
            sld, f"s28_r{i}_c1", col_x[1], ry, col_w[1], rh,
            [{"runs": r_mos, "align": PP_ALIGN_CENTER}],
            fill=bg, line=BORDER_GRAY, line_pt=0.75, default_align=PP_ALIGN_CENTER,
        )
        add_rich_box(
            sld, f"s28_r{i}_c2", col_x[2], ry, col_w[2], rh,
            [{"runs": r_igbt, "align": PP_ALIGN_CENTER}],
            fill=bg, line=BORDER_GRAY, line_pt=0.75, default_align=PP_ALIGN_CENTER,
        )
        add_rich_box(
            sld, f"s28_r{i}_c3", col_x[3], ry, col_w[3], rh,
            [{"runs": r_sic, "align": PP_ALIGN_CENTER}],
            fill=TEAL_LIGHT if i in (2, 3, 4) else bg, line=BORDER_GRAY, line_pt=0.75, default_align=PP_ALIGN_CENTER,
        )

    takeaway = add_label(
        sld, "s28_takeaway", 38.0, 452.0, 721.0, 52.0,
        "总结：器件从硅 MOSFET 演进到硅 IGBT 再到 4H-SiC MOSFET，本质上是围绕耐压、导通、开关与续流四项要求，\n不断突破材料与结构限制、在效率与成本之间持续推进的过程。",
        size=12.8, color=WHITE, bold=True, align=PP_ALIGN_CENTER, fill=NAVY, line=NAVY,
    )
    anim_group(sld, [takeaway], effect=EFF_FADE, duration=0.45, first_trigger=TRIG_ON_CLICK)


# ==============================================================================
# SLIDE 29 (NEW): 参考文献与感谢观看 (Closing bookend matching Cover Slide 1)
# ==============================================================================
def build_slide_29_refs_thanks(sld: Any) -> None:
    set_no_transition(sld)

    # Matching Slide 1 left vertical ice-blue margin strip & top deep-navy hero banner
    add_rect(sld, "s29_lstrip", 0.0, 0.0, 22.4, 540.0, fill=ICE_BLUE, line=None)
    add_rect(sld, "s29_banner", 22.4, 0.0, 937.6, 144.0, fill=NAVY, line=None)

    add_label(
        sld, "s29_thanks", 56.0, 28.0, 600.0, 54.0,
        "感谢观看 · 敬请老师指正",
        size=34.0, color=WHITE, bold=True, align=PP_ALIGN_LEFT,
    )
    add_label(
        sld, "s29_sub", 56.0, 88.0, 600.0, 28.0,
        "先进半导体器件在新能源汽车主驱逆变器的应用",
        size=14.0, color=ICE_BLUE, align=PP_ALIGN_LEFT,
    )
    add_label(
        sld, "s29_author", 670.0, 52.0, 250.0, 36.0,
        "集成电路学院    周春佳",
        size=16.0, color=WHITE, align=PP_ALIGN_RIGHT,
    )

    # References section header
    add_rect(sld, "s29_rbar", 56.0, 166.0, 4.5, 24.0, fill=STEEL_BLUE, line=None)
    add_label(
        sld, "s29_rhdr", 68.0, 164.0, 500.0, 28.0,
        "主要参考文献与资料来源",
        size=14.5, color=NAVY, bold=True, align=PP_ALIGN_LEFT,
    )
    add_line(sld, "s29_rdiv", 56.0, 198.0, 924.0, 198.0, color=ICE_BLUE, weight_pt=1.2)

    refs_left = [
        ("[1] ", "B. J. Baliga, Fundamentals of Power Semiconductor Devices, Springer.（硅 MOSFET 比导通电阻与耐压关系及功率器件物理基础）"),
        ("[2] ", "Texas Instruments, 永磁同步电机电流控制应用笔记 (SPRABQ2)、单相逆变器参考设计 (TIDUB21D) 与半桥死区应用笔记 (SLVA714D)."),
        ("[3] ", "Toshiba Electronic Devices & Storage Corp., IGBT 关断拖尾电流技术说明 (igbt-010); MDPI World Electr. Veh. J., vol. 14, no. 4, 112.（800 V / 10 kHz 逆变器台架）"),
        ("[4] ", "Proc. Jpn. Acad., Ser. B, vol. 96, no. 7（Si 与 4H-SiC 材料参数表）; MDPI Electronics, vol. 12, no. 11, 2551.（1200 V / 10 μm SiC 漂移层器件）"),
        ("[5] ", "Wang et al., IEEE ECCE, 2013, Table 1.（1200 V / 100 A 模块 600 V · 100 A · 125 ℃ 双脉冲关断能量与反向恢复对比）"),
    ]
    refs_right = [
        ("[6] ", "SEMI Webinar (Dave Kirsch), \"The SiC Value Chain Prepares for Mass Adoption,\" Apr. 2024; RSC CrystEngComm (d4ce01206b), 2025.（SiC 衬底外延成本结构与 150 mm 单晶生长）"),
        ("[7] ", "Infineon Technologies, SiC Modules Technical Overview（150 mm / 200 mm SiC 晶圆量产）; MDPI Energies, vol. 13, no. 5, 1122.（沟槽栅 SiC 电场屏蔽研究）"),
        ("[8] ", "Hybrid Si/SiC EV Traction Inverter 公开发表论文（小鹏 X9 混合并联方案与 CLTC 效率）; 比亚迪 2025 千伏平台与 1500 V 级 SiC 器件官方公告."),
        ("[9] ", "行业参考资料：《车规芯片实战笔记 · 主驱逆变器》《一文了解 SiC 碳化硅 MOSFET 的应用及性能优势》; Texas Instruments（第 2 页主驱逆变器三维实景图）."),
    ]

    def build_ref_paras(items: list[tuple[str, str]]) -> list[dict[str, Any]]:
        return [
            {
                "runs": [
                    make_run(tag, size=10.2, color=NAVY, bold=True),
                    make_run(body, size=10.2, color=INK_DARK),
                ],
                "space_after": 9,
                "line_spacing": 1.15,
            }
            for tag, body in items
        ]

    add_rich_box(
        sld, "s29_refs_l", 56.0, 208.0, 416.0, 304.0,
        build_ref_paras(refs_left), v_anchor=1, margins=(2, 2, 2, 2),
    )
    add_rich_box(
        sld, "s29_refs_r", 496.0, 208.0, 428.0, 304.0,
        build_ref_paras(refs_right), v_anchor=1, margins=(2, 2, 2, 2),
    )


def audit_slides(pres: Any) -> None:
    """Assert 29 slides, zero banned words / raw _ or ^ on Slides 2 & 13-29, zero transitions on Slides 13-29."""
    assert pres.Slides.Count == 29, f"Expected 29 slides, found {pres.Slides.Count}"
    slide2_names = {pres.Slides(2).Shapes(i).Name for i in range(1, pres.Slides(2).Shapes.Count + 1)}
    assert "s2_ti_photo" in slide2_names, "Slide 2 missing embedded TI photo s2_ti_photo"

    check_indices = [2] + list(range(13, 30))
    for s_idx in check_indices:
        sld = pres.Slides(s_idx)
        if s_idx >= 13:
            assert sld.SlideShowTransition.EntryEffect == 0, f"Slide {s_idx} has non-zero EntryEffect"
        for sh_i in range(1, sld.Shapes.Count + 1):
            sh = sld.Shapes(sh_i)
            if sh.HasTextFrame and sh.TextFrame.HasText:
                txt = sh.TextFrame.TextRange.Text
                for bw in BANNED_WORDS:
                    if bw in txt:
                        raise AssertionError(f"Slide {s_idx} ({sh.Name}) contains banned word {bw!r}: {txt!r}")
                if "_" in txt or "^" in txt:
                    raise AssertionError(f"Slide {s_idx} ({sh.Name}) contains raw sub/superscript char: {txt!r}")
    print("HYGIENE AUDIT PASSED (29 slides, Slide 2 photo ok, 0 banned words, 0 transitions on Slides 13-29)")


def main() -> None:
    if not BACKUP_PPTX.is_file():
        raise FileNotFoundError(f"Original backup not found: {BACKUP_PPTX}")

    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    for old_png in PREVIEW_DIR.glob("*.png"):
        old_png.unlink()

    work_pptx = ROOT_DIR / "ppt_builder" / "working_user_style_v4.pptx"
    shutil.copy2(BACKUP_PPTX, work_pptx)
    unwrap_notes_alternate_content(work_pptx)

    app = win32.gencache.EnsureDispatch("PowerPoint.Application")
    app.Visible = True
    pres = app.Presentations.Open(str(work_pptx), ReadOnly=False, Untitled=False, WithWindow=True)

    try:
        # Remove original backup slides 12..17 so only Original Slides 1..11 remain
        for idx in range(pres.Slides.Count, 11, -1):
            pres.Slides(idx).Delete()

        patch_slides_1_to_11(pres)

        # Duplicate Original Slide 2 -> Move to index 2 as New Slide 2 (shifts Original 2..11 to 3..12)
        pres.Slides(2).Duplicate()
        pres.Slides(3).MoveTo(2)
        print("Building Slide 2/29 (TI EV traction inverter overview)...")
        build_slide_2_ti_photo(pres.Slides(2))

        builders = [
            (13, build_slide_12),
            (14, build_slide_13),
            (15, build_slide_14),
            (16, build_slide_15),
            (17, build_slide_16),
            (18, build_slide_17),
            (19, build_slide_18),
            (20, build_slide_19),
            (21, build_slide_20),
            (22, build_slide_21),
            (23, build_slide_22),
            (24, build_slide_24_sic_cost_limits),
            (25, build_slide_25),
            (26, build_slide_26),
            (27, build_slide_27),
            (28, build_slide_28),
            (29, build_slide_29_refs_thanks),
        ]

        for s_num, fn in builders:
            print(f"Building Slide {s_num}/29...")
            sld = pres.Slides.Add(s_num, PP_LAYOUT_BLANK)
            fn(sld)

        audit_slides(pres)
        inject_notes_into_presentation(pres)

        pres.Save()
        pres.SaveCopyAs(str(OUT_USER_PPTX))
        pres.SaveCopyAs(str(OUT_CN_PPTX))

        for s_idx in [1, 2, 3] + list(range(13, 30)):
            out_png = PREVIEW_DIR / f"slide_{s_idx:02d}.png"
            pres.Slides(s_idx).Export(str(out_png), "PNG", 1920, 1080)
            print(f"Exported preview: {out_png}")

    finally:
        pres.Close()

    print(f"SUCCESS: Saved 29-slide deck to {OUT_USER_PPTX} and {OUT_CN_PPTX}")


if __name__ == "__main__":
    main()
