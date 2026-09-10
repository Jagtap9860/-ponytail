"""Verdict rendering (markdown / plain text)."""
from __future__ import annotations

from physics_agent.council.debate import Verdict
from physics_agent.council.personas import PERSONAS


def render_markdown(v: Verdict) -> str:
    """Render the verdict as markdown."""
    L: list[str] = ["# Council Verdict", ""]
    L.append(f"Confirmed: **{len(v.confirmed)}** · "
             f"Refuted: **{sum(1 for f in v.findings if f.status == 'refuted')}** · "
             f"Criticals open: **{len(v.open_at('critical'))}**")
    L.append("")
    L.append("## Scoreboard (ego points)")
    for name, pts in sorted(v.scoreboard.items(), key=lambda kv: -kv[1]):
        L.append(f"- {PERSONAS[name].name} ({PERSONAS[name].title}): **{pts}**")
    L.append("")
    L.append("## Awards")
    for award, who in v.awards.items():
        L.append(f"- **{award}**: {who}")
    if v.confirmed:
        L.append("")
        L.append("## Required actions")
        order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        for f in sorted(v.confirmed, key=lambda f: order[f.final_severity]):
            L.append(f"### [{f.final_severity.upper()}] {f.id} — {f.title}")
            L.append(f"- Filed by: {PERSONAS[f.persona].name} (claimed {f.severity})")
            L.append(f"- Location: `{f.location}`")
            L.append(f"- Evidence: {f.evidence}")
            for c in f.challenges:
                L.append(f"- Cross-exam ({PERSONAS[c.rival].name}): reproduced={c.reproduced}, "
                         f"vote={c.severity_vote} — _{c.remark}_")
    else:
        L.append("")
        L.append("No confirmed findings. The Council sharpens its knives for next time.")
    L.append("")
    L.append("## Transcript")
    L.append("```")
    L.extend(v.log)
    L.append("```")
    if v.llm_advisory:
        L.append("")
        L.append("## LLM advisory (unverified)")
        L.append(v.llm_advisory)
    return "\n".join(L) + "\n"


def render_text(v: Verdict) -> str:
    """Render the verdict as plain text."""
    md = render_markdown(v)
    return (md.replace("# ", "").replace("## ", "").replace("### ", "")
              .replace("**", "").replace("`", ""))
