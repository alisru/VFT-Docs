#!/usr/bin/env python3
"""
Local query tool for the Katz & Alexander Hansard corpus
(corpus_1998_to_2025.parquet, CC-BY 4.0, https://zenodo.org/records/17351233).

Uses duckdb to query the parquet file directly on disk with SQL --
nothing is loaded into memory up front, so this stays fast and cheap
regardless of how many times you run it. No network requests, no rate
limits, no result caps, no scraping etiquette concerns at all -- it's
just a local file.

Covers House of Representatives proceedings from 1998-03-02 to
2025-07-31 with full speech text already parsed out (the 'body' column),
plus electorate, party, and pre-flagged question/answer/interjection
metadata.

For anything outside this file's coverage (Senate, or after 31 Jul 2025),
use aph_scraper.py instead -- that hits aph.gov.au live and has no cap
either, it's just slower since it's a real web request per page.

Schema of the source parquet (647,852 rows):
    date, displayName, name, order, speech_no, page.no, time.stamp,
    name.id, electorate, partyAbbrev, partyName, body, fedchamb_flag,
    question, answer, q_in_writing, div_flag, uniqueID, gender, member,
    senator, interject

Name matching: displayName is stored as "Lastname, Firstname" (e.g.
"Albanese, Anthony"), so this script matches on substring, case-
insensitive -- "Albanese", "Anthony Albanese", "Albanese, Anthony" all work.

Usage:
    python3 query_hansard_corpus.py "Albanese"
    python3 query_hansard_corpus.py "Albanese" --from 2010-01-01 --to 2015-12-31
    python3 query_hansard_corpus.py "Albanese" --questions-only
    python3 query_hansard_corpus.py "Albanese" --exclude-interjections

Requires: duckdb
    pip install --break-system-packages duckdb
"""

import argparse
import json
import os
import sys

import duckdb

DEFAULT_PARQUET_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "corpus_1998_to_2025.parquet"
)


def build_query(corpus_path, name_query, date_from=None, date_to=None,
                 questions_only=False, exclude_interjections=False):
    where = ["displayName ILIKE ?"]
    params = [f"%{name_query}%"]

    if date_from:
        where.append("date >= ?")
        params.append(date_from)
    if date_to:
        where.append("date <= ?")
        params.append(date_to)
    if questions_only:
        where.append("(question = '1' OR answer = '1')")
    if exclude_interjections:
        where.append("(interject IS NULL OR interject != '1')")

    where_clause = " AND ".join(where)
    sql = f"""
        SELECT date, displayName, electorate, partyName, partyAbbrev,
               question, answer, interject, body, uniqueID
        FROM read_parquet(?)
        WHERE {where_clause}
        ORDER BY date
    """
    return sql, [corpus_path] + params


def to_record(row_dict):
    return {
        "speaker_name": row_dict["displayName"],
        "source": "hansard_corpus_1998_2025 (Katz & Alexander, CC-BY 4.0)",
        "date": str(row_dict["date"]),
        "electorate": row_dict["electorate"],
        "party": row_dict["partyName"] or row_dict["partyAbbrev"],
        "is_question": row_dict["question"] == "1",
        "is_answer": row_dict["answer"] == "1",
        "is_interjection": row_dict["interject"] == "1",
        "text": row_dict["body"],
        "uniqueID": row_dict["uniqueID"],
    }


def run_query(corpus_path, name_query, date_from=None, date_to=None,
              questions_only=False, exclude_interjections=False):
    """Returns (matched_names, list_of_row_dicts). matched_names is None
    if nothing matched the name at all."""
    if not os.path.exists(corpus_path):
        raise FileNotFoundError(f"Corpus file not found at: {corpus_path}")

    con = duckdb.connect()  # in-memory connection, doesn't touch/copy the parquet file
    sql, params = build_query(corpus_path, name_query, date_from, date_to,
                               questions_only, exclude_interjections)
    result = con.execute(sql, params).fetchdf()

    if result.empty:
        # Distinguish "no such person" from "person exists, filters excluded everything"
        name_check_sql = "SELECT DISTINCT displayName FROM read_parquet(?) WHERE displayName ILIKE ?"
        name_matches = con.execute(name_check_sql, [corpus_path, f"%{name_query}%"]).fetchall()
        if not name_matches:
            return None, []
        return [r[0] for r in name_matches], []

    matched_names = result["displayName"].unique().tolist()
    rows = result.to_dict(orient="records")
    return matched_names, rows


def main():
    ap = argparse.ArgumentParser(description="Query the local 1998-2025 Hansard corpus parquet file via duckdb.")
    ap.add_argument("name", help="Name to search for, e.g. 'Albanese' or 'Anthony Albanese'")
    ap.add_argument("--corpus-path", default=DEFAULT_PARQUET_PATH,
                     help="Path to corpus_1998_to_2025.parquet (default: looks one folder up from this script)")
    ap.add_argument("--out", default=None, help="Output JSONL path (default: <slug>_corpus.jsonl)")
    ap.add_argument("--from", dest="date_from", default=None, help="Earliest date YYYY-MM-DD")
    ap.add_argument("--to", dest="date_to", default=None, help="Latest date YYYY-MM-DD")
    ap.add_argument("--questions-only", action="store_true",
                     help="Only rows flagged as a question or an answer to one")
    ap.add_argument("--exclude-interjections", action="store_true",
                     help="Drop rows flagged as interjections (usually short, out-of-turn remarks)")
    args = ap.parse_args()

    try:
        matches, rows = run_query(
            args.corpus_path, args.name, args.date_from, args.date_to,
            args.questions_only, args.exclude_interjections,
        )
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        print("Pass --corpus-path if you saved it somewhere else.", file=sys.stderr)
        sys.exit(1)

    if matches is None:
        print(f"No displayName match found for '{args.name}'.", file=sys.stderr)
        print("Try a shorter surname fragment, e.g. just 'Albanese'.", file=sys.stderr)
        sys.exit(1)

    print(f"Matched displayName(s): {matches}", file=sys.stderr)
    print(f"{len(rows)} rows after filters.", file=sys.stderr)

    out_path = args.out or (args.name.lower().replace(" ", "_").replace(",", "") + "_corpus.jsonl")
    with open(out_path, "w", encoding="utf-8") as f:
        for row_dict in rows:
            f.write(json.dumps(to_record(row_dict), ensure_ascii=False) + "\n")

    print(f"Wrote {len(rows)} records -> {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
