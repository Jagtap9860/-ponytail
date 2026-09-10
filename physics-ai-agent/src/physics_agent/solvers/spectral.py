"""Spectral analysis: FFT spectra, windowing helpers."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Spectrum:
    """Single-sided amplitude spectrum with peak location."""
    freqs: np.ndarray
    amplitude: np.ndarray  # single-sided amplitude spectrum (same units as signal)
    peak_freq: float
    peak_amplitude: float


def fft_spectrum(signal: np.ndarray, dt: float, window: str | None = "hann") -> Spectrum:
    """Single-sided amplitude spectrum of a uniformly sampled signal."""
    x = np.asarray(signal, dtype=float)
    n = x.size
    w = np.ones(n) if window is None else np.hanning(n)
    coh_gain = float(np.mean(w))
    X = np.fft.rfft(x * w)
    amp = 2.0 * np.abs(X) / (n * coh_gain)
    amp[0] /= 2.0
    if n % 2 == 0:
        amp[-1] /= 2.0
    freqs = np.fft.rfftfreq(n, dt)
    i = int(np.argmax(amp[1:]) + 1) if amp.size > 1 else 0
    return Spectrum(freqs, amp, float(freqs[i]), float(amp[i]))
