# Anki Content Gaps — Uncategorized/Skipped Source Material

Running log of source content found in `plan/*-w{N}.md` that did **not** end up as a card in
either deck — because it didn't cleanly fit any of the categories in
`specs/anki-tsv-generation-process.md` Step 1, or because it was structurally impossible to card
given the current text-only note types. Reviewed alongside that process doc (see its Step 1a) so
nothing found during a week's generation gets silently dropped.

Every entry must include: the exact source quote, why it wasn't carded, a concrete example (what
a card *would* look like, or why one can't be made at all), and a next step or explicit "none
identified." Don't log a vague description — quote the actual text, every time (Step 1a).

---

## Week 2

### 1. Synonym partners from the Listening "言い換えの例" list — RESOLVED 2026-07-19

**Source** (`listening-w2.md`, section 2 課題理解):
> 言い換えの例
> 確認する = チェックする
> 準備する = 用意する
> 注文する = 頼む
> 訂正する = 直す
> 処分する = 捨てる

Only the left-hand word of each pair was carded as Deck 1 vocabulary (no "synonym pair" sub-type
exists to card the *pairing* itself). The right-hand words were originally skipped on an
unverified assumption that they're common/already-known.

**Verified by grepping both decks' TSVs**: 捨てる was already in the Vocabulary deck (from Week 1
kanji, tag `kanji::w1 kanji::w1d1`):
```html
Front: <div class="front-main">捨てる</div><div class="front-example-sentence-1">ごみをここに捨てないでください。</div>
Back:  <div class="back-main-reading">すてる</div><div class="back-main-english">Throw away</div><div class="back-example-sentence-1-reading">ごみをここにすてないでください。</div><div class="back-example-sentence-1-english">Please do not throw trash here.</div>
```
The other four (チェックする, 用意する, 頼む, 直す) were **not** in either deck. Added as new Deck 1
vocabulary cards, e.g.:
```html
Front: <div class="front-main">頼む</div><div class="front-example-sentence-1">レストランでコーヒーを頼む。</div>
Back:  <div class="back-main-reading">たのむ</div><div class="back-main-english">to order/ask for (synonym of 注文する in a restaurant context)</div><div class="back-example-sentence-1-reading">レストランでコーヒーをたのむ。</div><div class="back-example-sentence-1-english">I order coffee at the restaurant.</div>
```
Tagged `listening::w2 listening::w2d2 jlpt::n2` (real origin, same as their pair partners already
in the deck). **Resolution**: `anki/week2-v3-vocabulary.tsv`/`.apkg` now have 461 cards (was 457).

### 2. 動物園の入園料 (zoo admission fee) comprehension/calculation exercise — PARTIALLY RESOLVED 2026-07-19

**Source** (`listening-w2.md`, section 2 課題理解, 1番, plus the Answer Key):
> 【スクリプト】男：大人3人、子ども2人。1人は65歳以上です。…（計算問題）
> 【問題】合計いくら払いますか？
>
> Answer key: 1番: 4 (詳細計算: 大人(1000円×2) + シニア(800円) + 小学生(500円×2) = 3800円)

The exercise *as a unit* correctly has no card — it's a spoken word problem with an arithmetic
answer, not a vocabulary/grammar/keigo/contrast/contraction/idiom item, and there's no sensible
front/back split for "do this calculation." That part stays unresolved by design, not by
oversight.

But the exercise still contains real, topic-relevant vocabulary worth extracting on its own,
separately from the exercise-as-a-whole: **入園料** (admission fee), **シニア** (senior/elderly
discount category), and **以上** (the "N and above" threshold word, from 65歳以上). Verified none
of the three existed in either deck; added as new Deck 1 vocabulary cards, e.g.:
```html
Front: <div class="front-main">入園料</div><div class="front-example-sentence-1">この動物園の入園料は大人1000円です。</div>
Back:  <div class="back-main-reading">にゅうえんりょう</div><div class="back-main-english">admission fee (to a park/zoo/garden)</div><div class="back-example-sentence-1-reading">このどうぶつえんのにゅうえんりょうはおとな1000えんです。</div><div class="back-example-sentence-1-english">This zoo's admission fee is ¥1000 for adults.</div>
```
Tagged `listening::w2 listening::w2d2 jlpt::n2`. (大人, 子ども, 小学生 were considered and skipped
— too basic for an N2-focused deck, not because they don't fit a category.)

### 3. Listening chapter's comprehension-strategy sections — PARTIALLY RESOLVED 2026-07-19

Two different flavors here, both from `listening-w2.md`:

**(a) Sections with zero real script text** — ポイント理解, 概要理解, 統合理解①② — remain
correctly uncarded. Confirmed again: their "script" lines are pure instructional description
(e.g. 「（男の人の不満についての会話）」), not dialogue, so there is genuinely nothing to extract
here. Nothing changed for this part.

**(b) 即時応答 — has real stimulus lines, and they contained genuinely useful material**:
> 1番 【スクリプト】男：あー！ 今日、早く行かないといけなかったんだ！どうしよう…。
> 2番 【スクリプト】男：この間、新宿のカラオケボックスで、ばったり中村先生に会ったよ。
> 3番 【スクリプト】男：駅前に置いてった自転車、なくなっちゃった。

The multiple-choice *answers* to these are still unrecoverable (only the answer-key option number
survives, not the option text — that part of the gap is unchanged). But the stimulus lines
themselves are real, natural Japanese worth extracting as their own items, carded with the book's
actual sentence as the example (translated as-is, not rewritten):
- **どうしよう** (Deck 1 vocab) — "what should I do!" panic exclamation, from 1番.
- **この間** (このあいだ) and **ばったり(会う)** (Deck 1 vocab, two separate cards sharing one
  example sentence) — "the other day" / "to run into by chance," from 2番.
- **置いてった** and **なくなっちゃった** (Deck 2, `type::contraction`, two cards sharing one
  example sentence) — casual contractions of 置いていった (ていった→てった) and なくなってしまった
  (てしまった→ちゃった), from 3番. Example card:
```html
Front: <div class="front-main">置いてった</div><div class="front-example-sentence-1">駅前に置いてった自転車、なくなっちゃった。</div><div class="front-example-sentence-2">駅前に置いていった自転車、なくなってしまった。</div>
Back:  <div class="back-main-reading">置いていった</div><div class="back-main-english-explanation">casual contraction of ていった → てった</div><div class="back-example-sentence-1-reading">えきまえにおいてったじてんしゃ、なくなっちゃった。</div><div class="back-example-sentence-1-english">"The bike I left in front of the station is gone."</div><div class="back-example-sentence-2-reading">えきまえにおいていったじてんしゃ、なくなってしまった。</div><div class="back-example-sentence-2-english">"The bike I left in front of the station is gone."</div>
```
These 2 contraction cards also happen to be Week 2's *only* `type::contraction` cards — Week 2's
Listening chapter otherwise has no casual-contraction teaching block at all (unlike Week 1).

**Resolution**: `anki/week2-v3-vocabulary.tsv`/`.apkg` grew from 461 → 467 cards (6 added: 入園料,
シニア, 以上, どうしよう, この間, ばったり(会う)); `anki/week2-v3-grammar-usage.tsv`/`.apkg` grew
from 35 → 37 cards (2 added: 置いてった, なくなっちゃった). The *exercise itself* (item 2) and the
*missing answer-choice text* (item 3b) remain open — those are genuinely uncardable, not missed
extractions.
