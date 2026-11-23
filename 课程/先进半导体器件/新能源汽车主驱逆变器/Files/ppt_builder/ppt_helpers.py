"""Shared PowerPoint COM drawing, typography, chart, and animation primitives."""

from __future__ import annotations

from typing import Any

CM_TO_PT = 72.0 / 2.54  # 28.3464566929
SLIDE_W_CM = 33.867
SLIDE_H_CM = 19.05
SLIDE_W_PT = 960.0
SLIDE_H_PT = 540.0

# Exact Global Design Spec Palette
WHITE = "#FFFFFF"
PANEL_BG = "#F4F6F9"
PANEL_BORDER = "#D9DEE5"
TEXT_MAIN = "#1B2430"
TEXT_SUB = "#6B7785"

SI_COLOR = "#4A5A70"
SI_LIGHT = "#EAEFF5"
SIC_COLOR = "#0F9D8A"
SIC_LIGHT = "#E3F5F2"
COST_COLOR = "#E8743B"
COST_LIGHT = "#FDEBE3"
AMBER = "#F2A900"
AMBER_LIGHT = "#FFF6DC"

# Semiconductor & Carrier Colors
N_MINUS = "#DCE8F8"
N_PLUS = "#9DB8E8"
P_BODY = "#F6D5DE"
P_PLUS = "#F2B8C6"
METAL = "#9AA5B1"
GATE_POLY = "#5A6573"
GATE_OX = "#FFF3C4"
CHANNEL = "#2563EB"
DRIFT_HL = "#7C9CE0"
ELECTRON = "#2563EB"
HOLE = "#D6336C"

# Fonts
FONT_UI = "微软雅黑"
FONT_MATH = "Cambria Math"

# PowerPoint Shape & Text Constants
MSO_SHAPE_RECTANGLE = 1
MSO_SHAPE_ROUNDED_RECTANGLE = 5
MSO_SHAPE_RIGHT_TRIANGLE = 8
MSO_SHAPE_OVAL = 9
MSO_SHAPE_ISOSCELES_TRIANGLE = 7
MSO_SHAPE_RIGHT_ARROW = 33
MSO_SHAPE_DOWN_ARROW = 36
MSO_SHAPE_UP_ARROW = 35
MSO_SHAPE_LEFT_ARROW = 34
MSO_SHAPE_TRAPEZOID = 16

MSO_TEXTBOX = 17
MSO_LINE_SOLID = 1
MSO_LINE_DASH = 4
MSO_LINE_SQUARE_DOT = 2

MSO_ARROWHEAD_NONE = 1
MSO_ARROWHEAD_TRIANGLE = 2
MSO_ARROWHEAD_STEALTH = 5

MSO_EDITING_AUTO = 0
MSO_SEGMENT_LINE = 0

# Alignment
PP_ALIGN_LEFT = 1
PP_ALIGN_CENTER = 2
PP_ALIGN_RIGHT = 3

MSO_ANCHOR_TOP = 1
MSO_ANCHOR_MIDDLE = 3
MSO_ANCHOR_BOTTOM = 4

# Verified Office 16.0 Animation Constants
MSO_ANIM_EFFECT_APPEAR = 1
MSO_ANIM_EFFECT_FADE = 10
MSO_ANIM_EFFECT_WIPE = 22
MSO_ANIM_EFFECT_FLASH_BULB = 75
MSO_ANIM_EFFECT_MEDIA_PLAY = 83
MSO_ANIM_EFFECT_PATH_USER = 149

MSO_ANIM_DIR_TOP = 1
MSO_ANIM_DIR_RIGHT = 2
MSO_ANIM_DIR_BOTTOM = 3
MSO_ANIM_DIR_LEFT = 4

TRIG_CLICK = 1
TRIG_WITH_PREV = 2
TRIG_AFTER_PREV = 3

PP_EFFECT_FADE_SMOOTHLY = 3849

CHAPTERS = ["原理", "要求", "硅 IGBT", "SiC", "展望"]


def cm(val: float) -> float:
    """Convert centimeters to PowerPoint points."""
    return float(val) * CM_TO_PT


def rgb(hex_color: str) -> int:
    """Convert #RRGGBB hex string into PowerPoint COM BGR integer."""
    h = hex_color.lstrip("#")
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)
    return r + (g << 8) + (b << 16)


def clean_shape(shp: Any) -> Any:
    """Strip default Office shadows, 3D effects, and enable clean text wrapping."""
    try:
        shp.Shadow.Visible = 0
    except Exception:
        pass
    try:
        shp.ThreeD.Visible = 0
    except Exception:
        pass
    try:
        shp.Reflection.Type = 0
    except Exception:
        pass
    try:
        shp.Glow.Radius = 0
    except Exception:
        pass
    try:
        shp.SoftEdge.Radius = 0
    except Exception:
        pass
    return shp


def set_round_radius(shp: Any, w_cm: float, h_cm: float, radius_cm: float = 0.2) -> None:
    """Set rounded rectangle corner radius accurately in cm."""
    m = min(w_cm, h_cm)
    if m <= 0:
        return
    frac = min(0.5, max(0.0, radius_cm / m))
    shp.Adjustments.SetItem(1, frac)


def set_rich_text(
    shp: Any,
    paragraphs: list[dict[str, Any]],
    align: int = PP_ALIGN_LEFT,
    valign: int = MSO_ANCHOR_MIDDLE,
    margin_cm: tuple[float, float, float, float] = (0.12, 0.12, 0.06, 0.06),
    line_spacing: float = 1.15,
    word_wrap: bool = True,
) -> Any:
    """Populate TextFrame2 with structured rich text runs supporting 微软雅黑, Cambria Math, sub/superscripts.

    paragraphs: list of dicts with keys:
      - runs: list of dicts {text, size, color, bold, italic, font, sub, sup}
      - align: optional override
      - space_after: pt
      - line_spacing: optional override
    """
    tf = shp.TextFrame2
    tf.WordWrap = -1 if word_wrap else 0
    tf.AutoSize = 0
    tf.MarginLeft = cm(margin_cm[0])
    tf.MarginRight = cm(margin_cm[1])
    tf.MarginTop = cm(margin_cm[2])
    tf.MarginBottom = cm(margin_cm[3])
    tf.VerticalAnchor = valign

    full_text_parts: list[str] = []
    span_specs: list[tuple[int, int, dict[str, Any]]] = []
    para_specs: list[dict[str, Any]] = []

    cursor = 1  # TextFrame2.TextRange.Characters is 1-based
    for p_idx, p in enumerate(paragraphs):
        runs = p.get("runs", [])
        for r in runs:
            txt = str(r["text"])
            if txt:
                full_text_parts.append(txt)
                span_specs.append((cursor, len(txt), r))
                cursor += len(txt)
        para_specs.append(p)
        if p_idx < len(paragraphs) - 1:
            full_text_parts.append("\r")
            cursor += 1

    tr = tf.TextRange
    tr.Text = "".join(full_text_parts)

    # Paragraph formatting
    for p_idx, p in enumerate(para_specs):
        p_obj = tr.GetParagraphs(p_idx + 1, 1).ParagraphFormat
        p_obj.Alignment = p.get("align", align)
        p_obj.LineRuleWithin = -1
        p_obj.SpaceWithin = p.get("line_spacing", line_spacing)
        if "space_after" in p:
            p_obj.SpaceAfter = float(p["space_after"])
        if "space_before" in p:
            p_obj.SpaceBefore = float(p["space_before"])

    # Run formatting
    for start, length, spec in span_specs:
        if length <= 0:
            continue
        sub_tr = tr.GetCharacters(start, length)
        font_name = spec.get("font", FONT_UI)
        size = float(spec.get("size", 18))
        bold = -1 if spec.get("bold", False) else 0
        italic = -1 if spec.get("italic", False) else 0
        color_hex = spec.get("color", TEXT_MAIN)
        is_sub = spec.get("sub", False)
        is_sup = spec.get("sup", False)

        f = sub_tr.Font
        f.Name = font_name
        f.NameAscii = font_name
        f.NameFarEast = FONT_UI if font_name == FONT_UI else font_name
        f.NameComplexScript = font_name
        f.Bold = bold
        f.Italic = italic
        f.Fill.Visible = -1
        f.Fill.Solid()
        f.Fill.ForeColor.RGB = rgb(color_hex)

        if is_sub:
            f.BaselineOffset = -0.25
            f.Size = max(10.0, round(size * 0.72, 1))
        elif is_sup:
            f.BaselineOffset = 0.30
            f.Size = max(10.0, round(size * 0.72, 1))
        else:
            f.BaselineOffset = 0.0
            f.Size = size

    return shp


def make_run(
    text: str,
    size: float = 18,
    color: str = TEXT_MAIN,
    bold: bool = False,
    italic: bool = False,
    font: str = FONT_UI,
    sub: bool = False,
    sup: bool = False,
) -> dict[str, Any]:
    return {
        "text": text,
        "size": size,
        "color": color,
        "bold": bold,
        "italic": italic,
        "font": font,
        "sub": sub,
        "sup": sup,
    }


def add_box(
    sld: Any,
    name: str,
    x: float,
    y: float,
    w: float,
    h: float,
    fill: str | None = WHITE,
    line: str | None = PANEL_BORDER,
    line_pt: float = 0.75,
    round_cm: float | None = None,
    transp: float = 0.0,
    dash: int | None = None,
    shape_type: int | None = None,
) -> Any:
    """Create a clean rectangle or rounded rectangle in cm."""
    if shape_type is None:
        st = MSO_SHAPE_ROUNDED_RECTANGLE if round_cm is not None else MSO_SHAPE_RECTANGLE
    else:
        st = shape_type
    shp = sld.Shapes.AddShape(st, cm(x), cm(y), cm(w), cm(h))
    clean_shape(shp)
    shp.Name = name
    if round_cm is not None and st == MSO_SHAPE_ROUNDED_RECTANGLE:
        set_round_radius(shp, w, h, round_cm)
    if fill is not None:
        shp.Fill.Visible = -1
        shp.Fill.Solid()
        shp.Fill.ForeColor.RGB = rgb(fill)
        shp.Fill.Transparency = float(transp)
    else:
        shp.Fill.Visible = 0
    if line is not None:
        shp.Line.Visible = -1
        shp.Line.ForeColor.RGB = rgb(line)
        shp.Line.Weight = float(line_pt)
        if dash is not None:
            shp.Line.DashStyle = dash
    else:
        shp.Line.Visible = 0
    return shp


def add_oval(
    sld: Any,
    name: str,
    cx: float,
    cy: float,
    d: float,
    fill: str | None = WHITE,
    line: str | None = None,
    line_pt: float = 1.5,
    transp: float = 0.0,
) -> Any:
    """Create a circle centered at (cx, cy) with diameter d (cm)."""
    shp = sld.Shapes.AddShape(MSO_SHAPE_OVAL, cm(cx - d / 2.0), cm(cy - d / 2.0), cm(d), cm(d))
    clean_shape(shp)
    shp.Name = name
    if fill is not None:
        shp.Fill.Visible = -1
        shp.Fill.Solid()
        shp.Fill.ForeColor.RGB = rgb(fill)
        shp.Fill.Transparency = float(transp)
    else:
        shp.Fill.Visible = 0
    if line is not None:
        shp.Line.Visible = -1
        shp.Line.ForeColor.RGB = rgb(line)
        shp.Line.Weight = float(line_pt)
    else:
        shp.Line.Visible = 0
    return shp


def add_textbox(
    sld: Any,
    name: str,
    x: float,
    y: float,
    w: float,
    h: float,
    paragraphs: list[dict[str, Any]],
    align: int = PP_ALIGN_LEFT,
    valign: int = MSO_ANCHOR_MIDDLE,
    margin_cm: tuple[float, float, float, float] = (0.04, 0.04, 0.0, 0.0),
    line_spacing: float = 1.15,
    fill: str | None = None,
    line: str | None = None,
    line_pt: float = 0.75,
    round_cm: float | None = None,
    transp: float = 0.0,
    word_wrap: bool = True,
) -> Any:
    """Create a textbox (using MSO_SHAPE_RECTANGLE when transparent so AutoSize never collapses Height)."""
    shp = add_box(
        sld,
        name,
        x,
        y,
        w,
        h,
        fill=fill,
        line=line,
        line_pt=line_pt,
        round_cm=round_cm,
        transp=transp,
    )
    set_rich_text(
        shp,
        paragraphs,
        align=align,
        valign=valign,
        margin_cm=margin_cm,
        line_spacing=line_spacing,
        word_wrap=word_wrap,
    )
    return shp


def add_simple_label(
    sld: Any,
    name: str,
    x: float,
    y: float,
    w: float,
    h: float,
    text: str,
    size: float = 14,
    color: str = TEXT_MAIN,
    bold: bool = False,
    italic: bool = False,
    font: str = FONT_UI,
    align: int = PP_ALIGN_LEFT,
    valign: int = MSO_ANCHOR_MIDDLE,
    fill: str | None = None,
    line: str | None = None,
    line_pt: float = 0.75,
    round_cm: float | None = None,
    margin_cm: tuple[float, float, float, float] = (0.04, 0.04, 0.0, 0.0),
    line_spacing: float = 1.15,
    word_wrap: bool = True,
) -> Any:
    return add_textbox(
        sld,
        name,
        x,
        y,
        w,
        h,
        [{"runs": [make_run(text, size=size, color=color, bold=bold, italic=italic, font=font)]}],
        align=align,
        valign=valign,
        margin_cm=margin_cm,
        line_spacing=line_spacing,
        fill=fill,
        line=line,
        line_pt=line_pt,
        round_cm=round_cm,
        word_wrap=word_wrap,
    )


def add_line_seg(
    sld: Any,
    name: str,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    color: str = TEXT_MAIN,
    weight_pt: float = 1.5,
    dash: int | None = None,
    arrow_end: bool = False,
    arrow_start: bool = False,
) -> Any:
    """Create a straight connector/line in cm."""
    shp = sld.Shapes.AddLine(cm(x1), cm(y1), cm(x2), cm(y2))
    clean_shape(shp)
    shp.Name = name
    shp.Line.Visible = -1
    shp.Line.ForeColor.RGB = rgb(color)
    shp.Line.Weight = float(weight_pt)
    if dash is not None:
        shp.Line.DashStyle = dash
    if arrow_end:
        shp.Line.EndArrowheadStyle = MSO_ARROWHEAD_TRIANGLE
    if arrow_start:
        shp.Line.BeginArrowheadStyle = MSO_ARROWHEAD_TRIANGLE
    return shp


def add_polyline(
    sld: Any,
    name: str,
    pts_cm: list[tuple[float, float]],
    color: str | None = TEXT_MAIN,
    weight_pt: float = 2.0,
    dash: int | None = None,
    arrow_end: bool = False,
    arrow_start: bool = False,
    fill_color: str | None = None,
    fill_transp: float = 0.0,
    closed: bool = False,
) -> Any:
    """Build a crisp polyline or closed polygon via BuildFreeform."""
    x0, y0 = pts_cm[0]
    fb = sld.Shapes.BuildFreeform(MSO_EDITING_AUTO, cm(x0), cm(y0))
    for x, y in pts_cm[1:]:
        fb.AddNodes(MSO_SEGMENT_LINE, MSO_EDITING_AUTO, cm(x), cm(y))
    if closed and pts_cm[-1] != pts_cm[0]:
        fb.AddNodes(MSO_SEGMENT_LINE, MSO_EDITING_AUTO, cm(x0), cm(y0))
    shp = fb.ConvertToShape()
    clean_shape(shp)
    shp.Name = name
    if fill_color is not None:
        shp.Fill.Visible = -1
        shp.Fill.Solid()
        shp.Fill.ForeColor.RGB = rgb(fill_color)
        shp.Fill.Transparency = float(fill_transp)
    else:
        shp.Fill.Visible = 0
    if color is not None:
        shp.Line.Visible = -1
        shp.Line.ForeColor.RGB = rgb(color)
        shp.Line.Weight = float(weight_pt)
        if dash is not None:
            shp.Line.DashStyle = dash
        if arrow_end:
            shp.Line.EndArrowheadStyle = MSO_ARROWHEAD_TRIANGLE
        if arrow_start:
            shp.Line.BeginArrowheadStyle = MSO_ARROWHEAD_TRIANGLE
    else:
        shp.Line.Visible = 0
    return shp


def add_bracket(
    sld: Any,
    name: str,
    x1: float,
    x2: float,
    y: float,
    h_tick: float = 0.22,
    up: bool = True,
    color: str = SI_COLOR,
    weight_pt: float = 1.25,
) -> Any:
    """Create a clean horizontal dimension bracket [x1, x2] at baseline y."""
    dy = -h_tick if up else h_tick
    pts = [(x1, y + dy), (x1, y), (x2, y), (x2, y + dy)]
    return add_polyline(sld, name, pts, color=color, weight_pt=weight_pt)


def group_shapes(sld: Any, shapes: list[Any], group_name: str) -> Any:
    """Group shapes cleanly and assign final semantic group_name."""
    if len(shapes) == 1:
        shapes[0].Name = group_name
        return shapes[0]
    names = [s.Name for s in shapes]
    grp = sld.Shapes.Range(names).Group()
    clean_shape(grp)
    grp.Name = group_name
    return grp


def add_table_row_group(
    sld: Any,
    group_name: str,
    x: float,
    y: float,
    col_widths: list[float],
    row_height: float,
    cells: list[list[dict[str, Any]]],
    fill_colors: list[str] | None = None,
    default_fill: str = WHITE,
    border_color: str = PANEL_BORDER,
    border_pt: float = 0.75,
    aligns: list[int] | None = None,
    margin_cm: tuple[float, float, float, float] = (0.16, 0.14, 0.04, 0.04),
) -> Any:
    """Build one table row as rectangle cells and group them so the row can animate independently."""
    cx = x
    shapes = []
    for idx, (w, runs) in enumerate(zip(col_widths, cells)):
        bg = fill_colors[idx] if fill_colors is not None else default_fill
        al = aligns[idx] if aligns is not None else PP_ALIGN_LEFT
        cell = add_textbox(
            sld,
            f"{group_name}_c{idx + 1}",
            cx,
            y,
            w,
            row_height,
            [{"runs": runs}],
            align=al,
            valign=MSO_ANCHOR_MIDDLE,
            margin_cm=margin_cm,
            fill=bg,
            line=border_color,
            line_pt=border_pt,
        )
        shapes.append(cell)
        cx += w
    return group_shapes(sld, shapes, group_name)


def add_req_badge(sld: Any, name: str, num: int, x: float, y: float, d: float = 0.8) -> Any:
    """Create numbered requirement badge ①..④ (0.8 cm circle, #1B2430, white 14 pt bold)."""
    shp = sld.Shapes.AddShape(MSO_SHAPE_OVAL, cm(x), cm(y), cm(d), cm(d))
    clean_shape(shp)
    shp.Name = name
    shp.Fill.Visible = -1
    shp.Fill.Solid()
    shp.Fill.ForeColor.RGB = rgb(TEXT_MAIN)
    shp.Line.Visible = 0
    set_rich_text(
        shp,
        [{"runs": [make_run(str(num), size=14, color=WHITE, bold=True)]}],
        align=PP_ALIGN_CENTER,
        valign=MSO_ANCHOR_MIDDLE,
        margin_cm=(0.0, 0.0, 0.0, 0.0),
    )
    return shp


def add_carrier_legend(sld: Any, page_num: int, x: float = 1.5, y: float = 17.95) -> Any:
    """Bottom-left carrier legend (electron solid blue dot + hole hollow magenta ring, 14 pt)."""
    e_dot = add_oval(sld, f"p{page_num}_leg_e_dot", x + 0.14, y + 0.30, 0.28, fill=ELECTRON, line=None)
    e_lbl = add_simple_label(
        sld, f"p{page_num}_leg_e_lbl", x + 0.36, y, 1.3, 0.60, "电子", size=14, color=TEXT_MAIN
    )
    h_dot = add_oval(sld, f"p{page_num}_leg_h_dot", x + 1.85 + 0.14, y + 0.30, 0.28, fill=WHITE, line=HOLE, line_pt=1.5)
    h_lbl = add_simple_label(
        sld, f"p{page_num}_leg_h_lbl", x + 2.22, y, 1.3, 0.60, "空穴", size=14, color=TEXT_MAIN
    )
    return group_shapes(sld, [e_dot, e_lbl, h_dot, h_lbl], f"p{page_num}_legend_1")


def set_slide_white_bg(sld: Any) -> None:
    sld.FollowMasterBackground = 0
    bg = sld.Background.Fill
    bg.Visible = -1
    bg.Solid()
    bg.ForeColor.RGB = rgb(WHITE)


def add_slide_chrome(
    sld: Any,
    page_num: int,
    title: str,
    active_chapter: str,
    title_y: float = 0.65,
    rule_y: float = 3.00,
    set_transition: bool = True,
) -> None:
    """Apply clean white background, 28 pt conclusion title, 5-stage progress pills, divider rule, page number."""
    set_slide_white_bg(sld)
    if set_transition:
        sld.SlideShowTransition.EntryEffect = PP_EFFECT_FADE_SMOOTHLY
        sld.SlideShowTransition.Duration = 0.5

    # Title (x=1.5, y=0.65..2.85, w=19.6 so it never collides with progress bar at x=21.5)
    add_simple_label(
        sld,
        f"p{page_num}_title_1",
        1.5,
        title_y,
        19.6,
        2.15,
        title,
        size=28,
        color=TEXT_MAIN,
        bold=True,
        align=PP_ALIGN_LEFT,
        valign=MSO_ANCHOR_MIDDLE,
        margin_cm=(0.0, 0.10, 0.0, 0.0),
        line_spacing=1.12,
    )

    # Top-right 5-chapter progress pills (x 21.5..32.4, y 0.90..1.60)
    widths = [1.85, 1.85, 2.55, 1.85, 1.85]  # sum = 9.95; 4 gaps * 0.2375 = 0.95 -> total 10.90 cm (21.5..32.4)
    gap = (10.90 - sum(widths)) / 4.0
    cx = 21.5
    active_fill_map = {
        "硅 IGBT": SI_COLOR,
        "SiC": SIC_COLOR,
    }
    for idx, (ch, w) in enumerate(zip(CHAPTERS, widths), start=1):
        is_act = ch == active_chapter
        bg = active_fill_map.get(ch, TEXT_MAIN) if is_act else PANEL_BG
        fg = WHITE if is_act else TEXT_SUB
        ln = bg if is_act else PANEL_BORDER
        add_simple_label(
            sld,
            f"p{page_num}_prog_{idx}",
            cx,
            0.90,
            w,
            0.70,
            ch,
            size=12,
            color=fg,
            bold=is_act,
            align=PP_ALIGN_CENTER,
            valign=MSO_ANCHOR_MIDDLE,
            fill=bg,
            line=ln,
            line_pt=0.75,
            round_cm=0.35,
            margin_cm=(0.04, 0.04, 0.02, 0.02),
            word_wrap=False,
        )
        cx += w + gap

    if rule_y is not None:
        add_line_seg(sld, f"p{page_num}_rule_1", 1.5, rule_y, 32.4, rule_y, color=PANEL_BORDER, weight_pt=0.75)

    # Bottom-right page number (12 pt, x 29.4..32.4, y 18.20..18.75)
    add_simple_label(
        sld,
        f"p{page_num}_pagenum_1",
        29.4,
        18.20,
        3.0,
        0.55,
        f"{page_num:02d} / 10",
        size=12,
        color=TEXT_SUB,
        align=PP_ALIGN_RIGHT,
        valign=MSO_ANCHOR_MIDDLE,
        margin_cm=(0.0, 0.0, 0.0, 0.0),
    )


# ---------------- Animation Primitives ----------------

def anim_fade(sld: Any, shp: Any, trigger: int = TRIG_CLICK, duration: float = 0.4, delay: float = 0.0) -> Any:
    eff = sld.TimeLine.MainSequence.AddEffect(shp, MSO_ANIM_EFFECT_FADE, 0, trigger)
    eff.Timing.Duration = float(duration)
    eff.Timing.TriggerDelayTime = float(delay)
    return eff


def anim_wipe(
    sld: Any,
    shp: Any,
    direction: int = MSO_ANIM_DIR_LEFT,
    trigger: int = TRIG_CLICK,
    duration: float = 0.6,
    delay: float = 0.0,
) -> Any:
    eff = sld.TimeLine.MainSequence.AddEffect(shp, MSO_ANIM_EFFECT_WIPE, 0, trigger)
    eff.EffectParameters.Direction = int(direction)
    eff.Timing.Duration = float(duration)
    eff.Timing.TriggerDelayTime = float(delay)
    return eff


def anim_appear(sld: Any, shp: Any, trigger: int = TRIG_CLICK, delay: float = 0.0) -> Any:
    eff = sld.TimeLine.MainSequence.AddEffect(shp, MSO_ANIM_EFFECT_APPEAR, 0, trigger)
    eff.Timing.TriggerDelayTime = float(delay)
    return eff


def anim_pulse(
    sld: Any, shp: Any, trigger: int = TRIG_AFTER_PREV, duration: float = 0.5, delay: float = 0.0
) -> Any:
    eff = sld.TimeLine.MainSequence.AddEffect(shp, MSO_ANIM_EFFECT_FLASH_BULB, 0, trigger)
    eff.Timing.Duration = float(duration)
    eff.Timing.TriggerDelayTime = float(delay)
    return eff


def anim_exit_fade(
    sld: Any, shp: Any, trigger: int = TRIG_WITH_PREV, duration: float = 0.4, delay: float = 0.0
) -> Any:
    eff = sld.TimeLine.MainSequence.AddEffect(shp, MSO_ANIM_EFFECT_FADE, 0, trigger)
    eff.Exit = -1
    eff.Timing.Duration = float(duration)
    eff.Timing.TriggerDelayTime = float(delay)
    return eff


def anim_motion_path(
    sld: Any,
    shp: Any,
    pts_cm: list[tuple[float, float]],
    trigger: int = TRIG_WITH_PREV,
    duration: float = 2.2,
    delay: float = 0.0,
    repeat: int = 2,
) -> Any:
    """Create linear polyline motion path relative to shape's initial center (pts_cm[0])."""
    x0, y0 = pts_cm[0]
    segs = ["M 0 0"]
    for x, y in pts_cm[1:]:
        dx = (x - x0) / SLIDE_W_CM
        dy = (y - y0) / SLIDE_H_CM
        segs.append(f"L {dx:.5f} {dy:.5f}")
    segs.append("E")
    path_str = " ".join(segs)

    eff = sld.TimeLine.MainSequence.AddEffect(shp, MSO_ANIM_EFFECT_PATH_USER, 0, trigger)
    eff.Behaviors.Item(1).MotionEffect.Path = path_str
    eff.Timing.Duration = float(duration)
    eff.Timing.TriggerDelayTime = float(delay)
    eff.Timing.SmoothStart = 0
    eff.Timing.SmoothEnd = 0
    eff.Timing.AutoReverse = 0
    eff.Timing.RepeatCount = int(repeat)
    return eff


def anim_media_play(sld: Any, shp: Any, trigger: int = TRIG_WITH_PREV, delay: float = 0.0) -> Any:
    eff = sld.TimeLine.MainSequence.AddEffect(shp, MSO_ANIM_EFFECT_MEDIA_PLAY, 0, trigger)
    eff.Timing.TriggerDelayTime = float(delay)
    return eff
