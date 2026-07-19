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

### 2. 動物園の入園料 (zoo admission fee) comprehension/calculation exercise — OPEN

**Source** (`listening-w2.md`, section 2 課題理解, 1番, plus the Answer Key):
> 【スクリプト】男：大人3人、子ども2人。1人は65歳以上です。…（計算問題）
> 【問題】合計いくら払いますか？
>
> Answer key: 1番: 4 (詳細計算: 大人(1000円×2) + シニア(800円) + 小学生(500円×2) = 3800円)

This is real, complete content (unlike gap #3 below) — a spoken word problem plus its worked
answer. But it doesn't fit any existing sub-type: it's not a vocabulary item, not a grammar
pattern, not keigo/contrast/contraction/idiom — it's a comprehension exercise built around doing
arithmetic while listening. There's no meaningful "front/back" flashcard split for a word problem
(the "answer" is a calculation, not a reading+meaning+translation), so this can't be shoehorned
into either current note type. **No card exists for this.**

**Next step**: none identified yet. Only worth acting on if this pattern (word-problem-style
listening comprehension) turns out to be common across future weeks — at that point it would need
its own new sub-type/note type designed specifically for it, not a retrofit of Deck 1 or 2.

### 3. Listening chapter's comprehension-strategy sections — OPEN (documented, not actionable)

Two different flavors here, both from `listening-w2.md`:

**(a) Sections with zero real script text** — ポイント理解, 概要理解, 統合理解①②:
> 【スクリプト】（男の人の不満についての会話）
> 【問題】男の人が一番気に入らないと言っているのは何？

The "script" is a *description* of what the audio contains, not the dialogue itself — there is
no Japanese sentence here to put on a card front. Nothing to extract.

**(b) 即時応答 — has a real stimulus line but no answer choices**:
> 【スクリプト】男：あー！ 今日、早く行かないといけなかったんだ！どうしよう…。
> 【問題】(3つの選択肢から選ぶ)
>
> Answer key: 1番: 3

Here the spoken line itself *is* real text (「あー！今日、早く行かないといけなかったんだ！
どうしよう…。」) — but the exercise is "pick the natural reply from 3 options," and the actual
text of those 3 options isn't reproduced in the source file, only the answer key's option number
(3). Without the option text, there's no way to know or reconstruct what the "correct response"
actually says, so this can't be carded either, even though it's closer to being real content than
(a).

Neither (a) nor (b) is a classification problem — even if the missing text existed, it wouldn't
map to vocabulary/grammar/keigo/contrast/contraction/idiom anyway (this would need something like
the "Card Type C — Cloze conversational response" idea floated in `specs/anki-card-styles.md`,
which was never built). This is a structural gap: no current note type handles
audio-comprehension-strategy drilling, and the source markdown doesn't contain enough text to
build one manually even if it did. **No action identified.**
