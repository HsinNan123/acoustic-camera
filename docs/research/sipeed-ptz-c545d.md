# Sipeed 6+1 mic board steering a Tapo C545D: feasibility

Date: 2026-10-25. Asked by Aaron: use the Sipeed 6+1 USB mic board to turn the
outdoor TP-Link Tapo C545D toward a singing bird, then film it.

## Conclusion

Feasible, and a better fit than a heat map on a webcam. The sound only has to aim the
telephoto lens, and that lens sees 57° × 32°, so a coarse direction is enough. Three
things are unverified and decide the plan: PTZ control from Python, outdoor mounting,
and how fast the camera turns.

```
[Sipeed board]  ->  [PC or Pi]           ->  [C545D telephoto]   ->  [video clip]
 6 raw channels      direction (our code)     pan/tilt to it          bird in frame
 over USB            angle -> camera angle    (ONVIF or pytapo)       saved
```

## Facts

| Item | Value | Source |
|---|---|---|
| C545D telephoto lens | 6 mm, 57.3° × 31.7° view, 2304 × 1296, 15 fps | TP-Link datasheet |
| C545D telephoto movement | pan 360°, tilt 121° | TP-Link datasheet |
| C545D wide lens | fixed, 137.6° × 73.0° view; pan/tilt by hand only | TP-Link datasheet |
| C545D local access | RTSP yes, ONVIF yes, IP66, 12 V | TP-Link datasheet |
| Sipeed MA-USB8 audio | UAC2, 48 kHz, 16 bit; CH0–CH5 raw mics, CH6 beam output | Sipeed wiki |
| Sipeed built-in output | 16 × 16 heat map over USB serial; no angle; firmware closed | Sipeed wiki |
| Sipeed geometry | 6 mics on a 40 mm radius ring (centre mic unused) | Sipeed wiki |

## Simulation (our code, ideal conditions)

Bird song 2–8 kHz, 0.1 s, one source at 20° right and 10° up, 40 runs per row,
direction from `acam.beamform.power_map` with PHAT.

| Noise vs sound | Sipeed: in telephoto frame | Sipeed: near centre (±10°, ±5°) | UMA-16: near centre |
|---|---|---|---|
| +10 dB (sound 10× louder) | 100% | 100% | 100% |
| 0 dB (same) | 100% | 100% | 100% |
| −10 dB (noise 10× louder) | 100% | 100% | 100% |
| −20 dB (noise 100× louder) | 100% | 77.5% | 100% |

Not covered: echoes from walls, wind, two birds at once, rain. Real numbers come only
from the board.

Image size (inference, by calculation): 2304 px over 57.3° is about 40 px per degree.
A 12 cm bird is about 28 px wide at 10 m and about 55 px at 5 m. Enough to find and
film a bird; not enough for a close-up photo.

## Open risks

1. **PTZ control from Python is unverified.** ONVIF is listed, but which ONVIF PTZ
   moves the C545D accepts (absolute or only continuous) is unknown. `pytapo` is an
   unofficial fallback. Test: Aaron creates a Camera Account in the Tapo app; a
   20-line script pans 30° and reads the position back.
2. **Mounting.** Window glass blocks sound, so the board must sit outdoors next to the
   camera, under a rain cover with wind foam, on a USB cable (5 m at most) to a PC or
   Pi. A 1 m gap between board and camera adds about 6° at 10 m (inference).
3. **Front-back mirror.** A flat ring cannot tell front from back. Mount it facing
   the garden with the wall behind it.
4. **Turn speed.** Motor speed is not in the datasheet. A bird song lasts a few
   seconds; if the turn takes longer, the camera arrives late.
5. **Framing (Legal).** A camera that turns toward a sound is a security-product
   feature. Posts stay bird-only; no security words; contract side-project clause
   still unchecked. Limit pan in software to the garden so the camera never turns to
   a neighbour's window or the street. Save no audio.

## Plan impact

- Step 3 changes from "heat map on the webcam" to "turn the camera to the sound".
- UMA-16 is no longer needed. Chapter 2 still stands (it compared both boards).
- The bonus post says "I take the bow path: UMA-16". If Aaron picks Sipeed, section 8
  and summary point 3 change.

Hours (Aaron): PTZ test 1 h; record 6 channels and find the direction 1.5 h;
calibrate mic angle to camera angle 1.5 h; full loop 2 h. About 6 h, 2–3 weeks.

Sources:
[C545D datasheet](https://static.tp-link.com/upload/product-overview/2025/202510/20251028/Tapo%20C545D%201.0&1.6&1.8_Datasheet.pdf) ·
[Sipeed MA-USB8 wiki](https://wiki.sipeed.com/hardware/zh/modules/micarray_usbboard_bl616.html) ·
[pytapo](https://github.com/JurajNyiri/pytapo)
