# Status

Updated: 2026-10-24

## Stage
Step 1 code done: two simulated mics find the angle (GCC-PHAT), 10 tests pass.
Max error 0.5 deg within +-60 deg. Chapter 1 reviewed with Aaron, rewritten for a
12-year-old, 8 figures in Chinese; style rules in `docs/blog/STYLE.md`.
Path: simulate first (steps 1-3), buy an array after step 2. Each step: post + git tag.

## In progress
- Post 1 is live on Vocus (2026-10-24): https://vocus.cc/article/6adcc21cfd89780001a98cf2.
  LinkedIn short post not done.

## Blockers (needs Aaron)
- None.

## Next (in order)
1. Post 1 on LinkedIn (English, short, links to Vocus and tag `step-1`). · Hours: 0.5
2. Step 2: delay-and-sum beamformer, 2D power map. Simulate the UMA-16 4x4 grid and the
   Sipeed 6-mic circle side by side. Pass: peak within 3 deg at 1, 2, 4 kHz. Post 2:
   "Which array to buy, decided by simulation". · Hours: 3
3. Aaron: check Taobao prices for UMA-16, Pawpaw PXUA216MB-DL2-M, Sipeed MicArray +
   MA-USB8; confirm raw PCM of every mic over USB. Buy one. · Hours: 0.5
4. Step 3: heat map and dB label over the laptop webcam, simulated moving source.
   Pass: saved frames show the hot spot on the expected pixel. Post 3 + case. · Hours: 3
5. Step 4: live audio from the real array. Pass: phone playing bird song, hot spot on
   the phone, lag under 0.5 s. Post 4. · Hours: 3
6. Step 5: bird mode: 2-8 kHz band-pass, event trigger, save short clips. Pass: one
   real bird located. Post 5 + case. · Hours: 3

## Known debt (not blocking)
- None.

## Decisions log
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
