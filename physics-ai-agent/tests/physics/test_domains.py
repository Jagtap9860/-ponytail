import math

import pytest

from physics_agent.physics import (
    electromagnetism as EM,
)
from physics_agent.physics import (
    fluids as F,
)
from physics_agent.physics import (
    optics_waves as OW,
)
from physics_agent.physics import (
    quantum as Q,
)
from physics_agent.physics import (
    relativity as R,
)
from physics_agent.physics import (
    thermo as T,
)


def test_ideal_gas():
    assert T.ideal_gas(p=101325, V=0.0224, n=1).value == pytest.approx(273.4, rel=1e-2)


def test_carnot():
    assert T.carnot_efficiency(600, 300).value == pytest.approx(0.5)


def test_conduction():
    assert T.conduction_1d(200, 1.0, 400, 300, 0.1).value == pytest.approx(200000.0)


def test_bernoulli_torricelli():
    v = F.bernoulli_velocity(p1=101325, p2=101325, rho=1000, z1=2.0, z2=0.0).value
    assert v == pytest.approx(math.sqrt(2 * 9.80665 * 2), rel=1e-9)


def test_reynolds_laminar_flag():
    assert F.reynolds(1000, 0.01, 0.05, 1e-3).value == pytest.approx(500.0)


def test_coulomb():
    assert EM.coulomb(1e-6, -1e-6, 1.0).value == pytest.approx(-0.0089875517923, rel=1e-6)


def test_rlc():
    assert EM.rlc_resonance(10e-3, 100e-9).value == pytest.approx(5032.9, rel=1e-4)


def test_snell():
    assert OW.snell(1.0, 30.0, 1.5).value == pytest.approx(19.4712, rel=1e-4)


def test_doppler_approaching():
    f = OW.doppler_sound(440, v_src=10).value
    assert f > 440


def test_photon_green():
    E = Q.photon_energy(lam=532e-9)["energy_eV"].value
    assert E == pytest.approx(2.3305, rel=1e-3)


def test_time_dilation_muon():
    assert R.time_dilation(2.2e-6, 0.998 * 299792458).value == pytest.approx(2.2e-6 * 15.82, rel=1e-2)


def test_relativity_newtonian_limit():
    ke = R.relativistic_energy(1.0, 1000.0)["kinetic"].value
    assert ke == pytest.approx(0.5 * 1.0 * 1000**2, rel=1e-6)
