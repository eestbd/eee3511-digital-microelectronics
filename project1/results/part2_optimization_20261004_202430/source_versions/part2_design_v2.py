"""Optional Part 2 channel doping; the evaluator only needs saved NetDoping."""
from dataclasses import dataclass
import math

import devsim
import numpy as np

from mosfet_tool.cell import CellSimulator
from mosfet_tool.simulator import UM


@dataclass(frozen=True)
class ChannelDoping:
    source_side_na_cm3: float
    drain_side_na_cm3: float
    split_fraction: float = 0.5

    def __post_init__(self):
        for value in (self.source_side_na_cm3, self.drain_side_na_cm3):
            if not math.isfinite(value) or not 1e14 <= value <= 1e17:
                raise ValueError("Local body doping must be 1e14..1e17 cm^-3")
        if not math.isfinite(self.split_fraction) or not 0.1 <= self.split_fraction <= 0.9:
            raise ValueError("Channel split fraction must be 0.1..0.9")


def channel_acceptor_cm3(x_cm, device, profile: ChannelDoping):
    """Outside the gate keep the original body; under the gate use two zones."""
    x = np.asarray(x_cm)
    # Use the exact decimal boundaries registered in the DEVSIM equation.
    # Reassociated floating arithmetic can otherwise classify x==middle
    # differently after mesh serialization.
    raw_left = device.source_length_um * UM
    left = float(f"{raw_left:.6e}")
    right = float(f"{raw_left + device.gate_length_um * UM:.6e}")
    middle = float(f"{raw_left + device.gate_length_um * UM * profile.split_fraction:.6e}")
    return np.where(x < left, device.body_doping_cm3,
                    np.where(x < middle, profile.source_side_na_cm3,
                             np.where(x <= right, profile.drain_side_na_cm3,
                                      device.body_doping_cm3)))


class ProfileCellSimulator(CellSimulator):
    def __init__(self, device, capacitor, profile: ChannelDoping):
        self.profile = profile
        super().__init__(device, capacitor)

    def _build_doping(self):
        super()._build_doping()
        middle = self.x_gate_left + self.dev.gate_length_um * UM * self.profile.split_fraction
        acceptor = (
            f"ifelse(x < {self.x_gate_left:.6e}, {self.dev.body_doping_cm3:.6e}, "
            f"ifelse(x < {middle:.6e}, {self.profile.source_side_na_cm3:.6e}, "
            f"ifelse(x <= {self.x_gate_right:.6e}, {self.profile.drain_side_na_cm3:.6e}, "
            f"{self.dev.body_doping_cm3:.6e})))")
        # No HaloDoping/LDDDoping dependency: the actual spatial distribution
        # lives in the standard NetDoping model before structure-only export.
        devsim.node_model(device=self.name, region="bulk", name="NetDoping",
                          equation=f"SourceDoping + DrainDoping - ({acceptor})")
        x = devsim.get_node_model_values(device=self.name, region="bulk", name="x")
        source = np.asarray(devsim.get_node_model_values(device=self.name, region="bulk", name="SourceDoping"))
        drain = np.asarray(devsim.get_node_model_values(device=self.name, region="bulk", name="DrainDoping"))
        actual = np.asarray(devsim.get_node_model_values(device=self.name, region="bulk", name="NetDoping"))
        expected = source + drain - channel_acceptor_cm3(x, self.dev, self.profile)
        if not np.allclose(actual, expected, rtol=1e-12, atol=1e6):
            raise RuntimeError("Actual NetDoping disagrees with channel profile")
