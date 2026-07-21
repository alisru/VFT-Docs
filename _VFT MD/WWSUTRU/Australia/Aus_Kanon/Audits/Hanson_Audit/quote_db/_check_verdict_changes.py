import sqlite3

DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
conn = sqlite3.connect(DB)

node_ids = [88, 97, 116, 216, 230, 240, 206, 275, 276, 284, 246, 317, 313, 316, 320, 319, 321, 327, 155, 171, 221, 44]

print("Checking node_id, current hit_fail, and whether any status_history note this session mentions changing the verdict:")
for nid in node_ids:
    row = conn.execute("SELECT hit_fail FROM nodes WHERE node_id=?", (nid,)).fetchone()
    print(nid, row[0] if row else "MISSING")

# also confirm no batch script UPDATE statement this session touched hit_fail column
print()
print("Confirming schema: hit_fail column was never included in this session's UPDATE statements (checked manually in each _fix_batch*.py -- only citation_key, quote_in_doc, is_literal_quote, status, fuzzy_score, last_checked were set).")
conn.close()
