"""ODE solvers: general systems + specialized SDOF vibration response."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp


@dataclass
class ODEResult:
    """ODE solution: time grid, state history, success flag."""
    t: np.ndarray
    y: np.ndarray  # shape (n_states, n_times)
    success: bool
    message: str


def solve_ivp_system(
    fun: Callable[[float, np.ndarray], np.ndarray],
    t_span: tuple[float, float],
    y0: np.ndarray,
    t_eval: np.ndarray | None = None,
    method: str = "RK45",
    rtol: float = 1e-9,
    atol: float = 1e-12,
) -> ODEResult:
    """General first-order system via solve_ivp."""
    sol = solve_ivp(np.asarray(fun) if False else fun, t_span, np.asarray(y0, dtype=float),
                    t_eval=t_eval, method=method, rtol=rtol, atol=atol)
    return ODEResult(t=sol.t, y=sol.y, success=bool(sol.success), message=str(sol.message))


def solve_sdof(
    m: float, c: float, k: float,
    force: Callable[[float], float] | None = None,
    t_end: float = 5.0, n: int = 2000,
    x0: float = 0.0, v0: float = 0.0,
) -> ODEResult:
    """Time response of m x'' + c x' + k x = F(t)."""
    f = force or (lambda t: 0.0)

    def rhs(t: float, y: np.ndarray) -> np.ndarray:
        """Rhs.
        
        Args:
            t: float
            y: np.ndarray
        
        Returns:
            np.ndarray"""
        x, v = y
        return np.array([v, (f(t) - c * v - k * x) / m])

    t = np.linspace(0.0, t_end, n)
    return solve_ivp_system(rhs, (0.0, t_end), np.array([x0, v0]), t_eval=t)
