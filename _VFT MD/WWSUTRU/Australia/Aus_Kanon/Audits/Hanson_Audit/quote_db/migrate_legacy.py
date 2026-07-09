#!/usr/bin/env python3
import re
import sqlite3
import datetime
import sys

# Windows console defaults to cp1252, which can't print the emoji status
# marks below -- force UTF-8 stdout so a print never crashes the script
# after the DB writes are already committed.
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

AUDIT_DIR = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit"
DB_PATH = AUDIT_DIR + r"\quote_db\quote_verification.db"

NODE_MARK_MAP = {
    "✅": "verified_legacy",
    "🔧": "fixed_legacy",
    "⚠️": "flagged_legacy",
    "🚩": "suspect_legacy",
    "⬜": "unchecked_legacy",
}
SOURCE_MARK_MAP = {
    "✅": "verified",
    "❌": "fabricated",
    "⚠️": "flagged",
    "⬜": "unchecked",
}


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def strip_md(s):
    s = s.strip()
    s = re.sub(r"\*\*|`", "", s)
    s = s.replace("\\", "")
    return s.strip()


def parse_pipe_table_rows(lines, start_idx):
    i = start_idx
    rows = []
    while i < len(lines):
        line = lines[i].rstrip("\n")
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not re.match(r"^:?-+:?$", cells[0]):
            rows.append(cells)
        i += 1
    return rows, i


def migrate_nodes_checklist(conn):
    path = f"{AUDIT_DIR}/Nodes_Verification_Checklist.md"
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    cur_plane = None
    updated = 0
    unmatched = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^## Plane (\d+)", line)
        if m:
            cur_plane = int(m.group(1))
        if line.startswith("| Node | Citation | Status | Note |"):
            rows, next_i = parse_pipe_table_rows(lines, i + 1)
            for cells in rows:
                if len(cells) < 4:
                    continue
                node_name = strip_md(cells[0])
                citation = strip_md(cells[1])
                status_emoji = cells[2].strip()
                note = cells[3].strip()
                legacy_status = NODE_MARK_MAP.get(status_emoji, status_emoji)

                cur = conn.cursor()
                cur.execute(
                    """
                    SELECT node_id FROM nodes
                    WHERE plane=? AND REPLACE(vector_name, '\\', '') = ?
                    """,
                    (cur_plane, node_name),
                )
                match = cur.fetchone()
                if match:
                    conn.execute(
                        "UPDATE nodes SET legacy_status=?, legacy_note=? WHERE node_id=?",
                        (legacy_status, note, match[0]),
                    )
                    updated += 1
                else:
                    unmatched.append((cur_plane, node_name, citation))
            i = next_i
            continue
        i += 1
    conn.commit()
    print(f"  nodes checklist: {updated} rows matched and migrated")
    if unmatched:
        print(f"  {len(unmatched)} node-checklist rows had no DB match:")
        for plane, name, citation in unmatched:
            print(f"    Plane {plane} / {name} / {citation}")


def migrate_sources_checklist(conn):
    path = f"{AUDIT_DIR}/Sources_Verification_Checklist.md"
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    updated = 0
    unmatched = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("| Tag | Status | Notes | Archive file |"):
            rows, next_i = parse_pipe_table_rows(lines, i + 1)
            for cells in rows:
                if len(cells) < 4:
                    continue
                tag_raw = strip_md(cells[0])
                key = tag_raw.strip("[^]")
                status_raw = cells[1].strip()
                note = cells[2].strip()
                archive = strip_md(cells[3])

                final_mark = status_raw.split("→")[-1].strip()
                final_mark = final_mark.split(" ")[0]
                legacy_status = SOURCE_MARK_MAP.get(final_mark, status_raw)

                cur = conn.cursor()
                cur.execute("SELECT citation_key FROM hanson_sources WHERE citation_key=?", (key,))
                match = cur.fetchone()
                if match:
                    conn.execute(
                        """
                        UPDATE hanson_sources
                        SET legacy_status=?, legacy_note=?, status=?, last_checked=?
                        WHERE citation_key=?
                        """,
                        (legacy_status, note, legacy_status, now(), key),
                    )
                    updated += 1
                else:
                    unmatched.append((key, status_raw))
            i = next_i
            continue
        i += 1
    conn.commit()
    print(f"  sources checklist: {updated} rows matched and migrated")
    if unmatched:
        print(f"  {len(unmatched)} source-checklist tags had no matching citation in nodes:")
        for key, status in unmatched:
            print(f"    [^{key}]  ({status}) -- cited in checklist but not used by any parsed node header")


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    print("1. migrate Nodes_Verification_Checklist.md (Plane 4 only, per its own scope note)")
    migrate_nodes_checklist(conn)
    print("2. migrate Sources_Verification_Checklist.md (all planes, citation-key level)")
    migrate_sources_checklist(conn)
    conn.close()
    print("done")
