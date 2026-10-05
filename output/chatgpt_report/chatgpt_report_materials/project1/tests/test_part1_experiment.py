# -*- coding: utf-8 -*-
"""탐색 상한과 물리 설정 보호에 관한 독립 edge case 검증."""

from copy import deepcopy
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
import io
import json
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from part1_experiment import changed_fields, remaining_budget, run_trial


class SearchGuardTests(unittest.TestCase):
    def test_removed_time_limit_still_enforces_count(self):
        start = datetime(2026, 10, 4, tzinfo=timezone.utc)
        self.assertIsNone(remaining_budget(start, start + timedelta(days=2), 9, 10, None))
        with self.assertRaises(RuntimeError):
            remaining_budget(start, start + timedelta(days=2), 10, 10, None)

    def test_count_limit_includes_all_attempts(self):
        now = datetime(2026, 10, 4, tzinfo=timezone.utc)
        self.assertEqual(remaining_budget(None, now, 0, 10, 1800), 1800)
        self.assertEqual(remaining_budget(now, now, 9, 10, 1800), 1800)
        with self.assertRaises(RuntimeError):
            remaining_budget(now, now, 10, 10, 1800)

    def test_wall_clock_limit_and_backwards_clock(self):
        start = datetime(2026, 10, 4, tzinfo=timezone.utc)
        self.assertEqual(remaining_budget(start, start + timedelta(seconds=1799), 2, 10, 1800), 1)
        for delta in (-1, 1800, 2000):
            with self.subTest(delta=delta), self.assertRaises(RuntimeError):
                remaining_budget(start, start + timedelta(seconds=delta), 2, 10, 1800)

    def test_single_variable_and_protected_physics(self):
        baseline = yaml.safe_load((Path(__file__).parents[1] / "part1_baseline.yaml").read_text(encoding="utf-8"))
        candidate = deepcopy(baseline)
        candidate["device"]["gate_length_um"] = 0.5
        self.assertEqual(set(changed_fields(baseline, candidate, "single")), {"gate_length_um"})
        candidate["device"]["oxide_thickness_nm"] = 5
        with self.assertRaises(ValueError):
            changed_fields(baseline, candidate, "single")
        self.assertEqual(len(changed_fields(baseline, candidate, "combination")), 2)
        candidate["device"]["mu_n"] = 450
        with self.assertRaises(ValueError):
            changed_fields(baseline, candidate, "combination")

    def test_measurement_conditions_and_assignment_bounds(self):
        baseline = yaml.safe_load((Path(__file__).parents[1] / "part1_baseline.yaml").read_text(encoding="utf-8"))
        for key, value in (("gate_length_um", 0.2), ("oxide_thickness_nm", 3.9)):
            candidate = deepcopy(baseline)
            candidate["device"][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                changed_fields(baseline, candidate, "single")
        candidate = deepcopy(baseline)
        candidate["device"]["gate_material"] = "TaN"
        candidate["part1"]["step_v"] = 0.1
        with self.assertRaises(ValueError):
            changed_fields(baseline, candidate, "single")

    def test_timeout_preserves_inputs_and_consumes_last_slot(self):
        root = Path(__file__).parents[1]
        baseline = yaml.safe_load((root / "part1_baseline.yaml").read_text(encoding="utf-8"))
        temp_root = root / "tmp" / "search_guard_tests"
        temp_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temp_root) as folder:
            session = Path(folder)
            (session / "session.json").write_text(json.dumps({"max_trials": 1,
                "budget_seconds": 1800, "started_at_utc": None}), encoding="utf-8")
            baseline["device"]["gate_length_um"] = 0.5
            config = session / "config.yaml"
            config.write_text(yaml.safe_dump(baseline), encoding="utf-8")
            with patch("part1_experiment.subprocess.run",
                       side_effect=subprocess.TimeoutExpired("part1", 1)) as child, redirect_stdout(io.StringIO()):
                result = run_trial(session, config, "timeout", "single", "Test failed attempt accounting")
                self.assertEqual(result["status"], "TIMEOUT")
                self.assertEqual(len(list(session.glob("trial_*/trial.json"))), 1)
                self.assertEqual((session / "trial_01_timeout/input.yaml").read_bytes(), config.read_bytes())
                self.assertIn("part1.py", result["source_sha256"])
                baseline["device"]["gate_length_um"] = 0.7
                config.write_text(yaml.safe_dump(baseline), encoding="utf-8")
                with self.assertRaises(RuntimeError):
                    run_trial(session, config, "second", "single", "Must not launch")
                self.assertEqual(child.call_count, 1)


if __name__ == "__main__":
    unittest.main()
