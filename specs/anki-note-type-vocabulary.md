# Anki Note Type: "Japanese vocabulary" — Finalized Spec

Status: **Finalized** (approved 2026-07-19). This is the settled spec for the "Type 1" card
family described in `specs/anki-card-styles.md` (word/kanji/phrase + example sentence). Unlike
that file (a draft comparing options), this document is the source of truth to regenerate the
deck/note type identically in the future — update it first if the design changes, then regenerate.

Covers: **Kanji, Vocabulary, and Reading** content types (a single word/kanji/phrase tested with
one example sentence). Does **not** cover Grammar, Listening minimal-pairs, keigo mappings,
casual-speech contractions, or idiomatic set-phrases — those are a different card family
("Type 2"), spec TBD.

## Anki object names

| Object | Name |
|---|---|
| Deck | `Japanese N2 Vocabulary` |
| Note type (model) | `Japanese vocabulary` |
| Card type (template) | `Card 1` |

## Stable IDs (for idempotent re-import — do not change once in use)

Generated deterministically from the names above via `sha256(name)[:9 hex chars] % 1e9 + 1e9`,
so any script reproducing this formula on the same name yields the same ID and re-importing
updates the existing deck/note-type in place instead of duplicating it.

- Deck ID (`Japanese N2 Vocabulary`): `1265466646`
- Model ID (`Japanese vocabulary`): `1074616827`

## Fields

Standard **Basic**-shaped note: `Front`, `Back` (2 fields). Tags are supplied separately via
Anki's tag mechanism, not as a field.

## Card template — Card 1

The template itself must **not** contain any custom HTML/wrapper divs — it just inserts the
field content verbatim. All layout HTML lives in the Front/Back field values (see below), not
the template.

**Front (qfmt):**
```
{{Front}}
```

**Back (afmt):**
```
{{FrontSide}}
<hr id="answer">
{{Back}}
```

## Styling (CSS)

```css
.card {
    font-family: 'Hiragino Kaku Gothic ProN','Hiragino Sans','Yu Gothic Medium','Yu Gothic','Noto Sans JP','Meiryo',sans-serif;
    text-align: center;
    color: #1f1f1f;
    background-color: #fafafa;
    font-size: 20px;
}

div {
    padding-bottom: 2vh;
}

.front-main {
    font-size: 30px;
}

hr#answer {
    max-width: 92vw;
    margin: 3vh auto;
    border: none;
    border-top: 1px solid #ccc;
}
```

Note: spacing between stacked divs comes from the CSS `div { padding-bottom: 2vh; }` rule, not
from empty spacer `<div style="height:...">` elements (those were used in the v2 prototype but
are dropped here — the field HTML below has no spacer divs).

## Field HTML structure

**Front field:**
```html
<div class="front-main">{WORD}</div><div class="front-example-sentence-1">{SENTENCE}</div>
```
- `{WORD}` — the kanji/word/phrase, no furigana.
- `{SENTENCE}` — one natural example sentence containing the word, no furigana.

**Back field:**
```html
<div class="back-main-reading">{WORD_READING}</div><div class="back-main-english">{WORD_MEANING_EN}</div><div class="back-example-sentence-1-reading">{SENTENCE_READING}</div><div class="back-example-sentence-1-english">{SENTENCE_TRANSLATION_EN}</div>
```
- `{WORD_READING}` — hiragana reading of `{WORD}` alone.
- `{WORD_MEANING_EN}` — English meaning of `{WORD}`.
- `{SENTENCE_READING}` — full hiragana reading of the entire example sentence (kanji → hiragana;
  katakana/Latin script/digits stay as-is).
- `{SENTENCE_TRANSLATION_EN}` — English translation of the example sentence.

**Why "-1" is in the class names**: the suffix reserves room for a future multi-example-sentence
layout (`front-example-sentence-2`, `back-example-sentence-2-reading`, etc.) without renaming
existing classes — added now so the convention doesn't need to change later if a card gets a
second example sentence.

## Example (real card from the deck)

Front:
```html
<div class="front-main">禁止</div><div class="front-example-sentence-1">関係者以外立ち入り禁止です。</div>
```

Back:
```html
<div class="back-main-reading">きんし</div><div class="back-main-english">Prohibition</div><div class="back-example-sentence-1-reading">かんけいしゃいがいたちいりきんしです。</div><div class="back-example-sentence-1-english">Entry is prohibited except for those concerned.</div>
```

## Tags

Same tag scheme as before (`kanji::w1 kanji::w1d1`, `vocabulary::w1 vocabulary::w1d3`,
`reading::w1 reading::w1d5`, etc.), **plus** a JLPT-level tag on every note: `jlpt::n2` for all
Week 1 content (Sou Matome N2 material). Example final tag set: `kanji::w1 kanji::w1d1 jlpt::n2`.

## TSV → apkg generation

- Source TSV: `anki/week{N}-v3-vocabulary.tsv` (3 columns: Front, Back, Tags — same
  `#separator:tab` / `#html:true` / `#columns:Front\tBack\tTags` header convention as prior
  weekly TSVs).
- Built with `genanki` (already installed in `.venv`) using the model/deck/IDs/CSS/templates
  above. No standalone generator script is checked into the repo yet — ask to have one added
  under `anki/` if this needs to run unattended/repeatedly.
