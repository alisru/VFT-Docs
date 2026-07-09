import os
import json
import re

directories = [".", "fetch", "raw_fetches"]
tags = [
    "alboadelaide23",
    "alborepublictrans25",
    "alburyvisit26",
    "alp_platform_2022",
    "alpoleadership13",
    "eurekaballarat23",
    "jscemelectoral24",
    "loopholes23",
    "nrfpass23",
    "voicesenate23"
]

print("Scanning local caches for exact tag occurrences in previous search results...")

for d in directories:
    if not os.path.exists(d):
        continue
    for fn in os.listdir(d):
        if fn.endswith(".json") or fn.endswith(".jsonl"):
            path = os.path.join(d, fn)
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    data = json.load(f)
                
                # Check results array
                results = data.get("results", [])
                if isinstance(results, list):
                    for r in results:
                        excerpts = r.get("excerpts", [])
                        url = r.get("url", "")
                        title = r.get("title", "")
                        
                        # Check if any tag or keyword is in title, url, or excerpts
                        text_to_check = (url + " " + title + " " + " ".join(excerpts)).lower()
                        for tag in tags:
                            # Also match simpler terms if tag is complex
                            search_terms = [tag]
                            if tag == "alboadelaide23": search_terms.append("adelaide")
                            if tag == "alborepublictrans25": search_terms.append("republic")
                            if tag == "alburyvisit26": search_terms.append("farrer")
                            if tag == "alp_platform_2022": search_terms.append("platform")
                            if tag == "alpoleadership13": search_terms.append("leadership-stability")
                            if tag == "eurekaballarat23": search_terms.append("eureka")
                            if tag == "jscemelectoral24": search_terms.append("jscem")
                            if tag == "loopholes23": search_terms.append("loopholes")
                            if tag == "nrfpass23": search_terms.append("reconstruction fund")
                            if tag == "voicesenate23": search_terms.append("19 june 2023")
                            
                            for term in search_terms:
                                if term in text_to_check:
                                    print(f"\nMatch found in [{fn}] for tag/term: {tag} ({term})")
                                    print(f"  Title: {title}")
                                    print(f"  URL: {url}")
                                    for exc in excerpts[:2]: # Show first 2 excerpts
                                        print(f"  Excerpt: {exc.strip()[:200]}...")
                                    break
            except Exception as e:
                pass
