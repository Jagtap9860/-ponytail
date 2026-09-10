"""Centralized physical-constant database (SI values, never hard-coded in solvers)."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Constant:
    symbol: str
    name: str
    value: float
    unit: str
    description: str = ""
    source: str = ""
    precision: str = ""


def _data_dirs() -> list[Path]:
    here = Path(__file__).resolve()
    return [
        here.parents[3] / "data" / "constants",  # repo checkout: physics-ai-agent/data
        here.parents[1] / "data" / "constants",  # installed alongside package (fallback)
    ]


def _load() -> dict[str, Constant]:
    out: dict[str, Constant] = {}
    for d in _data_dirs():
        if not d.exists():
            continue
        for f in sorted(d.glob("*.json")):
            for row in json.loads(f.read_text(encoding="utf-8")):
                out[row["symbol"]] = Constant(**row)
    if not out:  # pragma: no cover - last-resort fallback keeps solvers working
        out = {
            "c": Constant("c", "speed of light", 299792458.0, "m/s"),
            "G": Constant("G", "gravitation", 6.6743e-11, "m^3/kg/s^2"),
            "h": Constant("h", "Planck", 6.62607015e-34, "J*s"),
            "g0": Constant("g0", "standard gravity", 9.80665, "m/s^2"),
        }
    return out


CONSTANTS: dict[str, Constant] = _load()


def get_constant(symbol: str) -> Constant:
    """Fetch a constant by symbol (e.g. 'c', 'hbar', 'g0'). Raises KeyError with hint."""
    if symbol in CONSTANTS:
        return CONSTANTS[symbol]
    close = [s for s in CONSTANTS if symbol.lower() in s.lower() or symbol.lower() in CONSTANTS[s].name.lower()]
    hint = f" Did you mean one of {close}?" if close else f" Known: {sorted(CONSTANTS)}."
    raise KeyError(f"Unknown constant '{symbol}'." + hint)


def search_constants(query: str) -> list[Constant]:
    q = query.lower()
    return [c for c in CONSTANTS.values() if q in c.symbol.lower() or q in c.name.lower()]
