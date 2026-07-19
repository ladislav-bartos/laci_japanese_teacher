# Anki Note Type: "Japanese grammar and usage" — Requirements (Draft)

Status: **Captured, not yet built.** This is the "Type 2" card family from
`specs/anki-card-styles.md` — everything that isn't a plain word+sentence card (that's
`specs/anki-note-type-vocabulary.md`). Edit this file directly to change the spec; nothing has
been generated from it yet, so there's no existing deck/TSV to keep in sync until we build it.

Covers **all Listening-section content** plus the **Grammar** section — five content sub-types,
all sharing a single Card Type/template (see "Why a single Card Type" below).

## Why a single Card Type

All five sub-types share the same visual structure (a `front-main` + one or two example
sentences; a back with a reading/meaning line and matching sentence reading/translation lines) —
the only differences are which CSS classes get used and how many example sentences are present,
and both of those already live in the Front/Back field *content* (same approach as the Vocabulary
note type), not in template logic. Since the template never needs to behave differently per
sub-type, there's no need for multiple Card Types with guard fields — a single shared template
renders every sub-type correctly, and a `type::*` tag on each note (see "Tags" below) does the
filtering/organizing job instead.

## Meaning field convention: `back-main-english` vs `back-main-english-explanation`

Two different class names are used for the "meaning" line on the back, depending on what kind of
meaning it actually is:

- **`back-main-english`** — a direct, literal English translation of the front-main content.
  Used only by **Sub-type 3** (word contrast), since "assert/claim ↔ business trip" is a
  straight word-for-word translation of 主張 and 出張, not a paraphrase.
- **`back-main-english-explanation`** — a functional explanation/paraphrase rather than a literal
  translation. Used by **Sub-types 1, 2, 4, and 5**, since what's being conveyed in each case
  isn't a dictionary meaning but a description of what the pattern/form *does*: a grammar
  pattern's function ("if I could..."), what a keigo form maps to in plain speech, a contraction
  rule, or an idiom's pragmatic nuance.

## Anki object names

| Object             | Name                           |
| ------------------ | ------------------------------ |
| Deck                | `Japanese N2 Grammar & Usage`  |
| Note type (model)   | `Japanese grammar and usage`   |
| Card Type           | `Card 1` (single, shared by all sub-types) |

## Card template — Card 1

Same approach as the Vocabulary note type: the template contains no custom HTML, it just inserts
the field content verbatim (all layout HTML lives in the Front/Back field values).

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

Same as the Vocabulary note type (`specs/anki-note-type-vocabulary.md`):

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

## Sub-type 1 — Grammar pattern + example sentence(s)

Content: the Grammar section's 24 patterns, plus Listening's giving/receiving・passive・causative
formulas and わけ／こと expressions (all pattern-shaped content, wherever it originated). Tag:
`type::grammar`.

Front:

```html
<div class="front-main">〜ものなら / もんなら</div><div class="front-example-sentence-1">帰れるものなら、今すぐ、国へ帰りたい。</div>
```

Back:

```html
<div class="back-main-reading">〜ものなら / もんなら</div><div class="back-main-english-explanation">if I could...</div><div class="back-example-sentence-1-reading">かえれるものなら、いますぐ、くにへかえりたい。</div><div class="back-example-sentence-1-english">If I could, I'd like to go back to my country right now.</div>
```

Notes:
- `back-main-reading` is included in case a grammar item contains kanji that needs a hiragana
  reading. If the pattern has no kanji, it's shown as-is (identical to `front-main`).
- Uses `back-main-english-explanation`, not `back-main-english` — see "Meaning field convention"
  above. A grammar pattern's meaning is a functional paraphrase ("if I could..."), not a literal
  word-for-word translation.
- One example sentence per card — a pattern with 2 book examples becomes 2 separate notes, not
  one note with 2 sentences (matches how the Grammar section was built in `week1-v2.tsv`).

## Sub-type 2 — Keigo / register mapping

Content: Listening Day 3's keigo terms (9 items). Tag: `type::keigo`.

Front:

```html
<div class="front-main">〜ものなら / もんなら</div><div class="front-example-sentence-1">お酒もタバコも召し上がらないんですか。</div><div class="front-example-sentence-2">お酒もタバコもやらないの。</div>
```

Back:

```html
<div class="back-main-reading">めす／めしあがる</div><div class="back-main-english-explanation">keigo for 着る・風邪をひく (wear/catch a cold) or 食べる・飲む・吸う (eat/drink/smoke)</div><div class="back-example-sentence-1-reading">おさけもタバコもめしあがらないんですか。</div><div class="back-example-sentence-1-english">Do you not drink alcohol or smoke at all?</div><div class="back-example-sentence-2-reading">おさけもたばこもやらないの。</div><div class="back-example-sentence-2-english">Do you not drink or smoke?</div>
```

Note: exactly 2 example sentences per card — sentence 1 formal/keigo register, sentence 2
informal/casual register (a different, natural-sounding casual equivalent, not the same sentence
minus politeness). Where the source material only had one, write a matching sentence in the
other register. Uses `back-main-english-explanation` — see "Meaning field convention" above.

## Sub-type 3 — Two similar words/pairs contrasted

Content: Listening Day 1's minimal pairs (7 items, e.g. 主張↔出張). Tag: `type::contrast`.

Front:

```html
<div class="front-main">主張 ↔ 出張</div><div class="front-example-sentence-1">彼は自分の意見を強く主張した。</div><div class="front-example-sentence-2">来週は東京へ出張に行きます。</div>
```

Back:

```html
<div class="back-main-reading">しゅちょう ↔ しゅっちょう</div><div class="back-main-english">assert/claim ↔ business trip</div><div class="back-example-sentence-1-reading">かれはじぶんのいけんをつよくしゅちょうした。</div><div class="back-example-sentence-1-english">He strongly asserted his opinion.</div><div class="back-example-sentence-2-reading">らいしゅうはとうきょうへしゅっちょうにいきます。</div><div class="back-example-sentence-2-english">I am going on a business trip to Tokyo next week.</div>
```

Note: exactly 2 example sentences per card — sentence 1 for the first word, sentence 2 for the
second word. When sentences are missing please write a matching one. Uses plain
`back-main-english` (not `-explanation`) — see "Meaning field convention" above; this is the one
sub-type where the back's meaning is a literal translation, not a paraphrase.

## Sub-type 4 — Casual-speech contraction mapping

Content: Listening Day 1's casual contractions (10 items, e.g. わかんない, 見てる, 置いとく). Tag:
`type::contraction`.

Front:

```html
<div class="front-main">わかんない</div><div class="front-example-sentence-1">何を言っているのか、全然わかんない。</div><div class="front-example-sentence-2">何を言っているのか、全然わからない。</div>
```

Back:

```html
<div class="back-main-reading">わからない</div><div class="back-main-english-explanation">casual contraction of ら・り・る・れ・に・の → ん</div><div class="back-example-sentence-1-reading">なにをいっているのか、ぜんぜんわかんない。</div><div class="back-example-sentence-1-english">I don't understand at all what you're saying.</div><div class="back-example-sentence-2-reading">なにをいっているのか、ぜんぜんわからない。</div><div class="back-example-sentence-2-english">I don't understand at all what you're saying.</div>
```

Note: exactly 2 example sentences per card — sentence 1 shows the sentence with the casual
contraction in it, sentence 2 is the *same* sentence with the contraction swapped out for its
correct/full written form (not a different example, not a formality change — just the one word
substituted). Where the source material only shows the contracted form, write sentence 2 by
substituting the full form into the same sentence. Uses `back-main-english-explanation` — see
"Meaning field convention" above; the back's meaning line explains the contraction rule (e.g.
"casual contraction of ら・り・る・れ・に・の → ん"), it isn't a translation of the word itself.

## Sub-type 5 — Fixed idiomatic/attitude set-phrases

Content: Listening Day 4's idiom/attitude words (どうせ, どうだか, そこをなんとか, また、そのうちに,
それはそれは, あいにく, 張り切る, ぎりぎりの線 — 8 items). Tag: `type::idiom`.

Front:

```html
<div class="front-main">どうせ</div><div class="front-example-sentence-1">どうせ最後まで読まないんだから、その本は買わなくていいよ。</div>
```

Back:

```html
<div class="back-main-reading">どうせ</div><div class="back-main-english-explanation">a sense of resignation/giving up ("it's no use anyway...")</div><div class="back-example-sentence-1-reading">どうせさいごまでよまないんだから、そのほんはかわなくていいよ。</div><div class="back-example-sentence-1-english">You're not going to read it to the end anyway, so you don't need to buy that book.</div>
```

Notes:
- `back-main-reading` shows the hiragana reading only if the idiom/phrase contains kanji (e.g.
  張り切る → はりきる). If it's already all-kana (e.g. どうせ, そこをなんとか), it's shown as-is,
  identical to `front-main`.
- Uses `back-main-english-explanation` — see "Meaning field convention" above. These are
  pragmatic/attitude expressions ("a sense of resignation..."), not literal translations.

**Resolved**: 落ち込む moves to the Vocabulary deck (`specs/anki-note-type-vocabulary.md`) as a
Type 1 card instead — it's a plain verb, not an idiom, so it doesn't belong here. Sub-type 5 is
therefore just the 8 idiom/attitude items.

## Tags

Same base scheme as the Vocabulary note type: existing tags (`grammar::w1 grammar::w1d1`,
`listening::w1 listening::w1d3`, etc.) plus `jlpt::n2` on every note — **plus** a sub-type tag so
the five content sub-types are filterable/browsable despite sharing one Card Type:

| Sub-type | Tag |
|---|---|
| 1 — Grammar pattern | `type::grammar` |
| 2 — Keigo / register mapping | `type::keigo` |
| 3 — Word contrast | `type::contrast` |
| 4 — Casual contraction | `type::contraction` |
| 5 — Idiom/attitude phrase | `type::idiom` |

Example final tag set: `grammar::w1 grammar::w1d1 jlpt::n2 type::grammar`.

## Item-to-subtype mapping counts (proposed, not yet built)

Sub-type 1 (grammar) = Grammar's 48 cards + Listening's 7 giving/receiving·passive·causative
items + 8 わけ／こと items = 63; Sub-type 2 (keigo) = 9; Sub-type 3 (contrast) = 7; Sub-type 4
(contraction) = 10; Sub-type 5 (idiom) = 8. **Total 97** (Grammar 48 + Listening 50 − 1 for
落ち込む, which moved to the Vocabulary deck).

## Missing example sentences (need writing before building)

- Sub-type 2's second (informal-register) sentence for all 9 keigo items.
- Sub-type 3's second example sentence (for the pair's second word) for all 7 minimal pairs (none
  existed in the source material — the v2 minimal-pair cards had no sentences at all).
