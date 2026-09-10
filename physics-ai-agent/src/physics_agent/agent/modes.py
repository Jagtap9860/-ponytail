"""Explanation levels (1–4) and interaction modes (spec §3–§4)."""
from __future__ import annotations

LEVELS = {
    1: "Beginner — basic math, intuition first, minimal jargon.",
    2: "Engineering undergraduate — standard university physics/engineering math.",
    3: "Advanced — ODEs, linear algebra, tensors, continuum formulations.",
    4: "Research — full formulation, approximations, literature terminology.",
}

MODES = {
    "direct": "Solve directly, concise but complete.",
    "guided": "Socratic: ask one focused question at a time, then continue.",
    "teaching": "Explain each step pedagogically with checkpoints.",
    "exam": "Hints only — never reveal the solution; probe understanding.",
    "research": "Derivation-heavy, assumptions and limits foregrounded.",
    "engineering": "Design-oriented: margins, standards language, validation reminders.",
}

DISCLAIMER_SAFETY = (
    "Safety note: simulation/analysis results for safety-critical decisions must be "
    "validated against applicable standards, experiments, or qualified review."
)


def level_guidance(level: int) -> str:
    return LEVELS.get(level, LEVELS[2])


def mode_guidance(mode: str) -> str:
    return MODES.get(mode, MODES["direct"])
