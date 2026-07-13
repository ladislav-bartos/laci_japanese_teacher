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

# Phase 2 Spec — Voice Tutor App (`specs/phase2.md`)

**Build only after 2–3 weeks of consistent Phase 1 routine.** Estimated effort: 2–4 evenings with Claude Code.

## Goal
A small personal web app that replaces the manual drill + logging workflow:
speak → be graded → everything auto-committed to this repo.

## Core features
1. **Sentence drills:** app calls the Claude API to generate original mixed drill sentences from the day's Sou Matome items (typed or photographed — Claude API accepts images).
2. **Speech input:** capture microphone audio of me reading the sentence aloud. Prefer sending **raw audio to a speech-to-text API** (e.g., Google Cloud STT — fits my GCP background) configured to minimize auto-correction, because browser Web Speech API silently fixes pronunciation mistakes and hides errors.
3. **Grading:** Claude API compares my transcription/answers to the target, grades reading / comprehension / production, explains misses.
4. **Conversation agent:** free-talk mode — my speech → STT → Claude (tutor persona, today's topics) → text-to-speech reply. Full conversation logged.
5. **Auto-logging:** every task, answer, grade, and explanation auto-committed to `logs/` as markdown (GitHub API, personal access token).
6. **Anki generation:** button to generate the weekly TSV from logged misses into `anki/`.
7. **Weak-points tracking:** structured JSON alongside the MD logs so trends can be computed automatically.

## Non-goals (keep it simple)
- No user accounts, no deployment for others — local or single-user hosting is fine.
- No custom SRS — Anki already does spaced repetition.

## Success criteria
- Daily drill takes no longer than the manual Phase 1 version.
- Zero manual copy-paste to the repo.
- Pronunciation errors that dictation used to hide are now caught.
