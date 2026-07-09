import re
import os

files = ["Plane_1_Identity_albanese.md", "Plane_2_Definition_Albanese.md"]
all_urls = []

for fn in files:
    if os.path.exists(fn):
        with open(fn, "r", encoding="utf-8") as f:
            content = f.read()
        # Find all footnote definitions [^key]: text: URL
        footnotes = re.findall(r'^\[\^([^\]]+)\]:\s*(.+)', content, re.MULTILINE)
        for key, val in footnotes:
            # Extract URLs
            urls = re.findall(r'https?://\S+', val)
            for url in urls:
                all_urls.append((fn, key, url))

print(f"Total urls found: {len(all_urls)}")
for fn, key, url in all_urls:
    print(f"  [{fn}] [^{key}]: {url}")
