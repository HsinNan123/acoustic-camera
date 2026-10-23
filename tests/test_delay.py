import numpy as np
import pytest

from acam.delay import SPEED_OF_SOUND, angle_from_delay, gcc_phat
from acam.sim import fractional_delay, two_mic_plane_wave

FS = 48_000
D = 0.042  # UMA-16 mic spacing, metres


def noise(n=4800, seed=0):
    return np.random.default_rng(seed).standard_normal(n)


def test_gcc_phat_finds_whole_sample_delay():
    x = noise()
    y = np.roll(x, 5)  # y hears the same sound 5 samples later
    assert gcc_phat(y, x, FS) == pytest.approx(5 / FS, abs=0.05 / FS)


def test_gcc_phat_finds_fraction_of_a_sample():
    x = noise()
    y = fractional_delay(x, 2.5 / FS, FS)
    assert gcc_phat(y, x, FS) == pytest.approx(2.5 / FS, abs=0.1 / FS)


def test_angle_from_delay():
    tau = D * np.sin(np.radians(30)) / SPEED_OF_SOUND
    assert angle_from_delay(tau, D) == pytest.approx(30)


def test_angle_from_delay_clips_impossible_delay():
    assert angle_from_delay(1.0, D) == pytest.approx(90)


def test_band_limit_fixes_a_narrow_band_sound():
    t = np.arange(4800) / FS
    whistle = np.sin(2 * np.pi * (2000 + 4000 * t / t[-1] / 2) * t) * np.hanning(len(t))
    for seed in [1, 2, 3]:
        mic0, mic1 = two_mic_plane_wave(whistle, FS, 30, D, snr_db=20, seed=seed)
        tau = gcc_phat(mic0, mic1, FS, max_tau=D / SPEED_OF_SOUND, band=(2000, 6000))
        assert angle_from_delay(tau, D) == pytest.approx(30, abs=2)


@pytest.mark.parametrize("true_deg", [-60, -30, 0, 30, 60])
def test_two_mics_find_the_angle(true_deg):
    mic0, mic1 = two_mic_plane_wave(noise(), FS, true_deg, D, snr_db=20, seed=1)
    tau = gcc_phat(mic0, mic1, FS, max_tau=D / SPEED_OF_SOUND)
    assert angle_from_delay(tau, D) == pytest.approx(true_deg, abs=2)
