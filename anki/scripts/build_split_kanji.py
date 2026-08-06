#!/usr/bin/env python3
"""Build a week-specific, Kanji-only Anki deck with one subdeck per day.

Splits the Kanji-section rows (tagged kanji::w{N}) out of the existing
anki/week{N}-v3-vocabulary.tsv into a standalone deck:

    Japanese N2 Kanji — Week {N}
    ├── Day 1
    ├── Day 2
    └── ...

Card format (Front/Back HTML, CSS, note type) is identical to the existing
"Japanese vocabulary" note type (specs/anki-note-type-vocabulary.md) — this
script reuses that exact model definition so cards look the same in review.

These are a deliberately INDEPENDENT copy of the source cards, not a move:
guids are salted (see SALT) so they don't collide with the notes already
living in "Japanese N2 Vocabulary", and studying one deck doesn't affect
scheduling in the other.

Usage (from repo root):
    .venv/bin/python anki/scripts/build_split_kanji.py <week_number>
    .venv/bin/python anki/scripts/build_split_kanji.py 1
"""
import genanki
import hashlib
import os
import re
import sys

MODEL_ID = 1074616827  # same as "Japanese vocabulary" in the main decks
MODEL_NAME = "Japanese vocabulary"
SALT = "split-kanji-v1"  # distinguishes these guids from the mainline deck's


def stable_id(name):
    h = hashlib.sha256(name.encode('utf-8')).hexdigest()
    return int(h[:9], 16) % 1_000_000_000 + 1_000_000_000


CSS = """
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
"""

QFMT = "{{Front}}"
AFMT = '{{FrontSide}}\n<hr id="answer">\n{{Back}}'


def make_model():
    return genanki.Model(
        MODEL_ID, MODEL_NAME,
        fields=[{"name": "Front"}, {"name": "Back"}],
        templates=[{"name": "Card 1", "qfmt": QFMT, "afmt": AFMT}],
        css=CSS,
    )


def parse_tsv_rows(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            assert len(parts) == 3, f"bad row in {path}: {line!r}"
            front, back, tags = parts
            rows.append((front, back, tags))
    return rows


def day_from_tags(tags, week):
    """Return the day number (int) for a kanji::w{week}d{N} tag, or None
    (e.g. kanji::w{week}dExtra) if it's a non-numbered bonus/extra section."""
    m = re.search(rf'kanji::w{week}d(\d+)\b', tags)
    if m:
        return int(m.group(1))
    if re.search(rf'kanji::w{week}dExtra\b', tags):
        return "Extra"
    return None


def build(week):
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../anki
    src_path = os.path.join(base, f"week{week}-v3-vocabulary.tsv")
    rows = parse_tsv_rows(src_path)

    kanji_rows = [(f, b, t) for f, b, t in rows if re.search(rf'\bkanji::w{week}\b', t)]
    if not kanji_rows:
        raise SystemExit(f"No kanji::w{week} rows found in {src_path}")

    by_day = {}
    for front, back, tags in kanji_rows:
        d = day_from_tags(tags, week)
        if d is None:
            raise SystemExit(f"Row has kanji::w{week} tag but no day sub-tag: tags={tags!r}")
        by_day.setdefault(d, []).append((front, back, tags))

    def day_sort_key(d):
        return (0, d) if isinstance(d, int) else (1, d)

    parent_name = f"Japanese N2 Kanji — Week {week}"
    model = make_model()
    decks = []
    out_lines = [
        "#separator:tab",
        "#html:true",
        "#columns:Front\tBack\tTags",
        f"# Week {week} (Sou Matome N2) — Japanese vocabulary: Kanji-only split deck, grouped by day",
    ]
    total = 0
    for d in sorted(by_day, key=day_sort_key):
        day_label = f"Day {d}" if isinstance(d, int) else d
        deck_name = f"{parent_name}::{day_label}"
        deck_id = stable_id(deck_name)
        deck = genanki.Deck(deck_id, deck_name)
        for front, back, tags in by_day[d]:
            guid = genanki.guid_for(front, back, SALT)
            note = genanki.Note(model=model, fields=[front, back], tags=tags.split(), guid=guid)
            deck.add_note(note)
            out_lines.append(f"{front}\t{back}\t{tags}")
            total += 1
        decks.append(deck)

    out_tsv = os.path.join(base, "split", f"week{week}-kanji.tsv")
    out_apkg = os.path.join(base, "split", f"week{week}-kanji.apkg")
    os.makedirs(os.path.dirname(out_tsv), exist_ok=True)
    with open(out_tsv, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines) + "\n")
    genanki.Package(decks).write_to_file(out_apkg)

    print(f"Week {week}: {total} kanji cards across {len(by_day)} day(s): "
          f"{ {d: len(v) for d, v in by_day.items()} }")
    print(f"Wrote {out_tsv}")
    print(f"Wrote {out_apkg} ({len(decks)} subdecks under \"{parent_name}\")")


if __name__ == "__main__":
    week = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    build(week)
