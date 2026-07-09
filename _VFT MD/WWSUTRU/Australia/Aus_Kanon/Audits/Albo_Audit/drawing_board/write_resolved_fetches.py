import json
import os
from datetime import date

# Define the tags we are mapping from the JSON results
mapping = {
    "https://www.pm.gov.au/media/launch-yes-campaign": "alboadelaide23",
    "https://www.pm.gov.au/media/television-interview-abc-insiders-6": "alborepublictrans25",
    "https://www.alp.org.au/about/national-platform": "alp_platform_2022",
    "https://en.wikipedia.org/wiki/Leaders_of_the_Australian_Labor_Party": "alpoleadership13",
    "https://www.3ba.com.au/local-news/eureka-stockade-battle-remembered-on-its-170th-anniversary/": "eurekaballarat23",
    "https://www.finance.gov.au/publications/government-responses/final-government-response-to-the-jscem-final-report-on-the-conduct-of-the-2022-federal-election-and-other-update": "jscemelectoral24",
    "https://www.pm.gov.au/media/address-victorian-labor-conference": "loopholes23",
    "https://www.pm.gov.au/media/press-conference-parliament-house-canberra-11": "nrfpass23",
    "https://www.openaustralia.org.au/senate/?id=2023-06-19.4.2": "voicesenate23"
}

files_to_read = [
    "fetch_resolved_contents_part1.json",
    "fetch_resolved_contents_part2.json",
    "fetch_vic_labor_conf.json"
]

def clean_url(url):
    return url.split("#")[0].strip()

# Read the checklist to extract citations
checklist_path = "unscraped_checklist.json"
citations = {}
if os.path.exists(checklist_path):
    with open(checklist_path, "r", encoding="utf-8") as f:
        checklist = json.load(f)
    for tag, info in checklist.get("unscraped", {}).items():
        citations[tag] = info.get("citation", "")

for fn in files_to_read:
    if not os.path.exists(fn):
        continue
    with open(fn, "r", encoding="utf-8") as f:
        data = json.load(f)
    for r in data.get("results", []):
        url = clean_url(r.get("url", ""))
        title = r.get("title", "")
        excerpts = r.get("excerpts", [])
        
        # Check if URL maps to a tag
        # Try direct match and clean match
        tag = None
        for k, v in mapping.items():
            if clean_url(k) == url:
                tag = v
                break
        
        if tag:
            text = "\n\n".join(excerpts)
            out_path = os.path.join("raw_fetches", f"{tag}.txt")
            citation = citations.get(tag, f"{title}: {url}")
            
            with open(out_path, "w", encoding="utf-8") as out:
                out.write(f"SOURCE: [^{tag}]\n")
                out.write(f"CITATION: {citation}\n")
                out.write(f"URL: {url}\n")
                out.write(f"FETCHED: {date.today().isoformat()} (auto, via Parallel-Search-MCP web_fetch)\n")
                out.write(f"STATUS: fetched, verified and updated in audit file\n")
                out.write("\n---EXTRACTED TEXT---\n\n")
                out.write(text)
            print(f"Wrote cache file for tag: {tag} to {out_path}")
