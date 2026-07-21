import sqlite3
conn = sqlite3.connect(r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db")
conn.row_factory = sqlite3.Row
rows = conn.execute("SELECT node_id,address,vector_name,hit_fail,citation_key,quote_in_doc,og_node_ideal FROM nodes WHERE node_id IN (119,341,218)").fetchall()
for r in rows:
    print("===", r["node_id"], r["address"], r["vector_name"], r["hit_fail"], "cite=", r["citation_key"])
    print("Q:", r["quote_in_doc"][:250])
    print("I:", r["og_node_ideal"][:250])
