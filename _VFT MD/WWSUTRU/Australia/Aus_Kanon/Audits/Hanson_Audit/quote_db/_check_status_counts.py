import sqlite3
conn = sqlite3.connect(r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db")
conn.row_factory = sqlite3.Row

print("=== Status counts ===")
for r in conn.execute("SELECT status, COUNT(*) c FROM nodes GROUP BY status ORDER BY c DESC"):
    print(r["status"], r["c"])

print("\n=== Fabricated nodes remaining ===")
for r in conn.execute("SELECT node_id, address, vector_name FROM nodes WHERE status='fabricated'"):
    print(r["node_id"], r["address"], r["vector_name"])

print("\n=== Paraphrased nodes remaining ===")
for r in conn.execute("SELECT node_id, address, vector_name FROM nodes WHERE status='paraphrased'"):
    print(r["node_id"], r["address"], r["vector_name"])
