"""Special relativity: Lorentz factor, dilation/contraction, energy-momentum."""
from __future__ import annotations

import math

from physics_agent.knowledge.constants import get_constant
from physics_agent.physics.base import PhysicsResult, require_positive

C = get_constant("c").value


def lorentz_factor(v: float) -> PhysicsResult:
    if not 0 <= v < C:
        raise ValueError(f"Need 0 ≤ v < c; got v={v} m/s.")
    return PhysicsResult("lorentz_factor", 1 / math.sqrt(1 - (v / C) ** 2), "dimensionless",
                         "γ = 1/√(1−v²/c²)", "analytic")


def time_dilation(dt0: float, v: float) -> PhysicsResult:
    require_positive(dt0=dt0)
    g = lorentz_factor(v).scalar()
    return PhysicsResult("dilated_time", g * dt0, "s", "Δt = γΔt0", "analytic")


def length_contraction(L0: float, v: float) -> PhysicsResult:
    require_positive(L0=L0)
    g = lorentz_factor(v).scalar()
    return PhysicsResult("contracted_length", L0 / g, "m", "L = L0/γ", "analytic")


def relativistic_energy(m: float, v: float) -> dict[str, PhysicsResult]:
    require_positive(m=m)
    g = lorentz_factor(v).scalar()
    E, E0 = g * m * C**2, m * C**2
    return {
        "total": PhysicsResult("total_energy", E, "J", "E = γmc²", "analytic"),
        "kinetic": PhysicsResult("kinetic_energy", E - E0, "J", "KE = (γ−1)mc²", "analytic"),
        "rest": PhysicsResult("rest_energy", E0, "J", "E0 = mc²", "analytic"),
    }


def relativistic_momentum(m: float, v: float) -> PhysicsResult:
    require_positive(m=m)
    g = lorentz_factor(v).scalar()
    return PhysicsResult("momentum", g * m * v, "kg*m/s", "p = γmv", "analytic")
