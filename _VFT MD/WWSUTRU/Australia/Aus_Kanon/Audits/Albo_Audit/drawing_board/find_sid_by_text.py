import requests
import re
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# The scraped entries for 2019-11-28 from fetch_aph_direct_urls_raw.json
with open("fetch_aph_direct_urls_raw.json", "r") as f:
    data = json.load(f)

entries = data.get("2019-11-28", [])
print(f"Checking {len(entries)} APH display URLs for the veterans suicide quote...")

target_text = "I associate Labor with the remarks of the Minister for Veterans"

for entry in entries:
    url = entry["display_url"]
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            # Check if target_text is in the HTML
            if target_text.lower() in resp.text.lower():
                print(f"\nFOUND MATCH!")
                print(f"Title: {entry['title']}")
                print(f"Display URL: {url}")
                print(f"PDF URL: {entry['pdf_url']}")
                break
            else:
                # Print title to show progress
                print(f"  No match: {entry['title']}")
        else:
            print(f"  Error {resp.status_code} for: {entry['title']}")
    except Exception as e:
        print(f"  Failed to fetch {entry['title']}: {e}")
