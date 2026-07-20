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

## Week 1 (retroactive completeness sweep, done 2026-07-19 after Week 2's gaps prompted it)

Week 1 predates Step 1a/1b existing at all, so this is a retroactive audit applying them now.
Method: for Kanji/Vocabulary, parsed every source bullet and diffed word-for-word against the
deck (found 0 gaps — both sections were already 100% complete, the only "missing" words were the
2 intentional Kanji/Vocabulary dedups from Step 2, 家賃 and 銀行口座). For Reading/Grammar/
Listening, grepped for every `（注）`-style book-annotated term, checked Day 7/"Bonus" sections
specifically (since Week 2's kanji Day 7 showed these can hide new content), and reviewed the
Listening "まとめ問題" summary test line-by-line against what the main teaching tables already
covered. All 8 confirmed gaps below have been added as new cards.

**1. `〜させていただきます`** (`grammar-w1.md`, "Bonus: 敬語 — 自分について話す①", after Day 7):
> ❶ 自己紹介します → させていただきます
> **【問い】** すみませんが、風邪気味なので休ませて（a. お願いします / b. 申し上げます / c. いただきます）。

A genuine grammar pattern (causative-stem + いただきます, "I will humbly do X") distinct from the
already-carded 申し上げる — this bonus section's *other* item (❷ お願い申し上げます) was already
covered verbatim as 申し上げる's example sentence, which is likely why the whole section read as
"already covered" on first pass. Added to Deck 2 as `type::grammar`, tag `grammar::w1d7`.

**2–5. Reading Day 7's book-annotated vocabulary** (`reading-w1.md`, 7日目, hotel-listing and
dry-cleaning passages — Day 7 has no separate "Key vocabulary" block like Days 1–6, so these were
never pulled out):
> （注）連泊＝同じところに続けて泊まること／バイキング＝好きなだけ皿に取って食べる食事スタイル／素泊まり＝食事なしで泊まること
> （注）衣替え＝洋服を季節に合わせて替えること

**連泊, バイキング, 素泊まり, 衣替え** — all four are explicitly annotated by the book itself
(the same signal Days 1–6 use for "this is vocabulary worth learning"), so this was a parsing
gap, not a judgment call: Day 7 sections were treated as "review only, skip" across the board,
which was right for the *questions* but wrong for annotated vocabulary sitting in the passage
text. Added to Deck 1, tag `reading::w1d7` (new tag — Week 1's reading section previously only
went to d6).

**6. もれなく** (`reading-w1.md`, 2日目 dry-cleaning DM... actually the sale-DM passage):
> （注）もれなく＝without exception

Same category as #2–5 (a book-annotated word), but from Day 2, not Day 7 — missed for the same
reason (the day's separate "Key vocabulary" Q&A block doesn't include every annotated word in the
passage itself, only the block's own bullets). Added to Deck 1, tag `reading::w1d2`.

**7. ご存知** (`listening-w1.md`, section 5 まとめ問題, 問題II 3番#2):
> あの方をご存知ですか。 → 1 あの人を知っていますか ／ 2 あの人をどう思いますか

The main keigo teaching table (section 3, already fully carded as 9 `type::keigo` cards) only
covers 存じる／存じ上げる, the *humble* "I know" form. ご存知, the *respectful* "you/they know"
counterpart, only appears in the summary test, not the teaching table itself — easy to miss
because it reads as "testing already-covered content" unless you check the direction (humble vs.
respectful) specifically. Added to Deck 2 as `type::keigo`, tag `listening::w1d3` (grouped with
the other keigo cards it pairs with conceptually, even though it physically appears in section 5).

**8. やっぱり** (`listening-w1.md`, section 5 まとめ問題, 問題II 5番#2):
> 女：何、その服の組み合わせ。変だよ。／男：やっぱり？

Same pattern as #7 — an attitude/discourse word (same category as the already-carded どうせ/
どうだか/そこをなんとか) that only shows up in the summary test, not the section-4 "気持ちを表す
表現" teaching list it conceptually belongs to. Added to Deck 2 as `type::idiom`, tag
`listening::w1d4`.

**Checked and confirmed NOT gaps** (logged so they aren't re-flagged in a future re-sweep):
- **くんない** (「窓、閉めといてくんない？」, summary test 1番#1) — looks like a new contraction
  (くれない→くんない) but is actually the *same* already-documented rule (ら・り・る・れ・に・の
  → ん, which explicitly includes れ→ん) applied to a different verb. No new card needed.
  同様に 見てらんない／直したげる／太りたくなけりゃ in the same table are all the already-carded
  てらんない grammar pattern or already-carded てあげる／なければ contractions — the whole 1番
  block turned out to be review, this one line just needed the extra check to confirm it.
- **足りるわけないよ** (summary test 4番#3) uses わけない in its はずがない sense ("there's no way
  it's enough"), while the existing わけない card's example uses its 簡単だ sense ("this is
  easy") — the *same word* genuinely carries two different colloquial meanings depending on
  context. Not a missing-card gap (adding a second わけない card with a conflicting explanation
  would be confusing, not helpful) — flagged here as a nuance worth remembering when reviewing
  that card, not something to act on structurally.

**Resolution**: `anki/week1-v3-vocabulary.tsv`/`.apkg` grew from 400 → 405 cards.
`anki/week1-v3-grammar-usage.tsv`/`.apkg` grew from 97 → 100 cards.

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

---

## Week 3

Unlike Weeks 1–2, Steps 1a/1b were applied *during* generation this time, not retroactively — so
this section records what was checked and found, rather than gaps discovered after the fact.

**1. Reading's "ポイント" lists turned out to be grammar patterns, not vocabulary** — a new
structural pattern worth watching for in future weeks. `reading-w3.md` Day 1 and Day 6 each open
with a bulleted "ポイント：文末表現に注意！" list:
> ～一方だ／～つつある／～に至る／～次第だ／～始末だ (Day 1)
> ～とは限らない／～にすぎない／～に違いない／～かねない／～わけにはいかない (Day 6)

These aren't reading-comprehension vocabulary (Deck 1) — they're literally grammar patterns
(sentence-ending forms), so per Step 1 they belong in Deck 2 as `type::grammar`, not Deck 1. Two
of the ten (一方だ, わけにはいかない) were already covered by `grammar-w3.md`'s own Day 2/Day 6
patterns — skipped as duplicates. The other **8** (つつある, に至る, 次第だ, 始末だ, とは限らない,
にすぎない, に違いない, かねない) were genuinely new, and the book gives no example sentences for
them here (unlike `grammar-w3.md`'s patterns) — fresh sentences were written for all 8. Added to
`anki/week3-v3-grammar-usage.tsv` as `type::grammar`, tagged `reading::w3d1`/`reading::w3d6` (real
origin, not `grammar::`).

**2. `reading-w3.md`'s actual passages (Days 1, 2, 3, 4, 5, 6) were scanned for extractable
vocabulary, per Step 1b** — none of these days have a "Key vocabulary" list at all this week
(unlike Weeks 1–2), only a short strategy tip and then straight into the passage. Extracted 12
words verified not already in either deck: 点滴, 人ごと, 患者 (Day 1); モーニングコール,
ケアレスミス, ペーパーテスト, ベビーカー (Day 2, from the "和製英語に注意" wasei-eigo point —
パソコン/リモコン/コンビニ/マナー from the same list were skipped as too basic for an N2 deck,
consistent with the bar set in Week 2); 強盗 (Day 3); だらだら, 老後 (Day 4); 分煙 (Day 5);
でこぼこ (Day 6). Added to `anki/week3-v3-vocabulary.tsv`, tagged `reading::w3d{N}` by the day
each was found in.

**3. `listening-w3.md` has zero extractable content — confirmed, not assumed.** Every one of its
13 `【スクリプト】` entries is a parenthetical description (e.g. `（お母さんと子どもの会話：
スリッパをそろえる）`), never real quoted dialogue — unlike Week 2, where 即時応答 at least had
real (if incomplete) stimulus lines. Verified by grepping the whole file for `スクリプト` and
confirming every instance is wrapped in `（...）`. No teaching tables (no keigo/contraction/
minimal-pair lists) exist in this chapter either. **Zero cards from Listening this week** — this
is the expected, fully-checked result, not a skipped section.

**4. Kanji's "Extra Topic" section** (between Day 6 and Day 7, introducing new kanji 昨/翌/軒/毒/
涙/笑 plus symbolic pairs like 未読/送信済み) was caught proactively this time, unlike Week 2's
kanji Day 7 (which needed a later gap-fix). Tagged `kanji::w3dExtra` since the source doesn't
number it as a day. 18 cards.

**5. Both Day 7 "実戦問題" exercises (kanji and vocabulary) verified as pure review** — every
distinctive word/reading tested was grepped against the assembled deck (checking inflected forms
against their dictionary-form base entries, e.g. かついで → かつぐ, つまづいて → つまずく) and
confirmed already covered. No new cards needed from either Day 7.

**Resolution**: no retroactive fixes needed — `anki/week3-v3-vocabulary.tsv`/`.apkg` (536 cards)
and `anki/week3-v3-grammar-usage.tsv`/`.apkg` (55 cards) already include everything found above
in their initial build.
