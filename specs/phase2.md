# Phase 2 Spec — Voice Tutor App

**Build only after 2–3 weeks of consistent Phase 1 routine.** Estimated effort: 2–4 evenings with Claude Code.

## Goal
A small personal web app that replaces the manual drill + logging workflow:
speak → be graded → everything auto-committed to this repo.

## Core features
1. **Sentence drills:** app calls the Claude API to generate original mixed drill sentences from the day's Sou Matome items (typed or photographed — Claude API accepts images). Generated sentences must be **similar to but not identical to** the source book's example/practice sentences — same grammar/vocab/kanji points, different wording — so the drill actually tests recall instead of memorized book sentences (Phase 1 issue, 2026-07-13: text-drill questions were reused verbatim from the book).
2. **Speech input:** capture microphone audio of me reading the sentence aloud. Prefer sending **raw audio to a speech-to-text API** (e.g., Google Cloud STT — fits my GCP background) configured to minimize auto-correction, because browser Web Speech API silently fixes pronunciation mistakes and hides errors.
3. **Grading:** Claude API compares my transcription/answers to the target, grades reading / comprehension / production, explains misses.
4. **Conversation agent:** free-talk mode — my speech → STT → Claude (tutor persona, today's topics) → text-to-speech reply. Full conversation logged. Should support **pre-planning conversation subtopics**, not just a general theme: e.g. theme "self-introduction" (自己紹介) should let me specify subtopics in advance such as family (siblings, their ages, where everyone lives), education/studies (what and where I studied, where I lived before), etc., so sessions cover a planned checklist rather than whatever comes up.
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
