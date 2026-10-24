"""Step 1: two simulated mics find the angle of a sound.

Writes three figures to docs/blog/img/ and prints the numbers used in the blog post.
Run from the project folder: .venv\\Scripts\\python scripts\\step1_two_mics.py
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import numpy as np
from scipy.signal import chirp, resample

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from acam.delay import SPEED_OF_SOUND, angle_from_delay, gcc_phat  # noqa: E402
from acam.sim import two_mic_plane_wave  # noqa: E402

FS = 48_000
D = 0.042  # UMA-16 mic spacing, metres
MAX_TAU = D / SPEED_OF_SOUND
OUT = Path(__file__).resolve().parents[1] / "docs" / "blog" / "img"


def noise_burst(n=4800, seed=0):
    return np.random.default_rng(seed).standard_normal(n)


def bird_whistle(n=4800):
    t = np.arange(n) / FS
    return chirp(t, f0=2000, t1=t[-1], f1=6000) * np.hanning(n)


def estimate(source, true_deg, interp, seed=1, band=None):
    mic0, mic1 = two_mic_plane_wave(source, FS, true_deg, D, snr_db=20, seed=seed)
    tau = gcc_phat(mic0, mic1, FS, max_tau=MAX_TAU, interp=interp, band=band)
    return angle_from_delay(tau, D)


def fig_geometry(path):
    theta = np.radians(30)
    fig, ax = plt.subplots(figsize=(6, 4))
    mics = np.array([[-D / 2, 0], [D / 2, 0]]) * 100  # cm
    ax.plot(*mics.T, "ko", ms=10)
    for (x, y), name in zip(mics, ["mic 0", "mic 1"]):
        ax.annotate(name, (x, y), (x, y - 0.6), ha="center")
    # d: the distance between the mics.
    ax.annotate("", mics[1] + [0, -1.1], mics[0] + [0, -1.1], arrowprops=dict(arrowstyle="<->"))
    ax.text(0, -1.0, f"d = {D * 100:.1f} cm", ha="center", va="bottom")
    direction = np.array([np.sin(theta), np.cos(theta)])
    ax.annotate("", 3.5 * direction, (0, 0), arrowprops=dict(arrowstyle="->", color="C1", lw=2))
    ax.text(*(3.6 * direction), "to the sound", color="C1")
    ax.plot([0, 0], [0, 3.5], "k:", lw=1)
    ax.text(-0.1, 3.6, "straight ahead (0 deg)", fontsize=8, ha="right")
    # Angle θ between straight ahead and the sound.
    ax.add_patch(Arc((0, 0), 5.6, 5.6, theta1=90 - 30, theta2=90, color="C1"))
    ax.text(0.1, 2.95, "θ = 30°", color="C1", fontsize=9)
    # Wavefront through mic 1, perpendicular to the direction.
    wave = np.array([direction[1], -direction[0]])
    p = mics[1] + np.outer([-4.6, 1], wave)
    ax.plot(p[:, 0], p[:, 1], "C0--", lw=1)
    ax.text(*(p[0] + [-0.2, 0.25]), "wavefront", color="C0", fontsize=8)
    # The same θ sits between the mic line and the wavefront, at mic 1.
    ax.add_patch(Arc(mics[1], 2.0, 2.0, theta1=180 - 30, theta2=180, color="C0"))
    ax.text(mics[1][0] - 1.45, 0.12, "θ", color="C0", fontsize=10)
    foot = mics[1] + wave * np.dot(mics[0] - mics[1], wave)
    ax.plot([mics[0][0], foot[0]], [0, foot[1]], "C3", lw=3)
    # Right-angle mark where the extra path meets the wavefront.
    s = 0.2
    corner = foot - s * direction
    ax.plot(*np.array([corner, corner + s * wave, foot + s * wave]).T, "k", lw=0.8)
    ax.text(-3.9, 0.9, "extra path\n= d · sin θ", color="C3", fontsize=9)
    ax.set_title("The sound reaches mic 1 first; mic 0 waits for the extra path")
    ax.set_aspect("equal")
    ax.set_xlim(-4, 4)
    ax.set_ylim(-1.6, 4.3)
    ax.set_xlabel("cm")
    ax.set_yticks([])
    fig.tight_layout()
    fig.savefig(path, dpi=150)


def fig_correlation(path):
    mic0, mic1 = two_mic_plane_wave(noise_burst(), FS, 30, D, snr_db=20, seed=1)
    true_us = D * np.sin(np.radians(30)) / SPEED_OF_SOUND * 1e6
    fig, (top, ax) = plt.subplots(2, 1, figsize=(6, 6.5))

    # Top: the sound each mic hears. Dots are the real samples; the line between
    # them is the smooth wave they come from (16x resampled).
    start, length = 1000, 24
    t_us = np.arange(length) / FS * 1e6
    t_fine = np.arange(length * 16) / (16 * FS) * 1e6
    for sig, name, color in [(mic1, "mic 1 (hears it first)", "C2"), (mic0, "mic 0", "C3")]:
        fine = resample(sig, len(sig) * 16)[start * 16 : (start + length) * 16]
        top.plot(t_fine, fine, "-", color=color, lw=1.2, label=name)
        top.plot(t_us, sig[start : start + length], "o", color=color, ms=3)
    # Arrow from mic 1's highest peak to the same peak in mic 0.
    fine1 = resample(mic1, len(mic1) * 16)[start * 16 : (start + length) * 16]
    peak_t, peak_y = t_fine[np.argmax(fine1)], fine1.max()
    for t in (peak_t, peak_t + true_us):
        top.axvline(t, color="grey", ls=":", lw=0.8)
    top.annotate("", (peak_t + true_us, peak_y + 0.4), (peak_t, peak_y + 0.4),
                 arrowprops=dict(arrowstyle="->"))
    top.text(peak_t + true_us / 2, peak_y + 0.55, f"same peak, {true_us:.0f} us later",
             ha="center", fontsize=8)
    top.set_xlabel("time (microseconds); dots = samples, 20.8 us apart")
    top.set_ylabel("sound level")
    top.set_title("What the mics hear: mic 0 gets the same wave, later")
    top.set_ylim(top.get_ylim()[0], 3.4)
    top.legend(fontsize=8, loc="upper left")

    # Bottom: the GCC-PHAT score for each trial delay.
    for interp, style, label in [
        (1, "o-", "score every 20.8 us (whole samples)"),
        (16, "-", "score every 1.3 us (16x finer)"),
    ]:
        n = len(mic0) * 2
        cross = np.fft.rfft(mic0, n) * np.conj(np.fft.rfft(mic1, n))
        cc = np.fft.irfft(cross / (np.abs(cross) + 1e-12), n * interp)
        k = 8 * interp
        cc = np.concatenate((cc[-k:], cc[: k + 1])) * interp
        lags_us = np.arange(-k, k + 1) / (interp * FS) * 1e6
        ax.plot(lags_us, cc, style, label=label)
    ax.axvline(true_us, color="k", ls=":", label=f"true delay {true_us:.0f} us")
    ax.set_xlabel("trial delay of mic 0 after mic 1 (microseconds)")
    ax.set_ylabel("GCC-PHAT score")
    ax.set_title("GCC-PHAT score vs. delay: the peak marks the delay")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150)


def fig_sweep(path, truth, whole, fine):
    fig, (a, b) = plt.subplots(2, 1, figsize=(6, 6), sharex=True)
    a.plot(truth, truth, "k:", label="perfect")
    a.plot(truth, whole, "o-", ms=3, label="whole samples")
    a.plot(truth, fine, "-", label="16x finer")
    a.set_ylabel("estimated angle (deg)")
    a.legend(fontsize=8)
    a.set_title("Two mics, 4.2 cm apart, 48 kHz, noise 20 dB below the sound")
    b.plot(truth, np.abs(whole - truth), "o-", ms=3, label="whole samples")
    b.plot(truth, np.abs(fine - truth), "-", label="16x finer")
    b.set_xlabel("true angle (deg)")
    b.set_ylabel("error (deg)")
    b.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    truth = np.arange(-85, 86, 1)
    whole = np.array([estimate(noise_burst(), t, interp=1) for t in truth])
    fine = np.array([estimate(noise_burst(), t, interp=16) for t in truth])
    inner = np.abs(truth) <= 60

    fig_geometry(OUT / "step1_geometry.png")
    fig_correlation(OUT / "step1_correlation.png")
    fig_sweep(OUT / "step1_sweep.png", truth, whole, fine)

    print(f"Largest delay possible: {MAX_TAU * 1e6:.1f} us = {MAX_TAU * FS:.2f} samples")
    print(f"Delay at 30 deg: {MAX_TAU * 0.5 * 1e6:.1f} us = {MAX_TAU * 0.5 * FS:.2f} samples")
    print(f"Distinct angles with whole samples: {len(np.unique(np.round(whole, 3)))}")
    print(f"Max error within +-60 deg, whole samples: {np.max(np.abs(whole - truth)[inner]):.1f} deg")
    print(f"Max error within +-60 deg, 16x finer: {np.max(np.abs(fine - truth)[inner]):.1f} deg")
    print(f"Max error 61-85 deg, 16x finer: {np.max(np.abs(fine - truth)[~inner]):.1f} deg")
    for seed in [1, 2, 3]:
        full = estimate(bird_whistle(), 30, 16, seed=seed)
        band = estimate(bird_whistle(), 30, 16, seed=seed, band=(2000, 6000))
        print(f"Bird whistle at 30 deg, noise seed {seed}: all frequencies {full:.1f} deg, "
              f"2-6 kHz only {band:.1f} deg")


if __name__ == "__main__":
    main()
