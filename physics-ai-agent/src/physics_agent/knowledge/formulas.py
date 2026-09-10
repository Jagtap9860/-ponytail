"""Structured formula database: load, search, retrieve with metadata."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Variable:
    meaning: str = ""
    si_unit: str = ""


@dataclass(frozen=True)
class Formula:
    name: str
    equation: str
    domain: str
    variables: dict[str, Variable] = field(default_factory=dict)
    assumptions: tuple[str, ...] = ()
    validity: str = ""
    derivation: str = ""
    related: tuple[str, ...] = ()
    mistakes: tuple[str, ...] = ()
    applications: tuple[str, ...] = ()
    difficulty: int = 1
    keywords: tuple[str, ...] = ()
    source: str = ""

    def describe(self) -> str:
        lines = [f"{self.name}: {self.equation}  [{self.domain}]"]
        for sym, var in self.variables.items():
            lines.append(f"  {sym}: {var.meaning} [{var.si_unit}]")
        if self.assumptions:
            lines.append("  assumes: " + "; ".join(self.assumptions))
        if self.validity:
            lines.append(f"  valid: {self.validity}")
        if self.mistakes:
            lines.append("  watch out: " + "; ".join(self.mistakes))
        return "\n".join(lines)


def _data_dirs() -> list[Path]:
    here = Path(__file__).resolve()
    return [
        here.parents[3] / "data" / "formulas",
        here.parents[1] / "data" / "formulas",
    ]


def _load() -> dict[str, Formula]:
    out: dict[str, Formula] = {}
    for d in _data_dirs():
        if not d.exists():
            continue
        for f in sorted(d.glob("*.json")):
            rows = json.loads(f.read_text(encoding="utf-8"))
            for row in rows:
                vars_ = {k: Variable(**v) for k, v in row.get("variables", {}).items()}
                out[row["name"]] = Formula(
                    name=row["name"], equation=row["equation"], domain=row["domain"],
                    variables=vars_, assumptions=tuple(row.get("assumptions", [])),
                    validity=row.get("validity", ""), derivation=row.get("derivation", ""),
                    related=tuple(row.get("related", [])), mistakes=tuple(row.get("mistakes", [])),
                    applications=tuple(row.get("applications", [])),
                    difficulty=int(row.get("difficulty", 1)),
                    keywords=tuple(row.get("keywords", [])), source=row.get("source", ""),
                )
    return out


FORMULAS: dict[str, Formula] = _load()


def lookup_formula(name: str) -> Formula:
    if name in FORMULAS:
        return FORMULAS[name]
    low = name.lower()
    for key in FORMULAS:
        if key.lower() == low:
            return FORMULAS[key]
    raise KeyError(f"Unknown formula '{name}'. Use search_formulas() to browse.")


def search_formulas(query: str, domain: str | None = None, limit: int = 10) -> list[Formula]:
    """Keyword search over names, equations, keywords, applications."""
    q = query.lower()
    scored: list[tuple[int, Formula]] = []
    for f in FORMULAS.values():
        if domain and f.domain != domain:
            continue
        hay = " ".join([f.name, f.equation, f.domain, *f.keywords, *f.applications]).lower()
        score = sum(2 if tok in f.name.lower() else 1 for tok in q.split() if tok in hay)
        if score:
            scored.append((score, f))
    scored.sort(key=lambda t: -t[0])
    return [f for _, f in scored[:limit]]
