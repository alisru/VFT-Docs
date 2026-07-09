import os
import json
import re

directories = [".", "fetch", "raw_fetches"]
keywords = ["Farrer", "Eureka", "republic", "platform", "JSCEM", "loopholes", "referendum", "Reconstruction Fund"]

print("Searching local JSON caches for keywords...")

found_urls = []

for d in directories:
    if not os.path.exists(d):
        continue
    for fn in os.listdir(d):
        if fn.endswith(".json") or fn.endswith(".jsonl"):
            path = os.path.join(d, fn)
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                # Find any URLs in this file that match our keywords in their vicinity
                for kw in keywords:
                    matches = re.finditer(re.escape(kw), content, re.IGNORECASE)
                    for m in matches:
                        start = max(0, m.start() - 300)
                        end = min(len(content), m.end() + 300)
                        snippet = content[start:end]
                        urls = re.findall(r'https?://[^\s\"\'<>]+', snippet)
                        for url in urls:
                            found_urls.append((fn, kw, url))
            except Exception as e:
                print(f"Error reading {path}: {e}")

# Clean and print unique URLs found
unique_found = sorted(list(set(found_urls)))
print(f"\nFound {len(unique_found)} unique URL candidate matches:")
for fn, kw, url in unique_found[:60]: # Print first 60 matches
    print(f"  [{fn}] ({kw}) -> {url}")
