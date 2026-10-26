"""Bonus post 2: how far away can the Sipeed ring still find a bird?

A bird's song gets quieter with distance (spreading, then air absorption). The ring
finds the direction while the song is loud enough above the garden's background
sound. A simulation gives the share of right answers at each signal-to-noise ratio, with
all the background noise inside the song's 2-8 kHz band (the cautious case);
the distance turns into that ratio. Writes the bonus 2 figures to docs/blog/img/
and prints the numbers the post uses.

Sources: red-winged blackbird about 90 dB SPL at 1 m (Brenowitz 1982); many small
songbirds below 80 dB (Brumm et al. 2025); quiet urban daytime 50 dBA, night 40 dBA
(Caltrans Technical Noise Supplement 2013); Sipeed mic MSM261S4030H0 SNR 57 dB(A)
(Sipeed wiki), so its own noise is 94 - 57 = 37 dBA.
Run from the project folder: .venv\\Scripts\\python scripts\\bonus2_how_far.py
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import chirp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from acam.beamform import peak_direction, power_map  # noqa: E402
from acam.geometry import direction, sipeed6  # noqa: E402
from acam.propagation import air_absorption, level_at  # noqa: E402
from acam.sim import plane_wave  # noqa: E402

FS = 48_000
AZ = np.arange(-90, 91, 2.0)
EL = np.arange(-60, 61, 2.0)
BIRD_DIR = (20, 10)
BAND = (2000, 8000)
SONG_FREQ = 5000  # middle of the song, for air absorption
BIRDS = [("大聲的鳥", 90, "C3"), ("小聲的鳥", 75, "C0")]  # dB at 1 m
DAY, DAWN = 50, 40  # background, dBA
MIC_SELF = 94 - 57  # dBA
RIGHT_DEG = 10  # a right answer: within 10 deg of the bird
RUNS = 100
SNRS = np.arange(0, -31, -2)
DIST = np.logspace(0, np.log10(300), 400)
DIST_TICKS = [1, 2, 5, 10, 20, 50, 100, 200]
OUT = Path(__file__).resolve().parents[1] / "docs" / "blog" / "img"

# Figures are in Traditional Chinese for the blog.
plt.rcParams["font.family"] = ["Microsoft JhengHei", "Noto Sans TC"]
plt.rcParams["axes.unicode_minus"] = False


def bird_song(n=4800):
    t = np.arange(n) / FS
    return chirp(t, f0=BAND[0], t1=t[-1], f1=BAND[1]) * np.hanning(n)


def band_noise(shape, rms, seed):
    """Noise only inside the bird's band: the cautious case, all background sound where the song is."""
    x = np.random.default_rng(seed).normal(size=shape)
    spec = np.fft.rfft(x, axis=-1)
    f = np.fft.rfftfreq(shape[-1], 1 / FS)
    spec[..., (f < BAND[0]) | (f > BAND[1])] = 0
    x = np.fft.irfft(spec, shape[-1], axis=-1)
    return x * rms / x.std()


def accuracy_by_snr():
    """Share of runs (percent) within RIGHT_DEG of the bird, for each SNR."""
    mics, song, u = sipeed6(), bird_song(), direction(*BIRD_DIR)
    acc = []
    for snr in SNRS:
        right = 0
        for s in range(RUNS):
            sig = plane_wave(song, FS, mics, *BIRD_DIR)
            sig = sig + band_noise(sig.shape, np.std(song) * 10 ** (-snr / 20), s)
            az, el = peak_direction(power_map(sig, FS, mics, AZ, EL, band=BAND, phat=True), AZ, EL)
            right += np.degrees(np.arccos(np.clip(direction(az, el) @ u, -1, 1))) <= RIGHT_DEG
        acc.append(100 * right / RUNS)
        print(f"  snr {snr:>4} dB: {acc[-1]:5.1f}% right")
    return np.array(acc)


def snr_at(share, acc):
    """Lowest SNR (dB) where the share of right answers is still `share` percent."""
    i = np.argmax(acc < share)  # SNRS run from high to low
    return float(np.interp(share, [acc[i], acc[i - 1]], [SNRS[i], SNRS[i - 1]]))


def reach(level_1m, background, snr_needed):
    """Farthest distance (m) where the song is still `snr_needed` above the background."""
    ok = level_at(level_1m, DIST, freq=SONG_FREQ) - background >= snr_needed
    return float(DIST[ok][-1])  # DIST ends at 300 m: 300 means "300 or more"


def log_axis(ax):
    ax.set_xscale("log")
    ax.set_xticks(DIST_TICKS)
    ax.set_xticklabels([str(d) for d in DIST_TICKS])
    ax.set_xlim(1, 300)
    ax.set_xlabel("鳥離麥克風幾公尺")


def fig_distance(path):
    fig, ax = plt.subplots(figsize=(7, 4))
    for name, l1, col in BIRDS:
        ax.plot(DIST, level_at(l1, DIST), c=col, lw=2, label=f"{name}（1 公尺外 {l1} dB）")
    ax.axhline(DAY, c="0.4", ls="--", label=f"白天背景的聲音（{DAY} dB）")
    quiet_cross = 10 ** ((BIRDS[1][1] - DAY) / 20)
    log_axis(ax)
    ax.set_ylim(20, 100)
    ax.set_yticks(range(20, 101, 10))
    ax.set_ylabel("鳥叫有多大聲（dB）")
    ax.legend(fontsize=8, loc="upper right")
    ax.set_title(f"距離每加倍，聲音小 4 倍：小聲的鳥 {quiet_cross:.0f} 公尺外，就比背景還小聲", fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    return quiet_cross


def fig_air(path, r=50):
    freqs = [1000, 2000, 4000, 8000]
    spread = 20 * np.log10(r)
    air = [air_absorption(f) * (r - 1) for f in freqs]
    fig, ax = plt.subplots(figsize=(7, 4))
    x = np.arange(len(freqs))
    ax.bar(x - 0.2, [spread] * len(freqs), 0.4, color="0.7", label="散開變小的部分")
    ax.bar(x + 0.2, air, 0.4, color="C1", label="被空氣吃掉的部分")
    for xi, a in zip(x, air):
        ax.text(xi + 0.2, a + 0.8, f"{a:.1f}", ha="center", fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{f // 1000} kHz" for f in freqs])
    ax.set_xlabel("← 低音　　　　高音 →")
    ax.set_ylabel(f"走 {r} 公尺，聲音小了幾 dB")
    ax.set_ylim(0, 45)
    ax.set_yticks(range(0, 41, 10))
    ax.legend(fontsize=9, loc="upper center", ncol=2)
    ax.set_title(f"走 {r} 公尺：散開吃掉 {spread:.0f} dB，空氣最多只吃掉 {air[-1]:.0f} dB", fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    return spread, air


def fig_range(path, acc, reach90):
    fig, ax = plt.subplots(figsize=(7, 4))
    for name, l1, col in BIRDS:
        snr = level_at(l1, DIST, freq=SONG_FREQ) - DAY
        share = np.interp(snr, SNRS[::-1], acc[::-1])  # outside the simulated range: hold the end value
        ax.plot(DIST, share, c=col, lw=2, label=f"{name}（1 公尺外 {l1} dB）")
    ax.axvspan(30, 300, color="0.92", zorder=0)
    ax.text(32, 62, "30 公尺外：\n這裡算得太樂觀", fontsize=8, color="0.35")
    ax.axhline(90, c="0.5", ls=":", lw=1)
    ax.text(1.1, 92, "正確率 90%", fontsize=8, color="0.4")
    log_axis(ax)
    ax.set_ylim(0, 105)
    ax.set_yticks(range(0, 101, 20))
    ax.set_ylabel("正確率（%，越高越好）")
    ax.legend(fontsize=8, loc="lower left")
    big, small = reach90
    ax.set_title(f"白天，院子的距離都指得對：小聲的鳥 {small:.0f} 公尺、大聲的鳥 {big:.0f} 公尺外才開始指錯",
                 fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=150)


def main():
    quiet_cross = fig_distance(OUT / "bonus2_distance.png")
    print(f"Quiet bird ({BIRDS[1][1]} dB) equals the day background at {quiet_cross:.1f} m; "
          f"loud bird at {10 ** ((BIRDS[0][1] - DAY) / 20):.0f} m")
    spread, air = fig_air(OUT / "bonus2_air.png")
    print(f"50 m: spreading {spread:.1f} dB; air at 1/2/4/8 kHz " + ", ".join(f"{a:.1f}" for a in air)
          + f" dB; 8 kHz in dry air (20%): {air_absorption(8000, rh=20) * 49:.1f} dB")
    print(f"Mic self-noise {MIC_SELF} dBA vs day {DAY} / dawn {DAWN} dBA")

    print(f"Sipeed ring, {RUNS} runs per SNR, right = within {RIGHT_DEG} deg:")
    acc = accuracy_by_snr()
    snr90, snr50 = snr_at(90, acc), snr_at(50, acc)
    print(f"90% right down to {snr90:.1f} dB; cliff (50%) at {snr50:.1f} dB")
    reach90 = [reach(l1, DAY, snr90) for _, l1, _ in BIRDS]
    for (name, l1, _), r in zip(BIRDS, reach90):
        print(f"{name} {l1} dB: 90% right up to {r:.0f} m in the day, "
              f"{reach(l1, DAWN, snr90):.0f} m at dawn; cliff at {reach(l1, DAY, snr50):.0f} m (day)")
    fig_range(OUT / "bonus2_range.png", acc, reach90)


if __name__ == "__main__":
    main()
