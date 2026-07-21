import sqlite3, os

DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
BASE = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit"
PLANE_FILES = [f"Plane_{i}_{n}.md" for i, n in enumerate(
    ["Identity", "Definition", "Land", "Drive", "Method", "Foundation", "Result"], start=1)]

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

node_ids = [88, 97, 116, 216, 230, 240, 206, 275, 276, 284, 246, 317, 313, 316, 320, 319, 321, 327, 155, 171, 221, 44]

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
    cite_present = f"[^{cite}]" in all_text
    snippet = (row["quote_in_doc"] or "")[:40]
    snippet_present = snippet in all_text if snippet else False
    status = "OK" if (cite_present and snippet_present) else "MISMATCH"
    if status == "MISMATCH":
        mismatches.append(nid)
    print(f"node {nid:4d} {row['vector_name']:30s} cite=[^{cite}] cite_in_md={cite_present} quote_snippet_in_md={snippet_present} -> {status}")

print()
print("Mismatches:", mismatches if mismatches else "NONE")
conn.close()
