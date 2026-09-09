import json, os, glob

log_file = os.path.join("bluesky_bot", "harvested_stories_log.jsonl")

# Index log by id and url
log_by_id = {}
log_by_url = {}

with open(log_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line: continue
        try:
            d = json.loads(line)
            sid = d.get("id", "").strip()
            url = d.get("url", "").strip()
            if sid: log_by_id[sid] = d
            if url: log_by_url[url] = d
        except Exception:
            pass

print(f"Indexed {len(log_by_id)} entries by ID and {len(log_by_url)} by URL from harvested_stories_log.jsonl.")

# Check all live stories in stories/live/
live_files = glob.glob(os.path.join("bluesky_bot", "stories", "live", "factcheck_*.json"))
matched = 0
for fpath in live_files:
    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)
        d = data[0] if isinstance(data, list) else data
    sid = d.get("id", "")
    url = d.get("link", "")
    
    if sid in log_by_id or url in log_by_url:
        matched += 1

print(f"Total live story files: {len(live_files)}")
print(f"Total matched directly in harvested_stories_log: {matched} / {len(live_files)}")