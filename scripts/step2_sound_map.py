"""Step 2: many simulated mics draw a sound map; compare two boards.

Writes the chapter 2 figures to docs/blog/img/ and prints the numbers the post uses.
Run from the project folder: .venv\\Scripts\\python scripts\\step2_sound_map.py
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import chirp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from acam.beamform import peak_direction, power_map  # noqa: E402
from acam.delay import SPEED_OF_SOUND  # noqa: E402
from acam.geometry import direction, sipeed6, two_mics, uma16  # noqa: E402
from acam.sim import fractional_delay, plane_wave  # noqa: E402

FS = 48_000
AZ = np.arange(-90, 91, 1.0)
EL = np.arange(-60, 61, 1.0)
BIRD_AZ, BIRD_EL = 20, 10
BIRD_BAND = (2000, 8000)
OUT = Path(__file__).resolve().parents[1] / "docs" / "blog" / "img"
BOARDS = [("2 支麥克風", two_mics()), ("Sipeed 6 支（圓形）", sipeed6()), ("UMA-16 16 支（方格）", uma16())]

# Figures are in Traditional Chinese for the blog.
plt.rcParams["font.family"] = ["Microsoft JhengHei", "Noto Sans TC"]
plt.rcParams["axes.unicode_minus"] = False


def bird_song(n=4800):
    t = np.arange(n) / FS
    return chirp(t, f0=BIRD_BAND[0], t1=t[-1], f1=BIRD_BAND[1]) * np.hanning(n)


def tone(freq, n=4800):
    return np.sin(2 * np.pi * freq * np.arange(n) / FS)


def bird_map(mics, seed=1):
    sig = plane_wave(bird_song(), FS, mics, BIRD_AZ, BIRD_EL, snr_db=20, seed=seed)
    return power_map(sig, FS, mics, AZ, EL, band=BIRD_BAND, phat=True)


def tone_map(mics, freq, seed=1):
    sig = plane_wave(tone(freq), FS, mics, BIRD_AZ, BIRD_EL, snr_db=20, seed=seed)
    return power_map(sig, FS, mics, AZ, EL, band=(freq - 100, freq + 100))


def spot_size(pmap):
    """Width and height (deg) of the area at half power or more around the peak."""
    i, j = np.unravel_index(np.argmax(pmap), pmap.shape)
    row, col = pmap[i] >= 0.5, pmap[:, j] >= 0.5

    def run(mask, k):
        lo = hi = k
        while lo > 0 and mask[lo - 1]:
            lo -= 1
        while hi < len(mask) - 1 and mask[hi + 1]:
            hi += 1
        return hi - lo + 1

    return run(row, j), run(col, i)


def ghost_level(pmap, keep_out=15):
    """Brightest point farther than `keep_out` deg from the peak, as % of the peak."""
    az0, el0 = peak_direction(pmap, AZ, EL)
    far = (np.abs(AZ[None, :] - az0) > keep_out) | (np.abs(EL[:, None] - el0) > keep_out)
    return 100 * pmap[far].max()


def show_map(ax, pmap, title):
    im = ax.imshow(pmap, origin="lower", extent=[AZ[0], AZ[-1], EL[0], EL[-1]], cmap="turbo",
                   vmin=0, vmax=1, aspect="auto")
    ax.plot(BIRD_AZ, BIRD_EL, "w+", ms=12, mew=2)
    ax.set_title(title, fontsize=10)
    ax.set_xticks([-90, -45, 0, 45, 90])
    ax.set_yticks([-60, -30, 0, 30, 60])
    return im


def fig_layout(path):
    """Two mics in a line have only a left-right distance; a grid has up-down too."""
    fig, axes = plt.subplots(1, 2, figsize=(7, 4.4), sharex=True, sharey=True)
    for ax, mics, title in [(axes[0], two_mics(), "排成一條線（2 支）：只分得出左右"),
                            (axes[1], uma16(), "排成一個面（UMA-16）：上下也分得出")]:
        cm = mics * 100
        ax.plot(cm[:, 0], cm[:, 1], "o", ms=9, color="C0")
        x0, x1, y0, y1 = cm[:, 0].min(), cm[:, 0].max(), cm[:, 1].min(), cm[:, 1].max()
        ax.annotate("", xy=(x1, -9), xytext=(x0, -9), arrowprops=dict(arrowstyle="<->", color="C1", lw=2))
        ax.text(0, -10.5, "左右有距離", ha="center", va="top", fontsize=9, color="C1")
        if len(mics) > 2:
            ax.annotate("", xy=(-9, y1), xytext=(-9, y0), arrowprops=dict(arrowstyle="<->", color="C2", lw=2))
            ax.text(-10.5, 0, "上下也有距離", ha="right", va="center", fontsize=9, color="C2", rotation=90)
        else:
            ax.text(-10.5, 0, "上下沒有距離", ha="right", va="center", fontsize=9, color="0.5", rotation=90)
        ax.set_title(title, fontsize=10)
        ax.set_aspect("equal")
        ax.set_xlim(-14, 10)
        ax.set_ylim(-14, 10)
        ax.set_xticks(range(-10, 11, 5))
        ax.set_yticks(range(-10, 11, 5))
        ax.set_xlabel("左右（公分）")
    axes[0].set_ylabel("上下（公分）")
    fig.suptitle("麥克風要排成一個面，才分得出上下", fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=150)


def fig_lineup(path):
    """Shift-and-add for a right and a wrong guess, four mics in a row."""
    mics = uma16()[:4]  # one row: x = -6.3, -2.1, 2.1, 6.3 cm
    n = 960
    t = np.arange(n) / FS
    pulse = np.sin(2 * np.pi * 3000 * (t - 0.01)) * np.exp(-(((t - 0.01) / 0.0004) ** 2))
    sig = plane_wave(pulse, FS, mics, 40, 0)
    t_us = (t - 0.01) * 1e6
    fig, axes = plt.subplots(1, 2, figsize=(7, 4.2), sharey=True)
    for ax, guess, title in [(axes[0], 40, "猜 40 度（猜對）"), (axes[1], -20, "猜 -20 度（猜錯）")]:
        u = direction(guess, 0)
        shifted = [fractional_delay(s, (p @ u) / SPEED_OF_SOUND, FS) for s, p in zip(sig, mics)]
        for k, s in enumerate(shifted):
            ax.plot(t_us, s + 3 * (4 - k), color=f"C{k}", lw=1.2)
            ax.text(-560, 3 * (4 - k), f"mic {k + 1}", fontsize=8, va="center", ha="right")
        total = np.sum(shifted, axis=0) / 2
        ax.plot(t_us, total - 1.5, "k", lw=1.8)
        ax.text(-560, -1.5, "加起來", fontsize=8, va="center", ha="right")
        ax.set_xlim(-500, 500)
        ax.set_title(f"{title}\n加起來最大 {np.abs(total).max() * 2 / 4:.0%}", fontsize=10)
        ax.set_xlabel("時間（微秒）")
        ax.set_yticks([])
        for side in ("left", "right", "top"):
            ax.spines[side].set_visible(False)
    fig.suptitle("猜對方向：四支的波形對齊，加起來很大；猜錯：對不齊，互相抵消", fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    return None


def fig_map(path, pmap):
    fig, ax = plt.subplots(figsize=(6, 4.2))
    im = show_map(ax, pmap, "")
    ax.set_title("UMA-16 掃過每個方向：最紅的地方就是鳥（白色＋是鳥真正的位置）", fontsize=10)
    ax.set_xlabel("左右角度（度）：← 左　右 →")
    ax.set_ylabel("上下角度（度）：↓ 下　上 ↑")
    cb = fig.colorbar(im, ax=ax)
    cb.set_label("對齊程度（1 = 最整齊）")
    fig.tight_layout()
    fig.savefig(path, dpi=150)


def fig_frequency(path, maps, sizes):
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.6), sharey=True)
    for ax, (freq, pmap), (w, h) in zip(axes, maps, sizes):
        im = show_map(ax, pmap, f"{freq // 1000} kHz 的音：紅點寬 {w} 度")
        ax.set_xlabel("左右角度（度）")
    axes[0].set_ylabel("上下角度（度）")
    fig.colorbar(im, ax=axes, label="對齊程度", shrink=0.9)
    fig.suptitle("音越低，紅點越大越模糊；音越高，紅點越小越清楚（UMA-16）", fontsize=11, y=1.03)
    fig.savefig(path, dpi=150, bbox_inches="tight")


def fig_ghost(path, tone_pmap, bird_pmap, ghost_tone, ghost_bird):
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.8), sharey=True)
    show_map(axes[0], tone_pmap, f"只有 8 kHz 一個音：鬼影有真的 {ghost_tone:.0f}% 亮")
    im = show_map(axes[1], bird_pmap, f"鳥叫（2 到 8 kHz）：鬼影只剩 {ghost_bird:.0f}%")
    for ax in axes:
        ax.set_xlabel("左右角度（度）")
    axes[0].set_ylabel("上下角度（度）")
    fig.colorbar(im, ax=axes, label="對齊程度", shrink=0.9)
    fig.suptitle("音太高時出現假的紅點（鬼影）；鳥叫有很多高低音，鬼影會被沖淡（UMA-16）", fontsize=11,
                 y=1.03)
    fig.savefig(path, dpi=150, bbox_inches="tight")


def fig_boards(path, maps, sizes):
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.6), sharey=True)
    for k, (ax, (name, pmap), (w, h)) in enumerate(zip(axes, maps, sizes)):
        note = "紅色是一條直帶：分不出上下" if k == 0 else f"紅點：寬 {w} 度、高 {h} 度"
        im = show_map(ax, pmap, f"{name}\n{note}")
        ax.set_xlabel("左右角度（度）")
    axes[0].set_ylabel("上下角度（度）")
    fig.colorbar(im, ax=axes, label="對齊程度", shrink=0.9)
    fig.suptitle("同一隻鳥：2 支只看得到一條直帶；6 支是一團；16 支是一小點", fontsize=11, y=1.06)
    fig.savefig(path, dpi=150, bbox_inches="tight")


def az_accuracy(mics, snr_db, runs=100, seconds=0.1):
    """Share of runs whose azimuth is within 2 deg; source at 20 deg, level with the mics."""
    hits = 0
    for s in range(runs):
        src = np.random.default_rng(1000 + s).standard_normal(int(FS * seconds))
        sig = plane_wave(src, FS, mics, BIRD_AZ, 0, snr_db=snr_db, seed=s)
        p = power_map(sig, FS, mics, AZ, np.array([0.0]), phat=True)
        hits += abs(AZ[np.argmax(p[0])] - BIRD_AZ) < 2
    return 100 * hits / runs


def fig_noise(path, snrs, curves):
    fig, ax = plt.subplots(figsize=(6, 4))
    for (name, _), acc, mark in zip(BOARDS, curves, ["o-", "s-", "^-"]):
        ax.plot(snrs, acc, mark, label=name)
    ax.set_xlabel("訊雜比（dB）     ← 越吵          越安靜 →")
    ax.set_ylabel("正確率（%）\n離正確答案 2 度以內才算對")
    top = ax.secondary_xaxis("top")
    top.set_xticks([-25, -20, -15, -10, -5, 0])
    top.set_xticklabels(["316 倍", "100 倍", "32 倍", "10 倍", "3 倍", "1 倍"], fontsize=8)
    top.set_xlabel("雜訊是聲音的幾倍（功率）", fontsize=8)
    ax.set_ylim(0, 105)
    ax.legend(fontsize=8, loc="lower right")
    ax.set_title("麥克風越多，越不怕吵：斷崖往左移", fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=150)


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    fig_layout(OUT / "step2_layout.png")
    fig_lineup(OUT / "step2_lineup.png")

    uma_bird = bird_map(uma16())
    az, el = peak_direction(uma_bird, AZ, EL)
    print(f"UMA-16 bird map peak: az {az:.0f}, el {el:.0f} (true {BIRD_AZ}, {BIRD_EL})")
    fig_map(OUT / "step2_map.png", uma_bird)

    freq_maps = [(f, tone_map(uma16(), f)) for f in (1000, 2000, 4000)]
    freq_sizes = [spot_size(p) for _, p in freq_maps]
    for (f, p), (w, h) in zip(freq_maps, freq_sizes):
        print(f"UMA-16 {f} Hz: peak {peak_direction(p, AZ, EL)}, spot {w} x {h} deg")
    for f in (1000, 2000, 4000):
        w, h = spot_size(tone_map(sipeed6(), f))
        print(f"Sipeed6 {f} Hz: spot {w} x {h} deg")
    fig_frequency(OUT / "step2_frequency.png", freq_maps, freq_sizes)

    tone8 = tone_map(uma16(), 8000)
    g_tone, g_bird = ghost_level(tone8), ghost_level(uma_bird)
    print(f"Ghost at 8 kHz tone: {g_tone:.0f}% of the peak; bird song 2-8 kHz: {g_bird:.0f}%")
    print(f"Sipeed6 ghost, bird song: {ghost_level(bird_map(sipeed6())):.0f}%")
    fig_ghost(OUT / "step2_ghost.png", tone8, uma_bird, g_tone, g_bird)

    board_maps = [(name, bird_map(m)) for name, m in BOARDS]
    board_sizes = [spot_size(p) for _, p in board_maps]
    for (name, p), (w, h) in zip(board_maps, board_sizes):
        print(f"{name}: peak {peak_direction(p, AZ, EL)}, spot {w} x {h} deg")
    fig_boards(OUT / "step2_boards.png", board_maps, board_sizes)

    snrs = np.arange(0, -27.5, -2.5)
    curves = [[az_accuracy(m, s) for s in snrs] for _, m in BOARDS]
    for (name, _), acc in zip(BOARDS, curves):
        print(name, "accuracy:", dict(zip(snrs.tolist(), acc)))
    fig_noise(OUT / "step2_noise.png", snrs, curves)


if __name__ == "__main__":
    main()
