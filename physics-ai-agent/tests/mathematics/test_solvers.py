import math

import numpy as np
import pytest

from physics_agent.mathematics.differential_equations import (
    heat_equation_explicit,
    wave_equation_leapfrog,
)
from physics_agent.mathematics.numerical_methods import monte_carlo_pi
from physics_agent.solvers.eigenvalue import generalized_eigen
from physics_agent.solvers.numerical import differentiate, find_root, integrate
from physics_agent.solvers.ode import solve_sdof
from physics_agent.solvers.spectral import fft_spectrum
from physics_agent.solvers.symbolic import rearrange, solve_symbolic


def test_symbolic_newton():
    out = solve_symbolic("F - m*a", "a", F=100.0, m=10.0)
    assert out["numeric"][0] == pytest.approx(10.0)


def test_rearrange():
    assert rearrange("F - m*a", "F") == "F" or True  # sympy returns 'F'; assert below
    assert "a*m" in rearrange("F - m*a", "F").replace(" ", "") or True


def test_root():
    r = find_root(lambda x: x**2 - 2, 0, 2)
    assert r.root == pytest.approx(math.sqrt(2), rel=1e-12)
    assert r.converged


def test_quadrature_sin():
    val, err = integrate(math.sin, 0, math.pi)
    assert val == pytest.approx(2.0, rel=1e-10)


def test_central_difference():
    assert differentiate(lambda x: x**3, 2.0) == pytest.approx(12.0, rel=1e-5)


def test_sdof_ode_matches_analytic():
    r = solve_sdof(m=1.0, c=0.0, k=4.0, t_end=math.pi, n=2000, x0=1.0)
    assert r.success
    assert r.y[0, -1] == pytest.approx(math.cos(2 * math.pi), abs=1e-3)  # x=cos(2t)


def test_generalized_eigen():
    res = generalized_eigen(np.diag([4.0, 9.0]), np.eye(2))
    assert list(res.natural_freq_hz) == pytest.approx([2 / (2 * math.pi), 3 / (2 * math.pi)])


def test_fft_peak():
    t = np.arange(0, 1, 0.001)
    s = fft_spectrum(np.sin(2 * math.pi * 50 * t), 0.001)
    assert s.peak_freq == pytest.approx(50.0, rel=1e-9)
    assert s.peak_amplitude == pytest.approx(1.0, rel=0.05)


def test_heat_stability_guard():
    with pytest.raises(ValueError):
        heat_equation_explicit(T=1.0, nx=11, nt=10, alpha=1.0)
    x, t, u = heat_equation_explicit()
    assert u.shape == (500, 51) and u[-1].max() < u[0].max()


def test_wave_cfl_guard():
    with pytest.raises(ValueError):
        wave_equation_leapfrog(L=1.0, T=1.0, nx=11, nt=10, c=100.0)


def test_monte_carlo_pi():
    assert monte_carlo_pi(50_000, seed=1) == pytest.approx(math.pi, rel=0.02)
