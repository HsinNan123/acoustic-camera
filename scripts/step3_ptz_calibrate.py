"""Step 3a': how many degrees is one ONVIF pan or tilt unit on the Tapo C545D?

Moves the lens by a few small steps, grabs a frame before and after each step, and
measures how far the picture slid (phase correlation). Every move comes from the same
side, after a run-up, so gear slack (backlash) does not hide part of the step. A line
through all steps gives degrees per unit. The slide in pixels becomes
degrees through the telephoto lens's view (datasheet: 57.3 x 31.7 deg). The wide lens
is grabbed too: it must not slide, which shows which stream is the moving lens.
Frames go to out/calib/ (ignored by git). The lens returns to its start.

Run from the project folder: .venv\\Scripts\\python scripts\\step3_ptz_calibrate.py
"""
import os
import sys
import time
from pathlib import Path
from urllib.parse import quote

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"
import cv2  # noqa: E402
import numpy as np  # noqa: E402
from onvif import ONVIFCamera  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from acam.camera import pixels_to_degrees  # noqa: E402
from step3_ptz_test import position, read_env, wait_until_still  # noqa: E402

TELE, WIDE = "stream6", "stream1"  # found by probing streams 1-8; this script confirms it
TELE_FOV = (57.3, 31.7)  # horizontal, vertical, deg (TP-Link datasheet)
STEPS = (0.02, 0.04, 0.06, 0.08, 0.10)
RUN_UP = 0.05  # start each move from this far below the start, to take up gear slack
CROP = slice(80, 1220)  # rows without the timestamp (top) and logo (bottom left)
OUT = Path(__file__).resolve().parents[1] / "out" / "calib"


def grab(base, stream):
    cap = cv2.VideoCapture(base + stream, cv2.CAP_FFMPEG)
    frame = None
    for _ in range(5):  # skip the first frames; they can be from before the move
        ok, f = cap.read()
        if ok:
            frame = f
    cap.release()
    if frame is None:
        sys.exit(f"No video from {stream}")
    return frame


def slide(a, b):
    """Pixels the picture moved from a to b (x right +, y down +), and the match strength."""
    ga, gb = (np.float32(cv2.cvtColor(f[CROP], cv2.COLOR_BGR2GRAY)) for f in (a, b))
    win = cv2.createHanningWindow(ga.shape[::-1], cv2.CV_32F)
    (dx, dy), strength = cv2.phaseCorrelate(ga, gb, win)
    return dx, dy, strength


def move_to(ptz, token, x, y):
    ptz.AbsoluteMove({"ProfileToken": token, "Position": {"PanTilt": {"x": x, "y": y}}})
    wait_until_still(ptz, token)
    time.sleep(1.0)  # let the picture settle after the motor stops


def main():
    env = read_env()
    base = f"rtsp://{quote(env['TAPO_USER'])}:{quote(env['TAPO_PASS'], safe='')}@{env['TAPO_HOST']}:554/"
    cam = ONVIFCamera(env["TAPO_HOST"], int(env.get("TAPO_ONVIF_PORT", 2020)),
                      env["TAPO_USER"], env["TAPO_PASS"])
    ptz = cam.create_ptz_service()
    token = cam.create_media_service().GetProfiles()[0].token
    x0, y0 = position(ptz, token)
    print(f"Start position: ({x0:.4f}, {y0:.4f})")
    OUT.mkdir(parents=True, exist_ok=True)

    results = {"pan": [], "tilt": []}
    try:
        for axis in ("pan", "tilt"):
            for step in STEPS:
                if axis == "pan":
                    move_to(ptz, token, x0 - RUN_UP, y0)
                else:
                    move_to(ptz, token, x0, y0 - RUN_UP)
                move_to(ptz, token, x0, y0)
                tele_a, wide_a = grab(base, TELE), grab(base, WIDE)
                x, y = (x0 + step, y0) if axis == "pan" else (x0, y0 + step)
                move_to(ptz, token, x, y)
                tele_b, wide_b = grab(base, TELE), grab(base, WIDE)
                xr, yr = position(ptz, token)
                moved = (xr - x0) if axis == "pan" else (yr - y0)
                dx, dy, strength = slide(tele_a, tele_b)
                wdx, wdy, _ = slide(wide_a, wide_b)
                px = dx if axis == "pan" else dy
                size = tele_a.shape[1] if axis == "pan" else tele_a.shape[0]  # FOV is for the whole frame
                deg = pixels_to_degrees(px, size, TELE_FOV[0] if axis == "pan" else TELE_FOV[1])
                results[axis].append((moved, deg))
                cv2.imwrite(str(OUT / f"{axis}_{step}_before.jpg"), tele_a)
                cv2.imwrite(str(OUT / f"{axis}_{step}_after.jpg"), tele_b)
                print(f"{axis} +{step}: lens reports +{moved:.4f} units; tele slid "
                      f"({dx:+.0f}, {dy:+.0f}) px, match {strength:.2f} -> {deg:+.2f} deg "
                      f"= {abs(deg) / abs(moved):.1f} deg/unit; wide slid ({wdx:+.0f}, {wdy:+.0f}) px")
    finally:
        move_to(ptz, token, x0, y0)
        print(f"Back at: {position(ptz, token)}")

    for axis, pairs in results.items():
        units, degs = np.array(pairs).T
        slope, offset = np.polyfit(units, degs, 1)
        worst = np.max(np.abs(np.polyval((slope, offset), units) - degs))
        print(f"{axis}: {slope:+.1f} deg per unit, offset {offset:+.2f} deg, worst miss {worst:.2f} deg")


if __name__ == "__main__":
    main()
