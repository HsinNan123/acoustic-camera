# Open-source acoustic cameras (聲學攝影機): survey

Role: PM (+Marketing, Lawyer). Date: 2026-10-25. Repo facts (licence, stars, last push)
checked with the GitHub API on that date; other facts from the linked pages.

## Summary

- The community splits into four tiers by hardware: software only, Raspberry Pi + USB
  array, microcontroller (ESP32 / Teensy / STM32 / K210), and FPGA with 60 to 96 mics.
- The closest match to our build is Benn Jordan's "sound camera under $400": miniDSP
  UMA-16 + Raspberry Pi 5 + Acoular, which found a hawk in a tree. Same board we chose.
- No real "Arduino" acoustic camera exists: classic Arduino boards are too slow for
  many-mic audio; ESP32 projects stream audio to a PC that draws the map.

## The four tiers

```
[Software]            [Pi + USB array]          [Microcontroller]          [FPGA, 60-96 mics]
Acoular, Spectacoular  UMA-16 + Pi 5 (Jordan)    ESP32 4-mic (AcousticCam)  Sesenta 60-mic tiles
ODAS, pyroomacoustics  Matrix Creator + Pi 3     Teensy / STM32 4-6 mic     jduanen 96-mic spiral
                       ReSpeaker + ODAS          Sipeed K210 7-mic (map)
cost: free             about US$400              about US$20-60             hundreds of US$
```

## Projects

| Project | Tier | Mics | What it does | Licence | Activity | Fit for a Taiwan intro |
|---|---|---|---|---|---|---|
| [Acoular](https://github.com/acoular/acoular) | Software | any | Python beamforming and source maps; the standard library (TU Berlin) | BSD-3 | 664 stars, pushed 2026-10-24 | High: the engine most builds use |
| [Spectacoular](https://github.com/acoular/spectacoular) | Software | any | Browser GUI apps on top of Acoular (mic geometry, beamforming, level meter) | BSD-3 | 54 stars, pushed 2026-10-24 | Medium |
| [ODAS](https://github.com/introlab/odas) | Software | 4-16 | Localize and track sound sources live on a Pi; ODAS Studio shows them on a globe (Univ. Sherbrooke) | MIT | 1,081 stars, last push 2024-12-05 | High: works with ReSpeaker boards sold in Taiwan |
| [pyroomacoustics](https://github.com/LCAV/pyroomacoustics) | Software | any | Room simulation and direction finding (SRP-PHAT, MUSIC) | MIT | 1,996 stars, pushed 2026-07-17 | Medium: good for learning |
| Benn Jordan, [Hackaday write-up](https://hackaday.com/2024/10/10/building-a-sound-camera-for-under-400/) | Pi + USB | 16 | miniDSP UMA-16 (about US$275) + Raspberry Pi 5 + 1080p camera + Acoular; found a hawk in a tree and which chicken was calling | No code linked | Video 2024 | High: the story readers will like; same path as ours |
| [rabeaifeanyi/acoustic-camera](https://github.com/rabeaifeanyi/acoustic-camera) | Pi/PC + USB | 16 | Acoular acoustic camera for UMA-16, optional ML model | None stated | 58 stars; author says unmaintained, points to Spectacoular | Low |
| [gzazartur/Acoustic-Camera](https://github.com/gzazartur/Acoustic-Camera) | Pi + HAT | 8 | Raspberry Pi 3B+ + Matrix Creator, delay-and-sum, Pi camera, 5-inch screen | GPL-3.0 | 0 stars, 2021 | Low: Matrix boards are hard to buy (not verified) |
| [22carlo22/AcousticCam](https://github.com/22carlo22/AcousticCam) | ESP32 | 4 | ESP32 sends camera and 4 mics to a PC, which draws the heat map; standalone v2 in progress | None stated | 43 stars, pushed 2026-09-26 | High: cheapest build, a kid could follow |
| [Sipeed MicArray](https://wiki.sipeed.com/hardware/zh/modules/micarray.html) + MaixPy | K210 | 7 | The board itself draws a sound-source map on an LCD (`mic.get_map()`) | MaixPy: not asserted | MaixPy 1,709 stars, last push 2024-06 | Medium: Chinese docs; candidate board from step 2 |
| [aditalrazi/embedded-acoustic-camera](https://github.com/aditalrazi/embedded-acoustic-camera), [totoroKr/Acoustic-Camera](https://github.com/totoroKr/Acoustic-Camera) | Teensy / STM32 | 4 | Student projects: 4 mics, GCC-PHAT / SRP-PHAT, marker on a webcam | None stated | 0 stars, 2026-10 | Low |
| [mcbridejc/acoustic-array-tools](https://github.com/mcbridejc/acoustic-array-tools) | STM32H7 | 6 | Beamforming on the MCU, GUI power grid | None stated | 10 stars, 2022 | Low |
| [Sesenta / OpenAcousticCamera](https://hackaday.io/project/192750-sesenta-open-source-tileable-acoustic-camera) ([repo](https://github.com/Iari-Lab/OpenAcousticCamera)) | FPGA | 60 per tile | Tileable boards of 60 MEMS mics, Zynq XC7Z020; 8-mic beamforming demo Jan 2026 | Page states GPL-3.0 (software) + CERN-OHL-2 (hardware); GitHub detects none | 26 stars, pushed 2026-10-24 | Medium: impressive open hardware |
| [jduanen/Acoustic-Camera](https://github.com/jduanen/Acoustic-Camera) | FPGA | 96 | Staged build: simulation → ReSpeaker → UMA-16 (done) → 96-mic log-spiral on Artix-7 (PCB in layout); DAS, MVDR, CLEAN-SC, MUSIC | MIT | 15 stars, pushed 2026-10-24 | High: best design write-up, same staged path as ours |
| [simongapp/xmos_usb_mems_interface](https://github.com/simongapp/xmos_usb_mems_interface) | USB hardware | 16 | XMOS board that turns 16 MEMS mics into a USB sound card; tested with Acoular | None stated | 22 stars, 2021 | Low |

Lists for further digging: [beamforming-tools](https://github.com/eac-ufsm/beamforming-tools),
[Awesome Acoustic](https://nitnelav.github.io/awesome-acoustic/).

## What this means for our project

- **Our board choice matches the community default.** Benn Jordan, jduanen (phase 3) and
  rabeaifeanyi all use the miniDSP UMA-16. This supports the step 2 decision.
- **Acoular is the next tool**, not something to rebuild. Its CLEAN-SC can sharpen the
  map and remove ghosts; worth a chapter after step 4.
- **ODAS is the tool for moving birds** (tracking several sources), if step 5 needs it.

## Taiwan audience: a bonus post

- Idea: 「聲音相機 番外篇：全世界的人怎麼自己做聲學攝影機」. Four tiers, each with one
  hero project and its price, written to STYLE.md (12-year-old, metaphors).
- Growth: audience = Taiwan makers on Vocus; message = "you can build one from
  NT$1,000 to NT$13,000"; cost about 1 Aaron-hour to review; metric = views and new
  followers vs chapter 1; smallest test = this one post.
- Legal: describe projects in our own words and link to them. Do not copy their images
  or code into the post; several repos state no licence, which means no reuse rights.
  Our own figures and a Gemini picture only.

## Not verified

- Prices: only the UMA-16 (about US$275, from the Hackaday article) is quoted; the
  others are tier estimates.
- Whether each repo builds and runs today.
- Matrix Creator availability.
- Sesenta's licence files (GitHub detects none; the project page states them).
