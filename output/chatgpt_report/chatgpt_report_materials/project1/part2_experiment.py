"""Bounded Part 2 screening; uses the existing official physics and transients.

screen/retention1 are partial measurements. Final verification uses part2.py.
Every invocation writes to a new directory and preserves its raw evidence.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import time
import traceback

import devsim
import pandas as pd
import yaml

from mosfet_tool.cell import Capacitor, CellSimulator, WIDTH_UM, read_transient, retention
from mosfet_tool.config import Device
from mosfet_tool.physics import OFFICIAL_MODEL_ID, silicon_mobility, silicon_properties
from part2_design import BodyTap, ChannelDoping, ProfileCellSimulator

ROOT = Path(__file__).resolve().parent


def evaluate(config: Path, output: Path, stage: str,
             structure: Path | None = None, delta_v: float = 0.003) -> dict:
    if output.exists() and any(output.iterdir()):
        raise FileExistsError("Use a new empty output directory")
    data = yaml.safe_load(config.read_text(encoding="utf-8"))
    device, capacitor = Device(**data["device"]), Capacitor(**data["capacitor"])
    profile = ChannelDoping(**data["doping_profile"]) if "doping_profile" in data else None
    tap = BodyTap(**data["body_tap"]) if "body_tap" in data else None
    sim = ProfileCellSimulator(device, capacitor, profile, tap) if profile or tap else CellSimulator(device, capacitor)
    output.mkdir(parents=True, exist_ok=True)
    (output / "config.yaml").write_bytes(config.read_bytes())
    started = time.monotonic()
    result = {"stage": stage, "device": asdict(device), "capacitor": asdict(capacitor),
              "doping_profile": asdict(profile) if profile else None,
              "body_tap": asdict(tap) if tap else None,
              "measurement_complete": False, "all_specs_pass": False,
              "partial_characterization": True, "physics_model_id": OFFICIAL_MODEL_ID,
              "physics_398K": {**silicon_properties(398), **silicon_mobility(398)},
              "source_sha256": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in [Path(__file__), ROOT / "part2_design.py", ROOT / "part2.py", ROOT / "check_structure_file.py",
                                          *sorted((ROOT / "mosfet_tool").glob("*.py"))]},
              "read": {}, "retention": {}, "off_currents": [],
              "conditions": {"T_K": 398, "VB_V": -0.5, "WL_high_V": 2.5,
                             "width_um": WIDTH_UM, "CBL_F": 100e-15, "READ_dt_s": 1e-11,
                             "READ_decision_s": 0.5e-9, "retention_requirement_s": 0.064,
                             "retention_max_delta_V": delta_v, "ramp_step_V": 0.1}}

    def save():
        result["elapsed_s"] = time.monotonic() - started
        (output / "metrics.json").write_text(
            json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")

    for name in ("extended_solver", "extended_model", "extended_equation"):
        devsim.set_parameter(name=name, value=True)
    try:
        saved = structure or output / "part2_diagnostic.devsim"
        if structure:
            sim.load_structure(structure)
        else:
            sim.build(saved)
        result["structure_file"] = str(saved)
        result["structure_sha256"] = hashlib.sha256(saved.read_bytes()).hexdigest()
        child = subprocess.run([sys.executable, "-B", str(ROOT / "check_structure_file.py"),
                                str(saved)], capture_output=True, text=True, encoding="utf-8")
        (output / "checker.log").write_text(child.stdout + child.stderr, encoding="utf-8")
        result["structure_check_passed"] = child.returncode == 0
        if child.returncode:
            raise RuntimeError("Fresh structure checker rejected candidate")
        sim.solve_equilibrium()
        cstore, points = sim.extract_capacitance(0.01)
        fine, fine_points = sim.extract_capacitance(0.005)
        reference = capacitor.parallel_plate_f
        result["capacitance"] = {"CSTORE_F": cstore, "fine_delta_CSTORE_F": fine,
                                 "parallel_plate_reference_F": reference,
                                 "plate_points": points, "fine_plate_points": fine_points,
                                 "passed": 0 < cstore <= 20e-15,
                                 "perturbation_checks_pass": abs(cstore-fine) <= cstore*1e-6,
                                 "reference_check_pass": abs(cstore-reference) <= reference*0.01}
        result["fields"] = {"gate_MV_cm": 2.5/(device.oxide_thickness_nm*1e-7)/1e6,
                            "capacitor_MV_cm": 1/(capacitor.dielectric_nm*1e-7)/1e6}
        result["reliability_pass"] = (result["capacitance"]["passed"] and
                                     result["fields"]["gate_MV_cm"] <= 5 and
                                     result["fields"]["capacitor_MV_cm"] <= 4)
        save()
        if not result["reliability_pass"]:
            result["early_rejection"] = "Capacitance or field hard constraint"
            save()
            return result
        if not all(result["capacitance"][key] for key in
                   ("perturbation_checks_pass", "reference_check_pass")):
            raise RuntimeError("Capacitance numerical checks failed")
        sim.enable_transport()
        result["native_physics"] = {
            name: devsim.get_parameter(device=sim.name, region="bulk", name=name)
            for name in ("mu_n", "mu_p", "n_i", "n1", "p1")}
        if stage == "screen":
            for bit, initial in (("0", 0.0), ("1", 2.0)):
                frame, metric = read_transient(sim.current_at, initial, cstore)
                frame.to_csv(output / f"read_{bit}.csv", index=False)
                result["read"][bit] = metric
                save()
                print(f"READ {bit} margin={metric['margin_V']:.9g}", flush=True)
            if not all(metric["passed"] for metric in result["read"].values()):
                result["early_rejection"] = "Initial READ margin below 60 mV"
            else:
                for bit, cell_v, bl_v in (("1", 2.0, 0.0), ("1", 1.8, 0.0), ("0", 0.0, 2.0)):
                    currents = sim.current_at(0, cell_v, bl_v)
                    result["off_currents"].append({
                        "bit": bit, "Vcell_V": cell_v, "BL_V": bl_v,
                        "terminal_currents_A_per_um": currents,
                        "Istorage_A": currents["source"]*WIDTH_UM})
                    save()
        elif stage == "endpoint1":
            # A cheap endpoint screen, not a first-failure retention measurement.
            # The leakage Euler updates and 3 mV/8 ms bounds are unchanged.
            cell_v, elapsed = 2.0, 0.0
            rows = [{"time_s": 0.0, "Vcell_V": cell_v, "dt_s": 0.0, "Istorage_A": None}]
            for _ in range(10000):
                if elapsed >= 0.064:
                    break
                amperes = sim.current_at(0, cell_v, 0)["source"] * WIDTH_UM
                dt = min(0.008, 0.064-elapsed, delta_v*cstore/abs(amperes) if amperes else 0.008)
                if elapsed+dt == elapsed:
                    raise RuntimeError("Endpoint screen time step cannot advance")
                cell_v -= amperes*dt/cstore
                elapsed += dt
                if not math.isfinite(cell_v) or not -0.05 <= cell_v <= 2.05:
                    raise RuntimeError("Endpoint screen overshoot")
                rows.append({"time_s": elapsed, "Vcell_V": cell_v,
                             "dt_s": dt, "Istorage_A": amperes})
            else:
                raise RuntimeError("Endpoint screen step limit exceeded")
            pd.DataFrame(rows).to_csv(output / "endpoint_1.csv", index=False)
            frame, metric = read_transient(sim.current_at, cell_v, cstore)
            frame.to_csv(output / "read_1_at_64ms.csv", index=False)
            result["endpoint1"] = {"time_s": elapsed, "Vcell_V": cell_v,
                                    "read_margin_V": metric["margin_V"],
                                    "endpoint_pass": metric["passed"],
                                    "first_failure_time_measured": False}
        elif stage == "retention1":
            def margin(voltage):
                _, metric = read_transient(sim.current_at, voltage, cstore)
                print(f"READ after retention Vcell={voltage:.9g} margin={metric['margin_V']:.9g}",
                      flush=True)
                return metric["margin_V"]
            frame, metric = retention(sim.current_at, margin, 2.0, cstore, max_delta_v=delta_v)
            frame.to_csv(output / "retention_1.csv", index=False)
            result["retention"]["1"] = metric
        else:
            raise ValueError("Unknown experiment stage")
        result["measurement_complete"] = True
    except Exception as error:
        result["error"] = {"type": type(error).__name__, "message": str(error),
                           "traceback": traceback.format_exc()}
        print(result["error"]["traceback"], flush=True)
    save()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--stage", choices=("screen", "retention1", "endpoint1"), default="screen")
    parser.add_argument("--reload-structure", type=Path)
    parser.add_argument("--retention-delta-v", type=float, default=0.003)
    args = parser.parse_args()
    result = evaluate(args.config, args.output_dir, args.stage, args.reload_structure,
                      args.retention_delta_v)
    print(json.dumps({key: result.get(key) for key in
                     ("stage", "measurement_complete", "early_rejection", "read", "retention", "error")},
                     indent=2), flush=True)
    return 1 if "error" in result else 0


if __name__ == "__main__":
    raise SystemExit(main())
