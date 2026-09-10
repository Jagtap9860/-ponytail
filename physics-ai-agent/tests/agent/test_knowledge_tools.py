import pytest

from physics_agent.knowledge.constants import get_constant
from physics_agent.knowledge.formulas import FORMULAS, lookup_formula, search_formulas
from physics_agent.tools import call_tool, tool_names


def test_constants_loaded():
    assert get_constant("c").value == pytest.approx(299792458.0)
    assert get_constant("g0").value == pytest.approx(9.80665)
    with pytest.raises(KeyError):
        get_constant("nope")


def test_formulas_loaded():
    assert len(FORMULAS) >= 40
    f = lookup_formula("Newton's Second Law")
    assert f.variables["F"].si_unit == "N"
    assert search_formulas("natural frequency")


def test_tool_registry_roundtrip():
    assert "convert_units" in tool_names()
    assert call_tool("convert_units", value=10, from_unit="psi", to_unit="Pa") == pytest.approx(68947.57, rel=1e-6)
    out = call_tool("solve_equation", equation="F - m*a", symbol="a",
                    subs={"F": 100.0, "m": 10.0})
    assert out["numeric"][0] == pytest.approx(10.0)
    eig = call_tool("solve_eigenvalue_problem", K=[[4.0, 0], [0, 9.0]])
    assert eig["natural_freq_hz"][0] == pytest.approx(2 / (2 * 3.14159265), rel=1e-6)
    with pytest.raises(KeyError):
        call_tool("teleport")
