"""Microphone layouts and look directions.

The array lies flat in the x-y plane and looks along +z, like a camera:
x is left-right, y is down-up, z is straight ahead.
"""
import numpy as np


def direction(az_deg, el_deg):
    """Unit vector toward a sound at azimuth (right is +) and elevation (up is +)."""
    az, el = np.radians(az_deg), np.radians(el_deg)
    return np.array([np.sin(az) * np.cos(el), np.sin(el), np.cos(az) * np.cos(el)])


def two_mics(d=0.042):
    """Two mics on the x axis, `d` metres apart (chapter 1)."""
    return np.array([[-d / 2, 0, 0], [d / 2, 0, 0]])


def uma16(pitch=0.042):
    """miniDSP UMA-16: a 4x4 grid, `pitch` metres apart, centred on the camera."""
    k = (np.arange(4) - 1.5) * pitch
    xx, yy = np.meshgrid(k, k)
    return np.column_stack([xx.ravel(), yy.ravel(), np.zeros(16)])


def sipeed6(radius=0.040):
    """Sipeed MicArray outer ring: 6 mics on a circle (centre mic unused)."""
    ang = np.radians([90, 30, 330, 270, 210, 150])
    return np.column_stack([radius * np.cos(ang), radius * np.sin(ang), np.zeros(6)])
