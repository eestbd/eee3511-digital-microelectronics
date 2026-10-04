# -*- coding: utf-8 -*-
"""공식 Part 2 cell: 구조·plate dQ/dV·READ·adaptive retention, 실패도 보존."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import traceback

import devsim
import yaml

from mosfet_tool.cell import (CBL_F, WIDTH_UM, Capacitor, CellSimulator,
                              read_transient, retention)
from mosfet_tool.config import Device
from mosfet_tool.physics import OFFICIAL_MODEL_ID, silicon_mobility, silicon_properties

ROOT = Path(__file__).resolve().parent


def evaluate(config: Path, output: Path, skip_retention: bool = False,
             structure_input: Path | None = None, retention_delta_v: float = 0.003) -> dict:
    if output.exists() and any(output.iterdir()):
        raise FileExistsError("Use a new empty output directory")
    config_text = config.read_text(encoding="utf-8")
    data = yaml.safe_load(config_text)
    device, capacitor = Device(**data["device"]), Capacitor(**data["capacitor"])
    sim = CellSimulator(device, capacitor)
    output.mkdir(parents=True, exist_ok=True)
    (output / "config.yaml").write_text(config_text, encoding="utf-8")
    hashes = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in [ROOT / "part2.py", ROOT / "check_structure_file.py",
                        *sorted((ROOT / "mosfet_tool").glob("*.py"))]}
    result = {"purpose": "Part 2 characterization; diagnostic structure until final review",
              "device": asdict(device), "capacitor": asdict(capacitor),
              "physics_model_id": OFFICIAL_MODEL_ID,
              "physics_398K": {**silicon_properties(398), **silicon_mobility(398)},
              "source_sha256": hashes, "source_snapshot_phase": "before_simulation",
              "conditions": {"T_K": 398, "VB_V": -0.5, "WL_high_V": 2.5,
                             "width_um": WIDTH_UM, "CBL_F": CBL_F,
                             "READ_dt_s": 10e-12, "READ_decision_s": 0.5e-9,
                             "READ_margin_requirement_V": 0.060,
                             "retention_BL_V": {"0": 2, "1": 0},
                             "retention_requirement_s": 0.064,
                             "retention_max_delta_V": retention_delta_v,
                             "retention_read_checkpoint_V": 0.03,
                             "retention_failure_time_relative_bracket": 0.01,
                             "ramp_step_V": sim.RAMP_STEP_V},
              "measurement_complete": False, "all_specs_pass": False,
              "retention_executed": not skip_retention}
    def checkpoint(stage):
        path = output / f"{stage}_checkpoint.json"
        if path.exists():
            raise FileExistsError(f"Preserve checkpoint: {path}")
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)+"\n",
                        encoding="utf-8")
    checkpoint("input")
    for name in ("extended_solver", "extended_model", "extended_equation"):
        devsim.set_parameter(name=name, value=True)
    try:
        structure = structure_input or output / "part2_diagnostic.devsim"
        if structure_input:
            sim.load_structure(structure_input)
        else:
            sim.build(structure)
        result["structure_sha256"] = hashlib.sha256(structure.read_bytes()).hexdigest()
        result["structure_file"] = str(structure)
        child = subprocess.run([sys.executable, "-B", str(ROOT / "check_structure_file.py"),
                                str(structure)], capture_output=True, text=True, encoding="utf-8")
        (output / "checker.log").write_text(child.stdout + child.stderr, encoding="utf-8")
        result["structure_check_passed"] = child.returncode == 0
        if child.returncode:
            raise RuntimeError("Fresh structure self-check failed")
        sim.solve_equilibrium()
        cstore, points = sim.extract_capacitance(0.01)
        fine_c, fine_points = sim.extract_capacitance(0.005)
        reference = capacitor.parallel_plate_f
        result["capacitance"] = {"CSTORE_F": cstore, "fine_delta_CSTORE_F": fine_c,
                                  "parallel_plate_reference_F": reference,
                                  "plate_bias_V": 1.0, "plate_points": points,
                                  "fine_plate_points": fine_points,
                                  "difference_from_reference_relative": abs(cstore-reference)/reference,
                                  "perturbation_checks_pass": abs(fine_c-cstore) <= cstore*1e-6,
                                  "reference_check_pass": abs(cstore-reference) <= reference*0.01,
                                  "passed": 0 < cstore <= 20e-15}
        result["fields"] = {"gate_MV_cm": 2.5/(device.oxide_thickness_nm*1e-7)/1e6,
                             "capacitor_MV_cm": 1/(capacitor.dielectric_nm*1e-7)/1e6}
        result["field_checks_pass"] = (result["fields"]["gate_MV_cm"] <= 5 and
                                       result["fields"]["capacitor_MV_cm"] <= 4)
        if not result["capacitance"]["passed"]:
            raise ValueError("CSTORE outside assignment range; preserve diagnostic, redesign")
        checkpoint("capacitance")
        sim.enable_transport()
        read_results, retention_results = {}, {}
        result["read"], result["retention"] = read_results, retention_results
        for bit, initial_v in (("0", 0.0), ("1", 2.0)):
            print(f"READ data {bit}", flush=True)
            frame, metrics = read_transient(sim.current_at, initial_v, cstore)
            frame.to_csv(output / f"read_{bit}.csv", index=False)
            # 5 ps is a numerical sensitivity check, never a replacement grading step.
            fine_frame, fine_metrics = read_transient(sim.current_at, initial_v, cstore, 5e-12)
            fine_frame.to_csv(output / f"read_{bit}_5ps.csv", index=False)
            metrics["fine_5ps_margin_V"] = fine_metrics["margin_V"]
            metrics["time_step_sensitivity_V"] = abs(metrics["margin_V"]-fine_metrics["margin_V"])
            metrics["step_validation_pass"] = metrics["time_step_sensitivity_V"] <= 0.002
            metrics["charge_validation_pass"] = metrics["max_charge_residual_C"] <= 1e-24
            read_results[bit] = metrics
            checkpoint(f"read_{bit}")
        result["read"] = read_results
        if not skip_retention:
            for bit, initial_v in (("0", 0.0), ("1", 2.0)):
                print(f"RETENTION data {bit}", flush=True)
                def degraded_margin(v):
                    _, metric = read_transient(sim.current_at, v, cstore)
                    print(f"degraded Vcell={v:.9g}, margin={metric['margin_V']:.9g}", flush=True)
                    return metric["margin_V"]
                frame, metrics = retention(sim.current_at, degraded_margin, initial_v, cstore,
                                            max_delta_v=retention_delta_v)
                frame.to_csv(output / f"retention_{bit}.csv", index=False)
                retention_results[bit] = metrics
                checkpoint(f"retention_{bit}")
            result["retention"] = retention_results
        result["measurement_complete"] = not skip_retention
        result["all_specs_pass"] = bool(not skip_retention and result["structure_check_passed"] and
            result["field_checks_pass"] and result["capacitance"]["passed"] and
            result["capacitance"]["reference_check_pass"] and result["capacitance"]["perturbation_checks_pass"] and
            all(r["passed"] and r["step_validation_pass"] and r["charge_validation_pass"]
                for r in read_results.values()) and all(r["passed"] for r in retention_results.values()))
    except Exception as error:
        result["error"] = {"type": type(error).__name__, "message": str(error),
                           "traceback": traceback.format_exc(),
                           "last_biases_V": {c: devsim.get_parameter(device=sim.name, name=f"{c}_bias")
                                             for c in sim.bias} if sim.name in devsim.get_device_list()
                                             else dict(sim.bias)}
        print(result["error"]["traceback"], flush=True)
    (output / "metrics.json").write_text(json.dumps(result, ensure_ascii=False, indent=2,
                                                     allow_nan=False)+"\n", encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "part2_initial.yaml")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--skip-retention", action="store_true", help="READ diagnostic only; not full PASS")
    parser.add_argument("--reload-structure", type=Path, help="Fresh remeasurement of an existing saved structure")
    parser.add_argument("--retention-delta-v", type=float, default=0.003,
                        help="Maximum voltage change per leakage step; halve for sensitivity check")
    args = parser.parse_args()
    result = evaluate(args.config, args.output_dir, args.skip_retention, args.reload_structure,
                      args.retention_delta_v)
    print(json.dumps({k: result.get(k) for k in ("measurement_complete", "all_specs_pass", "capacitance",
                                               "read", "retention", "error")}, ensure_ascii=False, indent=2))
    return 1 if "error" in result else 0


if __name__ == "__main__":
    raise SystemExit(main())
