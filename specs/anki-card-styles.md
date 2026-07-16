# Anki Card Styles — Review Draft

This is a comparison of candidate Anki card styles for the future generic Japanese-study Anki
skill (Kanji, Vocabulary, Grammar, Reading, Listening/Conversation). Nothing here is final —
review each style's example, note which ones you like/dislike per content type, and that
feedback becomes the actual skill's card-format rules.

Examples below reuse real content from `plan/conversation-topics/11-home-daily-life.md` and
`anki/week1.tsv` so the comparison is grounded in material you already know.

**How to give feedback:** for each content type, say which style (A/B/C/...) you want as the
default, or mix-and-match (e.g. "Kanji: Style B, but Vocabulary: Style A").

---

## Decision so far (from review of this draft)

- **Prefer cloze styles (B/C) over the isolated Style A** across content types — confirmed for
  Kanji and Vocabulary by rebuilding `anki/topic11-home-daily-life.tsv` as cloze cards (both the
  no-hint and meaning-hint variant per item, so every kanji/vocab entry now produces 2 cards
  instead of 1).
- **Whenever a card's front shows a Japanese sentence (any cloze style), the Back/Back Extra
  must include the full sentence's hiragana reading, not just the English translation.**
  Format used: `{reading} — {meaning} (JLPT)<br>Sentence reading: {hiragana}<br>Translation:
  {English}`. Katakana loanwords and any Latin-script text (e.g. brand names) stay as-is in the
  reading line — only kanji gets converted to hiragana, matching normal furigana convention.
- **JLPT tags apply to Reading and Listening cards too**, not just Kanji/Vocabulary — carry this
  into the skill so all five content types are taggable/filterable by level.
- Grammar-pattern vocab entries (e.g. "〜だから〜なんだよ") get a **multi-blank cloze** — every
  blank in the sentence uses the same `{{c1::...}}` tag so they reveal together as one card,
  rather than splitting into separate c1/c2 cards.
- **Deck structure**: conversation-topic decks go under a top-level Anki deck named
  `Japanese Conversation`, as `Japanese Conversation::Topic N - {name}` (e.g.
  `Japanese Conversation::Topic 11 - Home & Daily Life`) — kept separate from the `Japanese N2`
  deck used for the weekly Sou Matome material (`anki/week*.apkg`).

---

## Note-type reminder

Everything below is either a **Basic** card (plain Front/Back, what `anki/week*.tsv` already
uses) or a **Cloze** card (a sentence with a blanked-out piece you must recall). Cloze cards
need a different Anki note type on import — Anki will ask you to pick "Cloze" instead of
"Basic" for those files, and the TSV needs a `Text` + `Back Extra` column pair instead of
Front/Back. This doc flags which style is which so you know what you're picking.

---

## 1. Kanji

### Style A — Isolated word + example (current convention, extended with a sentence)
Basic card. What `anki/week1.tsv` already does, plus the example-sentence addition from the
topic-11 deck.

| Front | Back |
|---|---|
| 起 | お(きる)、お(こす) — wake up / wake someone (N5) *(kanji: 起)*<br>Example: 起きて！朝だよ。 — Wake up! It's morning. |

Pros: simple, consistent with existing decks, fast to review.
Cons: tests the kanji in isolation — you can get the meaning right without being able to read
it in a sentence you haven't memorized.

### Style B — Cloze: recall the reading, kanji stays visible
Cloze card. The kanji/word stays on screen; you have to produce the *reading* before flipping.

| Text | Back Extra |
|---|---|
| 早く{{c1::起きて}}、幼稚園に遅れるよ。 | おきて — from 起きる (to wake up), N5. Get up quickly, you'll be late for kindergarten. |

Pros: forces you to actually read kanji in running text, which is the real N2 skill (reading
passages, signage, not flashcards). Directly targets "can I read this" rather than "do I
recognize this."
Cons: slightly slower to author (needs a real sentence per card, not just a word+reading pair).

### Style C — Cloze: recall the word itself, meaning as the hint
Cloze card. The whole word is hidden; the hint is the English meaning, so you're producing
kanji + reading together from context.

| Text | Back Extra |
|---|---|
| 早く{{c1::起きて::wake up}}、幼稚園に遅れるよ。 | 起きて (おきて) — Get up quickly, you'll be late for kindergarten. |

Pros: hardest/most complete test — production of the word from meaning + context.
Cons: can feel frustrating if you're not ready for production-level recall yet; probably better
suited to words you've already seen a few times via Style A/B.

---

## 2. Vocabulary

### Style A — Isolated word + example (current convention, extended)
Basic card, same shape as the topic-11 deck already committed.

| Front | Back |
|---|---|
| 片付ける | かたづける — to clear/tidy up (N4)<br>Example: 食べ終わったら、お皿を片付けようね。 — Once you're done, let's clear the plates. |

### Style B — Cloze in a real sentence
Cloze card, same mechanism as Kanji Style B.

| Text | Back Extra |
|---|---|
| 食べ終わったら、お皿を{{c1::片付けよう}}ね。 | かたづけよう — from 片付ける (to clear/tidy up), N4. Once you're done, let's clear the plates. |

### Style C — Production (reversed): English prompt, Japanese answer
Basic card, reversed direction — tests active recall (useful for speaking prep, not just
reading).

| Front | Back |
|---|---|
| "to clear/tidy up" — say it in Japanese | 片付ける (かたづける), N4<br>Example: 食べ終わったら、お皿を片付けようね。 |

Pros: closer to what you actually need for the voice-conversation drills (producing the word,
not just recognizing it).
Cons: doubles card count if added alongside Style A instead of replacing it; harder, so more
early "fail" reviews while you're building the vocabulary.

---

## 3. Grammar

### Style A — Current convention (already close to best-practice)
Basic card. This is what `anki/week1.tsv` grammar rows already do — no change needed if you
like it as-is.

| Front | Back |
|---|---|
| 〜げ (seems / looks like) | Appears / gives the impression of (a feeling or state). Equivalent to 〜そう(な). N3.<br>**Connection:** A + げ / na + げ / Vたい(stem) + げ<br>**Ex:** あの人はさびしげな目をしている。(＝さびしそうな) — That person has a lonely look in his eye.<br>彼は何か言いたげだった。(＝言いたそう) — He looked like he wanted to say something. |

### Style B — Cloze: produce the grammar pattern in context
Cloze card. Arguably the single highest-value addition for grammar — you have to supply the
correct pattern in a real sentence, not just recognize its definition.

| Text | Back Extra |
|---|---|
| 彼は何か言い{{c1::たげ}}だった。 | 〜げ (N3) — looks like/seems. Equivalent to 〜そう(な). He looked like he wanted to say something. |

### Style C — Contrast cloze: same sentence, near-synonym as the distractor
Cloze card that explicitly targets the "which near-synonym pattern fits here" failure mode
(the actual thing that trips up N2 grammar sections), by noting the contrast in Back Extra.

| Text | Back Extra |
|---|---|
| 彼は何か言い{{c1::たげ}}だった。 | 〜げ, not 〜そう — げ leans more literary/descriptive, そう is the default spoken equivalent. Both mean "looked like." |

Pros: directly trains the discrimination skill N2 grammar questions actually test.
Cons: needs the pattern to have a genuine near-synonym worth contrasting — not every grammar
point has one, so this would be used selectively, not as a blanket replacement for Style A/B.

---

## 4. Reading

### Style A — Word + source sentence (recommended baseline)
Basic card. Anchors the word to the exact sentence it came from in the passage, instead of an
isolated definition.

| Front | Back |
|---|---|
| 有効期限 | ゆうこうきげん — the date/time until which something is valid (N2)<br>Source: 本券の有効期限は発行日より30日間です。 — This coupon is valid for 30 days from the date of issue. |

### Style B — Cloze within the actual passage sentence
Cloze card, same mechanism as above, but the passage sentence itself is the front instead of
being tucked into the back.

| Text | Back Extra |
|---|---|
| 本券の{{c1::有効期限}}は発行日より30日間です。 | ゆうこうきげん — the date/time until which something is valid (N2). This coupon is valid for 30 days from the date of issue. |

### Style C — Whole-sentence comprehension card
Basic card, different purpose: not vocabulary recall, but "can you parse this whole sentence."
Useful for the harder/longer N2 reading sentences where the struggle is parsing structure, not
a single word.

| Front | Back |
|---|---|
| 本券の有効期限は発行日より30日間です。 | This coupon is valid for 30 days from the date of issue.<br>(有効期限 = valid-until date, 発行日 = issue date) |

---

## 5. Listening / Conversation

### Style A — Minimal-pair discrimination (current convention)
Basic card. What `anki/week1.tsv` listening rows already do — unchanged, still useful for pitch
/ small-tsu / long-vowel discrimination drills.

| Front | Back |
|---|---|
| しゅちょう（主張）↔ しゅっちょう（出張） | 主張 = assert/claim, 出張 = business trip — small っ changes the meaning |

### Style B — Set-phrase + example exchange
Basic card, for conversational set phrases (the kind that show up in the topic docs), rather
than sound-discrimination drills.

| Front | Back |
|---|---|
| 行ってきます | I'm leaving (and coming back), N5<br>A: 行ってきます！ — I'm off!<br>B: 行ってらっしゃい、気をつけてね。 — Take care, see you later. |

### Style C — Cloze conversational response (production-oriented)
Cloze card, but the "blank" is an entire response line, not a word — you have to produce a
natural next line in the conversation before flipping. This is the closest card style to your
actual voice-conversation practice.

| Text | Back Extra |
|---|---|
| A: 今日はどうだった？<br>B: {{c1::…あなたの答え…}} | Sample answer: 楽しかったよ、でもちょっと疲れた。 — It was fun, but a bit tiring. N4. (Any reasonable answer to "how was your day" works — this card is about producing *a* natural response, not matching this exact line.) |

Pros: trains production and conversational reflexes directly, not just recognition.
Cons: doesn't have a single "correct" answer, so it grades more like a self-assessed
speaking-practice card than a normal recall card — could feel odd in a deck otherwise scored
pass/fail on exact recall.

### Note on audio
None of the styles above include actual audio clips — everything is text-only. Real listening
practice benefits from an audio prompt (e.g. TTS-generated), but that's a bigger addition (needs
an audio-generation step in the pipeline) and is flagged here as a possible future enhancement,
not something to build into the first version of the skill.

---

## Cross-cutting additions worth considering

- **JLPT tags everywhere**: every style above tags JLPT level in the Back/Back Extra text — as
  agreed, this should also become an actual Anki tag (e.g. `jlpt::n3`) on Reading/Listening
  cards, matching what Kanji/Vocabulary already do, so you can filter/study by level across all
  five content types.
- **Production (reversed) direction**: Vocabulary Style C and the general "reversed card" idea
  could apply to any content type, not just vocabulary — worth deciding once, as a global
  on/off, rather than per content type.
- **Sentence mining**: several styles above (Kanji B/C, Vocabulary B, Reading B, Grammar B/C)
  are all instances of the same underlying technique — cloze-deleting a real sentence instead
  of testing an isolated fact. If you like any one of them, you'll probably like the others,
  since it's the same mechanism applied to different content types.
