"""
build_source_shards.py

Compiles primary source article bodies into 16 lightweight web shards (shard_0.json .. shard_f.json)
for zero-latency on-demand retrieval in the Aletheia Audit Control Panel and static distribution site.

Zero external dependencies.
"""
import os
import sys
import json
import sqlite3
import re

# Ensure UTF-8 output encoding on Windows
if sys.stdout and sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

bot_dir = os.path.dirname(os.path.abspath(__file__))
dist_sources_dir = os.path.join(bot_dir, "dist_audit_site", "sources")
local_sources_dir = os.path.join(bot_dir, "sources")
os.makedirs(dist_sources_dir, exist_ok=True)
os.makedirs(local_sources_dir, exist_ok=True)

registry_file = os.path.join(bot_dir, "stories_registry.js")
live_dir = os.path.join(bot_dir, "stories", "live")
sqlite_path = os.path.join(bot_dir, "scraped_articles_cache.sqlite")

def get_shard_key(story_id):
    clean = re.sub(r'^factcheck_', '', str(story_id).strip())
    h = 0
    for ch in clean:
        h = ((h << 5) - h) + ord(ch)
        h = (h & 0xFFFFFFFF)
        if h >= 0x80000000:
            h -= 0x100000000
    return hex(abs(h) % 16)[2:]

def norm_url(url):
    if not url:
        return ''
    u = re.sub(r'[\s\u200b\u00ad]+', '', str(url).strip())
    if '?' in u:
        u = u.split('?')[0]
    if '#' in u:
        u = u.split('#')[0]
    return u.lower().rstrip('/').strip()

def build_shards():
    print("=" * 60)
    print("BUILDING 16-SHARD SOURCE TEXT DATASET")
    print("=" * 60)

    if not os.path.exists(registry_file):
        print(f"Error: {registry_file} not found.")
        return

    with open(registry_file, 'r', encoding='utf-8') as f:
        content = f.read()

    prefix = "window.ALETHEIA_STORIES_REGISTRY = "
    if prefix in content:
        content = content.replace(prefix, '').rstrip(';\n')
    else:
        content = content.split(' = ')[-1].rstrip(';\n')

    registry = json.loads(content)
    print(f"Loaded {len(registry)} stories from stories_registry.js.")

    conn = None
    if os.path.exists(sqlite_path):
        conn = sqlite3.connect(sqlite_path)
    cur = conn.cursor() if conn else None

    # Prepare 16 shard buckets
    shards = {hex(i)[2:]: {} for i in range(16)}

    populated = 0
    missing = 0

    for story in registry:
        sid = story.get('id', '')
        if not sid:
            continue
        clean_id = re.sub(r'^factcheck_', '', sid)
        shard_key = get_shard_key(clean_id)

        text = ""

        # 1. Check live JSON file
        lp = os.path.join(live_dir, f"factcheck_{clean_id}.json")
        if not os.path.exists(lp):
            lp = os.path.join(live_dir, f"{clean_id}.json")

        if os.path.exists(lp):
            try:
                with open(lp, 'r', encoding='utf-8') as sf:
                    sd = json.load(sf)
                item = sd[0] if isinstance(sd, list) else sd
                s_text = item.get('scraped_text', '')
                if s_text and len(s_text.strip()) > 100 and not s_text.startswith("Error"):
                    if "Actual Article Body:\n" in s_text:
                        text = s_text.split("Actual Article Body:\n")[-1].strip()
                    else:
                        text = s_text.strip()
            except Exception:
                pass

        # 2. Check SQLite cache
        if not text and cur:
            url = norm_url(story.get('link') or story.get('target_url') or '')
            if url:
                try:
                    cur.execute("SELECT body FROM scraped_articles WHERE url = ?", (url,))
                    row = cur.fetchone()
                    if row and row[0] and len(row[0].strip()) > 100:
                        b = row[0].strip()
                        if "Actual Article Body:\n" in b:
                            text = b.split("Actual Article Body:\n")[-1].strip()
                        else:
                            text = b
                except Exception:
                    pass

        if text:
            # Store in shard by clean_id and by sid
            shards[shard_key][clean_id] = text
            populated += 1
        else:
            missing += 1

    if conn:
        conn.close()

    print(f"Populated text for {populated} / {len(registry)} stories ({(populated/len(registry))*100:.1f}%).")
    print(f"Missing text for {missing} stories (will use graceful fallback on web).")

    # Write out each shard into dist_audit_site/sources and bluesky_bot/sources
    total_bytes = 0
    for sk in sorted(shards.keys()):
        shard_data = shards[sk]
        dist_path = os.path.join(dist_sources_dir, f"shard_{sk}.json")
        local_path = os.path.join(local_sources_dir, f"shard_{sk}.json")

        json_bytes = json.dumps(shard_data, ensure_ascii=False).encode('utf-8')
        total_bytes += len(json_bytes)

        with open(dist_path, 'wb') as df:
            df.write(json_bytes)
        with open(local_path, 'wb') as lf:
            lf.write(json_bytes)

        size_mb = len(json_bytes) / (1024 * 1024)
        print(f"  [Shard {sk}] {len(shard_data):4d} stories -> {size_mb:.2f} MB")

    print(f"\n[SUCCESS] Wrote 16 shards. Total dataset size: {total_bytes / (1024 * 1024):.2f} MB.")

if __name__ == "__main__":
    build_shards()
