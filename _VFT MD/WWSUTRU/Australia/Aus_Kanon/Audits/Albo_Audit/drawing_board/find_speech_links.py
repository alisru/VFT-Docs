"""
Fetch an OpenAustralia day page and find the specific speech link containing a quote snippet.
"""
import urllib.request
import re

SEARCHES = [
    ("hansard25penalty", "https://www.openaustralia.org.au/debates/?d=2025-07-24", "earn more and to keep more"),
    ("hansard19defend",  "https://www.openaustralia.org.au/debates/?d=2019-11-28", "to defend all of us"),
    ("hansard25ack",     "https://www.openaustralia.org.au/debates/?d=2025-02-10", "traditional owners of the land"),
    ("hansard20future",  "https://www.openaustralia.org.au/debates/?d=2020-10-08", "mass mobilisation"),
    ("hansard22climate", "https://www.openaustralia.org.au/debates/?d=2022-03-31", "stark contrast to this government"),
    ("voterintegrity21", "https://www.openaustralia.org.au/debates/?d=2021-11-24", "voter suppression"),
]

for key, url, snippet in SEARCHES:
    print(f"\n=== {key} ===")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        # Find all debate links with their surrounding text
        # Pattern: <a href="/debates/?id=DATE.N.N">...</a>
        links = re.findall(r'<a href="(/debates/\?id=[^"]+)"[^>]*>([^<]*)</a>', html)
        # Find snippet in surrounding context
        idx = html.lower().find(snippet.lower())
        if idx == -1:
            print(f"  Snippet not found on page. First 5 links:")
            for href, text in links[:5]:
                print(f"  https://www.openaustralia.org.au{href}")
        else:
            # Find the closest preceding debate link
            chunk = html[max(0, idx-2000):idx+200]
            nearby = re.findall(r'/debates/\?id=([^\'"]+)', chunk)
            if nearby:
                print(f"  DIRECT URL: https://www.openaustralia.org.au/debates/?id={nearby[-1]}")
            else:
                print(f"  Snippet found at idx {idx} but no nearby id link")
    except Exception as e:
        print(f"  FETCH ERROR: {e}")
