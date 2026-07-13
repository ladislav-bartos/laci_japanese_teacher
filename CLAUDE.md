# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A personal Japanese study log, not (yet) a software project. It tracks JLPT N2 preparation
(target: December 2026) and a longer-term CEFR C1 goal, using Sou Matome N2 materials
(Kanji, Vocabulary, Grammar, Reading, Listening).

The repo is currently in **Phase 1**: a manual, markdown-based logging workflow. There is no
application code yet — only `README.md` and an empty Python 3.14 venv (`.venv/`, no
dependencies installed). Don't assume build/lint/test tooling exists; there is none right now.

## Repository layout (per README; created incrementally as logs accumulate)

```
plan/         topics to cover, uploaded in advance: {topic}-w{n}.md
              (kanji-w1.md, vocabulary-w1.md, grammar-w1.md, reading-w1.md, listening-w1.md, ...)
logs/         one file per study day: YYYY-MM-DD.md
              (items covered, drill sentences, answers, grades, explanations, weak points, conversation notes)
diagnostics/  weekly N5-N3 legacy quizzes: YYYY-Wnn.md
anki/         weekly TSV export of missed items for Anki import
reports/      weekly weakness reports and trends
specs/        specs for future tooling, e.g. specs/phase2.md
```

When asked to create or edit study content, follow these file naming conventions and place
files in the matching directory.

## Weekly workflow (the thing this repo supports)

0. Ahead of the week: commit that week's `plan/{topic}-w{n}.md` files (Kanji, Vocabulary, Grammar, Reading, Listening).
1. Weekdays: study that day's items from the current week's `plan/` files → text drill in the Claude Tutor Project → "log it" → download the MD → commit to `logs/`.
2. Voice conversation (30 min) in Claude voice mode; optionally append a summary to that day's log.
3. Weekly: run the 10-sentence legacy diagnostic → commit to `diagnostics/`.
4. Weekly: paste the week's logs into the Tutor Project → receive Anki TSV (`anki/`) and weakness report (`reports/`) → import TSV into Anki.

Commits are frequently made from mobile (GitHub mobile app / github.com), so keep changes to
this repo simple, single-file, and mergeable.

## Git commit conventions

Do not add a `Co-Authored-By: Claude ...` trailer to commit messages in this repo.

## Phase 2 — planned voice tutor app (not started)

`specs/phase2.md` describes a future small web app that would replace the manual workflow above:
speak a drill sentence → speech-to-text → Claude API grades it → auto-commits results to `logs/`,
plus a free-talk conversation mode and Anki TSV generation. Key constraints from the spec:
- Prefer raw audio sent to a dedicated STT API (e.g. Google Cloud STT) over the browser Web
  Speech API, because the latter silently auto-corrects pronunciation and hides errors — the
  whole point of the app is to catch those errors.
- No user accounts/multi-user deployment, no custom SRS (Anki already handles spaced repetition).
- Success = daily drill is no slower than the manual version, zero manual copy-paste, and
  pronunciation errors are actually surfaced.

**Do not start implementing Phase 2 unless explicitly asked.** The README states it should only
be built after 2-3 weeks of consistent Phase 1 routine, so Phase 1 is very likely still in progress.
