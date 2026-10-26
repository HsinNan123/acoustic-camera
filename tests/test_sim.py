import numpy as np
import pytest

from acam.delay import SPEED_OF_SOUND, gcc_phat
from acam.geometry import direction, mirror, two_mics
from acam.sim import plane_wave, point_source

FS = 48_000


def noise(n=4800, seed=0):
    return np.random.default_rng(seed).standard_normal(n)


def test_far_point_source_matches_a_plane_wave():
    mics, src = two_mics(), np.concatenate([noise(), np.zeros(1000)])
    near = point_source(src, FS, mics, 5 * direction(30, 0))
    far = plane_wave(src, FS, mics, 30, 0)
    tau_near = gcc_phat(near[1], near[0], FS)
    tau_far = gcc_phat(far[1], far[0], FS)
    assert tau_near == pytest.approx(tau_far, abs=1e-6)


def test_point_source_is_later_and_quieter_farther_away():
    mics = np.array([[0, 0, 0], [0, 0, 1.0]])  # second mic 1 m nearer the source
    src = np.zeros(4800)
    src[100] = 1
    sig = point_source(src, FS, mics, [0, 0, 3.0])
    assert np.argmax(sig[0]) - np.argmax(sig[1]) == round(1 / SPEED_OF_SOUND * FS)
    assert sig[1].max() / sig[0].max() == pytest.approx(1.5, rel=0.05)


def test_mirror_in_the_ground():
    assert np.allclose(mirror([2, 5, 10], [0, -3, 0], [0, 1, 0]), [2, -11, 10])
