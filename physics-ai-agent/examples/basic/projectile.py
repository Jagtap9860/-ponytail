"""Basic: projectile range + symbolic cross-check."""
from physics_agent.agent.orchestrator import Orchestrator
from physics_agent.solvers.symbolic import solve_symbolic

print(Orchestrator().solve(
    "A projectile is launched at 25 m/s at 40 deg. Find its range.").report())
print(solve_symbolic("R*g - v0**2*sin(2*theta)", "R",
                     g=9.80665, v0=25.0, theta=0.6981317007))
