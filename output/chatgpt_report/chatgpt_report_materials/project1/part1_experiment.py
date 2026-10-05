# -*- coding: utf-8 -*-
"""설계 하나를 기존 Part 1 CLI로 측정하고 탐색 예산·실패·입력을 보존한다."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import time

import yaml

from mosfet_tool.config import Device
from part1 import validate_device

ROOT = Path(__file__).resolve().parent
SEARCH_FIELDS = {"gate_length_um", "oxide_thickness_nm", "body_doping_cm3", "gate_material"}


def remaining_budget(start: datetime | None, now: datetime, count: int,
                     max_trials: int, seconds: float | None) -> float | None:
    """실패도 횟수에 포함하며, 선택에 쓴 wall-clock 시간도 예산에서 뺀다."""
    if max_trials <= 0 or (seconds is not None and (not math.isfinite(seconds) or seconds <= 0)):
        raise ValueError("Use a positive trial limit and positive finite time limit or None")
    if count >= max_trials:
        raise RuntimeError("Search trial limit reached")
    if seconds is None:
        return None  # 사용자 승인으로 시간 상한을 해제한 session; 횟수 상한은 유지한다.
    elapsed = (now - start).total_seconds() if start is not None else 0.0
    if elapsed < 0:
        raise RuntimeError("UTC clock moved backwards; inspect the search session")
    remaining = seconds - elapsed
    if remaining <= 0:
        raise RuntimeError("Search time limit reached")
    return remaining


def changed_fields(baseline: dict, candidate: dict, phase: str) -> dict:
    """무의식적인 physics/measurement 변경과 잘못된 단일 변수 실험을 막는다."""
    if candidate.get("part1") != baseline.get("part1"):
        raise ValueError("Keep measurement conditions fixed during design search")
    original, proposed = baseline["device"], candidate["device"]
    if set(original) != set(proposed):
        raise ValueError("Preserve the complete baseline device schema")
    changes = {key: {"baseline": original[key], "candidate": proposed[key]}
               for key in original if original[key] != proposed[key]}
    if not changes or set(changes) - SEARCH_FIELDS:
        raise ValueError("Only the documented design variables may change")
    if phase == "single" and len(changes) != 1:
        raise ValueError("A single-variable trial must change exactly one variable")
    validate_device(Device(**proposed))
    return changes


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
                    encoding="utf-8")


def run_trial(session: Path, config: Path, label: str, phase: str, reason: str) -> dict:
    if not label or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789_-" for c in label):
        raise ValueError("Use a lowercase filename-safe label")
    baseline_text = (ROOT / "part1_baseline.yaml").read_text(encoding="utf-8")
    input_text = config.read_text(encoding="utf-8")
    candidate = yaml.safe_load(input_text)
    changes = changed_fields(yaml.safe_load(baseline_text), candidate, phase)
    session_file = session / "session.json"
    limits = json.loads(session_file.read_text(encoding="utf-8"))
    if limits.get("search_closed"):
        raise RuntimeError("This search session is closed")
    prior = sorted(session.glob("trial_*/trial.json"))
    for record in prior:
        if json.loads(record.read_text(encoding="utf-8"))["device"] == candidate["device"]:
            raise ValueError("This configuration was already attempted; preserve its result")
    now = datetime.now(timezone.utc)
    start = (datetime.fromisoformat(limits["started_at_utc"])
             if limits.get("started_at_utc") else None)
    remaining_budget(start, now, len(prior), limits["max_trials"], limits["budget_seconds"])
    if start is None:
        start = now
        limits["started_at_utc"] = start.isoformat()
        write_json(session_file, limits)
    trial = session / f"trial_{len(prior)+1:02d}_{label}"
    trial.mkdir(exist_ok=False)
    (trial / "input.yaml").write_text(input_text, encoding="utf-8")
    command = [sys.executable, "-B", str(ROOT / "part1.py"), "--config",
               str((trial / "input.yaml").resolve()), "--output-dir", str((trial / "primary").resolve())]
    record = {"index": len(prior) + 1, "label": label, "phase": phase, "reason": reason,
              "status": "RUNNING", "started_at_utc": now.isoformat(),
              "device": candidate["device"], "changed_from_baseline": changes,
              "input_sha256": hashlib.sha256(input_text.encode("utf-8")).hexdigest(),
              "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "source_sha256": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in [ROOT / "part1.py", ROOT / "check_structure_file.py",
                                          *sorted((ROOT / "mosfet_tool").glob("*.py"))]},
              "command": command, "purpose": "Bounded design search; diagnostic structure only"}
    write_json(trial / "trial.json", record)
    timer = time.monotonic()
    with (trial / "solver.log").open("w", encoding="utf-8") as log:
        try:
            timeout = remaining_budget(start, datetime.now(timezone.utc), len(prior),
                                       limits["max_trials"], limits["budget_seconds"])
            record["timeout_seconds"] = timeout
            write_json(trial / "trial.json", record)
            budget_text = f"remaining {timeout:.1f} s" if timeout is not None else "count limit only"
            print(f"Starting trial {record['index']}/{limits['max_trials']}: {label}; "
                  f"{budget_text}", flush=True)
            child = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, timeout=timeout)
            record["returncode"] = child.returncode
            metrics_file = trial / "primary" / "metrics.json"
            if metrics_file.exists():
                result = json.loads(metrics_file.read_text(encoding="utf-8"))
                record.update(status="MEASURED" if child.returncode == 0 else "ERROR",
                              measurement_complete=result["measurement_complete"],
                              all_specs_pass=result["all_specs_pass"], metrics=result["metrics"])
            else:
                record.update(status="ERROR", error="Measurement failed; inspect solver.log and partial outputs")
        except subprocess.TimeoutExpired:
            # subprocess.run은 timeout 때 child를 종료하고 기다린다. 실패도 1회로 보존한다.
            record.update(status="TIMEOUT", error="Search wall-clock budget exhausted; child killed and waited")
        except RuntimeError as error:
            record.update(status="TIMEOUT", error=f"Budget expired during launch preparation: {error}")
    record["duration_seconds"] = time.monotonic() - timer
    record["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
    record["search_elapsed_seconds"] = (datetime.now(timezone.utc) - start).total_seconds()
    write_json(trial / "trial.json", record)
    print(f"Finished {label}: {record['status']} in {record['duration_seconds']:.2f} s", flush=True)
    for metric in record.get("metrics", []):
        print(f"{metric['name']:12} {str(metric['value']):22} {metric['unit']:8} {metric['status']}")
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--phase", choices=("single", "combination", "local"), required=True)
    parser.add_argument("--reason", required=True)
    args = parser.parse_args()
    record = run_trial(args.session, args.config, args.label, args.phase, args.reason)
    return 0 if record["status"] == "MEASURED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
