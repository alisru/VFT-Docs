import datetime
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "data" / "chats.sqlite"
CANVASES_DIR = ROOT / "canvases"

con = sqlite3.connect(DB_PATH)
con.row_factory = sqlite3.Row

chat_id = "gemini-4e95e5ac9ec7cf48"
row = con.execute("SELECT * FROM chats WHERE id=?", (chat_id,)).fetchone()
if not row:
    print(f"Chat {chat_id} not found")
    exit(1)

chat_title = row["title"]
chat_url = row["url"]
msg_row = con.execute("SELECT text FROM messages WHERE chat_id=? AND idx=1", (chat_id,)).fetchone()
if not msg_row:
    print("Message 1 not found")
    exit(1)

raw_text = msg_row["text"]

# Extract Canvas part
start_marker = "The Genie Binding Dilemma & The HegemonikonExport"
end_marker = "Edit directly or with Gemini"

if start_marker in raw_text and end_marker in raw_text:
    parts = raw_text.split(start_marker)
    pre_text = parts[0].strip()
    after_parts = parts[1].split(end_marker)
    canvas_text = after_parts[0].strip()
    
    # post text comes after "changes."
    post_raw = after_parts[1]
    post_marker = "select text to prompt Gemini for changes."
    if post_marker in post_raw:
        post_text = post_raw.split(post_marker)[1].strip()
    else:
        post_text = post_raw.strip()
    
    clean_msg_text = f"{pre_text}\n\n[[CANVAS: {canvas_title}]]\n\n{post_text}".strip()
    
    canvas_id = f"{chat_id}-genie_binding"
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Save Canvas file
    safe_chat_folder = re.sub(r'[\\/*?:"<>|]', '_', chat_title)[:60].strip()
    chat_canvas_dir = CANVASES_DIR / safe_chat_folder
    chat_canvas_dir.mkdir(parents=True, exist_ok=True)
    
    safe_filename = re.sub(r'[\\/*?:"<>|]', '_', canvas_title)[:50].strip()
    file_path = chat_canvas_dir / f"{safe_filename}.md"
    
    md_doc = f"""---
title: "{canvas_title}"
chat_id: "{chat_id}"
chat_title: "{chat_title}"
chat_url: "{chat_url}"
type: "markdown"
updated: "{now_iso}"
---

{canvas_text}
"""
    file_path.write_text(md_doc, encoding="utf-8")
    print(f"Wrote canvas file: {file_path}")
    
    # Upsert into database
    con.execute(
        """INSERT INTO canvases(id, chat_id, title, content, type, file_path, updated)
           VALUES(?,?,?,?,?,?,?)
           ON CONFLICT(id) DO UPDATE SET title=excluded.title, content=excluded.content,
           type=excluded.type, file_path=excluded.file_path, updated=excluded.updated""",
        (canvas_id, chat_id, canvas_title, canvas_text, "markdown", str(file_path), now_iso),
    )
    
    # Update message text with inline canvas marker
    con.execute("UPDATE messages SET text=? WHERE chat_id=? AND idx=1", (clean_msg_text, chat_id))
    con.commit()
    print("Database updated: Canvas registered, message text updated with inline canvas marker!")
    
    # Notify cloud sync
    from ctx.cloud_sync import cloud_sync
    cloud_sync.notify_change(canvas_title)
    print("Cloud sync notified!")
else:
    print("Markers not found in raw_text")
