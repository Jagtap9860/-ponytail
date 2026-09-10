"""Numerical methods via NumPy/SciPy: roots, quadrature, derivatives, fits, FFT helpers."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
from scipy import integrate as _integrate
from scipy import optimize as _optimize


@dataclass
class RootResult:
    """Bracketed-root result: root, iterations, convergence, residual."""
    root: float
    iterations: int
    converged: bool
    residual: float


def find_root(f: Callable[[float], float], a: float, b: float) -> RootResult:
    """Bracketed root find (Brent). Requires sign change on [a, b]."""
    sol = _optimize.root_scalar(f, bracket=(a, b), method="brentq")
    return RootResult(float(sol.root), int(sol.iterations), bool(sol.converged), float(abs(f(sol.root))))


def find_minimum(f: Callable[[float], float], a: float, b: float) -> tuple[float, float]:
    """Bounded scalar minimization. Returns (x_min, f_min)."""
    sol = _optimize.minimize_scalar(f, bounds=(a, b), method="bounded")
    return float(sol.x), float(sol.fun)


def integrate(f: Callable[[float], float], a: float, b: float) -> tuple[float, float]:
    """Adaptive quadrature. Returns (value, estimated error)."""
    val, err = _integrate.quad(f, a, b)
    return float(val), float(err)


def differentiate(f: Callable[[float], float], x: float, h: float = 1e-6) -> float:
    """Central difference, O(h^2). For exact work use solvers.symbolic.differentiate."""
    return float((f(x + h) - f(x - h)) / (2.0 * h))


def fit_curve(
    model: Callable[..., float],
    xdata: np.ndarray,
    ydata: np.ndarray,
    p0: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Nonlinear least squares. Returns (popt, perr)."""
    from scipy.optimize import curve_fit

    popt, pcov = curve_fit(model, np.asarray(xdata), np.asarray(ydata), p0=p0)
    return np.asarray(popt), np.sqrt(np.diag(pcov))


def interpolate(x: np.ndarray, y: np.ndarray, kind: str = "cubic") -> Callable[[np.ndarray], np.ndarray]:
    """1-D interpolating function (extrapolates outside range)."""
    from scipy.interpolate import interp1d

    return interp1d(np.asarray(x), np.asarray(y), kind=kind, fill_value="extrapolate")  # type: ignore[return-value]
