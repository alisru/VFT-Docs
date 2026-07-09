import requests
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

url = 'https://www.aph.gov.au/Parliamentary_Business/Hansard/Search?q=%22I+associate+Labor+with+the+remarks+of+the+Minister%22&f=28/11/2019&to=28/11/2019'
print("Searching APH...")
resp = requests.get(url, headers=HEADERS, timeout=10)

blocks = re.split(r'<li>\s*<p class="title">', resp.text)[1:]
for block in blocks:
    m = re.search(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', block)
    if m:
        display_url = m.group(1)
        if not display_url.startswith("http"):
            display_url = "https://www.aph.gov.au" + display_url
        print(f"Title: {m.group(2).strip()}")
        print(f"URL: {display_url}")
