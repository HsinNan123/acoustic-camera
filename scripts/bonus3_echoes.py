"""Bonus post 3: do echoes from the ground and the wall fool the microphones?

An echo off a flat surface sounds as if it came from the bird's mirror image behind
that surface. The board hangs on the house wall, 3 m above paved ground; the bird
sits in a tree 12 m away. The script draws the side view, the map with the ground
echo, the map from only the first few milliseconds of the call, and the map with the
wall echo. Writes the bonus 3 figures to docs/blog/img/ and prints the numbers the
post uses.

Assumed (not measured): paving reflects 90 % of the sound pressure, the wall 95 %;
the board is 5 cm in front of the wall.
Run from the project folder: .venv\\Scripts\\python scripts\\bonus3_echoes.py
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import chirp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from acam.beamform import peak_direction, power_map  # noqa: E402
from acam.delay import SPEED_OF_SOUND  # noqa: E402
from acam.geometry import direction, mirror, sipeed6  # noqa: E402
from acam.sim import point_source  # noqa: E402

FS = 48_000
AZ = np.arange(-90, 91, 1.0)
EL = np.arange(-60, 61, 1.0)
BAND = (2000, 8000)
BIRD_DIR, BIRD_DIST = (20, 10), 12.0
HEIGHT = 3.0  # board above the ground, m
WALL_GAP = 0.05  # board in front of the wall, m
GROUND_REFLECT, WALL_REFLECT = 0.9, 0.95
GATE_MS = 5
SNR_DB = 20
OUT = Path(__file__).resolve().parents[1] / "docs" / "blog" / "img"

# Board at the origin, looking along +z (the garden); y is up (geometry.py).
GROUND = ([0, -HEIGHT, 0], [0, 1, 0])
WALL = ([0, 0, -WALL_GAP], [0, 0, 1])

# Figures are in Traditional Chinese for the blog.
plt.rcParams["font.family"] = ["Microsoft JhengHei", "Noto Sans TC"]
plt.rcParams["axes.unicode_minus"] = False


def bird_call(notes=4, note_ms=20, every_ms=40, total=12_000):
    """A trill: short notes sliding from high to low (8 to 2 kHz), each with a sharp start."""
    n = note_ms * FS // 1000
    t = np.arange(n) / FS
    env = np.minimum(1, np.minimum(t / 0.0005, (t[-1] - t) / 0.002))
    note = chirp(t, f0=BAND[1], t1=t[-1], f1=BAND[0]) * env
    call = np.zeros(total)
    for i in range(notes):
        k = i * every_ms * FS // 1000
        call[k:k + n] = note
    return call


def record(surfaces, seed=1):
    """Mic signals: the bird plus one echo per (plane, reflection) surface, plus noise."""
    mics, call = sipeed6(), bird_call()
    bird = BIRD_DIST * direction(*BIRD_DIR)
    sig = point_source(call, FS, mics, bird)
    for plane, k in surfaces:
        sig = sig + k * point_source(call, FS, mics, mirror(bird, *plane))
    noise_rms = np.std(sig[:, sig.std(axis=0) > 0]) * 10 ** (-SNR_DB / 20)
    return sig + np.random.default_rng(seed).normal(0, noise_rms, sig.shape)


def onset(sig, frac=0.1):
    """First sample where the sound starts (envelope above `frac` of its peak), minus 1 ms."""
    env = np.convolve(np.abs(sig).mean(axis=0), np.ones(48) / 48, mode="same")
    return max(0, int(np.argmax(env > frac * env.max())) - FS // 1000)


def to_dir(p):
    """(azimuth, elevation) in degrees of a point seen from the board."""
    x, y, z = p
    return np.degrees(np.arctan2(x, z)), np.degrees(np.arctan2(y, np.hypot(x, z)))


def bmap(sig):
    return power_map(sig, FS, sipeed6(), AZ, EL, band=BAND, phat=True)


def value_at(pmap, d):
    return pmap[np.argmin(np.abs(EL - round(d[1]))), np.argmin(np.abs(AZ - round(d[0])))]


def show_map(ax, pmap, title, marks):
    im = ax.imshow(pmap, origin="lower", extent=[AZ[0], AZ[-1], EL[0], EL[-1]], cmap="turbo",
                   vmin=0, vmax=1, aspect="auto")
    for (az, el), mk in marks:
        ax.plot(az, el, mk, ms=12, mew=2, mfc="none")
    ax.set_title(title, fontsize=10)
    ax.set_xticks(range(-90, 91, 30))
    ax.set_yticks(range(-60, 61, 30))
    ax.set_xlabel("左右（度，右邊是正）")
    ax.set_ylabel("上下（度，上面是正）")
    return im


def fig_side(path, bird, echo):
    """Side view: the board on the wall, the bird in the tree, the bounce and the mirror bird."""
    fig, ax = plt.subplots(figsize=(7, 4.6))
    h = np.hypot(bird[0], bird[2])  # distance along the ground
    gy = -HEIGHT
    ax.axhspan(gy - 12, gy, color="0.88")
    ax.axhline(gy, c="0.4", lw=2)
    ax.text(h * 0.55, gy - 0.6, "地面（會反射聲音）", fontsize=9, color="0.3")
    ax.plot([-WALL_GAP - 0.3] * 2, [gy, bird[1] + 2.5], c="0.4", lw=6)
    ax.text(-1.9, gy + 1, "牆", fontsize=10, color="0.3")
    ax.plot(0, 0, "s", c="C2", ms=10)
    ax.text(0.3, 0.4, "麥克風板", fontsize=9, color="C2")
    ax.plot(h, bird[1], "o", c="C3", ms=10)
    ax.text(h + 0.3, bird[1] + 0.3, "鳥", fontsize=10, color="C3")
    ax.plot(h, echo[1], "o", c="C3", ms=10, mfc="none", mew=2)
    ax.text(h + 0.3, echo[1] - 0.2, "鏡子裡的假鳥\n（回音好像從這裡來）", fontsize=9, color="C3")
    ax.plot([0, h], [0, bird[1]], c="C3", lw=2, label="直接來的聲音（先到）")
    t = (bird[1] - gy) / (bird[1] - echo[1])  # where the line to the mirror bird hits the ground
    bounce = (h * (1 - t), gy)
    ax.plot([h, bounce[0], 0], [bird[1], gy, 0], c="C1", lw=2, label="碰到地面再彈回來的回音（晚到）")
    ax.plot([bounce[0], h], [gy, echo[1]], c="C1", lw=1.5, ls=":")
    ax.set_xlim(-2.5, h + 4.5)
    ax.set_ylim(echo[1] - 1.5, bird[1] + 2.5)
    ax.set_aspect("equal")
    ax.set_xlabel("離牆幾公尺")
    ax.set_ylabel("比麥克風板高幾公尺")
    ax.legend(fontsize=8, loc="upper left")
    ax.set_title("回音像從地面下「鏡子裡的假鳥」傳來，而且比較晚到", fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=150)


def main():
    bird = BIRD_DIST * direction(*BIRD_DIR)
    ground_echo = mirror(bird, *GROUND)
    echo_dir = to_dir(ground_echo)
    extra = np.linalg.norm(ground_echo) - BIRD_DIST
    print(f"Bird at {BIRD_DIST} m, ({BIRD_DIR[0]}, {BIRD_DIR[1]}) deg, {bird[1] + HEIGHT:.1f} m above ground")
    print(f"Ground echo seems to come from ({echo_dir[0]:.0f}, {echo_dir[1]:.0f}) deg; path {extra:.2f} m longer = "
          f"{extra / SPEED_OF_SOUND * 1000:.1f} ms later; "
          f"{20 * np.log10(GROUND_REFLECT * BIRD_DIST / np.linalg.norm(ground_echo)):.1f} dB vs the bird")
    fig_side(OUT / "bonus3_side.png", bird, ground_echo)

    marks = [(BIRD_DIR, "w+"), (echo_dir, "wo")]
    clean = bmap(record([]))
    print(f"No echo: peak at {peak_direction(clean, AZ, EL)}")

    sig = record([(GROUND, GROUND_REFLECT)])
    whole = bmap(sig)
    k = onset(sig)
    gated = bmap(sig[:, k:k + GATE_MS * FS // 1000])
    for name, m in [("Whole call", whole), (f"First {GATE_MS} ms", gated)]:
        print(f"{name}: peak at {peak_direction(m, AZ, EL)}; bird {value_at(m, BIRD_DIR):.2f}, "
              f"echo spot {value_at(m, echo_dir):.2f}")
    print(f"Onset found at {k / FS * 1000:.1f} ms (direct sound arrives at {BIRD_DIST / SPEED_OF_SOUND * 1000:.1f} ms)")

    fig, ax = plt.subplots(figsize=(6, 4.2))
    im = show_map(ax, whole, "", marks)
    fig.colorbar(im, ax=ax, label="對齊程度（1 = 最整齊）")
    ax.set_title("最紅的還是鳥；地面下的假鳥，只多出一團淡淡的亮光（＋是鳥，○是假鳥）", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "bonus3_ground.png", dpi=150)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    show_map(axes[0], whole, "聽整段叫聲：假鳥有一團淡淡的亮光", marks)
    im = show_map(axes[1], gated, f"只聽最前面 {GATE_MS} 毫秒：回音還沒到，只剩鳥", marks)
    fig.colorbar(im, ax=axes, label="對齊程度", shrink=0.9)
    fig.suptitle("只聽叫聲最前面的一小段，地面回音的亮光就變淡了（＋是鳥，○是假鳥）", fontsize=11, y=1.03)
    fig.savefig(OUT / "bonus3_gate.png", dpi=150, bbox_inches="tight")

    wall_echo = mirror(bird, *WALL)
    wall_extra = np.linalg.norm(wall_echo) - BIRD_DIST
    wall = bmap(record([(WALL, WALL_REFLECT)]))
    print(f"Wall echo: path {wall_extra * 100:.1f} cm longer = {wall_extra / SPEED_OF_SOUND * 1000:.2f} ms later; "
          f"seems to come from behind, mirror of ({to_dir(wall_echo)[0]:.0f}, {to_dir(wall_echo)[1]:.0f}) deg; "
          f"map peak at {peak_direction(wall, AZ, EL)}")
    lag = wall_extra / SPEED_OF_SOUND
    notches = [(2 * k + 1) / (2 * lag) for k in range(3)]
    print("Wall echo cancels these frequencies: " + ", ".join(f"{f / 1000:.1f} kHz" for f in notches))
    fig, ax = plt.subplots(figsize=(6, 4.2))
    im = show_map(ax, wall, "", [(BIRD_DIR, "w+")])
    fig.colorbar(im, ax=ax, label="對齊程度（1 = 最整齊）")
    ax.set_title("板子貼著牆裝：牆的回音和鳥落在同一個紅點（白色＋是鳥）", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / "bonus3_wall.png", dpi=150)


if __name__ == "__main__":
    main()
