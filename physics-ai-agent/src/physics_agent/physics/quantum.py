"""Modern physics, quantum mechanics, statistical mechanics."""
from __future__ import annotations

import math

from physics_agent.knowledge.constants import get_constant
from physics_agent.physics.base import PhysicsResult, require_positive

H = get_constant("h").value
HBAR = get_constant("hbar").value
C = get_constant("c").value
KB = get_constant("kB").value
EV = 1.602176634e-19


def photon_energy(f: float | None = None, lam: float | None = None) -> dict[str, PhysicsResult]:
    if (f is None) == (lam is None):
        raise ValueError("Provide exactly one of f, lambda.")
    E = H * f if f is not None else H * C / lam
    return {
        "energy_J": PhysicsResult("photon_energy", E, "J", "E = hf = hc/λ", "analytic"),
        "energy_eV": PhysicsResult("photon_energy", E / EV, "eV", "E/e", "analytic"),
    }


def de_broglie(m: float, v: float) -> PhysicsResult:
    require_positive(m=m, v=v)
    return PhysicsResult("wavelength", H / (m * v), "m", "λ = h/p", "analytic",
                         ["non-relativistic p = mv"])


def particle_in_box(n: int, m: float, L: float) -> PhysicsResult:
    require_positive(m=m, L=L)
    if n < 1:
        raise ValueError("n >= 1.")
    return PhysicsResult("energy_level", n**2 * H**2 / (8 * m * L**2), "J",
                         "En = n²h²/8mL²", "analytic", ["infinite walls"])


def uncertainty_dx(dp: float) -> PhysicsResult:
    require_positive(dp=dp)
    return PhysicsResult("min_position_spread", HBAR / (2 * dp), "m",
                         "Δx ≥ ℏ/2Δp", "analytic")


def radioactive_decay(N0: float, half_life: float, t: float) -> dict[str, PhysicsResult]:
    require_positive(N0=N0, half_life=half_life)
    lam = math.log(2) / half_life
    N = N0 * math.exp(-lam * t)
    return {
        "remaining": PhysicsResult("remaining", N, "nuclei", "N = N0·e^(−λt)", "analytic"),
        "activity": PhysicsResult("activity", lam * N, "Bq", "A = λN", "analytic"),
    }


def maxwell_boltzmann_speeds(m: float, T: float) -> dict[str, PhysicsResult]:
    require_positive(m=m, T=T)
    vp = math.sqrt(2 * KB * T / m)
    return {
        "most_probable": PhysicsResult("speed", vp, "m/s", "vp = √(2kT/m)", "analytic"),
        "mean": PhysicsResult("speed", vp * 2 / math.sqrt(math.pi), "m/s",
                              "v̄ = √(8kT/πm)", "analytic"),
        "rms": PhysicsResult("speed", math.sqrt(3 * KB * T / m), "m/s",
                             "vrms = √(3kT/m)", "analytic"),
    }


def blackbody_exitance(T: float) -> PhysicsResult:
    require_positive(T=T)
    sig = get_constant("sigma").value
    return PhysicsResult("exitance", sig * T**4, "W/m^2", "M = σT⁴", "analytic")
