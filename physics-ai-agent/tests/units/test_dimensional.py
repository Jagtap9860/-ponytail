from physics_agent.units.dimensional_analysis import (
    buckingham_pi,
    check_equation,
    dimension_of,
    dimensionless_numbers,
)


def test_newton_dimensions():
    assert check_equation("N", {"kg": 1, "m/s^2": 1}).ok


def test_mismatch_detected():
    assert not check_equation("N", {"kg": 1, "m/s": 1}).ok


def test_unit_alias_resolution():
    assert dimension_of("psi").as_tuple() == dimension_of("Pa").as_tuple()
    assert dimension_of("rpm").as_tuple() == dimension_of("Hz").as_tuple()


def test_stiffness_dimension():
    d = dimension_of("N/m")
    assert d.is_dimensionless is False
    assert check_equation("N/m", {"kg": 1, "Hz": 2}).ok  # k ~ m·ω²


def test_buckingham_reynolds():
    rho = dimension_of("kg/m^3")
    v = dimension_of("m/s")
    L = dimension_of("m")
    mu = dimension_of("Pa*s")
    groups = buckingham_pi({"rho": rho, "v": v, "L": L, "mu": mu}, ["rho", "v", "L"])
    assert len(groups) == 1 and "mu" in groups[0]


def test_dimensionless_catalog():
    nums = dimensionless_numbers()
    assert {"Reynolds", "Mach", "Nusselt", "Prandtl"} <= set(nums)
