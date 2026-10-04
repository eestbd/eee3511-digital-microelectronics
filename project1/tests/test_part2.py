# -*- coding: utf-8 -*-
"""공식 READ/retention의 독립 charge·시간 기대값 및 실제 capacitor extraction."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mosfet_tool.cell import Capacitor, CellSimulator, read_transient, retention, validate_currents


class CellIntegrationTests(unittest.TestCase):
    def test_joint_ramp_updates_all_biases_and_skips_identical_state(self):
        sim = CellSimulator.__new__(CellSimulator)
        sim.name = "fixture"
        sim.bias = {"gate": 0, "source": 0, "drain": 0, "body": 0}
        sim._solve = Mock()
        sim.contact_currents = lambda: {"drain": 1e-6, "source": -1e-6, "body": 0}
        with patch("mosfet_tool.cell.devsim.set_parameter") as setting:
            sim.current_at(2.5, 0, 1)
            self.assertEqual(sim._solve.call_count, 25)
            self.assertEqual(setting.call_count, 100)
            self.assertEqual(sim.bias, {"gate": 2.5, "source": 0, "drain": 1, "body": -0.5})
            sim._solve.reset_mock()
            sim.current_at(2.5, 0, 1)
            self.assertEqual(sim._solve.call_count, 0)
            sim.current_at(2.5, 0.005, 0.999)
            self.assertEqual(sim._solve.call_count, 1)

    def test_width_sign_time_and_charge(self):
        calls = []
        def current(wl, cell, bl):
            calls.append((wl, cell, bl))
            return {"drain": 1e-6, "source": -1e-6, "body": 0.0}
        frame, result = read_transient(current, 0.0, 10e-15)
        self.assertEqual(len(calls), 50)
        self.assertEqual(len(frame), 51)
        self.assertAlmostEqual(frame.Vcell_V.iloc[-1], 0.005, places=12)
        self.assertAlmostEqual(frame.VBL_V.iloc[-1], 0.9995, places=12)
        self.assertAlmostEqual(result["decision_time_s"], 0.5e-9, places=20)
        self.assertLess(result["max_charge_residual_C"], 1e-26)

    def test_reverse_current_and_body_charge(self):
        frame, result = read_transient(lambda *args: {"drain": -1e-6, "source": 0.9e-6,
                                                     "body": 0.1e-6}, 2.0, 10e-15)
        self.assertAlmostEqual(frame.VBL_V.iloc[-1], 1.0005, places=12)
        self.assertAlmostEqual(frame.Vcell_V.iloc[-1], 1.9955, places=12)
        self.assertLess(result["max_charge_residual_C"], 1e-26)

    def test_bad_inputs_and_conservation_are_not_clamped(self):
        for args in ((0, 21e-15, 10e-12), (0, 10e-15, 0),
                     (0, 10e-15, 13e-12), (float("nan"), 10e-15, 10e-12)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                read_transient(lambda *args: {}, *args)
        for currents in ({"drain": 1e-6, "source": 0, "body": 0},
                         {"drain": float("nan"), "source": 0, "body": 0}):
            with self.subTest(currents=currents), self.assertRaises(RuntimeError):
                validate_currents(currents)

    def test_retention_uses_degraded_read_and_brackets_first_failure(self):
        current = lambda *args: {"drain": 1e-12, "source": -1e-12, "body": 0.0}
        frame, result = retention(current, lambda v: 0.08-0.1*v, 0.0, 10e-15)
        # Istorage=-0.1 pA, C=10 fF -> +10 V/s. READ fails at Vcell>0.2 V -> 20 ms.
        lower, upper = result["failure_bracket_s"]
        self.assertLessEqual(lower, 0.020+1e-12)
        self.assertGreaterEqual(upper, 0.020-1e-12)
        self.assertLessEqual(upper-lower, 0.000300000001)
        self.assertFalse(result["passed"])
        self.assertLessEqual(frame.Vcell_V.diff().dropna().abs().max(), 0.003000000001)

    def test_retention_initial_read_failure_and_lower_bound(self):
        def forbidden(*args):
            raise AssertionError("Initial read failure must stop before integration")
        _, result = retention(forbidden, lambda v: 0.059, 2.0, 10e-15)
        self.assertEqual(result["failure_bracket_s"], [0, 0])
        self.assertFalse(result["passed"])
        frame, result = retention(lambda *args: {"drain": 0, "source": 0, "body": 0},
                                  lambda v: 0.060, 0.0, 10e-15)
        self.assertTrue(result["passed"])
        self.assertIsNone(result["failure_bracket_s"])
        self.assertEqual(result["retention_lower_bound_s"], 0.064)

    def test_capacitor_ranges_and_independent_geometric_value(self):
        self.assertAlmostEqual(Capacitor().parallel_plate_f/1e-15, 18.585, places=9)
        for change in ({"material": "35"}, {"height_um": 0.1},
                       {"dielectric_nm": 2}, {"height_um": float("nan")}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                Capacitor(**change)


class NativeCapacitorTests(unittest.TestCase):
    def test_native_structure_charge_derivative_and_fresh_reload(self):
        root = Path(__file__).resolve().parents[1]
        scratch = root / "tmp" / "tests"
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as folder:
            code = '''
import sys
from pathlib import Path
sys.path.insert(0,sys.argv[1])
import devsim,yaml
from mosfet_tool.config import Device
from mosfet_tool.cell import CellSimulator,Capacitor
from check_structure_file import validate
data=yaml.safe_load((Path(sys.argv[1])/'part2_initial.yaml').read_text(encoding='utf-8'))
for name in ('extended_solver','extended_model','extended_equation'):
 devsim.set_parameter(name=name,value=True)
cap=Capacitor(**data['capacitor'])
sim=CellSimulator(Device(**data['device']),cap)
path=Path(sys.argv[2])/'cell.devsim'
sim.build(path)
sim._clear_session()
devsim.load_devices(file=str(path))
assert not validate(devsim.get_device_list()[0])
sim.load_structure(path)
sim.solve_equilibrium()
c,points=sim.extract_capacitance()
assert abs(c-cap.parallel_plate_f)/cap.parallel_plate_f<0.01,(c,cap.parallel_plate_f)
assert points[2]['plate_charge_C']>points[0]['plate_charge_C']
sim.enable_transport()
for contact,value in (('body',-0.5),('gate',2.5),('drain',1.1),('source',1.8)):
 sim.set_bias(contact,value)
sequential=sim.contact_currents()
other=CellSimulator(Device(**data['device']),cap)
other.load_structure(path)
other.solve_equilibrium()
other.enable_transport()
joint=other.current_at(2.5,1.8,1.1)
for contact in sequential:
 assert abs(joint[contact]-sequential[contact])<=max(1e-17,1e-6*max(abs(joint[contact]),abs(sequential[contact]))),(contact,joint,sequential)
print('CAP_NATIVE_OK',c)
'''
            result = subprocess.run([sys.executable, "-B", "-c", code, str(root), folder],
                                    capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stdout[-3000:]+result.stderr)
            self.assertIn("CAP_NATIVE_OK", result.stdout)


if __name__ == "__main__":
    unittest.main()
