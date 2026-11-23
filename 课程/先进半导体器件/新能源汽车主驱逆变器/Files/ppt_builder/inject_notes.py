"""Parse slide-by-slide speech markdown and inject formatted notes (with true math runs) into PowerPoint."""

from __future__ import annotations

from pathlib import Path
import re
import shutil
from typing import Any
import zipfile

import win32com.client as win32

from user_style_helpers import INK_DARK, PP_ALIGN_LEFT, STEEL_BLUE, apply_runs, make_run

ROOT_DIR = Path(r"c:\Users\Casper\Documents\Proj")
SPEECH_PAGED_MD = ROOT_DIR / "新能源汽车主驱逆变器_按页发言稿.md"
OUT_USER_PPTX = ROOT_DIR / "advanced semiconductor device course pre.pptx"
OUT_CN_PPTX = ROOT_DIR / "新能源汽车主驱逆变器_课堂汇报.pptx"
NOTES_VERIFY_PDF = ROOT_DIR / "ppt_builder" / "preview_v4" / "notes_verify.pdf"

FONT_NOTES_CN = "微软雅黑"
FONT_NOTES_LATIN = "Times New Roman"
FONT_NOTES_MATH = "Cambria Math"

CMD_MAP: dict[str, tuple[str, bool]] = {
    "cdot": ("·", False),
    "approx": ("≈", False),
    "ll": ("≪", False),
    "gg": ("≫", False),
    "propto": ("∝", False),
    "int": ("∫", False),
    "sigma": ("σ", True),
    "tau": ("τ", True),
    "circ": ("°", False),
    "%": ("%", False),
    ",": (" ", False),
}

FORBIDDEN_RAW_TOKENS = ("$", "\\", "{", "}", "_", "^")


def _read_arg(s: str, idx: int) -> tuple[str, int, bool]:
    """Read a braced argument `{...}`, a single command `\\cmd`, or a single char starting at `idx`."""
    n = len(s)
    while idx < n and s[idx] == " ":
        idx += 1
    if idx >= n:
        raise ValueError(f"Unexpected end of math expression: {s!r}")
    if s[idx] == "{":
        depth = 0
        start = idx + 1
        j = idx
        while j < n:
            if s[j] == "{":
                depth += 1
            elif s[j] == "}":
                depth -= 1
                if depth == 0:
                    return s[start:j], j + 1, True
            j += 1
        raise ValueError(f"Unclosed brace in math expression: {s!r}")
    if s[idx] == "\\":
        m = re.match(r"\\([A-Za-z]+|%|,)", s[idx:])
        if not m:
            raise ValueError(f"Invalid LaTeX token at {idx} in {s!r}")
        return m.group(0), idx + len(m.group(0)), False
    return s[idx], idx + 1, False


def _coalesce_runs(runs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge adjacent runs with identical formatting and verify single-codeunit safety."""
    merged: list[dict[str, Any]] = []
    style_keys = ("size", "color", "bold", "italic", "font_cn", "font_latin", "baseline")
    for r in runs:
        txt = r["text"]
        if not txt:
            continue
        if any(ord(ch) >= 0x10000 for ch in txt):
            raise ValueError(f"Non-BMP character in run {txt!r}; TextFrame2 GetCharacters expects BMP.")
        if merged and all(merged[-1][k] == r[k] for k in style_keys):
            merged[-1]["text"] += txt
        else:
            merged.append(dict(r))
    return merged


def _make_math_run(
    text: str,
    *,
    size: float,
    color: tuple[int, int, int],
    bold: bool,
    italic: bool,
    baseline: float | None,
    font_latin: str = FONT_NOTES_MATH,
) -> dict[str, Any]:
    return {
        "text": text,
        "size": size,
        "color": color,
        "bold": bold,
        "italic": italic,
        "font_cn": FONT_NOTES_CN,
        "font_latin": font_latin,
        "baseline": baseline,
    }


def _parse_math_segment(
    expr: str,
    *,
    size: float,
    color: tuple[int, int, int],
    bold: bool = False,
    italic_override: bool | None = None,
    baseline: float | None = None,
) -> list[dict[str, Any]]:
    """Recursively convert an inline LaTeX math string into formatted PowerPoint runs."""
    runs: list[dict[str, Any]] = []
    i = 0
    n = len(expr)

    while i < n:
        if expr.startswith(r"\frac", i):
            num, next_i, _ = _read_arg(expr, i + 5)
            den, next_i, _ = _read_arg(expr, next_i)
            if num == "1" and den == "2":
                runs.append(_make_math_run("½", size=size, color=color, bold=bold, italic=False, baseline=baseline))
                if next_i < n and expr[next_i].isalnum():
                    runs.append(_make_math_run(" ", size=size, color=color, bold=bold, italic=False, baseline=baseline))
            else:
                runs.extend(
                    _parse_math_segment(
                        num, size=size, color=color, bold=bold, italic_override=italic_override, baseline=baseline
                    )
                )
                runs.append(_make_math_run("/", size=size, color=color, bold=bold, italic=False, baseline=baseline))
                runs.extend(
                    _parse_math_segment(
                        den, size=size, color=color, bold=bold, italic_override=italic_override, baseline=baseline
                    )
                )
            i = next_i
            continue

        if expr.startswith(r"\text", i) or expr.startswith(r"\mathrm", i):
            cmd_len = 5 if expr.startswith(r"\text", i) else 7
            inner, next_i, _ = _read_arg(expr, i + cmd_len)
            runs.extend(
                _parse_math_segment(
                    inner, size=size, color=color, bold=bold, italic_override=False, baseline=baseline
                )
            )
            i = next_i
            continue

        if expr.startswith(r"\bar", i):
            inner, next_i, _ = _read_arg(expr, i + 4)
            if inner == "u":
                # Times New Roman reliably contains Latin Extended-A U+016B ('ū') with italic styling
                runs.append(
                    _make_math_run(
                        "ū",
                        size=size,
                        color=color,
                        bold=bold,
                        italic=(italic_override if italic_override is not None else True),
                        baseline=baseline,
                        font_latin=FONT_NOTES_LATIN,
                    )
                )
            else:
                runs.append(
                    _make_math_run(
                        inner + "\u0304",
                        size=size,
                        color=color,
                        bold=bold,
                        italic=(italic_override if italic_override is not None else True),
                        baseline=baseline,
                        font_latin=FONT_NOTES_LATIN,
                    )
                )
            i = next_i
            continue

        if expr[i] == "\\":
            m = re.match(r"\\([A-Za-z]+|%|,)", expr[i:])
            if not m or m.group(1) not in CMD_MAP:
                raise ValueError(f"Unsupported LaTeX command at {i} in {expr!r}")
            sym, default_it = CMD_MAP[m.group(1)]
            it = italic_override if italic_override is not None else default_it
            runs.append(_make_math_run(sym, size=size, color=color, bold=bold, italic=it, baseline=baseline))
            i += len(m.group(0))
            if m.group(1) == "cdot" and i < n and expr[i] == " ":
                i += 1
            continue

        if expr[i] == "^":
            arg, next_i, _ = _read_arg(expr, i + 1)
            if arg == r"\circ":
                runs.append(_make_math_run("°", size=size, color=color, bold=bold, italic=False, baseline=baseline))
            else:
                sub_sz = round(size * 0.75, 1)
                runs.extend(
                    _parse_math_segment(
                        arg, size=sub_sz, color=color, bold=bold, italic_override=italic_override, baseline=0.30
                    )
                )
            i = next_i
            continue

        if expr[i] == "_":
            arg, next_i, _ = _read_arg(expr, i + 1)
            sub_sz = round(size * 0.75, 1)
            runs.extend(
                _parse_math_segment(
                    arg, size=sub_sz, color=color, bold=bold, italic_override=italic_override, baseline=-0.25
                )
            )
            i = next_i
            continue

        ch = expr[i]
        if ch == "-":
            runs.append(_make_math_run("−", size=size, color=color, bold=bold, italic=False, baseline=baseline))
        elif ch.isalpha() and ch.isascii():
            if italic_override is not None:
                is_it = italic_override
            elif ch == "d" and i + 1 < n and expr[i + 1] in ("i", "t") and (i == 0 or not expr[i - 1].isalpha()):
                # Standard mathematical differential operator 'd' in di/dt is upright
                is_it = False
            else:
                is_it = True
            runs.append(_make_math_run(ch, size=size, color=color, bold=bold, italic=is_it, baseline=baseline))
        else:
            runs.append(_make_math_run(ch, size=size, color=color, bold=bold, italic=False, baseline=baseline))
        i += 1

    return runs


def parse_markdown_math_to_runs(
    text: str,
    *,
    size: float = 12.0,
    color: tuple[int, int, int] = INK_DARK,
    bold: bool = False,
) -> list[dict[str, Any]]:
    """Split prose + inline `$...$` expressions into styled rich runs with zero raw LaTeX tokens."""
    runs: list[dict[str, Any]] = []
    parts = re.split(r"(\$[^$]+\$)", text)
    for part in parts:
        if not part:
            continue
        if part.startswith("$") and part.endswith("$"):
            inner = part[1:-1]
            math_runs = _parse_math_segment(inner, size=size, color=color, bold=bold)
            for mr in math_runs:
                for bad in FORBIDDEN_RAW_TOKENS:
                    if bad in mr["text"]:
                        raise AssertionError(f"Unconverted math token {bad!r} in run: {mr['text']!r} from {text!r}")
            runs.extend(math_runs)
        else:
            clean_prose = part.replace("`", "")
            for bad in ("$", "\\", "{", "}", "^"):
                if bad in clean_prose:
                    raise AssertionError(f"Unconverted prose token {bad!r} in run: {clean_prose!r} from {text!r}")
            if "_" in re.sub(r"[A-Za-z0-9_]+\.mp4", "", clean_prose):
                raise AssertionError(f"Unexpected '_' in prose run: {clean_prose!r} from {text!r}")
            runs.append(
                make_run(
                    clean_prose,
                    size=size,
                    color=color,
                    bold=bold,
                    font_cn=FONT_NOTES_CN,
                    font_latin=FONT_NOTES_LATIN,
                )
            )
    return _coalesce_runs(runs)


def parse_paged_speech_md(md_path: Path = SPEECH_PAGED_MD) -> dict[int, tuple[str, list[str]]]:
    """Extract per-slide cue + spoken paragraphs for Slides 1..29 (ignoring Q&A appendix)."""
    if not md_path.is_file():
        raise FileNotFoundError(f"Paged speech file not found: {md_path}")
    full_txt = md_path.read_text(encoding="utf-8")
    body = full_txt.split("## 答问备查与出处")[0]

    pattern = re.compile(r"^### Slide (\d+)｜[^\n]+\n(.*?)(?=^### Slide |\Z)", re.MULTILINE | re.DOTALL)
    parsed: dict[int, tuple[str, list[str]]] = {}
    for m in pattern.finditer(body):
        slide_num = int(m.group(1))
        block = m.group(2).strip()
        cue = ""
        paras: list[str] = []
        for raw_line in block.splitlines():
            line = raw_line.strip()
            if not line or line == "---" or line.startswith("## "):
                continue
            if line.startswith(">"):
                cue = line.lstrip(">").strip()
            else:
                paras.append(line)
        parsed[slide_num] = (cue, paras)

    if sorted(parsed.keys()) != list(range(1, 30)):
        raise AssertionError(f"Expected Slides 1..29 in {md_path}, got {sorted(parsed.keys())}")
    return parsed


def _prepare_single_notes_body_shape(sld: Any) -> Any:
    """Keep strictly one NotesPage body placeholder (`ppPlaceholderBody` == 2) and delete duplicates."""
    notes_shapes = sld.NotesPage.Shapes
    body_indices = [
        i
        for i in range(1, notes_shapes.Count + 1)
        if notes_shapes.Item(i).Type == 14 and notes_shapes.Item(i).PlaceholderFormat.Type == 2
    ]
    if not body_indices:
        return notes_shapes.Placeholders(2)
    for dup_idx in reversed(body_indices[1:]):
        notes_shapes.Item(dup_idx).Delete()
    return notes_shapes.Item(body_indices[0])


def inject_notes_into_presentation(pres: Any, md_path: Path = SPEECH_PAGED_MD) -> None:
    """Populate formatted Speaker Notes (with rich-text formulas) across all 29 slides."""
    slides_data = parse_paged_speech_md(md_path)
    if pres.Slides.Count != 29:
        raise AssertionError(f"Expected 29 slides in presentation, found {pres.Slides.Count}")

    for s_idx in range(1, 30):
        cue, paras = slides_data[s_idx]
        rich_paras: list[dict[str, Any]] = []
        if cue:
            rich_paras.append(
                {
                    "runs": parse_markdown_math_to_runs(cue, size=11.0, color=STEEL_BLUE, bold=True),
                    "space_after": 6.0,
                    "line_spacing": 1.2,
                }
            )
        for p_idx, p_txt in enumerate(paras):
            rich_paras.append(
                {
                    "runs": parse_markdown_math_to_runs(p_txt, size=12.0, color=INK_DARK, bold=False),
                    "space_after": 4.0 if p_idx < len(paras) - 1 else 0.0,
                    "line_spacing": 1.25,
                }
            )

        notes_shp = _prepare_single_notes_body_shape(pres.Slides(s_idx))
        notes_shp.TextFrame2.TextRange.Font.BaselineOffset = 0.0
        apply_runs(notes_shp, rich_paras, default_align=PP_ALIGN_LEFT)


_ALT_NOTES_RE = re.compile(
    r"<mc:AlternateContent\b[^>]*>\s*<mc:Choice\b[^>]*>(<p:sp>.*?</p:sp>)</mc:Choice>\s*<mc:Fallback\b[^>]*>.*?</mc:Fallback>\s*</mc:AlternateContent>",
    re.DOTALL,
)


def unwrap_notes_alternate_content(pptx_path: Path) -> int:
    """Promote <mc:Choice> body placeholder out of <mc:AlternateContent> to drop stale <mc:Fallback> text."""
    tmp_path = pptx_path.with_suffix(".tmp.pptx")
    unwrapped = 0
    with zipfile.ZipFile(pptx_path, "r") as zin, zipfile.ZipFile(tmp_path, "w") as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", item.filename):
                txt = data.decode("utf-8")
                if "<mc:AlternateContent" in txt:
                    new_txt, n_sub = _ALT_NOTES_RE.subn(
                        lambda m: m.group(1) if '<p:ph type="body"' in m.group(1) else m.group(0),
                        txt,
                    )
                    if n_sub > 0:
                        data = new_txt.encode("utf-8")
                        unwrapped += n_sub
            zout.writestr(item, data)
    shutil.move(str(tmp_path), str(pptx_path))
    return unwrapped


def main() -> None:
    if not OUT_USER_PPTX.is_file():
        raise FileNotFoundError(f"Target presentation not found: {OUT_USER_PPTX}")

    # Validate markdown parsing before opening PowerPoint COM
    slides_data = parse_paged_speech_md(SPEECH_PAGED_MD)
    for s_idx in range(1, 30):
        cue, paras = slides_data[s_idx]
        if cue:
            parse_markdown_math_to_runs(cue, size=11.0, color=STEEL_BLUE, bold=True)
        for p_txt in paras:
            parse_markdown_math_to_runs(p_txt, size=12.0, color=INK_DARK)
    print("Validated LaTeX-to-rich-runs conversion for all 29 slides.")

    n_unwrapped = unwrap_notes_alternate_content(OUT_USER_PPTX)
    if n_unwrapped:
        print(f"Unwrapped {n_unwrapped} stale <mc:AlternateContent> notes wrapper(s).")

    NOTES_VERIFY_PDF.parent.mkdir(parents=True, exist_ok=True)

    app = win32.gencache.EnsureDispatch("PowerPoint.Application")
    app.Visible = True
    pres = app.Presentations.Open(str(OUT_USER_PPTX), ReadOnly=False, Untitled=False, WithWindow=True)
    try:
        inject_notes_into_presentation(pres, SPEECH_PAGED_MD)
        pres.Save()
        pres.SaveCopyAs(str(OUT_CN_PPTX))
        # OutputType=5 -> ppPrintOutputNotesPages, FixedFormatType=2 -> PDF
        pres.ExportAsFixedFormat(
            Path=str(NOTES_VERIFY_PDF),
            FixedFormatType=2,
            Intent=1,
            FrameSlides=0,
            HandoutOrder=1,
            OutputType=5,
            PrintRange=None,
        )
    finally:
        pres.Close()

    print(f"SUCCESS: Injected formatted speaker notes into {OUT_USER_PPTX} and {OUT_CN_PPTX}")
    print(f"Exported verification Notes Pages PDF: {NOTES_VERIFY_PDF}")


if __name__ == "__main__":
    main()
