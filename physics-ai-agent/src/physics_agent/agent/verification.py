"""Verification agent + error detection (spec §12, step 9, §25 checklist)."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Check:
    name: str
    passed: bool | None  # None = not applicable
    detail: str


@dataclass
class VerificationReport:
    checks: list[Check] = field(default_factory=list)

    @property
    def all_passed(self) -> bool:
        return all(c.passed is not False for c in self.checks)

    def summary(self) -> str:
        return "\n".join(
            f"[{'PASS' if c.passed else ('N/A' if c.passed is None else 'FAIL')}] "
            f"{c.name}: {c.detail}" for c in self.checks)


def detect_errors(text: str, values: dict[str, float]) -> list[str]:
    """Scan for impossible/ambiguous inputs. Returns warning strings."""
    warns: list[str] = []
    t = text.lower()
    for k, v in values.items():
        if k in {"m", "mass", "rho", "density", "E", "k", "stiffness", "L", "length",
                 "D", "diameter", "T", "temp_K", "f", "freq"} and v <= 0:
            warns.append(f"'{k} = {v}' is non-positive — impossible for this quantity.")
        if k in {"v", "velocity", "speed"} and abs(v) > 299792458.0:
            warns.append(f"|v| = {v} m/s exceeds c — check relativity regime/units.")
        if k in {"mu", "viscosity", "c", "damping", "h", "k_thermal"} and v < 0:
            warns.append(f"'{k} = {v}' is negative — unphysical for this coefficient.")
        if k in {"eps", "emissivity"} and not 0 < v <= 1:
            warns.append(f"emissivity {v} outside (0, 1].")
    if "celsius" in t or "degc" in t or "°c" in t:
        warns.append("Celsius detected — gas/radiation/T⁴ laws need absolute kelvin.")
    if "gauge" in t or "psig" in t:
        warns.append("Gauge pressure detected — state equations need absolute pressure.")
    if "rpm" in t and "rad/s" in t:
        warns.append("Both rpm and rad/s appear — confirm which applies where.")
    if "centrifugal" in t:
        warns.append("'Centrifugal' is fictitious (rotating frame); use centripetal in inertial frame.")
    if "fanning" in t:
        warns.append("Fanning friction factor is Darcy/4 — confirm convention.")
    return warns


def limiting_case_note(domain: str) -> str:
    return {
        "vibrations": "ζ→0 recovers undamped ωn; r≫1 response → mass line (X→F0/mω²).",
        "classical_mechanics": "μ→0 recovers frictionless; v≪c recovers Newtonian.",
        "fluid_mechanics": "Re→0 Stokes regime; inviscid+steady recovers Bernoulli.",
        "relativity": "v≪c: γ→1, KE→½mv².",
        "quantum_mechanics": "n≫1 / h→0 correspondence principle.",
    }.get(domain, "Check trivial limits (zero load → zero response; symmetry; statics).")


def self_check_list() -> list[str]:
    return ["Problem correctly understood", "Correct physics domain",
            "Correct governing law", "Correct equation", "Correct assumptions",
            "Units consistent", "Numerical calculation verified",
            "Result physically plausible", "Boundary conditions considered",
            "Limit cases considered where applicable", "No unsupported claims",
            "Explanation matches calculation"]
