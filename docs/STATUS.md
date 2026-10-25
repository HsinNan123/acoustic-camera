# Status

Updated: 2026-10-25

## Stage
Step 2 code done: a 16-mic map finds a bird at (20, 10) deg; 19 tests pass.
Chapter 1 live on Vocus; chapter 2 drafted (`docs/blog/02-sound-map.md`), not reviewed.
Simulation says buy UMA-16 (spot 24 vs 40 deg, ghost 34 vs 66%); price not checked.

## In progress
- Chapter 2: Aaron reviews (batch until DONE); then Claude publishes on Vocus from
  `docs/blog/02-sound-map.vocus.md`.
- Chapter 2 opening picture is made in Gemini; download waits for Aaron's OK.

## Blockers (needs Aaron)
- Price check and purchase of the array (UMA-16 first choice).

## Next (in order)
1. Aaron: review chapter 2. · Hours: 1
1a. Aaron: decide the direction: Sipeed 6+1 board steering the outdoor Tapo C545D
   (`docs/research/sipeed-ptz-c545d.md`), or UMA-16 + webcam heat map. If Sipeed,
   steps 3-5 and bonus post section 8 change. · Hours: 0.5
2. Aaron: check Taobao prices for UMA-16, Pawpaw PXUA216MB-DL2-M, Sipeed MicArray +
   MA-USB8; confirm raw PCM of every mic over USB. Buy one. · Hours: 0.5
3. Step 3: heat map over the laptop webcam, simulated moving source. Pass: saved frames
   show the hot spot on the expected pixel. Post 3 + case. · Hours: 3
4. Step 4: live audio from the real array. Pass: phone playing bird song, hot spot on
   the phone, lag under 0.5 s. Post 4. · Hours: 3
5. Step 5: bird mode: 2-8 kHz band-pass, event trigger, save short clips. Pass: one
   real bird located. Post 5 + case. · Hours: 3
6. LinkedIn post: wait for a real demo (Aaron, 2026-10-25). · Hours: 0.5

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
