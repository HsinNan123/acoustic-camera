"""Bonus post 5: can AI tell which bird is singing, and where?

BirdNET (Cornell Lab + TU Chemnitz) names the species in every 3 s of a recording.
The script runs it on one real call of a Light-vented Bulbul (白頭翁), then adds
BirdNET's location model (which birds live here in this season), and last joins it
with our own direction finder: the same call, simulated as arriving at the Sipeed
board, gives the direction; BirdNET on one mic gives the species. Writes the bonus 5
figures to docs/blog/img/ and prints the numbers the post uses.

Recording: "Pycnonotus sinensis call.ogg", The Nature Box, Kaohsiung, Taiwan,
2024-01-18, CC0, from Wikimedia Commons. Downloaded to recordings/ (not committed).
Models: BirdNET acoustic + geo model 2.4, CC BY-NC-SA 4.0 (non-commercial use only);
the `birdnet` package (MIT) downloads them on first use.
Needs: pip install birdnet==1.3.0 ai-edge-litert
Run from the project folder: .venv\\Scripts\\python scripts\\bonus5_birdnet.py
"""
import sys
import urllib.request
from pathlib import Path

import birdnet
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
from scipy.ndimage import maximum_filter1d
from scipy.signal import resample_poly, spectrogram

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from acam.beamform import peak_direction, power_map  # noqa: E402
from acam.geometry import sipeed6  # noqa: E402
from acam.sim import plane_wave  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
REC_URL = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Pycnonotus_sinensis_call.ogg"
REC = ROOT / "recordings" / "bonus5" / "Pycnonotus_sinensis_call.ogg"
OUT = ROOT / "docs" / "blog" / "img"
FS = 48_000  # BirdNET and our simulation both use 48 kHz
LAT, LON, WEEK = 22.63, 120.30, 3  # Kaohsiung; BirdNET week 3 = mid-January
TRUE = "Pycnonotus sinensis_Light-vented Bulbul"
STEP_S = 1  # a new 3 s window every second
CONF_MIN = 0.10  # BirdNET's default: below this, an answer is not shown
AZ = np.arange(-90, 91, 1.0)
EL = np.arange(-60, 61, 1.0)
BAND = (2000, 8000)
BIRD_DIR = (20, 10)
SNR_DB = 20  # each mic's own noise, on top of the background already in the recording

# Taiwan names for every species a figure shows (BirdNET labels are scientific_English).
ZH = {
    "Pycnonotus sinensis": "白頭翁", "Pycnonotus taivanus": "烏頭翁",
    "Pycnonotus jocosus": "紅耳鵯", "Pycnonotus leucotis": "白耳鵯",
    "Gracupica contra": "斑椋鳥", "Monticola solitarius": "藍磯鶇",
    "Upupa epops": "戴勝", "Human vocal": "人聲",
}

plt.rcParams["font.family"] = ["Microsoft JhengHei", "Noto Sans TC"]
plt.rcParams["axes.unicode_minus"] = False


def zh(label):
    return ZH[label.split("_")[0]]


def load_recording():
    if not REC.exists():
        REC.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(REC_URL, headers={"User-Agent": "acoustic-camera-blog/1.0"})
        REC.write_bytes(urllib.request.urlopen(req).read())
    x, fs = sf.read(REC)
    x = x.mean(axis=1) if x.ndim == 2 else x
    return resample_poly(x, FS // 100, fs // 100)  # 44.1 kHz -> 48 kHz


def windows(model, audio, species=None):
    """BirdNET's top 5 guesses for every 3 s window, one window per second."""
    r = model.predict_arrays((audio.astype(np.float32), FS), top_k=5, n_workers=1,
                             overlap_duration_s=3 - STEP_S, default_confidence_threshold=None,
                             custom_species_list=species)
    return r.to_dataframe()[["start_time", "end_time", "species_name", "confidence"]]


def call_spans(audio):
    """Start and end (s) of each stretch where the 1.5-4 kHz sound is loud: the calls."""
    f, t, s = spectrogram(audio, FS, nperseg=2048, noverlap=1536)
    level = 10 * np.log10(s[(f > 1500) & (f < 4000)].sum(axis=0) + 1e-20)
    level = maximum_filter1d(level, round(0.3 / (t[1] - t[0])))  # bridge gaps inside a call
    loud = level > level.max() - 30
    edges = np.flatnonzero(np.diff(loud.astype(int)))
    spans, start = [], t[0] if loud[0] else None
    for e in edges:
        if loud[e + 1]:
            start = t[e + 1]
        elif start is not None:
            spans.append((start, t[e]))
            start = None
    if start is not None:
        spans.append((start, t[-1]))
    return [(a, b) for a, b in spans if b - a > 0.4]


def fig_spectrogram(path, audio, spans):
    f, t, s = spectrogram(audio, FS, nperseg=1024, noverlap=768)
    fig, ax = plt.subplots(figsize=(7, 3.6))
    db = 10 * np.log10(s + 1e-20)
    ax.pcolormesh(t, f / 1000, db, shading="auto", cmap="magma", vmin=db.max() - 70, vmax=db.max())
    for a, b in spans:
        ax.annotate("叫聲", xy=((a + b) / 2, 4.2), xytext=((a + b) / 2, 7.5), ha="center",
                    color="white", fontsize=10, arrowprops=dict(arrowstyle="->", color="white"))
    ax.set_ylim(0, 10)
    ax.set_yticks(range(0, 11, 2))
    ax.set_xticks(range(0, int(t[-1]) + 1))
    ax.set_xlabel("時間（秒）")
    ax.set_ylabel("音高（kHz，越上面越高）")
    ax.set_title(f"白頭翁的叫聲畫成樂譜：{len(spans)} 段叫聲，其他時間是背景聲音", fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_guesses(path, top1):
    fig, ax = plt.subplots(figsize=(7, 4))
    x = np.arange(len(top1))
    for xi, (_, row) in zip(x, top1.iterrows()):
        ok = row.species_name == TRUE
        ax.bar(xi, row.confidence * 100, 0.7, color="C2" if ok else "0.65")
        y = row.confidence * 100 + 0.8
        if abs(y - CONF_MIN * 100) < 2:  # keep the name off the dashed line
            y = CONF_MIN * 100 + 1.2
        ax.text(xi, y, zh(row.species_name), ha="center", fontsize=9, color="C2" if ok else "0.25")
    ax.axhline(CONF_MIN * 100, c="C3", ls="--", lw=1)
    ax.text(len(top1) - 0.6, CONF_MIN * 100 - 1.6, f"{CONF_MIN * 100:.0f}%", color="C3", fontsize=9,
            ha="right")
    ax.set_xticks(x)
    ax.set_xticklabels([f"{s:.0f}–{e:.0f}" for s, e in zip(top1.start_time, top1.end_time)], fontsize=8)
    ax.set_xlabel("聽的是哪 3 秒（秒）")
    ax.set_ylabel("最有把握的答案（%）")
    ax.set_ylim(0, 30)
    ax.set_yticks(range(0, 31, 10))
    best = top1.loc[top1.confidence.idxmax()]
    ax.set_title(f"AI 每 3 秒猜一次：最有把握的也只有 {best.confidence * 100:.0f}%，"
                 f"而且是{zh(best.species_name)}，猜錯了", fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_location(path, cands):
    fig, ax = plt.subplots(figsize=(7, 4))
    x = np.arange(len(cands))
    ax.bar(x - 0.2, cands.sound * 100, 0.4, color="0.65", label="聽起來像（把握 %）")
    ax.bar(x + 0.2, cands.here * 100, 0.4, color="C0", label="高雄一月有沒有這種鳥（%）")
    for xi, h in zip(x, cands.here):
        ax.text(xi + 0.2, h * 100 + 2, f"{h * 100:.0f}", ha="center", fontsize=9, color="C0")
    ax.set_xticks(x)
    ax.set_xticklabels([zh(s) for s in cands.index])
    ax.set_ylabel("%")
    ax.set_ylim(0, 115)
    ax.set_yticks(range(0, 101, 20))
    ax.legend(fontsize=9, loc="upper right")
    left = [zh(s) for s in cands.index[cands.score > 0]]
    ax.set_title(f"加上地點和季節：聽起來像、這裡也有的，只剩{'和'.join(left)}", fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_who_where(path, pmap, peak, name, conf, right):
    fig, ax = plt.subplots(figsize=(7, 4.4))
    im = ax.imshow(pmap, origin="lower", extent=[AZ[0], AZ[-1], EL[0], EL[-1]], cmap="turbo",
                   vmin=0, vmax=1, aspect="auto")
    ax.plot(*BIRD_DIR, "w+", ms=14, mew=2)
    ax.annotate(f"{name}{'' if right else '？'}（把握 {conf * 100:.0f}%）", xy=peak,
                xytext=(peak[0] + 12, peak[1] + 28), color="white", fontsize=10,
                arrowprops=dict(arrowstyle="->", color="white"))
    ax.set_xticks(range(-90, 91, 30))
    ax.set_yticks(range(-60, 61, 30))
    ax.set_xlabel("左右（度，右邊是正）")
    ax.set_ylabel("上下（度，上面是正）")
    fig.colorbar(im, ax=ax, label="對齊程度（1 = 最整齊）")
    where_ok = (peak[0], peak[1]) == BIRD_DIR
    ax.set_title(f"在哪裡：右 {peak[0]:.0f} 度、上 {peak[1]:.0f} 度{'，找對了' if where_ok else ''}。"
                 f"誰在叫：{'猜對了' if right else f'猜成{name}，猜錯了'}", fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main():
    audio = load_recording()
    model = birdnet.load("acoustic", "2.4", "tf", library="litert")
    geo = birdnet.load("geo", "2.4", "tf", library="litert")
    print(f"Recording {len(audio) / FS:.1f} s; BirdNET knows {len(model.species_list)} labels")

    spans = call_spans(audio)
    print("Calls at " + ", ".join(f"{a:.1f}-{b:.1f} s" for a, b in spans))
    fig_spectrogram(OUT / "bonus5_spectrogram.png", audio, spans)

    df = windows(model, audio)
    top1 = df.loc[df.groupby("start_time").confidence.idxmax()].reset_index(drop=True)
    for _, r in top1.iterrows():
        print(f"  {r.start_time:.0f}-{r.end_time:.1f} s: {r.species_name} {r.confidence:.3f}")
    fig_guesses(OUT / "bonus5_guesses.png", top1)
    true_best = df[df.species_name == TRUE].confidence.max()
    print(f"Light-vented Bulbul best score anywhere: {true_best:.3f}")

    here = geo.predict(LAT, LON, week=WEEK, min_confidence=0.0).to_dataframe()
    here = here.set_index("species_name").confidence
    local = list(here[here >= 0.03].index)  # BirdNET's default cut for the location filter
    print(f"Kaohsiung, week {WEEK}: {len(local)} of {len(here)} labels are likely here")
    birds = df[(df.confidence >= CONF_MIN) & ~df.species_name.str.startswith("Human")]
    cands = birds.groupby("species_name").confidence.max().to_frame("sound")
    cands["here"] = [here.get(s, 0.0) for s in cands.index]
    cands["score"] = cands.sound * (cands.here >= 0.03)
    cands = cands.sort_values(["score", "sound"], ascending=False)
    print(cands.round(3).to_string())
    fig_location(OUT / "bonus5_location.png", cands)

    # Who + where: the window where the top local bird scored best, as the Sipeed board
    # would hear it from (20, 10) deg, each mic with its own noise.
    best = df[df.species_name == cands.index[0]].sort_values("confidence").iloc[-1]
    a, b = best.start_time, best.end_time
    clip = audio[int(a * FS):int(b * FS)]
    sig = plane_wave(clip, FS, sipeed6(), *BIRD_DIR, snr_db=SNR_DB, seed=1)
    pmap = power_map(sig, FS, sipeed6(), AZ, EL, band=BAND, phat=True)
    peak = peak_direction(pmap, AZ, EL)
    who = model.predict_arrays((sig[0].astype(np.float32), FS), top_k=1, n_workers=1,
                               default_confidence_threshold=None, custom_species_list=local)
    w = who.to_dataframe().iloc[0]
    print(f"Who + where: {w.species_name} {w.confidence:.3f} at az {peak[0]:.0f}, el {peak[1]:.0f} "
          f"(true {BIRD_DIR}); clip {a:.1f}-{b:.1f} s, SNR {SNR_DB} dB")
    fig_who_where(OUT / "bonus5_who_where.png", pmap, peak, zh(w.species_name), w.confidence,
                  w.species_name == TRUE)


if __name__ == "__main__":
    main()
