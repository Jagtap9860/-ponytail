"""Base types + domain registry for physics modules (SI in / SI out)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


PROVENANCE = (
    "GENERAL PHYSICS KNOWLEDGE",
    "USER-PROVIDED",
    "EXTERNAL REFERENCE",
    "COMPUTED",
    "ASSUMPTION",
    "APPROXIMATION",
    "NEEDS EXPERIMENTAL VALIDATION",
)


@dataclass
class PhysicsResult:
    """Standard result envelope for every physics solver."""

    name: str
    value: Any                       # float, ndarray, or dict of floats
    unit: str                        # SI unit string
    symbolic: str = ""               # governing equation used
    method: str = ""                 # analytic / numeric / ...
    assumptions: list[str] = field(default_factory=list)
    verification: list[str] = field(default_factory=list)
    provenance: str = "COMPUTED"

    def scalar(self) -> float:
        """Return the value as a float."""
        return float(self.value)

    def __str__(self) -> str:
        v = self.value if not isinstance(self.value, float) else f"{self.value:.6g}"
        return f"{self.name} = {v} {self.unit}  [{self.symbolic}]"


@dataclass
class DomainModule:
    """Registered physics domain: key, title, keywords, description."""
    key: str
    title: str
    keywords: tuple[str, ...]
    description: str = ""


_REGISTRY: dict[str, DomainModule] = {}


def register_domain(key: str, title: str, keywords: tuple[str, ...], description: str = "") -> None:
    """Register a physics domain for classification and discovery."""
    _REGISTRY[key] = DomainModule(key, title, keywords, description)


def domains() -> dict[str, DomainModule]:
    """Return the domain registry (copy)."""
    return dict(_REGISTRY)


def require_positive(**kw: float) -> None:
    """Raise ValueError unless every named value is positive."""
    bad = {k: v for k, v in kw.items() if not v > 0}
    if bad:
        raise ValueError(f"Must be positive: {bad}.")
