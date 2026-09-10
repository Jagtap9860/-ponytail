"""Dimensional-analysis engine over the 7 SI base dimensions.

Dimension vector order: [M, L, T, I, Theta, N, J].
Supports equation checks, Buckingham-Pi helper, and standard
dimensionless numbers.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

_BASES = ("M", "L", "T", "I", "Theta", "N", "J")


@dataclass(frozen=True)
class Dimension:
    """Dimension as exponents of SI bases."""

    M: Fraction = Fraction(0)
    L: Fraction = Fraction(0)
    T: Fraction = Fraction(0)
    I: Fraction = Fraction(0)  # noqa: E741
    Theta: Fraction = Fraction(0)
    N: Fraction = Fraction(0)
    J: Fraction = Fraction(0)

    def as_tuple(self) -> tuple[Fraction, ...]:
        return (self.M, self.L, self.T, self.I, self.Theta, self.N, self.J)

    def __mul__(self, o: Dimension) -> Dimension:
        return _v(tuple(a + b for a, b in zip(self.as_tuple(), o.as_tuple())))

    def __truediv__(self, o: Dimension) -> Dimension:
        return _v(tuple(a - b for a, b in zip(self.as_tuple(), o.as_tuple())))

    def __pow__(self, p: int | Fraction) -> Dimension:
        p = Fraction(p)
        return _v(tuple(a * p for a in self.as_tuple()))

    @property
    def is_dimensionless(self) -> bool:
        return all(a == 0 for a in self.as_tuple())

    def __str__(self) -> str:
        parts = [f"{n}^{e}" for n, e in zip(_BASES, self.as_tuple()) if e != 0]
        return " · ".join(parts) if parts else "dimensionless"


def _v(t: tuple[Fraction, ...]) -> Dimension:
    return Dimension(*t)


def _d(**kw: int | Fraction) -> Dimension:
    args = {b: Fraction(kw.get(b, 0)) for b in _BASES}
    return Dimension(**args)  # type: ignore[arg-type]


# ---- SI base units ----
_BASE_DIM: dict[str, Dimension] = {
    "kg": _d(M=1), "m": _d(L=1), "s": _d(T=1), "A": _d(I=1),
    "K": _d(Theta=1), "mol": _d(N=1), "cd": _d(J=1),
    "rad": _d(), "Hz": _d(T=-1),
}

# ---- derived SI units ----
_DERIVED_DIM: dict[str, Dimension] = {
    "N": _d(M=1, L=1, T=-2),
    "Pa": _d(M=1, L=-1, T=-2),
    "J": _d(M=1, L=2, T=-2),
    "W": _d(M=1, L=2, T=-3),
    "C": _d(T=1, I=1),
    "V": _d(M=1, L=2, T=-3, I=-1),
    "ohm": _d(M=1, L=2, T=-3, I=-2),
    "F": _d(M=-1, L=-2, T=4, I=2),
    "H": _d(M=1, L=2, T=-2, I=-2),
    "T": _d(M=1, T=-2, I=-1),
    "Wb": _d(M=1, L=2, T=-2, I=-1),
    "m/s": _d(L=1, T=-1),
    "m/s^2": _d(L=1, T=-2),
    "m^2": _d(L=2), "m^3": _d(L=3),
    "kg/m^3": _d(M=1, L=-3),
    "Pa*s": _d(M=1, L=-1, T=-1),
    "m^2/s": _d(L=2, T=-1),
    "N/m": _d(M=1, T=-2),
    "Ns/m": _d(M=1, T=-1),
    "rad/s": _d(T=-1),
    "W/m/K": _d(M=1, L=1, T=-3, Theta=-1),
    "W/m^2/K": _d(M=1, T=-3, Theta=-1),
    "J/kg/K": _d(L=2, T=-2, Theta=-1),
}

# quantity-name aliases for equation checking
_QUANTITY_DIM: dict[str, Dimension] = {
    "mass": _d(M=1), "length": _d(L=1), "time": _d(T=1), "current": _d(I=1),
    "temperature": _d(Theta=1),
    "force": _d(M=1, L=1, T=-2), "pressure": _d(M=1, L=-1, T=-2),
    "energy": _d(M=1, L=2, T=-2), "power": _d(M=1, L=2, T=-3),
    "velocity": _d(L=1, T=-1), "acceleration": _d(L=1, T=-2),
    "frequency": _d(T=-1), "angular_frequency": _d(T=-1),
    "charge": _d(T=1, I=1), "voltage": _d(M=1, L=2, T=-3, I=-1),
    "density": _d(M=1, L=-3), "viscosity": _d(M=1, L=-1, T=-1),
    "stiffness": _d(M=1, T=-2), "damping": _d(M=1, T=-1),
}


def dimension_of(unit_or_quantity: str) -> Dimension:
    """Resolve an SI unit string or quantity name to a Dimension."""
    from physics_agent.units.converter import UnitConverter  # lazy: avoid cycle

    key = unit_or_quantity.strip()
    if key in _BASE_DIM:
        return _BASE_DIM[key]
    if key in _DERIVED_DIM:
        return _DERIVED_DIM[key]
    if key in _QUANTITY_DIM:
        return _QUANTITY_DIM[key]
    # Try converting 1.0 of the unit to SI, then look up the SI unit.
    try:
        _, si = UnitConverter.to_si(1.0, key)
    except ValueError as exc:
        raise ValueError(f"Unknown dimension for '{unit_or_quantity}'.") from exc
    if si in _BASE_DIM:
        return _BASE_DIM[si]
    if si in _DERIVED_DIM:
        return _DERIVED_DIM[si]
    raise ValueError(f"No dimension mapping for SI unit '{si}'.")


@dataclass(frozen=True)
class DimCheck:
    ok: bool
    lhs: Dimension
    rhs: Dimension
    message: str


def check_equation(lhs_unit: str, rhs_units: dict[str, float]) -> DimCheck:
    """Check `lhs = prod(rhs ^ power)`, e.g. check_equation('N', {'kg':1,'m/s^2':1}).

    Returns ok=True with a human-readable message; never raises on mismatch.
    """
    lhs = dimension_of(lhs_unit)
    rhs = _d()
    for unit, power in rhs_units.items():
        rhs = rhs * (dimension_of(unit) ** Fraction(power).limit_denominator(100))
    ok = lhs.as_tuple() == rhs.as_tuple()
    msg = (
        f"[{lhs_unit}] = {lhs}  vs  RHS = {rhs}  → "
        + ("CONSISTENT ✓" if ok else "INCONSISTENT ✗")
    )
    return DimCheck(ok, lhs, rhs, msg)


def buckingham_pi(variables: dict[str, Dimension], repeating: list[str]) -> list[str]:
    """Form dimensionless Pi groups from variables + repeating variables.

    Returns human-readable group expressions (exponents solved via integer
    null-space over the base-dimension matrix, small systems only).
    """
    import itertools

    others = [v for v in variables if v not in repeating]
    groups: list[str] = []
    for target in others:
        # Solve: dim(target) + sum_j e_j dim(r_j) = 0 for small integer e_j.
        t = variables[target].as_tuple()
        found = None
        for exps in itertools.product(range(-3, 4), repeat=len(repeating)):
            if all(e == 0 for e in exps):
                continue
            acc = list(t)
            for e, r in zip(exps, repeating):
                rd = variables[r].as_tuple()
                acc = [a + Fraction(e) * b for a, b in zip(acc, rd)]
            if all(a == 0 for a in acc):
                found = exps
                break
        if found is None:
            groups.append(f"Π_{target}: (no small-integer group found)")
            continue
        terms = [target] + [f"{r}^{e}" if e != 1 else r for e, r in zip(found, repeating) if e != 0]
        groups.append(f"Π_{target} = " + " · ".join(terms))
    return groups


def dimensionless_numbers() -> dict[str, dict[str, str]]:
    """Standard dimensionless groups with definitions."""
    return {
        "Reynolds": {"formula": "Re = rho*v*L/mu", "meaning": "inertia / viscous forces"},
        "Mach": {"formula": "Ma = v/a", "meaning": "flow speed / speed of sound"},
        "Froude": {"formula": "Fr = v/sqrt(g*L)", "meaning": "inertia / gravity"},
        "Prandtl": {"formula": "Pr = mu*cp/k", "meaning": "momentum / thermal diffusivity"},
        "Nusselt": {"formula": "Nu = h*L/k", "meaning": "convective / conductive heat transfer"},
        "Strouhal": {"formula": "St = f*L/v", "meaning": "oscillation / flow time scales"},
        "Weber": {"formula": "We = rho*v^2*L/sigma", "meaning": "inertia / surface tension"},
        "Biot": {"formula": "Bi = h*L/k_solid", "meaning": "surface / internal conduction resistance"},
        "Fourier": {"formula": "Fo = alpha*t/L^2", "meaning": "conducted / stored heat"},
        "Cauchy": {"formula": "Ca = rho*v^2/E", "meaning": "inertia / elastic forces"},
        "Knudsen": {"formula": "Kn = lambda/L", "meaning": "mean free path / length scale"},
    }
