"""Reference PDE solvers (method-of-lines / finite-difference teaching codes).

Not a CFD/FEA replacement: small, explicit, stability-checked schemes for
the heat and wave equations used in verification and teaching.
"""
from __future__ import annotations

import numpy as np


def heat_equation_explicit(
    L: float = 1.0, T: float = 0.1, nx: int = 51, nt: int = 500,
    alpha: float = 0.01, left: float = 0.0, right: float = 0.0,
    initial: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """1-D heat eq u_t = α u_xx, Dirichlet BCs. Returns (x, t, u[nt×nx]).

    Raises if the explicit stability limit r = α·dt/dx² ≤ 1/2 is violated.
    """
    dx, dt = L / (nx - 1), T / (nt - 1)
    r = alpha * dt / dx**2
    if r > 0.5:
        raise ValueError(f"Unstable: r={r:.3f} > 1/2. Increase nt or decrease T/nx.")
    x = np.linspace(0, L, nx)
    u = np.zeros((nt, nx))
    u[0] = np.sin(np.pi * x / L) if initial is None else np.asarray(initial, float)
    u[:, 0], u[:, -1] = left, right
    for n in range(nt - 1):
        u[n + 1, 1:-1] = u[n, 1:-1] + r * (u[n, 2:] - 2 * u[n, 1:-1] + u[n, :-2])
    return x, np.linspace(0, T, nt), u


def wave_equation_leapfrog(
    L: float = 1.0, T: float = 1.0, nx: int = 101, nt: int = 400,
    c: float = 1.0, initial: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """1-D wave eq u_tt = c² u_xx, fixed ends. Returns (x, t, u).

    Raises if CFL c·dt/dx > 1 is violated.
    """
    dx, dt = L / (nx - 1), T / (nt - 1)
    cfl = c * dt / dx
    if cfl > 1.0:
        raise ValueError(f"CFL violated: {cfl:.3f} > 1.")
    x = np.linspace(0, L, nx)
    u = np.zeros((nt, nx))
    u0 = np.exp(-200 * (x - 0.3 * L) ** 2) if initial is None else np.asarray(initial, float)
    u[0] = u0
    u[1, 1:-1] = u0[1:-1] + 0.5 * cfl**2 * (u0[2:] - 2 * u0[1:-1] + u0[:-2])
    for n in range(1, nt - 1):
        u[n + 1, 1:-1] = (2 * u[n, 1:-1] - u[n - 1, 1:-1]
                          + cfl**2 * (u[n, 2:] - 2 * u[n, 1:-1] + u[n, :-2]))
    return x, np.linspace(0, T, nt), u
