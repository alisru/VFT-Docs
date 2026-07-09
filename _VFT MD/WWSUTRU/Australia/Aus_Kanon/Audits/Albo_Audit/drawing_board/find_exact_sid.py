import duckdb

PARQUET = "e:/Vector Field Theory/VFT Docs/_VFT MD/WWSUTRU/Australia/Aus_Kanon/corpus_1998_to_2025.parquet"
conn = duckdb.connect()

res = conn.execute("""
    SELECT date, name, "order", speech_no, "page.no", body
    FROM read_parquet(?)
    WHERE displayName = 'Albanese, Anthony'
      AND date = '2019-11-28'
      AND body ILIKE '%to defend all of us%'
""", [PARQUET]).fetchdf()

if not res.empty:
    row = res.iloc[0]
    print("Match found:")
    print("Name:", row["name"])
    print("Order:", row["order"])
    print("Speech No:", row["speech_no"])
    print("Page No:", row["page.no"])
    print("Text snippet:", row["body"][:300])
else:
    print("No match found for the 2019-11-28 quote.")
