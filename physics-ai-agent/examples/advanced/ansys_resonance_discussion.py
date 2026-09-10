"""Advanced: near-resonance triage (215 Hz excitation vs 217 Hz mode)."""
from physics_agent.agent.orchestrator import Orchestrator

print(Orchestrator(level=3, mode="engineering").solve(
    "My ANSYS modal analysis shows a natural frequency of 217 Hz while my "
    "operating excitation is 215 Hz. What does this mean?").report())
