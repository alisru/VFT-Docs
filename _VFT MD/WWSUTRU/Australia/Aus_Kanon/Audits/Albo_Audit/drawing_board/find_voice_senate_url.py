import requests
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

url = "https://www.openaustralia.org.au/senate/?d=2023-06-19"
print("Fetching OpenAustralia Senate debates for 19 June 2023...")
try:
    resp = requests.get(url, headers=HEADERS, timeout=15)
    if resp.status_code == 200:
        print("Page fetched successfully. Searching for Constitution Alteration links...")
        # Find all links like /senate/?id=... and their text
        links = re.findall(r'href="(/senate/\?id=[^"]+)"[^>]*>(.*?)</a>', resp.text)
        found = False
        for link, text in links:
            if "Constitution Alteration" in text or "Voice" in text or "Third Reading" in text:
                full_url = "https://www.openaustralia.org.au" + link
                print(f"  Match: {text.strip()} -> {full_url}")
                found = True
        if not found:
            print("  No direct links with keywords found. Listing first 10 links:")
            for link, text in links[:10]:
                print(f"    {text.strip()} -> https://www.openaustralia.org.au{link}")
    else:
        print(f"Failed to fetch page: HTTP {resp.status_code}")
except Exception as e:
    print(f"Error fetching page: {e}")
