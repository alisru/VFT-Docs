import os
import json
import re

directories = ["."]
tags_keywords = {
    "alboadelaide23": ["transcript-44855", "referendum-date", "30 August 2023", "transcript-46152", "transcript"],
    "alborepublictrans25": ["republic", "King Charles", "Balmoral", "republic referendum", "referendum"],
    "alburyvisit26": ["Farrer", "campaigns-in-farrer", "One Nation last"],
    "alp_platform_2022": ["platform", "national-platform"],
    "alpoleadership13": ["leadership stability", "lock in leadership", "stability"],
    "eurekaballarat23": ["eureka", "eureka-centre", "Ballarat Courier"],
    "jscemelectoral24": ["JSCEM", "2022 Federal Election", "Electoral Matters"],
    "loopholes23": ["loopholes", "Closing the Loopholes"],
    "nrfpass23": ["reconstruction-fund", "National Reconstruction Fund", "passes Parliament", "transcript-44421"],
    "voicesenate23": ["19 June 2023", "Senate Hansard", "Voice Bill", "openaustralia.org/senate"]
}

print("Searching yesterday's cache files for targeted URLs...")

matches_found = {tag: [] for tag in tags_keywords}

for fn in os.listdir("."):
    if fn.endswith(".json") and fn.startswith("fetch_"):
        try:
            with open(fn, "r", encoding="utf-8", errors="replace") as f:
                data = json.load(f)
            results = data.get("results", [])
            if isinstance(results, list):
                for r in results:
                    url = r.get("url", "")
                    title = r.get("title", "")
                    excerpts = r.get("excerpts", [])
                    combined_text = (url + " " + title + " " + " ".join(excerpts)).lower()
                    
                    for tag, kws in tags_keywords.items():
                        for kw in kws:
                            if kw.lower() in combined_text:
                                matches_found[tag].append({
                                    "file": fn,
                                    "title": title,
                                    "url": url,
                                    "excerpts": excerpts
                                })
                                break
        except Exception as e:
            pass

for tag, matches in matches_found.items():
    print(f"\n==================== Tag: {tag} ====================")
    if not matches:
        print("  No matches found in cache.")
        continue
    # Dedup by URL
    seen_urls = set()
    unique_matches = []
    for m in matches:
        if m["url"] not in seen_urls:
            seen_urls.add(m["url"])
            unique_matches.append(m)
    
    for m in unique_matches[:5]:
        print(f"  [{m['file']}] Title: {m['title']}")
        print(f"  URL: {m['url']}")
        if m["excerpts"]:
            print(f"  Excerpt: {m['excerpts'][0].strip()[:180]}...")
