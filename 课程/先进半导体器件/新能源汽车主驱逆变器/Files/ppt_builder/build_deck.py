"""Build the 10-slide native PowerPoint presentation, run programmatic audit, and export QA PNGs."""

from __future__ import annotations

import pathlib
import re
import sys
import traceback

import win32com.client as win32

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from ppt_helpers import (  # noqa: E402
    FONT_MATH,
    FONT_UI,
    PP_EFFECT_FADE_SMOOTHLY,
    SLIDE_H_PT,
    SLIDE_W_PT,
    TRIG_CLICK,
)
from slides_1_to_5 import (  # noqa: E402
    build_slide_1,
    build_slide_2,
    build_slide_3,
    build_slide_4,
    build_slide_5,
)
from slides_6_to_10 import (  # noqa: E402
    build_slide_6,
    build_slide_7,
    build_slide_8,
    build_slide_9,
    build_slide_10,
)

PROJ_ROOT = pathlib.Path(r"c:\Users\Casper\Documents\Proj")
OUT_PPTX = PROJ_ROOT / "新能源汽车主驱逆变器_课堂汇报.pptx"
SCRIPT_MD = PROJ_ROOT / "新能源汽车主驱逆变器_发言稿_润色版.md"
PREVIEW_DIR = pathlib.Path(__file__).resolve().parent / "preview"

EXPECTED_CLICKS = [0, 3, 4, 4, 5, 4, 4, 4, 4, 4]
ALLOWED_EFFECTS = {1, 10, 22, 75, 83, 149}


def parse_speaker_notes(md_path: pathlib.Path) -> dict[int, str]:
    """Extract per-slide speaker notes from 新能源汽车主驱逆变器_发言稿_润色版.md."""
    text = md_path.read_text(encoding="utf-8")
    main_body = text.split("\n---\n", 1)[0]
    sections = re.split(r"^## 第 (\d+) 页[^\n]*\n", main_body, flags=re.MULTILINE)
    notes: dict[int, str] = {}
    for i in range(1, len(sections), 2):
        s_num = int(sections[i])
        body = sections[i + 1].strip()
        notes[s_num] = body
    return notes


def run_audit(pres: Any) -> None:
    """Programmatic audit against every global and per-slide specification."""
    errors: list[str] = []
    if pres.Slides.Count != 10:
        errors.append(f"Expected 10 slides, got {pres.Slides.Count}")
    if abs(pres.PageSetup.SlideWidth - SLIDE_W_PT) > 0.5 or abs(pres.PageSetup.SlideHeight - SLIDE_H_PT) > 0.5:
        errors.append(f"Wrong slide dimensions: {pres.PageSetup.SlideWidth} x {pres.PageSetup.SlideHeight}")

    clicks_observed: list[int] = []
    for s_idx in range(1, pres.Slides.Count + 1):
        sld = pres.Slides(s_idx)
        # Transition check on Slides 2..10
        if s_idx >= 2:
            if sld.SlideShowTransition.EntryEffect != PP_EFFECT_FADE_SMOOTHLY:
                errors.append(f"Slide {s_idx}: unexpected transition {sld.SlideShowTransition.EntryEffect}")
            if abs(sld.SlideShowTransition.Duration - 0.5) > 0.05:
                errors.append(f"Slide {s_idx}: unexpected transition duration {sld.SlideShowTransition.Duration}")

        # InteractiveSequences must be empty (no click-on-video conflict)
        if sld.TimeLine.InteractiveSequences.Count != 0:
            errors.append(f"Slide {s_idx}: InteractiveSequences.Count={sld.TimeLine.InteractiveSequences.Count}")

        # MainSequence check
        seq = sld.TimeLine.MainSequence
        clicks = 0
        for e_idx in range(1, seq.Count + 1):
            eff = seq.Item(e_idx)
            if eff.Timing.TriggerType == TRIG_CLICK:
                clicks += 1
            if eff.EffectType not in ALLOWED_EFFECTS:
                errors.append(f"Slide {s_idx} eff {e_idx}: disallowed effect {eff.EffectType} on {eff.Shape.Name}")
        clicks_observed.append(clicks)
        if clicks != EXPECTED_CLICKS[s_idx - 1]:
            errors.append(f"Slide {s_idx}: expected {EXPECTED_CLICKS[s_idx - 1]} clicks, got {clicks}")

        # Shape naming, shadow/3D, font check
        prefix = f"p{s_idx}_"
        for sh_idx in range(1, sld.Shapes.Count + 1):
            shp = sld.Shapes(sh_idx)
            if not shp.Name.startswith(prefix):
                errors.append(f"Slide {s_idx}: shape '{shp.Name}' does not start with '{prefix}'")
            try:
                if shp.Shadow.Visible != 0:
                    errors.append(f"Slide {s_idx}: shape '{shp.Name}' has shadow visible")
            except Exception:
                pass
            try:
                if shp.ThreeD.Visible != 0:
                    errors.append(f"Slide {s_idx}: shape '{shp.Name}' has 3D visible")
            except Exception:
                pass

            # Check font families & sizes recursively across group items or single shape
            items = [shp.GroupItems(k) for k in range(1, shp.GroupItems.Count + 1)] if shp.Type == 6 else [shp]
            for item in items:
                try:
                    if item.HasTextFrame and item.TextFrame2.HasText:
                        tr = item.TextFrame2.TextRange
                        txt = tr.Text.strip()
                        if txt:
                            if "_" in txt or "^" in txt:
                                errors.append(f"Slide {s_idx} '{item.Name}': raw '_' or '^' found in '{txt}'")
                            idxs = sorted(set(range(1, len(tr.Text) + 1, 3)) | {1, len(tr.Text)})
                            for ch_i in idxs:
                                ch = tr.GetCharacters(ch_i, 1)
                                fname = ch.Font.Name
                                fsize = ch.Font.Size
                                if fname not in (FONT_UI, FONT_MATH, "Arial", "Segoe UI"):
                                    errors.append(f"Slide {s_idx} '{item.Name}': disallowed font '{fname}'")
                                    break
                                if ch.Font.BaselineOffset == 0 and fsize < 11.9:
                                    errors.append(f"Slide {s_idx} '{item.Name}': font too small ({fsize} pt) in '{txt}'")
                                    break
                except Exception:
                    pass

    print("Observed clicks per slide:", clicks_observed)
    if errors:
        for e in errors[:40]:
            print("AUDIT ERROR:", e)
        raise RuntimeError(f"Audit failed with {len(errors)} error(s)")
    print("AUDIT PASSED")


def export_qa_previews(pres: Any) -> None:
    """Export clean 1920x1080 PNGs for all 10 slides + intermediate states for Slides 6, 8, 10."""
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    for old_png in PREVIEW_DIR.glob("*.png"):
        old_png.unlink()

    def set_vis(sld: Any, names: list[str], vis: bool) -> None:
        val = -1 if vis else 0
        for nm in names:
            try:
                sld.Shapes(nm).Visible = val
            except Exception:
                pass

    def hide_prefixes(sld: Any, prefixes: tuple[str, ...], vis: bool) -> None:
        val = -1 if vis else 0
        for k in range(1, sld.Shapes.Count + 1):
            sh = sld.Shapes(k)
            if any(sh.Name.startswith(p) for p in prefixes):
                sh.Visible = val

    # Export default views for Slides 1, 2, 3, 4, 5, 7, 9
    for idx in (1, 2, 3, 4, 5, 7, 9):
        pres.Slides(idx).Export(str(PREVIEW_DIR / f"slide_{idx:02d}.png"), "PNG", 1920, 1080)

    # Slide 6 multi-state QA (mutates in-memory only AFTER SaveAs!)
    s6 = pres.Slides(6)
    s6_anim_only = [
        "p6_drift_hl",
        "p6_channel_L",
        "p6_channel_R",
        "p6_gate_on",
        "p6_gate_off",
        "p6_mod_badge",
        "p6_plasma_top",
        "p6_iv_igbt",
        "p6_iv_mos",
        "p6_iv_igbt_lbl",
        "p6_iv_mos_lbl",
        "p6_iv_vce_lbl",
        "p6_wf_vce_off",
        "p6_wf_vce_lbl",
        "p6_wf_ic_fast",
        "p6_wf_tail_fill",
        "p6_wf_ic_tail",
        "p6_wf_tail_lbl",
        "p6_wf_ic_on",
        "p6_wf_irr_lbl",
        "p6_cost_2",
        "p6_cost_3",
        "p6_cost_4",
    ]
    # 6.0 Initial static base
    set_vis(s6, s6_anim_only, False)
    hide_prefixes(s6, ("p6_plasma_deep_", "p6_electron_", "p6_hole_"), False)
    s6.Export(str(PREVIEW_DIR / "slide_06_init.png"), "PNG", 1920, 1080)

    # 6.1 Click 1 (On-state + conductivity modulation plasma)
    set_vis(s6, ["p6_drift_hl", "p6_channel_L", "p6_channel_R", "p6_gate_on", "p6_mod_badge", "p6_plasma_top"], True)
    hide_prefixes(s6, ("p6_plasma_deep_",), True)
    s6.Export(str(PREVIEW_DIR / "slide_06_click1.png"), "PNG", 1920, 1080)

    # 6.2 Final state (after Click 4: Gate 0V, waveforms + all 3 cost cards)
    set_vis(
        s6,
        [
            "p6_drift_hl",
            "p6_channel_L",
            "p6_channel_R",
            "p6_gate_on",
            "p6_mod_badge",
            "p6_plasma_top",
        ],
        False,
    )
    hide_prefixes(s6, ("p6_plasma_deep_", "p6_electron_", "p6_hole_"), False)
    set_vis(
        s6,
        [
            "p6_gate_off",
            "p6_iv_igbt",
            "p6_iv_mos",
            "p6_iv_igbt_lbl",
            "p6_iv_mos_lbl",
            "p6_iv_vce_lbl",
            "p6_wf_vce_off",
            "p6_wf_vce_lbl",
            "p6_wf_ic_fast",
            "p6_wf_tail_fill",
            "p6_wf_ic_tail",
            "p6_wf_tail_lbl",
            "p6_wf_ic_on",
            "p6_wf_irr_lbl",
            "p6_cost_2",
            "p6_cost_3",
            "p6_cost_4",
        ],
        True,
    )
    s6.Export(str(PREVIEW_DIR / "slide_06_final.png"), "PNG", 1920, 1080)

    # Slide 8 multi-state QA
    s8 = pres.Slides(8)
    set_vis(s8, ["p8_p3_syncrec", "p8_bot_4"], False)
    s8.Export(str(PREVIEW_DIR / "slide_08_click3.png"), "PNG", 1920, 1080)
    set_vis(s8, ["p8_p3_deadtime"], False)
    set_vis(s8, ["p8_p3_syncrec", "p8_bot_4"], True)
    s8.Export(str(PREVIEW_DIR / "slide_08_final.png"), "PNG", 1920, 1080)

    # Slide 10 multi-state QA
    s10 = pres.Slides(10)
    set_vis(s10, ["p10_mat_hdr", "p10_mat_row_1", "p10_mat_row_2", "p10_mat_row_3", "p10_mat_takeaway"], False)
    s10.Export(str(PREVIEW_DIR / "slide_10_state1.png"), "PNG", 1920, 1080)
    set_vis(s10, ["p10_dir_1", "p10_dir_2", "p10_dir_3"], False)
    set_vis(s10, ["p10_mat_hdr", "p10_mat_row_1", "p10_mat_row_2", "p10_mat_row_3", "p10_mat_takeaway"], True)
    s10.Export(str(PREVIEW_DIR / "slide_10_state2.png"), "PNG", 1920, 1080)


def main() -> None:
    notes = parse_speaker_notes(SCRIPT_MD)
    ppt = win32.gencache.EnsureDispatch("PowerPoint.Application")
    pres = None
    try:
        pres = ppt.Presentations.Add(WithWindow=True)
        pres.PageSetup.SlideWidth = SLIDE_W_PT
        pres.PageSetup.SlideHeight = SLIDE_H_PT

        builders = [
            build_slide_1,
            build_slide_2,
            build_slide_3,
            build_slide_4,
            build_slide_5,
            build_slide_6,
            build_slide_7,
            build_slide_8,
            build_slide_9,
            build_slide_10,
        ]
        for idx, builder in enumerate(builders, start=1):
            print(f"Building Slide {idx}/10...")
            sld = pres.Slides.Add(idx, 12)  # ppLayoutBlank = 12
            builder(sld)
            if idx in notes:
                sld.NotesPage.Shapes.Placeholders(2).TextFrame.TextRange.Text = notes[idx]

        run_audit(pres)
        if OUT_PPTX.exists():
            OUT_PPTX.unlink()
        pres.SaveAs(str(OUT_PPTX))
        print(f"Saved presentation: {OUT_PPTX} ({OUT_PPTX.stat().st_size / (1024 * 1024):.2f} MB)")

        export_qa_previews(pres)
        print(f"Exported previews to: {PREVIEW_DIR}")
    except Exception:
        traceback.print_exc()
        raise
    finally:
        if pres is not None:
            try:
                pres.Close()
            except Exception:
                pass
        try:
            ppt.Quit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
