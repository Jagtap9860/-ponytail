"""Matplotlib plots (Agg backend — no display needed). File output only."""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def _save(fig: plt.Figure, path: str) -> str:
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return path


def plot_function(expr: str, x_range: tuple[float, float] = (0, 10),
                  path: str = "/tmp/physics_plot.png", title: str = "",
                  xlabel: str = "x", ylabel: str = "y", n: int = 400) -> str:
    """Plot a sympy/NumPy expression of x, e.g. 'sin(x)*exp(-0.1*x)'."""
    import sympy as sp
    x = np.linspace(x_range[0], x_range[1], n)
    f = sp.lambdify(sp.Symbol("x"), sp.sympify(expr), "numpy")
    fig, ax = plt.subplots()
    ax.plot(x, f(x))
    ax.set(xlabel=xlabel, ylabel=ylabel, title=title or expr)
    ax.grid(True, alpha=0.3)
    return _save(fig, path)


def plot_time_response(t: np.ndarray, x: np.ndarray, path: str,
                       title: str = "Time response", ylabel: str = "x [m]") -> str:
    """Plot x(t) to a PNG file."""
    fig, ax = plt.subplots()
    ax.plot(np.asarray(t), np.asarray(x))
    ax.set(xlabel="t [s]", ylabel=ylabel, title=title)
    ax.grid(True, alpha=0.3)
    return _save(fig, path)


def plot_frequency_response(freqs: np.ndarray, mag: np.ndarray, phase: np.ndarray,
                            path: str, title: str = "Frequency response") -> str:
    """Magnitude/phase (Bode-style) plot to a PNG file."""
    fig, (a1, a2) = plt.subplots(2, 1, sharex=True, figsize=(6, 5))
    a1.semilogy(np.asarray(freqs), np.asarray(mag))
    a1.set(ylabel="|X| [m]", title=title)
    a1.grid(True, alpha=0.3, which="both")
    a2.semilogx(np.asarray(freqs), np.asarray(phase))
    a2.set(xlabel="f [Hz]", ylabel="phase [deg]")
    a2.grid(True, alpha=0.3, which="both")
    return _save(fig, path)


def plot_fft_spectrum(freqs: np.ndarray, amp: np.ndarray, path: str,
                      title: str = "Amplitude spectrum") -> str:
    """Stem amplitude-spectrum plot to a PNG file."""
    fig, ax = plt.subplots()
    ax.stem(np.asarray(freqs), np.asarray(amp), basefmt=" ")
    ax.set(xlabel="f [Hz]", ylabel="amplitude", title=title)
    ax.grid(True, alpha=0.3)
    return _save(fig, path)
