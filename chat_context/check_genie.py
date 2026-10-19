import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
con = sqlite3.connect('data/chats.sqlite')
con.row_factory = sqlite3.Row

rows = con.execute("SELECT id, title, n_msgs, updated FROM chats WHERE title LIKE '%Genie%' OR title LIKE '%Stress%' OR title LIKE '%Philosophical%'").fetchall()
print(f"Chats matched: {len(rows)}")
for r in rows:
    print(f"ID: {r['id']}, Title: {r['title']}, Msgs: {r['n_msgs']}, Updated: {r['updated']}")
    canvases = con.execute("SELECT id, title, type, LENGTH(content) as len FROM canvases WHERE chat_id=?", (r['id'],)).fetchall()
    print(f"  Canvases in DB: {[dict(c) for c in canvases]}")

txt = con.execute("SELECT text FROM messages WHERE chat_id='gemini-4e95e5ac9ec7cf48' AND idx=1").fetchone()['text']
idx2 = txt.find("rectly, or select text")
if idx2 != -1:
    print("Found 'rectly, or select text' at pos:", idx2)
    print("Context around end of canvas:\n", txt[max(0, idx2-300):min(len(txt), idx2+400)])




