"""
shard_manager.py

Lightweight incremental manager for article source shards.
Enables adding or updating individual stories in their designated shard
WITHOUT rebuilding or reloading the entire historical corpus.

Usage:
    from shard_manager import save_story_source, sync_story_to_shard
    save_story_source("quick-hits-renshaw-floored", article_text, url="https://...")
"""
import os
import sys
import json
import sqlite3
import re
import time

BOT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCES_DIRS = [
    os.path.join(BOT_DIR, "sources"),
    os.path.join(BOT_DIR, "dist_audit_site", "sources")
]
SQLITE_PATH = os.path.join(BOT_DIR, "scraped_articles_cache.sqlite")
STORIES_DIR = os.path.join(BOT_DIR, "stories")
LIVE_DIR = os.path.join(STORIES_DIR, "live")

for d in SOURCES_DIRS:
    os.makedirs(d, exist_ok=True)


def get_shard_key(story_id):
    """Computes the 0-f hexadecimal shard partition for a story id."""
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


def clean_article_body(raw_text):
    if not raw_text:
        return ''
    text = str(raw_text).strip()
    if "Actual Article Body:\n" in text:
        text = text.split("Actual Article Body:\n")[-1].strip()
    return text


def get_text_from_cache(story_id=None, url=None):
    """Retrieves full article text from SQLite cache or story JSON files."""
    text = ""
    clean_id = re.sub(r'^factcheck_', '', str(story_id or '')).strip()

    # 1. Try SQLite
    if os.path.exists(SQLITE_PATH):
        try:
            conn = sqlite3.connect(SQLITE_PATH)
            cur = conn.cursor()
            if url:
                nurl = norm_url(url)
                cur.execute("SELECT body FROM scraped_articles WHERE url = ? OR url LIKE ?", (nurl, f"%{nurl}%"))
                row = cur.fetchone()
                if row and row[0]:
                    text = clean_article_body(row[0])
            if not text and clean_id:
                # Try finding by slug in URL
                cur.execute("SELECT body FROM scraped_articles WHERE url LIKE ?", (f"%{clean_id}%",))
                row = cur.fetchone()
                if row and row[0]:
                    text = clean_article_body(row[0])
            conn.close()
        except Exception:
            pass

    if text and len(text) > 50:
        return text

    # 2. Try Story JSON file
    candidates = []
    if clean_id:
        candidates.extend([
            os.path.join(STORIES_DIR, f"factcheck_{clean_id}.json"),
            os.path.join(STORIES_DIR, f"{clean_id}.json"),
            os.path.join(LIVE_DIR, f"factcheck_{clean_id}.json"),
            os.path.join(LIVE_DIR, f"{clean_id}.json")
        ])

    for p in candidates:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                item = data[0] if isinstance(data, list) else data
                st = item.get("scraped_text", "")
                if st and len(st.strip()) > 50 and not st.startswith("Error"):
                    return clean_article_body(st)
            except Exception:
                pass

    return ""


def append_story_to_shard(story_id, text, url=None):
    """
    Surgically appends/updates a single story's article text into its designated shard.
    Touches ONLY that one shard file across local and dist directories.
    Runs in milliseconds with zero global rebuild.
    """
    clean_id = re.sub(r'^factcheck_', '', str(story_id).strip())
    if not clean_id or not text or len(text.strip()) < 30:
        return False

    body = clean_article_body(text)
    shard_key = get_shard_key(clean_id)
    shard_filename = f"shard_{shard_key}.json"

    # Also persist to SQLite if url is provided
    if url and os.path.exists(SQLITE_PATH):
        try:
            conn = sqlite3.connect(SQLITE_PATH)
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS scraped_articles (
                    url TEXT PRIMARY KEY,
                    title TEXT,
                    body TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute("""
                INSERT OR REPLACE INTO scraped_articles (url, body)
                VALUES (?, ?)
            """, (norm_url(url), body))
            conn.commit()
            conn.close()
        except Exception:
            pass

    # Update the single shard across all targets
    for sdir in SOURCES_DIRS:
        shard_path = os.path.join(sdir, shard_filename)
        data = {}
        if os.path.exists(shard_path):
            try:
                with open(shard_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}

        data[clean_id] = body
        data[f"factcheck_{clean_id}"] = body

        tmp_path = f"{shard_path}.tmp.{os.getpid()}"
        payload = json.dumps(data, ensure_ascii=False)
        last_err = None
        for attempt in range(5):
            try:
                with open(tmp_path, "w", encoding="utf-8") as f:
                    f.write(payload)
                os.replace(tmp_path, shard_path)
                last_err = None
                break
            except OSError as e:
                last_err = e
                if os.path.exists(tmp_path):
                    try:
                        os.remove(tmp_path)
                    except OSError:
                        pass
                time.sleep(0.15 * (attempt + 1))
            except Exception as e:
                last_err = e
                if os.path.exists(tmp_path):
                    try:
                        os.remove(tmp_path)
                    except OSError:
                        pass
                break
        if last_err is not None:
            print(f"Warning: Failed to write {shard_path}: {last_err}")

    return True


# Backward compatibility and API alias matching google_ai_studio_one_shot import
save_story_source = append_story_to_shard


def sync_story_to_shard(story_id, url=None):
    """Finds cached text for story_id and updates its shard."""
    text = get_text_from_cache(story_id=story_id, url=url)
    if text:
        return append_story_to_shard(story_id, text, url=url)
    return False


__all__ = [
    "get_shard_key",
    "norm_url",
    "clean_article_body",
    "get_text_from_cache",
    "append_story_to_shard",
    "save_story_source",
    "sync_story_to_shard",
]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        sid = sys.argv[1]
        u = sys.argv[2] if len(sys.argv) > 2 else None
        res = sync_story_to_shard(sid, url=u)
        print(f"Synced {sid} to shard: {res}")
    else:
        print("Usage: python shard_manager.py <story_id> [url]")