"""Optics, waves, sound/acoustics."""
from __future__ import annotations

import math

from physics_agent.knowledge.constants import get_constant
from physics_agent.physics.base import PhysicsResult, require_positive

C = get_constant("c").value


def snell(n1: float, theta1_deg: float, n2: float) -> PhysicsResult:
    """Refraction angle (deg from normal); raises on total internal reflection."""
    s = n1 * math.sin(math.radians(theta1_deg)) / n2
    if abs(s) > 1:
        raise ValueError(f"Total internal reflection: sin(θ2)={s:.3f}. No refracted ray.")
    return PhysicsResult("refraction_angle", math.degrees(math.asin(s)), "deg",
                         "n1·sinθ1 = n2·sinθ2", "analytic")


def critical_angle(n_core: float, n_clad: float) -> PhysicsResult:
    """TIR critical angle thc = asin(n_clad/n_core)."""
    if n_core <= n_clad:
        raise ValueError("TIR needs n_core > n_clad.")
    return PhysicsResult("critical_angle", math.degrees(math.asin(n_clad / n_core)), "deg",
                         "θc = asin(n2/n1)", "analytic")


def thin_lens(f: float | None = None, do: float | None = None,
              di: float | None = None) -> PhysicsResult:
    """Solve 1/f = 1/do + 1/di (real-is-positive)."""
    args = {"f": f, "do": do, "di": di}
    if sum(v is None for v in args.values()) != 1:
        raise ValueError("Provide exactly two of f, do, di.")
    if f is None:
        return PhysicsResult("focal_length", 1 / (1 / do + 1 / di), "m", "1/f=1/do+1/di", "analytic")
    if di is None:
        return PhysicsResult("image_distance", 1 / (1 / f - 1 / do), "m", "1/f=1/do+1/di", "analytic")
    return PhysicsResult("object_distance", 1 / (1 / f - 1 / di), "m", "1/f=1/do+1/di", "analytic")


def wave_speed(f: float | None = None, lam: float | None = None,
               v: float | None = None) -> PhysicsResult:
    """Solve v = f*lambda for the missing quantity."""
    args = {"f": f, "lambda": lam, "v": v}
    if sum(x is None for x in args.values()) != 1:
        raise ValueError("Provide exactly two of f, lambda, v.")
    if v is None:
        return PhysicsResult("wave_speed", f * lam, "m/s", "v = fλ", "analytic")
    if f is None:
        return PhysicsResult("frequency", v / lam, "Hz", "f = v/λ", "analytic")
    return PhysicsResult("wavelength", v / f, "m", "λ = v/f", "analytic")


def doppler_sound(f: float, v_sound: float = 343.0, v_obs: float = 0.0,
                  v_src: float = 0.0) -> PhysicsResult:
    """f' = f(v+vo)/(v−vs); +vo toward source, +vs toward observer."""
    require_positive(f=f, v_sound=v_sound)
    if abs(v_src) >= v_sound:
        raise ValueError("Supersonic source: shock regime, Doppler formula invalid.")
    return PhysicsResult("observed_freq", f * (v_sound + v_obs) / (v_sound - v_src), "Hz",
                         "f′ = f(v+vo)/(v−vs)", "analytic", ["subsonic", "stationary medium"])


def sound_pressure_level(p_rms: float, p_ref: float = 20e-6) -> PhysicsResult:
    """SPL = 20*log10(p/p_ref) in dB."""
    require_positive(p_rms=p_rms, p_ref=p_ref)
    return PhysicsResult("spl", 20 * math.log10(p_rms / p_ref), "dB",
                         "SPL = 20log10(p/pref)", "analytic")


def string_modes(L: float, tension: float, mu: float, n: int = 1) -> PhysicsResult:
    """Fixed-fixed string mode n: fn = n/2L·√(T/μ)."""
    require_positive(L=L, tension=tension, mu=mu)
    if n < 1:
        raise ValueError("n >= 1.")
    return PhysicsResult("mode_freq", n / (2 * L) * math.sqrt(tension / mu), "Hz",
                         "fn = n/2L·√(T/μ)", "analytic")
