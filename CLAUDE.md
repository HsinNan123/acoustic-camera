# Acoustic Camera: project facts

Only what is specific to this project. The working agreement (roles, gates, how to
work, verify, ship, token rules, Windows notes) is `../CLAUDE.md`; do not repeat it.
Volatile state (stage, blockers, next, decisions) is `docs/STATUS.md`.

## Context
- **What it is:** an acoustic camera prototype: a microphone array finds where a sound
  comes from and draws its position and volume as a heat map on live video.
- **For whom:** Aaron first (learning, finding birds outside his window); readers of
  his public build log.
- **Goals, in order:** 1. learn the method and explain it; 2. a public build log with a
  demo GIF per step; 3. a working live demo on a real bird.
- **Stack and where it runs:** Python 3.13, numpy, scipy, matplotlib (simulation and
  plots), pytest; later sounddevice (audio in), opencv-python (video). Runs
  on Aaron's Windows laptop. No server, no web. Public repo:
  https://github.com/HsinNan123/acoustic-camera
- **Scale:** one user, one machine. Rules out cloud, accounts, database.
- **Serves portfolio goal:** brand.

## Repo map
- `acam/`: core module (geometry, delays, beamformer, map-to-pixels). Tested.
- `tests/`: pytest, one test file per `acam/` module.
- `scripts/`: one runnable script per build step (`step1_two_mics.py`, ...).
- `docs/blog/`: one Markdown chapter per step, the source for each post; figures in
  `docs/blog/img/`, written by the step scripts.
- Never search: `out/`, `recordings/`, `.venv/`.

## Commands (from `Acoustic Camera/`)
- Setup: `python -m venv .venv`, then `.venv\Scripts\pip install -r requirements.txt`.
- Tests: `.venv\Scripts\python -m pytest`.
- Dev server: none. A step script writes its figures to `docs/blog/img/` and prints
  the numbers the post uses; Aaron checks the images.

## Project-specific gate lines
- Legal: process audio in memory; save no raw audio by default. Clips (step 5 only)
  are band-passed to the bird range. Posted video shows sky and trees; blur any face
  or plate. Public framing is a bird hobby: no VIVOTEK names, products or security
  pitch until Aaron checks his contract's side-project clause. Code is MIT; blog text
  in `docs/blog/` is © Aaron. BirdNET, if used, is CC BY-NC-SA: hobby use only.
- Growth: one post per step. Long-form in Chinese on Vocus (方格子); short English
  post + GIF on LinkedIn, linking to Vocus and to the step's git tag (`step-1`, ...).
- Blog voice (Aaron, 2026-10-24): write every chapter for a 12-year-old. Each idea
  starts with a metaphor or picture (one metaphor per idea, reused across chapters).
  Formulas and exact settings go in short "大人補充" notes a child can skip. The
  opening summary is three points, concepts only: no math, no numbers. Headings
  state the knowledge point, not a story hook. Figure titles state the point; axis
  labels say what they mean in plain words.
- Ship: `main` is public on GitHub. Never commit audio, video or `.env*` files.

## Gotchas (learned the hard way)
- _[one line each; a fact that stopped changing in STATUS moves here]_
