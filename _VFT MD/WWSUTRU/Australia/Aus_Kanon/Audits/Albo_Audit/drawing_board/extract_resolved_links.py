import json
import os

part1_path = "fetch_resolve_part1_20260706.json"
part2_path = "fetch_resolve_part2_20260706.json"

def show_results(path, label):
    if not os.path.exists(path):
        print(f"File {path} does not exist.")
        return
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"\n==================== {label} ====================")
    results = data.get("results", [])
    for i, r in enumerate(results):
        print(f"[{i}] Title: {r.get('title')}")
        print(f"    URL: {r.get('url')}")
        excerpts = r.get('excerpts', [])
        if excerpts:
            print(f"    Excerpt: {excerpts[0].strip()[:180]}...")

show_results(part1_path, "PART 1 RESULTS")
show_results(part2_path, "PART 2 RESULTS")
