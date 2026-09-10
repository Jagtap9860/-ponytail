"""Tool-call architecture: typed wrappers over the deterministic layer.

The agent (or an LLM with function calling) selects tools dynamically;
every tool is reproducible and unit-testable without any LLM.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass
class Tool:
    name: str
    description: str
    parameters: dict[str, Any]   # JSON-schema-ish {name: {type, description}}
    function: Callable[..., Any]


def _t_solve_equation(equation: str, symbol: str, subs: dict[str, float] | None = None) -> dict:
    """Solve equation (e.g. 'F - m*a') for symbol; subs plugs numbers in."""
    from physics_agent.solvers.symbolic import solve_symbolic
    return solve_symbolic(equation, symbol, **(subs or {}))


def _t_convert_units(value: float, from_unit: str, to_unit: str) -> float:
    from physics_agent.units.converter import convert
    return convert(value, from_unit, to_unit)


def _t_check_dimensions(lhs_unit: str, rhs: dict[str, float]) -> dict:
    from physics_agent.units.dimensional_analysis import check_equation
    c = check_equation(lhs_unit, rhs)
    return {"ok": c.ok, "message": c.message}


def _t_derivative(expr: str, symbol: str, at: float | None = None) -> str | float:
    from physics_agent.solvers.symbolic import differentiate
    d = differentiate(expr, symbol)
    if at is None:
        return d
    import sympy as sp
    return float(sp.sympify(d).subs(sp.Symbol(symbol), at))


def _t_integral(expr: str, symbol: str, a: float, b: float) -> float:
    from physics_agent.solvers.numerical import integrate
    import sympy as sp
    f = sp.lambdify(sp.Symbol(symbol), sp.sympify(expr), "numpy")
    val, _ = integrate(lambda x: float(f(x)), a, b)
    return val


def _t_solve_ode(m: float, c: float, k: float, t_end: float = 5.0,
                 x0: float = 0.0, v0: float = 0.0) -> dict:
    from physics_agent.solvers.ode import solve_sdof
    r = solve_sdof(m, c, k, None, t_end, 1000, x0, v0)
    return {"t": r.t.tolist()[::100], "x": r.y[0].tolist()[::100], "success": r.success}


def _t_eigen(K: list[list[float]], M: list[list[float]] | None = None) -> dict:
    from physics_agent.solvers.eigenvalue import generalized_eigen, modal_analysis
    r = generalized_eigen(np.array(K), np.array(M)) if M else modal_analysis(np.array(K))
    return {"eigenvalues": r.eigenvalues.tolist(),
            "natural_freq_hz": r.natural_freq_hz.tolist()}


def _t_fft(signal: list[float], dt: float) -> dict:
    from physics_agent.solvers.spectral import fft_spectrum
    s = fft_spectrum(np.array(signal), dt)
    return {"peak_freq": s.peak_freq, "peak_amplitude": s.peak_amplitude}


def _t_plot(kind: str, x0: float = 0.0, x1: float = 10.0,
            expr: str = "sin(x)", path: str = "/tmp/physics_plot.png") -> str:
    from physics_agent.visualization.plots import plot_function
    return plot_function(expr, (x0, x1), path, title=expr)


def _t_sweep(expr: str, symbol: str, values: list[float]) -> list[float]:
    import sympy as sp
    f = sp.lambdify(sp.Symbol(symbol), sp.sympify(expr), "numpy")
    return [float(f(v)) for v in values]


def _t_sensitivity(expr: str, base: dict[str, float],
                   perturbations: dict[str, list[float]]) -> list[dict]:
    from physics_agent.mathematics.numerical_methods import sensitivity_table
    import sympy as sp
    syms = {k: sp.Symbol(k) for k in base}
    e = sp.sympify(expr)
    f = lambda **kw: float(e.subs({syms[k]: v for k, v in kw.items()}))  # noqa: E731
    return sensitivity_table(f, base, perturbations).to_dict("records")


def _t_verify(solution: str, domain: str, values: dict[str, float]) -> dict:
    from physics_agent.agent.verification import detect_errors, limiting_case_note
    return {"warnings": detect_errors(solution, domain and solution or "", values)
            if False else detect_errors(solution, values),
            "limiting_case": limiting_case_note(domain)}


def _t_formula(query: str, domain: str | None = None) -> list[str]:
    from physics_agent.knowledge.formulas import search_formulas
    return [f.describe() for f in search_formulas(query, domain)]


def _t_constant(symbol: str) -> dict:
    from physics_agent.knowledge.constants import get_constant
    c = get_constant(symbol)
    return {"symbol": c.symbol, "value": c.value, "unit": c.unit, "source": c.source}


def _P(**kw: Any) -> dict[str, Any]:
    return kw


TOOLS: dict[str, Tool] = {
    t.name: t for t in [
        Tool("solve_equation", "Symbolically solve equation for a symbol.",
             _P(equation={"type": "str"}, symbol={"type": "str"},
                subs={"type": "object"}), _t_solve_equation),
        Tool("convert_units", "Convert value between units via SI.",
             _P(value={"type": "number"}, from_unit={"type": "str"},
                to_unit={"type": "str"}), _t_convert_units),
        Tool("check_dimensions", "Dimensional consistency of lhs = prod(rhs^powers).",
             _P(lhs_unit={"type": "str"}, rhs={"type": "object"}), _t_check_dimensions),
        Tool("derivative", "Symbolic derivative, optionally evaluated at a point.",
             _P(expr={"type": "str"}, symbol={"type": "str"}, at={"type": "number"}),
             _t_derivative),
        Tool("integral", "Definite integral of expr from a to b.",
             _P(expr={"type": "str"}, symbol={"type": "str"}, a={"type": "number"},
                b={"type": "number"}), _t_integral),
        Tool("solve_ode", "SDOF time response m x''+c x'+k x=0.",
             _P(m={"type": "number"}, c={"type": "number"}, k={"type": "number"},
                t_end={"type": "number"}), _t_solve_ode),
        Tool("solve_eigenvalue_problem", "Eigenvalues (+modal freqs) of K, or (K, M).",
             _P(K={"type": "array"}, M={"type": "array"}), _t_eigen),
        Tool("fft", "Peak frequency/amplitude of a sampled signal.",
             _P(signal={"type": "array"}, dt={"type": "number"}), _t_fft),
        Tool("plot_function", "Plot expr over [x0,x1] to a PNG file.",
             _P(expr={"type": "str"}, x0={"type": "number"}, x1={"type": "number"},
                path={"type": "str"}), _t_plot),
        Tool("parameter_sweep", "Evaluate expr over a value list.",
             _P(expr={"type": "str"}, symbol={"type": "str"}, values={"type": "array"}),
             _t_sweep),
        Tool("sensitivity_analysis", "One-at-a-time sensitivity table.",
             _P(expr={"type": "str"}, base={"type": "object"},
                perturbations={"type": "object"}), _t_sensitivity),
        Tool("verify_solution", "Error scan + limiting-case note.",
             _P(solution={"type": "str"}, domain={"type": "str"}, values={"type": "object"}),
             _t_verify),
        Tool("lookup_formula", "Search the formula database.",
             _P(query={"type": "str"}, domain={"type": "str"}), _t_formula),
        Tool("lookup_constant", "Fetch a physical constant by symbol.",
             _P(symbol={"type": "str"}), _t_constant),
    ]
}


def tool_names() -> list[str]:
    return sorted(TOOLS)


def call_tool(name: str, **kwargs: Any) -> Any:
    if name not in TOOLS:
        raise KeyError(f"Unknown tool '{name}'. Available: {tool_names()}.")
    return TOOLS[name].function(**kwargs)
