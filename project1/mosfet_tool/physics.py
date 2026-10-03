# -*- coding: utf-8 -*-
"""Part 1의 gate 기준 전위와 300 K에 anchor한 silicon 온도 모델.

모델 식·계수·출처·적용 한계는 project1/PART1_BASELINE.md에 기록한다.
Boltzmann/complete-ionization 및 기존 상수 이동도·수명 가정은 유지한다.
"""

from __future__ import annotations

import math

from .materials import GATE_WORK_FUNCTION_EV, canonical_gate_material

# 기존 DEVSIM helper와 같은 q/k를 사용해 단위·thermal voltage 기준을 유지한다.
Q_C = 1.6e-19
K_J_K = 1.3806503e-23
K_EV_K = K_J_K / Q_C
NI_300_CM3 = 1.0e10
NC_300_CM3 = 2.8e19
SI_AFFINITY_EV = 4.05
EG_ZERO_EV = 1.17
VARSHNI_ALPHA_EV_K = 4.73e-4
VARSHNI_BETA_K = 636.0


def silicon_bandgap_ev(temperature_k: float) -> float:
    """Varshni 식. 이 작업에서는 300/398 K의 비퇴화 모델을 검증한다."""
    if not math.isfinite(temperature_k) or temperature_k <= 0:
        raise ValueError("Temperature must be finite and positive")
    return EG_ZERO_EV - VARSHNI_ALPHA_EV_K * temperature_k**2 / (
        temperature_k + VARSHNI_BETA_K)


def silicon_properties(temperature_k: float, model: str = "varshni") -> dict[str, float]:
    """ni와 Nc에서 intrinsic-reference 일함수를 일관되게 계산한다."""
    bandgap = silicon_bandgap_ev(temperature_k)
    if model not in ("legacy", "varshni"):
        raise ValueError("Unknown silicon temperature model")
    vt = K_EV_K * temperature_k
    log_ni = math.log(NI_300_CM3)
    if model == "varshni":
        # Nc,Nv ∝ T^(3/2), ni ∝ sqrt(Nc*Nv)*exp(-Eg/(2kT)).
        # 300 K 값을 보존하는 비율식이며 실제 TA ni 모델과 동일함을 뜻하지 않는다.
        log_ni += 1.5 * math.log(temperature_k / 300.0)
        log_ni += silicon_bandgap_ev(300.0) / (2 * K_EV_K * 300.0)
        log_ni -= bandgap / (2 * vt)
    ni = NI_300_CM3 if temperature_k == 300.0 or model == "legacy" else math.exp(log_ni)
    nc = NC_300_CM3 * (temperature_k / 300.0)**1.5
    intrinsic_phi = SI_AFFINITY_EV + vt * math.log(nc / ni)
    return {"bandgap_eV": bandgap, "n_i_cm3": ni, "Nc_cm3": nc,
            "V_t_V": vt, "intrinsic_work_function_eV": intrinsic_phi}


def gate_offset_v(material: str, temperature_k: float, model: str) -> float:
    """psi_gate = VG − offset. PhiM 증가는 같은 양만큼 Vth를 높인다."""
    phi_m = GATE_WORK_FUNCTION_EV[canonical_gate_material(material)]
    return phi_m - silicon_properties(temperature_k, model)["intrinsic_work_function_eV"]
