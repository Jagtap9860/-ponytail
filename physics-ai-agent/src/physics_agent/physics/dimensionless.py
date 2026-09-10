"""Dimensionless-number evaluators (Re, Ma, Pr, Nu, Fr, St, ...)."""
from __future__ import annotations

import math

from physics_agent.knowledge.constants import get_constant
from physics_agent.physics.base import PhysicsResult

_G0 = get_constant("g0").value


def reynolds(rho: float, v: float, L: float, mu: float) -> PhysicsResult:
    """Reynolds number Re = rho*v*L/mu."""
    return PhysicsResult("Re", rho * v * L / mu, "dimensionless", "Re = ρvL/μ", "analytic")


def mach(v: float, a: float) -> PhysicsResult:
    """Mach number Ma = v/a."""
    return PhysicsResult("Ma", v / a, "dimensionless", "Ma = v/a", "analytic")


def prandtl(mu: float, cp: float, k: float) -> PhysicsResult:
    """Prandtl number Pr = mu*cp/k."""
    return PhysicsResult("Pr", mu * cp / k, "dimensionless", "Pr = μcp/k", "analytic")


def nusselt(h: float, L: float, k: float) -> PhysicsResult:
    """Nusselt number Nu = h*L/k."""
    return PhysicsResult("Nu", h * L / k, "dimensionless", "Nu = hL/k", "analytic")


def froude(v: float, L: float, g: float | None = None) -> PhysicsResult:
    """Froude number Fr = v/√(gL); g defaults to standard gravity."""
    g = _G0 if g is None else g
    return PhysicsResult("Fr", v / math.sqrt(g * L), "dimensionless", "Fr = v/√(gL)", "analytic")


def biot(h: float, L: float, k: float) -> PhysicsResult:
    """Biot number Bi = h*L/k_solid."""
    return PhysicsResult("Bi", h * L / k, "dimensionless", "Bi = hL/k_solid", "analytic")


def fourier(alpha: float, t: float, L: float) -> PhysicsResult:
    """Fourier number Fo = alpha*t/L^2."""
    return PhysicsResult("Fo", alpha * t / L**2, "dimensionless", "Fo = αt/L²", "analytic")
