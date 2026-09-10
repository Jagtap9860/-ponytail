"""Eigenvalue solvers: standard + generalized (modal analysis [K]{φ}=λ[M]{φ})."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import linalg as _la


@dataclass
class EigenResult:
    eigenvalues: np.ndarray       # ascending, real for symmetric problems
    eigenvectors: np.ndarray      # columns; mass-normalized if M given
    natural_freq_hz: np.ndarray   # sqrt(λ)/2π for vibration problems


def modal_analysis(A: np.ndarray, symmetric: bool = True) -> EigenResult:
    A = np.asarray(A, dtype=float)
    if symmetric:
        w, v = _la.eigh(A)
    else:
        w, v = _la.eig(A)
        w, v = np.real(w), np.real(v)
        idx = np.argsort(w)
        w, v = w[idx], v[:, idx]
    freq = np.sqrt(np.clip(w, 0, None)) / (2 * np.pi)
    return EigenResult(w, v, freq)


def generalized_eigen(K: np.ndarray, M: np.ndarray) -> EigenResult:
    """Solve [K]{φ} = λ[M]{φ} for symmetric positive (semi)definite M."""
    K = np.asarray(K, dtype=float)
    M = np.asarray(M, dtype=float)
    w, v = _la.eigh(K, M)
    # eigh with M already returns M-orthonormal vectors; enforce ascending order
    idx = np.argsort(w)
    w, v = w[idx], v[:, idx]
    freq = np.sqrt(np.clip(w, 0, None)) / (2 * np.pi)
    return EigenResult(w, v, freq)
