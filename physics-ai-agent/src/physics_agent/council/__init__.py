"""The Council — adversarial review panel (hunt, cross-examine, verdict)."""
from physics_agent.council.debate import run_council
from physics_agent.council.findings import SEVERITY_ORDER, Finding
from physics_agent.council.personas import PERSONAS

__all__ = ["run_council", "Finding", "SEVERITY_ORDER", "PERSONAS"]
