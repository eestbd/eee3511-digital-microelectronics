# -*- coding: utf-8 -*-
"""과제와 checker에 지정된 게이트 재료 이름 및 유효 일함수(eV)."""

GATE_WORK_FUNCTION_EV = {
    "n+poly": 4.05, "Al": 4.10, "Ta": 4.25, "Ti": 4.33, "TaN": 4.45,
    "W": 4.60, "TiN": 4.65, "Mo": 4.70, "Ni": 5.10, "p+poly": 5.15,
    "Pt": 5.30,
}


def canonical_gate_material(name: str) -> str:
    """PDF의 poly-Si 별칭을 checker가 받는 이름으로 바꾸고 숫자는 거부한다."""
    if not isinstance(name, str):
        raise ValueError("gate_material must be a material name, not a number")
    key = name.replace(" ", "").replace("-", "").replace("_", "").lower()
    aliases = {k.lower(): k for k in GATE_WORK_FUNCTION_EV}
    aliases.update({"n+polysi": "n+poly", "p+polysi": "p+poly"})
    if key not in aliases:
        raise ValueError(f"Unknown gate material {name!r}; choose {list(GATE_WORK_FUNCTION_EV)}")
    return aliases[key]
