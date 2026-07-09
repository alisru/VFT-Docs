import json
import duckdb
import difflib

PARQUET = "e:/Vector Field Theory/VFT Docs/_VFT MD/WWSUTRU/Australia/Aus_Kanon/corpus_1998_to_2025.parquet"
RAW_JSON = "e:/Vector Field Theory/VFT Docs/_VFT MD/WWSUTRU/Australia/Aus_Kanon/Audits/Albo_Audit/fetch_aph_direct_urls_raw.json"

QUERIES = [
    ("hansard25penalty", "2025-07-24", "earn more and to keep more"),
    ("hansard19defend", "2019-11-28", "to defend all of us"),
    ("hansard25ack", "2025-02-10", "traditional owners of the land"),
    ("hansard20future", "2020-10-08", "mass mobilisation"),
    ("hansard22climate", "2022-03-31", "stark contrast to this government"),
    ("voterintegrity21", "2021-11-24", "voter suppression"),
]

with open(RAW_JSON, "r", encoding="utf-8") as f:
    aph_data = json.load(f)

conn = duckdb.connect()

for key, date, snippet in QUERIES:
    # 1. Get detailed row from parquet
    res = conn.execute("""
        SELECT date, name, SUBSTR(body, 1, 150) as body_snippet, body
        FROM read_parquet(?)
        WHERE displayName = 'Albanese, Anthony'
          AND date = ?
          AND body ILIKE ?
    """, [PARQUET, date, f"%{snippet}%"]).fetchdf()
    
    print(f"\n=== {key} ({date}) ===")
    if res.empty:
        print("  NO MATCH IN PARQUET")
        continue
        
    p_row = res.iloc[0]
    p_title = p_row["name"]
    p_body = p_row["body"]
    print(f"  Parquet Title: {p_title}")
    print(f"  Snippet found: {p_row['body_snippet'].strip()}")
    
    # 2. Find matching title in scraped APH records
    scraped_list = aph_data.get(date, [])
    if not scraped_list:
        print("  NO SCRAPED APH RECORDS FOR THIS DATE")
        continue
        
    best_match = None
    best_score = -1
    for r in scraped_list:
        # Check similarity of the title (e.g. "QUESTIONS WITHOUT NOTICE;Wages" vs "Wages and Salaries")
        score = difflib.SequenceMatcher(None, p_title.lower(), r["title"].lower()).ratio()
        if score > best_score:
            best_score = score
            best_match = r
            
    if best_match and best_score > 0.3:
        print(f"  Best Scraped Match (score={best_score:.2f}): {best_match['title']}")
        print(f"  DIRECT APH DISPLAY URL: {best_match['display_url']}")
        print(f"  DIRECT APH PDF URL: {best_match['pdf_url']}")
    else:
        print("  COULD NOT FIND CLOSE TITLE MATCH IN SCRAPED RESULTS. Options were:")
        for r in scraped_list:
            print(f"    - {r['title']}")
