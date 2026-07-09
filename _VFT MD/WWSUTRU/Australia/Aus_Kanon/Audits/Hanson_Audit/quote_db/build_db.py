#!/usr/bin/env python3
import os
import re
import json
import glob
import sqlite3
import datetime
import unicodedata

# These are real Windows paths -- this script is meant to be run via
# Desktop Commander (native local execution), not the Linux sandbox.
# SQLite cannot safely open a .db file through the sandbox's mount of this
# folder (see README.md), so DB_PATH must point at the real local file.
AUDIT_DIR = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit"
KANON_JSON_DIR = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\compact JSON"
ARCHIVE_DIR = os.path.join(AUDIT_DIR, "Sources_Archive")
DB_PATH = os.path.join(AUDIT_DIR, "quote_db", "quote_verification.db")
SCHEMA_PATH = os.path.join(AUDIT_DIR, "quote_db", "schema.sql")

PLANE_FILES = {
    1: "Plane_1_Identity.md",
    2: "Plane_2_Definition.md",
    3: "Plane_3_Land.md",
    4: "Plane_4_Drive.md",
    5: "Plane_5_Method.md",
    6: "Plane_6_Foundation.md",
    7: "Plane_7_Result.md",
}
PLANE_KANON_JSON = {
    1: "Plane_1_Identity_compact.json",
    2: "Plane_2_Definition_compact.json",
    3: "Plane_3_Land_compact.json",
    4: "Plane_4_Drive_compact.json",
    5: "Plane_5_Method_compact.json",
    6: "Plane_6_Foundation_compact.json",
    7: "Plane_7_Result_compact.json",
}

HEADER_RE = re.compile(
    r'^\*\*\((?P<address>[^)]+)\)\s+(?P<name>.+)\s+'
    r'\(υ:\s*\\?(?P<v>[+-]?[\d.]+),\s*ψ:\s*\\?(?P<psi>[+-]?[\d.]+)\):\s*'
    r'(?P<hitfail>HIT|FAIL)\.\*\*\s*\*\*Quote:\*\*\s*(?P<quote>.+?)\s+'
    r'-(?P<source>.+?)(?:\[\^(?P<key>[\w-]+)\])?\s*$'
)

STOPWORDS = {
    "a", "an", "the", "of", "to", "in", "on", "at", "and", "or", "but", "is",
    "was", "were", "are", "be", "been", "for", "with", "as", "that", "this",
    "it", "its", "i", "we", "you", "they", "he", "she", "not", "no", "do",
    "does", "did", "have", "has", "had", "will", "would", "should", "can",
    "could", "so", "if", "then", "than", "into", "up", "out", "about",
}


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def init_schema(conn):
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()


def load_kanon_ideals():
    ideals = {}
    for plane, fname in PLANE_KANON_JSON.items():
        path = os.path.join(KANON_JSON_DIR, fname)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for entry in data:
            addr = entry.get("address")
            if not addr:
                continue
            ideals[addr] = {
                "name": entry.get("name"),
                "canonical_quote": entry.get("canonical_quote"),
                "description": entry.get("description"),
                "coordinates": entry.get("coordinates"),
            }
    return ideals


def seed_nodes(conn, ideals):
    cur = conn.cursor()
    inserted = 0
    no_citation = []
    for plane, fname in PLANE_FILES.items():
        path = os.path.join(AUDIT_DIR, fname)
        if not os.path.exists(path):
            print(f"  WARNING: {path} not found, skipping")
            continue
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
        for i, raw_line in enumerate(lines, 1):
            line = raw_line.rstrip("\n")
            if not line.startswith("**("):
                continue
            m = HEADER_RE.match(line)
            if not m:
                print(f"  UNPARSED header at {fname}:{i} -> {line[:120]}")
                continue
            address = m.group("address")
            name = m.group("name").strip()
            v = float(m.group("v"))
            psi = float(m.group("psi"))
            hitfail = m.group("hitfail")
            raw_quote = m.group("quote").strip()
            is_literal = 1 if raw_quote.startswith('"') else 0
            quote = raw_quote.strip('"')
            source_context = m.group("source").strip()
            key = m.group("key")

            if key is None:
                no_citation.append((fname, i, address, name))

            archive_file = None
            if key:
                candidate = os.path.join(ARCHIVE_DIR, f"{key}.txt")
                if os.path.exists(candidate):
                    archive_file = candidate

            ideal = ideals.get(address)
            og_ideal = None
            if ideal:
                og_ideal = f"{ideal.get('name')}: {ideal.get('canonical_quote')} -- {ideal.get('description')}"

            status = "unchecked" if key else "no_citation"

            cur.execute(
                """
                INSERT INTO nodes
                    (plane, plane_name, address, vector_name, upsilon, psi, hit_fail,
                     original_node, og_node_ideal, source_file, line, quote_in_doc,
                     is_literal_quote, source_context, citation_key, archive_file, status, last_checked)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(address, vector_name, source_file) DO UPDATE SET
                    original_node=excluded.original_node,
                    quote_in_doc=excluded.quote_in_doc,
                    is_literal_quote=excluded.is_literal_quote,
                    source_context=excluded.source_context,
                    citation_key=excluded.citation_key,
                    archive_file=excluded.archive_file,
                    line=excluded.line
                """,
                (
                    plane, fname.replace("Plane_", "").split("_")[1].replace(".md", ""),
                    address, name, v, psi, hitfail,
                    line, og_ideal, fname, i, quote, is_literal,
                    source_context, key, archive_file, status, now(),
                ),
            )
            inserted += 1
    conn.commit()
    print(f"  seeded/updated {inserted} node rows")
    if no_citation:
        print(f"  {len(no_citation)} nodes have NO citation key at all (status=no_citation):")
        for fname, i, address, name in no_citation:
            print(f"    {fname}:{i}  {address}  {name}")
    return inserted, no_citation


def rebuild_sources(conn):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT citation_key, archive_file, COUNT(*) FROM nodes
        WHERE citation_key IS NOT NULL
        GROUP BY citation_key
        """
    )
    rows = cur.fetchall()
    for key, archive_file, count in rows:
        cur.execute(
            """
            INSERT INTO hanson_sources (citation_key, archive_file, node_count, last_checked)
            VALUES (?,?,?,?)
            ON CONFLICT(citation_key) DO UPDATE SET
                archive_file=excluded.archive_file,
                node_count=excluded.node_count
            """,
            (key, archive_file, count, now()),
        )
    conn.commit()
    print(f"  rebuilt hanson_sources table: {len(rows)} distinct citation keys")


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    print("1. init schema")
    init_schema(conn)
    print("2. load Kanon compact JSON ideals")
    ideals = load_kanon_ideals()
    print(f"   loaded {len(ideals)} canonical addresses")
    print("3. seed nodes from Plane_1..7.md")
    seed_nodes(conn, ideals)
    print("4. rebuild sources table")
    rebuild_sources(conn)
    conn.close()
    print("done ->", DB_PATH)
