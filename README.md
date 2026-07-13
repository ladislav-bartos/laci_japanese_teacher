# Japanese Study Log — Repository Guide

Personal study log for JLPT N2 (target: December 2026) and long-term CEFR C1.
Daily material: Sou Matome N2 (Kanji, Vocabulary, Grammar, Reading, Listening — one day-unit each, weekdays only).

## Structure

```
japanese-study/
├── README.md              ← this file
├── plan/                  ← topics to cover, uploaded in advance: {topic}-w{n}.md
│                            (kanji-w1.md, vocabulary-w1.md, grammar-w1.md,
│                             reading-w1.md, listening-w1.md, ...)
├── logs/                  ← one file per study day: YYYY-MM-DD.md
│                            (items covered, drill sentences, my answers,
│                             grades, explanations, weak points, conversation notes)
├── diagnostics/           ← weekly N5–N3 legacy quizzes: YYYY-Wnn.md
├── anki/                  ← weekly TSV export of missed items for Anki import
├── reports/               ← weekly weakness reports and trends
└── specs/
    └── phase2.md          ← spec for the voice tutor app (below)
```

## Weekly workflow
0. Ahead of the week: commit that week's `plan/{topic}-w{n}.md` files (Kanji, Vocabulary, Grammar, Reading, Listening).
1. Weekdays: study that day's items from the current week's `plan/` files → text drill in the Claude Tutor Project → say "log it" → download the MD → commit to `logs/`.
2. Voice conversation (30 min) in Claude voice mode; optionally append a summary to that day's log.
3. Once a week: run the 10-sentence legacy diagnostic → commit to `diagnostics/`.
4. Once a week: paste the week's logs into the Tutor Project → receive the Anki TSV (`anki/`) and weakness report (`reports/`) → import TSV into Anki.

Committing from mobile: GitHub mobile app or github.com in the browser both allow uploading/creating files in a folder.

---

# Phase 2 Spec — Voice Tutor App

See [`specs/phase2.md`](specs/phase2.md). Build only after 2–3 weeks of consistent Phase 1 routine.
