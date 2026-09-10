"""Engineering: cantilever tip deflection with unit conversion + dim check."""
from physics_agent.physics import mechanics as M
from physics_agent.tools import call_tool

# 100 lbf tip load, 39.37 in beam, steel E=30e6 psi, I=2.0 in^4 → convert to SI
F = call_tool("convert_units", value=100, from_unit="lbf", to_unit="N")
L = call_tool("convert_units", value=39.37, from_unit="in", to_unit="m")
E = call_tool("convert_units", value=30e6, from_unit="psi", to_unit="Pa")
I = 2.0 * 0.0254**4  # in^4 → m^4
print(call_tool("check_dimensions", lhs_unit="m",
                rhs={"N": 1, "m": 3, "Pa": -1, "m^2": -2}))
r = M.cantilever_tip(F, L, E, I)
print(r, f"= {r.value/0.0254:.4f} in")
