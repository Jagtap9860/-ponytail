"""Round 1 (hunt) → Round 2 (cross-examination) → Round 3 (verdict + ego board)."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from physics_agent.council import checks as C
from physics_agent.council.findings import (
    SEV_POINTS,
    Challenge,
    Finding,
    median_severity,
)
from physics_agent.council.personas import PERSONAS, RIVALS, rival_vote


@dataclass
class Verdict:
    """Session outcome: findings, scoreboard, awards, transcript."""
    findings: list[Finding]
    scoreboard: dict[str, int]
    awards: dict[str, str]
    log: list[str] = field(default_factory=list)
    llm_advisory: str = ""

    @property
    def confirmed(self) -> list[Finding]:
        """Findings whose status is confirmed."""
        return [f for f in self.findings if f.status == "confirmed"]

    def open_at(self, severity: str) -> list[Finding]:
        """Confirmed findings at or above a severity."""
        order = ["low", "medium", "high", "critical"]
        return [f for f in self.confirmed
                if order.index(f.final_severity) >= order.index(severity)]


def _run_checks(checks: list[tuple[str, Callable[[], list[Finding]]]] | None = None) -> list[Finding]:
    out: list[Finding] = []
    for persona, fn in (checks if checks is not None else C.CHECKS):
        try:
            found = fn()
        except Exception as e:  # noqa: BLE001 - a crashing check is itself evidence
            found = [Finding(f"{persona.upper()}-XX", persona, "high",
                             f"Check battery crashed: {fn.__name__}",
                             "council/checks.py", repr(e), lambda: True, False)]
        out.extend(found)
    return out


def _cross_examine(f: Finding, log: list[str]) -> None:
    """Round 2: rivals independently re-run the reproduction and vote severity."""
    votes = [f.severity]
    for rival in RIVALS[f.persona]:
        try:
            reproduced = bool(f.recheck()) if f.recheck else True
        except Exception as e:  # noqa: BLE001
            reproduced, err = False, f" (recheck crashed: {e!r})"
        else:
            err = ""
        vote, remark = rival_vote(rival, f.severity, f.user_facing)
        votes.append(vote)
        f.challenges.append(Challenge(rival, reproduced, vote, remark))
        log.append(f"  {PERSONAS[rival].name} → {f.id}: "
                   f"reproduced={reproduced}{err}; severity vote={vote} ({remark})")
        if not reproduced:
            f.status = "refuted"
            log.append(f"  ☠ {f.id} REFUTED by {PERSONAS[rival].name} — "
                       f"{PERSONAS[f.persona].name} filed a ghost.")
            return
    f.status = "confirmed"
    f.final_severity = median_severity(votes)
    if len(set(votes)) > 1:
        log.append(f"  ⚖ {f.id}: severity {votes} → median {f.final_severity} (dissent recorded)")


def _score(findings: list[Finding]) -> dict[str, int]:
    board = {k: 0 for k in PERSONAS}
    for f in findings:
        if f.status == "confirmed":
            board[f.persona] += SEV_POINTS[f.final_severity]
        elif f.status == "refuted":
            board[f.persona] -= 2
            for c in f.challenges:
                if not c.reproduced:
                    board[c.rival] += 3
                    break
    return board


def _awards(findings: list[Finding], board: dict[str, int]) -> dict[str, str]:
    confirmed = [f for f in findings if f.status == "confirmed"]
    refuted = [f for f in findings if f.status == "refuted"]
    top = max(board, key=board.get)
    awards = {"Sharpest Blade": f"{PERSONAS[top].name} ({board[top]} ego pts)"}
    if refuted:
        worst = max(set(PERSONAS) - {None}, key=lambda p: sum(1 for f in refuted if f.persona == p))
        awards["Glass Jaw"] = f"{PERSONAS[worst].name} ({sum(1 for f in refuted if f.persona == worst)} ghosts filed)"
    else:
        awards["Glass Jaw"] = "nobody — no ghosts filed this session"
    crit = [f for f in confirmed if f.final_severity == "critical"]
    awards["State of the code"] = ("ON FIRE 🔥" if crit else
                                   "bruised but standing" if confirmed else "clean — suspiciously clean")
    return awards


def run_council(checks: list[tuple[str, Callable[[], list[Finding]]]] | None = None,
                llm_advisory: bool = False) -> Verdict:
    """Full three-round session. Set checks=... in tests to inject synthetic batteries."""
    log = ["ROUND 1 — THE HUNT"]
    findings = _run_checks(checks)
    for f in findings:
        log.append(f"  [{f.severity.upper()}] {f.id} ({PERSONAS[f.persona].name}): "
                   f"{f.title} @ {f.location}")
    if not findings:
        log.append("  ...silence. No findings. The Council is disappointed in the code's obedience.")
    log.append("ROUND 2 — CROSS-EXAMINATION")
    for f in findings:
        _cross_examine(f, log)
    log.append("ROUND 3 — VERDICT")
    board = _score(findings)
    awards = _awards(findings, board)
    for name, pts in sorted(board.items(), key=lambda kv: -kv[1]):
        log.append(f"  {PERSONAS[name].name}: {pts} pts")
    advisory = _llm_pass(findings) if llm_advisory else ""
    return Verdict(findings, board, awards, log, advisory)


def _llm_pass(findings: list[Finding]) -> str:
    from physics_agent.llm import provider_from_env
    from physics_agent.llm.base import Message
    from physics_agent.llm.echo import EchoProvider
    provider = provider_from_env()
    if isinstance(provider, EchoProvider):
        return "(LLM advisory skipped — offline echo provider. Set PHYSICS_AGENT_LLM_PROVIDER=openai_compatible for a qualitative pass.)"
    summary = "\n".join(f"- [{f.final_severity}] {f.id}: {f.title} @ {f.location}" for f in findings) or "(none)"
    try:
        return provider.complete([Message(
            "system", "You advise a hostile code-review council. List ADDITIONAL suspected "
                      "issues (not repeats) in a physics-agent Python repo, with file guesses. "
                      "Be terse. Never invent test results."),
            Message("user", f"Confirmed findings so far:\n{summary}\n\nWhat else smells?")])
    except Exception as e:  # noqa: BLE001
        return f"(LLM advisory failed: {e})"
