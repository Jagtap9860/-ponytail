"""Explanation agent: level/mode-aware rendering of the 13-section report."""
from __future__ import annotations

from physics_agent.agent.modes import DISCLAIMER_SAFETY, level_guidance, mode_guidance


def physical_meaning(domain: str, headline: str) -> str:
    hints = {
        "vibrations": ("Compare fn to excitation: separation margin and damping decide whether "
                       "motion stays small or amplifies toward resonance."),
        "classical_mechanics": "Compare accelerations to g (9.81 m/s²) for intuition.",
        "fluid_mechanics": "Use Re to name the regime (laminar/turbulent) the number implies.",
        "thermodynamics": "Compare efficiencies to the Carnot bound.",
        "relativity": "Quote γ and name the Newtonian vs relativistic regime.",
        "quantum_mechanics": "Compare energies to kT or eV scales; name the classical limit.",
    }
    return f"{headline} {hints.get(domain, 'Sanity-check against familiar scales.')}"


def render_report(sections: dict[str, str], level: int, mode: str,
                  simple: bool = False, safety_critical: bool = False) -> str:
    order_full = ["Problem Understanding", "Given Data", "Required", "Assumptions",
                  "Physical Model", "Governing Principle", "Equation Derivation",
                  "Calculation", "Unit Check", "Verification", "Final Answer",
                  "Physical Interpretation", "Important Notes"]
    order_simple = ["Given Data", "Calculation", "Final Answer", "Physical Interpretation"]
    order = order_simple if simple else order_full
    head = f"_Level {level}: {level_guidance(level)}  ·  Mode: {mode} — {mode_guidance(mode)}_\n"
    parts = [head]
    for i, key in enumerate(order, 1):
        body = sections.get(key, "").strip()
        if body:
            parts.append(f"## {i}. {key}\n{body}")
    if safety_critical:
        parts.append(f"> {DISCLAIMER_SAFETY}")
    return "\n\n".join(parts)
