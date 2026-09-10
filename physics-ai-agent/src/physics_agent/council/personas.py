"""The five Council members: egos, expertise, roasts."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Persona:
    """A Council member: ego, hunting grounds, roast."""
    key: str
    name: str
    title: str
    ego: str
    hunts: str
    roast: str  # what they say about the other members' craft


PERSONAS: dict[str, Persona] = {
    p.key: p for p in [
        Persona("vex", "Dr. Vex", "Theoretical Physicist",
                "If the physics is wrong, nothing else matters.",
                "wrong equations, bad constants, dimensional lies",
                "Merge polishes docstrings while the physics predicts perpetual motion. Priorities, Major."),
        Persona("null", "Prof. Null", "Numerical Analyst",
                "It converges? Prove it. On MY grid.",
                "instability, tolerance fraud, FFT sins",
                "Vex derives in a vacuum; I compute in floating point, where his beautiful equations go to die."),
        Persona("merge", "Major Merge", "Software Engineer",
                "Untyped, undocumented, unpackaged = a toy, not a product.",
                "packaging, typing, error handling, dead code",
                "Chaos breaks things. I prevent them from ever compiling broken. Prevention beats heroics."),
        Persona("chaos", "Agent Chaos", "Adversarial Tester",
                "I break things for breakfast.",
                "crashes, garbage input, silent wrong answers",
                "Nia checks that the README runs. I check what happens when the USER can't read. Guess who finds more?"),
        Persona("nia", "Scribe Nia", "Docs & Honesty Auditor",
                "Docs lie. I catch them, with receipts.",
                "README fraud, phantom features, missing LICENSE",
                "Four geniuses, and I'm the only one who noticed the box says MIT but contains no license. Receipts."),
    ]
}

# Round-2 rival assignment (deliberately spicy pairings).
RIVALS: dict[str, tuple[str, str]] = {
    "vex": ("null", "chaos"),     # Null re-derives numerically; Chaos feeds garbage to the equations
    "null": ("vex", "merge"),     # Vex checks analytic limits; Merge checks the code is even sane
    "merge": ("chaos", "nia"),    # Chaos breaks the packaging; Nia checks the claims
    "chaos": ("merge", "vex"),    # Merge: 'that's not a bug, it's my error path'; Vex: 'your input is unphysical'
    "nia": ("merge", "null"),     # Merge defends the code; Null demands numerical receipts
}

# Deterministic rival severity biases (the ego in the vote).
def rival_vote(rival: str, author_claim: str, user_facing: bool) -> tuple[str, str]:
    """Return (vote, remark). Rivals are skeptical by charter."""
    order = ["low", "medium", "high", "critical"]
    i = order.index(author_claim)
    down = order[max(0, i - 1)]
    if rival == "chaos":
        # Chaos upgrades anything a user can trip over, downgrades the rest.
        return (author_claim if user_facing else down,
                "user can trip on it — stands" if user_facing else "no user impact — downgraded")
    if rival == "merge":
        return (down, "works as coded; severity inflated") if i > 0 else ("low", "nit, at best")
    if rival == "nia":
        return (author_claim, "claim-vs-reality gap matters") if user_facing else (down, "internal detail")
    if rival == "null":
        return (author_claim, "numbers don't lie") if author_claim in ("critical", "high") else (down, "within tolerance")
    # vex
    return (author_claim, "physics is physics") if user_facing else (down, "engineering trivia")
