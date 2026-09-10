"""Problem understanding, physical-model builder, assumption & error management."""
from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class QuantitySpec:
    name: str
    value: float | None
    unit: str | None
    status: str  # KNOWN | ASSUMED | DERIVED | ESTIMATED | UNKNOWN


@dataclass
class Assumption:
    statement: str
    justification: str
    impact: str = ""


@dataclass
class SolutionPlan:
    question: str
    system: str
    knowns: list[QuantitySpec] = field(default_factory=list)
    unknowns: list[str] = field(default_factory=list)
    assumptions: list[Assumption] = field(default_factory=list)
    principles: list[str] = field(default_factory=list)
    equations: list[str] = field(default_factory=list)
    model: dict[str, str] = field(default_factory=dict)
    missing_info: list[str] = field(default_factory=list)


_QTY_RE = re.compile(
    r"(?P<name>[A-Za-z_][\w]*)\s*=\s*(?P<val>[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)"
    r"\s*(?P<unit>[A-Za-z°Ωμ²³/^\-\.\* ]+)?"
)
_INLINE_QTY_RE = re.compile(
    r"(?P<val>[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)\s*"
    r"(?P<unit>kg|g|N|kN|Pa|kPa|MPa|GPa|psi|ksi|J|kJ|W|kW|m/s|km/h|mph|m|mm|cm|km|in|ft|s|ms|Hz|kHz|rpm|rad/s|deg|K|degC|degF|m\^2|m\^3|L|T|V|A|ohm|F|H|Ns/m|N/m|W/m/K|W/m\^2/K|kg/m\^3|Pa\*s)"
)

_PRINCIPLES = {
    "vibrations": ["Newton's 2nd law (M x¨ + C x˙ + Kx = F)",
                    "Free/forced response of linear oscillators", "Energy dissipation via damping"],
    "classical_mechanics": ["Newton's laws", "Work–energy theorem", "Momentum conservation"],
    "engineering_mechanics": ["Static equilibrium (ΣF=0, ΣM=0)", "Euler-Bernoulli beam theory",
                              "Linear elasticity (Hooke's law)"],
    "fluid_mechanics": ["Mass conservation (continuity)", "Momentum (Navier-Stokes/Euler)",
                        "Bernoulli (with stated limits)", "Reynolds-number similarity"],
    "thermodynamics": ["First law (energy balance)", "Second law / entropy", "Ideal-gas relations"],
    "heat_transfer": ["Fourier's law", "Newton cooling (definition of h)",
                      "Stefan-Boltzmann (gray surfaces)", "Energy balance"],
    "electromagnetism": ["Maxwell's equations", "Lorentz force", "Circuit laws (KVL/KCL, Ohm)"],
    "optics": ["Fermat's principle", "Snell's law", "Paraxial imaging"],
    "waves": ["Wave equation", "Superposition", "Doppler kinematics"],
    "quantum_mechanics": ["Planck postulate", "Schrödinger equation", "Born rule"],
    "relativity": ["Light postulate + relativity principle", "Lorentz invariance"],
    "fea": ["Virtual work / Galerkin discretization", "Eigenanalysis for modes",
            "Convergence & verification theory"],
}


def parse_problem(text: str) -> SolutionPlan:
    """Extract quantities (name=value unit + inline), unknowns, and system hints."""
    knowns: list[QuantitySpec] = []
    seen: set[str] = set()
    for m in _QTY_RE.finditer(text):
        name, val, unit = m.group("name"), float(m.group("val")), (m.group("unit") or "").strip()
        if name.lower() in {"find", "what", "the", "and"} or len(name) > 12:
            continue
        if name in seen:
            continue
        seen.add(name)
        knowns.append(QuantitySpec(name, val, unit or None, "KNOWN"))
    n_inline = 0
    for m in _INLINE_QTY_RE.finditer(text):
        tag = f"value_{n_inline}"
        if tag in seen:
            continue
        seen.add(tag)
        n_inline += 1
        knowns.append(QuantitySpec(tag, float(m.group("val")), m.group("unit"), "KNOWN"))
    unknowns: list[str] = []
    m = re.search(r"(?:find|compute|calculate|determine|what is|estimate)\s+(.{3,80})(\?|$)", text, re.I)
    if m:
        unknowns.append(m.group(1).strip().rstrip("?"))
    system = "unspecified system"
    for cand in ("spring", "mass", "machine", "beam", "pipe", "circuit", "lens", "pendulum",
                 "rotor", "isolator", "heat exchanger", "projectile", "string", "gas"):
        if cand in text.lower():
            system = cand
            break
    return SolutionPlan(question=text.strip(), system=system, knowns=knowns, unknowns=unknowns)


def build_plan(parsed: SolutionPlan, domain: str) -> SolutionPlan:
    """Attach physical-model slots, principles, and standard assumptions."""
    parsed.model = {
        "geometry": "to be specified from problem statement",
        "coordinates": "choose inertial frame; state origin/axes before use",
        "loads": "list all forces/moments/fluxes; avoid double counting",
        "boundary_conditions": "supports, far-field, inlet/outlet as applicable",
        "initial_conditions": "x(0), v(0) / T(0) as applicable",
        "materials": "E, nu, rho, k, mu... cite source, never invent",
        "constraints": "contacts, joints, symmetries",
    }
    parsed.principles = list(_PRINCIPLES.get(domain, ["Conservation laws", "Constitutive relations"]))
    std = {
        "classical_mechanics": Assumption("g = 9.80665 m/s² unless stated",
                                          "standard gravity", "scales weight terms"),
        "vibrations": Assumption("linear viscous damping unless stated",
                                 "standard first model; check amplitude regime",
                                 "nonlinearities shift peaks"),
        "fluid_mechanics": Assumption("incompressible unless Ma > 0.3 indicated",
                                      "liquid/low-speed gas default", "density variation"),
    }
    if domain in std:
        parsed.assumptions.append(std[domain])
    return parsed
