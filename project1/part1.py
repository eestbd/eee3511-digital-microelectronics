# -*- coding: utf-8 -*-
"""동일한 저장 구조에서 Part 1의 8개 spec을 측정한다. 설계 탐색은 하지 않는다."""

from __future__ import annotations

import argparse
from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

import devsim
import numpy as np
import pandas as pd
import yaml

from mosfet_tool.config import Device
from mosfet_tool.metrics import evaluate_specs
from mosfet_tool.physics import silicon_properties
from mosfet_tool.simulator import MosfetSimulator, voltage_points

ROOT = Path(__file__).resolve().parent


def validate_device(device: Device) -> None:
    bounds = {
        "gate_length_um": (0.3, None), "source_length_um": (0.2, 1.0),
        "drain_length_um": (0.2, 1.0), "oxide_thickness_nm": (4.0, None),
        "silicon_thickness_um": (0.3, 2.0), "junction_depth_um": (0.02, 0.25),
        "body_doping_cm3": (1e14, 1e17), "sd_doping_cm3": (1e18, 1e21),
    }
    for name, (low, high) in bounds.items():
        value = getattr(device, name)
        if not np.isfinite(value) or value < low or (high is not None and value > high):
            raise ValueError(f"{name}={value!r} outside Part 1 range {low}..{high}")
    if device.junction_depth_um >= device.silicon_thickness_um:
        raise ValueError("Junction must be above the bottom of silicon")
    if device.gate_material is None or device.silicon_temperature_model != "varshni":
        raise ValueError("Part 1 requires an explicit gate material and varshni temperature model")
    if (device.mu_n, device.mu_p) != (400.0, 200.0):
        raise ValueError("Part 1 baseline keeps the original mu_n=400 and mu_p=200")
    if device.temperature_k != 300.0:
        raise ValueError("Base configuration temperature must be 300 K; hot case is separate")


def prepared_simulator(device: Device, structure: Path, temperature_k: float,
                       drain_v: float, body_v: float) -> MosfetSimulator:
    sim = MosfetSimulator(replace(device, temperature_k=temperature_k))
    sim.load_structure(structure)
    sim.solve_equilibrium()
    sim.enable_transport()
    if body_v != 0:
        sim.set_bias("body", body_v)
    sim.set_bias("drain", drain_v)
    return sim


def current_sample(sim: MosfetSimulator, gate_v: float) -> dict[str, float]:
    sim.set_bias("gate", gate_v)
    currents = sim.contact_currents()
    if not all(np.isfinite(v) for v in currents.values()):
        raise RuntimeError("Non-finite terminal current; inspect solver output")
    balance = sum(currents.values())
    scale = max(abs(v) for v in currents.values())
    return {"Vg_V": gate_v, "Id_A_per_um": currents["drain"],
            "Is_A_per_um": currents["source"], "Ib_A_per_um": currents["body"],
            "current_balance_A_per_um": balance,
            "relative_current_balance": abs(balance) / scale if scale else 0.0}


def run_evaluation(device: Device, voltages: np.ndarray, output_dir: Path,
                   extended_precision: bool) -> dict:
    validate_device(device)
    if voltages[0] != 0.0 or voltages[-1] != 2.0:
        raise ValueError("The baseline sweep must include actual VG=0 and 2 V endpoints")
    for name in ("extended_solver", "extended_model", "extended_equation"):
        devsim.set_parameter(name=name, value=extended_precision)
    output_dir.mkdir(parents=True, exist_ok=True)
    if any(output_dir.iterdir()):
        raise FileExistsError("Use a new empty output directory; existing results are preserved")
    # 긴 계산 도중 편집된 파일을 실제 실행 source로 오인하지 않도록 먼저 기록한다.
    source_sha256 = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in [ROOT / "part1.py", ROOT / "check_structure_file.py",
                               *sorted((ROOT / "mosfet_tool").glob("*.py"))]}
    structure = output_dir / "part1_baseline_diagnostic.devsim"
    MosfetSimulator(device, name="part1_baseline").build(structure)
    check = subprocess.run([sys.executable, "-B", str(ROOT / "check_structure_file.py"),
                            str(structure)], capture_output=True, text=True, encoding="utf-8")
    (output_dir / "checker.log").write_text(check.stdout + check.stderr, encoding="utf-8")
    if check.returncode != 0:
        raise RuntimeError("Structure checker failed; inspect checker.log")
    curves = {}
    for name, vd, vb in (("idvg_low", 0.05, 0.0), ("idvg_high", 2.0, 0.0),
                         ("idvg_body", 0.05, -0.5)):
        sim = prepared_simulator(device, structure, 300.0, vd, vb)
        frame = pd.DataFrame([current_sample(sim, float(vg)) for vg in voltages])
        frame.to_csv(output_dir / f"{name}.csv", index=False)
        curves[name] = frame
    sim = prepared_simulator(device, structure, 398.0, 2.0, 0.0)
    hot = current_sample(sim, 0.0)
    pd.DataFrame([hot]).to_csv(output_dir / "off_398K.csv", index=False)
    # tox는 저장 파일을 로드한 실제 geometry에서 읽는다.
    oxide_y = devsim.get_node_model_values(device=sim.name, region="oxide", name="y")
    tox_nm = (max(oxide_y) - min(oxide_y)) / 1e-7
    metrics = evaluate_specs(curves["idvg_low"], curves["idvg_high"], curves["idvg_body"],
                             hot["Id_A_per_um"], tox_nm)
    geometry = {r: {axis: [min(values), max(values)] for axis in ("x", "y")
                   for values in [devsim.get_node_model_values(device=sim.name, region=r, name=axis)]}
                for r in ("bulk", "oxide", "gate_metal")}
    result = {
        "purpose": "Initial Part 1 baseline, not an optimized design or student submission",
        "device": asdict(device), "structure_sha256": hashlib.sha256(structure.read_bytes()).hexdigest(),
        "geometry_cm": geometry, "gate_material_loaded": sim.dev.gate_material,
        "python": platform.python_version(), "devsim": devsim.get_parameter(name="info"),
        "command_arguments": sys.argv,
        "source_sha256": source_sha256, "source_snapshot_phase": "before_simulation",
        "precision": "extended" if extended_precision else "double",
        "solver": {"ramp_step_V": sim.RAMP_STEP_V, "relative_error": 1e-6,
                   "absolute_error": 1e30, "maximum_iterations": 80},
        "sweep": {"start_V": float(voltages[0]), "stop_V": float(voltages[-1]),
                  "step_V": float(voltages[1] - voltages[0]), "points": len(voltages)},
        "conditions": {"idvg_low": {"T_K": 300, "VD_V": 0.05, "VB_V": 0},
                       "idvg_high": {"T_K": 300, "VD_V": 2, "VB_V": 0},
                       "idvg_body": {"T_K": 300, "VD_V": 0.05, "VB_V": -0.5},
                       "off_398K": {"T_K": 398, "VD_V": 2, "VB_V": 0, "VG_V": 0}},
        "physics": {str(t): silicon_properties(t) for t in (300.0, 398.0)},
        "metrics": [m.to_dict() for m in metrics],
        "measurement_complete": all(m.status != "ERROR" for m in metrics),
        "all_specs_pass": all(m.status == "PASS" for m in metrics),
        "max_relative_current_balance": {k: float(v["relative_current_balance"].max())
                                          for k, v in curves.items()},
        "hot_relative_current_balance": hot["relative_current_balance"],
    }
    (output_dir / "metrics.json").write_text(json.dumps(result, ensure_ascii=False, indent=2,
                                                       allow_nan=False) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "part1_baseline.yaml")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--step-v", type=float, help="Override measurement resolution, not geometry")
    parser.add_argument("--double-precision", action="store_true", help="Numerical validation only")
    args = parser.parse_args()
    config_text = args.config.read_text(encoding="utf-8")
    data = yaml.safe_load(config_text)
    device = Device(**data["device"])
    sweep = data["part1"]
    step = args.step_v if args.step_v is not None else sweep["step_v"]
    voltages = voltage_points(sweep["start_v"], sweep["stop_v"], step)
    if len(voltages) < 2:
        raise ValueError("Need at least two sweep points")
    result = run_evaluation(device, voltages, args.output_dir,
                            sweep.get("extended_precision", True) and not args.double_precision)
    # 입력 조건도 실행 결과와 함께 보존한다.
    (args.output_dir / "config.yaml").write_text(config_text, encoding="utf-8")
    for metric in result["metrics"]:
        print(f"{metric['name']:12} {str(metric['value']):22} {metric['unit']:8} {metric['status']}")
    return 0 if result["measurement_complete"] else 1


if __name__ == "__main__":
    sys.exit(main())
