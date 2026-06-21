import urllib.request
import xml.etree.ElementTree as ET

urls = {
    "DW Science 1": "https://rss.dw.com/xml/rss-en-science",
    "DW Science 2": "https://rss.dw.com/xml/rss-en-sci",
    "DW Business 1": "https://rss.dw.com/xml/rss-en-bus",
    "DW Business 2": "https://rss.dw.com/xml/rss-en-business",
    "DW Tech 1": "https://rss.dw.com/xml/rss-en-tech",
    "DW Tech 2": "https://rss.dw.com/xml/rss-en-technology"
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

for name, url in urls.items():
    print(f"Testing {name}: {url}")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=3) as response:
            content = response.read()
        root = ET.fromstring(content)
        items = root.findall('.//item')
        print(f"  Success: {len(items)} items")
    except Exception as e:
        print(f"  Failed: {e}")
