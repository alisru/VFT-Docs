#!/usr/bin/env python3
"""Propose corrections for near-miss quotes and mismatched citation dates.

Proposes only. Nothing is written unless --apply is passed, and nothing is
proposed at all unless the correction is unambiguous:

  * the corrected quote must come from a paragraph the target speaker actually
    spoke, not one where they are being quoted by someone else
  * the matched span must not sit inside quotation marks in the source
  * the aligned window must score above --floor against the audit's text
  * the corrected text must differ from the original only in wording, not in
    which occasion it belongs to

Anything failing those tests is listed as NEEDS A HUMAN and left alone.
"""

import argparse
import re
import sys
from pathlib import Path

import duckdb
from rapidfuzz import fuzz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from search import MIN_CAND_RATIO, NEAR_FLOOR, keywords, norm, quoted_span  # noqa: E402
from verify_quotes import (KEY_RE, cited_date, extract_quotes,  # noqa: E402
                           is_hansard)

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "hansard.duckdb"
WORD = re.compile(r"\S+")


ELLIPSIS = re.compile(r"^\s*(?:\.\.\.|…)\s*|\s*(?:\.\.\.|…)\s*$")
ALNUM = re.compile(r"[^\w\s]")


def edge_words(text):
    """(first, last) content words, punctuation and case stripped."""
    words = ALNUM.sub("", norm(text)).split()
    return (words[0], words[-1]) if words else ("", "")


def split_ellipses(quote):
    """Peel off leading/trailing ellipses, which are truncation marks.

    An audit quote written as "...week after week" or "the Kokoda Track..."
    is not misquoted -- the ellipsis says the sentence continues either side.
    Aligning it against the source counts those dots as wording drift and
    "corrects" them into a comma, which silently turns a properly truncated
    quote into a mangled one. Strip them, align the inner text, put them back.
    """
    lead = "... " if re.match(r"^\s*(?:\.\.\.|…)", quote) else ""
    trail = "..." if re.search(r"(?:\.\.\.|…)\s*$", quote) else ""
    inner = ELLIPSIS.sub("", quote).strip()
    return lead, inner, trail


def best_window(paragraph, quote):
    """Find the span of `paragraph` corresponding to `quote`.

    Works on word boundaries against the ORIGINAL text so the replacement
    keeps the source's real capitalisation and punctuation -- which is the
    whole point of the correction. After the coarse search, both edges are
    trimmed greedily: a window allowed to run two words long will happily
    swallow the start of the next clause and score well doing it.
    """
    toks = list(WORD.finditer(paragraph))
    if not toks:
        return None, 0.0
    qn = norm(quote)
    want = max(1, len(qn.split()))
    best, best_score = None, -1.0
    for width in {max(1, want - 2), max(1, want - 1), want, want + 1, want + 2}:
        for i in range(0, max(1, len(toks) - width + 1)):
            j = min(i + width, len(toks)) - 1
            span = paragraph[toks[i].start(): toks[j].end()]
            score = fuzz.ratio(qn, norm(span))
            if score > best_score:
                best, best_score, bi, bj = span, score, i, j

    # Greedy edge refinement: drop a word from either end while that helps.
    improved = True
    while improved and bj > bi:
        improved = False
        for ni, nj in ((bi + 1, bj), (bi, bj - 1)):
            if nj <= ni:
                continue
            span = paragraph[toks[ni].start(): toks[nj].end()]
            score = fuzz.ratio(qn, norm(span))
            if score > best_score:
                best, best_score, bi, bj = span, score, ni, nj
                improved = True
    return best, best_score


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--sources")
    ap.add_argument("--speaker", required=True)
    ap.add_argument("--floor", type=float, default=90.0,
                    help="minimum alignment score to call a fix unambiguous")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    con = duckdb.connect(str(DB_PATH), read_only=True)
    con.execute("INSTALL fts; LOAD fts;")

    shared = {}
    if args.sources:
        for m in KEY_RE.finditer(Path(args.sources).read_text(encoding="utf-8")):
            shared[m.group("key")] = m.group("body")

    edits, manual = [], []

    for fp in args.files:
        path = Path(fp)
        text = path.read_text(encoding="utf-8")
        keys = dict(shared)
        keys.update({m.group("key"): m.group("body")
                     for m in KEY_RE.finditer(text)})

        for rec in extract_quotes(text):
            if rec["shape"] != "full" or not rec["quote"]:
                continue
            key_body = keys.get(rec["key"]) if rec["key"] else None
            if not is_hansard(rec["context"], key_body):
                continue

            q = norm(rec["quote"])
            # Every occurrence, ordered -- never LIMIT 1 on an unordered scan.
            # A quote said on more than one day has no single "actual date",
            # and picking an arbitrary row would produce a confident, wrong
            # correction.
            hits = con.execute("""
                SELECT sitting_date, speech_id FROM para_search
                WHERE text_norm LIKE ? AND lower(speakername) LIKE ?
                ORDER BY sitting_date
            """, [f"%{q}%", f"%{args.speaker.lower()}%"]).fetchall()

            if hits:  # verbatim: only the cited date can be wrong
                want = cited_date(rec["context"]) or cited_date(key_body or "")
                dates = sorted({str(h[0]) for h in hits})
                if not want or want in dates:
                    continue
                if len(dates) > 1:
                    manual.append((path.name, rec,
                                   f"cited {want} but said on {len(dates)} "
                                   f"separate days ({', '.join(dates)}) -- "
                                   "which occasion is meant is a judgement"))
                    continue
                edits.append(("DATE", path, rec, want, dates[0],
                              hits[0][1].split("/")[-1]))
                continue

            terms = " ".join(keywords(rec["quote"], 14))
            if not terms:
                continue
            cands = con.execute("""
                SELECT text, text_norm, sitting_date, speakername
                FROM (SELECT *, fts_main_para_search.match_bm25(pid, ?) AS s
                      FROM para_search)
                WHERE s IS NOT NULL AND lower(speakername) LIKE ?
                ORDER BY s DESC LIMIT 60
            """, [terms, f"%{args.speaker.lower()}%"]).fetchall()

            floor_len = len(q) * MIN_CAND_RATIO
            scored = sorted(((fuzz.partial_ratio(q, c[1]), c)
                             for c in cands if len(c[1]) >= floor_len),
                            key=lambda x: -x[0])
            if not scored or scored[0][0] < NEAR_FLOOR:
                continue

            score, c = scored[0]
            if quoted_span(c[1], q):
                manual.append((path.name, rec, "match sits inside quotation "
                               "marks -- the speaker is quoting, not speaking"))
                continue

            lead, inner, trail = split_ellipses(rec["quote"])
            span, align = best_window(c[0], inner)
            if not span or align < args.floor:
                manual.append((path.name, rec,
                               f"best alignment only {align:.0f}% -- "
                               "not a clean wording fix"))
                continue
            if norm(span) == norm(inner):
                continue  # only the ellipses differed; nothing to correct
            # A correction rewrites words *inside* the quote. If the aligned
            # span starts or ends on a different word, the edit is changing
            # how much of the sentence is quoted -- a judgement call about
            # what the quote is, not a fidelity fix. Those go to a human.
            if edge_words(span) != edge_words(inner):
                manual.append((path.name, rec,
                               "aligned span starts/ends on different words "
                               f"({edge_words(inner)} vs {edge_words(span)}) "
                               "-- changes the extent, not the wording"))
                continue

            # Don't strand source punctuation in front of a truncation mark.
            if trail:
                span = span.rstrip(" ,;:—-")
            if lead:
                span = span.lstrip(" ,;:—-")

            proposed = f"{lead}{span}{trail}"
            if proposed == rec["quote"]:
                continue  # only the ellipsis differed; nothing to correct
            edits.append(("QUOTE", path, rec, rec["quote"], proposed, str(c[2])))

    print(f"{'=' * 78}\nPROPOSED: {len(edits)} unambiguous "
          f"| NEEDS A HUMAN: {len(manual)}\n{'=' * 78}")

    for kind, path, rec, old, new, date in edits:
        print(f"\n{path.name}:{rec['line']}  {kind}")
        if kind == "DATE":
            print(f"  cited  {old}\n  actual {new}")
        else:
            print(f"  was: \"{old}\"")
            print(f"  now: \"{new}\"")
            print(f"  ({date})")

    for fname, rec, why in manual:
        print(f"\n{fname}:{rec['line']}  NEEDS A HUMAN\n  {why}\n"
              f"  \"{rec['quote'][:90]}...\"")

    if not args.apply:
        print("\n(dry run -- pass --apply to write)")
        return 0

    by_file = {}
    for kind, path, rec, old, new, date in edits:
        by_file.setdefault(path, []).append((kind, rec, old, new))

    for path, items in by_file.items():
        text = path.read_text(encoding="utf-8")
        n = 0
        for kind, rec, old, new in items:
            if kind == "QUOTE":
                needle = f'"{old}"'
                if text.count(needle) == 1:
                    text = text.replace(needle, f'"{new}"')
                    n += 1
                else:
                    print(f"  !! skipped {path.name}:{rec['line']} -- "
                          f"quote appears {text.count(needle)} times, "
                          "not uniquely replaceable")
            else:
                if text.count(old) >= 1:
                    text = text.replace(old, new)
                    n += 1
        path.write_text(text, encoding="utf-8")
        print(f"  {path.name}: {n} edit(s) written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
