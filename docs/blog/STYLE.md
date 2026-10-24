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
- One idea per heading. If it needs "；", the idea is the part before it, or the
  metaphor carries both halves (例："在吵鬧的教室找叫你的朋友：太吵會突然指錯，多叫幾聲就找得到").
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
   in `C:\Users\Aaron\Downloads`.
5. **Save** as `docs/blog/img/stepN_concept.jpg`, resized to 1600 px wide, JPEG
   quality 85 (about 120 KB). Leave the original in Downloads.
6. **Caption** under the image: what to notice, then `（AI 生成，Gemini）`.
7. **Record** the scene sentence in the commit message, so the picture can be made
   again.

Chapter 1 scene: "View from inside a home, looking out a window at a garden tree. A
small bird sings on a branch. A colorful heat-map glow is overlaid on the bird, like
a thermal camera image: red at the center, fading to yellow, green and blue. It shows
where the sound comes from. On the window sill sits the microphone board."
