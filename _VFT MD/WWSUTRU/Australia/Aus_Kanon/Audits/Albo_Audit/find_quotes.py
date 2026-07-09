import duckdb
import sys

db = duckdb.connect()
corpus_path = "E:/Vector Field Theory/VFT Docs/_VFT MD/WWSUTRU/Australia/Aus_Kanon/corpus_1998_to_2025.parquet"

queries = {
    "crimson_thread": ["%multicultural%", "%national story%"],
    "workingmans_paradise": ["%trade union movement%", "%working people%", "%cause of labor%"],
    "bulwark": ["%deter%", "%aggressor%", "%defend our nation%", "%defend australia%"],
    "connection": ["%connection to land%", "%traditional owners%"],
    "common_market": ["%future made in australia%", "%potential%"],
    "quiet_life": ["%climate wars%", "%safe change%", "%bring an end to%"]
}

for name, patterns in queries.items():
    print(f"--- {name.upper()} ---")
    for p in patterns:
        res = db.execute(f"""
            SELECT date, uniqueID, body 
            FROM '{corpus_path}' 
            WHERE displayName ILIKE '%Albanese%' 
              AND body ILIKE ? 
              AND interject = 0
            LIMIT 3
        """, (p,)).fetchall()
        for date, uid, body in res:
            idx = body.lower().find(p.replace('%', '').lower())
            if idx != -1:
                start = max(0, idx - 200)
                end = min(len(body), idx + 200)
                snippet = "... " + body[start:end].replace('\n', ' ') + " ..."
            else:
                snippet = body[:200].replace('\n', ' ')
            print(f"{date} [{uid}]: {snippet}")
    print()
