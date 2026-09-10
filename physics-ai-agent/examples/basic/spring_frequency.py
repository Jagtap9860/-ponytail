"""Basic: SDOF natural frequency of a spring-mass system.

Run:  PYTHONPATH=src python3 examples/basic/spring_frequency.py
"""
from physics_agent.agent.orchestrator import Orchestrator

print(Orchestrator().solve(
    "A 10 kg mass is attached to a spring with k = 500 N/m. Find its natural frequency."
).report())
