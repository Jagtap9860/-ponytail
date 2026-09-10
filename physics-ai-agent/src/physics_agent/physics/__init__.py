"""Physics domain solvers (SI in / SI out) + domain registry."""
from physics_agent.physics import (
    dimensionless,
    electromagnetism,
    fluids,
    mechanics,
    optics_waves,
    quantum,
    relativity,
    thermo,
    vibrations,
)
from physics_agent.physics.base import PhysicsResult, domains, register_domain

register_domain("classical_mechanics", "Classical Mechanics",
                ("newton", "force", "mass", "acceleration", "projectile", "kinematics",
                 "statics", "dynamics", "energy", "momentum", "incline", "friction",
                 "orbit", "gravity", "beam", "cantilever", "deflection", "torsion"))
register_domain("vibrations", "Vibrations & Structural Dynamics",
                ("vibration", "natural frequency", "resonance", "damping", "sdof",
                 "mdof", "mode", "modal", "harmonic", "transmissibility", "isolator",
                 "rotor", "campbell", "fft", "frequency response", "spring"))
register_domain("thermodynamics", "Thermodynamics",
                ("thermodynamic", "entropy", "carnot", "ideal gas", "heat engine",
                 "refrigerator", "enthalpy", "cycle"))
register_domain("heat_transfer", "Heat Transfer",
                ("conduction", "convection", "radiation", "heat transfer", "fourier",
                 "lmtd", "heat exchanger", "emissivity", "insulation"))
register_domain("fluid_mechanics", "Fluid Mechanics",
                ("fluid", "bernoulli", "reynolds", "pipe", "pressure drop", "drag",
                 "navier", "stokes", "flow", "viscosity", "pump", "turbulent", "laminar"))
register_domain("electromagnetism", "Electromagnetism",
                ("coulomb", "electric", "magnetic", "maxwell", "faraday", "induct",
                 "capacitor", "resistor", "circuit", "voltage", "current", "impedance",
                 "lorentz", "solenoid", "wire"))
register_domain("optics", "Optics",
                ("lens", "snell", "refraction", "reflection", "focal", "mirror",
                 "diffraction", "interference", "polarization"))
register_domain("waves", "Waves & Acoustics",
                ("wave", "sound", "acoustic", "doppler", "decibel", "string",
                 "standing wave", "wavelength"))
register_domain("quantum_mechanics", "Quantum & Modern Physics",
                ("quantum", "photon", "planck", "schrodinger", "de broglie", "particle in a box",
                 "uncertainty", "radioactive", "half-life", "blackbody", "photoelectric"))
register_domain("relativity", "Relativity",
                ("relativ", "lorentz", "time dilation", "length contraction", "gamma",
                 "rest energy", "muon"))
register_domain("statistical_mechanics", "Statistical Mechanics",
                ("boltzmann", "maxwell-boltzmann", "partition", "ensemble", "rms speed"))
register_domain("fea", "FEA & Computational Mechanics",
                ("fea", "finite element", "ansys", "abaqus", "mesh", "convergence",
                 "singularity", "contact", "buckling", "prestress", "harmonic analysis",
                 "transient", "fatigue", "modal analysis"))

__all__ = [
    "mechanics", "vibrations", "thermo", "fluids", "electromagnetism",
    "optics_waves", "quantum", "relativity", "dimensionless",
    "PhysicsResult", "domains", "register_domain",
]
