import sqlite3
conn = sqlite3.connect(r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db")
rows = conn.execute("SELECT node_id,plane,address,vector_name,hit_fail,citation_key,quote_in_doc FROM nodes WHERE status='no_citation'").fetchall()
for r in rows:
    print(r)
