"""Mechanical vibrations: SDOF/MDOF, free/forced, damping, FRF, transmissibility.

Covers §10 of the spec: natural frequency, resonance, modal analysis,
harmonic excitation, FFT (via solvers.spectral), Campbell/rotor basics.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from physics_agent.physics.base import PhysicsResult, require_positive
from physics_agent.solvers.eigenvalue import generalized_eigen
from physics_agent.solvers.ode import solve_sdof


@dataclass
class SDOF:
    m: float
    c: float
    k: float

    @property
    def wn(self) -> float:
        require_positive(m=self.m, k=self.k)
        return math.sqrt(self.k / self.m)

    @property
    def fn(self) -> float:
        return self.wn / (2 * math.pi)

    @property
    def zeta(self) -> float:
        require_positive(m=self.m, k=self.k)
        return self.c / (2 * math.sqrt(self.k * self.m))

    @property
    def wd(self) -> float:
        z = self.zeta
        if z >= 1:
            raise ValueError(f"Not oscillatory: zeta={z:.3f} >= 1.")
        return self.wn * math.sqrt(1 - z**2)

    @property
    def Q(self) -> float:
        return 1.0 / (2 * self.zeta) if self.zeta > 0 else math.inf


def sdof_free(m: float, k: float, c: float = 0.0) -> dict[str, PhysicsResult]:
    """Free vibration parameters: ωn, fn, ζ, ωd, Q."""
    s = SDOF(m, c, k)
    out = {
        "wn": PhysicsResult("natural_circular_freq", s.wn, "rad/s", "ωn = √(k/m)", "analytic"),
        "fn": PhysicsResult("natural_freq", s.fn, "Hz", "fn = ωn/2π", "analytic"),
        "zeta": PhysicsResult("damping_ratio", s.zeta, "dimensionless",
                              "ζ = c/2√(km)", "analytic", ["linear viscous damping"]),
    }
    if s.zeta < 1:
        out["wd"] = PhysicsResult("damped_freq", s.wd, "rad/s", "ωd = ωn√(1−ζ²)", "analytic")
    out["Q"] = PhysicsResult("Q_factor", s.Q, "dimensionless", "Q ≈ 1/2ζ", "analytic")
    return out


def magnification(r: float, zeta: float) -> PhysicsResult:
    """Receptance magnification M = 1/sqrt((1−r²)² + (2ζr)²)."""
    M = 1.0 / math.sqrt((1 - r**2) ** 2 + (2 * zeta * r) ** 2)
    return PhysicsResult("magnification", M, "dimensionless",
                         "M = 1/√((1−r²)²+(2ζr)²)", "analytic",
                         ["harmonic excitation", "steady state"])


def transmissibility(r: float, zeta: float) -> PhysicsResult:
    """Force/displacement transmissibility T(r, ζ)."""
    T = math.sqrt(1 + (2 * zeta * r) ** 2) / math.sqrt((1 - r**2) ** 2 + (2 * zeta * r) ** 2)
    return PhysicsResult("transmissibility", T, "dimensionless",
                         "T = √(1+(2ζr)²)/√((1−r²)²+(2ζr)²)", "analytic")


def frequency_response(m: float, c: float, k: float, freqs_hz: np.ndarray,
                       F0: float = 1.0) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Receptance FRF: returns (freqs, |X| [m], phase [deg]) for force amplitude F0."""
    w = 2 * math.pi * np.asarray(freqs_hz, float)
    H = (F0 / k) / (1 - (w / math.sqrt(k / m)) ** 2 + 1j * 2 * (c / (2 * math.sqrt(k * m))) * w / math.sqrt(k / m))
    return np.asarray(freqs_hz, float), np.abs(H), np.angle(H, deg=True)


def resonance_assessment(fn_hz: float, fexc_hz: float, zeta: float = 0.02) -> dict:
    """Structured near-resonance discussion (frequency margin, amplification, caveats).

    Implements the §23 worked reasoning: proximity is necessary, not sufficient.
    """
    r = fexc_hz / fn_hz
    M = 1.0 / math.sqrt((1 - r**2) ** 2 + (2 * zeta * r) ** 2)
    margin_pct = abs(fn_hz - fexc_hz) / fn_hz * 100.0
    risk = "HIGH" if margin_pct < 5 else ("MODERATE" if margin_pct < 15 else "LOW")
    return {
        "frequency_ratio": r, "separation_margin_pct": margin_pct,
        "steady_state_magnification": M, "risk": risk,
        "conditions_for_true_resonance": [
            "excitation projects onto the mode (participation/direction)",
            "low damping at that mode (measured ζ, not assumed)",
            "sustained dwell near the peak (not a fast sweep)",
            "linear regime (no contact/gap stiffening shifting fn)",
            "frequency certainty: BC, preload, temperature & unit-to-unit scatter",
        ],
        "recommended_actions": [
            "harmonic/response analysis with realistic damping",
            "frequency separation redesign (stiffness/mass tuning) if margin < 10–15%",
            "experimental modal validation if safety-critical",
        ],
    }


def mdof_modal(K: np.ndarray, M: np.ndarray) -> dict:
    """Undamped MDOF modes: frequencies + mass-normalized shapes."""
    res = generalized_eigen(K, M)
    return {"freqs_hz": res.natural_freq_hz, "shapes": res.eigenvectors,
            "eigenvalues": res.eigenvalues}


def log_decrement_zeta(delta: float) -> PhysicsResult:
    """Damping ratio from log decrement δ: ζ = δ/√(4π²+δ²)."""
    z = delta / math.sqrt(4 * math.pi**2 + delta**2)
    return PhysicsResult("damping_ratio", z, "dimensionless",
                         "ζ = δ/√(4π²+δ²)", "analytic", ["single dominant mode"])


def campbell_critical_speeds(fn0_hz: float, n_modes: int = 1) -> list[float]:
    """Rigid-rotor estimate: critical ≈ undamped natural frequencies (1× line).

    Placeholder-grade estimator with explicit limits — full rotor dynamics
    (gyroscopics, bearings) is roadmap v0.3; included so the API shape is fixed.
    """
    return [fn0_hz * (i + 1) for i in range(n_modes)]


def free_decay_response(m: float, c: float, k: float, x0: float = 1.0,
                        t_end: float | None = None, n: int = 2000):
    """Numeric free-decay via solve_ivp (cross-check for analytic ωd)."""
    s = SDOF(m, c, k)
    T = 1.0 / s.fn
    t_end = t_end or 10 * T
    return solve_sdof(m, c, k, None, t_end, n, x0=x0, v0=0.0)
