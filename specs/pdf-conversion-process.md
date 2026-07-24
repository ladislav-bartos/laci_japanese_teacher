# PDF → plan/*.md Conversion Log

Reference notes on how source PDFs under `plan/source/` get turned into the study `plan/*.md`
files. Kept here (rather than in a one-off chat) so the method is reproducible for the remaining
weeks/subjects that still need filling in.

## Tools used

- **Read tool's built-in PDF support** — the same `Read` tool used for any file in this repo can
  open a `.pdf` directly and returns the page content as rendered images (not raw text
  extraction/OCR run separately). No external PDF library, script, or `pdftotext`-style CLI is
  involved.
- **Page-range limit** — the tool caps a single call at **20 pages**. PDFs longer than that
  return an error naming the actual page count, and must be read in two or more calls with a
  `pages: "start-end"` argument (e.g. `pages: "1-12"`, then `pages: "13-23"`).
- **No OCR/transcription tool beyond reading the images directly** — the page images are read
  visually (this is a multimodal model), and the Japanese text, furigana, tables, and margin
  annotations are transcribed by reading the page layout, not by a separate text-extraction step.
- **Write/Edit tools** — used to author or update the corresponding `plan/*.md` file once the PDF
  content has been read and organized.

## General method (repeatable steps)

1. **Diff the existing plan file against its source PDF** — check the plan `.md` file's size/
   content against the book. A file that's a small skeleton (headings + one-line scene summaries,
   no full scripts/choices, or a placeholder-looking Answer Key) is a sign the PDF hasn't been
   fully transcribed yet, as opposed to a file that already has full れんしゅう content.
2. **Get the PDF's page count** — call `Read` on the PDF with no `pages` argument first; if it's
   under 20 pages, it comes back in one call. If not, the error message reports the exact page
   count, which tells you how many follow-up calls (and what ranges) are needed.
2. **Read the PDF in ≤20-page chunks**, covering both:
   - the **exercise pages** (practice questions, printed answer choices, reference tables,
     margin vocab notes) — usually near the front of the chapter, and
   - the **別冊 solutions booklet** (答え・スクリプト) — usually appended at the back of the same
     PDF, containing the full dialogue/script text plus the correct answer and any (※) footnote
     glosses. The exercise pages alone are not enough — for listening in particular, the script
     text a learner would hear only exists in the solutions booklet, not on the exercise page.
3. **Cross-reference exercise-page choices with solution-page answers** by item number (1番,
   2番, 3番, …) — the printed multiple-choice options live on the exercise page; the correct
   answer number and full script live on the solution page days/pages later in the same PDF.
4. **Sanity-check numeric/logic answers independently before trusting the book's answer key**,
   especially for money/math items (e.g. adding up rent + deposit + agent fees, or postage
   weight bands) — this catches whether the source's stated answer is self-consistent, and also
   catches transcription mistakes made while reading.
5. **Preserve the book's own structure and register** when writing the `.md`: same section
   numbering/titles, tables reproduced as markdown tables, (※N) footnote glosses kept attached
   to the word they explain, and the "don't reveal the Answer Key before grading" instruction
   preserved at the top of the file for whoever (human or AI tutor) runs the drill.
6. **Diff any existing placeholder content against the freshly-read PDF answer key** — a
   previously-written skeleton file may contain guessed answers that don't match the book once
   the actual solutions booklet is read; treat the PDF as authoritative and correct any
   mismatches rather than assuming the skeleton was right.

## Applied: `plan/listening-w3.md` (2026-07-24)

- **Symptom:** `plan/listening-w3.md` was a 4KB skeleton — section headings, one-line Japanese
  parenthetical summaries of each scene (e.g. "（お母さんと子どもの会話：スリッパをそろえる）")
  instead of real スクリプト text, no printed 選択肢, and a bare Answer Key with just numbers and
  no scripts/explanations. Compared to `listening-w2.md` (41KB, full scripts + choices +
  explanations), this was clearly unfinished.
- **Source:** `plan/source/listening/listening-w3.pdf`, 23 pages total.
- **Read in two calls:** pages 1–12 (chapter intro + exercise pages for sections 1–5, i.e. book
  pages ~40–50) and pages 13–23 (the 別冊 解答・スクリプト booklet, book pages 22–33).
- **Content recovered from the exercise pages:** the four reference tables (場面/話し手/内容の例
  for sections 1–4), all printed 選択肢 for every れんしゅう item and for まとめ問題 問題I/II, and
  the 不在連絡票 (delivery notice) graphic used in section 3's 1番.
- **Content recovered from the solutions booklet:** full スクリプト dialogue for every item in
  sections 1–4 and all three parts of まとめ問題 (問題I/II/III — including 問題III, whose choices
  aren't printed on the exercise page at all since that question type is read aloud only), the
  correct answer number for each item, and every (※N) footnote gloss.
- **Correction found:** the old skeleton's Answer Key listed section 1's 3番 (マンションの支払い)
  as answer **3**. Reading the actual solution script and doing the math (家賃5万+管理費3千 +
  敷金1か月分5万 + 手数料1か月分5万 = 15万3千円) confirms the book's real answer is **2**, not 3 —
  the skeleton's answer was a guess made before the PDF had been read, and has been corrected.
  All other section answers in the old skeleton (sections 2–4) matched the book once verified.
- **Result:** `plan/listening-w3.md` rewritten in place, following the same structure as
  `listening-w2.md` (reference tables → れんしゅう with full scripts+choices → Answer Key with
  brief reasoning per item), keeping the original file's top-of-file "how to use this file" note
  and updating it to describe this chapter's specific section list and lack of 例をやってみよう
  worked examples (chapter 3 goes straight from reference table to practice, unlike chapter 2).
