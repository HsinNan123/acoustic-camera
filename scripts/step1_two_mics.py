"""Step 1: two simulated mics find the angle of a sound.

Writes four figures to docs/blog/img/ and prints the numbers used in the blog post.
Run from the project folder: .venv\\Scripts\\python scripts\\step1_two_mics.py
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import numpy as np
from scipy.signal import butter, chirp, resample, sosfiltfilt

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from acam.delay import SPEED_OF_SOUND, angle_from_delay, gcc_phat  # noqa: E402
from acam.sim import two_mic_plane_wave  # noqa: E402

FS = 48_000
D = 0.042  # UMA-16 mic spacing, metres
MAX_TAU = D / SPEED_OF_SOUND
OUT = Path(__file__).resolve().parents[1] / "docs" / "blog" / "img"

# Figures are in Traditional Chinese for the blog.
plt.rcParams["font.family"] = ["Microsoft JhengHei", "Noto Sans TC"]
plt.rcParams["axes.unicode_minus"] = False


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
    ax.text(0, -1.0, f"d = {D * 100:.1f} 公分（兩支麥克風的距離）", ha="center", va="bottom",
            fontsize=9)
    direction = np.array([np.sin(theta), np.cos(theta)])
    ax.annotate("", 3.5 * direction, (0, 0), arrowprops=dict(arrowstyle="->", color="C1", lw=2))
    ax.text(*(3.6 * direction), "聲音從這裡來", color="C1")
    ax.plot([0, 0], [0, 3.5], "k:", lw=1)
    ax.text(-0.1, 3.6, "正前方（0 度）", fontsize=8, ha="right")
    # Angle θ between straight ahead and the sound.
    ax.add_patch(Arc((0, 0), 5.6, 5.6, theta1=90 - 30, theta2=90, color="C1"))
    ax.text(0.1, 2.95, "θ = 30°", color="C1", fontsize=9)
    # Wavefront through mic 1, perpendicular to the direction.
    wave = np.array([direction[1], -direction[0]])
    p = mics[1] + np.outer([-4.6, 1], wave)
    ax.plot(p[:, 0], p[:, 1], "C0--", lw=1)
    ax.text(*(p[0] + [-0.2, 0.25]), "浪頭（波前）", color="C0", fontsize=8)
    # The same θ sits between the mic line and the wavefront, at mic 1.
    ax.add_patch(Arc(mics[1], 2.0, 2.0, theta1=180 - 30, theta2=180, color="C0"))
    ax.text(mics[1][0] - 1.45, 0.12, "θ", color="C0", fontsize=10)
    foot = mics[1] + wave * np.dot(mics[0] - mics[1], wave)
    ax.plot([mics[0][0], foot[0]], [0, foot[1]], "C3", lw=3)
    # Right-angle mark where the extra path meets the wavefront.
    s = 0.2
    corner = foot - s * direction
    ax.plot(*np.array([corner, corner + s * wave, foot + s * wave]).T, "k", lw=0.8)
    ax.text(-3.9, 0.9, "多走的路\n= d · sin θ", color="C3", fontsize=9)
    ax.set_title("浪頭先碰到 mic 1；mic 0 要多走一段路，晚一點才聽到")
    ax.set_aspect("equal")
    ax.set_xlim(-4, 4)
    ax.set_ylim(-1.6, 4.3)
    ax.set_xlabel("左右位置（公分），0 = 兩支麥克風的正中間")
    ax.set_ylabel("往前（公分）")
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
    for sig, name, color in [(mic1, "mic 1（先聽到）", "C2"), (mic0, "mic 0", "C3")]:
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
    top.text(peak_t + true_us / 2, peak_y + 0.55, f"同一個波峰，晚 {true_us:.0f} 微秒",
             ha="center", fontsize=8)
    top.set_xlabel("時間（微秒）；點 = 聲音照片，每 20.8 微秒一張")
    top.set_ylabel("聲音大小")
    top.set_title("兩支麥克風聽到的聲音：一模一樣，只是 mic 0 晚一點")
    top.set_ylim(top.get_ylim()[0], 3.4)
    top.legend(fontsize=8, loc="upper left")

    # Bottom: the GCC-PHAT score for each trial delay.
    for interp, style, label in [
        (1, "o-", "只在每張照片計票（每 20.8 微秒）"),
        (16, "-", "照片之間補畫後計票（每 1.3 微秒）"),
    ]:
        n = len(mic0) * 2
        cross = np.fft.rfft(mic0, n) * np.conj(np.fft.rfft(mic1, n))
        cc = np.fft.irfft(cross / (np.abs(cross) + 1e-12), n * interp)
        k = 8 * interp
        cc = np.concatenate((cc[-k:], cc[: k + 1])) * interp
        lags_us = np.arange(-k, k + 1) / (interp * FS) * 1e6
        ax.plot(lags_us, cc, style, label=label)
    ax.axvline(true_us, color="k", ls=":", label=f"真正的時間差 {true_us:.0f} 微秒")
    ax.set_xlabel("猜的時間差：mic 0 比 mic 1 晚多少（微秒）")
    ax.set_ylabel("票數（GCC-PHAT 分數）")
    ax.set_title("評審投票：票數最高的地方，就是時間差")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150)


def fig_sweep(path, truth, whole, fine):
    fig, (a, b) = plt.subplots(2, 1, figsize=(6, 7), sharex=True)
    whole_label, fine_label = "只數照片（每 20.8 微秒）", "照片之間補畫（每 1.3 微秒）"
    a.plot(truth, truth, "k:", label="正確答案")
    a.plot(truth, whole, "o-", ms=3, label=whole_label)
    a.plot(truth, fine, "-", label=fine_label)
    a.set_ylabel("麥克風回答的角度（度）")
    a.legend(fontsize=8)
    a.set_title("只數照片：答案只有 13 種（樓梯）\n照片之間補畫：貼著正確答案", fontsize=11)
    for ax in (a, b):
        ax.axvspan(-60, 60, color="grey", alpha=0.08)
    b.plot(truth, np.abs(whole - truth), "o-", ms=3, label=whole_label)
    b.plot(truth, np.abs(fine - truth), "-", label=fine_label)
    b.text(0, 19, "灰色：左右 60 度以內", ha="center", fontsize=8, color="grey")
    b.set_xlabel("聲音真正的角度（模擬時設定，度）")
    b.set_ylabel("答錯幾度")
    b.legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.5, 0.84))
    inner = np.abs(truth) <= 60
    worst_whole = np.max(np.abs(whole - truth)[inner])
    worst_fine = np.max(np.abs(fine - truth)[inner])
    b.set_title(f"60 度以內最多答錯：{worst_whole:.1f} → {worst_fine:.1f} 度；越靠側面越不準",
                fontsize=11)
    fig.suptitle("兩支麥克風相距 4.2 公分，每秒 48,000 張聲音照片，雜訊比聲音小 100 倍（20 dB）",
                 fontsize=8, color="grey", y=0.995)
    fig.tight_layout()
    fig.savefig(path, dpi=150)


def angle_errors(snr_db, seconds, fs=FS, runs=200, bird_band=False):
    """Angle errors (deg) for a source at 30 deg over `runs` random sounds and noises.

    `bird_band`: the sound and the GCC-PHAT score keep only 2-8 kHz.
    """
    sos = butter(6, [2000, 8000], btype="band", fs=fs, output="sos")
    errors = []
    for s in range(runs):
        src = np.random.default_rng(1000 + s).standard_normal(int(fs * seconds))
        if bird_band:
            src = sosfiltfilt(sos, src)
        mic0, mic1 = two_mic_plane_wave(src, fs, 30, D, snr_db=snr_db, seed=s)
        band = (2000, 8000) if bird_band else None
        errors.append(angle_from_delay(gcc_phat(mic0, mic1, fs, max_tau=MAX_TAU, band=band), D) - 30)
    return np.array(errors)


def rms(errors):
    return np.sqrt(np.mean(errors**2))


def fig_noise(path, snrs, hit_short, hit_long):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(snrs, hit_short, "o-", label="聽 0.1 秒")
    ax.plot(snrs, hit_long, "s-", label="聽 0.4 秒（4 倍久）")
    ax.axvline(0, color="grey", ls=":", lw=0.8)
    ax.text(0.5, 76, "← 聲音和雜訊\n    一樣大", color="grey", fontsize=8)
    ax.text(5, 50, "安靜：\n聲音比雜訊大", ha="center", fontsize=8, color="grey")
    ax.text(-18.5, 72, "吵：\n雜訊比聲音大", ha="center", fontsize=8, color="grey")
    ax.annotate("斷崖：\n正確率突然掉下去", (-12.5, 50), (-8, 25), fontsize=8,
                arrowprops=dict(arrowstyle="->", color="grey"))
    ax.set_xlabel("訊雜比（dB）     ← 越吵          越安靜 →")
    ax.set_ylabel("正確率（%）\n離正確答案 2 度以內才算對")
    top = ax.secondary_xaxis("top")
    top.set_xticks([-20, -15, -10, -5, 0])
    top.set_xticklabels(["100 倍", "32 倍", "10 倍", "3 倍", "1 倍"], fontsize=8)
    top.set_xlabel("雜訊是聲音的幾倍（功率）", fontsize=8)
    ax.set_title("太吵時答案會突然全錯（斷崖）；聽久一點可以撐住", fontsize=11)
    ax.set_ylim(0, 105)
    ax.legend(fontsize=8, loc="lower right")
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

    # Noise and listening time: source at 30 deg, 200 runs per point.
    snrs = np.arange(10, -22.5, -2.5)
    short = [angle_errors(s, 0.1) for s in snrs]
    long = [angle_errors(s, 0.4) for s in snrs]
    fig_noise(OUT / "step1_noise.png", snrs,
              [np.mean(np.abs(e) < 2) * 100 for e in short],
              [np.mean(np.abs(e) < 2) * 100 for e in long])
    for s, e1, e4 in zip(snrs, short, long):
        print(f"SNR {s:6.1f} dB: RMS error 0.1 s {rms(e1):5.2f} deg, 0.4 s {rms(e4):5.2f} deg; "
              f"within 2 deg {np.mean(np.abs(e1) < 2) * 100:3.0f}% / {np.mean(np.abs(e4) < 2) * 100:3.0f}%")

    # Sample rate, fair test: 2-8 kHz sound, same noise per Hz (96 kHz total SNR 3 dB lower).
    for snr in [0, -5]:
        e48 = rms(angle_errors(snr, 0.1, bird_band=True))
        e96 = rms(angle_errors(snr - 3, 0.1, fs=96_000, bird_band=True))
        print(f"2-8 kHz sound, SNR {snr} dB at 48 kHz, same noise per Hz at 96 kHz: "
              f"48 kHz {e48:.2f} deg, 96 kHz {e96:.2f} deg")

    for metres in [10, 50]:
        print(f"0.5 deg at {metres} m = {np.tan(np.radians(0.5)) * metres * 100:.0f} cm")


if __name__ == "__main__":
    main()
