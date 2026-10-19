import hashlib
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "data" / "chats.sqlite"
CANVASES_DIR = ROOT / "canvases"

def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta_str, body = parts[1], parts[2].strip()
    meta = {}
    for line in meta_str.strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            meta[k] = v
    return meta, body

def main():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    
    print("1. Repairing canvas files and database records...")
    
    # Clean out old un-scoped canvas rows
    con.execute("DELETE FROM canvases WHERE id LIKE 'canvas-%' OR id LIKE 'card-%'")
    
    count = 0
    for p in CANVASES_DIR.rglob("*.md"):
        try:
            raw_text = p.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Error reading {p}: {e}")
            continue
            
        meta, body = parse_frontmatter(raw_text)
        if not meta or not meta.get("chat_id"):
            print(f"Skipping {p.name}: No chat_id in frontmatter")
            continue
            
        chat_id = meta["chat_id"]
        raw_title = meta.get("title") or p.stem
        clean_title = re.sub(r'\s*(Contents\s*Share\s*&\s*Export\s*Create|Contents|Share\s*&\s*Export|Share|Export|Download|Close|Create)\s*$', '', raw_title, flags=re.IGNORECASE).strip() or p.stem
        c_type = meta.get("type", "markdown")
        updated = meta.get("updated", "")
        
        # If title changed (e.g. stripped 'Export'), re-write file with clean frontmatter
        if clean_title != raw_title:
            new_doc = f"""---
title: "{clean_title}"
chat_id: "{chat_id}"
chat_title: "{meta.get('chat_title', '')}"
chat_url: "{meta.get('chat_url', '')}"
type: "{c_type}"
updated: "{updated}"
---

{body}
"""
            p.write_text(new_doc, encoding="utf-8")
            print(f"  Cleaned frontmatter in: {p.name} ('{raw_title}' -> '{clean_title}')")
            
        c_id = f"{chat_id}-{hashlib.sha1(clean_title.encode()).hexdigest()[:8]}"
        
        con.execute(
            """INSERT INTO canvases(id, chat_id, title, content, type, file_path, updated)
               VALUES(?,?,?,?,?,?,?)
               ON CONFLICT(id) DO UPDATE SET chat_id=excluded.chat_id, title=excluded.title,
               content=excluded.content, type=excluded.type, file_path=excluded.file_path,
               updated=excluded.updated""",
            (c_id, chat_id, clean_title, body, c_type, str(p), updated)
        )
        count += 1
        
    print(f"Successfully upserted {count} scoped canvases.")
    
    # 2. Clean message canvas tags in database
    print("2. Cleaning message canvas tags...")
    rows = con.execute("SELECT chat_id, idx, text FROM messages WHERE text LIKE '%[[CANVAS:%'").fetchall()
    msg_cleaned = 0
    for r in rows:
        cid, idx, txt = r["chat_id"], r["idx"], r["text"]
        new_txt = re.sub(r'\[\[CANVAS:\s*([^\]]+?)\s*(?:Contents\s*Share\s*&\s*Export\s*Create|Contents|Share\s*&\s*Export|Share|Export|Download|Close|Create)\s*\]\]', r'[[CANVAS: \1]]', txt, flags=re.IGNORECASE)
        if new_txt != txt:
            con.execute("UPDATE messages SET text=? WHERE chat_id=? AND idx=?", (new_txt, cid, idx))
            msg_cleaned += 1
            
    print(f"Cleaned {msg_cleaned} messages with canvas tags.")
    con.commit()
    con.close()
    
    # Notify cloud sync
    try:
        from ctx.cloud_sync import cloud_sync
        cloud_sync.notify_change("Canvas DB Repair")
        print("Notified cloud sync.")
    except Exception as e:
        print("Cloud sync notification skipped:", e)
        
    print("All repairs complete!")

if __name__ == "__main__":
    main()
