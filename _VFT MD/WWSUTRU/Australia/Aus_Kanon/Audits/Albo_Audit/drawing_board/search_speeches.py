import duckdb
db_path = "e:/Vector Field Theory/VFT Docs/_VFT MD/WWSUTRU/Australia/Aus_Kanon/corpus_1998_to_2025.parquet"
conn = duckdb.connect()

q = "SELECT date, speech_no, body FROM '" + db_path + "' WHERE displayName = 'Albanese, Anthony' AND date >= '2022-05-21'"
res = conn.execute(q).fetchall()
print(f"Total speeches: {len(res)}")
for date, s_no, body in res:
    body_l = body.lower()
    if "destination" in body_l or "background" in body_l:
        for s in body.split('.'):
            s_l = s.lower()
            if "destination" in s_l or "background" in s_l:
                clean_s = s.strip().replace('\n', ' ')
                if any(x in clean_s.lower() for x in ["determine", "shouldn't", "should not", "circumstance", "opportunity"]):
                    print(f"{date} | Speech {s_no} | {clean_s}")
