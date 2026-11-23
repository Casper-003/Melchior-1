"""Generate chunky retro pixel-art meme explosion RGBA sprite sequence."""

from __future__ import annotations

from pathlib import Path
import numpy as np
from PIL import Image


def _value_noise_2d(h: int, w: int, grid_size: int, rng: np.random.Generator) -> np.ndarray:
    grid = rng.random((grid_size + 1, grid_size + 1), dtype=np.float32)
    ys = np.linspace(0.0, grid_size - 1e-4, h, dtype=np.float32)
    xs = np.linspace(0.0, grid_size - 1e-4, w, dtype=np.float32)
    y0 = np.floor(ys).astype(int)
    x0 = np.floor(xs).astype(int)
    wy = (ys - y0)[:, None]
    wx = (xs - x0)[None, :]
    wy = wy * wy * (3.0 - 2.0 * wy)
    wx = wx * wx * (3.0 - 2.0 * wx)

    v00 = grid[y0[:, None], x0[None, :]]
    v10 = grid[y0[:, None] + 1, x0[None, :]]
    v01 = grid[y0[:, None], x0[None, :] + 1]
    v11 = grid[y0[:, None] + 1, x0[None, :] + 1]

    top = v00 * (1.0 - wx) + v01 * wx
    bot = v10 * (1.0 - wx) + v11 * wx
    return top * (1.0 - wy) + bot * wy


def _fbm(h: int, w: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return (
        0.52 * _value_noise_2d(h, w, 5, rng)
        + 0.30 * _value_noise_2d(h, w, 9, rng)
        + 0.18 * _value_noise_2d(h, w, 16, rng)
    )


def generate_explosion_sequence(out_dir: Path, n_frames: int = 24) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    size = 56
    up_size = 224
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    cx = (size - 1) * 0.5
    cy = (size - 1) * 0.56
    dx = (xx - cx) / (size * 0.48)
    dy = (yy - cy) / (size * 0.48)
    angle = np.arctan2(dy, dx)

    noise_a = _fbm(size, size, seed=42)
    noise_b = _fbm(size, size, seed=137)

    # Asymmetric cartoon mushroom/billow puff clusters (classic meme explosion look)
    blobs = [
        # (dx_dir, dy_dir, speed, base_r, delay)
        (0.00, -0.55, 0.95, 0.36, 0.00),
        (-0.55, -0.25, 0.85, 0.31, 0.03),
        (0.58, -0.20, 0.88, 0.32, 0.02),
        (-0.42, 0.32, 0.78, 0.27, 0.04),
        (0.44, 0.30, 0.80, 0.28, 0.05),
        (-0.18, -0.68, 1.05, 0.28, 0.06),
        (0.24, -0.65, 1.00, 0.26, 0.07),
        (0.02, 0.10, 0.30, 0.34, 0.00),
        (-0.72, 0.05, 0.92, 0.22, 0.08),
        (0.74, 0.08, 0.90, 0.22, 0.09),
    ]

    rng = np.random.default_rng(777)
    n_debris = 16
    deb_angles = np.linspace(0, 2 * np.pi, n_debris, endpoint=False) + rng.uniform(-0.18, 0.18, n_debris)
    deb_speeds = rng.uniform(0.80, 1.45, n_debris)

    for idx in range(n_frames):
        t = idx / (n_frames - 1)
        rgba = np.zeros((size, size, 4), dtype=np.float32)

        turbulence = noise_a * (1.0 - t) + noise_b * t
        rise = 0.25 * (t ** 1.3)

        # Accumulate heat & smoke fields across puff lobes
        heat_field = np.zeros((size, size), dtype=np.float32)
        smoke_field = np.zeros((size, size), dtype=np.float32)

        for bx, by, bspd, br, bdelay in blobs:
            bt = max(0.0, (t - bdelay) / max(1.0 - bdelay, 1e-4))
            if bt <= 0.0 and t < 0.05:
                bt = 0.08
            px = bx * bspd * (bt ** 0.58)
            py = by * bspd * (bt ** 0.58) - rise * 0.75
            pr = br * (0.45 + 0.95 * (bt ** 0.45)) * (1.0 + 0.25 * t)
            d = np.sqrt((dx - px) ** 2 + (dy - py) ** 2)
            lobe = np.clip(1.0 - d / max(pr, 1e-4), 0.0, 1.0)
            # Fire cools from edges inward over time
            blob_heat = lobe * max(0.0, 1.0 - (t / 0.62)) * (0.75 + 0.50 * turbulence)
            heat_field = np.maximum(heat_field, blob_heat)
            smoke_field = np.maximum(smoke_field, lobe * (0.70 + 0.55 * turbulence))

        # Jagged cartoon starburst spikes in the first 4 frames
        if t < 0.22:
            spike_wave = np.abs(np.cos(5.5 * angle + 0.3)) ** 2.2
            r_center = np.sqrt(dx * dx + dy * dy)
            spike_reach = (0.38 + 0.75 * (t / 0.22)) * (0.52 + 0.68 * spike_wave)
            burst = np.clip(1.0 - r_center / spike_reach, 0.0, 1.0) * (1.15 - t / 0.22)
            heat_field = np.maximum(heat_field, burst)

        # Smoke envelope appears quickly behind the fireball and lingers/fades
        smoke_alpha_env = np.clip((t - 0.14) / 0.20, 0.0, 1.0) * np.clip((1.0 - t) / 0.34, 0.0, 1.0)
        smoke_mask = (smoke_field * smoke_alpha_env) > 0.26

        # Two-tone retro gray smoke (darker bottom/edge, lighter puff top)
        smoke_dark = smoke_mask & (smoke_field < 0.56)
        smoke_mid = smoke_mask & (smoke_field >= 0.56)
        alpha_val = np.clip(smoke_alpha_env * 255.0, 0.0, 245.0)
        rgba[smoke_dark] = [62.0, 58.0, 62.0, alpha_val]
        rgba[smoke_mid] = [118.0, 114.0, 118.0, alpha_val]

        # Crunchy cartoon fire ramp (red outline -> orange -> bright yellow -> white hot)
        fire_alpha = 255.0 * np.clip((0.68 - t) / 0.18, 0.0, 1.0)
        if fire_alpha > 5.0:
            r_mask = heat_field > 0.24
            o_mask = heat_field > 0.40
            y_mask = heat_field > 0.58
            w_mask = heat_field > 0.78
            rgba[r_mask] = [215.0, 32.0, 16.0, fire_alpha]
            rgba[o_mask] = [255.0, 118.0, 12.0, fire_alpha]
            rgba[y_mask] = [255.0, 224.0, 42.0, fire_alpha]
            rgba[w_mask] = [255.0, 254.0, 232.0, fire_alpha]

        # Flying 2x2 pixel embers/debris chunks
        if 0.04 <= t <= 0.65:
            fade = 1.0 - (t - 0.04) / 0.61
            for s_idx in range(n_debris):
                dist_s = deb_speeds[s_idx] * (t ** 0.68) * 0.92
                grav = 0.35 * (t ** 2)
                sx = int(round(cx + dist_s * np.cos(deb_angles[s_idx]) * (size * 0.45)))
                sy = int(round(cy + (dist_s * np.sin(deb_angles[s_idx]) + grav) * (size * 0.45)))
                if 1 <= sx < size - 2 and 1 <= sy < size - 2:
                    if s_idx % 3 == 0:
                        col = [65.0, 60.0, 64.0, 240.0 * fade]
                    elif s_idx % 3 == 1:
                        col = [255.0, 140.0, 20.0, 255.0 * fade]
                    else:
                        col = [255.0, 235.0, 70.0, 255.0 * fade]
                    rgba[sy : sy + 2, sx : sx + 2] = col

        img = Image.fromarray(np.clip(rgba, 0, 255).astype(np.uint8), mode="RGBA")
        img.resize((up_size, up_size), resample=Image.NEAREST).save(out_dir / f"exp_{idx:02d}.png")

    # Crisp comic scorched soot starburst smudge
    soot = np.zeros((size, size, 4), dtype=np.float32)
    r_soot = np.sqrt(dx * dx + dy * dy)
    sp = 0.5 + 0.5 * np.cos(7.0 * angle + 0.7)
    s_mask = r_soot < (0.30 + 0.22 * sp) * (0.65 + 0.55 * noise_a)
    alpha_s = np.clip((1.0 - r_soot / 0.60) * 210.0, 0.0, 195.0)
    soot[s_mask, 0] = 36.0
    soot[s_mask, 1] = 34.0
    soot[s_mask, 2] = 38.0
    soot[s_mask, 3] = alpha_s[s_mask]
    Image.fromarray(soot.astype(np.uint8), mode="RGBA").resize(
        (up_size, up_size), resample=Image.NEAREST
    ).save(out_dir / "soot.png")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    generate_explosion_sequence(project_root / "assets" / "explosion", n_frames=24)
    print("Regenerated chunky meme explosion frames")
