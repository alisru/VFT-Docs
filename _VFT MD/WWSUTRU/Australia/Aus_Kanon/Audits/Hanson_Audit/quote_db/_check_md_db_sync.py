import sqlite3, re, os

DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
BASE = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit"
PLANE_FILES = [f"Plane_{i}_{n}.md" for i, n in enumerate(
    ["Identity", "Definition", "Land", "Drive", "Method", "Foundation", "Result"], start=1)]

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

# nodes touched this session
node_ids = [87, 29, 73, 144, 92, 139, 108, 212, 207, 289, 248, 294, 300, 312, 272]

# load all plane text
all_text = ""
for fn in PLANE_FILES:
    p = os.path.join(BASE, fn)
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            all_text += f.read()

mismatches = []
for nid in node_ids:
    row = conn.execute("SELECT node_id, vector_name, citation_key, quote_in_doc FROM nodes WHERE node_id=?", (nid,)).fetchone()
    if not row:
        continue
    cite = row["citation_key"]
    # check citation key appears in the md text near a quote (rough check: [^cite] exists at all)
    cite_present = f"[^{cite}]" in all_text
    # check first ~40 chars of the DB quote appear verbatim in the md text
    snippet = (row["quote_in_doc"] or "")[:40]
    snippet_present = snippet in all_text if snippet else False
    status = "OK" if (cite_present and snippet_present) else "MISMATCH"
    if status == "MISMATCH":
        mismatches.append(nid)
    print(f"node {nid:4d} {row['vector_name']:20s} cite=[^{cite}] cite_in_md={cite_present} quote_snippet_in_md={snippet_present} -> {status}")

print()
print("Mismatches:", mismatches if mismatches else "NONE")
conn.close()
