"""
source_server.py

Lightweight HTTP server that serves scraped article text from harvested_stories_log.jsonl.
Runs on localhost:8765. Started automatically by launch_panel.bat.

Endpoints:
  GET /source?url=<encoded_url>   → returns {"url":..., "title":..., "text":...} or {"error":...}
  GET /health                     → returns {"status":"ok"}
"""
import os
import json
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

script_dir = os.path.dirname(os.path.abspath(__file__))
LOG_FILE   = os.path.join(script_dir, "harvested_stories_log.jsonl")
PORT       = 8765

# --- Build in-memory index on startup ---
print(f"Loading source index from {LOG_FILE}...")
SOURCE_INDEX = {}  # url (stripped) → entry dict

if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                url = entry.get("url", "").strip()
                if url:
                    SOURCE_INDEX[url] = entry
            except Exception:
                pass
    print(f"Indexed {len(SOURCE_INDEX)} stories.")
else:
    print(f"WARNING: {LOG_FILE} not found. Source viewer will return empty results.")


class SourceHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        pass  # Suppress request logs for cleanliness

    def send_json(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")  # Allow browser fetch from file://
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/health":
            self.send_json(200, {"status": "ok", "indexed": len(SOURCE_INDEX)})
            return

        if parsed.path == "/source":
            params = urllib.parse.parse_qs(parsed.query)
            url = params.get("url", [""])[0].strip()
            sid = params.get("id", [""])[0].strip()

            if not url and not sid:
                self.send_json(400, {"error": "Missing 'url' or 'id' parameter"})
                return

            text = ""
            title = ""

            # 1. Try shard_manager / SQLite cache directly
            try:
                from shard_manager import get_text_from_cache
                text = get_text_from_cache(story_id=sid, url=url)
            except Exception:
                pass

            # 2. Try SOURCE_INDEX fallback
            if not text and url:
                entry = SOURCE_INDEX.get(url)
                if not entry:
                    clean = url.split("?")[0].rstrip("/")
                    entry = SOURCE_INDEX.get(clean)
                if not entry:
                    for key in SOURCE_INDEX:
                        if key.rstrip("/").split("?")[0] == url.rstrip("/").split("?")[0]:
                            entry = SOURCE_INDEX[key]
                            break
                if entry:
                    text = entry.get("text", "")
                    title = entry.get("title", "")

            # 3. Try reading shard file directly
            if not text and sid:
                try:
                    from shard_manager import get_shard_key
                    sk = get_shard_key(sid)
                    sp = os.path.join(script_dir, "sources", f"shard_{sk}.json")
                    if os.path.exists(sp):
                        with open(sp, "r", encoding="utf-8") as sf:
                            sdata = json.load(sf)
                        clean_sid = sid.replace("factcheck_", "")
                        text = sdata.get(clean_sid) or sdata.get(sid) or ""
                except Exception:
                    pass

            if text:
                self.send_json(200, {
                    "url":   url,
                    "id":    sid,
                    "title": title or sid or url,
                    "text":  text
                })
            else:
                self.send_json(404, {"error": f"No scraped content found for: {url or sid}"})
            return

        self.send_response(404)
        self.end_headers()


if __name__ == "__main__":
    server = HTTPServer(("localhost", PORT), SourceHandler)
    print(f"Source server running at http://localhost:{PORT}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nSource server stopped.")
