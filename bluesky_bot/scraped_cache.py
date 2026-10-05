import os
import sys
import json
import re
import sqlite3
import datetime

# Ensure UTF-8 output encoding on Windows
if sys.stdout and sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

bot_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(bot_dir, "scraped_articles_cache.sqlite")
LOG_PATH = os.path.join(bot_dir, "harvested_stories_log.jsonl")

def sanitize_url(url):
    if not url:
        return ""
    return re.sub(r'[\s\u200b\u00ad]+', '', str(url).strip())

def normalize_url(url):
    if not url:
        return ""
    url = sanitize_url(url)
    if "?" in url:
        url = url.split("?")[0]
    if "#" in url:
        url = url.split("#")[0]
    return url.lower().rstrip("/").strip()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.execute("PRAGMA journal_mode = WAL")
    return conn

def init_cache(force=False):
    """
    Initializes the SQLite cache table and seeds it from harvested_stories_log.jsonl
    and existing story files if empty.
    """
    conn = get_db_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scraped_articles (
                url TEXT PRIMARY KEY,
                title TEXT,
                description TEXT,
                body TEXT,
                scraped_at TEXT
            )
        """)
        conn.commit()

        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM scraped_articles")
        row_count = cur.fetchone()[0]

        if row_count > 0 and not force:
            return row_count

        print(f"[Scrape Cache] Initializing cache from existing log and stories...")
        batch = []
        seen_urls = set()

        # 1. Seed from harvested_stories_log.jsonl
        if os.path.exists(LOG_PATH):
            try:
                with open(LOG_PATH, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            entry = json.loads(line)
                            raw_url = entry.get("url", "")
                            u_norm = normalize_url(raw_url)
                            if not u_norm or u_norm in seen_urls:
                                continue
                            
                            text = entry.get("text", "")
                            # Extract actual article body if composite text
                            if "Actual Article Body:\n" in text:
                                body = text.split("Actual Article Body:\n")[-1].strip()
                            else:
                                body = text.strip()
                                
                            if len(body) < 150 or body.startswith("Error"):
                                continue

                            title = entry.get("title", "")
                            ts = entry.get("timestamp", datetime.datetime.now(datetime.timezone.utc).isoformat())
                            batch.append((u_norm, title, "", body, ts))
                            seen_urls.add(u_norm)

                            if len(batch) >= 1000:
                                conn.executemany("""
                                    INSERT OR IGNORE INTO scraped_articles (url, title, description, body, scraped_at)
                                    VALUES (?, ?, ?, ?, ?)
                                """, batch)
                                batch = []
                        except Exception:
                            pass
            except Exception as e:
                print(f"Warning: Error reading {LOG_PATH} during cache init: {e}")

        # 2. Seed from stories/*.json and stories/live/*.json
        for sub_dir in ["stories", os.path.join("stories", "live"), os.path.join("stories", "darkroom")]:
            scan_path = os.path.join(bot_dir, sub_dir)
            if not os.path.exists(scan_path):
                continue
            for fname in os.listdir(scan_path):
                if fname.startswith("factcheck_") and fname.endswith(".json"):
                    fpath = os.path.join(scan_path, fname)
                    try:
                        with open(fpath, "r", encoding="utf-8") as sf:
                            sdata = json.load(sf)
                        items = sdata if isinstance(sdata, list) else [sdata]
                        for it in items:
                            s_body = it.get("scraped_text", "")
                            if not s_body or len(s_body.strip()) < 150 or s_body.startswith("Error"):
                                continue
                            s_url = it.get("link") or it.get("target_url") or ""
                            u_norm = normalize_url(s_url)
                            if not u_norm or u_norm in seen_urls:
                                continue
                            s_title = it.get("subject", "")
                            ts = it.get("published_at") or datetime.datetime.now(datetime.timezone.utc).isoformat()
                            batch.append((u_norm, s_title, "", s_body.strip(), ts))
                            seen_urls.add(u_norm)
                    except Exception:
                        pass

        if batch:
            conn.executemany("""
                INSERT OR IGNORE INTO scraped_articles (url, title, description, body, scraped_at)
                VALUES (?, ?, ?, ?, ?)
            """, batch)

        conn.commit()

        cur.execute("SELECT count(*) FROM scraped_articles")
        final_count = cur.fetchone()[0]
        print(f"[Scrape Cache] Ready. Cached {final_count} articles locally.")
        return final_count
    finally:
        conn.close()

def get_cached_article(url):
    """
    Checks if article body already exists locally.
    Returns (title, description, body) or (None, None, None) if not found.
    """
    if not url:
        return None, None, None

    u_norm = normalize_url(url)
    if not u_norm:
        return None, None, None

    # Check SQLite cache
    try:
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT title, description, body FROM scraped_articles WHERE url = ?", (u_norm,))
            row = cur.fetchone()
            if row:
                title, desc, body = row
                if body and len(body.strip()) >= 150 and not body.startswith("Error"):
                    return title or "Article", desc or "", body.strip()
        finally:
            conn.close()
    except Exception as ex:
        # Fallback if DB locked or uninitialized
        pass

    # Fallback: check live/draft stories on disk
    for sub_dir in ["stories", os.path.join("stories", "live"), os.path.join("stories", "darkroom")]:
        scan_path = os.path.join(bot_dir, sub_dir)
        if not os.path.exists(scan_path):
            continue
        try:
            for fname in os.listdir(scan_path):
                if fname.startswith("factcheck_") and fname.endswith(".json"):
                    fpath = os.path.join(scan_path, fname)
                    with open(fpath, "r", encoding="utf-8") as sf:
                        sdata = json.load(sf)
                    items = sdata if isinstance(sdata, list) else [sdata]
                    for it in items:
                        s_url = it.get("link") or it.get("target_url") or ""
                        if normalize_url(s_url) == u_norm:
                            s_body = it.get("scraped_text", "")
                            if s_body and len(s_body.strip()) >= 150 and not s_body.startswith("Error"):
                                save_cached_article(url, it.get("subject", ""), "", s_body.strip())
                                return it.get("subject", "") or "Article", "", s_body.strip()
        except Exception:
            pass

    return None, None, None

def save_cached_article(url, title, desc, body):
    """
    Persists newly scraped article to SQLite cache and appends to harvested_stories_log.jsonl.
    """
    if not url or not body or len(body.strip()) < 150 or body.startswith("Error"):
        return False

    u_norm = normalize_url(url)
    if not u_norm:
        return False

    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        conn = get_db_connection()
        try:
            conn.execute("""
                INSERT OR REPLACE INTO scraped_articles (url, title, description, body, scraped_at)
                VALUES (?, ?, ?, ?, ?)
            """, (u_norm, title or "", desc or "", body.strip(), ts))
            conn.commit()
        finally:
            conn.close()
    except Exception as ex:
        print(f"Warning: Failed to save to scraped_articles cache: {ex}")

    # Also append to log file for backwards compatibility
    try:
        entry = {
            "url": url.strip(),
            "title": title or "",
            "text": body.strip(),
            "timestamp": ts
        }
        with open(LOG_PATH, "a", encoding="utf-8") as lf:
            lf.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass

    return True

if __name__ == "__main__":
    init_cache()
