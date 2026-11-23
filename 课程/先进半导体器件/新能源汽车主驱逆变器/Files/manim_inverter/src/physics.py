"""Fast deterministic physics & waveform calculation helpers."""

from __future__ import annotations

import math
import numpy as np


def square_u(t: float, period: float = 1.0) -> float:
    """Bipolar square wave (+1 on [0, T/2), -1 on [T/2, T))."""
    phase = (t % period) / period
    return 1.0 if phase < 0.5 else -1.0


def triangle_i(t: float, period: float = 1.0) -> float:
    """Steady-state inductive triangle current (-1 -> +1 -> -1, zero at T/4 and 3T/4)."""
    phase = (t % period) / period
    if phase < 0.5:
        return -1.0 + 4.0 * phase
    return 1.0 - 4.0 * (phase - 0.5)


def hbridge_mode_at(t: float, period: float = 1.0) -> str:
    """Exact conduction mode of single-phase H-bridge with inductive load.

    - [0, T/4):    u=+U, i<0 -> freewheeling via D1, D4
    - [T/4, T/2):  u=+U, i>0 -> active via S1, S4
    - [T/2, 3T/4): u=-U, i>0 -> freewheeling via D2, D3
    - [3T/4, T):   u=-U, i<0 -> active via S2, S3
    """
    phase = (t % period) / period
    if phase < 0.25:
        return "D1_D4"
    if phase < 0.50:
        return "S1_S4"
    if phase < 0.75:
        return "D2_D3"
    return "S2_S3"


def bipolar_period_duty(k: int, n_sw: int = 24, amp: float = 0.88) -> tuple[float, float]:
    """Return (duty_cycle D_k, normalized avg voltage u_bar_k) for period index k."""
    theta = 2.0 * math.pi * (k + 0.5) / n_sw
    u_bar = amp * math.sin(theta)
    duty = 0.5 + 0.5 * u_bar
    return duty, u_bar


def triangle_carrier(t: np.ndarray, f_sw: float) -> np.ndarray:
    """Symmetric [-1, 1] triangle carrier at switching frequency f_sw."""
    return 1.0 - 4.0 * np.abs(np.mod(f_sw * t - 0.25, 1.0) - 0.5)


def spwm_pulses_from_mod(
    amp: float,
    freq: float,
    phase: float,
    f_sw: float,
    t_start: float = 0.0,
    t_max: float = 1.0,
    n_grid: int = 2400,
) -> tuple[np.ndarray, np.ndarray]:
    """Compare u_ref(t) = A sin(2*pi*f*t + phi) with symmetric carrier -> (edges, levels)."""
    t_grid = np.linspace(t_start, t_max, n_grid)
    u_ref = amp * np.sin(2.0 * np.pi * freq * t_grid + phase)
    u_tri = triangle_carrier(t_grid, f_sw)
    diff = u_ref - u_tri

    edges_list = [float(t_start)]
    levels_list = [1.0 if diff[0] >= 0.0 else -1.0]

    for idx in range(len(t_grid) - 1):
        d0 = diff[idx]
        d1 = diff[idx + 1]
        if (d0 >= 0.0 and d1 < 0.0) or (d0 <= 0.0 and d1 > 0.0):
            denom = d1 - d0
            frac = 0.5 if abs(denom) < 1e-12 else -d0 / denom
            frac = float(np.clip(frac, 0.0, 1.0))
            t_cross = float(t_grid[idx] + frac * (t_grid[idx + 1] - t_grid[idx]))
            if t_cross - edges_list[-1] > 1e-7 and t_max - t_cross > 1e-7:
                edges_list.append(t_cross)
                levels_list.append(-levels_list[-1])

    edges_list.append(float(t_max))
    return np.asarray(edges_list, dtype=np.float64), np.asarray(levels_list, dtype=np.float64)


def solve_rl_current(
    amp: float,
    freq: float,
    phase: float,
    f_sw: float,
    tau: float = 0.14,
    r_val: float = 1.0,
    t_max: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Exact piecewise exponential RL filter solution without startup transient.

    Simulates from t_pre = -0.75 (initialized on exact analytical fundamental steady-state)
    through t_max so arbitrary non-integer frequencies remain completely continuous.
    """
    t_pre = -0.75
    n_grid_full = max(3200, int(round(80 * f_sw * (t_max - t_pre))))
    edges, levels = spwm_pulses_from_mod(
        amp=amp,
        freq=freq,
        phase=phase,
        f_sw=f_sw,
        t_start=t_pre,
        t_max=t_max,
        n_grid=n_grid_full,
    )

    omega = 2.0 * math.pi * freq
    l_val = tau * r_val
    z_mag = math.hypot(r_val, omega * l_val)
    lag = math.atan2(omega * l_val, r_val)
    i_curr = (amp / z_mag) * math.sin(omega * t_pre + phase - lag)

    t_out = []
    i_out = []
    for k in range(len(levels)):
        t0 = float(edges[k])
        t1 = float(edges[k + 1])
        u_k = float(levels[k]) / r_val
        dt = t1 - t0
        exp_dt = math.exp(-dt / tau)
        i_next = u_k + (i_curr - u_k) * exp_dt

        if t1 >= 0.0:
            if t0 < 0.0:
                # Interpolate exact value at t = 0
                i_zero = u_k + (i_curr - u_k) * math.exp(-(-t0) / tau)
                t_start_seg = 0.0
                i_start_seg = i_zero
            else:
                t_start_seg = t0
                i_start_seg = i_curr

            n_pts = 3 if (t1 - t_start_seg) > 0.008 else 2
            ts = np.linspace(t_start_seg, t1, n_pts, endpoint=(k == len(levels) - 1))
            vals = u_k + (i_start_seg - u_k) * np.exp(-(ts - t_start_seg) / tau)
            t_out.append(ts)
            i_out.append(vals)

        i_curr = i_next

    return np.concatenate(t_out), np.concatenate(i_out)


def solve_rl_periodic_edges(
    edges: np.ndarray,
    levels: np.ndarray,
    tau: float = 0.14,
    r_val: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Exact closed-form periodic steady-state RL current for edges on [0, T]."""
    a = 1.0
    b = 0.0
    for k in range(len(levels)):
        dt = float(edges[k + 1] - edges[k])
        ek = math.exp(-dt / tau)
        a *= ek
        b = ek * b + (float(levels[k]) / r_val) * (1.0 - ek)
    i_curr = b / max(1.0 - a, 1e-9)

    t_out = []
    i_out = []
    for k in range(len(levels)):
        t0 = float(edges[k])
        t1 = float(edges[k + 1])
        u_k = float(levels[k]) / r_val
        dt = t1 - t0
        ts = np.linspace(t0, t1, 3, endpoint=(k == len(levels) - 1))
        vals = u_k + (i_curr - u_k) * np.exp(-(ts - t0) / tau)
        t_out.append(ts)
        i_out.append(vals)
        i_curr = u_k + (i_curr - u_k) * math.exp(-dt / tau)

    return np.concatenate(t_out), np.concatenate(i_out)


def gate_states_deadtime(t: float, period: float = 1.0, td: float = 0.07) -> tuple[bool, bool]:
    """Return (s1_on, s3_on) for asynchronous non-overlapping switching with dead-time td."""
    p = (t % period) / period
    half = 0.5
    if td <= p < half - td:
        return True, False
    if half + td <= p < 1.0 - td:
        return False, True
    return False, False
