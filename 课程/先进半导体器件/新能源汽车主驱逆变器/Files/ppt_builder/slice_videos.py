"""Slice Manim 1080p60 videos into seamless click-beat clips for Slides 3 and 4."""

from __future__ import annotations

import pathlib
import subprocess
import tempfile
import numpy as np
from PIL import Image

FFMPEG = r"C:\Users\Casper\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-essentials_build\bin\ffmpeg.exe"
FFPROBE = r"C:\Users\Casper\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-essentials_build\bin\ffprobe.exe"

VIDEOS_DIR = pathlib.Path(r"c:\Users\Casper\Documents\Proj\manim_videos")
CLIPS_DIR = VIDEOS_DIR / "clips"

SRC_P3 = VIDEOS_DIR / "第3页_单相H桥与续流死区_1080p60.mp4"
SRC_P4 = VIDEOS_DIR / "第4页_SPWM调制与三相电机_1080p60.mp4"

CLIPS_SPEC = [
    (SRC_P3, "p3_clip1.mp4", 0.00, 35.30),
    (SRC_P3, "p3_clip2.mp4", 35.30, 61.70),
    (SRC_P3, "p3_clip3.mp4", 61.70, 87.10),
    (SRC_P3, "p3_clip4.mp4", 87.10, 108.45),
    (SRC_P4, "p4_clip1.mp4", 1.50, 17.60),
    (SRC_P4, "p4_clip2.mp4", 17.60, 43.40),
    (SRC_P4, "p4_clip3.mp4", 43.40, 91.00),
    (SRC_P4, "p4_clip4.mp4", 91.00, 114.50),
]


def slice_clip(src: pathlib.Path, dst: pathlib.Path, start_s: float, end_s: float) -> None:
    dur = end_s - start_s
    cmd = [
        FFMPEG,
        "-y",
        "-loglevel",
        "error",
        "-ss",
        f"{start_s:.3f}",
        "-t",
        f"{dur:.3f}",
        "-i",
        str(src),
        "-vf",
        "tpad=stop_mode=clone:stop_duration=0.5",
        "-c:v",
        "libx264",
        "-crf",
        "17",
        "-preset",
        "medium",
        "-pix_fmt",
        "yuv420p",
        "-r",
        "60",
        "-an",
        "-movflags",
        "+faststart",
        str(dst),
    ]
    subprocess.run(cmd, check=True)


def extract_frame(video: pathlib.Path, at_end: bool, out_png: pathlib.Path) -> None:
    if at_end:
        cmd = [FFMPEG, "-y", "-loglevel", "error", "-sseof", "-0.05", "-i", str(video), "-frames:v", "1", str(out_png)]
    else:
        cmd = [FFMPEG, "-y", "-loglevel", "error", "-i", str(video), "-frames:v", "1", str(out_png)]
    subprocess.run(cmd, check=True)


def main() -> None:
    CLIPS_DIR.mkdir(parents=True, exist_ok=True)
    for src, name, t0, t1 in CLIPS_SPEC:
        if not src.exists():
            raise FileNotFoundError(f"Missing source video: {src}")
        dst = CLIPS_DIR / name
        print(f"Slicing {name}: {t0:.2f}s -> {t1:.2f}s (+0.5s freeze)...")
        slice_clip(src, dst, t0, t1)

    print("\n=== ffprobe verification ===")
    for _, name, _, _ in CLIPS_SPEC:
        dst = CLIPS_DIR / name
        info = subprocess.check_output(
            [
                FFPROBE,
                "-v",
                "error",
                "-select_streams",
                "v:0",
                "-show_entries",
                "stream=codec_name,width,height,pix_fmt,r_frame_rate",
                "-show_entries",
                "format=duration",
                "-of",
                "csv=p=0",
                str(dst),
            ],
            text=True,
        ).strip()
        mb = dst.stat().st_size / (1024 * 1024)
        print(f"  {name}: {mb:.2f} MB | {info.replace(chr(10), ' | ')}")

    print("\n=== Seam continuity verification ===")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = pathlib.Path(tmp)
        for prefix in ("p3", "p4"):
            for i in (1, 2, 3):
                c1 = CLIPS_DIR / f"{prefix}_clip{i}.mp4"
                c2 = CLIPS_DIR / f"{prefix}_clip{i+1}.mp4"
                f1 = tmp_dir / f"{prefix}_{i}_end.png"
                f2 = tmp_dir / f"{prefix}_{i+1}_start.png"
                extract_frame(c1, True, f1)
                extract_frame(c2, False, f2)
                a1 = np.asarray(Image.open(f1).convert("RGB"), dtype=np.float32)
                a2 = np.asarray(Image.open(f2).convert("RGB"), dtype=np.float32)
                rmse = float(np.sqrt(np.mean((a1 - a2) ** 2)))
                print(f"  {c1.name} (last) vs {c2.name} (first): RMSE = {rmse:.2f}")
                if rmse >= 5.0:
                    raise RuntimeError(f"Seam mismatch between {c1.name} and {c2.name}: RMSE={rmse:.2f}")
    print("SEAM CHECK PASSED")


if __name__ == "__main__":
    main()
