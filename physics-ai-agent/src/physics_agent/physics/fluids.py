"""Fluid mechanics: Bernoulli, Reynolds, pipe losses, drag (sphere approx)."""
from __future__ import annotations

import math

from physics_agent.knowledge.constants import get_constant
from physics_agent.physics.base import PhysicsResult, require_positive

G0 = get_constant("g0").value


def bernoulli_velocity(p1: float, p2: float, rho: float, v1: float = 0.0,
                       z1: float = 0.0, z2: float = 0.0, g: float = G0) -> PhysicsResult:
    """Downstream velocity from Bernoulli between stations 1 → 2."""
    require_positive(rho=rho)
    v2sq = v1**2 + 2 * (p1 - p2) / rho + 2 * g * (z1 - z2)
    if v2sq < 0:
        raise ValueError("Negative v2²: stations violate Bernoulli assumptions (losses? pump?).")
    return PhysicsResult("velocity", math.sqrt(v2sq), "m/s",
                         "p+½ρv²+ρgz = const", "analytic",
                         ["steady", "incompressible", "inviscid", "along streamline"])


def reynolds(rho: float, v: float, L: float, mu: float) -> PhysicsResult:
    """Reynolds number Re = rho*v*L/mu."""
    require_positive(rho=rho, v=v, L=L, mu=mu)
    return PhysicsResult("reynolds", rho * v * L / mu, "dimensionless",
                         "Re = ρvL/μ", "analytic")


def friction_factor(Re: float, roughness: float = 0.0, D: float = 1.0) -> PhysicsResult:
    """Darcy f: 64/Re laminar; Haaland turbulent; cubic blend in transition."""
    require_positive(Re=Re)
    if Re < 2300:
        f = 64.0 / Re
        method = "analytic (64/Re)"
    else:
        eD = roughness / D
        f = (-1.8 * math.log10((eD / 3.7) ** 1.11 + 6.9 / Re)) ** -2
        method = "Haaland approximation"
    return PhysicsResult("darcy_friction", f, "dimensionless", method, "analytic")


def pipe_pressure_drop(f: float, L: float, D: float, rho: float, v: float) -> PhysicsResult:
    """Δp = f(L/D)ρv²/2 (Darcy-Weisbach)."""
    require_positive(L=L, D=D, rho=rho, v=v)
    return PhysicsResult("pressure_drop", f * (L / D) * rho * v**2 / 2, "Pa",
                         "Δp = f(L/D)ρv²/2", "analytic")


def poiseuille_drop(mu: float, L: float, Q: float, D: float) -> PhysicsResult:
    """Laminar circular-pipe drop dP = 128*mu*L*Q/(pi*D^4)."""
    require_positive(mu=mu, L=L, Q=Q, D=D)
    return PhysicsResult("pressure_drop", 128 * mu * L * Q / (math.pi * D**4), "Pa",
                         "Δp = 128μLQ/πD⁴", "analytic",
                         ["laminar", "fully developed", "circular pipe"])


def drag_sphere(rho: float, v: float, D: float, mu: float) -> dict[str, PhysicsResult]:
    """Sphere drag with standard Cd(Re) correlation (Clift-Gauvin-ish fit)."""
    Re = rho * v * D / mu
    if Re < 0.1:
        Cd = 24 / max(Re, 1e-9)
    else:
        Cd = (24 / Re) * (1 + 0.15 * Re**0.687) + 0.42 / (1 + 42500 * Re**-1.16)
    A = math.pi * D**2 / 4
    F = 0.5 * rho * v**2 * A * Cd
    return {
        "reynolds": PhysicsResult("reynolds", Re, "dimensionless", "Re = ρvD/μ", "analytic"),
        "drag_coefficient": PhysicsResult("drag_coefficient", Cd, "dimensionless",
                                          "Cd(Re) correlation", "empirical"),
        "drag_force": PhysicsResult("drag_force", F, "N", "F = ½ρv²ACd", "analytic"),
    }
