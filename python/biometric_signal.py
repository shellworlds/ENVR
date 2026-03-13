# SN-112BA: Biometric signal generation for stress/HR simulation. Main developer: shellworlds.
"""Synthetic biometric signals for stress maps and dashboard POC."""

import numpy as np
from typing import Tuple


def generate_hr_signal(duration_sec: float, fs: float = 64.0, bpm_base: float = 72.0) -> Tuple[np.ndarray, np.ndarray]:
    t = np.arange(0, duration_sec, 1.0 / fs)
    bpm = bpm_base + 5 * np.sin(2 * np.pi * 0.1 * t) + np.random.randn(len(t)) * 2
    signal = np.sin(2 * np.pi * (bpm / 60.0) * t) + 0.1 * np.random.randn(len(t))
    return t, signal


def stress_level_from_hr(hr_signal: np.ndarray, fs: float) -> float:
    hr_est = np.abs(np.fft.rfft(hr_signal))
    freqs = np.fft.rfftfreq(len(hr_signal), 1.0 / fs)
    idx = np.argmax(hr_est[1:]) + 1
    dominant_hz = freqs[idx]
    bpm_est = dominant_hz * 60.0
    stress = max(0, min(1, (bpm_est - 60) / 40.0))
    return stress


if __name__ == "__main__":
    t, sig = generate_hr_signal(10.0)
    s = stress_level_from_hr(sig, 64.0)
    print("Biometric stress index:", round(s, 4))
