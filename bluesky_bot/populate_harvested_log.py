"""
populate_harvested_log.py

Reads URLs from harvested_history.json and all existing story files (stories/live and stories/),
scrapes them concurrently with ArticleContentExtractor, attaches Story ID and titles,
and appends results to harvested_stories_log.jsonl. Fully resumable.
"""
import os
import json
import sys
import time
import glob
import requests
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser

script_dir     = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE   = os.path.join(script_dir, "harvested_history.json")
LOG_FILE       = os.path.join(script_dir, "harvested_stories_log.jsonl")
CHUNK_SIZE     = 50     # process 50 URLs at a time
MAX_WORKERS    = 12
REQUEST_TIMEOUT = 10


class ArticleContentExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_p = False
        self.in_title = False
        self.paragraphs = []
        self.current_para = []
        self.title_data = []
        self.meta_desc = ""
        self.meta_og_desc = ""
        self.meta_og_title = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.in_p = True
        elif tag == 'title':
            self.in_title = True
        elif tag == 'meta':
            attrs_dict = dict(attrs)
            name = attrs_dict.get('name', '').lower()
            prop = attrs_dict.get('property', '').lower()
            content = attrs_dict.get('content', '').strip()
            if content:
                if name == 'description' or prop == 'description':
                    self.meta_desc = content
                elif prop == 'og:description' or name == 'og:description':
                    self.meta_og_desc = content
                elif prop == 'og:title' or name == 'og:title':
                    self.meta_og_title = content

    def handle_endtag(self, tag):
        if tag == 'p':
            self.in_p = False
            para_text = "".join(self.current_para).strip()
            if para_text:
                self.paragraphs.append(para_text)
            self.current_para = []
        elif tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_p:
            self.current_para.append(data)
        elif self.in_title:
            self.title_data.append(data)

    def get_results(self):
        title = "".join(self.title_data).strip()
        final_title = self.meta_og_title or title or ""
        final_desc = self.meta_og_desc or self.meta_desc or ""
        body = "\n\n".join(self.paragraphs).strip()
        return final_title, final_desc, body


def scrape(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    try:
        r = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        if r.status_code != 200:
            return "", f"Error: HTTP {r.status_code}"
        parser = ArticleContentExtractor()
        parser.feed(r.text)
        title, desc, body = parser.get_results()
        if not body:
            return title, "Error: No paragraph text found."
        return title, body
    except Exception as e:
        return "", f"Error: {e}"


def process_chunk(chunk_items):
    """Scrape a chunk of (url, id, fallback_title) concurrently."""
    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(scrape, item["url"]): item for item in chunk_items}
        for future in as_completed(futures):
            item = futures[future]
            url = item["url"]
            try:
                extracted_title, text = future.result()
            except Exception as e:
                extracted_title, text = "", f"Error: {e}"
            
            title = extracted_title or item.get("fallback_title") or ""
            results.append({
                "id": item.get("id", ""),
                "url": url,
                "title": title,
                "text": text,
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
            })
    return results


def main():
    print("=" * 60)
    print("ALETHEIA SOURCE HARVEST LOG REMEDIATION")
    print("=" * 60)

    # 1. Build map of all stories from stories/live and stories/
    story_map = {} # url -> {"id": sid, "title": title}
    stories_glob = glob.glob(os.path.join(script_dir, "stories", "live", "*.json")) + glob.glob(os.path.join(script_dir, "stories", "*.json"))
    for sp in stories_glob:
        try:
            with open(sp, "r", encoding="utf-8", errors="ignore") as sf:
                sd = json.load(sf)
                item = sd[0] if isinstance(sd, list) and sd else sd
                if isinstance(item, dict):
                    u = (item.get("link") or item.get("grounding_url") or item.get("target_url") or "").strip()
                    sid = item.get("id") or os.path.splitext(os.path.basename(sp))[0]
                    subj = item.get("subject") or ""
                    if u:
                        story_map[u] = {"id": sid, "title": subj}
        except Exception:
            pass
    print(f"Mapped {len(story_map)} unique story URLs from disk.")

    # 2. Load historical URLs
    all_urls = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                all_urls = json.load(f)
        except Exception:
            all_urls = []
    print(f"Loaded {len(all_urls)} URLs from harvested_history.json.")

    # Ensure all story URLs are in the candidate set
    history_set = set(all_urls)
    for u in story_map.keys():
        if u not in history_set:
            all_urls.append(u)
            history_set.add(u)

    # 3. Find already-logged URLs so we skip them
    logged_urls = set()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        logged_urls.add(json.loads(line).get("url", "").strip())
                    except Exception:
                        pass
        print(f"Skipping {len(logged_urls)} already-logged URLs in {LOG_FILE}.")

    # 4. Form list of pending items, PRIORITIZING active stories
    pending_stories = []
    pending_other = []

    for u in all_urls:
        u_clean = u.strip()
        if not u_clean or u_clean in logged_urls:
            continue
        meta = story_map.get(u_clean, {})
        entry = {
            "url": u_clean,
            "id": meta.get("id", ""),
            "fallback_title": meta.get("title", "")
        }
        if meta:
            pending_stories.append(entry)
        else:
            pending_other.append(entry)

    pending = pending_stories + pending_other
    total = len(pending)
    print(f"\nPending to scrape: {total} total ({len(pending_stories)} are live/draft stories, {len(pending_other)} other history).")
    if total == 0:
        print("Nothing to do — all URLs already logged!")
        return

    # 5. Chunk and process
    start = time.time()
    success = 0
    fail = 0
    done = 0
    num_chunks = (total + CHUNK_SIZE - 1) // CHUNK_SIZE

    with open(LOG_FILE, "a", encoding="utf-8") as lf:
        for chunk_idx in range(num_chunks):
            chunk_start = chunk_idx * CHUNK_SIZE
            chunk = pending[chunk_start : chunk_start + CHUNK_SIZE]

            print(f"Chunk {chunk_idx + 1}/{num_chunks} ({len(chunk)} URLs)...", end=" ", flush=True)
            chunk_results = process_chunk(chunk)

            for entry in chunk_results:
                lf.write(json.dumps(entry, ensure_ascii=False) + "\n")
                if entry["text"].startswith("Error:"):
                    fail += 1
                else:
                    success += 1
            lf.flush()

            done += len(chunk)
            elapsed = time.time() - start
            rate = done / elapsed if elapsed > 0 else 0
            eta_secs = (total - done) / rate if rate > 0 else 0
            print(f"done. Progress: {done}/{total} | OK: {success} | Fail: {fail} | ETA: {datetime.timedelta(seconds=int(eta_secs))}")

    elapsed_total = time.time() - start
    print(f"\n[DONE] Completed in {datetime.timedelta(seconds=int(elapsed_total))}. OK: {success} | Failed/Dead: {fail}")


if __name__ == "__main__":
    main()
