"""Engineering: 20 kg machine on isolator — fn, damping, FRF plot, sensitivity."""
import numpy as np

from physics_agent.agent.orchestrator import Orchestrator
from physics_agent.mathematics.numerical_methods import sensitivity_table
from physics_agent.physics import vibrations as V
from physics_agent.visualization.plots import plot_frequency_response

print(Orchestrator().solve(
    "I have a 20 kg machine mounted on a spring with stiffness 50000 N/m "
    "and damping coefficient 100 Ns/m. What is its natural frequency and "
    "resonance behavior?").report())

# FRF plot
f = np.linspace(0.5, 25, 600)
ff, mag, ph = V.frequency_response(20.0, 100.0, 50000.0, f, F0=500.0)
print("FRF plot →", plot_frequency_response(ff, mag, ph, "/tmp/machine_frf.png"))

# Stiffness uncertainty ±10%: how much does fn move?
import math
tbl = sensitivity_table(lambda k: math.sqrt(k / 20) / (2 * math.pi),
                        {"k": 50000.0}, {"k": [45000.0, 50000.0, 55000.0]})
print(tbl.to_string(index=False))
