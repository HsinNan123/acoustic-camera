# Status

Updated: 2026-10-26

## Stage
Step 2 code done: a 16-mic map finds a bird at (20, 10) deg; 23 tests pass.
Live on Vocus: chapter 1, chapter 2 (https://vocus.cc/article/6ade3729fd89780001e8fa1b)
and bonus post 1 (https://vocus.cc/article/6ade384efd89780001e92a0c), 2026-10-26.
Theory posts live 2026-10-26 (Aaron: "Post them", all three at once): bonus 2 how far
(https://vocus.cc/article/6adf4bf7fd8978000119d30b), bonus 3 echoes
(https://vocus.cc/article/6adf4cd2fd897800011a0799), bonus 4 angle to pixel
(https://vocus.cc/article/6adf4d7bfd897800011a314d).
Direction changed 2026-10-25: Sipeed 6+1 USB board steers the outdoor Tapo C545D
telephoto lens toward the sound (`docs/research/sipeed-ptz-c545d.md`).
Step 3a passed 2026-10-25: ONVIF moves the C545D (firmware 1.1.7). Absolute, relative
and continuous pan all work; a 0.1-unit pan settles in 1.4 s or less. Calibrated from
RTSP frames: pan 186 deg/unit, tilt 44 deg/unit (facts in CLAUDE.md Gotchas).

## In progress
- None. Waiting for the mic board.

## Blockers (needs Aaron)
- Buy the Sipeed 6+1 mic board with the MA-USB8 USB board; check the seller ships
  the USB board (raw 6 channels over USB), not the bare I2S board.

## Next (in order)
1. Aaron: buy Sipeed 6+1 + MA-USB8 (Taobao). · Hours: 0.5
2. Step 3b: record the 6 raw channels, find the direction with our code. Pass: phone
   playing bird song, direction within 10 deg. · Hours: 1.5
3. Step 3c: map mic angle to camera angle (mount the board next to the camera).
   Pass: camera turns to the phone, phone in the telephoto view. Post 3. · Hours: 1.5
4. Step 4: bird mode: 2-8 kHz band, trigger, turn, save a short clip; pan limited to
   the garden. Pass: one real bird filmed. Post 4 + case. · Hours: 2
5. LinkedIn post: wait for a real demo (Aaron, 2026-10-25). · Hours: 0.5

## Known debt (not blocking)
- Chapter 1 (published) still says 聲音地圖; STYLE now uses 聲源定位地圖. Left as is
  (Aaron, 2026-10-26).

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
