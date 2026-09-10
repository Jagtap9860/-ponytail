"""Deterministic solvers: symbolic, numeric, ODE, eigen, spectral."""
from physics_agent.solvers.symbolic import rearrange, solve_symbolic
from physics_agent.solvers.numerical import find_root, integrate, differentiate, fit_curve
from physics_agent.solvers.ode import solve_sdof, solve_ivp_system
from physics_agent.solvers.eigenvalue import generalized_eigen, modal_analysis
from physics_agent.solvers.spectral import fft_spectrum

__all__ = [
    "rearrange", "solve_symbolic", "find_root", "integrate", "differentiate",
    "fit_curve", "solve_sdof", "solve_ivp_system", "modal_analysis",
    "generalized_eigen", "fft_spectrum",
]
