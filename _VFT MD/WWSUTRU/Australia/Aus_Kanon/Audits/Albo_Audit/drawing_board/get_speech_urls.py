import duckdb

PARQUET = "e:/Vector Field Theory/VFT Docs/_VFT MD/WWSUTRU/Australia/Aus_Kanon/corpus_1998_to_2025.parquet"

QUERIES = [
    ("hansard25penalty", "2025-07-24", "earn more and to keep more"),
    ("hansard19defend", "2019-11-28", "to defend all of us can be given the respect"),
    ("hansard25ack", "2025-02-10", "traditional owners of the land on which we meet"),
    ("hansard20future", "2020-10-08", "mass mobilisation of resources"),
    ("hansard22climate", "2022-03-31", "in stark contrast to this government"),
    ("voterintegrity21", "2021-11-24", "oters and the ballot box"),
    # ms96albo is 1996 - outside parquet range (1998-2025), handle separately
]

conn = duckdb.connect()

for key, date, snippet in QUERIES:
    res = conn.execute("""
        SELECT date, "order", speech_no, SUBSTR(body, 1, 200) as body_snippet
        FROM read_parquet(?)
        WHERE displayName = 'Albanese, Anthony'
          AND date = ?
          AND body ILIKE ?
    """, [PARQUET, date, f"%{snippet}%"]).fetchdf()

    print(f"\n=== {key} ({date}) ===")
    if res.empty:
        print("  NO MATCH IN PARQUET - snippet not found")
    else:
        for _, row in res.iterrows():
            sno = int(row['speech_no']) if row['speech_no'] == row['speech_no'] else 0
            url = f"https://www.openaustralia.org.au/debates/?id={row['date'].date()}.{int(row['order'])}.{sno}"
            print(f"  DIRECT URL: {url}")
            print(f"  Body: {row['body_snippet']}")
