# Status

Updated: 2026-10-23

## Stage
Day -1: repo, docs and plan exist; no code yet.
Path: simulate first (steps 1-3, no hardware), buy an array after step 2.
Each step ends with a post (Vocus long-form, LinkedIn short) and a git tag.

## In progress
- Nothing yet. Plan: `C:\Users\Aaron\.claude\plans\i-want-to-start-effervescent-pretzel.md`.

## Blockers (needs Aaron)
- None for step 1.

## Next (in order)
1. Step 1: two simulated mics, time delay by cross-correlation (GCC-PHAT), find the
   angle. Pass: source at 30 deg estimated within 2 deg. Post 1. · Hours: 2.5
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
- 2026-10-23: Simulate before buying hardware; why: learn the limits (beam width,
  aliasing) for free and choose the array from data. Reverse: buy now.
- 2026-10-23: Public repo from Day -1, framed as a bird hobby; why: proof of work for
  the build log, and Aaron's employer works in security. Reverse: make repo private.
- 2026-10-23: Long-form on Vocus in Chinese, not own site or Medium; why: Taiwan
  audience, zero hosting hours (inference). Reverse: move posts, `docs/blog/` is the source.

## Pointers
Older decisions: `DECISIONS.md`. Shipped cases: `CASES.md`.
