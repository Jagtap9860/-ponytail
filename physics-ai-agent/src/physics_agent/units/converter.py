"""Robust unit handling: SI, CGS, Imperial/US customary.

All conversions go through SI. Temperatures with offsets (degC/degF) are
handled explicitly. Unknown or ambiguous units raise with suggestions.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass

from physics_agent.knowledge.constants import get_constant

_G0 = get_constant("g0").value      # kgf defined via standard gravity (exact conventional)
_E_JOULE = get_constant("e").value  # 1 eV in joules (exact by SI definition)

# unit -> (SI factor, SI unit, dimension key)
_LINEAR_UNITS: dict[str, tuple[float, str, str]] = {}

def _reg(names: tuple[str, ...], factor: float, si: str, dim: str) -> None:
    for n in names:
        _LINEAR_UNITS[n] = (factor, si, dim)

# Length (m)
_reg(("m", "meter", "meters", "metre"), 1.0, "m", "L")
_reg(("km",), 1000.0, "m", "L")
_reg(("cm",), 0.01, "m", "L")
_reg(("mm",), 1e-3, "m", "L")
_reg(("um", "µm", "micron", "microns"), 1e-6, "m", "L")
_reg(("nm",), 1e-9, "m", "L")
_reg(("in", "inch", "inches"), 0.0254, "m", "L")
_reg(("ft", "foot", "feet"), 0.3048, "m", "L")
_reg(("yd", "yard"), 0.9144, "m", "L")
_reg(("mi", "mile", "miles"), 1609.344, "m", "L")
_reg(("mil", "thou"), 2.54e-5, "m", "L")
_reg(("angstrom", "å"), 1e-10, "m", "L")
# Mass (kg)
_reg(("kg",), 1.0, "kg", "M")
_reg(("g", "gram", "grams"), 1e-3, "kg", "M")
_reg(("mg",), 1e-6, "kg", "M")
_reg(("tonne", "metric_ton", "t"), 1000.0, "kg", "M")
_reg(("lb", "lbs", "pound", "pounds", "lbm"), 0.45359237, "kg", "M")
_reg(("oz", "ounce"), 0.028349523125, "kg", "M")
_reg(("slug",), 14.59390294, "kg", "M")
# Time (s)
_reg(("s", "sec", "second", "seconds"), 1.0, "s", "T")
_reg(("ms",), 1e-3, "s", "T")
_reg(("us", "µs"), 1e-6, "s", "T")
_reg(("ns",), 1e-9, "s", "T")
_reg(("min", "minute", "minutes"), 60.0, "s", "T")
_reg(("h", "hr", "hour", "hours"), 3600.0, "s", "T")
_reg(("day", "days"), 86400.0, "s", "T")
# Force (N)
_reg(("N", "newton", "newtons"), 1.0, "N", "F")
_reg(("kN",), 1e3, "N", "F")
_reg(("MN",), 1e6, "N", "F")
_reg(("mN",), 1e-3, "N", "F")
_reg(("lbf", "lb_f", "pound_force"), 4.4482216152605, "N", "F")
_reg(("ozf",), 0.2780138509537812, "N", "F")
_reg(("dyne", "dyn"), 1e-5, "N", "F")
_reg(("kgf", "kp"), _G0, "N", "F")
# Pressure (Pa)
_reg(("Pa", "pascal"), 1.0, "Pa", "P")
_reg(("kPa",), 1e3, "Pa", "P")
_reg(("MPa",), 1e6, "Pa", "P")
_reg(("GPa",), 1e9, "Pa", "P")
_reg(("bar",), 1e5, "Pa", "P")
_reg(("mbar", "hPa"), 100.0, "Pa", "P")
_reg(("psi", "psia", "psig"), 6894.757293168, "Pa", "P")
_reg(("ksi",), 6894757.293168, "Pa", "P")
_reg(("psf",), 47.88025898, "Pa", "P")
_reg(("atm",), 101325.0, "Pa", "P")
_reg(("torr", "mmhg", "mmHg"), 133.3223684211, "Pa", "P")
_reg(("inh2o", 'inH2O'), 249.08891, "Pa", "P")
# Energy (J)
_reg(("J", "joule", "joules"), 1.0, "J", "E")
_reg(("kJ",), 1e3, "J", "E")
_reg(("MJ",), 1e6, "J", "E")
_reg(("cal",), 4.184, "J", "E")
_reg(("kcal",), 4184.0, "J", "E")
_reg(("btu", "BTU"), 1055.05585262, "J", "E")
_reg(("kWh", "kwh"), 3.6e6, "J", "E")
_reg(("eV", "ev"), _E_JOULE, "J", "E")
_reg(("erg",), 1e-7, "J", "E")
_reg(("ft_lbf", "ft-lbf", "ftlb"), 1.3558179483314004, "J", "E")
# Power (W)
_reg(("W", "watt", "watts"), 1.0, "W", "PW")
_reg(("kW",), 1e3, "W", "PW")
_reg(("MW",), 1e6, "W", "PW")
_reg(("mW",), 1e-3, "W", "PW")
_reg(("hp", "horsepower"), 745.69987158227022, "W", "PW")
# Frequency (Hz)
_reg(("Hz", "hz", "hertz"), 1.0, "Hz", "f")
_reg(("kHz",), 1e3, "Hz", "f")
_reg(("MHz",), 1e6, "Hz", "f")
_reg(("GHz",), 1e9, "Hz", "f")
_reg(("rpm", "RPM"), 1.0 / 60.0, "Hz", "f")
_reg(("rps", "rev/s"), 1.0, "Hz", "f")
# Angle (rad)
_reg(("rad", "radian"), 1.0, "rad", "A")
_reg(("deg", "degree", "degrees", "°"), math.pi / 180.0, "rad", "A")
_reg(("rev", "revolution"), 2 * math.pi, "rad", "A")
_reg(("arcmin",), math.pi / 10800.0, "rad", "A")
_reg(("arcsec",), math.pi / 648000.0, "rad", "A")
# Angular velocity (rad/s)
_reg(("rad/s", "rad_s"), 1.0, "rad/s", "AV")
# Speed (m/s)
_reg(("m/s", "mps"), 1.0, "m/s", "V")
_reg(("km/h", "kph"), 1.0 / 3.6, "m/s", "V")
_reg(("mph",), 0.44704, "m/s", "V")
_reg(("ft/s", "fps"), 0.3048, "m/s", "V")
_reg(("knot", "knots", "kt"), 0.5144444444444445, "m/s", "V")
# Area (m^2)
_reg(("m^2", "m2", "sqm"), 1.0, "m^2", "A2")
_reg(("cm^2", "cm2"), 1e-4, "m^2", "A2")
_reg(("mm^2", "mm2"), 1e-6, "m^2", "A2")
_reg(("in^2", "in2", "sqin"), 0.00064516, "m^2", "A2")
_reg(("ft^2", "ft2", "sqft"), 0.09290304, "m^2", "A2")
# Volume (m^3)
_reg(("m^3", "m3"), 1.0, "m^3", "V3")
_reg(("L", "l", "liter", "litre", "liters"), 1e-3, "m^3", "V3")
_reg(("mL", "ml"), 1e-6, "m^3", "V3")
_reg(("cm^3", "cm3", "cc"), 1e-6, "m^3", "V3")
_reg(("in^3", "in3"), 1.6387064e-5, "m^3", "V3")
_reg(("ft^3", "ft3"), 0.028316846592, "m^3", "V3")
_reg(("gal", "gallon", "gallons"), 0.003785411784, "m^3", "V3")
_reg(("qt", "quart"), 0.000946352946, "m^3", "V3")
# Density (kg/m^3)
_reg(("kg/m^3", "kg/m3"), 1.0, "kg/m^3", "D")
_reg(("g/cm^3", "g/cm3", "g/cc"), 1000.0, "kg/m^3", "D")
_reg(("lb/ft^3", "lb/ft3", "pcf"), 16.01846337396014, "kg/m^3", "D")
# Viscosity dynamic (Pa*s)
_reg(("Pa*s", "Pa.s", "pas"), 1.0, "Pa*s", "MU")
_reg(("poise", "P"), 0.1, "Pa*s", "MU")
_reg(("cP", "cp", "centipoise"), 1e-3, "Pa*s", "MU")
_reg(("lbf*s/ft^2",), 47.88025898, "Pa*s", "MU")
# Viscosity kinematic (m^2/s)
_reg(("m^2/s", "m2/s"), 1.0, "m^2/s", "NU")
_reg(("stokes", "St"), 1e-4, "m^2/s", "NU")
_reg(("cSt", "centistokes"), 1e-6, "m^2/s", "NU")
# Electric: charge C, current A, voltage V, resistance ohm, capacitance F, inductance H
_reg(("C", "coulomb"), 1.0, "C", "Q")
_reg(("A", "amp", "ampere"), 1.0, "A", "I")
_reg(("mA",), 1e-3, "A", "I")
_reg(("V", "volt", "volts"), 1.0, "V", "U")
_reg(("mV",), 1e-3, "V", "U")
_reg(("kV",), 1e3, "V", "U")
_reg(("ohm", "Ω", "ohms"), 1.0, "ohm", "R")
_reg(("kohm", "kΩ"), 1e3, "ohm", "R")
_reg(("Mohm", "MΩ"), 1e6, "ohm", "R")
_reg(("F", "farad"), 1.0, "F", "C")
_reg(("uF", "µF"), 1e-6, "F", "C")
_reg(("nF",), 1e-9, "F", "C")
_reg(("pF",), 1e-12, "F", "C")
_reg(("H", "henry"), 1.0, "H", "LH")
_reg(("mH",), 1e-3, "H", "LH")
# Magnetic flux density (T)
_reg(("T", "tesla"), 1.0, "T", "B")
_reg(("mT",), 1e-3, "T", "B")
_reg(("G", "gauss"), 1e-4, "T", "B")
# Temperature absolute (K)
_reg(("K", "kelvin"), 1.0, "K", "TH")
_reg(("degR", "rankine", "°R"), 5.0 / 9.0, "K", "TH")
# Thermal conductivity (W/m/K)
_reg(("W/m/K", "W/mK"), 1.0, "W/m/K", "TC")
_reg(("BTU/hr/ft/F", "btu/hr/ft/F"), 1.7307346663710808, "W/m/K", "TC")
# Heat transfer coeff (W/m^2/K)
_reg(("W/m^2/K", "W/m2/K"), 1.0, "W/m^2/K", "HTC")
_reg(("BTU/hr/ft^2/F", "btu/hr/ft2/F"), 5.678263341113488, "W/m^2/K", "HTC")

# rpm special-case for angular velocity
_RPM_TO_RADS = 2 * math.pi / 60.0

_TEMP_OFFSET = {"degC", "°C", "celsius", "Celsius", "degF", "°F", "fahrenheit", "Fahrenheit"}


@dataclass(frozen=True)
class Quantity:
    """A value with a unit, convertible to SI."""

    value: float
    unit: str

    def to_si(self) -> tuple[float, str]:
        """Convert this quantity to SI; return (value, unit)."""
        return UnitConverter.to_si(self.value, self.unit)

    def to(self, target: str) -> float:
        """Convert this quantity to the target unit."""
        return UnitConverter.convert(self.value, self.unit, target)


class UnitConverter:
    """Stateless converter. All paths go through SI."""

    @staticmethod
    def _canon(unit: str) -> str:
        u = unit.strip()
        if u in _LINEAR_UNITS or u in _TEMP_OFFSET:
            return u
        # case-insensitive fallback (careful: 'Pa' vs 'pa' kept distinct first)
        low = u.lower()
        for key in list(_LINEAR_UNITS) + list(_TEMP_OFFSET):
            if key.lower() == low:
                return key
        raise ValueError(f"Unknown unit '{unit}'.")

    @staticmethod
    def to_si(value: float, unit: str) -> tuple[float, str]:
        """Convert value+unit to SI."""
        u = UnitConverter._canon(unit)
        if u in ("degC", "°C", "celsius", "Celsius"):
            return value + 273.15, "K"
        if u in ("degF", "°F", "fahrenheit", "Fahrenheit"):
            return (value - 32.0) * 5.0 / 9.0 + 273.15, "K"
        factor, si, _ = _LINEAR_UNITS[u]
        return value * factor, si

    @staticmethod
    def from_si(si_value: float, unit: str) -> float:
        """Convert an SI value to the target unit."""
        u = UnitConverter._canon(unit)
        if u in ("degC", "°C", "celsius", "Celsius"):
            return si_value - 273.15
        if u in ("degF", "°F", "fahrenheit", "Fahrenheit"):
            return (si_value - 273.15) * 9.0 / 5.0 + 32.0
        factor, _, _ = _LINEAR_UNITS[u]
        return si_value / factor

    # pairs that cross dimension keys but are physically convertible
    _CROSS = {
        ("rad/s", "Hz"): lambda x: x / (2 * math.pi),
        ("Hz", "rad/s"): lambda x: x * 2 * math.pi,
        ("rpm", "rad/s"): lambda x: x * _RPM_TO_RADS,
        ("rad/s", "rpm"): lambda x: x / _RPM_TO_RADS,
        ("RPM", "rad/s"): lambda x: x * _RPM_TO_RADS,
        ("rad/s", "RPM"): lambda x: x / _RPM_TO_RADS,
        ("rev", "rad"): lambda x: x * 2 * math.pi,
    }

    @staticmethod
    def convert(value: float, from_unit: str, to_unit: str) -> float:
        """Convert between units via SI (Hz<->rad/s allowed)."""
        src = UnitConverter._canon(from_unit)
        dst = UnitConverter._canon(to_unit)
        if (src, dst) in UnitConverter._CROSS:
            return UnitConverter._CROSS[(src, dst)](value)
        # normalize rpm/rps to Hz for cross conversion
        si_val, si_unit = UnitConverter.to_si(value, src)
        # allow Hz <-> rad/s via SI Hz
        if si_unit == "Hz" and dst in ("rad/s", "rad_s"):
            return si_val * 2 * math.pi
        if src in ("rad/s", "rad_s") and _LINEAR_UNITS.get(dst, (0, "", ""))[2] == "f":
            return UnitConverter.from_si(value / (2 * math.pi), dst)
        _, dst_si, _ = _LINEAR_UNITS.get(dst, (1.0, dst, ""))
        if dst in _TEMP_OFFSET:
            return UnitConverter.from_si(si_val, dst)
        if si_unit != dst_si:
            raise ValueError(
                f"Incompatible units: '{from_unit}' ({si_unit}) vs '{to_unit}' ({dst_si})."
            )
        return UnitConverter.from_si(si_val, dst)

    @staticmethod
    def parse(text: str) -> Quantity:
        """Parse strings like '3000 rpm', '25 mm', '10 psi', '9.81 m/s^2'."""
        m = re.match(r"^\s*([+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)\s*(.+?)\s*$", text)
        if not m:
            raise ValueError(f"Could not parse quantity '{text}'. Expected '<number> <unit>'.")
        return Quantity(float(m.group(1)), m.group(2).strip())

    @staticmethod
    def dimension_key(unit: str) -> str:
        """Compatibility key for a unit."""
        u = UnitConverter._canon(unit)
        if u in _TEMP_OFFSET:
            return "TH"
        return _LINEAR_UNITS[u][2]


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convenience function: convert(value, 'psi', 'Pa')."""
    return UnitConverter.convert(value, from_unit, to_unit)
