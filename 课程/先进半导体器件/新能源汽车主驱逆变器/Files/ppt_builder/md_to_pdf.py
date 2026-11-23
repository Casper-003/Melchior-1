"""Convert the polished speech markdown into a print-ready A4 PDF via HTML + MathML + Chrome headless."""

from __future__ import annotations

import os
from pathlib import Path
import re
import subprocess
import tempfile

import latex2mathml.converter
import markdown
import pymupdf

ROOT_DIR = Path(r"c:\Users\Casper\Documents\Proj")
SRC_MD = ROOT_DIR / "新能源汽车主驱逆变器_发言稿_润色版.md"
OUT_PDF = ROOT_DIR / "新能源汽车主驱逆变器_发言稿_润色版.pdf"
PREVIEW_DIR = ROOT_DIR / "ppt_builder" / "pdf_preview"
OUT_HTML = PREVIEW_DIR / "speech.html"
CHROME_EXE = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

CSS = """\
* {
  box-sizing: border-box;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

@page {
  size: A4;
  margin: 18mm 18mm 19mm 18mm;

  @top-left {
    content: "新能源汽车主驱逆变器｜课堂汇报发言稿";
    font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
    font-size: 8.5pt;
    color: #64748B;
    border-bottom: 0.5pt solid #D9DEE5;
    padding-bottom: 4pt;
    margin-bottom: 6pt;
    vertical-align: bottom;
  }

  @top-right {
    content: "约 14 分钟 · 共 10 页";
    font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
    font-size: 8.5pt;
    color: #64748B;
    border-bottom: 0.5pt solid #D9DEE5;
    padding-bottom: 4pt;
    margin-bottom: 6pt;
    vertical-align: bottom;
  }

  @bottom-center {
    content: "第 " counter(page) " / " counter(pages) " 页";
    font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
    font-size: 8.5pt;
    color: #64748B;
    vertical-align: top;
    padding-top: 4pt;
  }
}

@page :first {
  @top-left {
    content: none;
    border: none;
  }
  @top-right {
    content: none;
    border: none;
  }
}

body {
  margin: 0;
  padding: 0;
  font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
  font-size: 10.5pt;
  line-height: 1.72;
  color: #1E293B;
  text-align: justify;
  background: #FFFFFF;
}

math {
  font-family: "Cambria Math", serif;
  font-size: 1.02em;
}

h1 {
  margin: 0 0 12px;
  padding-bottom: 8px;
  font-size: 18pt;
  font-weight: 700;
  line-height: 1.35;
  color: #1E293B;
  text-align: left;
  border-bottom: 2px solid #0F9D8A;
}

h2 {
  margin: 14px 0 8px;
  padding: 5px 10px;
  font-size: 12pt;
  font-weight: 700;
  line-height: 1.4;
  color: #1E293B;
  text-align: left;
  background: #F4F6F9;
  border-left: 3.5px solid #0F9D8A;
  border-radius: 0 4px 4px 0;
  break-after: avoid;
  page-break-after: avoid;
}

blockquote {
  margin: 0 0 14px;
  padding: 8px 12px;
  background: #F4F6F9;
  border-left: 3px solid #4A5A70;
  border-radius: 0 4px 4px 0;
  font-size: 9.5pt;
  line-height: 1.6;
  color: #334155;
  text-align: left;
}

blockquote p {
  margin: 0;
}

p {
  margin: 0 0 8px;
}

p.cue {
  margin: 6px 0 8px;
  padding: 5px 10px;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-left: 3px solid #4A5A70;
  border-radius: 4px;
  font-size: 9.3pt;
  line-height: 1.55;
  color: #475569;
  text-align: left;
  break-inside: avoid;
  page-break-inside: avoid;
  break-after: avoid;
  page-break-after: avoid;
}

.todo-badge {
  display: inline-block;
  background: #FDEBE3;
  color: #C2410C;
  border: 1px solid #FDBA74;
  padding: 0 4px;
  border-radius: 3px;
  font-weight: 700;
  font-size: 9.2pt;
  line-height: 1.35;
}

table {
  width: 100%;
  table-layout: fixed;
  border-collapse: collapse;
  margin: 10px 0 14px;
  font-size: 9.3pt;
  line-height: 1.5;
  text-align: left;
}

thead {
  display: table-header-group;
}

tr {
  break-inside: avoid;
  page-break-inside: avoid;
}

th, td {
  border: 1px solid #D9DEE5;
  padding: 6px 8px;
  vertical-align: top;
}

th {
  background: #4A5A70;
  color: #FFFFFF;
  font-weight: 700;
}

tbody tr:nth-child(even) td {
  background: #F8FAFC;
}

th:nth-child(1), td:nth-child(1) {
  width: 18%;
  font-weight: 600;
  color: #1E293B;
}

th:nth-child(2), td:nth-child(2) {
  width: 41%;
}

th:nth-child(3), td:nth-child(3) {
  width: 41%;
}

ul, ol {
  margin: 6px 0 12px;
  padding-left: 20px;
  font-size: 9.3pt;
  line-height: 1.6;
  text-align: left;
}

li {
  margin-bottom: 5px;
  break-inside: avoid;
  page-break-inside: avoid;
}

a {
  color: #0F9D8A;
  text-decoration: none;
  font-weight: 600;
  overflow-wrap: anywhere;
}

.page-break {
  break-before: page;
  page-break-before: always;
  height: 0;
  margin: 0;
  padding: 0;
}
"""


def preprocess_math(md_text: str) -> tuple[str, dict[str, str]]:
    """Extract inline $...$ formulas before Markdown conversion so _ and ^ are untouched."""
    placeholders: dict[str, str] = {}

    def _replace(match: re.Match[str]) -> str:
        idx = len(placeholders)
        token = f"MATHPLACEHOLDER{idx:04d}END"
        expr = match.group(1)
        expr = re.sub(r"\\text\{\s+", lambda _m: "\\text{\u00a0", expr)
        placeholders[token] = latex2mathml.converter.convert(expr)
        return token

    processed = re.sub(r"\$([^$\n]+)\$", _replace, md_text)
    return processed, placeholders


def postprocess_html(html_body: str, placeholders: dict[str, str]) -> str:
    """Restore MathML, style stage cues, highlight TODO badges, and split appendix page."""
    for token, mathml in placeholders.items():
        html_body = html_body.replace(token, mathml)

    html_body = re.sub(
        r"<p>(（(?:(?!</p>).)*?）)</p>",
        r'<p class="cue">\1</p>',
        html_body,
        flags=re.DOTALL,
    )
    html_body = html_body.replace("【待核对】", '<span class="todo-badge">【待核对】</span>')
    html_body = re.sub(r"<hr\s*/?>", '<div class="page-break"></div>', html_body)
    return html_body


def build_html(md_path: Path, html_path: Path) -> int:
    """Convert markdown speech file to standalone styled HTML5 and return formula count."""
    raw_md = md_path.read_text(encoding="utf-8")
    masked_md, placeholders = preprocess_math(raw_md)
    raw_html = markdown.markdown(masked_md, extensions=["tables", "sane_lists"])
    body_html = postprocess_html(raw_html, placeholders)

    full_html = (
        "<!DOCTYPE html>\n"
        '<html lang="zh-CN">\n'
        "<head>\n"
        '  <meta charset="utf-8">\n'
        "  <title>新能源汽车主驱逆变器｜发言稿</title>\n"
        f"  <style>\n{CSS}  </style>\n"
        "</head>\n"
        "<body>\n"
        f"{body_html}\n"
        "</body>\n"
        "</html>\n"
    )
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(full_html, encoding="utf-8")
    return len(placeholders)


def render_pdf_chrome(html_path: Path, pdf_path: Path) -> None:
    """Print HTML5 document to A4 PDF using headless Chrome."""
    if not CHROME_EXE.is_file():
        raise FileNotFoundError(f"Chrome executable not found: {CHROME_EXE}")

    if pdf_path.exists():
        os.remove(pdf_path)

    with tempfile.TemporaryDirectory(prefix="chrome_pdf_") as profile_dir:
        cmd = [
            str(CHROME_EXE),
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--user-data-dir={profile_dir}",
            f"--print-to-pdf={pdf_path}",
            html_path.resolve().as_uri(),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if res.returncode != 0:
            raise RuntimeError(
                f"Chrome print-to-pdf failed (rc={res.returncode}):\nSTDOUT:{res.stdout}\nSTDERR:{res.stderr}"
            )
    if not pdf_path.is_file() or pdf_path.stat().st_size == 0:
        raise RuntimeError(f"Chrome completed but output PDF is missing/empty: {pdf_path}")


def audit_and_export_previews(pdf_path: Path, preview_dir: Path) -> tuple[int, int, int, list[Path]]:
    """Audit generated PDF via PyMuPDF and render 150 DPI page PNGs."""
    for old_png in preview_dir.glob("page_*.png"):
        old_png.unlink()

    doc = pymupdf.open(str(pdf_path))
    page_count = doc.page_count
    if page_count <= 0:
        raise AssertionError("PDF has 0 pages")

    bad_tokens = ("MATHPLACEHOLDER", "$", r"\frac", r"\text", r"\bar", r"\approx", "extV")
    all_text = []
    link_count = 0
    png_paths: list[Path] = []

    for idx, page in enumerate(doc, start=1):
        txt = page.get_text("text")
        all_text.append(txt)
        for tok in bad_tokens:
            if tok in txt:
                raise AssertionError(f"Found raw token {tok!r} on page {idx}")
        link_count += len(page.get_links())
        pix = page.get_pixmap(dpi=150)
        out_png = preview_dir / f"page_{idx:02d}.png"
        pix.save(str(out_png))
        png_paths.append(out_png)

    doc.close()

    if link_count < 15:
        raise AssertionError(f"Expected >= 15 clickable links, found {link_count}")

    size_bytes = pdf_path.stat().st_size
    return page_count, size_bytes, link_count, png_paths


def main() -> None:
    formula_count = build_html(SRC_MD, OUT_HTML)
    render_pdf_chrome(OUT_HTML, OUT_PDF)
    page_count, size_bytes, link_count, png_paths = audit_and_export_previews(OUT_PDF, PREVIEW_DIR)
    print(
        f"PDF OK: {OUT_PDF} | pages={page_count} | size={size_bytes / 1024:.1f} KB "
        f"| formulas={formula_count} | links={link_count}"
    )
    for p in png_paths:
        print(f"PREVIEW: {p}")


if __name__ == "__main__":
    main()
