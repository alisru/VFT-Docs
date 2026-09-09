#!/usr/bin/env python3
"""Verification gate for a Kanon audit document.

Takes the audit's own plane files and checks every header quote against the
local Hansard corpus. Three verdicts, matching search.py:

    VERIFIED   the quote is in Hansard verbatim
    NEAR MISS  something very close is there -- misremembered wording; the
               real text is printed so it can be pasted in
    NOT FOUND  nothing resembles it in the chamber record

Plus two checks the audit could not previously make at all:

    DATE MISMATCH   the quote is real but the footnote cites the wrong sitting
                    day -- a right-quote-wrong-source citation
    ORPHAN MARKER   a [^key] with no matching line in the sources file

Exits non-zero if anything is NOT FOUND or has a broken citation, so it can be
wired to a hook or a pre-commit check.

    python verify_quotes.py ../Audits/Albo_Audit/Plane_1_Identity_albanese.md \
        --sources ../Audits/Albo_Audit/Sources.md --speaker Albanese
"""

import argparse
import re
import sys
from pathlib import Path

import duckdb
from rapidfuzz import fuzz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from search import (MIN_CAND_RATIO, NEAR_FLOOR, keywords, norm,  # noqa: E402
                    norm_words)

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "hansard.duckdb"

# **Quote:** "text" -Source Context (date)[^key]
#
# The source context is optional in this pattern even though the audit format
# requires it. Plenty of real nodes run the quote straight into [^key] with no
# context at all -- that is a format violation, but a gate that cannot parse a
# malformed node cannot check it either, and silently skipping the malformed
# ones is precisely how bad quotes survive. Extract everything, then report the
# missing context separately.
QUOTE_RE = re.compile(
    r'\*\*Quote:\*\*\s*"(?P<quote>.+?)"'
    r'\s*(?:[-–—]\s*(?P<context>[^\[\n]*?))?'
    r'\s*(?:\[\^(?P<key>[^\]]+)\])?\s*$',
    re.M,
)
KEY_RE = re.compile(r"^\[\^(?P<key>[^\]]+)\]:\s*(?P<body>.+)$", re.M)
DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})|(\d{1,2})\s+(\w+)\s+(\d{4})")
MONTHS = {m: f"{i:02d}" for i, m in enumerate(
    "january february march april may june july august september october "
    "november december".split(), 1)}


QUOTE_MARKER = re.compile(r"\*\*Quote:\*\*")
INNER_QUOTE = re.compile(r'"([^"]{20,})"')


def extract_quotes(text):
    """Every **Quote:** in the file, whatever shape it is in.

    Three shapes occur in real audit documents:
      full      a properly formed `"quote" -Context [^key]` header
      embedded  a quoted span inside a sentence the auditor wrote
      unquoted  no quoted text at all -- a summary with a citation bolted on,
                which the audit format explicitly forbids

    All three are yielded. A gate that only parses well-formed nodes checks
    only the nodes that were already careful.
    """
    seen = set()
    for m in QUOTE_RE.finditer(text):
        seen.add(m.start())
        yield {
            "shape": "full",
            "quote": m.group("quote").strip(),
            "context": (m.group("context") or "").strip(),
            "key": m.group("key"),
            "line": text[: m.start()].count("\n") + 1,
        }
    for m in QUOTE_MARKER.finditer(text):
        if any(abs(m.start() - s) < 3 for s in seen):
            continue
        line_text = text[m.start(): text.find("\n", m.start())]
        key = re.search(r"\[\^([^\]]+)\]", line_text)
        inner = INNER_QUOTE.search(line_text)
        yield {
            "shape": "embedded" if inner else "unquoted",
            "quote": inner.group(1).strip() if inner else "",
            "context": line_text,
            "key": key.group(1) if key else None,
            "line": text[: m.start()].count("\n") + 1,
        }


def cited_date(text):
    """Pull an ISO date out of a source context or footnote body."""
    m = DATE_RE.search(text or "")
    if not m:
        return None
    if m.group(1):
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    mon = MONTHS.get(m.group(5, ).lower()) if m.group(5) else None
    return f"{m.group(6)}-{mon}-{int(m.group(4)):02d}" if mon else None


def is_hansard(context, key_body):
    blob = f"{context} {key_body or ''}".lower()
    return "hansard" in blob or "openaustralia" in blob


ELLIPSIS_EDGE = re.compile(r"^\s*(?:\.\.\.|…)\s*|\s*(?:\.\.\.|…)\s*$")


def classify(con, quote, speaker):
    """Return (verdict, score, rows). Mirrors search.py's logic exactly.

    Leading/trailing ellipses are truncation marks, not part of the quote. A
    quote written "...week after week" is correctly marked as starting
    mid-sentence; matching it literally reports a near miss on every properly
    truncated quote in the document, and a gate that cries wolf on correct
    work gets switched off.
    """
    q = norm(ELLIPSIS_EDGE.sub("", quote).strip())
    params = [f"%{q}%"]
    clause = ""
    if speaker:
        clause = " AND lower(speakername) LIKE ?"
        params.append(f"%{speaker.lower()}%")
    exact = con.execute(f"""
        SELECT text, sitting_date, speakername, chamber, major_heading,
               minor_heading, url, speech_id
        FROM para_search WHERE text_norm LIKE ?{clause} LIMIT 5
    """, params).fetchall()
    if exact:
        return "VERIFIED", 100.0, exact

    # Same words, different punctuation. Hansard's transcription choices are
    # not misquotation, so this passes -- but it is reported separately so a
    # punctuation cleanup pass is still possible later.
    qw = norm_words(ELLIPSIS_EDGE.sub("", quote).strip())
    if len(qw) >= 25:
        wparams = [f"%{qw}%"]
        if speaker:
            wparams.append(f"%{speaker.lower()}%")
        loose = con.execute(f"""
            SELECT text, sitting_date, speakername, chamber, major_heading,
                   minor_heading, url, speech_id
            FROM para_search
            WHERE regexp_replace(text_norm, '[^\\w\\s]', ' ', 'g')
                  .regexp_replace('\\s+', ' ', 'g') LIKE ?{clause} LIMIT 5
        """, wparams).fetchall()
        if loose:
            return "VERIFIED (punctuation differs)", 100.0, loose

    terms = " ".join(keywords(quote, 14))
    if not terms:
        return "NOT FOUND", 0.0, []

    # A quote can legitimately run across a paragraph break -- two consecutive
    # paragraphs of one speech, quoted as continuous prose. Neither paragraph
    # contains it alone, so paragraph-level matching reports a near miss on
    # correctly-quoted material. Rejoin each candidate speech and retest.
    if " " in q:
        spans = con.execute(f"""
            WITH hits AS (
                -- Rank speeches by their best-scoring paragraph before
                -- limiting. A bare LIMIT with no ORDER BY takes an arbitrary
                -- 25 of every matching speech, which usually excludes the
                -- right one.
                SELECT speech_id FROM
                (SELECT *, fts_main_para_search.match_bm25(pid, ?) AS s
                 FROM para_search)
                WHERE s IS NOT NULL{clause}
                GROUP BY speech_id ORDER BY max(s) DESC LIMIT 25
            )
            SELECT p.speech_id, string_agg(p.text, ' ' ORDER BY p.para_no),
                   min(p.sitting_date), any_value(p.speakername),
                   any_value(p.chamber), any_value(p.major_heading),
                   any_value(p.minor_heading), any_value(p.url)
            FROM para_search p JOIN hits h ON p.speech_id = h.speech_id
            GROUP BY p.speech_id
        """, [terms] + ([f"%{speaker.lower()}%"] if speaker else [])).fetchall()
        for sid, joined, date, spk, ch, maj, minor, url in spans:
            jn = norm(joined)
            if q in jn:
                return "VERIFIED (spans paragraphs)", 100.0, [
                    (joined[:400], date, spk, ch, maj, minor, url, sid)]
            if len(qw) >= 25 and qw in norm_words(joined):
                return "VERIFIED (spans paragraphs)", 100.0, [
                    (joined[:400], date, spk, ch, maj, minor, url, sid)]
    where, cp = ["score IS NOT NULL"], [terms]
    if speaker:
        where.append("lower(speakername) LIKE ?")
        cp.append(f"%{speaker.lower()}%")
    cands = con.execute(f"""
        SELECT text, text_norm, sitting_date, speakername, chamber,
               major_heading, minor_heading, url, speech_id
        FROM (SELECT *, fts_main_para_search.match_bm25(pid, ?) AS score
              FROM para_search)
        WHERE {' AND '.join(where)} ORDER BY score DESC LIMIT 60
    """, cp).fetchall()

    floor = len(q) * MIN_CAND_RATIO
    scored = sorted(((fuzz.partial_ratio(q, c[1]), c)
                     for c in cands if len(c[1]) >= floor), key=lambda x: -x[0])
    if not scored:
        return "NOT FOUND", 0.0, []
    best, row = scored[0]
    rows = [(r[0], r[2], r[3], r[4], r[5], r[6], r[7], r[8])
            for s, r in scored[:3] if s >= NEAR_FLOOR]
    if best >= NEAR_FLOOR:
        return "NEAR MISS", best, rows
    return "NOT FOUND", best, []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--sources", help="file holding the [^key]: lines")
    ap.add_argument("--speaker", help="restrict corpus matching to this speaker")
    ap.add_argument("--quiet", action="store_true",
                    help="only print problems, not verified quotes")
    args = ap.parse_args()

    if not DB_PATH.exists():
        sys.exit("hansard.duckdb not found -- run parse.py then index.py first")
    con = duckdb.connect(str(DB_PATH), read_only=True)
    con.execute("INSTALL fts; LOAD fts;")

    # A marker resolves against the master key list in --sources OR against a
    # key section at the foot of the plane file itself; the audit format allows
    # either, so both must be loaded before anything is called an orphan.
    shared_keys = {}
    if args.sources:
        for m in KEY_RE.finditer(Path(args.sources).read_text(encoding="utf-8")):
            shared_keys[m.group("key")] = m.group("body")

    # Ordered, but tolerant of new verdicts so adding one never crashes a run.
    from collections import defaultdict
    tally = defaultdict(int)
    for k in ("VERIFIED", "VERIFIED (punctuation differs)",
              "VERIFIED (spans paragraphs)", "NEAR MISS", "NOT FOUND",
              "UNQUOTED", "SKIPPED (not Hansard)"):
        tally[k] = 0
    problems = []

    def check_all_markers(path, text, keys):
        """Every [^marker] in the body, not just the ones on header quotes.

        Actuality sections carry their own citations, and checking only header
        keys misses them entirely -- which is how removing a header quote's key
        can silently orphan the Actuality citations that still use it.
        """
        body = re.sub(r"^\[\^[^\]]+\]:.*$", "", text, flags=re.M)
        used = {m.group(1) for m in re.finditer(r"\[\^([^\]]+)\]", body)}
        local = {m.group("key") for m in KEY_RE.finditer(text)}
        for k in sorted(used - set(keys)):
            problems.append((path.name, 0, "ORPHAN MARKER (body)",
                             f"[^{k}] is cited in the body but resolves to no "
                             "key line"))
        for k in sorted(local - used):
            problems.append((path.name, 0, "UNUSED KEY LINE",
                             f"[^{k}] is defined but never cited"))

    for fp in args.files:
        path = Path(fp)
        text = path.read_text(encoding="utf-8")
        keys = dict(shared_keys)
        local = {m.group("key"): m.group("body") for m in KEY_RE.finditer(text)}
        keys.update(local)
        print(f"\n{'=' * 78}\n{path.name}  "
              f"({len(local)} local keys, {len(shared_keys)} shared)\n{'=' * 78}")
        check_all_markers(path, text, keys)

        for rec in extract_quotes(text):
            quote, context = rec["quote"], rec["context"]
            key, line = rec["key"], rec["line"]
            key_body = keys.get(key) if key else None

            if key and key not in keys:
                problems.append((path.name, line, "ORPHAN MARKER",
                                 f"[^{key}] resolves to no key line"))
            if not key:
                problems.append((path.name, line, "NO CITATION",
                                 f'"{quote[:60]}..."'))
            if rec["shape"] == "unquoted":
                tally["UNQUOTED"] += 1
                problems.append((path.name, line, "NOT A QUOTE",
                                 "no quoted text -- an auditor-written summary "
                                 f"with a citation attached: {context[:90]}"))
                continue
            if rec["shape"] == "full" and not context:
                problems.append((path.name, line, "NO SOURCE CONTEXT",
                                 f'"{quote[:60]}..." runs straight into its '
                                 "footnote marker"))

            if not is_hansard(context, key_body):
                tally["SKIPPED (not Hansard)"] += 1
                continue

            verdict, score, rows = classify(con, quote, args.speaker)
            tally[verdict] += 1

            if verdict.startswith("VERIFIED"):
                want = cited_date(context) or cited_date(key_body or "")
                got = {str(r[1]) for r in rows}
                if want and want not in got:
                    problems.append((
                        path.name, line, "DATE MISMATCH",
                        f'cited {want}, actually said {sorted(got)[0]}'
                        f' -- "{quote[:60]}..."'))
                elif not args.quiet:
                    print(f"  L{line:<5} VERIFIED   {quote[:66]}")
                continue

            problems.append((path.name, line, verdict,
                             f'[{score:.0f}%] "{quote[:70]}..."'))
            if verdict == "NEAR MISS" and rows:
                problems.append((path.name, line, "  -> real wording",
                                 f'"{rows[0][0][:150]}..." '
                                 f'({rows[0][2]}, {rows[0][1]})'))

    print(f"\n{'=' * 78}\nSUMMARY\n{'=' * 78}")
    for k, v in tally.items():
        print(f"  {k:24s} {v}")

    if problems:
        print(f"\n{len(problems)} item(s) needing attention:\n")
        for fname, line, kind, detail in problems:
            print(f"  {fname}:{line}  {kind}\n      {detail}")

    con.close()
    blocking = tally["NOT FOUND"] + sum(
        1 for p in problems if p[2] in ("ORPHAN MARKER", "DATE MISMATCH"))
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
