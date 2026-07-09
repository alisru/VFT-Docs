import json
import sys

# Set standard output to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

with open('fetch_section27_specific_search.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

results = d.get('results', [])
print(f"Total results: {len(results)}")

for i, r in enumerate(results):
    print(f"\n==================== Result {i} ====================")
    print(f"URL: {r.get('url')}")
    print(f"Title: {r.get('title')}")
    excerpts = r.get('excerpts', [])
    print(f"Excerpts ({len(excerpts)}):")
    for exc in excerpts:
        # Replace non-ascii chars or print cleanly
        clean_exc = exc.replace('\ufffd', ' ').replace('\u24d8', '(i)')
        print(f"  - {clean_exc.strip()}")
