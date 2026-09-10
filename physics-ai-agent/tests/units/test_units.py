import math

import pytest

from physics_agent.units.converter import UnitConverter, convert


def test_psi_to_pa():
    assert convert(10, "psi", "Pa") == pytest.approx(68947.57293168, rel=1e-9)


def test_mm_to_m():
    assert convert(25, "mm", "m") == pytest.approx(0.025)


def test_rpm_to_rads():
    assert convert(3000, "rpm", "rad/s") == pytest.approx(100 * math.pi, rel=1e-12)


def test_rpm_to_hz():
    assert convert(3000, "rpm", "Hz") == pytest.approx(50.0)


def test_temp_offset_roundtrip():
    k = convert(25, "degC", "K")
    assert k == pytest.approx(298.15)
    assert convert(k, "K", "degF") == pytest.approx(77.0)


def test_parse():
    q = UnitConverter.parse("10 psi")
    assert (q.value, q.unit) == (10.0, "psi")


def test_incompatible_raises():
    with pytest.raises(ValueError):
        convert(1, "kg", "m")


def test_unknown_raises():
    with pytest.raises(ValueError):
        convert(1, "furlongs", "m")
