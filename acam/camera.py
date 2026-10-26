"""Camera geometry: turn a shift in the picture into an angle."""
import numpy as np


def pixels_to_degrees(shift_px, size_px, fov_deg):
    """Angle from the picture centre to a point `shift_px` away (pinhole lens).

    `size_px` is the frame width (or height) and `fov_deg` the view across it.
    """
    focal_px = (size_px / 2) / np.tan(np.radians(fov_deg) / 2)
    return float(np.degrees(np.arctan(shift_px / focal_px)))


def degrees_to_pixels(angle_deg, size_px, fov_deg):
    """Pixels from the picture centre for a point `angle_deg` off the lens axis (pinhole lens)."""
    focal_px = (size_px / 2) / np.tan(np.radians(fov_deg) / 2)
    return float(focal_px * np.tan(np.radians(angle_deg)))
