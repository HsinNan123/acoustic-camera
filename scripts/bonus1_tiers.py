"""Bonus post 1: how many mics each kind of DIY acoustic camera uses.

Mic counts come from each project's own page (see docs/research/open-source-acoustic-cameras.md).
Writes docs/blog/img/bonus1_mics.png.
Run from the project folder: .venv\\Scripts\\python scripts\\bonus1_tiers.py
"""
from pathlib import Path

import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / "docs" / "blog" / "img"

# Figures are in Traditional Chinese for the blog.
plt.rcParams["font.family"] = ["Microsoft JhengHei", "Noto Sans TC"]
plt.rcParams["axes.unicode_minus"] = False

# (project, mics, way): way 1 = slingshot (small board), 2 = bow (Pi + USB board), 3 = cannon (FPGA).
PROJECTS = [
    ("ESP32\nAcousticCam", 4, 1),
    ("Sipeed K210\nMicArray", 7, 1),
    ("UMA-16\n（我選的）", 16, 2),
    ("Sesenta\n一塊", 60, 3),
    ("jduanen\n螺旋板", 96, 3),
]
WAYS = {1: ("彈弓：小電腦板", "C0"), 2: ("弓箭：樹莓派＋麥克風板", "C2"), 3: ("大砲：FPGA 大陣列", "C3")}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.5, 4))
    for k, (name, mics, way) in enumerate(PROJECTS):
        label, color = WAYS[way]
        shown = label if label not in ax.get_legend_handles_labels()[1] else None
        ax.bar(k, mics, color=color, label=shown)
        ax.text(k, mics + 2, f"{mics} 支", ha="center", fontsize=9)
    ax.set_xticks(range(len(PROJECTS)))
    ax.set_xticklabels([p[0] for p in PROJECTS], fontsize=8)
    ax.set_ylabel("麥克風數量（支）")
    ax.set_yticks(range(0, 101, 20))
    ax.set_ylim(0, 110)
    ax.legend(fontsize=8, loc="upper left")
    ax.set_title("麥克風越多，地圖越清楚，但也越貴、越難做", fontsize=11)
    for side in ("right", "top"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "bonus1_mics.png", dpi=150)
    for name, mics, way in PROJECTS:
        print(name.replace("\n", " "), mics, WAYS[way][0])


if __name__ == "__main__":
    main()
