"""Physics domain classifier: rule/keyword scoring over 38 spec domains.

Deterministic and dependency-free. Returns ranked domains plus problem-type
hints, complexity estimates, and suggested methods/tools.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class Classification:
    """Classification: domain, complexity, methods, suggested tools."""
    domain: str
    subdomain: str
    problem_type: str
    scores: dict[str, float]
    math_complexity: str          # low | medium | high
    computational_complexity: str
    needs_symbolic: bool
    needs_numeric: bool
    needs_plot: bool
    suggested_tools: list[str] = field(default_factory=list)


# key -> (title, keywords, subdomain hints: keyword -> (subdomain, problem_type))
_DOMAINS: dict[str, tuple[str, tuple[str, ...], dict[str, tuple[str, str]]]] = {
    "classical_mechanics": ("Classical Mechanics",
        ("newton", "force", "mass", "acceleration", "projectile", "kinematic", "incline",
         "friction", "momentum", "energy", "orbit", "gravity", "pendulum"),
        {"projectile": ("Kinematics", "Projectile motion"),
         "incline": ("Dynamics", "Inclined plane with friction"),
         "pendulum": ("Dynamics", "Pendulum"),
         "orbit": ("Gravitation", "Orbital motion")}),
    "engineering_mechanics": ("Engineering Mechanics",
        ("static equilibrium", "truss", "beam", "cantilever", "reactions", "free-body",
         "fbd", "shear", "bending moment", "torsion", "deflection"),
        {"beam": ("Strength of Materials", "Beam deflection"),
         "truss": ("Statics", "Truss analysis")}),
    "vibrations": ("Vibrations & Structural Dynamics",
        ("vibration", "natural frequenc", "resonance", "damping", "sdof", "mdof", "modal",
         "harmonic", "transmissibility", "isolat", "spring", "damper", "fft", "rotor",
         "campbell", "critical speed", "frequency response"),
        {"resonance": ("Forced Vibration", "Resonance assessment"),
         "modal": ("Modal Analysis", "Natural frequencies & mode shapes"),
         "transmissibility": ("Isolation", "Transmissibility"),
         "rotor": ("Rotor Dynamics", "Critical speeds")}),
    "fluid_mechanics": ("Fluid Mechanics",
        ("fluid", "bernoulli", "reynolds", "pipe", "pressure drop", "drag", "navier",
         "viscosity", "pump", "turbulent", "laminar", "flow", "head loss", "fsi"),
        {"bernoulli": ("Inviscid Flow", "Bernoulli application"),
         "pipe": ("Pipe Flow", "Head/pressure loss"),
         "reynolds": ("Dimensional Analysis", "Flow regime")}),
    "thermodynamics": ("Thermodynamics",
        ("thermodynamic", "entropy", "carnot", "ideal gas", "heat engine", "enthalpy",
         "cycle", "compressor", "turbine"),
        {"carnot": ("Second Law", "Carnot limit"),
         "ideal gas": ("Equations of State", "Ideal-gas state change")}),
    "heat_transfer": ("Heat Transfer",
        ("conduction", "convection", "radiation", "fourier", "lmtd", "heat exchanger",
         "emissivity", "insulation", "heat transfer", "nusselt"),
        {"conduction": ("Conduction", "Steady conduction"),
         "lmtd": ("Heat Exchangers", "LMTD sizing")}),
    "electromagnetism": ("Electromagnetism",
        ("coulomb", "electric", "magnetic", "maxwell", "faraday", "induct", "capacitor",
         "resistor", "circuit", "voltage", "current", "impedance", "lorentz", "solenoid",
         "gauss", "ampere", "rlc", "rc "),
        {"circuit": ("Circuits", "DC/AC circuit"),
         "coulomb": ("Electrostatics", "Point charges")}),
    "optics": ("Optics",
        ("lens", "snell", "refraction", "reflection", "focal", "mirror", "diffraction",
         "interference", "polarization", "tir", "fiber"),
        {"lens": ("Geometrical Optics", "Imaging"),
         "snell": ("Geometrical Optics", "Refraction")}),
    "waves": ("Waves & Acoustics",
        ("wave", "sound", "acoustic", "doppler", "decibel", "spl", "string",
         "standing wave", "wavelength", "octave"),
        {"doppler": ("Acoustics", "Doppler shift"),
         "string": ("Vibrating Systems", "String modes")}),
    "quantum_mechanics": ("Quantum & Modern Physics",
        ("quantum", "photon", "planck", "schrodinger", "de broglie", "particle in a box",
         "uncertainty", "radioactive", "half-life", "blackbody", "photoelectric",
         "bohr", "rydberg", "wavelength", "light", "spectroscopy"),
        {"photon": ("Photons", "Photon energy"),
         "particle in a box": ("Bound States", "Confinement energies")}),
    "relativity": ("Relativity",
        ("relativ", "lorentz", "time dilation", "length contraction", "rest energy",
         "muon", "twin paradox", "gamma factor"),
        {"time dilation": ("Special Relativity", "Time dilation")}),
    "statistical_mechanics": ("Statistical Mechanics",
        ("boltzmann", "maxwell-boltzmann", "partition function", "ensemble",
         "rms speed", "equipartition"),
        {}),
    "continuum_mechanics": ("Continuum Mechanics",
        ("continuum", "stress tensor", "strain tensor", "constitutive", "cauchy"),
        {}),
    "fea": ("FEA & Computational Mechanics",
        ("fea", "finite element", "ansys", "abaqus", "mesh", "convergence",
         "singularity", "contact", "buckling", "prestress", "harmonic analysis",
         "transient", "fatigue", "s-n", "miner", "participation factor"),
        {"ansys": ("FEA Practice", "Results interpretation"),
         "convergence": ("FEA Practice", "Mesh convergence"),
         "fatigue": ("Fatigue", "S–N / damage")}),
    "control": ("Control Systems",
        ("transfer function", "bode", "pid", "state-space", "stability", "nyquist",
         "step response"),
        {"bode": ("Frequency Domain", "Stability margins")}),
}

_MATH_HARD = ("pde", "navier", "schrodinger", "tensor", "nonlinear", "turbulent",
              "eigenvalue", "coupled", "transient", "optimization")
_PLOT_HINTS = ("plot", "graph", "frf", "bode", "fft", "spectrum", "response",
               "time history", "mode shape", "campbell", "diagram")


def classify(text: str) -> Classification:
    """Keyword-scored domain classifier over the 14 domain groups."""
    t = text.lower()
    scores: dict[str, float] = {}
    for key, (_, kws, _) in _DOMAINS.items():
        s = 0.0
        for kw in kws:
            n = len(re.findall(re.escape(kw), t))
            if n:
                s += n * (2.0 if len(kw.split()) > 1 or len(kw) > 8 else 1.0)
        if s:
            scores[key] = s
    domain = max(scores, key=scores.get) if scores else "classical_mechanics"
    title, _, sub_hints = _DOMAINS[domain]
    subdomain, problem_type = "General", "Quantitative problem"
    for kw, (sd, pt) in sub_hints.items():
        if kw in t:
            subdomain, problem_type = sd, pt
            break
    hard = sum(1 for k in _MATH_HARD if k in t)
    math_cx = "high" if hard >= 2 else ("medium" if hard == 1 or len(t.split()) > 60 else "low")
    needs_symbolic = any(k in t for k in ("derive", "derivation", "symbolic", "prove", "analytical"))
    needs_numeric = any(k in t for k in ("solve", "compute", "calculate", "find", "simulate",
                                         "optimize", "fit", "ode", "eigenvalue")) or bool(
        re.search(r"\d", t))
    needs_plot = any(k in t for k in _PLOT_HINTS)
    tools = ["lookup_formula", "check_dimensions", "convert_units"]
    if needs_symbolic:
        tools.append("solve_equation")
    if "ode" in t or "transient" in t or "time response" in t:
        tools.append("solve_ode")
    if "eigen" in t or "modal" in t or "mode shape" in t:
        tools.append("solve_eigenvalue_problem")
    if "fft" in t or "spectrum" in t:
        tools.append("fft")
    if needs_plot:
        tools.append("plot_function")
    return Classification(domain, subdomain, problem_type, scores, math_cx,
                          "medium" if needs_numeric else "low",
                          needs_symbolic, needs_numeric or not needs_symbolic,
                          needs_plot, tools)
