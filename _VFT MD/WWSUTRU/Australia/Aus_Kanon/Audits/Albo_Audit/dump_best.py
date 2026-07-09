import duckdb

db = duckdb.connect()
corpus = "E:/Vector Field Theory/VFT Docs/_VFT MD/WWSUTRU/Australia/Aus_Kanon/corpus_1998_to_2025.parquet"

def get_best(pattern):
    res = db.execute(f"SELECT date, uniqueID, body FROM '{corpus}' WHERE displayName ILIKE '%Albanese%' AND body ILIKE ? AND interject = 0 ORDER BY date DESC LIMIT 1", (pattern,)).fetchone()
    if res:
        print(f"[{res[0]}] ID: {res[1]}")
        print(f"QUOTE: {res[2][:800].strip()}...\n")
    else:
        print(f"NO MATCH FOR {pattern}\n")

print("--- CRIMSON THREAD ---")
get_best("%multicultural%")

print("--- WORKINGMANS PARADISE ---")
get_best("%working people%")
get_best("%trade union movement%")

print("--- BULWARK ---")
get_best("%defend our nation%")

print("--- CONNECTION ---")
get_best("%traditional owners%")

print("--- COMMON MARKET ---")
get_best("%future made in australia%")

print("--- QUIET LIFE ---")
get_best("%climate wars%")
