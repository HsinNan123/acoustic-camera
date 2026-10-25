import numpy as np
import pytest

from acam.beamform import peak_direction, power_map
from acam.geometry import direction, sipeed6, two_mics, uma16
from acam.sim import plane_wave, two_mic_plane_wave

FS = 48_000
AZ = np.arange(-90, 91, 1.0)
EL = np.arange(-60, 61, 1.0)


def noise(n=1200, seed=0):
    return np.random.default_rng(seed).standard_normal(n)


def tone(freq, n=4800):
    return np.sin(2 * np.pi * freq * np.arange(n) / FS)


def test_uma16_is_a_centred_4x4_grid_42mm_apart():
    m = uma16()
    assert m.shape == (16, 3)
    assert np.allclose(m.mean(axis=0), 0)
    xs = np.unique(np.round(m[:, 0], 6))
    assert np.allclose(np.diff(xs), 0.042)


def test_sipeed6_is_a_circle_of_radius_40mm():
    m = sipeed6()
    assert m.shape == (6, 3)
    assert np.allclose(np.linalg.norm(m, axis=1), 0.040)


def test_direction_is_a_unit_vector_straight_ahead_at_zero():
    assert np.allclose(direction(0, 0), [0, 0, 1])
    assert np.isclose(np.linalg.norm(direction(30, -20)), 1)


def test_plane_wave_matches_the_two_mic_simulator():
    src = noise()
    a = plane_wave(src, FS, two_mics(0.042), 30, 0)
    b = np.array(two_mic_plane_wave(src, FS, 30, 0.042))
    assert np.allclose(a, b, atol=1e-9)


def test_uma16_finds_a_noise_source_in_two_dimensions():
    sig = plane_wave(noise(), FS, uma16(), 20, 10, snr_db=20, seed=1)
    az, el = peak_direction(power_map(sig, FS, uma16(), AZ, EL, phat=True), AZ, EL)
    assert az == pytest.approx(20, abs=3) and el == pytest.approx(10, abs=3)


@pytest.mark.parametrize("freq", [1000, 2000, 4000])
def test_uma16_finds_a_tone(freq):
    sig = plane_wave(tone(freq), FS, uma16(), 20, 10, snr_db=20, seed=1)
    p = power_map(sig, FS, uma16(), AZ, EL, band=(freq - 100, freq + 100))
    az, el = peak_direction(p, AZ, EL)
    assert az == pytest.approx(20, abs=3) and el == pytest.approx(10, abs=3)


def test_power_map_is_scaled_to_one_at_the_peak():
    sig = plane_wave(noise(), FS, sipeed6(), -30, 0, snr_db=20, seed=2)
    p = power_map(sig, FS, sipeed6(), AZ, EL)
    assert p.shape == (len(EL), len(AZ))
    assert p.max() == pytest.approx(1)
