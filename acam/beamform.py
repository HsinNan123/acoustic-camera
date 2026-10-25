"""Sound maps from many mics: delay-and-sum beamforming.

For every look direction, shift each mic's signal by the delay that direction would
cause, add them up, and measure the power. If the guess is right the shifted signals
line up and add; if wrong they partly cancel.
"""
import numpy as np

from acam.delay import SPEED_OF_SOUND
from acam.geometry import direction


def power_map(signals, fs, mics, az_grid, el_grid, band=None, phat=False, c=SPEED_OF_SOUND):
    """Power for every (elevation, azimuth) on the grid, scaled so the peak is 1.

    `signals` has one row per mic. `band` (low_hz, high_hz) keeps only those
    frequencies. `phat` gives every frequency the same weight (as in GCC-PHAT).
    """
    spec = np.fft.rfft(signals, axis=1)
    f = np.fft.rfftfreq(signals.shape[1], 1 / fs)
    keep = f > 0
    if band is not None:
        keep &= (f >= band[0]) & (f <= band[1])
    spec, f = spec[:, keep], f[keep]
    if phat:
        spec = spec / (np.abs(spec) + 1e-12)

    out = np.empty((len(el_grid), len(az_grid)))
    for i, el in enumerate(el_grid):
        u = np.array([direction(az, el) for az in az_grid])        # (A, 3)
        tau = -(u @ mics.T) / c                                     # (A, M) delay each mic heard
        steer = np.exp(2j * np.pi * tau[:, :, None] * f[None, None, :])  # undo the delay
        out[i] = np.sum(np.abs(np.einsum("mf,amf->af", spec, steer)) ** 2, axis=1)
    return out / out.max()


def peak_direction(pmap, az_grid, el_grid):
    """(azimuth, elevation) of the highest point of a power map."""
    i, j = np.unravel_index(np.argmax(pmap), pmap.shape)
    return az_grid[j], el_grid[i]
