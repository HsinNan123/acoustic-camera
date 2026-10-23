"""Simulated microphone signals: no hardware needed."""
import numpy as np

from acam.delay import SPEED_OF_SOUND


def fractional_delay(x, tau, fs):
    """`x` delayed by `tau` seconds, any fraction of a sample (circular)."""
    n = len(x)
    f = np.fft.rfftfreq(n, 1 / fs)
    return np.fft.irfft(np.fft.rfft(x) * np.exp(-2j * np.pi * f * tau), n)


def two_mic_plane_wave(source, fs, angle_deg, d, snr_db=None, seed=None, c=SPEED_OF_SOUND):
    """Signals at mic0 (x = -d/2) and mic1 (x = +d/2) from a far source.

    `angle_deg` is from broadside; positive is toward mic1, so mic1 hears it first.
    """
    tau = d / 2 * np.sin(np.radians(angle_deg)) / c
    mic0 = fractional_delay(source, +tau, fs)
    mic1 = fractional_delay(source, -tau, fs)
    if snr_db is not None:
        rng = np.random.default_rng(seed)
        noise_rms = np.std(source) * 10 ** (-snr_db / 20)
        mic0 = mic0 + rng.normal(0, noise_rms, len(mic0))
        mic1 = mic1 + rng.normal(0, noise_rms, len(mic1))
    return mic0, mic1
