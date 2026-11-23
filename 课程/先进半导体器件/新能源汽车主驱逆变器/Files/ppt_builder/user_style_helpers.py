"""Helper primitives matching the user's exact visual language in 'advanced semiconductor device course pre.pptx'."""

from __future__ import annotations

from pathlib import Path
from typing import Any

# Canvas dimensions in points (16:9, 960 x 540 pt)
SLIDE_W = 960.0
SLIDE_H = 540.0
TOP_BAR_H = 23.7
SIDEBAR_W = 162.9
SIDEBAR_Y = 23.7
SIDEBAR_H = 516.3
STEP_BLOCK_H = 128.0

# User's exact palette
NAVY = (14, 40, 65)          # #0E2841 - primary structural deep navy
ICE_BLUE = (220, 234, 247)   # #DCEAF7 - secondary structural ice-blue
STEEL_BLUE = (31, 78, 121)   # #1F4E79 - technical accent / labels
LINE_BLUE = (33, 95, 154)    # #215F9A - signal arrows & electron path
RED = (192, 0, 0)            # #C00000 - penalty / limit / hole / highlight
BRIGHT_RED = (255, 0, 0)     # #FF0000 - vivid circuit highlight
RED_LIGHT = (253, 232, 232)  # #FDE8E8 - soft red tint background
ICE_LIGHT = (242, 246, 250)  # #F2F6FA - ultra-subtle cool surface
TEAL = (15, 118, 110)        # #0F766E - SiC / positive improvement accent
TEAL_LIGHT = (228, 245, 242) # #E4F5F2 - soft SiC tint
BLACK = (0, 0, 0)            # #000000 - primary ink
INK_DARK = (20, 35, 52)      # #142334 - body dark ink
MUTED = (89, 89, 89)         # #595959 - Tier-3 secondary caption gray
BORDER_GRAY = (191, 191, 191)# #BFBFBF - subtle inner grid line
WHITE = (255, 255, 255)      # #FFFFFF - pure canvas

# Unified semiconductor doping-concentration palette (N=blue, P=pink)
COL_N_PLUS = (58, 143, 214)      # #3A8FD6 - high doping N+
COL_N_SIC = (164, 216, 250)      # #A4D8FA - 4H-SiC medium-low N- drift
COL_N_MINUS = (216, 240, 255)    # #D8F0FF - Si low-doped N- drift
COL_P_PLUS = (217, 98, 136)      # #D96288 - high doping P+
COL_P_BODY = (245, 196, 212)     # #F5C4D4 - medium doping P
COL_SIO2 = (203, 230, 220)       # #CBE6DC - SiO2 gate oxide
COL_SIO2_STROKE = (44, 122, 104) # #2C7A68 - SiO2 stroke

# Fonts matching user's PPT
FONT_CN = "华文中宋"
FONT_LATIN = "Times New Roman"
FONT_MATH = "Cambria Math"

# PowerPoint COM constants
PP_LAYOUT_BLANK = 12
PP_EFFECT_MORPH = 3954

MSO_SHAPE_RECTANGLE = 1
MSO_SHAPE_ROUNDED_RECTANGLE = 5
MSO_SHAPE_OVAL = 9
MSO_SHAPE_RIGHT_TRIANGLE = 6
MSO_SHAPE_ISOSCELES_TRIANGLE = 5

PP_ALIGN_LEFT = 1
PP_ALIGN_CENTER = 2
PP_ALIGN_RIGHT = 3

MSO_ANCHOR_TOP = 1
MSO_ANCHOR_MIDDLE = 3

MSO_ARROW_NONE = 1
MSO_ARROW_TRIANGLE = 2
MSO_ARROW_OPEN = 3

MSO_LINE_SOLID = 1
MSO_LINE_DASH = 4

# Animation constants
EFF_APPEAR = 1
EFF_FADE = 10
EFF_WIPE = 22
EFF_MEDIA_PLAY = 83
EFF_PATH = 149

TRIG_ON_CLICK = 1
TRIG_WITH_PREV = 2
TRIG_AFTER_PREV = 3

WIPE_FROM_LEFT = 1
WIPE_FROM_RIGHT = 2
WIPE_FROM_TOP = 3
WIPE_FROM_BOTTOM = 4


def rgb(color: tuple[int, int, int]) -> int:
    r, g, b = color
    return int(r) + (int(g) << 8) + (int(b) << 16)


def set_morph_transition(sld: Any, duration: float = 1.5) -> None:
    tr = sld.SlideShowTransition
    tr.EntryEffect = PP_EFFECT_MORPH
    tr.Duration = float(duration)
    tr.AdvanceOnTime = 0
    tr.AdvanceOnClick = -1


def set_no_transition(sld: Any) -> None:
    tr = sld.SlideShowTransition
    tr.EntryEffect = 0
    tr.Duration = 0.0
    tr.AdvanceOnTime = 0
    tr.AdvanceOnClick = -1


def style_range(
    tr: Any,
    *,
    size: float = 14.0,
    color: tuple[int, int, int] = BLACK,
    bold: bool = False,
    italic: bool = False,
    font_cn: str = FONT_CN,
    font_latin: str = FONT_LATIN,
    baseline: float | None = None,
) -> None:
    f = tr.Font
    f.NameFarEast = font_cn
    f.NameAscii = font_latin
    f.NameOther = font_latin
    f.Name = font_latin
    f.Size = float(size)
    f.Bold = -1 if bold else 0
    f.Italic = -1 if italic else 0
    f.Fill.Visible = -1
    f.Fill.Solid()
    f.Fill.ForeColor.RGB = rgb(color)
    if baseline is not None:
        f.BaselineOffset = float(baseline)


def make_run(
    text: str,
    *,
    size: float = 14.0,
    color: tuple[int, int, int] = BLACK,
    bold: bool = False,
    italic: bool = False,
    font_cn: str = FONT_CN,
    font_latin: str = FONT_LATIN,
    sub: bool = False,
    sup: bool = False,
) -> dict[str, Any]:
    baseline = -0.25 if sub else (0.30 if sup else None)
    return {
        "text": text,
        "size": size,
        "color": color,
        "bold": bold,
        "italic": italic,
        "font_cn": font_cn,
        "font_latin": font_latin,
        "baseline": baseline,
    }


def apply_runs(
    shp: Any,
    paragraphs: list[dict[str, Any]],
    *,
    default_align: int = PP_ALIGN_LEFT,
) -> None:
    tf2 = shp.TextFrame2
    tf2.TextRange.Text = ""
    full_texts: list[str] = []
    for p in paragraphs:
        p_txt = "".join(r["text"] for r in p.get("runs", []))
        full_texts.append(p_txt)
    tf2.TextRange.Text = "\r".join(full_texts)

    char_cursor = 1
    for p_idx, p in enumerate(paragraphs):
        p_txt = full_texts[p_idx]
        p_len = len(p_txt)
        para_range = tf2.TextRange.GetParagraphs(p_idx + 1, 1)
        pf = para_range.ParagraphFormat
        pf.Alignment = p.get("align", default_align)
        if "space_after" in p:
            pf.SpaceAfter = float(p["space_after"])
        if "space_before" in p:
            pf.SpaceBefore = float(p["space_before"])
        if "line_spacing" in p:
            pf.SpaceWithin = float(p["line_spacing"])

        for r in p.get("runs", []):
            r_txt = r["text"]
            r_len = len(r_txt)
            if r_len > 0:
                ch_range = tf2.TextRange.GetCharacters(char_cursor, r_len)
                style_range(
                    ch_range,
                    size=r.get("size", 14.0),
                    color=r.get("color", BLACK),
                    bold=r.get("bold", False),
                    italic=r.get("italic", False),
                    font_cn=r.get("font_cn", FONT_CN),
                    font_latin=r.get("font_latin", FONT_LATIN),
                    baseline=r.get("baseline", None),
                )
            char_cursor += r_len
        char_cursor += 1  # step over '\r'


def add_rect(
    sld: Any,
    name: str,
    left: float,
    top: float,
    width: float,
    height: float,
    *,
    fill: tuple[int, int, int] | None = WHITE,
    line: tuple[int, int, int] | None = None,
    line_pt: float = 1.0,
    dash: int = MSO_LINE_SOLID,
) -> Any:
    shp = sld.Shapes.AddShape(MSO_SHAPE_RECTANGLE, float(left), float(top), float(width), float(height))
    shp.Name = name
    if fill is None:
        shp.Fill.Visible = 0
    else:
        shp.Fill.Visible = -1
        shp.Fill.Solid()
        shp.Fill.ForeColor.RGB = rgb(fill)
    if line is None:
        shp.Line.Visible = 0
    else:
        shp.Line.Visible = -1
        shp.Line.ForeColor.RGB = rgb(line)
        shp.Line.Weight = float(line_pt)
        shp.Line.DashStyle = dash
    return shp


def add_label(
    sld: Any,
    name: str,
    left: float,
    top: float,
    width: float,
    height: float,
    text: str,
    *,
    size: float = 14.0,
    color: tuple[int, int, int] = BLACK,
    bold: bool = False,
    italic: bool = False,
    font_cn: str = FONT_CN,
    font_latin: str = FONT_LATIN,
    align: int = PP_ALIGN_LEFT,
    v_anchor: int = MSO_ANCHOR_MIDDLE,
    fill: tuple[int, int, int] | None = None,
    line: tuple[int, int, int] | None = None,
    line_pt: float = 1.0,
    margins: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0),
    word_wrap: bool = True,
) -> Any:
    shp = add_rect(sld, name, left, top, width, height, fill=fill, line=line, line_pt=line_pt)
    tf2 = shp.TextFrame2
    tf2.AutoSize = 0
    tf2.WordWrap = -1 if word_wrap else 0
    tf2.VerticalAnchor = v_anchor
    ml, mr, mt, mb = margins
    tf2.MarginLeft = float(ml)
    tf2.MarginRight = float(mr)
    tf2.MarginTop = float(mt)
    tf2.MarginBottom = float(mb)
    tf2.TextRange.Text = text
    tf2.TextRange.ParagraphFormat.Alignment = align
    style_range(
        tf2.TextRange,
        size=size,
        color=color,
        bold=bold,
        italic=italic,
        font_cn=font_cn,
        font_latin=font_latin,
    )
    return shp


def add_rich_box(
    sld: Any,
    name: str,
    left: float,
    top: float,
    width: float,
    height: float,
    paragraphs: list[dict[str, Any]],
    *,
    fill: tuple[int, int, int] | None = None,
    line: tuple[int, int, int] | None = None,
    line_pt: float = 1.0,
    v_anchor: int = MSO_ANCHOR_MIDDLE,
    default_align: int = PP_ALIGN_LEFT,
    margins: tuple[float, float, float, float] = (6.0, 6.0, 4.0, 4.0),
    word_wrap: bool = True,
) -> Any:
    shp = add_rect(sld, name, left, top, width, height, fill=fill, line=line, line_pt=line_pt)
    tf2 = shp.TextFrame2
    tf2.AutoSize = 0
    tf2.WordWrap = -1 if word_wrap else 0
    tf2.VerticalAnchor = v_anchor
    ml, mr, mt, mb = margins
    tf2.MarginLeft = float(ml)
    tf2.MarginRight = float(mr)
    tf2.MarginTop = float(mt)
    tf2.MarginBottom = float(mb)
    apply_runs(shp, paragraphs, default_align=default_align)
    return shp


def add_line(
    sld: Any,
    name: str,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    color: tuple[int, int, int] = BLACK,
    weight_pt: float = 1.5,
    dash: int = MSO_LINE_SOLID,
    arrow_end: bool = False,
    arrow_start: bool = False,
) -> Any:
    ln = sld.Shapes.AddLine(float(x1), float(y1), float(x2), float(y2))
    ln.Name = name
    ln.Line.Visible = -1
    ln.Line.ForeColor.RGB = rgb(color)
    ln.Line.Weight = float(weight_pt)
    ln.Line.DashStyle = dash
    if arrow_end:
        ln.Line.EndArrowheadStyle = MSO_ARROW_TRIANGLE
    if arrow_start:
        ln.Line.BeginArrowheadStyle = MSO_ARROW_TRIANGLE
    return ln


def add_oval(
    sld: Any,
    name: str,
    left: float,
    top: float,
    width: float,
    height: float,
    *,
    fill: tuple[int, int, int] | None = LINE_BLUE,
    line: tuple[int, int, int] | None = None,
    line_pt: float = 1.5,
) -> Any:
    shp = sld.Shapes.AddShape(MSO_SHAPE_OVAL, float(left), float(top), float(width), float(height))
    shp.Name = name
    if fill is None:
        shp.Fill.Visible = 0
    else:
        shp.Fill.Visible = -1
        shp.Fill.Solid()
        shp.Fill.ForeColor.RGB = rgb(fill)
    if line is None:
        shp.Line.Visible = 0
    else:
        shp.Line.Visible = -1
        shp.Line.ForeColor.RGB = rgb(line)
        shp.Line.Weight = float(line_pt)
    return shp


def add_poly(
    sld: Any,
    name: str,
    points: list[tuple[float, float]],
    *,
    fill: tuple[int, int, int] | None = None,
    line: tuple[int, int, int] | None = None,
    line_pt: float = 1.5,
    closed: bool = True,
) -> Any:
    x0, y0 = points[0]
    ffb = sld.Shapes.BuildFreeform(0, float(x0), float(y0))
    for x, y in points[1:]:
        ffb.AddNodes(0, 0, float(x), float(y))
    if closed and points[-1] != points[0]:
        ffb.AddNodes(0, 0, float(x0), float(y0))
    shp = ffb.ConvertToShape()
    shp.Name = name
    if fill is None:
        shp.Fill.Visible = 0
    else:
        shp.Fill.Visible = -1
        shp.Fill.Solid()
        shp.Fill.ForeColor.RGB = rgb(fill)
    if line is None:
        shp.Line.Visible = 0
    else:
        shp.Line.Visible = -1
        shp.Line.ForeColor.RGB = rgb(line)
        shp.Line.Weight = float(line_pt)
    return shp


def add_top_nav_bar(sld: Any, active_tab: int) -> None:
    """Build the user's exact Morph top navigation bar (active_tab in 1..5)."""
    # Base navy strips matching user's exact shape names & coordinates
    add_rect(sld, "Rectangle 3", 162.9, 0.0, 797.1, TOP_BAR_H, fill=NAVY, line=None)
    add_rect(sld, "Rectangle 2", 0.0, 0.0, 162.9, TOP_BAR_H, fill=NAVY, line=None)

    tab_specs = [
        # (tab_index, pill_left, pill_w, text_name, text_str, text_left, text_w, font_latin)
        (1, 0.0, 162.9, "TextBox 6", "逆变器基本原理", 17.7, 127.6, FONT_CN),
        (2, 163.0, 184.3, "TextBox 9", "对开关器件的要求", 183.3, 143.8, FONT_CN),
        (3, 347.4, 184.3, "TextBox 1", "IGBT", 412.1, 54.9, FONT_LATIN),
        (4, 529.2, 184.3, "TextBox 7", "SiC MOSFET", 565.4, 111.9, FONT_LATIN),
        (5, 775.7, 184.3, "TextBox 11", "未来发展趋势", 812.1, 111.5, FONT_CN),
    ]

    # Moving ice-blue active pill ("Rectangle 5")
    _, pill_left, pill_w, _, _, _, _, _ = tab_specs[active_tab - 1]
    add_rect(sld, "Rectangle 5", pill_left, 0.0, pill_w, TOP_BAR_H, fill=ICE_BLUE, line=None)

    # All 5 text boxes (active at y=-1.5, inactive parked above at y=-40.0 for Morph slide-in/out)
    for idx, _, _, t_name, t_str, t_left, t_w, f_lat in tab_specs:
        t_top = -1.5 if idx == active_tab else -40.0
        add_label(
            sld,
            t_name,
            t_left,
            t_top,
            t_w,
            26.7,
            t_str,
            size=16.0,
            color=BLACK,
            bold=True,
            font_cn=FONT_CN,
            font_latin=f_lat,
            align=PP_ALIGN_CENTER,
            word_wrap=False,
        )


def add_left_sidebar(
    sld: Any,
    chapter_tag: str,
    steps: list[str],
    active_step: int,
    *,
    x_pos: float = 0.0,
) -> None:
    """Build the user's progressive Left Vertical Sidebar (Ice-Blue base, Deep Navy active step).

    Matches Slides 4-7: Steps 1..active_step are shown; steps 1..active_step-1 are ICE_BLUE with BLACK text,
    step active_step is NAVY with WHITE text.
    """
    add_rect(sld, f"LSB_Base_{chapter_tag}", x_pos, SIDEBAR_Y, SIDEBAR_W, SIDEBAR_H, fill=ICE_BLUE, line=None)

    for idx in range(1, active_step + 1):
        label_txt = steps[idx - 1]
        y_top = SIDEBAR_Y + (idx - 1) * STEP_BLOCK_H
        is_active = idx == active_step
        # Use a persistent shape name for the active dark-navy block so Morph glides it downward!
        shp_name = f"LSB_Active_{chapter_tag}" if is_active else f"LSB_Step_{chapter_tag}_{idx}"
        add_label(
            sld,
            shp_name,
            x_pos,
            y_top,
            SIDEBAR_W,
            STEP_BLOCK_H,
            label_txt,
            size=16.0,
            color=WHITE if is_active else BLACK,
            bold=True,
            align=PP_ALIGN_CENTER,
            fill=NAVY if is_active else ICE_BLUE,
            line=None,
            margins=(10.0, 10.0, 6.0, 6.0),
        )


def add_right_sidebar(
    sld: Any,
    chapter_tag: str,
    steps: list[str],
    active_step: int,
    *,
    x_pos: float = 797.1,
) -> None:
    """Build the user's progressive Right Vertical Sidebar (Deep Navy base, Ice-Blue active step).

    Matches Slides 8-11: Steps 1..active_step are shown; steps 1..active_step-1 are NAVY with WHITE text,
    step active_step is ICE_BLUE with BLACK text.
    """
    add_rect(sld, f"RSB_Base_{chapter_tag}", x_pos, SIDEBAR_Y, SIDEBAR_W, SIDEBAR_H, fill=NAVY, line=None)

    for idx in range(1, active_step + 1):
        label_txt = steps[idx - 1]
        y_top = SIDEBAR_Y + (idx - 1) * STEP_BLOCK_H
        is_active = idx == active_step
        shp_name = f"RSB_Active_{chapter_tag}" if is_active else f"RSB_Step_{chapter_tag}_{idx}"
        add_label(
            sld,
            shp_name,
            x_pos,
            y_top,
            SIDEBAR_W,
            STEP_BLOCK_H,
            label_txt,
            size=16.0,
            color=BLACK if is_active else WHITE,
            bold=True,
            align=PP_ALIGN_CENTER,
            fill=ICE_BLUE if is_active else NAVY,
            line=None,
            margins=(10.0, 10.0, 6.0, 6.0),
        )


def anim_group(
    sld: Any,
    shapes: list[Any],
    *,
    effect: int = EFF_FADE,
    duration: float = 0.45,
    first_trigger: int = TRIG_ON_CLICK,
    wipe_dir: int | None = None,
    delay: float = 0.0,
) -> None:
    """Animate a group of shapes where the first is triggered by first_trigger and the rest run WithPrevious."""
    seq = sld.TimeLine.MainSequence
    for i, shp in enumerate(shapes):
        if shp is None:
            continue
        trig = first_trigger if i == 0 else TRIG_WITH_PREV
        eff = seq.AddEffect(shp, effect, 0, trig)
        eff.Timing.Duration = float(duration)
        if delay > 0 and i == 0:
            eff.Timing.TriggerDelayTime = float(delay)
        if effect == EFF_WIPE and wipe_dir is not None:
            eff.EffectParameters.Direction = wipe_dir


def add_motion_path(
    sld: Any,
    shp: Any,
    vml_path: str,
    *,
    trigger: int = TRIG_WITH_PREV,
    duration: float = 1.6,
    delay: float = 0.0,
    repeat_count: int = 2,
) -> Any:
    seq = sld.TimeLine.MainSequence
    eff = seq.AddEffect(shp, EFF_PATH, 0, trigger)
    beh = eff.Behaviors.Item(1)
    beh.MotionEffect.Path = vml_path
    eff.Timing.Duration = float(duration)
    eff.Timing.TriggerDelayTime = float(delay)
    if repeat_count > 1:
        eff.Timing.RepeatCount = int(repeat_count)
    return eff


def add_embedded_video(
    sld: Any,
    name: str,
    mp4_path: Path | str,
    left: float,
    top: float,
    width: float,
    height: float,
    *,
    trigger: int = TRIG_ON_CLICK,
) -> Any:
    """Embed a local MP4 video, remove click-on-shape InteractiveSequences, and queue MainSequence MediaPlay."""
    p = Path(mp4_path)
    if not p.is_file():
        raise FileNotFoundError(f"Embedded video not found: {p}")
    shp = sld.Shapes.AddMediaObject2(str(p), False, True, float(left), float(top), float(width), float(height))
    shp.Name = name
    shp.Line.Visible = 0

    iseqs = sld.TimeLine.InteractiveSequences
    for s_idx in range(iseqs.Count, 0, -1):
        seq = iseqs.Item(s_idx)
        for e_idx in range(seq.Count, 0, -1):
            seq.Item(e_idx).Delete()

    mseq = sld.TimeLine.MainSequence
    eff = mseq.AddEffect(shp, EFF_MEDIA_PLAY, 0, trigger)
    return shp, eff
