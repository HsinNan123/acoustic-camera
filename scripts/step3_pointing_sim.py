"""Step 3: can the Sipeed ring point the C545D telephoto lens (57.3 x 31.7 deg) at a bird?

Bird song 2-8 kHz, 0.1 s, at 20 deg right and 10 deg up; 40 runs per noise level.
"In frame": the bird lands inside the telephoto view. "Near centre": within 10 deg
left-right and 5 deg up-down. Prints the numbers the bonus post and step 3 use.
Run from the project folder: .venv\\Scripts\\python scripts\\step3_pointing_sim.py
"""
import sys
from pathlib import Path

import numpy as np
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


def bird_song(n=4800):
    t = np.arange(n) / FS
    return chirp(t, f0=2000, t1=t[-1], f1=8000) * np.hanning(n)


def main():
    song = bird_song()
    for name, mics in [("Sipeed6", sipeed6()), ("UMA16", uma16())]:
        for snr in (10, 0, -10, -20):
            errs = []
            for s in range(40):
                sig = plane_wave(song, FS, mics, *BIRD, snr_db=snr, seed=s)
                p = power_map(sig, FS, mics, AZ, EL, band=(2000, 8000), phat=True)
                az, el = peak_direction(p, AZ, EL)
                errs.append((abs(az - BIRD[0]), abs(el - BIRD[1])))
            e = np.array(errs)
            in_frame = np.mean((e[:, 0] <= HALF_VIEW[0]) & (e[:, 1] <= HALF_VIEW[1])) * 100
            centre = np.mean((e[:, 0] <= 10) & (e[:, 1] <= 5)) * 100
            print(f"{name} snr {snr:>3} dB: in tele frame {in_frame:5.1f}%  near centre {centre:5.1f}%  "
                  f"median err az {np.median(e[:, 0]):.0f} el {np.median(e[:, 1]):.0f}")


if __name__ == "__main__":
    main()
