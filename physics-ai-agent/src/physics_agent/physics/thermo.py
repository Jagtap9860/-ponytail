"""Thermodynamics & heat transfer: ideal gas, laws, conduction/convection/radiation."""
from __future__ import annotations

import math

from physics_agent.knowledge.constants import get_constant
from physics_agent.physics.base import PhysicsResult, require_positive

R = get_constant("R").value
SIGMA = get_constant("sigma").value


def ideal_gas(p: float | None = None, V: float | None = None, n: float | None = None,
              T: float | None = None) -> PhysicsResult:
    """Solve pV = nRT for the missing variable (absolute T, absolute p)."""
    args = {"p": p, "V": V, "n": n, "T": T}
    if sum(v is None for v in args.values()) != 1:
        raise ValueError("Provide exactly three of p, V, n, T.")
    if T is not None and T <= 0:
        raise ValueError("Temperature must be absolute (K) and > 0.")
    if p is None:
        return PhysicsResult("pressure", n * R * T / V, "Pa", "p = nRT/V", "analytic")
    if V is None:
        return PhysicsResult("volume", n * R * T / p, "m^3", "V = nRT/p", "analytic")
    if n is None:
        return PhysicsResult("moles", p * V / (R * T), "mol", "n = pV/RT", "analytic")
    return PhysicsResult("temperature", p * V / (n * R), "K", "T = pV/nR", "analytic")


def carnot_efficiency(T_hot: float, T_cold: float) -> PhysicsResult:
    require_positive(T_hot=T_hot, T_cold=T_cold)
    if T_cold >= T_hot:
        raise ValueError("Need T_cold < T_hot.")
    return PhysicsResult("carnot_efficiency", 1 - T_cold / T_hot, "dimensionless",
                         "η = 1 − Tc/Th", "analytic", ["reversible", "two reservoirs"])


def conduction_1d(k: float, A: float, T1: float, T2: float, L: float) -> PhysicsResult:
    """Steady 1-D conduction Q = kA(T1−T2)/L."""
    require_positive(k=k, A=A, L=L)
    return PhysicsResult("heat_rate", k * A * (T1 - T2) / L, "W",
                         "Q = kA(T1−T2)/L", "analytic", ["steady 1-D", "constant k"])


def convection(h: float, A: float, Ts: float, Tinf: float) -> PhysicsResult:
    require_positive(h=h, A=A)
    return PhysicsResult("heat_rate", h * A * (Ts - Tinf), "W",
                         "Q = hA(Ts−T∞)", "analytic", ["h uniform over surface"])


def radiation(eps: float, A: float, Ts: float, Tsurr: float) -> PhysicsResult:
    require_positive(A=A)
    if not 0 < eps <= 1:
        raise ValueError("Emissivity must be in (0, 1].")
    return PhysicsResult("heat_rate", eps * SIGMA * A * (Ts**4 - Tsurr**4), "W",
                         "Q = εσA(Ts⁴−Tsurr⁴)", "analytic",
                         ["diffuse gray", "large isothermal surroundings"])


def lmtd(Th_in: float, Th_out: float, Tc_in: float, Tc_out: float,
         counterflow: bool = True) -> PhysicsResult:
    """Log-mean temperature difference for heat exchangers."""
    if counterflow:
        d1, d2 = Th_in - Tc_out, Th_out - Tc_in
    else:
        d1, d2 = Th_in - Tc_in, Th_out - Tc_out
    if d1 <= 0 or d2 <= 0:
        raise ValueError("Temperature cross detected; check flow arrangement.")
    val = (d1 - d2) / math.log(d1 / d2) if abs(d1 - d2) > 1e-12 else d1
    return PhysicsResult("lmtd", val, "K", "LMTD = (ΔT1−ΔT2)/ln(ΔT1/ΔT2)", "analytic")
