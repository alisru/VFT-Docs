import urllib.request
import xml.etree.ElementTree as ET

urls = {
    "DW News English (en)": "https://rss.dw.com/xml/rss-en-all",
    "DW News English (gb)": "https://rss.dw.com/xml/rss-gb-all",
    "Google News World": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en",
    "Google News World (Old)": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNR3FYZHpWdEVnSnJieG9FUkNnQVAB?hl=en-US&gl=US&ceid=US:en"
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

for name, url in urls.items():
    print(f"\nTesting {name}: {url}...")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            content = response.read()
        print(f"  Response size: {len(content)} bytes")
        root = ET.fromstring(content)
        items = root.findall('.//item')
        print(f"  Parsed successfully. Found {len(items)} items.")
    except Exception as e:
        print(f"  Failed: {e}")
