import json, os

log_file = os.path.join("bluesky_bot", "harvested_stories_log.jsonl")
count = 0
with open(log_file, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            count += 1

print(f"Total entries in harvested_stories_log.jsonl: {count}")

with open(log_file, "r", encoding="utf-8") as f:
    for i in range(3):
        line = f.readline()
        if line:
            data = json.loads(line)
            print(f"Sample {i+1} keys:", list(data.keys()))
            print(f"  Title: {data.get('title', '')[:40]}")
            print(f"  URL: {data.get('url', '')[:40]}")
            print(f"  Text len: {len(data.get('text', data.get('content', '')))}")