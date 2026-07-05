import os
import json
import duckdb

PARQUET_PATH = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\corpus_1998_to_2025.parquet"

QUERY_MAP = {
    "Mateship": "mateship",
    "Larrikin": "larrikin",
    "Battler": "battler",
    "Anzac": "anzac",
    "Stringybark": "common sense",
    "Custodian": "uluru",
    "Forgotten People": "forgotten people"
}

con = duckdb.connect()

print("Searching for Albanese speeches on Plane 1 concepts...")
for concept, keyword in QUERY_MAP.items():
    print(f"\n--- {concept} (Keyword: '{keyword}') ---")
    query = """
        SELECT date, partyAbbrev, electorate, body, uniqueID
        FROM read_parquet(?)
        WHERE displayName ILIKE '%Albanese%'
          AND body ILIKE ?
          AND interject = 0
        ORDER BY date DESC
        LIMIT 5
    """
    try:
        res = con.execute(query, [PARQUET_PATH, f"%{keyword}%"]).fetchall()
        if not res:
            print("No matches found.")
        for row in res:
            date, party, electorate, body, uid = row
            snippet = body[:300].replace('\n', ' ') + "..."
            print(f"Date: {date} | Party: {party} | UID: {uid}")
            print(f"Snippet: {snippet}\n")
    except Exception as e:
        print(f"Error: {e}")
