"""Time delay between two microphones, and the angle it implies."""
import numpy as np

SPEED_OF_SOUND = 343.0  # m/s in air at 20 C


def gcc_phat(sig, ref, fs, max_tau=None, interp=16, band=None):
    """Delay of `sig` relative to `ref`, in seconds. Positive: `sig` hears it later.

    GCC-PHAT: cross-correlate in the frequency domain, keep only the phase, so the
    peak is sharp whatever the sound's spectrum. `interp` zero-pads the inverse FFT
    to read the peak between samples. `band` (low_hz, high_hz) drops the other
    frequencies: PHAT weights every frequency equally, so bands with only noise
    pull the peak away.
    """
    n = len(sig) + len(ref)
    cross = np.fft.rfft(sig, n) * np.conj(np.fft.rfft(ref, n))
    cross /= np.abs(cross) + 1e-12
    if band is not None:
        f = np.fft.rfftfreq(n, 1 / fs)
        cross[(f < band[0]) | (f > band[1])] = 0
    cc = np.fft.irfft(cross, n * interp)

    max_shift = n * interp // 2
    if max_tau is not None:
        max_shift = min(int(np.ceil(interp * fs * max_tau)), max_shift)
    cc = np.concatenate((cc[-max_shift:], cc[: max_shift + 1]))
    return (np.argmax(np.abs(cc)) - max_shift) / (interp * fs)


def angle_from_delay(tau, d, c=SPEED_OF_SOUND):
    """Angle in degrees from broadside, for two mics `d` metres apart.

    0 is straight ahead. Positive is toward the mic that hears the sound first.
    """
    return np.degrees(np.arcsin(np.clip(c * tau / d, -1.0, 1.0)))
