"""Symbolic mathematics via SymPy: rearrange, solve, differentiate, integrate."""
from __future__ import annotations

import sympy as sp


def solve_symbolic(equation: str, symbol: str, **subs: float) -> dict:
    """Solve `equation` (e.g. 'F - m*a') for `symbol`, optionally substituting values.

    Returns {'symbolic': [solutions], 'numeric': [float values or None]}.
    """
    lhs = sp.sympify(equation)
    sym = sp.Symbol(symbol)
    sols = sp.solve(lhs, sym)
    out = {"symbolic": [str(s) for s in sols], "numeric": []}
    submap = {sp.Symbol(k): v for k, v in subs.items()}
    for s in sols:
        try:
            out["numeric"].append(float(complex(s.subs(submap)).real))
        except Exception:
            out["numeric"].append(None)
    return out


def rearrange(equation: str, symbol: str) -> str:
    """Rearrange equation isolating `symbol`. Returns expression string."""
    sols = sp.solve(sp.sympify(equation), sp.Symbol(symbol))
    if not sols:
        raise ValueError(f"Could not isolate '{symbol}' in '{equation}'.")
    return str(sols[0])


def differentiate(expr: str, symbol: str, order: int = 1) -> str:
    return str(sp.diff(sp.sympify(expr), sp.Symbol(symbol), order))


def integrate_symbolic(expr: str, symbol: str, a: float | None = None, b: float | None = None) -> str:
    x = sp.Symbol(symbol)
    e = sp.sympify(expr)
    res = sp.integrate(e, (x, a, b)) if a is not None and b is not None else sp.integrate(e, x)
    return str(res)


def simplify(expr: str) -> str:
    return str(sp.simplify(sp.sympify(expr)))
