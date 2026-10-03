# -*- coding: utf-8 -*-
"""초기 Part 1 결과의 간격·정밀도·재로딩·전류 보존을 검증한다. 설계 탐색 없음."""

from __future__ import annotations

import argparse
from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import devsim
import numpy as np
import pandas as pd
import yaml

from mosfet_tool.config import Device
from mosfet_tool.metrics import evaluate_specs
from mosfet_tool.simulator import MosfetSimulator
from part1 import current_sample, prepared_simulator


ABS_CURRENT_TOL = 1e-17  # A/um, spec Ioff 상한의 1e-5
REL_CURRENT_TOL = 1e-6


def close_current(a: float, b: float) -> bool:
    return abs(a - b) <= max(ABS_CURRENT_TOL, REL_CURRENT_TOL * max(abs(a), abs(b)))


def probe(device: dict, structure: str, temperature: float, vd: float, vb: float,
          vg: float, extended: bool, loaded: bool) -> dict:
    """독립 프로세스에서 하나의 정밀도만 사용해 측정한다."""
    device = Device(**device)
    for parameter in ("extended_solver", "extended_model", "extended_equation"):
        devsim.set_parameter(name=parameter, value=extended)
    try:
        if loaded:
            sim = prepared_simulator(device, Path(structure), temperature, vd, vb)
        else:
            sim = MosfetSimulator(replace(device, temperature_k=temperature))
            sim.build()
            sim.solve_equilibrium()
            sim.enable_transport()
            if vb:
                sim.set_bias("body", vb)
            sim.set_bias("drain", vd)
        return {"status": "OK", **current_sample(sim, vg)}
    except (devsim.error, RuntimeError) as error:
        devices = devsim.get_device_list()
        biases = ({c: devsim.get_parameter(device=devices[0], name=f"{c}_bias")
                   for c in ("gate", "source", "drain", "body")} if devices else {})
        return {"status": "ERROR", "error": str(error), "failed_biases_V": biases}


def validate(primary: Path, fine: Path, probe_log_dir: Path) -> dict:
    coarse_result = json.loads((primary / "metrics.json").read_text(encoding="utf-8"))
    fine_result = json.loads((fine / "metrics.json").read_text(encoding="utf-8"))
    if coarse_result["device"] != fine_result["device"]:
        raise ValueError("Compare measurement resolution for the same device only")
    if coarse_result["structure_sha256"] != fine_result["structure_sha256"]:
        raise ValueError("Resolution comparison requires identical saved structure")
    if coarse_result["precision"] != "extended" or fine_result["precision"] != "extended":
        raise ValueError("The resolution comparison uses extended precision")
    if not (coarse_result["measurement_complete"] and fine_result["measurement_complete"]):
        raise ValueError("Incomplete measurements; resolve ERROR before stability validation")
    if fine_result["sweep"]["step_V"] >= coarse_result["sweep"]["step_V"]:
        raise ValueError("Fine run must have a smaller voltage step")
    metric_tolerances = {"Vth": 0.001, "SS": 0.2, "DIBL": 0.5, "Body_effect": 0.001}
    fine_metrics = {m["name"]: m for m in fine_result["metrics"]}
    resolution = []
    for metric in coarse_result["metrics"]:
        other = fine_metrics[metric["name"]]
        delta = abs(metric["value"] - other["value"])
        # Endpoint currents/geometry should agree; threshold metrics allow interpolation error.
        tolerance = metric_tolerances.get(metric["name"],
                                          max(1e-8, abs(metric["value"]) * REL_CURRENT_TOL))
        resolution.append({"name": metric["name"], "coarse": metric["value"],
                           "fine": other["value"], "unit": metric["unit"],
                           "difference": delta, "tolerance": tolerance,
                           "passed": delta <= tolerance and metric["status"] == other["status"]})
    curves = {name: pd.read_csv(primary / f"{name}.csv")
              for name in ("idvg_low", "idvg_high", "idvg_body", "off_398K")}
    common_points = {}
    for name, frame in curves.items():
        comparison = pd.read_csv(fine / f"{name}.csv")
        merged = frame.merge(comparison, on="Vg_V", suffixes=("_coarse", "_fine"))
        passed = len(merged) == len(frame) and all(
            close_current(a, b) for a, b in zip(merged.Id_A_per_um_coarse, merged.Id_A_per_um_fine))
        common_points[name] = {"points_compared": len(merged), "passed": passed,
                               "max_absolute_difference_A_per_um": float(np.max(np.abs(
                                   merged.Id_A_per_um_coarse - merged.Id_A_per_um_fine)))}
    conservation = {}
    reextraction = {}
    for label, folder in (("primary", primary), ("fine", fine)):
        saved = coarse_result if label == "primary" else fine_result
        frames = {name: pd.read_csv(folder / f"{name}.csv") for name in curves}
        oxide_y = saved["geometry_cm"]["oxide"]["y"]
        measured = evaluate_specs(frames["idvg_low"], frames["idvg_high"], frames["idvg_body"],
                                 float(frames["off_398K"].Id_A_per_um.iloc[0]),
                                 (oxide_y[1] - oxide_y[0]) / 1e-7)
        reextraction[label] = {"passed": all(a.status == b["status"] and a.value is not None and
                                            np.isclose(a.value, b["value"], rtol=1e-12, atol=1e-12)
                                            for a, b in zip(measured, saved["metrics"])),
                               "metrics": [m.to_dict() for m in measured]}
        for name in curves:
            frame = frames[name]
            scale = frame[["Id_A_per_um", "Is_A_per_um", "Ib_A_per_um"]].abs().max(axis=1)
            passed = bool((frame.current_balance_A_per_um.abs() <=
                           np.maximum(ABS_CURRENT_TOL, scale * REL_CURRENT_TOL)).all())
            conservation[f"{label}/{name}"] = {
                "passed": passed, "max_relative_residual": float(frame.relative_current_balance.max()),
                "max_absolute_residual_A_per_um": float(frame.current_balance_A_per_um.abs().max())}
    data = yaml.safe_load((primary / "config.yaml").read_text(encoding="utf-8"))
    device = Device(**data["device"])
    structure = primary / "part1_baseline_diagnostic.devsim"
    threshold = next(m["value"] for m in coarse_result["metrics"] if m["name"] == "Vth")
    # 원래 곡선의 문턱 부근과 off/on 점을 새 초기화 경로로 다시 계산한다.
    threshold_vg = float(curves["idvg_low"].iloc[
        (curves["idvg_low"].Vg_V - threshold).abs().argmin()].Vg_V)
    cases = (("idvg_low", 300.0, 0.05, 0.0, threshold_vg),
             ("idvg_high", 300.0, 2.0, 0.0, 0.0),
             ("idvg_high", 300.0, 2.0, 0.0, 2.0),
             ("idvg_body", 300.0, 0.05, -0.5, threshold_vg),
             ("off_398K", 398.0, 2.0, 0.0, 0.0))
    replays = []
    probe_log_dir.mkdir(parents=True, exist_ok=True)
    child_code = """
import sys,json
sys.path.insert(0,sys.argv[1])
from validate_part1 import probe
result=probe(**json.load(sys.stdin))
print("PROBE_RESULT="+json.dumps(result,allow_nan=False))
"""
    for name, temperature, vd, vb, vg in cases:
        reference = float(curves[name].loc[np.isclose(curves[name].Vg_V, vg), "Id_A_per_um"].iloc[0])
        records = {}
        for label, extended, loaded in (("reload_extended", True, True),
                                       ("reload_double", False, True),
                                       ("live_extended", True, False)):
            log = probe_log_dir / f"{len(replays)}_{name}_{label}.log"
            if log.exists():
                raise FileExistsError(f"Preserve prior probe log: {log}")
            print(f"Probe {name} T={temperature} VG={vg} {label}", flush=True)
            data = {"device": asdict(device), "structure": str(structure.resolve()),
                    "temperature": temperature, "vd": vd, "vb": vb, "vg": vg,
                    "extended": extended, "loaded": loaded}
            child = subprocess.run([sys.executable, "-B", "-c", child_code,
                                    str(Path(__file__).resolve().parent)],
                                   input=json.dumps(data), capture_output=True,
                                   text=True, encoding="utf-8")
            log.write_text(child.stdout + child.stderr, encoding="utf-8")
            outputs = [s.removeprefix("PROBE_RESULT=") for s in child.stdout.splitlines()
                       if s.startswith("PROBE_RESULT=")]
            sample = (json.loads(outputs[-1]) if child.returncode == 0 and outputs else
                      {"status": "ERROR", "error": child.stderr[-2000:] or "Missing probe result"})
            if sample["status"] == "OK":
                scale = max(abs(sample[c]) for c in ("Id_A_per_um", "Is_A_per_um", "Ib_A_per_um"))
                records[label] = {**sample,
                                  "difference_from_sweep_A_per_um": sample["Id_A_per_um"] - reference,
                                  "current_matches": close_current(sample["Id_A_per_um"], reference),
                                  "conservation_passed": abs(sample["current_balance_A_per_um"]) <=
                                                         max(ABS_CURRENT_TOL, scale * REL_CURRENT_TOL)}
                records[label]["passed"] = records[label]["current_matches"] and records[label]["conservation_passed"]
            else:
                records[label] = {**sample, "passed": False}
        replays.append({"case": name, "T_K": temperature, "VD_V": vd, "VB_V": vb,
                        "VG_V": vg, "reference_Id_A_per_um": reference, "replays": records})
    extended_pass = (all(x["passed"] for x in resolution) and
                     all(x["passed"] for x in common_points.values()) and
                     all(x["passed"] for x in conservation.values()) and
                     all(x["passed"] for x in reextraction.values()) and
                     all(r["replays"][label]["passed"] for r in replays
                         for label in ("reload_extended", "live_extended")))
    double_complete = all(r["replays"]["reload_double"]["status"] == "OK" for r in replays)
    double_pass = all(r["replays"]["reload_double"]["passed"] for r in replays)
    return {"purpose": "Same-device numerical validation; no design-variable search",
            "primary": str(primary), "fine": str(fine),
            "current_tolerances": {"absolute_A_per_um": ABS_CURRENT_TOL, "relative": REL_CURRENT_TOL},
            "resolution": resolution, "common_points": common_points,
            "current_conservation": conservation, "critical_point_replays": replays,
            "final_extractor_recheck": reextraction,
            "final_extractor_sha256": hashlib.sha256(
                (Path(__file__).parent / "mosfet_tool" / "metrics.py").read_bytes()).hexdigest(),
            "validation_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "probe_isolation": "Fresh Python process for each precision and point",
            "probe_log_dir": str(probe_log_dir), "extended_baseline_checks_pass": extended_pass,
            "double_precision_complete": double_complete, "double_precision_checks_pass": double_pass,
            "all_checks_pass": extended_pass and double_complete and double_pass}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primary", type=Path, required=True)
    parser.add_argument("--fine", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--probe-log-dir", type=Path, required=True,
                        help="New directory for native solver logs; project1/tmp is recommended")
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("Preserve prior validation; choose a new output path")
    result = validate(args.primary, args.fine, args.probe_log_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(f"All numerical checks pass: {result['all_checks_pass']}")
    return 0 if result["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
