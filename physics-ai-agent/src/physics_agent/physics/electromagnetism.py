"""Electricity, magnetism, circuits (DC/AC phasor basics)."""
from __future__ import annotations

import cmath
import math

from physics_agent.knowledge.constants import get_constant
from physics_agent.physics.base import PhysicsResult, require_positive

KE = get_constant("k_e").value
MU0 = get_constant("mu0").value
EPS0 = get_constant("eps0").value


def coulomb(q1: float, q2: float, r: float) -> PhysicsResult:
    """Point-charge force F = k*q1*q2/r^2 (signed: +=repulsion)."""
    require_positive(r=r)
    return PhysicsResult("force", KE * q1 * q2 / r**2, "N", "F = kq1q2/r²", "analytic",
                         ["point charges", "static"])


def e_field_point(q: float, r: float) -> PhysicsResult:
    """Point-charge E-field E = k*q/r^2."""
    require_positive(r=r)
    return PhysicsResult("e_field", KE * q / r**2, "V/m", "E = kq/r²", "analytic")


def b_field_wire(I: float, r: float) -> PhysicsResult:
    """Infinite-wire field B = mu0*I/(2*pi*r)."""
    require_positive(r=r)
    return PhysicsResult("b_field", MU0 * I / (2 * math.pi * r), "T",
                         "B = μ₀I/2πr", "analytic", ["infinite straight wire", "DC"])


def solenoid_field(n_turns_per_m: float, I: float) -> PhysicsResult:
    """Long-solenoid field B = mu0*n*I."""
    require_positive(n_turns_per_m=n_turns_per_m)
    return PhysicsResult("b_field", MU0 * n_turns_per_m * I, "T",
                         "B = μ₀nI", "analytic", ["long solenoid", "vacuum core"])


def lorentz_force(q: float, E: float, v: float, B: float, theta_deg: float = 90.0) -> PhysicsResult:
    """|F| for E + v×B with angle θ between v and B (E parallel to motion assumed scalar)."""
    th = math.radians(theta_deg)
    return PhysicsResult("force", q * (E + v * B * math.sin(th)), "N",
                         "F = q(E + vBsinθ)", "analytic")


def ohms_law(V: float | None = None, I: float | None = None,
             R: float | None = None) -> PhysicsResult:
    """Solve V = I*R for whichever of V, I, R is None."""
    given = {"V": V, "I": I, "R": R}
    if sum(v is None for v in given.values()) != 1:
        raise ValueError("Provide exactly two of V, I, R.")
    if V is None:
        return PhysicsResult("voltage", I * R, "V", "V = IR", "analytic")
    if I is None:
        return PhysicsResult("current", V / R, "A", "I = V/R", "analytic")
    return PhysicsResult("resistance", V / I, "ohm", "R = V/I", "analytic")


def rc_time_constant(R: float, C: float) -> PhysicsResult:
    """RC time constant tau = R*C."""
    require_positive(R=R, C=C)
    return PhysicsResult("time_constant", R * C, "s", "τ = RC", "analytic")


def rlc_resonance(L: float, C: float) -> PhysicsResult:
    """Series-RLC resonance f0 = 1/(2*pi*sqrt(L*C))."""
    require_positive(L=L, C=C)
    return PhysicsResult("resonant_freq", 1 / (2 * math.pi * math.sqrt(L * C)), "Hz",
                         "f0 = 1/2π√(LC)", "analytic")


def ac_impedance(R: float, L: float, C: float, f: float) -> dict[str, PhysicsResult]:
    """Series RLC phasor impedance Z = R + j(ωL − 1/ωC)."""
    w = 2 * math.pi * f
    Z = complex(R, w * L - 1 / (w * C))
    return {
        "impedance": PhysicsResult("impedance_mag", abs(Z), "ohm", "|Z|", "analytic"),
        "phase_deg": PhysicsResult("phase", math.degrees(cmath.phase(Z)), "deg", "∠Z", "analytic"),
    }
