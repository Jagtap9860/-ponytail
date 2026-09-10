"""Classical / engineering mechanics, statics, dynamics, kinematics, rotation, beams."""
from __future__ import annotations

import math

import numpy as np

from physics_agent.knowledge.constants import get_constant
from physics_agent.physics.base import PhysicsResult, require_positive

G0 = get_constant("g0").value
G = get_constant("G").value


def newtons_second_law(F: float | None = None, m: float | None = None,
                       a: float | None = None) -> PhysicsResult:
    """Solve F = m·a for whichever one argument is None (SI units)."""
    given = {k: v for k, v in {"F": F, "m": m, "a": a}.items() if v is not None}
    if len(given) != 2:
        raise ValueError("Provide exactly two of F, m, a.")
    if F is None:
        require_positive(m=m if m else 1.0)
        return PhysicsResult("force", m * a, "N", "F = m·a", "analytic")
    if m is None:
        return PhysicsResult("mass", F / a, "kg", "m = F/a", "analytic")
    return PhysicsResult("acceleration", F / m, "m/s^2", "a = F/m", "analytic")


def projectile(v0: float, theta_deg: float, y0: float = 0.0, g: float = G0) -> dict[str, PhysicsResult]:
    """Vacuum projectile: range, max height, flight time (flat landing y=0)."""
    require_positive(v0=v0)
    th = math.radians(theta_deg)
    vx, vy = v0 * math.cos(th), v0 * math.sin(th)
    t = (vy + math.sqrt(vy**2 + 2 * g * y0)) / g
    R = vx * t
    H = y0 + vy**2 / (2 * g)
    return {
        "range": PhysicsResult("range", R, "m", "R = vx·t", "analytic",
                               ["no drag", "uniform g", "flat ground"]),
        "max_height": PhysicsResult("max_height", H, "m", "H = y0 + vy²/2g", "analytic"),
        "flight_time": PhysicsResult("flight_time", t, "s", "y(t)=0", "analytic"),
    }


def kinetic_energy(m: float, v: float) -> PhysicsResult:
    """Kinetic energy KE = 0.5*m*v^2."""
    require_positive(m=m)
    return PhysicsResult("kinetic_energy", 0.5 * m * v**2, "J", "KE = ½mv²", "analytic")


def gravitational_force(m1: float, m2: float, r: float) -> PhysicsResult:
    """Newton gravitation F = G*m1*m2/r^2 (point masses)."""
    require_positive(m1=m1, m2=m2, r=r)
    return PhysicsResult("gravitational_force", G * m1 * m2 / r**2, "N",
                         "F = G·m1·m2/r²", "analytic", ["point masses"])


def circular_motion(v: float | None = None, omega: float | None = None,
                    r: float = 1.0) -> PhysicsResult:
    """Centripetal acceleration a_c = v²/r = ω²r."""
    require_positive(r=r)
    if (v is None) == (omega is None):
        raise ValueError("Provide exactly one of v, omega.")
    a = v**2 / r if v is not None else omega**2 * r
    return PhysicsResult("centripetal_acceleration", a, "m/s^2", "a_c = v²/r = ω²r", "analytic")


def incline_slide(m: float, theta_deg: float, mu: float, g: float = G0) -> dict[str, PhysicsResult]:
    """Block on incline: acceleration and friction regime check."""
    require_positive(m=m)
    th = math.radians(theta_deg)
    if mu < 0:
        raise ValueError("mu must be >= 0.")
    slips = math.tan(th) > mu
    a = g * (math.sin(th) - mu * math.cos(th)) if slips else 0.0
    return {
        "acceleration": PhysicsResult("acceleration", max(a, 0.0), "m/s^2",
                                      "a = g(sinθ − μcosθ)", "analytic",
                                      ["Coulomb friction", "rigid block"]),
        "slips": PhysicsResult("slips", slips, "bool", "tanθ > μ", "analytic"),
    }


def cantilever_tip(F: float, L: float, E: float, I: float) -> PhysicsResult:
    """Euler-Bernoulli cantilever tip deflection δ = FL³/3EI."""
    require_positive(F=F, L=L, E=E, I=I)
    return PhysicsResult("tip_deflection", F * L**3 / (3 * E * I), "m",
                         "δ = F·L³/(3EI)", "analytic",
                         ["Euler-Bernoulli", "small deflection", "prismatic beam"])


def simply_supported_center(F: float, L: float, E: float, I: float) -> PhysicsResult:
    """Midspan deflection δ = FL³/48EI under central load."""
    require_positive(F=F, L=L, E=E, I=I)
    return PhysicsResult("midspan_deflection", F * L**3 / (48 * E * I), "m",
                         "δ = F·L³/(48EI)", "analytic")


def torsion_bar(T: float, L: float, GJ: float) -> PhysicsResult:
    """Angle of twist φ = TL/GJ."""
    require_positive(L=L, GJ=GJ)
    return PhysicsResult("twist_angle", T * L / GJ, "rad", "φ = T·L/GJ", "analytic")


def moment_of_inertia_solid_cylinder(m: float, r: float) -> PhysicsResult:
    """Solid cylinder I = 0.5*m*r^2 about its axis."""
    require_positive(m=m, r=r)
    return PhysicsResult("moment_of_inertia", 0.5 * m * r**2, "kg*m^2",
                         "I = ½mr²", "analytic")
