# Process: Generating Weekly Anki TSV/apkg Files from `plan/*-w{N}.md`

This is the step-by-step playbook for turning a week's source material
(`plan/kanji-w{N}.md`, `vocabulary-w{N}.md`, `grammar-w{N}.md`, `reading-w{N}.md`,
`listening-w{N}.md`) into the two Anki decks, repeatable for Week 2 onward. It assumes the note
types are already finalized — see `specs/anki-note-type-vocabulary.md` (Deck 1) and
`specs/anki-note-type-grammar-and-usage.md` (Deck 2) for the exact HTML/CSS/field spec; this doc
only covers *classification* (which item goes where) and the *build pipeline* (source → TSV →
apkg). See also `specs/anki-content-gaps.md` for source content that didn't fit anywhere — check
it before starting a week and update it (Step 1a) as you go.

## Two decks, one pipeline

| | Deck 1 | Deck 2 |
|---|---|---|
| Anki deck name | `Japanese N2 Vocabulary` | `Japanese N2 Grammar & Usage` |
| Note type | `Japanese vocabulary` | `Japanese grammar and usage` |
| Output file | `anki/week{N}-v3-vocabulary.tsv` | `anki/week{N}-v3-grammar-usage.tsv` |
| Spec | `specs/anki-note-type-vocabulary.md` | `specs/anki-note-type-grammar-and-usage.md` |

## Step 1 — Classify every item from the five source sections

**Kanji section** → always Deck 1. One card per kanji/compound word listed.

**Vocabulary section** → always Deck 1. One card per vocabulary entry.

**Reading section** → always Deck 1. One card per glossary term extracted from the reading
passages/notices.

**Grammar section** → always Deck 2, sub-type `grammar`. **Two cards per pattern** (one per book
example sentence) — not one card with both examples embedded. If a pattern has more than 2 book
examples, still one card per example.

**Listening section** → the only section that splits across *both* decks. Go item by item and
ask:

1. **Is it a genuinely plain word/phrase** that happens to be introduced inside a Listening
   passage or example dialogue (e.g. a footnote vocab word like 落ち込む)? → **Deck 1**
   (Vocabulary), tagged with its *actual* origin (`listening::w1 listening::w1dN`), not
   relabeled as if it came from the Vocabulary section. This is a real edge case that happened
   in Week 1 — don't assume everything under `listening::` belongs in Deck 2.
2. **Is it two similar-sounding words being discriminated** (a pronunciation/reading-confusion
   pair, e.g. 主張↔出張)? → Deck 2, sub-type `contrast`. In the Sou Matome book these usually
   live under the listening chapter's "発音" (pronunciation) teaching block, tagged
   `listening::`, even though they're about sound discrimination, not comprehension — check the
   actual tag in the source TSV/data, not the book's section title.
3. **Is it a casual-speech contraction mapping** (a spoken-form shortening → its dictionary
   form, e.g. わかんない → わからない)? → Deck 2, sub-type `contraction`.
4. **Is it a keigo (polite/humble) form mapped to its plain-form meaning** (e.g.
   召す／召し上がる)? → Deck 2, sub-type `keigo`.
5. **Is it a reusable grammatical construction** — giving/receiving formulas, passive/causative
   formulas, わけ／こと-type set expressions, or anything that's a *pattern* rather than a
   single lexical item? → Deck 2, sub-type `grammar` (grouped with the Grammar-section cards).
6. **Otherwise, is it a fixed conversational/attitude set-phrase** with a pragmatic nuance rather
   than a compositional meaning (e.g. どうせ, そこをなんとか, 張り切る)? → Deck 2, sub-type
   `idiom`.

If none of 2–6 clearly fit, default to rule 1 (Deck 1, plain vocabulary) — that was the correct
call for 落ち込む in Week 1.

## Step 1a — Log anything that doesn't fit, instead of silently dropping it

Not everything in the source material will fit Step 1's rules or be cardable at all (e.g. a
listening-comprehension exercise built around a calculation, or a chapter with no real dialogue
script to source a sentence from). When that happens:
- Don't force it into the nearest-sounding category just to have somewhere to put it.
- Don't silently skip it either — record it in `specs/anki-content-gaps.md` (one section per
  week) with **the exact source quote** (not a paraphrase/description of it), why it didn't fit,
  a concrete example of what a card *would* look like if one existed (or an explanation of why
  none can be made), and a next step if one exists (a new sub-type, or "no action identified").
  A gap entry without the source quote isn't done — go back and add it.
- **Never skip something because it's "probably already covered" or "probably common enough to
  not need a card" without actually checking.** Grep the existing `anki/week*-v3-*.tsv` files for
  the word/pattern first. This is not optional — Week 2 had exactly this mistake: 5 words were
  assumed redundant, but a grep afterward showed 4 of the 5 weren't in either deck at all, and
  they had to be added retroactively. Do the grep *before* deciding to skip, not after.

Check `specs/anki-content-gaps.md` before starting a new week too — a gap from an earlier week
might turn out to be relevant again (e.g. if a recurring pattern makes a new sub-type worth
designing).

## Step 1b — Completeness sweep before calling a week done

Don't rely on noticing gaps opportunistically while classifying (Step 1) — that's exactly how the
Week 2 gaps were almost missed. Before considering a week's TSVs final, go back through **every
bullet, list item, and table row** in each of the five `plan/*-w{N}.md` files (including
teaching-block asides, footnotes, and answer-key-only content — not just the headline vocab
lists) and confirm each one is in exactly one of these buckets:
- Turned into a card (in either TSV).
- Deliberately excluded per an established rule (Day 7 pure-review stub, an exact Kanji/Vocabulary
  duplicate per Step 2, a synonym/alternate already covered elsewhere *and verified* per Step 1a).
- Recorded in `specs/anki-content-gaps.md`.

If something doesn't land cleanly in one of those three, it's been missed — go back to Step 1 or
1a for it. This sweep is what catches content sitting in a section you didn't expect to have
cardable material (e.g. a stray real example buried inside an otherwise-empty listening-strategy
section, or a footnote vocab word in a dialogue transcript).

**"The whole thing doesn't fit" is not the same as "there's nothing inside worth extracting."** A
listening exercise, dialogue, or passage can correctly have no card for itself as a unit (e.g. a
word-problem-style comprehension exercise, or a script fragment whose punchline/answer isn't in
the source) while still containing individual words or natural phrases worth their own Deck 1 or
Deck 2 cards. When logging something in `specs/anki-content-gaps.md` as uncardable-as-a-whole,
still read through it specifically looking for extractable vocabulary or genuinely useful,
naturally-occurring phrases — using the source's own sentence as the card's example (translated
as-is) rather than inventing a new one. Only mark the *whole item* as fully closed once that
extraction pass has actually been done, not just assumed unnecessary.

## Step 2 — Deduplicate Kanji vs. Vocabulary

Some words appear in both the Kanji section (as a compound built from that day's target kanji)
and the Vocabulary section (as a standalone vocab entry) — Week 1 had 2 such collisions (家賃,
銀行口座). Compare word lists between the two sections; where an exact match exists, **keep it in
Kanji, drop the Vocabulary copy**.

## Step 3 — Source the example sentence(s)

Priority order, same as used for Week 1:
1. Check `plan/{section}-w{N}.md`'s own "Practice (練習)" / "Practice Questions" section for that
   day — if the word/pattern already appears in a full sentence there (even as an a/b
   multiple-choice item), resolve it to the correct choice and reuse it.
2. Check that week's `drills/YYYY-MM-DD-w{N}d{D}.md` and matching `-answers.md` files — these
   contain additional vetted sentences from the actual daily drills.
3. Otherwise, write a new natural sentence yourself: JLPT N2-appropriate register, roughly one
   clause to one short compound sentence, matching the tone of the source textbook. Verify it
   actually uses the word in the sense given by its listed meaning before reusing a sourced
   sentence — don't reuse a sentence where the "correct" resolved answer turns out to be a
   *different* word than the one being carded.

Grammar-section patterns already have 2 book example sentences each — reuse those directly, no
new sentences needed for that part.

Keigo cards (Deck 2) need a **second, informal-register** sentence conveying the same situation —
write one if the source only shows the formal line.

Contrast cards (Deck 2) need **one sentence per word in the pair** — write both if the source
material (typically just a bare word-pair list) has neither.

Contraction cards (Deck 2) need a **second sentence that's the *same* sentence** with the
contraction swapped for its full written form — not a new example, just the one substitution.

## Step 4 — Produce hiragana readings

- Convert every kanji in the example sentence to hiragana; katakana, Latin script, and Arabic
  numerals stay as-is (normal furigana convention).
- For a word/phrase's own reading (`back-main-reading` / `back-main-english`'s reading
  counterpart): give the **full** phonetic reading of the entire term, not just the kanji
  portion. Week 1 had ~60 vocabulary items where the original source data's reading only covered
  part of a multi-word phrase (e.g. 紙おむつ → reading given as just "かみ") — always reconstruct
  the complete reading, checking that every kana substring already present in the word appears
  verbatim in the reading too.
- For Grammar/Deck-2 "pattern" cards specifically: if the pattern contains no kanji (most don't
  — patterns like 〜げ, 〜わけだ, 〜ことはない are already all kana/symbols), `back-main-reading`
  is just the pattern repeated as-is. Only compute a real hiragana reading when the pattern label
  actually contains kanji (e.g. 〜気味 → 〜ぎみ; N(を)抜きにして → Nを ぬきにして).

## Step 5 — Format as HTML per the note-type spec

Use the exact field/class structure from the relevant note-type spec doc — do not improvise new
class names. Deck 1 is always `front-main` + `front-example-sentence-1` /
`back-main-reading` + `back-main-english` + `back-example-sentence-1-reading` +
`back-example-sentence-1-english`. Deck 2 varies by sub-type (1 or 2 example sentences,
`back-main-english` vs `back-main-english-explanation` — see "Meaning field convention" in
`specs/anki-note-type-grammar-and-usage.md` for which sub-types use which).

## Step 6 — Tags

Every card gets: `{section}::w{N} {section}::w{N}d{D} jlpt::n{level}` (JLPT level matches the
textbook level for that week's material — N2 for Sou Matome N2 weeks). Deck 2 cards additionally
get `type::{subtype}` (`grammar` / `keigo` / `contrast` / `contraction` / `idiom`).

`{section}` reflects the item's *actual origin* section (`kanji` / `vocabulary` / `reading` /
`grammar` / `listening`), regardless of which deck it ends up in — e.g. 落ち込む keeps
`listening::w1 listening::w1d2` even though it's filed in the Vocabulary deck.

## Step 7 — Write the TSV

3 tab-separated columns (`Front`, `Back`, `Tags`), with the standard header:
```
#separator:tab
#html:true
#columns:Front	Back	Tags
# Week {N} (Sou Matome N2) — {note type name}: {short content description}
```
One row per card (Grammar-section patterns and any 2-sentence-per-item sub-types still produce
one row per *card*, not per source item).

Before considering a TSV done, validate:
- Every row has exactly 3 tab-separated fields.
- Every row's Front/Back have balanced `<div>`/`</div>` tags.
- Every row's tags include the expected `jlpt::n2` (and `type::*` for Deck 2).
- Deck 2 sub-type counts match what was planned in Step 1 (e.g. Week 1: grammar 63, keigo 9,
  contrast 7, contraction 10, idiom 8 = 97).
- For Deck 1, spot-check that no word/reading pair got truncated by a parsing step (Week 1 had a
  bug where a combined `word (reading1) / word2 (reading2)`-style source field got parsed as if
  it were a single `word (reading)` pair, silently dropping half the content — always sanity
  check any row whose Front field contains multiple parenthesized readings or a `/` separator).
- For Deck 1, `front-main` must **never** append the word's reading in parentheses (e.g.
  `振込 (ふりこみ)`, `頼る (たよる)`) — the spec (`anki-note-type-vocabulary.md`) already says
  `{WORD}` has no furigana, and the reading already lives in `back-main-reading`; putting it in
  `front-main` too just gives the answer away on the question side. Weeks 1 and 3 both had this
  leak (4 words total, found retroactively 2026-07-29). Grep every row for
  `front-main">[^<]*(` and manually clear each hit: legitimate hits are grammar/word-formation
  notation (`(を)`, `(の)`, `(な)`, `(色)`, conjugation asides like `(いらっしゃいま)`) or
  non-kanji abbreviations (`1DK (ワンディーケー)`); a bare `kanji (hiragana-reading-of-that-kanji)`
  pair is always the bug — delete the parenthetical.
- For Deck 1, confirm every example sentence actually uses the word's kanji form when
  `front-main` has one, instead of silently falling back to its kana reading (e.g. `父に大声で
  どなられた` instead of `父に大声で怒鳴られた` for 怒鳴る). This defeats the kanji-recognition
  point of the card. Check: does every kanji character in `front-main` (ignoring parenthetical/
  slash-alternative notation) appear somewhere in `front-example-sentence-1`? If none of them do,
  the sentence was probably written in kana by mistake — fix it to use the kanji, matching
  conjugation/okurigana as needed. 5 cards across Weeks 1 and 3 had this bug (found retroactively
  2026-07-29).
- `specs/anki-content-gaps.md` has an entry for anything found during Step 1/1a that didn't make
  it into either TSV, for this week specifically.

## Step 8 — Generate the .apkg with genanki

Both note types use **stable, deterministic** deck/model IDs so re-running the generator for a
new week adds cards to the *same* existing Anki deck/note-type instead of creating a duplicate:

```python
import hashlib
def stable_id(name):
    h = hashlib.sha256(name.encode('utf-8')).hexdigest()
    return int(h[:9], 16) % 1_000_000_000 + 1_000_000_000
```

Current IDs (do not regenerate — reuse these exact values for every future week):

| Object | Name | ID |
|---|---|---|
| Deck 1 | `Japanese N2 Vocabulary` | `1265466646` |
| Model 1 | `Japanese vocabulary` | `1074616827` |
| Deck 2 | `Japanese N2 Grammar & Usage` | `1226860726` |
| Model 2 | `Japanese grammar and usage` | `1742781826` |

Build script shape (see the CSS/template in each note-type spec doc): create the `genanki.Model`
with fields `[Front, Back]`, a single `Card 1` template (`{{Front}}` / `{{FrontSide}}<hr
id="answer">{{Back}}`), the note type's CSS; create the `genanki.Deck` with the stable deck ID and
name; read the week's TSV, skip header/comment lines, and add one `genanki.Note` per row with
`fields=[front, back]` and `tags=tags.split()`; write the package to
`anki/week{N}-v3-{vocabulary|grammar-usage}.apkg`.

### Step 8a — Preserve note GUIDs when regenerating an existing week's `.apkg`

**This matters every time a TSV that already has a committed `.apkg` gets edited** (a typo fix, a
content correction, adding a few new rows) — not just for brand-new weeks. If you don't do this,
re-importing the regenerated `.apkg` resets the user's review history/scheduling on every card
whose field content changed, and the user has to re-study cards they'd already learned.

**Why this happens:** `genanki.Note` computes a note's `guid` (the identity Anki uses to match
notes on import) as a hash of the note's own field content, *unless* you pass `guid=` explicitly.
Anki's `Front`/`Back` field content is exactly what these TSV edits change — so any uncorrected
regeneration silently mints a new identity for every edited row, even though it's meant to be "the
same card, fixed."

**Fix: before regenerating, pull each row's *existing* guid out of the currently-committed
`.apkg`** (a `.apkg` is a zip containing a `collection.anki2` SQLite file with a `notes` table of
`(guid, flds, tags, ...)`; `flds` is `Front + "\x1f" + Back`) and pass it back in explicitly, so
the note's identity survives the edit:

```python
import sqlite3, zipfile, tempfile, os

def load_existing_guids(apkg_path):
    """(Front, Back) -> guid, read from the currently-committed apkg."""
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(apkg_path) as z:
            z.extract('collection.anki2', tmp)
        con = sqlite3.connect(os.path.join(tmp, 'collection.anki2'))
        rows = con.execute("select guid, flds from notes").fetchall()
        con.close()
    return {tuple(flds.split('\x1f')): guid for guid, flds in rows}

guid_map = load_existing_guids(f"anki/week{N}-v3-{deck}.apkg")  # BEFORE overwriting it
# ... when building notes:
key = (front, back)
note = genanki.Note(model=model, fields=[front, back], tags=tags.split(),
                     guid=guid_map.get(key))  # None → genanki falls back to its default hash
```

Match on exact `(Front, Back)` content — every unchanged row will hit, and every row whose content
you just fixed *won't*, which is expected (that row's identity does change, once, at the moment of
the fix — there's no way around that if the field content itself is what was wrong). New rows
(added vocabulary/patterns) naturally have no entry in `guid_map` and get a fresh default guid,
which is correct since they have no prior review history to preserve.

**After regenerating, verify no existing guid was lost** — the set of guids in the old `.apkg`
should be a subset of the guids in the new one:
```bash
diff <(sqlite3 old/collection.anki2 "select guid from notes" | sort) \
     <(sqlite3 new/collection.anki2 "select guid from notes" | sort)
```
Only additions (new rows) should show up in the diff; any *removed* guid means an existing row
failed to match (usually because its content was accidentally changed too) and needs
investigation before shipping.

Applied 2026-07-29: `anki/week3-v3-grammar-usage.apkg` grew from 55 → 59 notes (added the missing
keigo cards — see `specs/anki-content-gaps.md` item 6); all 55 pre-existing guids were preserved.

Weeks 1–3 were built ad hoc from throwaway scripts. Starting with Week 4, the build is a checked-in
script (`anki/scripts/build_week4.py`) holding the week's cards as structured Python data (`V(...)`
calls for Deck 1, `G(...)` calls for Deck 2) plus the TSV/apkg-writing and validation logic
described in Step 7 and this step. A future week can copy this file's shape rather than starting
from scratch — the GUID-preservation logic above still needs to be wired in explicitly if
regenerating an existing week's `.apkg` (the Week 4 script didn't need it, since Week 4 had no
prior `.apkg` to preserve GUIDs from).

## Known edge cases (learned from Week 1 — check for these every week)

- Kanji/Vocabulary word overlap (Step 2) — always check, even though Week 1 only had 2.
- Minimal-pair/contrast items are tagged `listening::`, not `reading::`, even though they're
  about sound/reading discrimination — don't assume from the book's section title.
- Plain vocabulary incidentally introduced in a Listening dialogue belongs in Deck 1, not Deck 2
  (Step 1, rule 1) — the exception, not "everything under listening:: is Deck 2."
- Multi-part Front fields (e.g. `1DK (ワンディーケー) / 2LDK (ニーエルディーケー)`) can get
  silently truncated by naive `word (reading)` regex parsing — verify anything with more than one
  parenthesis or a `/` separator survived intact.
- Partial word readings in older source data (reading only covers the kanji portion of a
  multi-word phrase) — always reconstruct the full reading (Step 4).
- **Day 7 sections are "review only, skip" for the *questions*, but Reading's Day 7 passages
  still contain book-annotated vocabulary (`（注）word＝meaning`) that has nowhere else to live**
  — Days 1–6 pull this into a separate "Key vocabulary" block, but Day 7 doesn't have one, so the
  same `（注）` annotations sitting directly in the Day 7 passage text get silently skipped if you
  only pull from "Key vocabulary" blocks. Grep every `plan/*-w{N}.md` file for `（注）` regardless
  of which day it's in, not just Days 1–6.
- **A section that's mostly review can still contain genuinely new content buried in the summary
  test, not the teaching table** — Week 1's Listening "まとめ問題" (summary test) tested mostly
  already-covered patterns, but 2 items (ご存知, やっぱり) only ever appear there, not in the
  actual teaching tables for keigo/attitude-words. Skimming a review section and confirming "yes,
  this pattern is covered" isn't the same as checking every individual word/line in it.
- **Reading's "ポイント" bullet lists are sometimes grammar patterns, not vocabulary** — Week 3's
  `reading-w{N}.md` opens some days with a "ポイント：文末表現に注意！" list of sentence-ending
  forms (e.g. ～つつある, ～に至る) rather than a word-meaning "Key vocabulary" list. These belong
  in Deck 2 as `type::grammar` (check for duplicates against that week's own `grammar-w{N}.md`
  patterns first), not Deck 1 — don't assume everything under Reading is a vocabulary word just
  because the section is Reading.
- **Not every week's Reading section has a separate "Key vocabulary" block at all** — Week 3's
  doesn't (unlike Weeks 1–2); each day just has a short strategy tip and then the passage. When
  that happens, the extractable vocabulary is *only* in the passage text itself (Step 1b) — there
  is no list to lean on, so the passage-by-passage scan isn't optional, it's the only way in.
- **Some weeks' `listening-w{N}.md` (or `kanji-w{N}.md` Day 7, etc.) genuinely have zero
  extractable content, and that's a fine, checked outcome** — Week 3's Listening chapter has no
  real dialogue text anywhere (confirmed by grepping every `スクリプト` line), so it correctly
  contributes 0 cards. Don't force content to appear where a proper check shows there's none —
  the goal is a verified answer either way, not a non-zero card count.
