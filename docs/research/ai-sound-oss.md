# AI for bird sound: who and where (survey for bonus post 5)

Researched 2026-10-26 for Aaron's question 「有沒有 AI 相關的聲音定位 & 辨識跟開源專案」.
Licences read from each project's own page on that date unless marked "not verified".

## The picture in one diagram

```
                 bird song (6 mic channels)
                          |
          +---------------+----------------+
          |                                |
   WHERE: direction                 WHO: species
   (this project, classical)        (AI, mature, open)
   GCC-PHAT / beamforming           BirdNET, Perch 2.0
          |                                |
          +------------ both? -------------+
                          |
          AI that does both = SELD (research)
          trained on indoor sounds, no bird class
```

Finding: AI that names the bird is mature and free to use for a hobby. AI that finds
where the bird is, is still research, and its open models do not know birds. For a
bird camera, the practical design is classical direction + an AI species model.
That is our design already; the post can explain why.

## WHO: species recognition (mature)

| Project | What it does | Licence | Fit for us |
|---|---|---|---|
| [BirdNET-Analyzer](https://github.com/birdnet-team/BirdNET-Analyzer) (Cornell + TU Chemnitz) | Names the species in a 3 s clip; 6,512 species | Code MIT; models CC BY-NC-SA 4.0 | Yes, hobby only (non-commercial) |
| [BirdNET-Go](https://github.com/tphakala/birdnet-go) | Runs BirdNET 24/7 on a Raspberry Pi 4 or a PC; web page, alerts | CC BY-NC-SA 4.0 | Yes, as a ready app; no direction feature |
| [Perch 2.0](https://arxiv.org/pdf/2508.04665) (Google) | Species model for 14,597 species: birds, mammals, frogs, insects; tops BirdSet and BEANS benchmarks | Code Apache 2.0 ([perch](https://github.com/google-research/perch), [perch-hoplite](https://github.com/google-research/perch-hoplite)); weights on Kaggle: **not verified** | Yes for learning; check weights licence before any public demo |
| [OpenSoundscape](https://github.com/kitzeslab/opensoundscape) (Kitzes Lab) | Python toolbox: runs BirdNET and Perch, trains your own classifier, **locates sounds from several synced recorders** | MIT (from the repo sidebar) | Best single toolbox to show both halves |
| [NatureLM-audio](https://projects.earthspecies.org/naturelm-audio/) (Earth Species Project) | Audio + language model: you ask "what animal is this?" in words | Open weights on Hugging Face; licence **not verified**; built on Llama 3.1 | Good "future" example, too big for a laptop demo |

## WHERE: AI localization (research)

| Project | What it does | Licence | Fit for us |
|---|---|---|---|
| [SELDnet baseline, DCASE 2023](https://github.com/sharathadavanne/seld-dcase2023) | One network outputs "which sound" + "which direction" every 100 ms, from a 4-mic array | MIT | Good to explain; needs retraining for birds |
| [STARSS23 dataset](https://zenodo.org/records/7709052) (Sony + Tampere) | Real recordings with direction labels | MIT | 13 classes, **none are birds** |
| [DCASE 2025 Task 3](https://zenodo.org/records/15559774) | Same task from stereo audio + video; adds distance | Repo licence **not verified** | Shows where research is going |
| HARKBird ([Interspeech 2016](https://www.isca-archive.org/interspeech_2016/suzuki16b_interspeech.html), [Journal of Ecoacoustics 2018](https://jea.jams.pub/article/2/2/43)) | Direction + separation of bird songs with HARK and a 16-mic array; 2.0 adds song clustering | Software licence and download **not found** | Closest to our project; cite, do not reuse |
| [EMF 2026 talk, Mike Davis](https://app.media.ccc.de/v/emf2026-83-1-taking-the-fun-out-of-bird-watching-microphone-array) | FPGA mic array + beamforming to find each bird in a tree, 3D video | Talk CC BY-SA 4.0; code not released | Good "someone else did this" story |

## Bonus post 5 outline (provisional)

Title: 聲音相機 番外篇 5：AI 能聽出是哪一種鳥、在哪裡嗎？

1. AI 很會「認鳥」：BirdNET 和 Perch 聽 3 秒就說出名字（metaphor: 圖鑑 vs 認得同學的聲音）.
2. AI 還不太會「指方向」：會指方向的 AI 是用室內聲音訓練的，13 種聲音裡沒有鳥.
3. 所以我的做法：麥克風板用數學指方向，AI 負責認鳥；兩邊各做最擅長的事.
4. 可以自己玩的開源專案：BirdNET-Go（樹莓派）、OpenSoundscape（Python）.
5. 授權要注意：BirdNET 模型只能非商業使用.

Hours (Aaron): review 1, publish 0.5.
Legal: text and links only, no third-party pictures; BirdNET and Perch are named, not
redistributed. Open item: the Perch 2.0 weights licence before any demo that uses it.
