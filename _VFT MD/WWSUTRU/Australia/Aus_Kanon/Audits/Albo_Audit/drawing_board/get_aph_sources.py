import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "compact JSON")))
import aph_scraper

DATES = [
    ("2025-07-24", "2025-07-24"),
    ("2019-11-28", "2019-11-28"),
    ("2025-02-10", "2025-02-10"),
    ("2020-10-08", "2020-10-08"),
    ("2022-03-31", "2022-03-31"),
    ("2021-11-24", "2021-11-24")
]

all_results = {}
for start_date, end_date in DATES:
    try:
        results = list(aph_scraper.search_all(
            "Anthony Albanese",
            date_from=start_date,
            date_to=end_date,
            role="all"
        ))
        all_results[start_date] = []
        for r in results:
            clean_url = r["hansard_display_url"].replace("&amp;", "&")
            all_results[start_date].append({
                "title": r["title"],
                "display_url": clean_url,
                "pdf_url": r["pdf_url"]
            })
    except Exception as e:
        all_results[start_date] = [{"error": str(e)}]

with open("fetch_aph_direct_urls_raw.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2)
print("Wrote direct APH links for all dates to fetch_aph_direct_urls_raw.json")
