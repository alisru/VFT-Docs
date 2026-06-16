import os
import json
import urllib.parse

script_dir = r"e:\Vector Field Theory\VFT Docs\bluesky_bot"
bot_stories_dir = os.path.join(script_dir, "stories")

historical_domain_counts = {}

scan_dirs = [
    bot_stories_dir,
    os.path.join(bot_stories_dir, 'live'),
    os.path.join(bot_stories_dir, 'darkroom')
]

for scan_dir in scan_dirs:
    if os.path.exists(scan_dir):
        try:
            story_files = [f for f in os.listdir(scan_dir) if f.startswith('factcheck_') and f.endswith('.json')]
            for sf in story_files:
                filepath = os.path.join(scan_dir, sf)
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                config = data[0] if isinstance(data, list) else data
                
                url = config.get("link") or config.get("target_url")
                if url:
                    url_clean = url.strip().lower()
                    try:
                        host = urllib.parse.urlparse(url_clean).hostname
                        if host:
                            host = host.replace("www.", "")
                            historical_domain_counts[host] = historical_domain_counts.get(host, 0) + 1
                    except Exception:
                        pass
        except Exception as e:
            print(f"Error scanning {scan_dir}: {e}")

sorted_counts = sorted(historical_domain_counts.items(), key=lambda x: x[1], reverse=True)
print("=== DOMAIN COUNTS IN REPO ===")
for host, count in sorted_counts:
    print(f"{host}: {count}")
