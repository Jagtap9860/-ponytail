"""Linear algebra, optimization, Monte Carlo, sensitivity utilities."""
from __future__ import annotations

from collections.abc import Callable

import numpy as np
import pandas as pd


def linear_solve(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Solve the linear system A*x = b."""
    A, b = np.asarray(A, float), np.asarray(b, float)
    return np.linalg.solve(A, b)


def least_squares(A: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, float]:
    """Least-squares solution and residual of A*x ~= b."""
    x, res, *_ = np.linalg.lstsq(np.asarray(A, float), np.asarray(b, float), rcond=None)
    return x, float(res[0]) if res.size else 0.0


def condition_number(A: np.ndarray) -> float:
    """2-norm condition number of A."""
    return float(np.linalg.cond(np.asarray(A, float)))


def gradient_descent(
    f: Callable[[np.ndarray], float],
    grad: Callable[[np.ndarray], np.ndarray],
    x0: np.ndarray,
    lr: float = 0.1,
    steps: int = 500,
) -> np.ndarray:
    """Fixed-step gradient descent from x0."""
    x = np.asarray(x0, float).copy()
    for _ in range(steps):
        x -= lr * grad(x)
    return x


def monte_carlo_pi(n: int = 200_000, seed: int = 0) -> float:
    """Seeded Monte Carlo estimate of pi."""
    rng = np.random.default_rng(seed)
    p = rng.random((n, 2))
    return float(4.0 * np.mean(np.sum(p**2, axis=1) <= 1.0))


def sensitivity_table(
    f: Callable[..., float], base: dict[str, float], perturbations: dict[str, list[float]]
) -> pd.DataFrame:
    """One-at-a-time sensitivity: vary each param, hold others at base."""
    rows = []
    f0 = f(**base)
    for name, values in perturbations.items():
        for v in values:
            kw = dict(base)
            kw[name] = v
            fv = f(**kw)
            rows.append({"parameter": name, "value": v, "result": fv,
                         "delta_pct": 100.0 * (fv - f0) / f0 if f0 else float("nan")})
    return pd.DataFrame(rows)
