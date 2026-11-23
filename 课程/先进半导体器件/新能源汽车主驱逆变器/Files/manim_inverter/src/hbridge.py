"""Reusable articulated H-bridge circuit with parallel freewheeling diodes & RL load."""

from __future__ import annotations

import numpy as np
from manim import *

from style import INK, INK_MUTED, RED_POS, BLUE_NEG, AMBER_FW, SHORT_RED, math_tnr, zh_label, sample_polyline_chevrons


class HBridgeCircuit(VGroup):
    """Single-phase H-bridge with separated parallel freewheeling diodes and switch blades."""

    def __init__(self, rl_mode: bool = True, **kwargs):
        super().__init__(**kwargs)

        # Canonical geometry constants (centered nicely around ORIGIN)
        self.x_dc = -3.85
        self.x_left = -1.55
        self.x_left_d = -2.45
        self.x_right = +1.55
        self.x_right_d = +2.45
        self.y_top = +2.15
        self.y_bot = -2.15

        # Switch vertical endpoints
        self.y_up_top_contact = +1.52
        self.y_up_bot_pivot = +0.82
        self.y_dn_top_contact = -0.82
        self.y_dn_bot_pivot = -1.52

        # Parallel diode tap heights
        self.y_up_tap_hi = +1.86
        self.y_up_tap_lo = +0.44
        self.y_dn_tap_hi = -0.44
        self.y_dn_tap_lo = -1.86

        # Invisible anchor dots so paths track arbitrary scale/move transforms exactly
        self._anchors: dict[str, Dot] = {}
        anchor_coords = {
            "dc_top": [self.x_dc, self.y_top, 0.0],
            "dc_bot": [self.x_dc, self.y_bot, 0.0],
            "dc_plus": [self.x_dc, +0.20, 0.0],
            "dc_minus": [self.x_dc, -0.20, 0.0],
            "dc_center": [self.x_dc, 0.0, 0.0],
            "lt_top": [self.x_left, self.y_top, 0.0],
            "lt_tap_hi": [self.x_left, self.y_up_tap_hi, 0.0],
            "lt_d_hi": [self.x_left_d, self.y_up_tap_hi, 0.0],
            "lt_d_lo": [self.x_left_d, self.y_up_tap_lo, 0.0],
            "lt_tap_lo": [self.x_left, self.y_up_tap_lo, 0.0],
            "lt_mid": [self.x_left, 0.0, 0.0],
            "lb_tap_hi": [self.x_left, self.y_dn_tap_hi, 0.0],
            "lb_d_hi": [self.x_left_d, self.y_dn_tap_hi, 0.0],
            "lb_d_lo": [self.x_left_d, self.y_dn_tap_lo, 0.0],
            "lb_tap_lo": [self.x_left, self.y_dn_tap_lo, 0.0],
            "lb_bot": [self.x_left, self.y_bot, 0.0],
            "rt_top": [self.x_right, self.y_top, 0.0],
            "rt_tap_hi": [self.x_right, self.y_up_tap_hi, 0.0],
            "rt_d_hi": [self.x_right_d, self.y_up_tap_hi, 0.0],
            "rt_d_lo": [self.x_right_d, self.y_up_tap_lo, 0.0],
            "rt_tap_lo": [self.x_right, self.y_up_tap_lo, 0.0],
            "rt_mid": [self.x_right, 0.0, 0.0],
            "rb_tap_hi": [self.x_right, self.y_dn_tap_hi, 0.0],
            "rb_d_hi": [self.x_right_d, self.y_dn_tap_hi, 0.0],
            "rb_d_lo": [self.x_right_d, self.y_dn_tap_lo, 0.0],
            "rb_tap_lo": [self.x_right, self.y_dn_tap_lo, 0.0],
            "rb_bot": [self.x_right, self.y_bot, 0.0],
            "s1_center": [self.x_left, +1.17, 0.0],
            "s3_center": [self.x_left, -1.17, 0.0],
            "s2_center": [self.x_right, +1.17, 0.0],
            "s4_center": [self.x_right, -1.17, 0.0],
            "load_center": [0.0, 0.0, 0.0],
        }
        anchor_group = VGroup()
        for k, pt in anchor_coords.items():
            d = Dot(pt, radius=0.001, fill_opacity=0.0, stroke_opacity=0.0)
            self._anchors[k] = d
            anchor_group.add(d)

        # 1. DC Bus Source & Rails
        dc_top_wire = Line([self.x_dc, +0.20, 0], [self.x_dc, self.y_top, 0], color=INK, stroke_width=2.6)
        dc_bot_wire = Line([self.x_dc, -0.20, 0], [self.x_dc, self.y_bot, 0], color=INK, stroke_width=2.6)
        dc_long_bar = Line([self.x_dc - 0.32, +0.20, 0], [self.x_dc + 0.32, +0.20, 0], color=INK, stroke_width=2.8)
        dc_short_bar = Line([self.x_dc - 0.18, -0.20, 0], [self.x_dc + 0.18, -0.20, 0], color=INK, stroke_width=5.2)
        plus_mark = math_tnr("+", font_size=22, color=INK).move_to([self.x_dc - 0.44, +0.42, 0])
        minus_mark = math_tnr("-", font_size=24, color=INK).move_to([self.x_dc - 0.44, -0.42, 0])
        u_label = math_tnr("U", font_size=34, color=INK).move_to([self.x_dc - 0.62, 0.0, 0])

        top_rail = Line([self.x_dc, self.y_top, 0], [self.x_right, self.y_top, 0], color=INK, stroke_width=2.8)
        bot_rail = Line([self.x_dc, self.y_bot, 0], [self.x_right, self.y_bot, 0], color=INK, stroke_width=2.8)
        self.bus_group = VGroup(
            dc_top_wire, dc_bot_wire, dc_long_bar, dc_short_bar, plus_mark, minus_mark, u_label, top_rail, bot_rail
        )

        # 2. Left Leg & Parallel Freewheeling Diodes (D1, D3)
        self.switches: dict[str, dict] = {}
        self.left_leg_group = self._build_leg(
            side="left",
            x_leg=self.x_left,
            x_d=self.x_left_d,
            sw_names=("S1", "S3"),
            d_names=("D1", "D3"),
            sw_label_x=self.x_left + 0.56,
            d_label_x=self.x_left_d - 0.44,
            blade_open_angle=-32 * DEGREES,  # swing inward/right away from left diode
        )

        # 3. Right Leg & Parallel Freewheeling Diodes (D2, D4)
        self.right_leg_group = self._build_leg(
            side="right",
            x_leg=self.x_right,
            x_d=self.x_right_d,
            sw_names=("S2", "S4"),
            d_names=("D2", "D4"),
            sw_label_x=self.x_right - 0.56,
            d_label_x=self.x_right_d + 0.44,
            blade_open_angle=+32 * DEGREES,  # swing inward/left away from right diode
        )

        # 4. Central Load Leads + Box & RL Equivalent
        mid_dot_l = Dot([self.x_left, 0.0, 0], radius=0.06, color=INK)
        mid_dot_r = Dot([self.x_right, 0.0, 0], radius=0.06, color=INK)
        lead_l = Line([self.x_left, 0.0, 0], [-0.94, 0.0, 0], color=INK, stroke_width=2.6)
        lead_r = Line([+0.94, 0.0, 0], [self.x_right, 0.0, 0], color=INK, stroke_width=2.6)
        self.load_leads_group = VGroup(mid_dot_l, mid_dot_r, lead_l, lead_r)

        self.load_box_group = self._build_load_box()
        self.load_rl_group = self._build_load_rl()

        self.rl_mode = rl_mode
        if rl_mode:
            self.active_load = self.load_rl_group
        else:
            self.active_load = self.load_box_group

        # Polarity overlay group (managed cleanly via set_polarity with caching)
        self.polarity_group = VGroup()
        self._polarity_cache_key: tuple | None = None
        # Pre-render static glyph templates once so 60fps updaters never re-invoke TeX
        self._pol_glyphs = {
            "plus_red": math_tnr("+", font_size=28, color=RED_POS),
            "minus_red": math_tnr("-", font_size=30, color=RED_POS),
            "u_pos": math_tnr("+U", font_size=30, color=RED_POS),
            "minus_blue": math_tnr("-", font_size=30, color=BLUE_NEG),
            "plus_blue": math_tnr("+", font_size=28, color=BLUE_NEG),
            "u_neg": math_tnr("-U", font_size=30, color=BLUE_NEG),
        }

        self.add(
            anchor_group,
            self.bus_group,
            self.left_leg_group,
            self.right_leg_group,
            self.load_leads_group,
            self.active_load,
            self.polarity_group,
        )

    def _make_diode(self, x: float, y_center: float) -> VGroup:
        """Upward-pointing freewheeling diode centered at (x, y_center)."""
        tip_y = y_center + 0.14
        base_y = y_center - 0.14
        tri = Polygon(
            [x, tip_y, 0],
            [x - 0.15, base_y, 0],
            [x + 0.15, base_y, 0],
            fill_color="#FFFFFF",
            fill_opacity=1.0,
            stroke_color=INK,
            stroke_width=2.4,
        )
        bar = Line([x - 0.16, tip_y, 0], [x + 0.16, tip_y, 0], color=INK, stroke_width=2.8)
        return VGroup(tri, bar)

    def _build_switch_unit(self, name: str, x: float, y_top: float, y_bot: float, open_ang: float) -> VGroup:
        top_dot = Dot([x, y_top, 0], radius=0.052, color=INK)
        pivot_dot = Dot([x, y_bot, 0], radius=0.052, color=INK)
        blade = Line([x, y_bot, 0], [x, y_top, 0], color=INK, stroke_width=3.2)
        blade.rotate(open_ang, about_point=np.array([x, y_bot, 0]))
        self.switches[name] = {
            "blade": blade,
            "pivot": pivot_dot,
            "top": top_dot,
            "open_angle": open_ang,
            "is_closed": False,
        }
        return VGroup(top_dot, pivot_dot, blade)

    def _build_leg(
        self,
        side: str,
        x_leg: float,
        x_d: float,
        sw_names: tuple[str, str],
        d_names: tuple[str, str],
        sw_label_x: float,
        d_label_x: float,
        blade_open_angle: float,
    ) -> VGroup:
        # Upper vertical wires (top rail -> switch -> midpoint)
        w_u1 = Line([x_leg, self.y_top, 0], [x_leg, self.y_up_top_contact, 0], color=INK, stroke_width=2.6)
        w_u2 = Line([x_leg, self.y_up_bot_pivot, 0], [x_leg, 0.0, 0], color=INK, stroke_width=2.6)
        sw_up = self._build_switch_unit(sw_names[0], x_leg, self.y_up_top_contact, self.y_up_bot_pivot, blade_open_angle)
        lbl_sw_up = math_tnr(f"S_{{{sw_names[0][1:]}}}", font_size=30, color=INK).move_to([sw_label_x, +1.17, 0])

        # Lower vertical wires (midpoint -> switch -> bottom rail)
        w_d1 = Line([x_leg, 0.0, 0], [x_leg, self.y_dn_top_contact, 0], color=INK, stroke_width=2.6)
        w_d2 = Line([x_leg, self.y_dn_bot_pivot, 0], [x_leg, self.y_bot, 0], color=INK, stroke_width=2.6)
        sw_dn = self._build_switch_unit(sw_names[1], x_leg, self.y_dn_top_contact, self.y_dn_bot_pivot, blade_open_angle)
        lbl_sw_dn = math_tnr(f"S_{{{sw_names[1][1:]}}}", font_size=30, color=INK).move_to([sw_label_x, -1.17, 0])

        # Upper parallel diode bypass loop
        d_up_wires = VGroup(
            Dot([x_leg, self.y_up_tap_hi, 0], radius=0.045, color=INK),
            Dot([x_leg, self.y_up_tap_lo, 0], radius=0.045, color=INK),
            Line([x_leg, self.y_up_tap_hi, 0], [x_d, self.y_up_tap_hi, 0], color=INK, stroke_width=2.2),
            Line([x_d, self.y_up_tap_hi, 0], [x_d, +1.31, 0], color=INK, stroke_width=2.2),
            Line([x_d, +1.03, 0], [x_d, self.y_up_tap_lo, 0], color=INK, stroke_width=2.2),
            Line([x_d, self.y_up_tap_lo, 0], [x_leg, self.y_up_tap_lo, 0], color=INK, stroke_width=2.2),
        )
        d_up_sym = self._make_diode(x_d, +1.17)
        lbl_d_up = math_tnr(f"D_{{{d_names[0][1:]}}}", font_size=26, color=INK_MUTED).move_to([d_label_x, +1.17, 0])

        # Lower parallel diode bypass loop
        d_dn_wires = VGroup(
            Dot([x_leg, self.y_dn_tap_hi, 0], radius=0.045, color=INK),
            Dot([x_leg, self.y_dn_tap_lo, 0], radius=0.045, color=INK),
            Line([x_leg, self.y_dn_tap_hi, 0], [x_d, self.y_dn_tap_hi, 0], color=INK, stroke_width=2.2),
            Line([x_d, self.y_dn_tap_hi, 0], [x_d, -1.03, 0], color=INK, stroke_width=2.2),
            Line([x_d, -1.31, 0], [x_d, self.y_dn_tap_lo, 0], color=INK, stroke_width=2.2),
            Line([x_d, self.y_dn_tap_lo, 0], [x_leg, self.y_dn_tap_lo, 0], color=INK, stroke_width=2.2),
        )
        d_dn_sym = self._make_diode(x_d, -1.17)
        lbl_d_dn = math_tnr(f"D_{{{d_names[1][1:]}}}", font_size=26, color=INK_MUTED).move_to([d_label_x, -1.17, 0])

        # Rail junction dots
        rail_dots = VGroup(
            Dot([x_leg, self.y_top, 0], radius=0.052, color=INK),
            Dot([x_leg, self.y_bot, 0], radius=0.052, color=INK),
        )

        # Store sub-groups for clean sequential drawing in Shot 2
        leg = VGroup(
            rail_dots,
            w_u1, w_u2, w_d1, w_d2,
            sw_up, sw_dn,
            lbl_sw_up, lbl_sw_dn,
            d_up_wires, d_up_sym, lbl_d_up,
            d_dn_wires, d_dn_sym, lbl_d_dn,
        )
        setattr(self, f"{side}_diode_group", VGroup(d_up_wires, d_up_sym, lbl_d_up, d_dn_wires, d_dn_sym, lbl_d_dn))
        setattr(self, f"{side}_sw_group", VGroup(rail_dots, w_u1, w_u2, w_d1, w_d2, sw_up, sw_dn, lbl_sw_up, lbl_sw_dn))
        return leg

    def _build_load_box(self) -> VGroup:
        box = RoundedRectangle(
            width=1.88,
            height=0.80,
            corner_radius=0.10,
            fill_color="#FFFFFF",
            fill_opacity=1.0,
            stroke_color=INK,
            stroke_width=2.6,
        )
        txt = zh_label("负载", font_size=24, color=INK)
        return VGroup(box, txt)

    def _build_load_rl(self) -> VGroup:
        bg = RoundedRectangle(
            width=1.96,
            height=1.06,
            corner_radius=0.10,
            fill_color="#FFFFFF",
            fill_opacity=0.96,
            stroke_color="#9CA3AF",
            stroke_width=1.4,
        )
        bg_dashed = DashedVMobject(bg, num_dashes=26, dashed_ratio=0.55)

        # Resistor zigzag from x=-0.82 to x=-0.20
        r_pts = [
            [-0.94, 0.0, 0],
            [-0.78, 0.0, 0],
            [-0.72, +0.16, 0],
            [-0.62, -0.16, 0],
            [-0.52, +0.16, 0],
            [-0.42, -0.16, 0],
            [-0.32, +0.16, 0],
            [-0.24, 0.0, 0],
            [-0.02, 0.0, 0],
        ]
        resistor = VMobject(color=INK, stroke_width=2.6).set_points_as_corners([np.array(p) for p in r_pts])

        # 4-arch inductor coil from x=+0.02 to x=+0.78
        coils = VGroup()
        x0 = 0.02
        arch_w = 0.19
        for idx in range(4):
            cx = x0 + (idx + 0.5) * arch_w
            arc = ArcBetweenPoints(
                np.array([cx - arch_w / 2.0, 0.0, 0.0]),
                np.array([cx + arch_w / 2.0, 0.0, 0.0]),
                angle=-PI,
                color=INK,
                stroke_width=2.6,
            )
            coils.add(arc)
        lead_out = Line([0.78, 0.0, 0.0], [0.94, 0.0, 0.0], color=INK, stroke_width=2.6)

        lbl_r = math_tnr("R", font_size=24, color=INK).move_to([-0.52, -0.38, 0.0])
        lbl_l = math_tnr("L", font_size=24, color=INK).move_to([+0.40, -0.38, 0.0])
        return VGroup(bg_dashed, resistor, coils, lead_out, lbl_r, lbl_l)

    def morph_to_rl_instant(self) -> None:
        """Replace simple load box with RL equivalent cleanly in place."""
        if self.rl_mode:
            return
        self.load_rl_group.match_width(self.load_box_group, stretch=False)
        self.load_rl_group.move_to(self.load_box_group.get_center())
        self.remove(self.active_load)
        self.active_load = self.load_rl_group
        self.add(self.active_load)
        self.rl_mode = True

    def get_anchor(self, key: str) -> np.ndarray:
        return self._anchors[key].get_center().copy()

    def set_switch_state(
        self,
        s1: bool = False,
        s2: bool = False,
        s3: bool = False,
        s4: bool = False,
        short_left: bool = False,
    ) -> None:
        """Set exact blade geometry and color instantaneously (safe inside updaters)."""
        desired = {"S1": s1, "S2": s2, "S3": s3, "S4": s4}
        for name, target_closed in desired.items():
            sw = self.switches[name]
            p_bot = sw["pivot"].get_center()
            p_top = sw["top"].get_center()
            vec = p_top - p_bot
            if target_closed:
                sw["blade"].put_start_and_end_on(p_bot, p_top)
            else:
                ang = sw["open_angle"]
                ca, sa = float(np.cos(ang)), float(np.sin(ang))
                rot_vec = np.array([ca * vec[0] - sa * vec[1], sa * vec[0] + ca * vec[1], 0.0])
                sw["blade"].put_start_and_end_on(p_bot, p_bot + rot_vec)
            sw["is_closed"] = target_closed
            if short_left and target_closed and name in ("S1", "S3"):
                col = SHORT_RED
            elif target_closed and name in ("S1", "S4"):
                col = RED_POS
            elif target_closed and name in ("S2", "S3"):
                col = BLUE_NEG
            else:
                col = INK
            sw["blade"].set_color(col)

    def animate_switch_state(
        self,
        s1: bool = False,
        s2: bool = False,
        s3: bool = False,
        s4: bool = False,
        short_left: bool = False,
    ) -> list[Animation]:
        """Return smooth blade rotation animations to reach desired switch states."""
        desired = {"S1": s1, "S2": s2, "S3": s3, "S4": s4}
        anims: list[Animation] = []
        for name, target_closed in desired.items():
            sw = self.switches[name]
            if short_left and target_closed and name in ("S1", "S3"):
                col = SHORT_RED
            elif target_closed and name in ("S1", "S4"):
                col = RED_POS
            elif target_closed and name in ("S2", "S3"):
                col = BLUE_NEG
            else:
                col = INK
            if sw["is_closed"] != target_closed:
                delta = -sw["open_angle"] if target_closed else +sw["open_angle"]
                sw["blade"].set_color(col)
                anims.append(
                    Rotate(sw["blade"], angle=delta, about_point=sw["pivot"].get_center())
                )
                sw["is_closed"] = target_closed
            else:
                sw["blade"].set_color(col)
        return anims

    def set_polarity(self, sign: int) -> None:
        """Display + / - / (+U or -U) above load terminals (sign in {-1, 0, +1}), cached for 60fps."""
        if sign == 0:
            if self._polarity_cache_key != (0,):
                self.polarity_group.submobjects.clear()
                self._polarity_cache_key = (0,)
            return

        pt_l = self.get_anchor("lt_mid")
        pt_r = self.get_anchor("rt_mid")
        pt_c = self.get_anchor("load_center")
        key = (
            sign,
            round(float(pt_l[0]), 3),
            round(float(pt_l[1]), 3),
            round(float(pt_r[0]), 3),
            round(float(pt_r[1]), 3),
        )
        if key == self._polarity_cache_key:
            return

        self._polarity_cache_key = key
        self.polarity_group.submobjects.clear()
        scale_est = np.linalg.norm(pt_r - pt_l) / (self.x_right - self.x_left)
        dy = 0.78 * scale_est
        dx = 0.28 * scale_est
        sym_scale = max(0.60, float(scale_est))

        if sign > 0:
            l_sym = self._pol_glyphs["plus_red"].copy().scale(sym_scale)
            r_sym = self._pol_glyphs["minus_red"].copy().scale(sym_scale)
            v_lbl = self._pol_glyphs["u_pos"].copy().scale(sym_scale)
        else:
            l_sym = self._pol_glyphs["minus_blue"].copy().scale(sym_scale)
            r_sym = self._pol_glyphs["plus_blue"].copy().scale(sym_scale)
            v_lbl = self._pol_glyphs["u_neg"].copy().scale(sym_scale)

        l_sym.move_to(pt_l + RIGHT * dx + UP * (0.34 * scale_est))
        r_sym.move_to(pt_r + LEFT * dx + UP * (0.34 * scale_est))
        v_lbl.move_to(pt_c + UP * dy)
        self.polarity_group.add(l_sym, r_sym, v_lbl)

    def get_mode_path(self, mode: str) -> tuple[list[np.ndarray], str]:
        """Return exact live-transformed polyline points & color for a conduction mode."""
        a = self.get_anchor
        if mode == "S1_S4":
            pts = [
                a("dc_plus"), a("dc_top"), a("lt_top"), a("lt_mid"),
                a("rt_mid"), a("rb_bot"), a("dc_bot"), a("dc_minus"),
            ]
            return pts, RED_POS
        if mode == "S2_S3":
            pts = [
                a("dc_plus"), a("dc_top"), a("rt_top"), a("rt_mid"),
                a("lt_mid"), a("lb_bot"), a("dc_bot"), a("dc_minus"),
            ]
            return pts, BLUE_NEG
        if mode == "D2_D3":
            # Freewheeling when u = -U, i > 0 (flows left->right through load, back into DC+)
            pts = [
                a("dc_minus"), a("dc_bot"), a("lb_bot"), a("lb_tap_lo"),
                a("lb_d_lo"), a("lb_d_hi"), a("lb_tap_hi"), a("lt_mid"),
                a("rt_mid"), a("rt_tap_lo"), a("rt_d_lo"), a("rt_d_hi"),
                a("rt_tap_hi"), a("rt_top"), a("dc_top"), a("dc_plus"),
            ]
            return pts, AMBER_FW
        if mode == "D1_D4":
            # Freewheeling when u = +U, i < 0 (flows right->left through load, back into DC+)
            pts = [
                a("dc_minus"), a("dc_bot"), a("rb_bot"), a("rb_tap_lo"),
                a("rb_d_lo"), a("rb_d_hi"), a("rb_tap_hi"), a("rt_mid"),
                a("lt_mid"), a("lt_tap_lo"), a("lt_d_lo"), a("lt_d_hi"),
                a("lt_tap_hi"), a("lt_top"), a("dc_top"), a("dc_plus"),
            ]
            return pts, AMBER_FW
        if mode == "SHORT_LEFT":
            pts = [
                a("dc_plus"), a("dc_top"), a("lt_top"),
                a("lb_bot"), a("dc_bot"), a("dc_minus"),
            ]
            return pts, SHORT_RED
        return [], INK

    def build_current_overlay(
        self,
        mode: str,
        phase: float = 0.0,
        n_markers: int = 14,
        stroke_scale: float = 1.0,
    ) -> VGroup:
        """Build glowing conducting wire overlay + directional flow chevrons across the entire loop."""
        pts, color = self.get_mode_path(mode)
        if not pts:
            return VGroup()
        glow = VMobject(color=color, stroke_width=9.5 * stroke_scale, stroke_opacity=0.26)
        glow.set_points_as_corners(pts)
        wire = VMobject(color=color, stroke_width=3.6 * stroke_scale, stroke_opacity=0.96)
        wire.set_points_as_corners(pts)
        chevrons = sample_polyline_chevrons(
            pts, phase=phase, color=color, n_markers=n_markers, size=0.105 * stroke_scale
        )
        return VGroup(glow, wire, chevrons)
