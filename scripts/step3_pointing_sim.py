"""Step 3: can the Sipeed ring point the C545D telephoto lens (57.3 x 31.7 deg) at a bird?

Bird song 2-8 kHz, 0.1 s, at 20 deg right and 10 deg up; 40 runs per noise level.
"In frame": the bird lands inside the telephoto view. "Near centre": within 10 deg
left-right and 5 deg up-down. Prints the numbers the bonus post and step 3 use, and
draws where the Sipeed ring pointed at -20 dB (docs/blog/img/bonus1_pointing.png).
Run from the project folder: .venv\\Scripts\\python scripts\\step3_pointing_sim.py
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from scipy.signal import chirp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from acam.beamform import peak_direction, power_map  # noqa: E402
from acam.geometry import sipeed6, uma16  # noqa: E402
from acam.sim import plane_wave  # noqa: E402

FS = 48_000
AZ = np.arange(-90, 91, 2.0)
EL = np.arange(-60, 61, 2.0)
BIRD = (20, 10)
HALF_VIEW = (57.3 / 2, 31.7 / 2)  # telephoto view, deg (TP-Link datasheet)
CENTRE = (10, 5)  # "near centre" box, deg
OUT = Path(__file__).resolve().parents[1] / "docs" / "blog" / "img"

# Figures are in Traditional Chinese for the blog.
plt.rcParams["font.family"] = ["Microsoft JhengHei", "Noto Sans TC"]
plt.rcParams["axes.unicode_minus"] = False


def bird_song(n=4800):
    t = np.arange(n) / FS
    return chirp(t, f0=2000, t1=t[-1], f1=8000) * np.hanning(n)


def fig_pointing(path, guesses, in_frame, centre):
    fig, ax = plt.subplots(figsize=(7, 4.2))
    (x0, y0), (hx, hy), (cx, cy) = BIRD, HALF_VIEW, CENTRE
    ax.add_patch(Rectangle((x0 - hx, y0 - hy), 2 * hx, 2 * hy, fill=False, lw=2, ec="C0",
                           label="長鏡頭一次看得到的範圍"))
    ax.add_patch(Rectangle((x0 - cx, y0 - cy), 2 * cx, 2 * cy, fill=False, lw=1.5, ls="--",
                           ec="C2", label="畫面正中間附近"))
    ax.scatter(guesses[:, 0], guesses[:, 1], s=40, c="0.3", alpha=0.35, label="彈弓指的方向（40 次）")
    ax.plot(*BIRD, "*", ms=16, c="C3", label="鳥真正的位置")
    ax.set_xlim(x0 - hx - 6, x0 + hx + 6)
    ax.set_ylim(y0 - hy - 4, y0 + hy + 4)
    ax.set_aspect("equal")
    ax.set_xticks(range(-10, 51, 10))
    ax.set_yticks(range(-10, 31, 10))
    ax.set_xlabel("左右（度，右邊是正）")
    ax.set_ylabel("上下（度，上面是正）")
    ax.legend(fontsize=8, loc="upper left", bbox_to_anchor=(1.01, 1))
    ax.set_title(f"就算雜訊大 100 倍，鳥 {in_frame:.0f}% 都在長鏡頭的畫面裡", fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=150)


def main():
    song = bird_song()
    for name, mics in [("Sipeed6", sipeed6()), ("UMA16", uma16())]:
        for snr in (10, 0, -10, -20):
            errs, guesses = [], []
            for s in range(40):
                sig = plane_wave(song, FS, mics, *BIRD, snr_db=snr, seed=s)
                p = power_map(sig, FS, mics, AZ, EL, band=(2000, 8000), phat=True)
                az, el = peak_direction(p, AZ, EL)
                guesses.append((az, el))
                errs.append((abs(az - BIRD[0]), abs(el - BIRD[1])))
            e = np.array(errs)
            in_frame = np.mean((e[:, 0] <= HALF_VIEW[0]) & (e[:, 1] <= HALF_VIEW[1])) * 100
            centre = np.mean((e[:, 0] <= CENTRE[0]) & (e[:, 1] <= CENTRE[1])) * 100
            if name == "Sipeed6" and snr == -20:
                fig_pointing(OUT / "bonus1_pointing.png", np.array(guesses), in_frame, centre)
                print(f"Sipeed6 -20 dB: {len(set(guesses))} different directions among 40 runs")
            print(f"{name} snr {snr:>3} dB: in tele frame {in_frame:5.1f}%  near centre {centre:5.1f}%  "
                  f"median err az {np.median(e[:, 0]):.0f} el {np.median(e[:, 1]):.0f}")


if __name__ == "__main__":
    main()
