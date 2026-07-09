import os
import re
import json

files = ["Plane_1_Identity_albanese.md", "Plane_2_Definition_Albanese.md", "Plane_3_Land_Albanese.md"]
raw_fetches_dir = "raw_fetches"

# Parse all footnote tags and URLs
sources = {}
for fn in files:
    if os.path.exists(fn):
        with open(fn, "r", encoding="utf-8") as f:
            content = f.read()
        # Find all footnote definitions [^key]: text: URL
        matches = re.findall(r'^\[\^([^\]]+)\]:\s*(.+)', content, re.MULTILINE)
        for tag, citation_text in matches:
            urls = re.findall(r'https?://\S+', citation_text)
            url = urls[0] if urls else ""
            sources[tag] = {
                "file": fn,
                "url": url,
                "citation": citation_text
            }

scraped = {}
unscraped = {}

for tag, info in sorted(sources.items()):
    txt_path = os.path.join(raw_fetches_dir, f"{tag}.txt")
    if os.path.exists(txt_path):
        scraped[tag] = info
    else:
        # Check if URL is empty
        if not info["url"]:
            print(f"Skipping empty URL for tag {tag}")
            continue
        unscraped[tag] = info

output_data = {
    "scraped_count": len(scraped),
    "unscraped_count": len(unscraped),
    "scraped": scraped,
    "unscraped": unscraped
}

with open("unscraped_checklist.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2)

print(f"Total defined sources: {len(sources)}")
print(f"Scraped count (exist in raw_fetches/): {len(scraped)}")
print(f"Unscraped count: {len(unscraped)}")
print("Wrote detailed lists to unscraped_checklist.json")
