# -*- coding: utf-8 -*-
"""Part 1 정전류·로그 전류 추출과 8개 spec의 독립 판정."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from collections.abc import Callable
import math

import numpy as np
import pandas as pd


class MeasurementError(ValueError):
    """주어진 데이터에서 정의된 지표를 신뢰할 수 있게 측정할 수 없음."""


def _curve_arrays(curve: pd.DataFrame | None) -> tuple[np.ndarray, np.ndarray]:
    if curve is None or not {"Vg_V", "Id_A_per_um"}.issubset(curve.columns):
        raise MeasurementError("Missing Vg_V/Id_A_per_um curve")
    vg = curve["Vg_V"].to_numpy(dtype=float)
    current = curve["Id_A_per_um"].to_numpy(dtype=float)
    if len(vg) < 2 or not np.isfinite(vg).all() or not np.isfinite(current).all():
        raise MeasurementError("Need at least two finite samples")
    if np.any(np.diff(vg) <= 0):
        raise MeasurementError("Gate voltages must be strictly increasing")
    return vg, current


def crossing_voltage(curve: pd.DataFrame | None, target_a_per_um: float) -> float:
    """양의 전류의 유일한 상승 crossing을 log10(I)에서 보간한다. 외삽은 없다."""
    vg, current = _curve_arrays(curve)
    if not math.isfinite(target_a_per_um) or target_a_per_um <= 0:
        raise MeasurementError("Target current must be finite and positive")
    exact = np.flatnonzero(current == target_a_per_um)
    rises = np.flatnonzero((current[:-1] < target_a_per_um) &
                          (current[1:] > target_a_per_um))
    falls = np.flatnonzero((current[:-1] > target_a_per_um) &
                          (current[1:] < target_a_per_um))
    if len(exact) + len(rises) + len(falls) > 1:
        raise MeasurementError("Ambiguous or non-monotonic current crossing")
    if len(exact) == 1:
        i = exact[0]
        if ((i > 0 and current[i-1] >= target_a_per_um) or
                (i + 1 < len(current) and current[i+1] <= target_a_per_um)):
            raise MeasurementError("Exact target sample must belong to a rising crossing")
        return float(vg[i])
    if len(rises) != 1 or len(falls):
        raise MeasurementError(f"Current {target_a_per_um:g} A/um has no rising bracket")
    i = rises[0]
    if current[i] <= 0:
        raise MeasurementError("Positive samples are required for logarithmic interpolation")
    fraction = math.log10(target_a_per_um / current[i]) / math.log10(current[i+1] / current[i])
    return float(vg[i] + fraction * (vg[i+1] - vg[i]))


def current_at_voltage(curve: pd.DataFrame | None, gate_v: float) -> float:
    """Ion/Ioff는 실제 해당 bias sample에서 읽는다. 전압 외삽·전류 clamp 금지."""
    vg, current = _curve_arrays(curve)
    at = np.flatnonzero(np.isclose(vg, gate_v, rtol=0.0, atol=1e-9))
    if len(at) != 1:
        raise MeasurementError(f"Need an actual VG={gate_v:g} V sample")
    value = float(current[at[0]])
    if value < 0:
        raise MeasurementError("Negative nMOS drain current; inspect raw currents and convergence")
    return value


@dataclass(frozen=True)
class SpecResult:
    name: str
    value: float | None
    unit: str
    minimum: float | None
    maximum: float | None
    status: str
    condition: str
    error: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def _spec(name: str, unit: str, condition: str, calculate: Callable[[], float],
          minimum: float | None = None, maximum: float | None = None) -> SpecResult:
    try:
        value = float(calculate())
        if not math.isfinite(value):
            raise MeasurementError("Non-finite metric")
    except MeasurementError as error:
        return SpecResult(name, None, unit, minimum, maximum, "ERROR", condition, str(error))
    passed = (minimum is None or value >= minimum) and (maximum is None or value <= maximum)
    return SpecResult(name, value, unit, minimum, maximum, "PASS" if passed else "FAIL", condition)


def evaluate_specs(low: pd.DataFrame | None, high: pd.DataFrame | None,
                   body: pd.DataFrame | None, hot_off_a_per_um: float | None,
                   oxide_thickness_nm: float) -> list[SpecResult]:
    """구조·gate 재료는 고정하고 정의된 세 Id–Vg와 398 K off-point를 사용한다."""
    def vth(curve: pd.DataFrame | None) -> float:
        return crossing_voltage(curve, 1e-7)

    def ss() -> float:
        result = (crossing_voltage(low, 1e-8) - crossing_voltage(low, 1e-10)) / 2 * 1000
        if result <= 0:
            raise MeasurementError("Non-positive subthreshold swing")
        return result

    def hot() -> float:
        if hot_off_a_per_um is None or not math.isfinite(hot_off_a_per_um) or hot_off_a_per_um < 0:
            raise MeasurementError("Missing or invalid 398 K off-current")
        return hot_off_a_per_um * 1e12

    def oxide_field() -> float:
        if not math.isfinite(oxide_thickness_nm) or oxide_thickness_nm <= 0:
            raise MeasurementError("Oxide thickness must be finite and positive")
        return 2 / (oxide_thickness_nm * 1e-7) / 1e6

    return [
        _spec("Vth", "V", "300 K, VD=0.05 V, VB=VS=0, ID=1e-7 A/um", lambda: vth(low), 0.40, 0.50),
        _spec("Ion", "uA/um", "300 K, VG=VD=2 V, VB=VS=0", lambda: current_at_voltage(high, 2) * 1e6, 450),
        _spec("Ioff", "pA/um", "300 K, VG=0, VD=2 V, VB=VS=0", lambda: current_at_voltage(high, 0) * 1e12, maximum=1),
        _spec("SS", "mV/dec", "300 K, VD=0.05 V, ID=1e-10..1e-8 A/um", ss, maximum=75),
        _spec("Ioff_398K", "pA/um", "398 K, VG=0, VD=2 V, VB=VS=0", hot, maximum=100),
        _spec("DIBL", "mV/V", "300 K, [Vth(VD=0.05)-Vth(VD=2)]/1.95", lambda: (vth(low) - vth(high)) / 1.95 * 1000, maximum=30),
        _spec("Body_effect", "V", "300 K, VD=0.05 V, Vth(VB=-0.5)-Vth(VB=0)", lambda: vth(body) - vth(low), maximum=0.08),
        _spec("Eox", "MV/cm", "VDD=2 V / tox", oxide_field, maximum=5),
    ]
