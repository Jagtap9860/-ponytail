"""Concept notes + FEA knowledge base (RAG-ready metadata).

Each concept: topic/subtopic/equation/explanation/assumptions/source/
difficulty/keywords/related. The FEA section teaches analysis physics
(modal, prestressed-modal, harmonic, transient, buckling, contact,
nonlinearity, convergence, singularities) rather than replacing
commercial software.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Concept:
    """RAG-ready concept note with topic, equation, source, difficulty."""
    topic: str
    subtopic: str
    equation: str = ""
    explanation: str = ""
    assumptions: tuple[str, ...] = ()
    source: str = "general physics knowledge"
    difficulty: int = 1
    keywords: tuple[str, ...] = ()
    related: tuple[str, ...] = ()


CONCEPTS: dict[str, Concept] = {}


def _c(key: str, **kw: object) -> None:
    CONCEPTS[key] = Concept(**kw)  # type: ignore[arg-type]


_c("newton_laws", topic="Classical Mechanics", subtopic="Newton's laws",
   equation="ΣF = m·a;  F₁₂ = −F₂₁",
   explanation=("First: inertia in inertial frames. Second: net force equals mass times "
                "acceleration of the mass centre. Third: interaction pairs are equal/opposite."),
   assumptions=("classical regime v≪c", "inertial reference frame", "point mass or rigid body"),
   difficulty=1, keywords=("force", "inertia", "action-reaction"),
   related=("momentum", "work_energy"))

_c("resonance", topic="Vibrations", subtopic="Resonance",
   equation="r = ω/ωn;  X/(F0/k) = 1/sqrt((1−r²)² + (2ζr)²)",
   explanation=("Large steady-state response when excitation frequency approaches a natural "
                "frequency AND the mode is excitable (force projects onto the mode shape), "
                "damping is low, and the excitation persists. Frequency proximity alone is "
                "necessary but not sufficient: check mode participation, excitation direction, "
                "damping, dwell time, and frequency uncertainty (manufacturing/BC scatter). "
                "Near resonance (e.g. 215 Hz excitation vs 217 Hz mode) demands a frequency-"
                "separation margin assessment, damping estimate, and response (harmonic) "
                "analysis — not just a modal list."),
   assumptions=("linear system", "harmonic excitation", "light damping for sharp peak"),
   difficulty=2, keywords=("natural frequency", "damping", "amplification", "modal", "harmonic"),
   related=("damping_ratio", "frf", "fea_modal"))

_c("damping_ratio", topic="Vibrations", subtopic="Damping ratio",
   equation="ζ = c/(2·sqrt(k·m)) = c/cc",
   explanation=("ζ<1 underdamped (oscillates), ζ=1 critical, ζ>1 overdamped. The damped "
                "natural frequency is ωd = ωn·sqrt(1−ζ²). Q factor ≈ 1/(2ζ)."),
   assumptions=("linear viscous damping",), difficulty=1,
   keywords=("damping", "zeta", "Q factor", "log decrement"), related=("resonance",))

_c("fea_modal", topic="FEA", subtopic="Modal analysis",
   equation="[K]{φ} = λ[M]{φ},  λ = ω²",
   explanation=("Undamped free-vibration eigenproblem. Natural frequencies and mass-"
                "normalized mode shapes; no loads needed. Prestressed modal adds stress-"
                "stiffening [Kσ] (spin, bolt preload, pressure). Validate with mass "
                "participation, mesh convergence, and BC realism — a mode list without "
                "participation factors cannot judge resonance risk."),
   assumptions=("linear elasticity", "small deflections", "consistent mass/stiffness"),
   difficulty=3, keywords=("eigenvalue", "mode shape", "participation", "prestress"),
   related=("resonance", "fea_harmonic", "fea_convergence"))

_c("fea_harmonic", topic="FEA", subtopic="Harmonic / frequency response",
   equation="([K] − ω²[M] + iω[C]){u} = {F}",
   explanation=("Steady-state response to sinusoidal loads vs frequency. Needs damping "
                "model (Rayleigh/modal/structural), sufficient frequency resolution near "
                "peaks, and mode-superposition truncation checks (residual vectors)."),
   assumptions=("linearity", "harmonic load", "known damping"), difficulty=3,
   keywords=("FRF", "Bode", "transmissibility", "damping"), related=("fea_modal", "resonance"))

_c("fea_convergence", topic="FEA", subtopic="Mesh convergence & singularities",
   explanation=("Refine until quantities of interest (frequencies, far-field stress, "
                "reactions) change < tolerance. Stress at sharp re-entrant corners, point "
                "loads/BCs is singular — it diverges with refinement; assess with "
                "submodelling, fillets, or fracture mechanics, and never converge on a "
                "singular peak. Check element quality (Jacobian, aspect ratio, warpage)."),
   assumptions=("correct BCs", "verified material model"), difficulty=3,
   keywords=("mesh", "convergence", "singularity", "element quality"), related=("fea_modal",))

_c("navier_stokes", topic="Fluid Mechanics", subtopic="Navier-Stokes",
   equation="ρ(∂u/∂t + u·∇u) = −∇p + μ∇²u + f;  ∇·u = 0 (incompressible)",
   explanation=("Momentum + continuity for a Newtonian fluid. Nonlinearity (u·∇u) drives "
                "turbulence; Reynolds number sets the regime. Bernoulli follows only for "
                "steady, incompressible, inviscid flow along a streamline."),
   assumptions=("continuum", "Newtonian fluid"), difficulty=3,
   keywords=("CFD", "Reynolds", "Bernoulli", "turbulence"), related=("bernoulli",))

_c("maxwell", topic="Electromagnetism", subtopic="Maxwell equations",
   equation="∇·E=ρ/ε₀; ∇·B=0; ∇×E=−∂B/∂t; ∇×B=μ₀J+μ₀ε₀∂E/∂t",
   explanation=("Complete classical EM: Gauss (E/B), Faraday, Ampère–Maxwell. In vacuum "
                "they yield waves at c = 1/sqrt(μ₀ε₀). Choose integral vs differential "
                "form by symmetry; statics decouples E and B."),
   assumptions=("classical fields", "macroscopic media need D/H forms"), difficulty=2,
   keywords=("EM waves", "Faraday", "Ampere", "Gauss"), related=("lorentz_force",))

_c("schrodinger", topic="Quantum Mechanics", subtopic="Schrödinger equation",
   equation="iℏ∂ψ/∂t = Ĥψ;  Ĥ = −ℏ²/2m ∇² + V",
   explanation=("Non-relativistic evolution of the wavefunction; |ψ|² is probability "
                "density. Time-independent form Ĥψ=Eψ gives stationary states "
                "(particle in a box, harmonic oscillator, hydrogen)."),
   assumptions=("non-relativistic", "single particle, no spin DST"), difficulty=3,
   keywords=("wavefunction", "quantization", "particle in a box"), related=("uncertainty",))

_c("uncertainty", topic="Quantum Mechanics", subtopic="Uncertainty principle",
   equation="Δx·Δp ≥ ℏ/2;  ΔE·Δt ≥ ℏ/2",
   explanation=("Fourier-conjugate observables cannot both be sharp; a spread theorem, "
                "not a measurement defect."),
   assumptions=("standard QM postulates",), difficulty=2,
   keywords=("Heisenberg", "standard deviation"), related=("schrodinger",))

_c("relativity_energy", topic="Relativity", subtopic="Mass–energy",
   equation="E² = (pc)² + (mc²)²;  γ = 1/sqrt(1−v²/c²)",
   explanation=("Invariant rest energy plus kinetic. At v≪c, E ≈ mc² + ½mv²; massless "
                "particles have E = pc. Simultaneity/length/time are frame-dependent; "
                "the interval and rest mass are invariant."),
   assumptions=("inertial frames (special relativity)",), difficulty=2,
   keywords=("gamma", "time dilation", "Lorentz"), related=("time_dilation",))


def lookup_concept(key: str) -> Concept:
    """Fetch a concept note by key."""
    return CONCEPTS[key]


def search_concepts(query: str, limit: int = 8) -> list[Concept]:
    """Keyword search over concept notes."""
    q = query.lower()
    scored = []
    for c in CONCEPTS.values():
        hay = " ".join([c.topic, c.subtopic, c.equation, c.explanation, *c.keywords]).lower()
        s = sum(1 for tok in q.split() if tok in hay)
        if s:
            scored.append((s, c))
    scored.sort(key=lambda t: -t[0])
    return [c for _, c in scored[:limit]]
