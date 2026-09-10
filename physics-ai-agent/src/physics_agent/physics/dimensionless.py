"""Dimensionless-number evaluators (Re, Ma, Pr, Nu, Fr, St, ...)."""
from __future__ import annotations

import math

from physics_agent.physics.base import PhysicsResult


def reynolds(rho: float, v: float, L: float, mu: float) -> PhysicsResult:
    return PhysicsResult("Re", rho * v * L / mu, "dimensionless", "Re = ρvL/μ", "analytic")


def mach(v: float, a: float) -> PhysicsResult:
    return PhysicsResult("Ma", v / a, "dimensionless", "Ma = v/a", "analytic")


def prandtl(mu: float, cp: float, k: float) -> PhysicsResult:
    return PhysicsResult("Pr", mu * cp / k, "dimensionless", "Pr = μcp/k", "analytic")


def nusselt(h: float, L: float, k: float) -> PhysicsResult:
    return PhysicsResult("Nu", h * L / k, "dimensionless", "Nu = hL/k", "analytic")


def froude(v: float, L: float, g: float = 9.80665) -> PhysicsResult:
    return PhysicsResult("Fr", v / math.sqrt(g * L), "dimensionless", "Fr = v/√(gL)", "analytic")


def biot(h: float, L: float, k: float) -> PhysicsResult:
    return PhysicsResult("Bi", h * L / k, "dimensionless", "Bi = hL/k_solid", "analytic")


def fourier(alpha: float, t: float, L: float) -> PhysicsResult:
    return PhysicsResult("Fo", alpha * t / L**2, "dimensionless", "Fo = αt/L²", "analytic")
