import pytest

from acam.camera import degrees_to_pixels, pixels_to_degrees


def test_half_the_frame_is_half_the_view():
    assert pixels_to_degrees(1152, 2304, 57.3) == pytest.approx(28.65)


def test_no_shift_is_no_angle():
    assert pixels_to_degrees(0, 2304, 57.3) == 0


def test_sign_is_kept():
    assert pixels_to_degrees(-300, 2304, 57.3) == pytest.approx(-pixels_to_degrees(300, 2304, 57.3))


def test_small_shift_is_nearly_linear_at_the_centre():
    # 40 px near the centre of a 2304 px, 57.3 deg view is about 40 * 57.3 / 2304 = 0.99 deg,
    # a little more, because a pixel near the centre covers more than the average angle.
    assert pixels_to_degrees(40, 2304, 57.3) == pytest.approx(1.09, abs=0.01)


def test_degrees_to_pixels_undoes_pixels_to_degrees():
    assert degrees_to_pixels(pixels_to_degrees(700, 2304, 57.3), 2304, 57.3) == pytest.approx(700)


def test_one_degree_takes_more_pixels_at_the_edge_than_at_the_centre():
    centre = degrees_to_pixels(1, 2304, 57.3)
    edge = degrees_to_pixels(28, 2304, 57.3) - degrees_to_pixels(27, 2304, 57.3)
    assert edge > 1.2 * centre
