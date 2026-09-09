#!/usr/bin/env python3
"""Build the speaker lookup: office id -> person, party, electorate, term.

A speech's `speakerid` is an *office* id (one per seat-term), not a person.
Someone who moves between chambers -- Pauline Hanson, House 1996-98 then
Senate 2016- -- holds several office ids. people.xml groups those offices
under one person id, which is what lets a single query return a politician's
whole career across both chambers.

    python members.py
"""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent
MEMBERS_DIR = ROOT / "xml" / "members"
DB_PATH = ROOT / "hansard.duckdb"
PARQUET = ROOT / "hansard_members.parquet"

SCHEMA = """
CREATE OR REPLACE TABLE members (
    office_id   VARCHAR,
    person_id   VARCHAR,
    person_name VARCHAR,
    firstname   VARCHAR,
    lastname    VARCHAR,
    house       VARCHAR,
    party       VARCHAR,
    division    VARCHAR,
    fromdate    VARCHAR,
    todate      VARCHAR
);
"""


def office_to_person():
    """Map every office id to its person id and canonical latest name."""
    root = ET.parse(MEMBERS_DIR / "people.xml").getroot()
    mapping = {}
    for person in root.findall("person"):
        pid = person.get("id")
        name = person.get("latestname")
        for office in person.findall("office"):
            mapping[office.get("id")] = (pid, name)
    return mapping


def main():
    o2p = office_to_person()
    print(f"people.xml: {len(set(v[0] for v in o2p.values())):,} people, "
          f"{len(o2p):,} offices", flush=True)

    rows = []
    for fname in ("senators.xml", "representatives.xml"):
        root = ET.parse(MEMBERS_DIR / fname).getroot()
        for m in root.findall("member"):
            a = m.attrib
            oid = a.get("id")
            pid, pname = o2p.get(oid, (None, None))
            rows.append((
                oid, pid,
                pname or f"{a.get('firstname','')} {a.get('lastname','')}".strip(),
                a.get("firstname"), a.get("lastname"), a.get("house"),
                a.get("party"), a.get("division"),
                a.get("fromdate"), a.get("todate"),
            ))
        print(f"{fname}: {len(root.findall('member')):,} seat-terms", flush=True)

    con = duckdb.connect(str(DB_PATH))
    con.execute(SCHEMA)
    con.executemany(
        "INSERT INTO members VALUES (?,?,?,?,?,?,?,?,?,?)", rows
    )
    con.execute(
        f"COPY members TO '{PARQUET.as_posix()}' (FORMAT PARQUET, COMPRESSION ZSTD)"
    )
    print(f"\nWrote {len(rows):,} seat-terms -> {PARQUET.name}", flush=True)

    unmapped = con.execute(
        "SELECT count(*) FROM members WHERE person_id IS NULL"
    ).fetchone()[0]
    if unmapped:
        print(f"  note: {unmapped} seat-terms had no person mapping", flush=True)

    print("\nCross-chamber careers (people holding seats in both houses):")
    for row in con.execute("""
        SELECT person_name, count(DISTINCT house) AS houses,
               string_agg(DISTINCT house, ' + ') AS chambers,
               min(fromdate) AS first_seat, max(todate) AS last_seat
        FROM members WHERE person_id IS NOT NULL
        GROUP BY person_name HAVING houses > 1
        ORDER BY person_name LIMIT 12
    """).fetchall():
        print(f"  {row[0]:28s} {row[2]:28s} {row[3]} .. {row[4]}")

    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
