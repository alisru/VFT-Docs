"""
Ingest chats from multiple sources into SQLite:
- Antigravity transcripts (~/.gemini/antigravity/brain)
- Saved chat logs folder (e.g. _AI files and chat logs)
- Drop folder (chat_context/inbox)
- Webhook / Extension live payloads

Skips unchanged chats by mtime. Failures are logged and skipped; nothing is ever deleted.
"""
import datetime
import hashlib
import json
import re
import time
from pathlib import Path

from .db import ROOT, connect
from .importers import parse_chat_file

BRAIN = Path.home() / ".gemini" / "antigravity" / "brain"
INBOX = ROOT / "inbox"
AI_LOGS_DIR = ROOT.parent / "_AI files and chat logs"

_REQ = re.compile(r"<USER_REQUEST>\s*(.*?)\s*</USER_REQUEST>", re.S)


def _clean_user(text: str) -> str:
    m = _REQ.search(text)
    return (m.group(1) if m else text).strip()


def _read_transcript(path: Path):
    msgs = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            continue
        t = o.get("type")
        content = (o.get("content") or "").strip()
        if not content:
            continue
        if t == "USER_INPUT":
            msgs.append(("user", o.get("created_at"), _clean_user(content)))
        elif t == "PLANNER_RESPONSE":
            msgs.append(("assistant", o.get("created_at"), content))
    return msgs


def ingest_antigravity(con, brain: Path = BRAIN):
    n_new = n_skip = n_fail = 0
    for d in sorted(brain.iterdir()) if brain.exists() else []:
        logs = d / ".system_generated" / "logs"
        f = logs / "transcript_full.jsonl"
        if not f.exists():
            f = logs / "transcript.jsonl"
        if not f.exists():
            continue
        try:
            mtime = f.stat().st_mtime
            row = con.execute("SELECT src_mtime FROM chats WHERE id=?", (d.name,)).fetchone()
            if row and row["src_mtime"] >= mtime:
                n_skip += 1
                continue
            msgs = _read_transcript(f)
            if not msgs:
                continue
            first_user = next((m[2] for m in msgs if m[0] == "user"), d.name)
            title = first_user.strip().splitlines()[0][:90] if first_user.strip() else d.name
            con.execute(
                """INSERT INTO chats(id, source, title, started, updated, n_msgs, src_mtime)
                   VALUES(?,?,?,?,?,?,?)
                   ON CONFLICT(id) DO UPDATE SET title=excluded.title, started=excluded.started,
                   updated=excluded.updated, n_msgs=excluded.n_msgs, src_mtime=excluded.src_mtime,
                   emb=NULL""",
                (d.name, "antigravity", title, msgs[0][1], msgs[-1][1], len(msgs), mtime),
            )
            con.execute("DELETE FROM messages WHERE chat_id=?", (d.name,))
            con.execute("DELETE FROM chunks WHERE chat_id=?", (d.name,))
            con.executemany(
                "INSERT INTO messages(chat_id, idx, role, ts, text) VALUES(?,?,?,?,?)",
                [(d.name, i, r, ts, tx) for i, (r, ts, tx) in enumerate(msgs)],
            )
            con.commit()
            n_new += 1
        except Exception as e:
            print(f"[warn] skipped antigravity {d.name}: {e}")
            n_fail += 1
    return n_new, n_skip, n_fail


def ingest_file(con, file_path: Path):
    """Ingest a single chatlog file (Gemini, ChatGPT, Claude, JSON)."""
    parsed = parse_chat_file(file_path)
    if not parsed or not parsed["messages"]:
        return False, "unrecognized or empty"

    mtime = file_path.stat().st_mtime
    # Stable ID derived from file path or URL
    if parsed.get("url"):
        chat_id = "url-" + hashlib.sha1(parsed["url"].encode()).hexdigest()[:16]
    else:
        chat_id = "file-" + hashlib.sha1(file_path.name.encode()).hexdigest()[:16]

    row = con.execute("SELECT src_mtime FROM chats WHERE id=?", (chat_id,)).fetchone()
    if row and row["src_mtime"] >= mtime:
        return None, "unchanged"

    msgs = parsed["messages"]
    source = parsed.get("source", "file")
    raw_title = parsed.get("title") or file_path.stem
    generic_titles = {"conversation with gemini", "gemini chat", "untitled", "new chat", "chat", ""}
    if raw_title.strip().lower() in generic_titles:
        first_user = next((m[2] for m in msgs if m[0] == "user"), raw_title)
        title = first_user.strip().splitlines()[0][:90] if first_user.strip() else raw_title
    else:
        title = raw_title

    url = parsed.get("url", "")
    file_iso = datetime.datetime.fromtimestamp(mtime, datetime.timezone.utc).isoformat()
    started = msgs[0][1] if (msgs and msgs[0][1] and str(msgs[0][1]).startswith("20")) else file_iso
    updated = msgs[-1][1] if (msgs and msgs[-1][1] and str(msgs[-1][1]).startswith("20")) else file_iso

    con.execute(
        """INSERT INTO chats(id, source, title, started, updated, n_msgs, src_mtime, url)
           VALUES(?,?,?,?,?,?,?,?)
           ON CONFLICT(id) DO UPDATE SET title=excluded.title, started=excluded.started,
           updated=excluded.updated, n_msgs=excluded.n_msgs, src_mtime=excluded.src_mtime,
           url=excluded.url, emb=NULL""",
        (chat_id, source, title, started, updated, len(msgs), mtime, url),
    )
    con.execute("DELETE FROM messages WHERE chat_id=?", (chat_id,))
    con.execute("DELETE FROM chunks WHERE chat_id=?", (chat_id,))
    con.executemany(
        "INSERT INTO messages(chat_id, idx, role, ts, text) VALUES(?,?,?,?,?)",
        [(chat_id, i, r, ts, tx) for i, (r, ts, tx) in enumerate(msgs)],
    )
    con.commit()
    return True, "ingested"


def ingest_folder(con, folder: Path):
    """Scans and ingests all recognizable chat files in a directory."""
    if not folder.exists():
        return 0, 0, 0
    n_new = n_skip = n_fail = 0
    for p in sorted(folder.iterdir()):
        if not p.is_file() or p.name.startswith("."):
            continue
        try:
            ok, status = ingest_file(con, p)
            if ok is True:
                n_new += 1
            elif ok is None:
                n_skip += 1
            else:
                n_fail += 1
        except Exception as e:
            print(f"[warn] error ingesting {p.name}: {e}")
            n_fail += 1
    return n_new, n_skip, n_fail


def ingest_payload(con, payload: dict):
    """
    Ingests live JSON payload from browser extension / userscript:
    {
       "id": "gemini-xxx" (optional),
       "source": "gemini",
       "title": "...",
       "url": "https://gemini.google.com/...",
       "messages": [{"role": "user"|"assistant", "text": "...", "ts": "..."}]
    }
    """
    msgs_raw = payload.get("messages") or []
    if not msgs_raw:
        return False, "no messages"

    url = payload.get("url") or ""
    source = payload.get("source") or "gemini"
    raw_title = (payload.get("title") or "").strip()
    generic_titles = {"conversation with gemini", "gemini chat", "untitled", "new chat", "chat", ""}
    if raw_title.lower() in generic_titles:
        first_user = next((m.get("text", "") for m in msgs_raw if m.get("role") == "user"), "")
        title = first_user.strip().splitlines()[0][:90] if first_user.strip() else "Gemini Chat"
    else:
        title = raw_title or (msgs_raw[0].get("text", "")[:90] if msgs_raw else "Gemini Chat")

    # ID precedence: explicit payload ID -> URL hash -> Title hash
    if payload.get("id"):
        chat_id = str(payload["id"])
    elif url:
        chat_id = f"{source}-" + hashlib.sha1(url.encode()).hexdigest()[:16]
    else:
        chat_id = f"{source}-" + hashlib.sha1(title.encode()).hexdigest()[:16]

    msgs = []
    for m in msgs_raw:
        role = m.get("role", "user")
        txt = (m.get("text") or m.get("content") or "").strip()
        ts = m.get("ts") or m.get("timestamp") or None
        if txt:
            msgs.append((role, ts, txt))

    if not msgs:
        return False, "no valid message text"

    mtime = time.time()
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    started = msgs[0][1] if (msgs[0][1] and str(msgs[0][1]).startswith("20")) else now_iso
    updated = msgs[-1][1] if (msgs[-1][1] and str(msgs[-1][1]).startswith("20")) else now_iso

    con.execute(
        """INSERT INTO chats(id, source, title, started, updated, n_msgs, src_mtime, url)
           VALUES(?,?,?,?,?,?,?,?)
           ON CONFLICT(id) DO UPDATE SET title=excluded.title, started=excluded.started,
           updated=excluded.updated, n_msgs=excluded.n_msgs, src_mtime=excluded.src_mtime,
           url=excluded.url, emb=NULL""",
        (chat_id, source, title, started, updated, len(msgs), mtime, url),
    )
    con.execute("DELETE FROM messages WHERE chat_id=?", (chat_id,))
    con.execute("DELETE FROM chunks WHERE chat_id=?", (chat_id,))
    con.executemany(
        "INSERT INTO messages(chat_id, idx, role, ts, text) VALUES(?,?,?,?,?)",
        [(chat_id, i, r, ts, tx) for i, (r, ts, tx) in enumerate(msgs)],
    )
    con.commit()
    return True, chat_id
