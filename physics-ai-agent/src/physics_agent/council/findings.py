"""Finding model + severity algebra for the Council."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

SEVERITY_ORDER = ("low", "medium", "high", "critical")
SEV_POINTS = {"low": 1, "medium": 2, "high": 3, "critical": 4}


def median_severity(votes: list[str]) -> str:
    """Median of severity votes (dissent-tolerant)."""
    idx = sorted(SEVERITY_ORDER.index(v) for v in votes)
    return SEVERITY_ORDER[idx[len(idx) // 2]]


@dataclass
class Challenge:
    """One rival cross-examination: recheck, vote, remark."""
    rival: str
    reproduced: bool
    severity_vote: str
    remark: str


@dataclass
class Finding:
    """A filed finding with evidence and a reproduction closure."""
    id: str
    persona: str
    severity: str                  # author claim
    title: str
    location: str
    evidence: str
    recheck: Callable[[], bool] | None = None   # True => still reproduces
    user_facing: bool = False
    status: str = "open"           # open | confirmed | refuted
    final_severity: str = ""
    challenges: list[Challenge] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.severity not in SEVERITY_ORDER:
            raise ValueError(f"bad severity {self.severity}")
        self.final_severity = self.severity
