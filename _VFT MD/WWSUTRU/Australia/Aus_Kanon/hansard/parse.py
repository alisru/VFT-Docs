#!/usr/bin/env python3
"""Parse harvested Hansard XML into a paragraph-grain parquet corpus.

Paragraph grain is deliberate: it is the unit you actually cite from and the
unit you embed. A single speech in the sample ran 13,513 characters, which is
far too coarse both for BM25 ranking and for quoting. Speech-level text is
recoverable at any time with a GROUP BY on speech_id.

    python parse.py                 # parse everything into hansard.duckdb + parquet
    python parse.py --chamber senate
"""

import argparse
import re
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent
XML_DIR = ROOT / "xml"
DB_PATH = ROOT / "hansard.duckdb"
PARQUET = ROOT / "hansard_paragraphs.parquet"

DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
WS_RE = re.compile(r"\s+")

SCHEMA = """
CREATE OR REPLACE TABLE paragraphs (
    chamber        VARCHAR,
    sitting_date   DATE,
    speech_id      VARCHAR,
    para_no        INTEGER,
    speakername    VARCHAR,
    speakerid      VARCHAR,
    talktype       VARCHAR,
    speech_time    VARCHAR,
    major_heading  VARCHAR,
    minor_heading  VARCHAR,
    text           VARCHAR,
    n_words        INTEGER,
    url            VARCHAR,
    source_file    VARCHAR
);
"""

INSERT = "INSERT INTO paragraphs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"


def clean(node):
    """Flatten an element's text content to a single normalised line."""
    return WS_RE.sub(" ", "".join(node.itertext())).strip()


def parse_file(path, chamber):
    """Yield paragraph rows for one sitting-day file."""
    m = DATE_RE.search(path.name)
    if not m:
        return
    sitting_date = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"

    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        print(f"  !! parse error {path.name}: {exc}", flush=True)
        return

    major = minor = None
    for node in root:
        tag = node.tag
        if tag == "major-heading":
            major = clean(node) or None
            minor = None
            continue
        if tag == "minor-heading":
            minor = clean(node) or None
            continue
        if tag != "speech":
            continue

        a = node.attrib
        para_no = 0
        for child in node:
            if child.tag not in ("p", "ul"):
                continue
            text = clean(child)
            if not text:
                continue
            para_no += 1
            yield (
                chamber,
                sitting_date,
                a.get("id"),
                para_no,
                a.get("speakername"),
                a.get("speakerid"),
                a.get("talktype"),
                a.get("time"),
                major,
                minor,
                text,
                len(text.split()),
                a.get("url"),
                path.name,
            )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chamber", choices=["senate", "reps", "all"], default="all")
    ap.add_argument("--batch", type=int, default=20000)
    args = ap.parse_args()

    chambers = ["senate", "reps"] if args.chamber == "all" else [args.chamber]

    con = duckdb.connect(str(DB_PATH))
    con.execute(SCHEMA)

    started = time.time()
    total_rows = total_files = 0
    batch = []

    for chamber in chambers:
        files = sorted((XML_DIR / chamber).glob("*.xml"))
        print(f"[{chamber}] {len(files)} files", flush=True)
        for i, path in enumerate(files, 1):
            for row in parse_file(path, chamber):
                batch.append(row)
                if len(batch) >= args.batch:
                    con.executemany(INSERT, batch)
                    total_rows += len(batch)
                    batch.clear()
            total_files += 1
            if i % 200 == 0:
                print(f"  [{chamber}] {i}/{len(files)} files, "
                      f"{total_rows + len(batch):,} paragraphs", flush=True)

    if batch:
        con.executemany(INSERT, batch)
        total_rows += len(batch)

    print(f"\nParsed {total_files:,} files -> {total_rows:,} paragraphs "
          f"in {(time.time() - started) / 60:.1f} min", flush=True)

    con.execute(
        f"COPY paragraphs TO '{PARQUET.as_posix()}' "
        "(FORMAT PARQUET, COMPRESSION ZSTD)"
    )
    size_mb = PARQUET.stat().st_size / 1048576
    print(f"Wrote {PARQUET.name}  ({size_mb:.0f} MB)", flush=True)

    # Coverage report -- this is the number that mattered.
    print("\nCoverage:")
    for row in con.execute("""
        SELECT chamber, min(sitting_date), max(sitting_date),
               count(DISTINCT sitting_date) AS days,
               count(DISTINCT speech_id) AS speeches,
               count(*) AS paragraphs
        FROM paragraphs GROUP BY chamber ORDER BY chamber
    """).fetchall():
        print(f"  {row[0]:7s} {row[1]} .. {row[2]}  "
              f"{row[3]:,} days  {row[4]:,} speeches  {row[5]:,} paragraphs")

    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
