# -*- coding: utf-8 -*-
"""공식 Part 2의 1T1C 구조와 DC-current 기반 READ/retention.

전류는 접점에서 소자로 들어가는 방향이 양수다. Capacitor node charge 변화는
−I_terminal*dt이며 A/µm→A 변환은 여기서 W=0.1 µm를 한 번만 적용한다.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Callable

import devsim
import pandas as pd
from devsim.python_packages.model_create import CreateSolution
from devsim.python_packages.simple_physics import (CreateOxideContact, CreateOxidePotentialOnly,
                                                  SetOxideParameters)

from .config import Device
from .simulator import MosfetSimulator, NM, UM

EPS0_F_CM = 8.85e-14  # 기존 DEVSIM helper와 같은 상수. 내부 길이는 cm다.
CAP_KAPPA = {"SiO2": 3.9, "Al2O3": 9.0, "HfO2": 20.0, "ZrO2": 35.0}
WIDTH_UM = 0.1
CBL_F = 100e-15
READ_DT_S = 10e-12
READ_TIME_S = 0.5e-9
READ_MARGIN_V = 0.060


@dataclass(frozen=True)
class Capacitor:
    """Source 위 금속 기둥 양쪽의 두 수직 dielectric slab."""

    material: str = "ZrO2"
    height_um: float = 0.9
    dielectric_nm: float = 3.0
    pillar_width_um: float = 0.1
    bottom_clearance_um: float = 0.05

    def __post_init__(self):
        if self.material not in CAP_KAPPA:
            raise ValueError("Use an assignment capacitor material name")
        if not math.isfinite(self.height_um) or not 0.2 <= self.height_um <= 1.5:
            raise ValueError("Capacitor height must be 0.2..1.5 um")
        if not math.isfinite(self.dielectric_nm) or not 3 <= self.dielectric_nm <= 10:
            raise ValueError("Dielectric thickness must be 3..10 nm")
        if any(not math.isfinite(v) or v <= 0
               for v in (self.pillar_width_um, self.bottom_clearance_um)):
            raise ValueError("Pillar width and clearance must be positive")

    @property
    def parallel_plate_f(self):
        return 2 * CAP_KAPPA[self.material] * EPS0_F_CM * self.height_um * UM / (
            self.dielectric_nm * NM) * WIDTH_UM * UM


def validate_cell_device(device: Device, capacitor: Capacitor) -> None:
    # Same physical ranges as Part 1, except fixed Part 2 geometry/temperature.
    from dataclasses import replace
    from part1 import validate_device
    validate_device(replace(device, temperature_k=300.0))
    if device.gate_length_um != 0.3 or device.oxide_thickness_nm < 5:
        raise ValueError("Part 2 requires Lg=0.3 um and tox>=5 nm")
    if device.temperature_k != 398.0:
        raise ValueError("Part 2 uses T=398 K")
    if capacitor.pillar_width_um + 2 * capacitor.dielectric_nm / 1000 >= device.source_length_um:
        raise ValueError("Capacitor must fit above the source")


class CellSimulator(MosfetSimulator):
    """TR physics/transport는 기존 simulator 그대로, 분리된 ideal-metal capacitor 추가.

    Metal stem은 source에 닿는 inert label이다. Storage contacts는 source bias에
    묶인다. Dielectric은 stem의 상단에 있어 bulk와 닿지 않으므로 bulk-hk interface가
    없다. 접하지 않는 영역에 임의 interface를 만들지 않는다.
    """

    def __init__(self, device: Device, capacitor: Capacitor, name: str = "part2_cell"):
        validate_cell_device(device, capacitor)
        super().__init__(device, name)
        self.capacitor = capacitor

    def _build_mesh(self):
        # 기존 planar TR의 좌표·접점 배치를 유지한 독립 cell mesh builder.
        cap = self.capacitor
        pad = 1e-8
        center = self.x_gate_left / 2
        left, right = center - cap.pillar_width_um * UM / 2, center + cap.pillar_width_um * UM / 2
        thickness = cap.dielectric_nm * NM
        bottom = -cap.bottom_clearance_um * UM
        top = bottom - cap.height_um * UM
        metal_top = self.y_oxide_top - 10 * NM
        devsim.create_2d_mesh(mesh=self.mesh)
        for x, dx in ((-pad, self.DX_CHANNEL), (0, self.DX_CHANNEL),
                      (left-thickness, thickness/2), (left, thickness/2),
                      (right, thickness/2), (right+thickness, thickness/2),
                      (self.x_gate_left, self.DX_CHANNEL),
                      (self.x_gate_right, self.DX_CHANNEL),
                      (self.x_right, self.DX_CHANNEL), (self.x_right+pad, self.DX_CHANNEL)):
            devsim.add_2d_mesh_line(mesh=self.mesh, dir="x", pos=x, ps=dx)
        for y, dy in ((top-pad, self.DY_BULK), (top, self.DY_BULK),
                      (bottom, self.DY_BULK), (metal_top, self.DY_OXIDE),
                      (self.y_oxide_top, self.DY_OXIDE), (0, self.DY_OXIDE),
                      (self.y_junction, self.DY_JUNCTION), (self.y_bottom, self.DY_BULK),
                      (self.y_bottom+pad, self.DY_BULK)):
            devsim.add_2d_mesh_line(mesh=self.mesh, dir="y", pos=y, ps=dy)
        devsim.add_2d_region(mesh=self.mesh, material="Air", region="air")
        for name, material, xl, xh, yl, yh in (
            ("bulk", "Silicon", 0, self.x_right, 0, self.y_bottom),
            ("oxide", "Oxide", self.x_gate_left, self.x_gate_right, self.y_oxide_top, 0),
            ("gate_metal", self.dev.gate_material, self.x_gate_left, self.x_gate_right,
             metal_top, self.y_oxide_top),
            ("metal_storage", "Metal", left, right, top, 0),
            ("hk_l", cap.material, left-thickness, left, top, bottom),
            ("hk_r", cap.material, right, right+thickness, top, bottom),
        ):
            devsim.add_2d_region(mesh=self.mesh, region=name, material=material,
                                 xl=xl, xh=xh, yl=yl, yh=yh)
        for name, region, xl, xh, yl, yh in (
            ("gate", "oxide", self.x_gate_left, self.x_gate_right, self.y_oxide_top, self.y_oxide_top),
            ("source", "bulk", 0, self.x_gate_left, 0, 0),
            ("drain", "bulk", self.x_gate_right, self.x_right, 0, 0),
            ("body", "bulk", 0, self.x_right, self.y_bottom, self.y_bottom),
            ("storage_l", "hk_l", left, left, top, bottom),
            ("plate_l", "hk_l", left-thickness, left-thickness, top, bottom),
            ("storage_r", "hk_r", right, right, top, bottom),
            ("plate_r", "hk_r", right+thickness, right+thickness, top, bottom),
        ):
            devsim.add_2d_contact(mesh=self.mesh, name=name, region=region, material="metal",
                                  xl=xl, xh=xh, yl=yl, yh=yh)
        devsim.add_2d_interface(mesh=self.mesh, name="bulk_oxide", region0="bulk", region1="oxide")
        devsim.finalize_mesh(mesh=self.mesh)
        devsim.create_device(mesh=self.mesh, device=self.name)

    def _build_physics(self):
        super()._build_physics()
        for side in ("l", "r"):
            region = f"hk_{side}"
            material = devsim.get_material(device=self.name, region=region)
            if material not in CAP_KAPPA:
                raise ValueError("Unsupported capacitor material in saved structure")
            CreateSolution(self.name, region, "Potential")
            SetOxideParameters(self.name, region, self.dev.temperature_k)
            devsim.set_parameter(device=self.name, region=region, name="Permittivity",
                                 value=EPS0_F_CM * CAP_KAPPA[material])
            CreateOxidePotentialOnly(self.name, region, "log_damp")
            for contact, bias in ((f"storage_{side}", 0.0), (f"plate_{side}", 1.0)):
                devsim.set_parameter(device=self.name, name=f"{contact}_bias", value=bias)
                CreateOxideContact(self.name, region, contact)

    def _solve(self):
        # Source가 ramp의 중간값일 때에도 storage electrodes를 같은 외부 전압에 묶는다.
        source = devsim.get_parameter(device=self.name, name="source_bias")
        for side in ("l", "r"):
            devsim.set_parameter(device=self.name, name=f"storage_{side}_bias", value=source)
        super()._solve()

    def extract_capacitance(self, delta_v: float = 0.01):
        if not math.isfinite(delta_v) or delta_v <= 0:
            raise ValueError("Positive plate perturbation required")
        values = []
        for voltage in (1-delta_v, 1, 1+delta_v):
            for side in ("l", "r"):
                devsim.set_parameter(device=self.name, name=f"plate_{side}_bias", value=voltage)
            self._solve()
            q = sum(devsim.get_contact_charge(device=self.name, contact=f"plate_{side}",
                                               equation="PotentialEquation") for side in ("l", "r"))
            values.append({"plate_V": voltage, "plate_charge_C": q * WIDTH_UM * UM})
        for side in ("l", "r"):
            devsim.set_parameter(device=self.name, name=f"plate_{side}_bias", value=1.0)
        self._solve()
        capacitance = (values[2]["plate_charge_C"]-values[0]["plate_charge_C"]) / (2*delta_v)
        if not math.isfinite(capacitance) or capacitance <= 0:
            raise RuntimeError("Non-positive or non-finite extracted CSTORE")
        return capacitance, values

    def current_at(self, wl_v, cell_v, bl_v):
        # READ는 S/D를 함께 갱신한 하나의 DC 상태를 요구한다. 모든 접점을 같은
        # ramp 비율로 이동시켜 중복 solve를 줄이되 각 접점의 최대 변화는 0.1 V다.
        target = {"body": -0.5, "gate": wl_v, "drain": bl_v, "source": cell_v}
        if not all(math.isfinite(v) for v in target.values()):
            raise ValueError("Finite operating point required")
        start = dict(self.bias)
        maximum_change = max(abs(target[c]-start[c]) for c in target)
        steps = 0 if maximum_change == 0 else max(1, math.ceil(maximum_change/self.RAMP_STEP_V-1e-9))
        for i in range(1, steps+1):
            for contact in target:
                value = start[contact]+(target[contact]-start[contact])*i/steps
                devsim.set_parameter(device=self.name, name=f"{contact}_bias", value=value)
            self._solve()
        self.bias.update(target)
        currents = self.contact_currents()
        validate_currents(currents)
        return currents


def validate_currents(currents):
    if not all(math.isfinite(currents[c]) for c in ("drain", "source", "body")):
        raise RuntimeError("Non-finite terminal current")
    scale = max(abs(v) for v in currents.values())
    if abs(sum(currents.values())) > max(1e-17, 1e-6 * scale):
        raise RuntimeError("Terminal current conservation failed")


def read_transient(current_at: Callable, initial_cell_v: float, cstore_f: float,
                   dt_s: float = READ_DT_S) -> tuple[pd.DataFrame, dict]:
    """Two-terminal current 방식; 몸체로 흐르는 전하는 balance 항에 포함한다."""
    if not all(math.isfinite(v) for v in (initial_cell_v, cstore_f, dt_s)):
        raise ValueError("Finite READ inputs required")
    if not 0 <= initial_cell_v <= 2 or not 0 < cstore_f <= 20e-15 or dt_s <= 0:
        raise ValueError("Invalid cell voltage, capacitance or time step")
    steps = round(READ_TIME_S / dt_s)
    if steps < 1 or not math.isclose(steps*dt_s, READ_TIME_S, rel_tol=1e-12):
        raise ValueError("READ dt must partition 0.5 ns exactly")
    cell_v, bl_v = initial_cell_v, 1.0
    initial_q = cstore_f*cell_v + CBL_F*bl_v
    body_q = 0.0
    rows = [{"time_s": 0.0, "Vcell_V": cell_v, "VBL_V": bl_v,
             "Id_A": None, "Is_A": None, "Ib_A": None, "charge_residual_C": 0.0}]
    for i in range(steps):
        currents = current_at(2.5, cell_v, bl_v)
        validate_currents(currents)
        id_a, is_a, ib_a = (currents[c]*WIDTH_UM for c in ("drain", "source", "body"))
        cell_v -= is_a * dt_s / cstore_f
        bl_v -= id_a * dt_s / CBL_F
        body_q += ib_a * dt_s
        if not all(math.isfinite(v) and -0.05 <= v <= 2.05 for v in (cell_v, bl_v)):
            raise RuntimeError("READ integration overshoot; do not clamp voltages")
        residual = cstore_f*cell_v + CBL_F*bl_v - initial_q - body_q
        rows.append({"time_s": (i+1)*dt_s, "Vcell_V": cell_v, "VBL_V": bl_v,
                     "Id_A": id_a, "Is_A": is_a, "Ib_A": ib_a,
                     "charge_residual_C": residual})
    margin = abs(bl_v-1)
    return pd.DataFrame(rows), {"initial_cell_V": initial_cell_v, "dt_s": dt_s,
                               "decision_time_s": READ_TIME_S, "margin_V": margin,
                               "passed": margin >= READ_MARGIN_V,
                               "max_charge_residual_C": max(abs(r["charge_residual_C"]) for r in rows)}


def retention(current_at: Callable, read_margin: Callable, initial_cell_v: float,
              cstore_f: float, max_time_s: float = 0.064,
              max_delta_v: float = 0.003, max_step_s: float = 0.008,
              read_checkpoint_v: float = 0.03):
    """누설은 3 mV 이하 step, READ는 checkpoint 및 실패 interval refinement.

    Max time까지 실패하지 않으면 정확한 tret이 아니라 해당 시간의 lower bound다.
    첫 sampled failure 구간은 재적분+READ bisection으로 1% time bracket까지 좁힌다.
    Checkpoint 사이의 단일 failure crossing을 가정하며 관측 margin도 보존한다.
    실패 bracket이 64 ms를 걸치면 PASS로 단정하지 않는다.
    """
    if initial_cell_v not in (0.0, 2.0):
        raise ValueError("Retention initial state must be 0 or 2 V")
    if not all(math.isfinite(v) and v > 0
               for v in (cstore_f, max_time_s, max_delta_v, max_step_s, read_checkpoint_v)):
        raise ValueError("Positive retention integration settings required")
    if cstore_f > 20e-15:
        raise ValueError("CSTORE exceeds 20 fF")
    bl_v = 2.0 if initial_cell_v == 0 else 0.0
    cell_v, time_s = initial_cell_v, 0.0
    margin = read_margin(cell_v)
    rows = [{"time_s": time_s, "Vcell_V": cell_v, "read_margin_V": margin,
             "dt_s": 0.0, "Istorage_A": None}]
    if not math.isfinite(margin):
        raise RuntimeError("Non-finite degraded READ margin")
    if margin < READ_MARGIN_V:
        return pd.DataFrame(rows), {"passed": False, "failure_bracket_s": [0, 0],
                                    "retention_lower_bound_s": 0.0, "reason": "Initial READ fails"}
    last_read_time, last_read_cell = 0.0, cell_v
    refinement = []

    def advance(start_time, start_cell, end_time):
        """재검증할 interval도 동일한 signed leakage·최대 ΔV로 재적분한다."""
        t, v = start_time, start_cell
        for _ in range(10000):
            if t >= end_time:
                return v
            currents = current_at(0.0, v, bl_v)
            validate_currents(currents)
            amperes = currents["source"] * WIDTH_UM
            dt = min(max_step_s, end_time-t,
                     max_delta_v*cstore_f/abs(amperes) if amperes else max_step_s)
            if t+dt == t:
                raise RuntimeError("Retention time step cannot advance")
            v -= amperes*dt/cstore_f
            t += dt
        raise RuntimeError("Retention refinement step limit exceeded")

    for _ in range(10000):
        if time_s >= max_time_s:
            break
        currents = current_at(0.0, cell_v, bl_v)
        validate_currents(currents)
        storage_a = currents["source"] * WIDTH_UM
        dt = min(max_step_s, max_time_s-time_s,
                 max_delta_v*cstore_f/abs(storage_a) if storage_a else max_step_s)
        if time_s+dt == time_s:
            raise RuntimeError("Retention time step cannot advance")
        cell_v -= storage_a*dt/cstore_f
        time_s += dt
        if not math.isfinite(cell_v) or not -0.05 <= cell_v <= 2.05:
            raise RuntimeError("Retention integration overshoot")
        check_read = (abs(cell_v-last_read_cell) >= read_checkpoint_v or
                      time_s-last_read_time >= max_step_s or time_s >= max_time_s)
        margin = read_margin(cell_v) if check_read else None
        if margin is not None and not math.isfinite(margin):
            raise RuntimeError("Non-finite degraded READ margin")
        rows.append({"time_s": time_s, "Vcell_V": cell_v, "read_margin_V": margin,
                     "dt_s": dt, "Istorage_A": storage_a})
        if check_read and margin < READ_MARGIN_V:
            low_t, low_v = last_read_time, last_read_cell
            high_t, high_v = time_s, cell_v
            coarse_bracket = [low_t, high_t]
            for _ in range(40):
                if high_t-low_t <= max(1e-8, high_t*0.01):
                    break
                middle = (low_t+high_t)/2
                middle_v = advance(low_t, low_v, middle)
                middle_margin = read_margin(middle_v)
                if not math.isfinite(middle_margin):
                    raise RuntimeError("Non-finite refined READ margin")
                refinement.append({"time_s": middle, "Vcell_V": middle_v,
                                   "read_margin_V": middle_margin})
                if middle_margin >= READ_MARGIN_V:
                    low_t, low_v = middle, middle_v
                else:
                    high_t, high_v = middle, middle_v
            return pd.DataFrame(rows), {"passed": low_t >= 0.064,
                                        "failure_bracket_s": [low_t, high_t],
                                        "retention_lower_bound_s": low_t,
                                        "coarse_failure_bracket_s": coarse_bracket,
                                        "read_checkpoint_delta_V": read_checkpoint_v,
                                        "refinement_trace": refinement,
                                        "failure_time_relative_bracket": (high_t-low_t)/high_t,
                                        "reason": "Degraded 0.5 ns READ margin below 60 mV"}
        if check_read:
            last_read_time, last_read_cell = time_s, cell_v
    else:
        raise RuntimeError("Retention step limit exceeded; preserve incomplete results")
    return pd.DataFrame(rows), {"passed": time_s >= 0.064,
                                "failure_bracket_s": None,
                                "retention_lower_bound_s": time_s,
                                "read_checkpoint_delta_V": read_checkpoint_v,
                                "refinement_trace": refinement,
                                "reason": "No read-margin failure observed; lower bound only"}
