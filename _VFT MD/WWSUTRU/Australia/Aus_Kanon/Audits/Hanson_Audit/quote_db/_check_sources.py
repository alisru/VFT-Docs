import sqlite3
conn = sqlite3.connect(r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db")
conn.row_factory = sqlite3.Row
for key in ["onenation", "tvfy", "senate18prot"]:
    r = conn.execute("SELECT citation_key,url,archive_file,source_type,status,length(full_text) as tl FROM hanson_sources WHERE citation_key=?", (key,)).fetchone()
    print(dict(r) if r else (key, "MISSING"))
