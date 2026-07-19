# Anki Content Gaps — Uncategorized/Skipped Source Material

Running log of source content found in `plan/*-w{N}.md` that did **not** end up as a card in
either deck — because it didn't cleanly fit any of the categories in
`specs/anki-tsv-generation-process.md` Step 1, or because it was structurally impossible to card
given the current text-only note types. Reviewed alongside that process doc (see its Step 1a) so
nothing found during a week's generation gets silently dropped.

Each entry should say: what the content is, why it wasn't carded, and a next step if one exists.

---

## Week 2

**Synonym partners from the Listening "言い換えの例" (paraphrase-equivalent) list** (Day 2,
`listening-w2.md` section 2 課題理解). The source list pairs 5 words: 確認する＝チェックする,
準備する＝用意する, 注文する＝頼む, 訂正する＝直す, 処分する＝捨てる. Only the first word of each
pair was carded (as plain Deck 1 vocabulary — `type::grammar`/`contrast` didn't fit a same-meaning
synonym pair, and there's no "synonym pair" sub-type). The second word of each pair
(チェックする, 用意する, 頼む, 直す, 捨てる) was skipped on the assumption it's common/already-known
vocabulary (捨てる was already carded in Week 1 kanji), but that assumption wasn't actually
verified against the existing decks. **Next step**: check whether these 5 words already exist
somewhere in either deck; if not, add them as ordinary Deck 1 vocabulary cards, or design a
proper "synonym pair" sub-type if this pattern recurs in later weeks.

**動物園の入園料 (zoo admission fee) comprehension example** (Day 2, `listening-w2.md` section 2
課題理解, 1番). This is a concrete listening-comprehension exercise with real numbers in the
answer key (大人 [adult] ¥1000 × 2, シニア [senior] ¥800, 小学生 [elementary schooler] ¥500 × 2 =
¥3800) — but it's a math/comprehension exercise, not a vocabulary item, grammar pattern, keigo
mapping, contrast pair, contraction, or idiom. No current sub-type fits. **Skipped entirely** —
no card was created. **Next step**: none identified yet; would need a new sub-type (e.g. a
"comprehension/calculation exercise" card) if this pattern is common enough across future weeks
to be worth carding.

**The rest of the Listening chapter's comprehension-strategy sections** (即時応答 items 1–3,
ポイント理解 items 1–2, 概要理解 item 1, 統合理解①② items 1–3, まとめ問題) contain no actual
dialogue script text in the source markdown — only Japanese descriptions of what the audio would
contain (e.g. "（男の人の不満についての会話）"), not the dialogue itself. This isn't a
classification gap (nothing here would map to vocabulary/grammar/keigo/contrast/contraction/idiom
even if the text existed) — it's a structural limitation: none of the current note types support
audio, and there's no real text to build a text-based card from anyway. Documented here for
completeness rather than as an actionable gap. Ties to the "Note on audio" section in
`specs/anki-card-styles.md`, which already flags audio-based cards as a possible future
enhancement, not something built into the current pipeline.
