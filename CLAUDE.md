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
- **Stack and where it runs:** Python 3.13, numpy, scipy, pyroomacoustics
  (simulation), sounddevice (audio in), opencv-python (video and overlay), pytest. Runs
  on Aaron's Windows laptop. No server, no web. Public repo:
  https://github.com/HsinNan123/acoustic-camera
- **Scale:** one user, one machine. Rules out cloud, accounts, database.
- **Serves portfolio goal:** brand.

## Repo map
- `acam/`: core module (geometry, delays, beamformer, map-to-pixels). Tested.
- `tests/`: pytest, one test file per `acam/` module.
- `scripts/`: one runnable script per build step (`step1_two_mics.py`, ...).
- `docs/blog/`: one Markdown chapter per step, the source for each post.
- Never search: `out/`, `recordings/`, `.venv/`.

## Commands (from `Acoustic Camera/`)
- Setup: `python -m venv .venv`, then `.venv\Scripts\pip install -r requirements.txt`.
- Tests: `.venv\Scripts\python -m pytest`.
- Dev server: none. A script writes its plot or frame to `out/`; Aaron checks the image.

## Project-specific gate lines
- Legal: process audio in memory; save no raw audio by default. Clips (step 5 only)
  are band-passed to the bird range. Posted video shows sky and trees; blur any face
  or plate. Public framing is a bird hobby: no VIVOTEK names, products or security
  pitch until Aaron checks his contract's side-project clause. Code is MIT; blog text
  in `docs/blog/` is © Aaron. BirdNET, if used, is CC BY-NC-SA: hobby use only.
- Growth: one post per step. Long-form in Chinese on Vocus (方格子); short English
  post + GIF on LinkedIn, linking to Vocus and to the step's git tag (`step-1`, ...).
- Ship: `main` is public on GitHub. Never commit audio, video or `.env*` files.

## Gotchas (learned the hard way)
- _[one line each; a fact that stopped changing in STATUS moves here]_
