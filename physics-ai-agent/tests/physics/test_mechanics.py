import math

import pytest

from physics_agent.physics import mechanics as M


def test_newton_second_law():
    assert M.newtons_second_law(F=100.0, m=10.0).value == pytest.approx(10.0)


def test_newton_needs_two():
    with pytest.raises(ValueError):
        M.newtons_second_law(F=1.0)


def test_projectile_45_max():
    r45 = M.projectile(20, 45)["range"].value
    r30 = M.projectile(20, 30)["range"].value
    assert r45 == pytest.approx(20**2 / 9.80665, rel=1e-9)
    assert r45 > r30


def test_cantilever():
    d = M.cantilever_tip(F=100, L=1.0, E=200e9, I=8.333e-10).value
    assert d == pytest.approx(100 * 1**3 / (3 * 200e9 * 8.333e-10), rel=1e-9)


def test_incline_static():
    out = M.incline_slide(m=5, theta_deg=10, mu=0.5)
    assert out["slips"].value is False
    assert out["acceleration"].value == 0.0


def test_circular_equivalence():
    a1 = M.circular_motion(v=10, r=2).value
    a2 = M.circular_motion(omega=5, r=2).value
    assert a1 == pytest.approx(a2) == pytest.approx(50.0)
