#!/usr/bin/env python3
"""Query the local Hansard corpus. Built around the audit's actual loop.

The Kanon audit works by recall-then-verify: the model remembers a quote, then
has to establish whether it is real. That loop has three outcomes, and this
tool is shaped to serve all three rather than just the first:

    VERIFIED   the remembered string is in Hansard verbatim -> cite it
    NEAR MISS  something very close is in Hansard -> you were misremembering
               *this*; the tool hands back the real wording to cite instead
    NOT FOUND  nothing resembles it -> stop repairing, go find a different
               quote with `search`

The near-miss path is the one that was impossible before: without a corpus,
a half-remembered quote could only be confirmed or abandoned, never corrected.

    python search.py verify "the quote as remembered" [--speaker "Hanson"]
    python search.py search "immigration multicultural" [--speaker X] [--chamber senate]
    python search.py who "Pauline Hanson"
    python search.py speech uk.org.publicwhip/lords/2026-08-20.3.3
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path

import duckdb
from rapidfuzz import fuzz

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "hansard.duckdb"

SMART = str.maketrans({
    "‘": "'", "’": "'", "‛": "'", "ʼ": "'", "´": "'", "`": "'",
    "“": '"', "”": '"', "„": '"',
    "‐": "-", "‑": "-", "‒": "-", "–": "-", "—": "-",
    "―": "-", "−": "-", " ": " ",
})
WS = re.compile(r"\s+")
STOP = set("""a an and are as at be by for from has have he her his i in is it its of on
or that the their they this to was were will with you your we our not but""".split())

# Classification bands, calibrated against Hanson's Senate record (see below).
#
# partial_ratio scores the best-matching *window* of the candidate, so it is
# blind to candidate length: the 8-character paragraph "system !" scores 87%
# against any query containing the word "system". Without the length guard a
# pure fabrication scored 87% and would have been waved through as a near
# miss -- the exact failure this gate exists to prevent.
#
# With the guard, measured separation on real data is wide and clean:
#   genuine near misses   86-87%   (Hanson restating her own 1996 line)
#   unrelated paragraphs  <=58%
# 75 sits in the gap with room on both sides.
NEAR_FLOOR = 75
MIN_CAND_RATIO = 0.6  # candidate must be >=60% of the query's length to score


def norm(text):
    """Normalise for comparison. Must mirror index.py's NORM_SQL."""
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text).translate(SMART)
    return WS.sub(" ", text).strip().lower()


PUNCT = re.compile(r"[^\w\s]")


def norm_words(text):
    """Normalise down to words alone, discarding all punctuation.

    What matters is whether the words are the ones actually spoken. Hansard's
    own transcription decisions -- a comma after a date, an em dash where the
    audit wrote a comma, a serial comma, a hyphen in "working-class" -- are
    not misquotation, and flagging them buries the real failures under noise.
    Word-level identity is the test; punctuation is reported, not failed.
    """
    return WS.sub(" ", PUNCT.sub(" ", norm(text))).strip()


def keywords(text, limit=12):
    """Distinctive content words, for BM25 candidate retrieval."""
    words = re.findall(r"[a-z']{3,}", norm(text))
    seen, out = set(), []
    for w in words:
        if w in STOP or w in seen:
            continue
        seen.add(w)
        out.append(w)
    return out[:limit]


def connect():
    if not DB_PATH.exists():
        sys.exit("hansard.duckdb not found -- run parse.py then index.py first")
    con = duckdb.connect(str(DB_PATH), read_only=True)
    con.execute("INSTALL fts; LOAD fts;")
    return con


def quoted_span(candidate_norm, query_norm):
    """True if the matched region sits inside quotation marks in the source.

    Hansard is full of members quoting each other. A verbatim search for one
    politician's words will happily land on a *different* politician quoting
    them -- Sarah Hanson-Young reciting Pauline Hanson's lines in order to
    attack them scores 92% on Hanson's own phrasing. Citing that hit would
    attribute the quote to the wrong speaker while looking fully verified,
    which is worse than not finding it at all.
    """
    # Hansard sets block quotations off with a leading ellipsis rather than
    # quote marks, so a paragraph opening "… Islam is a disease" is someone
    # reciting another member's words, not their own sentence.
    if candidate_norm.lstrip().startswith(("…", "...")):
        return True
    try:
        a = fuzz.partial_ratio_alignment(query_norm, candidate_norm)
    except Exception:  # noqa: BLE001 - alignment is best-effort
        return False
    if a is None:
        return False
    before = candidate_norm[:a.dest_start]
    after = candidate_norm[a.dest_end:]
    return before.count('"') % 2 == 1 and '"' in after


def cite(row):
    """One citation-complete line: everything a footnote needs."""
    date, speaker, chamber, major, minor, url = row
    house = "Senate" if chamber == "senate" else "House of Representatives"
    topic = " / ".join(x for x in (major, minor) if x)
    return (f"  -- {speaker}, {house}, Hansard, {date}"
            + (f"\n     {topic}" if topic else "")
            + f"\n     {url}")


def bm25_candidates(con, terms, speaker=None, chamber=None, limit=60):
    """Top-N BM25 hits, optionally narrowed to one speaker or chamber."""
    if not terms:
        return []
    where, params = [], [" ".join(terms)]
    if speaker:
        where.append("lower(speakername) LIKE ?")
        params.append(f"%{speaker.lower()}%")
    if chamber:
        where.append("chamber = ?")
        params.append(chamber)
    clause = (" AND " + " AND ".join(where)) if where else ""
    return con.execute(f"""
        SELECT text, text_norm, sitting_date, speakername, chamber,
               major_heading, minor_heading, url, speech_id, para_no, score
        FROM (
            SELECT *, fts_main_para_search.match_bm25(pid, ?) AS score
            FROM para_search
        ) WHERE score IS NOT NULL{clause}
        ORDER BY score DESC LIMIT {limit}
    """, params).fetchall()


def cmd_verify(args):
    con = connect()
    q = norm(args.quote)
    if len(q) < 12:
        sys.exit("quote too short to verify meaningfully")

    # 1. Exact: is the remembered string in Hansard verbatim?
    params = [f"%{q}%"]
    clause = ""
    if args.speaker:
        clause = " AND lower(speakername) LIKE ?"
        params.append(f"%{args.speaker.lower()}%")
    exact = con.execute(f"""
        SELECT text, sitting_date, speakername, chamber,
               major_heading, minor_heading, url, speech_id
        FROM para_search WHERE text_norm LIKE ?{clause} LIMIT 5
    """, params).fetchall()

    if exact:
        print(f"VERIFIED  ({len(exact)} occurrence{'s' if len(exact) > 1 else ''})\n")
        for r in exact:
            print(f'  "{r[0][:300]}{"..." if len(r[0]) > 300 else ""}"')
            print(cite((r[1], r[2], r[3], r[4], r[5], r[6])))
            print(f"     speech_id: {r[7]}\n")
        return

    # 2. Near miss: retrieve candidates, then score by fuzzy overlap.
    cands = bm25_candidates(con, keywords(args.quote), args.speaker, args.chamber)

    # A remembered quote may span paragraph breaks, in which case no single
    # paragraph is long enough to match it. Offer the joined speech as an
    # additional candidate wherever the retrieved paragraphs allow.
    by_speech = {}
    for c in cands:
        by_speech.setdefault(c[8], []).append(c)
    for parts in by_speech.values():
        if len(parts) > 1:
            parts.sort(key=lambda c: c[9])
            joined = " ".join(p[1] for p in parts)
            merged = list(parts[0])
            merged[0] = " ".join(p[0] for p in parts)
            merged[1] = joined
            cands.append(tuple(merged))

    floor = len(q) * MIN_CAND_RATIO
    scored = sorted(
        ((fuzz.partial_ratio(q, c[1]), c) for c in cands if len(c[1]) >= floor),
        key=lambda x: -x[0],
    )[:args.limit]

    if scored and scored[0][0] >= NEAR_FLOOR:
        print(f"NEAR MISS  -- not verbatim, but Hansard has this. "
              f"Best match {scored[0][0]:.0f}% similar.")
        print("Cite the real wording below, not the remembered version.")
        if not args.speaker:
            print("WARNING: no --speaker given. Members quote each other "
                  "constantly in Hansard;\n         check the speaker on every "
                  "hit before citing it.")
        print()
        for score, c in scored:
            if score < NEAR_FLOOR:
                break
            flag = ""
            if quoted_span(c[1], q):
                flag = ("\n     !! INSIDE QUOTATION MARKS in "
                        f"{c[3]}'s speech -- this is a\n"
                        "        quotation, of someone else or of themselves "
                        "on an earlier date.\n"
                        "        Cite the original occasion, not this one.")
            print(f"  [{score:.0f}%] \"{c[0][:300]}{'...' if len(c[0]) > 300 else ''}\"")
            print(cite((c[2], c[3], c[4], c[5], c[6], c[7])) + flag)
            print(f"     speech_id: {c[8]}\n")
        return

    print("NOT FOUND  -- no verbatim match and nothing close enough to be a "
          "misremembering.")
    print("Do not cite this. Use `search` to find a different quote.\n")
    if scored:
        print(f"Closest thing in the corpus (only {scored[0][0]:.0f}% similar, "
              "almost certainly unrelated):")
        c = scored[0][1]
        print(f'  "{c[0][:200]}..."')
        print(cite((c[2], c[3], c[4], c[5], c[6], c[7])))


def cmd_search(args):
    con = connect()
    rows = bm25_candidates(con, keywords(args.terms, 20), args.speaker,
                           args.chamber, args.limit)
    if args.date_from or args.date_to:
        lo = args.date_from or "1900-01-01"
        hi = args.date_to or "2100-01-01"
        rows = [r for r in rows if lo <= str(r[2]) <= hi]
    if not rows:
        print("No matches.")
        return
    print(f"{len(rows)} match{'es' if len(rows) > 1 else ''}\n")
    for r in rows:
        print(f'  "{r[0][:320]}{"..." if len(r[0]) > 320 else ""}"')
        print(cite((r[2], r[3], r[4], r[5], r[6], r[7])))
        print(f"     speech_id: {r[8]}  para {r[9]}  bm25 {r[10]:.1f}\n")


def cmd_who(args):
    con = connect()
    rows = con.execute("""
        SELECT person_name, house, party, division, fromdate, todate
        FROM members WHERE lower(person_name) LIKE ?
           OR lower(lastname) LIKE ?
        ORDER BY fromdate
    """, [f"%{args.name.lower()}%"] * 2).fetchall()
    if not rows:
        print("No member found.")
        return
    print(f"{rows[0][0]}\n")
    for r in rows:
        house = "Senate" if r[1] == "senate" else "House"
        print(f"  {house:7s} {r[3] or '':16s} {r[2] or '':26s} {r[4]} .. {r[5]}")

    counts = con.execute("""
        SELECT chamber, min(sitting_date), max(sitting_date),
               count(DISTINCT speech_id), count(*)
        FROM para_search WHERE lower(speakername) LIKE ?
        GROUP BY chamber ORDER BY chamber
    """, [f"%{args.name.lower()}%"]).fetchall()
    print("\nIn the local corpus (2006 onward):")
    if not counts:
        print("  nothing -- this person's service may predate 2006")
    for c in counts:
        print(f"  {c[0]:7s} {c[1]} .. {c[2]}  "
              f"{c[3]:,} speeches  {c[4]:,} paragraphs")


def cmd_speech(args):
    con = connect()
    rows = con.execute("""
        SELECT para_no, text, sitting_date, speakername, chamber,
               major_heading, minor_heading, url
        FROM para_search WHERE speech_id = ? ORDER BY para_no
    """, [args.speech_id]).fetchall()
    if not rows:
        print("No such speech_id.")
        return
    r = rows[0]
    print(cite((r[2], r[3], r[4], r[5], r[6], r[7])).lstrip(" -"))
    print()
    for p in rows:
        print(f"[{p[0]}] {p[1]}\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("verify", help="check a remembered quote against Hansard")
    v.add_argument("quote")
    v.add_argument("--speaker")
    v.add_argument("--chamber", choices=["senate", "reps"])
    v.add_argument("--limit", type=int, default=5)
    v.set_defaults(fn=cmd_verify)

    s = sub.add_parser("search", help="BM25 search for a quote to cite")
    s.add_argument("terms")
    s.add_argument("--speaker")
    s.add_argument("--chamber", choices=["senate", "reps"])
    s.add_argument("--date-from")
    s.add_argument("--date-to")
    s.add_argument("--limit", type=int, default=10)
    s.set_defaults(fn=cmd_search)

    w = sub.add_parser("who", help="a member's seats, terms and corpus coverage")
    w.add_argument("name")
    w.set_defaults(fn=cmd_who)

    p = sub.add_parser("speech", help="print a full speech by id")
    p.add_argument("speech_id")
    p.set_defaults(fn=cmd_speech)

    args = ap.parse_args()
    return args.fn(args) or 0


if __name__ == "__main__":
    sys.exit(main())
