"""
populate_harvested_log.py

Reads URLs from harvested_history.json in chunks, scrapes them concurrently,
and appends results to harvested_stories_log.jsonl. Fully resumable.
"""
import os
import json
import sys
import time
import requests
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser

script_dir     = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE   = os.path.join(script_dir, "harvested_history.json")
LOG_FILE       = os.path.join(script_dir, "harvested_stories_log.jsonl")
CHUNK_SIZE     = 50     # process 50 URLs at a time
MAX_WORKERS    = 10
REQUEST_TIMEOUT = 10


class ParagraphExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_p = False
        self.paragraphs = []
        self.current_para = []

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            self.in_p = True

    def handle_endtag(self, tag):
        if tag == "p":
            self.in_p = False
            text = "".join(self.current_para).strip()
            if text:
                self.paragraphs.append(text)
            self.current_para = []

    def handle_data(self, data):
        if self.in_p:
            self.current_para.append(data)


def scrape(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        r = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        if r.status_code != 200:
            return f"Error: HTTP {r.status_code}"
        parser = ParagraphExtractor()
        parser.feed(r.text)
        content = "\n\n".join(parser.paragraphs).strip()
        return content if content else "Error: No paragraph text found."
    except Exception as e:
        return f"Error: {e}"


def process_chunk(urls):
    """Scrape a chunk of URLs concurrently, return list of result dicts."""
    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(scrape, url): url for url in urls}
        for future in as_completed(futures):
            url = futures[future]
            try:
                text = future.result()
            except Exception as e:
                text = f"Error: {e}"
            results.append({
                "url": url.strip(),
                "title": "",
                "text": text,
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
            })
    return results


def main():
    # --- 1. Load all historical URLs ---
    if not os.path.exists(HISTORY_FILE):
        print(f"ERROR: {HISTORY_FILE} not found.")
        sys.exit(1)

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        all_urls = json.load(f)
    print(f"Loaded {len(all_urls)} URLs from harvested_history.json.")

    # --- 2. Find already-logged URLs so we can skip them ---
    logged_urls = set()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        logged_urls.add(json.loads(line)["url"].strip())
                    except Exception:
                        pass
        print(f"Skipping {len(logged_urls)} already-logged URLs.")

    pending = [u for u in all_urls if u.strip() not in logged_urls]
    total = len(pending)
    if total == 0:
        print("Nothing to do — all URLs already logged!")
        return

    print(f"{total} URLs remaining. Processing in chunks of {CHUNK_SIZE}...\n")

    # --- 3. Chunk and process ---
    start     = time.time()
    success   = 0
    fail      = 0
    done      = 0
    num_chunks = (total + CHUNK_SIZE - 1) // CHUNK_SIZE

    with open(LOG_FILE, "a", encoding="utf-8") as lf:
        for chunk_idx in range(num_chunks):
            chunk_start = chunk_idx * CHUNK_SIZE
            chunk       = pending[chunk_start : chunk_start + CHUNK_SIZE]

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
            elapsed  = time.time() - start
            rate     = done / elapsed if elapsed > 0 else 0
            eta_secs = (total - done) / rate if rate > 0 else 0
            print(f"done. Total: {done}/{total} | OK: {success} | Fail: {fail} | ETA: {datetime.timedelta(seconds=int(eta_secs))}")

    elapsed_total = time.time() - start
    print(f"\nCompleted in {datetime.timedelta(seconds=int(elapsed_total))}. OK: {success} | Failed/Dead: {fail}")


if __name__ == "__main__":
    main()
