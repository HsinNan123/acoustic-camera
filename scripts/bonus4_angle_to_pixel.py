"""Bonus post 4: how does a direction in degrees become a place in the picture?

Compares the C545D's two lenses, shows how many pixels one degree takes across the
telephoto picture, re-measures degrees per ONVIF pan unit from the frames that
step3_ptz_calibrate.py saved in out/calib/ (no camera needed), and shows how little
the gap between the mic board and the lens matters. Writes the bonus 4 figures to
docs/blog/img/ and prints the numbers the post uses.

Lens views from the TP-Link C545D datasheet: telephoto 57.3 x 31.7 deg, wide 137.6 x
73 deg; both streams are 2304 px wide (stream1, stream6).
Run from the project folder: .venv\\Scripts\\python scripts\\bonus4_angle_to_pixel.py
"""
import sys
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Wedge

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from acam.camera import degrees_to_pixels, pixels_to_degrees  # noqa: E402
from step3_ptz_calibrate import STEPS, TELE_FOV, slide  # noqa: E402

WIDTH_PX = 2304
WIDE_FOV = 137.6
BIRD_CM, BIRD_M = 15, 15  # a sparrow-sized bird, 15 m away
MIN_MATCH = 0.03  # phase-correlation strength below this: the two pictures did not match
OUT = Path(__file__).resolve().parents[1] / "docs" / "blog" / "img"
CALIB = Path(__file__).resolve().parents[1] / "out" / "calib"

# Figures are in Traditional Chinese for the blog.
plt.rcParams["font.family"] = ["Microsoft JhengHei", "Noto Sans TC"]
plt.rcParams["axes.unicode_minus"] = False


def px_per_degree(angle_deg, fov_deg):
    """Pixels that one degree takes at `angle_deg` from the centre."""
    return degrees_to_pixels(angle_deg + 0.5, WIDTH_PX, fov_deg) - degrees_to_pixels(angle_deg - 0.5, WIDTH_PX, fov_deg)


def fig_views(path, bird_px):
    fig, ax = plt.subplots(figsize=(7, 4.2))
    r = 20
    ax.add_patch(Wedge((0, 0), r, 90 - WIDE_FOV / 2, 90 + WIDE_FOV / 2, color="C0", alpha=0.18,
                       label=f"廣角鏡頭：一次看 {WIDE_FOV:.0f} 度"))
    ax.add_patch(Wedge((0, 0), r, 90 - TELE_FOV[0] / 2, 90 + TELE_FOV[0] / 2, color="C3", alpha=0.35,
                       label=f"長鏡頭：一次看 {TELE_FOV[0]:.0f} 度"))
    ax.plot(0, 0, "ks", ms=9)
    ax.text(0.8, -0.6, "相機", fontsize=9)
    ax.plot(0, BIRD_M, "*", c="C1", ms=14)
    ax.text(0.8, BIRD_M, f"{BIRD_M} 公尺外的鳥", fontsize=9)
    ax.set_xlim(-21, 21)
    ax.set_ylim(-2, 21)
    ax.set_aspect("equal")
    ax.set_xticks(range(-20, 21, 10))
    ax.set_yticks(range(0, 21, 5))
    ax.set_xlabel("左右（公尺）")
    ax.set_ylabel("往前（公尺）")
    ax.legend(fontsize=8, loc="upper left")
    ax.set_title(f"同樣 {WIDTH_PX} 個像素寬：長鏡頭看得窄，鳥佔 {bird_px[1]:.0f} 個像素；"
                 f"廣角只佔 {bird_px[0]:.0f} 個", fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=150)


def fig_pixels(path):
    half = TELE_FOV[0] / 2
    ang = np.linspace(0, half - 0.5, 200)
    ppd = [px_per_degree(a, TELE_FOV[0]) for a in ang]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(ang, ppd, c="C3", lw=2)
    ax.axhline(WIDTH_PX / TELE_FOV[0], c="0.5", ls="--", lw=1)
    ax.text(1, WIDTH_PX / TELE_FOV[0] + 0.4, "平均", fontsize=9, color="0.4")
    ax.set_xticks(range(0, 31, 5))
    ax.set_xlabel("離畫面中心幾度（長鏡頭，往左右）")
    ax.set_ylabel("1 度佔幾個像素")
    ax.set_ylim(30, 50)
    ax.set_yticks(range(30, 51, 5))
    ax.set_title(f"1 度在畫面中間佔 {ppd[0]:.0f} 個像素，在邊邊佔 {ppd[-1]:.0f} 個", fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    return ppd[0], ppd[-1]


def calibration():
    """Degrees the telephoto picture slid for each pan step, and the match strength."""
    degs, strengths = [], []
    for step in STEPS:
        a, b = (cv2.imread(str(CALIB / f"pan_{step}_{w}.jpg")) for w in ("before", "after"))
        dx, _, strength = slide(a, b)
        degs.append(abs(pixels_to_degrees(dx, a.shape[1], TELE_FOV[0])))
        strengths.append(strength)
    return np.array(STEPS), np.array(degs), np.array(strengths)


def fig_calibration(path, units, degs, ok, slope):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(units[ok], degs[ok], "o", c="C3", ms=8, label="量到的：畫面移了幾度")
    if (~ok).any():
        ax.plot(units[~ok], degs[~ok], "o", c="C3", ms=8, mfc="none", label="兩張照片對不上，不算")
    x = np.linspace(0, 0.11, 10)
    ax.plot(x, slope * x, c="0.4", lw=1, label="直線：每 1 個單位都轉一樣多")
    ax.set_xlim(0, 0.11)
    ax.set_ylim(0, 22)
    ax.set_xticks([0, 0.02, 0.04, 0.06, 0.08, 0.10])
    ax.set_yticks(range(0, 21, 5))
    ax.set_xlabel("叫相機往右轉幾個單位")
    ax.set_ylabel("畫面往左移了幾度")
    ax.legend(fontsize=9, loc="upper left")
    ax.set_title(f"每個點都在同一條直線上：1 個單位 = {slope:.0f} 度", fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=150)


def fig_parallax(path, offsets=(0.1, 0.3, 1.0)):
    dist = np.linspace(2, 30, 200)
    fig, ax = plt.subplots(figsize=(7, 4))
    for off, col in zip(offsets, ("C2", "C0", "C3")):
        ax.plot(dist, np.degrees(np.arctan(off / dist)), c=col, lw=2, label=f"板子離鏡頭 {off * 100:.0f} 公分")
    ax.axhline(TELE_FOV[1] / 2, c="0.5", ls="--", lw=1)
    ax.text(8, TELE_FOV[1] / 2 + 0.4, "差這麼多，鳥就跑出長鏡頭的畫面（上下）", fontsize=8, color="0.4")
    ax.set_xticks(range(0, 31, 5))
    ax.set_yticks(range(0, 21, 5))
    ax.set_ylim(0, 20)
    ax.set_xlabel("鳥離相機幾公尺")
    ax.set_ylabel("板子和鏡頭看到的方向差幾度")
    ax.legend(fontsize=9, loc="center right")
    at10 = np.degrees(np.arctan(offsets[1] / 10))
    ax.set_title(f"板子離鏡頭 {offsets[1] * 100:.0f} 公分、鳥在 10 公尺外：方向只差 {at10:.1f} 度", fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    return at10


def main():
    bird_deg = np.degrees(2 * np.arctan(BIRD_CM / 100 / 2 / BIRD_M))
    bird_px = [degrees_to_pixels(bird_deg / 2, WIDTH_PX, f) * 2 for f in (WIDE_FOV, TELE_FOV[0])]
    print(f"Bird {BIRD_CM} cm at {BIRD_M} m = {bird_deg:.2f} deg: wide {bird_px[0]:.1f} px, tele {bird_px[1]:.1f} px "
          f"({bird_px[1] / bird_px[0]:.1f}x)")
    fig_views(OUT / "bonus4_views.png", bird_px)

    centre, edge = fig_pixels(OUT / "bonus4_pixels.png")
    print(f"Tele: 1 deg = {centre:.1f} px at the centre, {edge:.1f} px at the edge, {WIDTH_PX / TELE_FOV[0]:.1f} on average; "
          f"focal length {degrees_to_pixels(45, WIDTH_PX, TELE_FOV[0]):.0f} px")
    print(f"Example: a bird 10 deg right of centre is {degrees_to_pixels(10, WIDTH_PX, TELE_FOV[0]):.0f} px right "
          f"of centre, at x = {WIDTH_PX / 2 + degrees_to_pixels(10, WIDTH_PX, TELE_FOV[0]):.0f} of {WIDTH_PX}")

    units, degs, strengths = calibration()
    ok = strengths >= MIN_MATCH
    u, d = units[ok], degs[ok]
    slope = float(np.sum(u * d) / np.sum(u ** 2))  # a line through 0: no move, no slide
    worst = float(np.max(np.abs(slope * u - d)))
    for un, de, st in zip(units, degs, strengths):
        print(f"  pan +{un:.2f} unit: picture slid {de:.2f} deg, match {st:.2f}" + ("" if st >= MIN_MATCH else " (not used)"))
    print(f"Pan: {slope:.1f} deg per unit (line through 0), worst miss {worst:.2f} deg; "
          f"0.01 unit = {slope * 0.01:.1f} deg; 20 deg = {20 / slope:.2f} unit")
    fig_calibration(OUT / "bonus4_calibration.png", units, degs, ok, slope)

    at10 = fig_parallax(OUT / "bonus4_parallax.png")
    print(f"Parallax: 30 cm at 10 m = {at10:.1f} deg; 1 m at 5 m = {np.degrees(np.arctan(1 / 5)):.1f} deg; "
          f"tele half height {TELE_FOV[1] / 2:.1f} deg")


if __name__ == "__main__":
    main()
