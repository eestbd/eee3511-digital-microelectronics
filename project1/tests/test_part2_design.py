from pathlib import Path
import sys
import unittest
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mosfet_tool.config import Device
from part2_design import BodyTap, ChannelDoping, ProfileCellSimulator, channel_acceptor_cm3


class ChannelProfileTests(unittest.TestCase):
    def test_distinct_zones_and_outside_source_drain_are_preserved(self):
        device = Device(source_length_um=0.2, gate_length_um=0.3,
                        drain_length_um=0.2, body_doping_cm3=7e16)
        profile = ChannelDoping(1e15, 9e16)
        x_um = np.array([0.1, 0.25, 0.4, 0.6])
        np.testing.assert_array_equal(channel_acceptor_cm3(x_um*1e-4, device, profile),
                                      [7e16, 1e15, 9e16, 7e16])

    def test_uniform_profile_keeps_baseline(self):
        device = Device(body_doping_cm3=7e16)
        x = np.linspace(0, 3e-4, 101)
        np.testing.assert_array_equal(channel_acceptor_cm3(x, device, ChannelDoping(7e16, 7e16)),
                                      np.full(101, 7e16))

    def test_split_fraction_is_geometric(self):
        device = Device(source_length_um=0.2, gate_length_um=0.3, body_doping_cm3=7e16)
        profile = ChannelDoping(2e15, 8e16, 0.25)
        np.testing.assert_array_equal(channel_acceptor_cm3(np.array([0.25, 0.3])*1e-4, device, profile),
                                      [2e15, 8e16])

    def test_serialized_midpoint_is_in_drain_side_zone(self):
        device = Device(source_length_um=0.2, gate_length_um=0.3, body_doping_cm3=7e16)
        profile = ChannelDoping(1e15, 7e16)
        np.testing.assert_array_equal(channel_acceptor_cm3([3.5e-5], device, profile), [7e16])

    def test_out_of_range_and_nonfinite_profiles_are_rejected(self):
        for values in ((1e13, 7e16, .5), (1e15, 2e17, .5),
                       (float("nan"), 7e16, .5), (1e15, 7e16, .01),
                       (1e15, 7e16, float("inf"))):
            with self.subTest(values=values), self.assertRaises(ValueError):
                ChannelDoping(*values)

    def test_tap_has_separate_positive_range_and_must_fit_silicon(self):
        self.assertEqual(BodyTap().additional_acceptor_cm3, 1e19)
        for values in ((float("nan"), .05), (1e19, 0), (1e19, float("inf"))):
            with self.subTest(values=values), self.assertRaises(ValueError):
                BodyTap(*values)
        with self.assertRaises(ValueError):
            ProfileCellSimulator(Device(silicon_thickness_um=.3), None,
                                 body_tap=BodyTap(thickness_um=.3))

    def test_asymmetric_donor_limits_are_independent(self):
        profile = ChannelDoping(7e16, 7e16, source_nd_cm3=1e21, drain_nd_cm3=1e19)
        self.assertEqual(profile.source_nd_cm3, 1e21)
        for value in (1e17, 2e21, float("nan")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                ChannelDoping(7e16, 7e16, source_nd_cm3=value)


if __name__ == "__main__":
    unittest.main()
