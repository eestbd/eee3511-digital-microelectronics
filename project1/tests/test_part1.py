# -*- coding: utf-8 -*-
"""독립 기대 곡선·단위·실패 사례와 MOS flat-band로 Part 1을 검증한다."""

from pathlib import Path
import hashlib
import io
import json
import math
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import devsim
import numpy as np
import pandas as pd

from mosfet_tool.config import Device
from mosfet_tool.materials import canonical_gate_material
from mosfet_tool.metrics import MeasurementError, crossing_voltage, evaluate_specs
from mosfet_tool.physics import gate_offset_v, silicon_bandgap_ev, silicon_properties
from mosfet_tool.simulator import MosfetSimulator, voltage_points
from part1 import validate_device
import part1


def exponential_curve(threshold: float) -> pd.DataFrame:
    # 독립 기대값: 65 mV/dec이며 ID=1e-7의 VG는 threshold다.
    vg = np.unique(np.r_[0.0, np.arange(0.2, 0.8, 0.037), 2.0])
    current = np.minimum(500e-6, 1e-7 * 10**((vg - threshold) / 0.065))
    return pd.DataFrame({"Vg_V": vg, "Id_A_per_um": current})


class MeasurementTests(unittest.TestCase):
    def test_eight_independent_expected_metrics(self):
        low, high, body = [exponential_curve(v) for v in (0.45, 0.43, 0.51)]
        high.loc[0, "Id_A_per_um"] = 0.5e-12
        rows = {r.name: r for r in evaluate_specs(low, high, body, 50e-12, 4.0)}
        expected = {"Vth": 0.45, "Ion": 500, "Ioff": 0.5, "SS": 65,
                    "Ioff_398K": 50, "DIBL": 20 / 1.95,
                    "Body_effect": 0.06, "Eox": 5}
        for name, value in expected.items():
            with self.subTest(name=name):
                self.assertAlmostEqual(rows[name].value, value, places=10)
                self.assertEqual(rows[name].status, "PASS")

    def test_incomplete_data_does_not_hide_other_results(self):
        results = {r.name: r for r in evaluate_specs(None, None, None, None, 10)}
        self.assertEqual(results["Vth"].status, "ERROR")
        self.assertIsNone(results["Vth"].value)
        self.assertEqual(results["Ion"].status, "ERROR")
        self.assertEqual(results["Ioff_398K"].status, "ERROR")
        self.assertEqual(results["Eox"].value, 2)

    def test_failing_design_is_not_a_measurement_error(self):
        curve = exponential_curve(0.60)
        results = {r.name: r for r in evaluate_specs(curve, curve, curve, 101e-12, 4)}
        self.assertEqual(results["Vth"].status, "FAIL")
        self.assertEqual(results["Ioff_398K"].status, "FAIL")

    def test_exact_crossing_and_no_extrapolation(self):
        frame = pd.DataFrame({"Vg_V": [0, 0.4, 0.8], "Id_A_per_um": [1e-10, 1e-7, 1e-4]})
        self.assertEqual(crossing_voltage(frame, 1e-7), 0.4)
        self.assertEqual(crossing_voltage(frame, 1e-10), 0.0)
        self.assertEqual(crossing_voltage(frame, 1e-4), 0.8)
        with self.assertRaises(MeasurementError):
            crossing_voltage(frame, 1e-12)

    def test_ambiguous_crossings_and_bad_samples(self):
        cases = [([0, 0.5, 1], [1e-8, 1e-6, 1e-8]),
                 ([0, 0.5, 1], [1e-8, 1e-7, 1e-7]),
                 ([0, 0.5, 1], [1e-6, 1e-7, 1e-8]),
                 ([0, 0.5, 1], [1e-8, 1e-7, 1e-8]),
                 ([0, 1], [1e-7, 1e-8]),
                 ([0, 0, 1], [1e-8, 1e-7, 1e-6]),
                 ([0, 0.5, 1], [1e-8, np.nan, 1e-6]),
                 ([0, 1], [-1e-8, 1e-6])]
        for vg, current in cases:
            with self.subTest(vg=vg, current=current), self.assertRaises(MeasurementError):
                crossing_voltage(pd.DataFrame({"Vg_V": vg, "Id_A_per_um": current}), 1e-7)

    def test_negative_off_current_is_not_clamped(self):
        high = exponential_curve(0.45)
        high.loc[0, "Id_A_per_um"] = -1e-15
        results = {r.name: r for r in evaluate_specs(high, high, high, -1e-15, 10)}
        self.assertEqual(results["Ioff"].status, "ERROR")
        self.assertEqual(results["Ioff_398K"].status, "ERROR")

    def test_bad_step_and_actual_ion_endpoint(self):
        for step in (0, -0.1, float("nan"), float("inf")):
            with self.subTest(step=step), self.assertRaises(ValueError):
                voltage_points(0, 2, step)
        high = exponential_curve(0.45).iloc[:-1]
        rows = {r.name: r for r in evaluate_specs(high, high, high, 1e-12, 10)}
        self.assertEqual(rows["Ion"].status, "ERROR")


class PhysicsTests(unittest.TestCase):
    def test_reference_and_temperature_dependence(self):
        self.assertEqual(silicon_properties(300)["n_i_cm3"], 1e10)
        self.assertAlmostEqual(silicon_bandgap_ev(300), 1.12452, places=5)
        self.assertAlmostEqual(silicon_bandgap_ev(398), 1.09754, places=5)
        # 문헌 계수로 모델을 검산하며 실제 측정 재료값을 뜻하지 않는다.
        self.assertTrue(4.7e12 < silicon_properties(398)["n_i_cm3"] < 4.8e12)
        self.assertEqual(silicon_properties(398, "legacy")["n_i_cm3"], 1e10)
        for t in (0, -1, float("inf"), float("nan")):
            with self.subTest(t=t), self.assertRaises(ValueError):
                silicon_properties(t)

    def test_gate_material_shift_and_aliases(self):
        self.assertAlmostEqual(gate_offset_v("Mo", 300, "varshni") -
                               gate_offset_v("W", 300, "varshni"), 0.1)
        self.assertEqual(canonical_gate_material("n+ poly-Si"), "n+poly")
        for bad in ("4.6", 4.6, "gold"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                canonical_gate_material(bad)

    def test_part1_constraints(self):
        validate_device(Device(gate_material="W", silicon_temperature_model="varshni"))
        for change in ({"gate_length_um": 0.29}, {"oxide_thickness_nm": 3.9},
                       {"body_doping_cm3": float("nan")}, {"mu_n": 900}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                validate_device(Device(gate_material="W", silicon_temperature_model="varshni", **change))
        with self.assertRaises(ValueError):
            Device(doping_decay_x_nm=float("nan"))


class ProvenanceTests(unittest.TestCase):
    def test_cli_keeps_starting_inputs_when_disk_changes_during_calculation(self):
        scratch = Path(__file__).resolve().parents[1] / "tmp" / "tests"
        scratch.mkdir(parents=True, exist_ok=True)
        original_config = (part1.ROOT / "part1_baseline.yaml").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory(dir=scratch) as folder:
            root = Path(folder)
            (root / "mosfet_tool").mkdir()
            config = root / "input.yaml"
            config.write_text(original_config, encoding="utf-8")
            source = root / "part1.py"
            source.write_text("starting source\n", encoding="utf-8")
            (root / "check_structure_file.py").write_text("checker fixture\n", encoding="utf-8")
            starting_hash = hashlib.sha256(source.read_bytes()).hexdigest()
            output = root / "output"

            class FakeSimulator:
                RAMP_STEP_V = 0.1

                def __init__(self, device, name="fixture"):
                    self.dev, self.name = device, name

                def build(self, path):
                    path.write_text("structure fixture\n", encoding="utf-8")
                    # A user edits disk inputs after the CLI has started its calculation.
                    source.write_text("later source\n", encoding="utf-8")
                    config.write_text("later configuration\n", encoding="utf-8")

            def sample(sim, vg):
                current = 1e-15 if vg == 0 else 500e-6
                return {"Vg_V": vg, "Id_A_per_um": current, "Is_A_per_um": -current,
                        "Ib_A_per_um": 0, "current_balance_A_per_um": 0,
                        "relative_current_balance": 0}

            def coordinates(*, region, name, **kwargs):
                return [-1e-6, 0] if region == "oxide" and name == "y" else [0, 1e-4]

            with patch.object(part1, "ROOT", root), \
                 patch.object(part1, "MosfetSimulator", FakeSimulator), \
                 patch.object(part1, "prepared_simulator", side_effect=lambda d, *args: FakeSimulator(d)), \
                 patch.object(part1, "current_sample", side_effect=sample), \
                 patch.object(part1.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "OK", "")), \
                 patch.object(devsim, "set_parameter"), \
                 patch.object(devsim, "get_parameter", return_value={"version": "fixture"}), \
                 patch.object(devsim, "get_node_model_values", side_effect=coordinates), \
                 patch.object(sys, "stdout", new=io.StringIO()), \
                 patch.object(sys, "argv", ["part1.py", "--config", str(config),
                                            "--step-v", "2", "--output-dir", str(output)]):
                self.assertEqual(part1.main(), 0)
            result = json.loads((output / "metrics.json").read_text(encoding="utf-8"))
            self.assertEqual(result["source_sha256"]["part1.py"], starting_hash)
            self.assertEqual(result["source_snapshot_phase"], "before_simulation")
            self.assertEqual((output / "config.yaml").read_text(encoding="utf-8"), original_config)
            self.assertNotEqual(config.read_text(encoding="utf-8"), original_config)


class NativePhysicsTests(unittest.TestCase):
    def tearDown(self):
        MosfetSimulator(Device())._clear_session()

    def test_uniform_mos_flatband_at_both_temperatures(self):
        class UniformMOS(MosfetSimulator):
            def _build_doping(self):
                devsim.node_model(device=self.name, region="bulk", name="NetDoping", equation="-1e16")
        for t in (300.0, 398.0):
            with self.subTest(T=t):
                sim = UniformMOS(Device(gate_material="W", temperature_k=t,
                                        silicon_temperature_model="varshni"))
                sim.build()
                props = silicon_properties(t)
                ni = props["n_i_cm3"]
                for parameter in ("n_i", "n1", "p1"):
                    self.assertEqual(devsim.get_parameter(device=sim.name, region="bulk", name=parameter), ni)
                # Charge-neutral p-type semiconductor: p−n=NA, pn=ni².
                holes = 0.5 * (1e16 + math.hypot(1e16, 2 * ni))
                psi_bulk = -props["V_t_V"] * math.log(holes / ni)
                sim.solve_equilibrium()
                sim.set_bias("gate", psi_bulk + gate_offset_v("W", t, "varshni"))
                for region in ("bulk", "oxide"):
                    values = devsim.get_node_model_values(device=sim.name, region=region, name="Potential")
                    self.assertLess(max(abs(v - psi_bulk) for v in values), 1e-8)

    def test_work_function_compensated_voltage_keeps_equilibrium(self):
        potentials = []
        for material, gate_v in (("W", 0.3), ("Mo", 0.4)):
            sim = MosfetSimulator(Device(gate_material=material, silicon_temperature_model="varshni"))
            sim.build()
            sim.solve_equilibrium()
            sim.set_bias("gate", gate_v)
            potentials.append(devsim.get_node_model_values(device=sim.name, region="bulk", name="Potential"))
        np.testing.assert_allclose(potentials[0], potentials[1], rtol=0, atol=1e-8)

    def test_structure_export_and_material_reload(self):
        scratch = Path(__file__).resolve().parents[1] / "tmp" / "tests"
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as folder:
            path = Path(folder) / "diagnostic.devsim"
            # DEVSIM 2.10 Windows loader keeps the file open until process exit.
            # Run the native fixture in a child so TemporaryDirectory can clean up.
            code = """
from pathlib import Path
import sys
sys.path.insert(0, sys.argv[1])
import devsim
from mosfet_tool.config import Device
from mosfet_tool.simulator import MosfetSimulator
path = Path(sys.argv[2])
sim = MosfetSimulator(Device(gate_material="W", silicon_temperature_model="varshni"))
sim.build(path)
sim._clear_session()
devsim.load_devices(file=str(path))
assert len(devsim.get_device_list()) == 1
for region in devsim.get_region_list(device=sim.name):
    assert not devsim.get_equation_list(device=sim.name, region=region)
    assert "Potential" not in devsim.get_node_model_list(device=sim.name, region=region)
assert not devsim.get_parameter_list(device=sim.name)
sim.load_structure(path)
assert sim.dev.gate_material == "W"
assert not devsim.get_equation_list(device=sim.name, region="gate_metal")
try:
    sim.build(path)
except FileExistsError:
    pass
else:
    raise AssertionError("Existing structure was not protected")
"""
            result = subprocess.run([sys.executable, "-B", "-c", code,
                                     str(scratch.parents[1]), str(path)],
                                    capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stdout[-3000:] + result.stderr)


if __name__ == "__main__":
    unittest.main()
