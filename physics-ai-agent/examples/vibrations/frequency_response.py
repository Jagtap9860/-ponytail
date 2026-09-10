"""Vibrations: MDOF modes + free-decay numeric vs analytic + FFT verification."""
import math

import numpy as np

from physics_agent.physics import vibrations as V
from physics_agent.solvers.ode import solve_sdof
from physics_agent.solvers.spectral import fft_spectrum
from physics_agent.visualization.plots import plot_fft_spectrum, plot_time_response

# 2-DOF: two 5 kg masses, three 1000 N/m springs
K = np.array([[2000.0, -1000.0], [-1000.0, 2000.0]])
modes = V.mdof_modal(K, np.diag([5.0, 5.0]))
print("modal frequencies [Hz]:", modes["freqs_hz"])
print("mode shapes (columns):\n", modes["shapes"])

# Numeric free decay of mode-1-like SDOF vs analytic wd, verified by FFT
m, k, c = 5.0, 1000.0, 2.0
res = solve_sdof(m, c, k, t_end=10.0, n=10000, x0=0.05)
spec = fft_spectrum(res.y[0], res.t[1] - res.t[0])
wd = math.sqrt(k / m) * math.sqrt(1 - (c / (2 * math.sqrt(k * m))) ** 2)
print(f"FFT peak {spec.peak_freq:.4f} Hz vs analytic wd/2π {wd/2/math.pi:.4f} Hz")
print("decay plot →", plot_time_response(res.t, res.y[0], "/tmp/decay.png"))
print("spectrum  →", plot_fft_spectrum(spec.freqs, spec.amplitude, "/tmp/spectrum.png"))
