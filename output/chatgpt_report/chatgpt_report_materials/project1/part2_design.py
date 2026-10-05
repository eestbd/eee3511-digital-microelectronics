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
    source_nd_cm3: float | None = None
    drain_nd_cm3: float | None = None

    def __post_init__(self):
        for value in (self.source_side_na_cm3, self.drain_side_na_cm3):
            if not math.isfinite(value) or not 1e14 <= value <= 1e17:
                raise ValueError("Local body doping must be 1e14..1e17 cm^-3")
        if not math.isfinite(self.split_fraction) or not 0.1 <= self.split_fraction <= 0.9:
            raise ValueError("Channel split fraction must be 0.1..0.9")
        for value in (self.source_nd_cm3, self.drain_nd_cm3):
            if value is not None and (not math.isfinite(value) or not 1e18 <= value <= 1e21):
                raise ValueError("Each source/drain donor concentration must be 1e18..1e21")


@dataclass(frozen=True)
class BodyTap:
    additional_acceptor_cm3: float = 1e19
    thickness_um: float = 0.05

    def __post_init__(self):
        if not math.isfinite(self.additional_acceptor_cm3) or not 1e18 <= self.additional_acceptor_cm3 <= 1e21:
            raise ValueError("Finite p+ tap concentration required")
        if not math.isfinite(self.thickness_um) or self.thickness_um <= 0:
            raise ValueError("Positive p+ tap thickness required")


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
    def __init__(self, device, capacitor, profile: ChannelDoping | None = None,
                 body_tap: BodyTap | None = None):
        self.profile = profile
        self.body_tap = body_tap
        if body_tap and body_tap.thickness_um >= device.silicon_thickness_um:
            raise ValueError("Body tap must be thinner than the silicon")
        super().__init__(device, capacitor)

    def _build_doping(self):
        super()._build_doping()
        if self.profile:
            decay_x = self.dev.doping_decay_x_nm * 1e-7
            decay_y = self.dev.doping_decay_y_nm * 1e-7
            for region_name, concentration, boundary, sign in (
                    ("SourceDoping", self.profile.source_nd_cm3, self.x_gate_left, ""),
                    ("DrainDoping", self.profile.drain_nd_cm3, self.x_gate_right, "-")):
                if concentration is not None:
                    devsim.node_model(
                        device=self.name, region="bulk", name=region_name,
                        equation=f"0.25*{concentration:.6e}*erfc({sign}(x-{boundary:.6e})/{decay_x:.6e})"
                                 f"*erfc((y-{self.y_junction:.6e})/{decay_y:.6e})")
        middle = self.x_gate_left + self.dev.gate_length_um * UM * self.profile.split_fraction if self.profile else 0
        acceptor = (
            f"ifelse(x < {self.x_gate_left:.6e}, {self.dev.body_doping_cm3:.6e}, "
            f"ifelse(x < {middle:.6e}, {self.profile.source_side_na_cm3:.6e}, "
            f"ifelse(x <= {self.x_gate_right:.6e}, {self.profile.drain_side_na_cm3:.6e}, "
            f"{self.dev.body_doping_cm3:.6e})))") if self.profile else f"{self.dev.body_doping_cm3:.6e}"
        tap_term = ""
        if self.body_tap:
            boundary = self.y_bottom - self.body_tap.thickness_um * UM
            devsim.node_model(device=self.name, region="bulk", name="TapDoping",
                              equation=f"ifelse(y >= {boundary:.6e}, {self.body_tap.additional_acceptor_cm3:.6e}, 0)")
            tap_term = " - TapDoping"
        # No HaloDoping/LDDDoping dependency: the actual spatial distribution
        # lives in the standard NetDoping model before structure-only export.
        devsim.node_model(device=self.name, region="bulk", name="NetDoping",
                          equation=f"SourceDoping + DrainDoping - ({acceptor}){tap_term}")
        x = devsim.get_node_model_values(device=self.name, region="bulk", name="x")
        source = np.asarray(devsim.get_node_model_values(device=self.name, region="bulk", name="SourceDoping"))
        drain = np.asarray(devsim.get_node_model_values(device=self.name, region="bulk", name="DrainDoping"))
        actual = np.asarray(devsim.get_node_model_values(device=self.name, region="bulk", name="NetDoping"))
        expected = source + drain - (channel_acceptor_cm3(x, self.dev, self.profile)
                                    if self.profile else self.dev.body_doping_cm3)
        if self.body_tap:
            expected -= np.asarray(devsim.get_node_model_values(device=self.name, region="bulk", name="TapDoping"))
        if not np.allclose(actual, expected, rtol=1e-12, atol=1e6):
            raise RuntimeError("Actual NetDoping disagrees with channel profile")
