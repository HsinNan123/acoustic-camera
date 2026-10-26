# Acoustic Camera

A hobby build: find a bird outside my window by its song.

A microphone array hears a sound a few microseconds earlier at one mic than at the
next. From those delays the code works out the direction of the sound, and draws it
as a heat map on live video: where the sound is, and how loud.

I build it step by step, in public, and write up what I learn at each step.

## The pipeline

```
[1 Sound + delay] -> [2 Beamformer map] -> [3 Heat map on video] -> [4 Real array] -> [5 Bird mode]
  2 simulated mics    16 simulated mics     webcam + overlay         real mic array      bird-song filter,
  find the angle      scan a grid           volume in dB             live audio          find a real bird
```

Steps 1-3 run on simulated sound, so no hardware is needed to follow along.

## Build log

| Step | What it proves | Code | Post |
|---|---|---|---|
| 1 | Two mics can find the angle of a sound | [`acam/delay.py`](acam/delay.py) | [Vocus](https://vocus.cc/article/6adcc21cfd89780001a98cf2) |
| 2 | Many mics make a 2D sound map | [`acam/beamform.py`](acam/beamform.py) | [Vocus](https://vocus.cc/article/6ade3729fd89780001e8fa1b) |
| Bonus | How people build acoustic cameras; why a small board can steer a long lens | [`scripts/step3_pointing_sim.py`](scripts/step3_pointing_sim.py) | [Vocus](https://vocus.cc/article/6ade384efd89780001e92a0c) |
| Bonus 2 | How far away a bird can still be found | [`scripts/bonus2_how_far.py`](scripts/bonus2_how_far.py) | [Vocus](https://vocus.cc/article/6adf4bf7fd8978000119d30b) |
| Bonus 3 | Echoes from the ground and the wall | [`scripts/bonus3_echoes.py`](scripts/bonus3_echoes.py) | [Vocus](https://vocus.cc/article/6adf4cd2fd897800011a0799) |
| Bonus 4 | From an angle to a turn and a pixel | [`scripts/bonus4_angle_to_pixel.py`](scripts/bonus4_angle_to_pixel.py) | [Vocus](https://vocus.cc/article/6adf4d7bfd897800011a314d) |
| Bonus 5 | Can AI tell which bird is singing, and where? (BirdNET demo) | [`scripts/bonus5_birdnet.py`](scripts/bonus5_birdnet.py) | draft |
| 3 | The map lines up with the video | not yet | not yet |
| 4 | It works with a real array | not yet | not yet |
| 5 | It finds a real bird | not yet | not yet |

## Run it

```
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python -m pytest
```

## Privacy

Audio is processed in memory. Nothing is recorded unless bird mode saves a short
clip, and that clip keeps only the bird-song frequencies.

## Licence

Code: MIT (see `LICENSE`). Blog text in `docs/blog/`: © Aaron, all rights reserved.
