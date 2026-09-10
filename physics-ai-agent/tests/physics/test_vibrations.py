import math

import numpy as np
import pytest

from physics_agent.physics import vibrations as V
from physics_agent.solvers.spectral import fft_spectrum


def test_sdof_spring_mass():
    out = V.sdof_free(m=10.0, k=500.0)
    assert out["wn"].value == pytest.approx(math.sqrt(50), rel=1e-12)
    assert out["fn"].value == pytest.approx(math.sqrt(50) / (2 * math.pi), rel=1e-12)


def test_machine_problem():
    out = V.sdof_free(m=20.0, k=50000.0, c=100.0)
    assert out["fn"].value == pytest.approx(7.9577, rel=1e-4)
    assert out["zeta"].value == pytest.approx(0.05, rel=1e-9)


def test_magnification_resonance_peak():
    M = V.magnification(1.0, 0.05).value
    assert M == pytest.approx(1 / (2 * 0.05), rel=1e-12)


def test_transmissibility_isolation():
    assert V.transmissibility(3.0, 0.05).value < 1.0
    assert V.transmissibility(1.0, 0.05).value > 1.0


def test_mdof_two_mass():
    K = np.array([[2.0, -1.0], [-1.0, 2.0]])
    M = np.eye(2)
    out = V.mdof_modal(K, M)
    assert out["freqs_hz"][0] == pytest.approx(math.sqrt(1) / (2 * math.pi), rel=1e-9)
    assert out["freqs_hz"][1] == pytest.approx(math.sqrt(3) / (2 * math.pi), rel=1e-9)


def test_free_decay_fft_matches_wd():
    r = V.free_decay_response(m=10.0, k=500.0, c=2.0, t_end=40.0, n=20000)
    dt = r.t[1] - r.t[0]
    spec = fft_spectrum(r.y[0], dt)
    wd_expected = math.sqrt(500 / 10) * math.sqrt(1 - (2 / (2 * math.sqrt(5000))) ** 2)
    assert spec.peak_freq == pytest.approx(wd_expected / (2 * math.pi), rel=0.03)


def test_resonance_assessment_margin():
    ra = V.resonance_assessment(217.0, 215.0)
    assert ra["separation_margin_pct"] == pytest.approx(0.9216, rel=1e-3)
    assert ra["risk"] == "HIGH"
    assert len(ra["conditions_for_true_resonance"]) == 5
