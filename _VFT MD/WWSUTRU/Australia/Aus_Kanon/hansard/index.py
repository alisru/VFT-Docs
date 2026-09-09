#!/usr/bin/env python3
"""Build the search layer: a normalised text column and a BM25 index.

The normalised column is what makes quote verification reliable. A quote
remembered as `don't` and printed in Hansard as `don&apos;t`, or with a smart
apostrophe, or an em dash where the transcript has a hyphen, is the *same
quote* -- and a raw substring test would call it a fabrication. Normalise both
sides once here, compare against it forever after.

    python index.py
"""

import sys
import time
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "hansard.duckdb"

# Applied identically here and in search.py -- see norm() there.
NORM_SQL = """
lower(
  regexp_replace(
    regexp_replace(
      regexp_replace(text, '[‘’‛ʼ´`]', '''', 'g'),
      '[“”„]', '"', 'g'),
    '[‐‑‒–—―−]', '-', 'g')
)
"""


def step(label, fn):
    t = time.time()
    result = fn()
    print(f"  {label}: {time.time() - t:.1f}s", flush=True)
    return result


def main():
    if not DB_PATH.exists():
        print("hansard.duckdb not found -- run parse.py first", file=sys.stderr)
        return 1

    con = duckdb.connect(str(DB_PATH))

    n = con.execute("SELECT count(*) FROM paragraphs").fetchone()[0]
    print(f"Indexing {n:,} paragraphs\n", flush=True)

    # pid, not speech_id: the FTS document key must be UNIQUE, and speech_id
    # repeats once per paragraph (~4.4 paragraphs per speech across the
    # corpus). Indexing on a non-unique key builds without complaint and then
    # fails at query time with "more than one row returned by a subquery".
    print("Normalised text column + unique paragraph id")
    step("build", lambda: con.execute(f"""
        CREATE OR REPLACE TABLE para_search AS
        SELECT row_number() OVER () AS pid, *,
               regexp_replace({NORM_SQL}, '\\s+', ' ', 'g') AS text_norm
        FROM paragraphs
    """))

    print("\nBM25 full-text index")
    con.execute("INSTALL fts; LOAD fts;")
    step("build", lambda: con.execute(
        "PRAGMA create_fts_index('para_search', 'pid', 'text', "
        "stemmer='porter', stopwords='english', overwrite=1)"
    ))

    print("\nSanity check")
    t = time.time()
    rows = con.execute("""
        SELECT fts_main_para_search.match_bm25(pid, 'multicultural immigration') AS s,
               sitting_date, speakername, left(text, 90)
        FROM para_search WHERE s IS NOT NULL
        ORDER BY s DESC LIMIT 3
    """).fetchall()
    print(f"  query: {time.time() - t:.2f}s")
    for r in rows:
        print(f"    {r[1]} {(r[2] or '(no speaker)'):22s} {r[3]}...")

    con.close()
    print("\nIndex ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
