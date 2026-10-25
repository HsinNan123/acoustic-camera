# Status

Updated: 2026-10-25

## Stage
Step 2 code done: a 16-mic map finds a bird at (20, 10) deg; 19 tests pass.
Chapter 1 live on Vocus; chapter 2 drafted (`docs/blog/02-sound-map.md`), not reviewed.
Direction changed 2026-10-25: Sipeed 6+1 USB board steers the outdoor Tapo C545D
telephoto lens toward the sound (`docs/research/sipeed-ptz-c545d.md`).
Step 3a passed 2026-10-25: ONVIF moves the C545D (firmware 1.1.7). Absolute, relative
and continuous pan all work; a 0.1-unit pan settles in 1.4 s or less. Degrees per
unit not measured yet.

## In progress
- Chapter 2: Aaron reviews (batch until DONE); then Claude publishes on Vocus from
  `docs/blog/02-sound-map.vocus.md`.
- Chapter 2 opening picture is made in Gemini; download waits for Aaron's OK.

## Blockers (needs Aaron)
- Buy the Sipeed 6+1 mic board with the MA-USB8 USB board; check the seller ships
  the USB board (raw 6 channels over USB), not the bare I2S 1. Step 3a': measure degrees per ONVIF unit: grab an RTSP frame before and after a
   pan, match the shift. Pass: a fixed number for pan and tilt. · Hours: 0.5
deg and back. · Hours: 0.5
2. Aaron: review chapter 2. · Hours: 1
3. Aaron: buy Sipeed 6+1 + MA-USB8 (Taobao). · Hours: 0.5
4. Step 3b: record the 6 raw channels, find the direction with our code. Pass: phone
   playing bird song, direction within 10 deg. · Hours: 1.5
5. Step 3c: map mic angle to camera angle (mount the board next to the camera).
   Pass: camera turns to the phone, phone in the telephoto view. Post 3. · Hours: 1.5
6. Step 4: bird mode: 2-8 kHz band, trigger, turn, save a short clip; pan limited to
   the garden. Pass: one real bird filmed. Post 4 + case. · Hours: 2
7. Bonus post: rewrite section 8 and summary point 3 for the Sipeed path. · Hours: 0.5
8. LinkedIn post: wait for a real demo (Aaron, 2026-10-25). · Hours: 0.5

## Known debt (not blocking)
- None.

## Decisions log
- 2026-10-25: Sipeed 6+1 board steering the Tapo C545D, not UMA-16 + webcam heat map;
  why: the telephoto view (57x32 deg) needs only a rough direction, the Sipeed board
  is cheaper, Aaron already has the camera. Reverse: buy UMA-16, back to the webcam.
- 2026-10-24: Blog style guide `docs/blog/STYLE.md`; why: chapter 1 took about 30
  corrections, the guide turns each into a rule and a checklist. Reverse: delete it.
- 2026-10-23: Simulate with numpy plane waves, not pyroomacoustics; why: no echoes
  needed yet, no extra install. Reverse: add pyroomacoustics when rooms matter.
- 2026-10-23: `gcc_phat` takes a `band`; why: a 2-6 kHz whistle read 25.8-36.5 deg at
  30 deg with all frequencies, 30.0 deg with the band. Reverse: drop the argument.
- 2026-10-23: Simulate before buying hardware; why: learn the limits (beam width,
  aliasing) for free and choose the array from data. Reverse: buy now.
- 2026-10-23: Public repo from Day -1, framed as a bird hobby; why: proof of work for
  the build log, and Aaron's employer works in security. Reverse: make repo private.
- 2026-10-23: Long-form on Vocus in Chinese, not own site or Medium; why: Taiwan
  audience, zero hosting hours (inference). Reverse: move posts, `docs/blog/` is the source.

## Pointers
Older decisions: `DECISIONS.md`. Shipped cases: `CASES.md`.
