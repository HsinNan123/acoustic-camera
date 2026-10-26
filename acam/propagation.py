"""How loud a sound still is after it travels: spreading plus air absorption."""
import numpy as np


def air_absorption(freq, temp_c=20.0, rh=70.0, pa_kpa=101.325):
    """Air absorption in dB per metre (ISO 9613-1 formula).

    `rh` is relative humidity in percent. High notes lose much more than low notes.
    """
    f = np.asarray(freq, dtype=float)
    t, t0, t01, pr = temp_c + 273.15, 293.15, 273.16, 101.325
    p = pa_kpa / pr
    h = rh * 10 ** (-6.8346 * (t01 / t) ** 1.261 + 4.6151) / p   # water vapour, percent
    fr_o = p * (24 + 4.04e4 * h * (0.02 + h) / (0.391 + h))
    fr_n = p * (t / t0) ** -0.5 * (9 + 280 * h * np.exp(-4.170 * ((t / t0) ** (-1 / 3) - 1)))
    return 8.686 * f ** 2 * (
        1.84e-11 / p * (t / t0) ** 0.5
        + (t / t0) ** -2.5 * (0.01275 * np.exp(-2239.1 / t) / (fr_o + f ** 2 / fr_o)
                              + 0.1068 * np.exp(-3352.0 / t) / (fr_n + f ** 2 / fr_n)))


def level_at(level_1m, distance_m, freq=None, **air):
    """Sound level (dB) at `distance_m` from a source that is `level_1m` at 1 m.

    Spreading takes 20 log10(distance); with `freq`, air absorption is taken too.
    """
    r = np.asarray(distance_m, dtype=float)
    level = level_1m - 20 * np.log10(r)
    if freq is not None:
        level = level - air_absorption(freq, **air) * (r - 1)
    return level
