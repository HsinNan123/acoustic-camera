# Build log: style guide

Every chapter follows this file. It comes from Aaron's review of chapter 1
(2026-10-23 to 2026-10-24); each rule fixes a correction he had to make.
Run the checklist at the end before handing a draft to Aaron.

## 1. Reader

- A 12-year-old reads it on a phone. If a child would stop at a word, change the word.
- Long-form is Traditional Chinese for Vocus. Aaron's own sentences stay exactly as
  he wrote them.

## 2. Chapter shape

1. Title: `聲音相機 #N：<the question this chapter answers>`.
2. Draft note (one quote line): numbers come from the step script; code tag `step-N`.
3. **重點摘要：3 points.** Concepts only: no formula, no number, no technical term
   that the chapter has not explained yet. Each point is one idea, not two.
4. Hook: why this step matters for finding the bird, in two to three lines.
5. A concept picture made with Gemini, right after the hook. Every chapter has one.
   How to make it: section 9.
6. Numbered sections. Last section: what this method cannot do, which leads to the
   next chapter. Then a 程式碼 section with links.

## 3. Section headings

- State the knowledge point in a child's words. Not a story hook ("第一個驚訝"),
  not a question, not a formula (no "∝ 1/cos θ", no "5.9 個取樣點").
- One idea per heading. If it needs "；", the idea is the part before it.
- The heading states the finding; the metaphor stays in the body (Aaron, 2026-10-26:
  "像海上的浮板" out of the heading). 例："3. 高音比低音容易定位". Name the finding, not
  the topic: never "…的關係".
- Results from an experiment are 發現 (findings), not 規則. A 規則 is how a method
  is designed (例：GCC-PHAT 每位評審只有一票).

## 4. Inside a section

Order: metaphor → plain explanation → figure → how to read the figure → key numbers
→ `深入一點` note.

- **Metaphor first.** One metaphor per idea, reused in every later chapter.
- **A metaphor must not collide with a real thing in the project.** This project has
  a real video camera, so never say "更快的相機"; name the real thing
  (取樣更快的麥克風).
- **Define every new word at first use**: 微秒, 正確率, 訊雜比, dB.
- **Say what a number counts.** "整數" alone confused Aaron (seconds?); write
  "晚 0、1、2、3… 張照片".
- **Software and algorithms never get a hardware metaphor**: readers mix them up with
  the boards (Aaron, 2026-10-26: 瞄準鏡 for software). Use a non-object one (食譜書).
- **Stay on topic**: cut a side question that does not move the post's idea (the
  Arduino section), and keep notes about the post itself out of it.
- **Plain verbs over vivid ones.** "雜訊多的時候，聽久一點，比較好判斷", not
  "聽久一點可以撐住". "猜照片之間", not "補畫".
- **dB always comes with 幾倍**: "-10 dB（雜訊大 10 倍）". dB is a multiply scale,
  like 地震規模.
- **Math goes in `> **深入一點：**`** notes a child can skip: formulas, exact
  settings, sample counts. Never call them 大人補充.

## 5. Fixed terms (one term per thing, in text and figures)

| Thing | Term to use | Never |
|---|---|---|
| Sample | 聲音照片（取樣點, defined once） | 取樣點 alone after section 2 |
| Sample rate | 每秒拍幾張聲音照片 / 取樣更快的麥克風 | 更快的相機 |
| Wavefront | 浪頭（波前） | |
| Coarse method | 只猜整數張照片 | 只數照片, 只看取樣點 |
| Fine method | 也猜照片之間 | 補畫, 補細, 16x finer |
| Why fine works | 連連看：點跟點之間只有一種平滑的連法 | |
| GCC-PHAT | 評審投票；每個高低音是一位評審，每人一票 | |
| Counting votes | 計票 | 算票 |
| A dot in the vote figure | 一個猜法 | 照片 |
| Share of right answers | 正確率（200 次裡指對的比例） | runs within 2 deg, 成功率, 指對 |
| Sudden failure | 斷崖 | |
| Error grows toward the side | 爬圓山：山腰走一步高度變很多，山頂幾乎不變 | |
| Angle error spreads with distance | 手電筒：手轉一點，遠處光點移很多 | |
| Front-back ambiguity | 照鏡子 | |

| Angle (1D) to map (2D) | 一條線只分得出左右，排成一個面才分得出上下；倉鴞的耳朵一高一低 | |
| Delay-and-sum beamforming | 每個方向都計算一次；方向對時大家齊步走（運動會進場）。板子不動，電腦算 | 軍訓, 猜, 掃過, 掃描 |
| The map itself | 聲源定位地圖 | 聲音地圖, 定位地圖 |
| Beamforming output | 對齊程度（地圖顏色，1 = 最整齊） | |
| Main lobe | 紅點 | |
| Array | 板子（UMA-16、Sipeed） | |
| Wavelength | 波長, defined once as 兩個浪頭之間的距離; 浪頭 only inside the 浮板 metaphor | 浪頭間距 after the definition |
| Why low sound is blurry | 浮板：浪很長，整塊浮板一起上下，感覺不出方向 | 尺 (taken by chapter 1) |
| Grating lobe / strong sidelobe | 鬼影 | |
| Spatial aliasing | 車輪倒轉：照片拍得不夠密 | |
| 2-mic ambiguity on a map | 一條紅色直帶 | |
| Array gain | 多幾隻耳朵一起聽 | |

| DIY build tiers | 彈弓（小電腦板）、弓箭（樹莓派＋麥克風板）、大砲（FPGA 大陣列） | 走路、腳踏車、汽車、火車 |
| Software toolbox | 食譜書：每一道食譜是一種方法（齊步走是其中一道） | 瞄準鏡 |
| Small board + long lens | 彈弓負責聽（給方向），大砲負責看（長鏡頭轉過去拍） | |
| Why weapon words are safe here | 拍鳥的人把拍鳥叫「打鳥」，長鏡頭叫「大砲」；工具都是拿來聽鳥、看鳥 | 射鳥, 打下來 |
| Open source / licence | 開源；授權（沒寫授權 = 只能看，不能拿來用） | |

| Spreading loss | 噴漆：離越遠，噴到的範圍越大，顏色越淡。距離加倍，聲音小 4 倍 | 手電筒 (taken) |
| Air absorption | 遠處的打雷只剩轟隆隆：高音在空氣裡掉得比較快 | |
| Song vs background sound | 在吵雜的教室裡聽悄悄話 | |
| Reflection | 撞球碰到桌邊彈回來 | |
| Image source | 假鳥（回音好像從它那裡傳來） | 鬼影 (taken) |
| Listen to the first arrival only | 浴室裡也聽得出朋友在哪：大腦相信最先到的聲音 | |
| Field of view | 紙筒：長紙筒（長鏡頭）看得窄，短紙筒（廣角）看得寬 | |
| Pixel | 像素（畫面上的一個小格子） | |
| Angle to pixel | 針孔相機：紙箱上戳一個小洞 | |
| More pixels per degree at the edge | 傍晚的影子拉得長 | |
| Measuring a turn from two frames | 疊兩張描圖紙，推到圖案對齊 | |
| Gear slack | 腳踏車鏈條鬆鬆的；每次從同一邊轉過去 | |
| Two viewpoints differ | 閉一隻眼看手指，手指好像跳了一下 | |

New chapters add rows here; they do not invent a second word for an existing row.

## 6. Figures

- **Language**: Traditional Chinese, font Microsoft JhengHei, `axes.unicode_minus`
  off. Same terms as the text (table above).
- **Title states the point**, as a sentence a child can repeat. Not a description of
  the axes.
- **Axis labels say the meaning**, with the direction when it matters:
  "答錯幾度（越低越準）", "← 越吵　越安靜 →".
- **Integer ticks** (0, 5, 10, 15, 20); no 2.5 steps.
- **Helper axes** when a unit is abstract: "猜：晚幾張照片" above microseconds;
  "雜訊是聲音的幾倍" above dB.
- **One idea per figure**, placed in the section whose idea it shows. Do not stack
  a waveform and a vote result in one image.
- **When dots mean different things in two figures, say so in the text**
  (聲音照片 vs 一個猜法).
- **Under every figure**: one line per line or colour, saying what it is and what to
  notice.
- **Pictures from other projects**: only from a project whose licence allows reuse (MIT,
  BSD, Creative Commons). No licence: no picture, a link only. The alt text ends with
  `（圖：作者，repo，授權）`, because the alt text becomes the Vocus caption. Strip photo
  metadata (GPS) when resizing. Add the licence text to `docs/blog/img/THIRD_PARTY.md`
  and a 圖片出處與授權 table at the end of the post.
- **Numbers in titles are computed by the script**, never typed.
- **Check by eye** after every redraw: no label on a line, no legend over a label,
  no cut-off title, no meaningless tick (例：-200 on a time axis).

## 7. Numbers

- Every number in the text comes from the step script's printed output. Rerun the
  script after any change and check the numbers still match.
- Pick examples that show the effect (36 度 shows the 5-degree error; 30 度 sits
  almost on a line and hides it). Say in the text which example the figure uses.

## 8. Checklist before handing a draft to Aaron

- [ ] Opening concept picture from Gemini is in place, captioned `AI 生成，Gemini`.
- [ ] Summary: 3 points, no math, no numbers, one idea each.
- [ ] Every heading: one knowledge point, child's words, no hook, no formula.
- [ ] Every section opens with a metaphor from the table, or adds a new row.
- [ ] No term outside the table's "Term to use" column (search for the "Never" words).
- [ ] Every new word defined at first use; every number says what it counts.
- [ ] Every formula and exact setting is inside a 深入一點 note.
- [ ] Every figure: Chinese, point in title, plain axis labels, integer ticks,
      text under it explains each line, checked by eye.
- [ ] Script rerun; numbers in text match its output; tests pass.
- [ ] Publish kit `NN-<slug>.vocus.md` is ready; 摘要 counted at 150 characters or fewer.

## 9. Opening picture with Gemini (every chapter)

Aaron asked for this on 2026-10-24. Claude makes it; Aaron does not need to.

1. **Browser**: the built-in browser of the Claude desktop app (the session's
   default browser), at `https://gemini.google.com/app`. Aaron's Google account is
   already signed in there. If a sign-in page shows, stop and ask Aaron to sign in.
2. **Prompt**: start with `Create an image:`, then the shared style, then this
   chapter's scene. Keep the shared style word for word so every chapter looks like
   one series:

   ```
   A friendly flat-vector illustration for a children's science blog. Soft daylight,
   clean and simple, no text, 16:9. Recurring characters: a small brown songbird with
   an orange chest; a square green circuit board with 16 tiny microphones in a 4x4
   grid and a small camera in the middle; a home window looking out at a garden tree.
   Scene: <one or two sentences showing this chapter's main idea>
   ```

   No text in the image: Gemini writes Chinese wrongly. Labels go in the caption.
3. **Check** the result before saving: it shows the chapter's idea, no text, no
   real brand or person. If not, ask Gemini for one new version, saying what to fix.
4. **Download**: ask Aaron in one line first (file, source, size), as every download
   needs his OK. Then use Gemini's "Download full size image" button; the file lands
   in `C:\Users\Aaron\Downloads` as an unnamed `*.tmp` first, renamed to
   `Gemini_Generated_Image_*.jpg` some seconds later. Check it is a whole JPEG
   (opens, ends in `ff d9`).
5. **Save** as `docs/blog/img/stepN_concept.jpg`, resized to 1600 px wide, JPEG
   quality 85 (about 120 KB). Leave the original in Downloads.
6. **Caption** under the image: what to notice, then `（AI 生成，Gemini）`.
7. **Record** the scene sentence in the commit message, so the picture can be made
   again.

Chapter 1 scene: "View from inside a home, looking out a window at a garden tree. A
small bird sings on a branch. A colorful heat-map glow is overlaid on the bird, like
a thermal camera image: red at the center, fading to yellow, green and blue. It shows
where the sound comes from. On the window sill sits the microphone board."

## 10. Publishing on Vocus

Aaron asked on 2026-10-24: every setting is prepared before publishing, not decided
on the settings page. Chapter 1's kit is `01-two-mics.vocus.md`; copy its shape.

**Publish kit** (`docs/blog/NN-<slug>.vocus.md`, written with the draft, shown to
Aaron with it):

| Setting | Rule |
|---|---|
| 標題 | Same as the chapter's H1 |
| 分類 | 科技 (default for this series) |
| 摘要 | **150 characters at most**, Vocus's hard limit. Concepts only, no math, like the summary. Count it. |
| 縮圖 | The Gemini picture (first image in the article) |
| 關鍵字 | 3 to 20. No hyphen (Vocus rejected "GCC-PHAT"). Never a security word (監控, 安防, 監視). Fixed series words: 聲音相機、麥克風陣列、聲源定位、訊號處理、科普、賞鳥, plus the chapter's own |
| 主題活動 | Only one that fits the post; say its end date |
| 進階 | 文章目錄 on; 標記含 AI 輔助或生成 on (Gemini picture, Claude draft) |
| 權限和狀態 | 免費公開, 林信男的沙龍, 公開發佈 |

**Steps** (built-in browser, Aaron's account is signed in; phone verification done):

1. Push the repo first: Vocus copies each image from its public GitHub address.
2. `python scripts/md_to_vocus.py docs/blog/NN-<slug>.md out/chN_vocus.json`. It drops
   the H1 and the draft note, points images at GitHub, and joins lines.
3. vocus.cc → 創作 → 文章 opens a new draft. Type the title into the title box.
4. Click once into the body (the paste needs a cursor), then paste the HTML with a
   `ClipboardEvent('paste')` carrying `text/html`. Check: headings, images all on
   `images.vocus.cc`, notes, tables, links.
5. 準備發佈 → fill the three pages from the kit. Watch for traps:
   - The summary box is pre-filled: select all, delete, then type.
   - The keyword box is pre-filled with auto words: remove them all.
   - A theme tag opens a dialog; confirm with 確定投稿.
6. Stop before 確認發佈 and show Aaron the kit and the draft, unless his request
   already said to publish with this kit.
7. After publishing, open the article URL and check: 9-ish headings, no broken
   image, no draft note. Write the URL into the kit file and `docs/STATUS.md`.
