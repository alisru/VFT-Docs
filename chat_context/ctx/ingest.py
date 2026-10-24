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

from .cloud_sync import cloud_sync
from .db import CANVASES_DIR, ROOT, connect
from .importers import parse_chat_file

BRAIN = Path.home() / ".gemini" / "antigravity" / "brain"
INBOX = ROOT / "inbox"
AI_LOGS_DIR = ROOT.parent / "_AI files and chat logs"

_REQ = re.compile(r"<USER_REQUEST>\s*(.*?)\s*</USER_REQUEST>", re.S)


def _clean_user(text: str) -> str:
    m = _REQ.search(text)
    return (m.group(1) if m else text).strip()


def resolve_canvas_title(raw_title: str, content: str) -> str:
    """
    Extracts the true, descriptive title of a canvas by prioritizing inner document
    metadata (YAML frontmatter, top # Heading, HTML <title>) over generic or toolbar-polluted UI titles.
    """
    clean_raw = (raw_title or "").strip()
    clean_raw = re.sub(
        r'\s*(Contents\s*Share\s*&\s*Export\s*Create|Contents|Share\s*&\s*Export|Share|Export|Download|Close|Create)\s*$',
        '',
        clean_raw,
        flags=re.IGNORECASE
    ).strip()

    is_generic = bool(
        not clean_raw
        or clean_raw.lower() in {"untitled", "untitled canvas", "canvas", "artifact", "card", "document"}
        or re.match(r'^(canvas|artifact|card)\s*\d+$', clean_raw, re.IGNORECASE)
    )

    body = content or ""

    # 1. Check for YAML frontmatter title
    fm_match = re.search(r"^---\s*\n(.*?)\n---", body, re.DOTALL)
    if fm_match:
        t_match = re.search(r"^title:\s*[\"']?(.*?)[\"']?$", fm_match.group(1), re.MULTILINE)
        if t_match and t_match.group(1).strip():
            candidate = t_match.group(1).strip()
            if candidate.lower() not in {"untitled", "canvas"} and not re.match(r'^(canvas|artifact)\s*\d+$', candidate, re.IGNORECASE):
                return candidate
        body = body[fm_match.end():]

    # 2. Check for Top Markdown Heading (# Heading)
    h1_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    if h1_match:
        candidate = h1_match.group(1).strip()
        candidate = re.sub(r'^(?:H1|Title|Document)\s*:\s*', '', candidate, flags=re.IGNORECASE)
        candidate = re.sub(r'[*_`]', '', candidate).strip()
        if candidate and len(candidate) > 2:
            if is_generic or len(candidate) > len(clean_raw):
                return candidate

    # 3. Check for HTML <title> tag
    html_title = re.search(r"<title>(.*?)</title>", body, re.IGNORECASE)
    if html_title and html_title.group(1).strip():
        candidate = html_title.group(1).strip()
        if is_generic or len(candidate) > len(clean_raw):
            return candidate

    # 4. Use cleaned raw title if valid
    if not is_generic and clean_raw:
        return clean_raw

    # 5. Fallback: H2 or H3 heading
    h2_match = re.search(r"^#{2,3}\s+(.+)$", body, re.MULTILINE)
    if h2_match:
        candidate = h2_match.group(1).strip()
        candidate = re.sub(r'[*_`]', '', candidate).strip()
        if candidate and len(candidate) > 2:
            return candidate

    return clean_raw or "Canvas Document"


def make_safe_canvas_filename(title: str, max_len: int = 120) -> str:
    """Creates a clean filename without cutting off words mid-character."""
    s = re.sub(r'[\\/*?:"<>|]', '_', title).strip()
    s = re.sub(r'\s+', ' ', s)
    s = s.strip('. ')
    if len(s) > max_len:
        clipped = s[:max_len]
        last_space = clipped.rfind(' ')
        if last_space > 40:
            s = clipped[:last_space].strip()
        else:
            s = clipped.strip()
    return s or "canvas"


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
            row = con.execute("SELECT src_mtime, n_msgs FROM chats WHERE id=?", (d.name,)).fetchone()
            if row and row["src_mtime"] >= mtime:
                n_skip += 1
                continue
            msgs = _read_transcript(f)
            if not msgs:
                continue
            if row and row["n_msgs"] == len(msgs):
                # No new messages; update mtime to avoid repeatedly re-reading and leave embeddings intact
                con.execute("UPDATE chats SET src_mtime=? WHERE id=?", (mtime, d.name))
                con.commit()
                n_skip += 1
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


def merge_messages(existing_msgs: list, incoming_msgs: list) -> list:
    """
    Non-destructive merge of existing and incoming messages.
    Preserves all historical turns while appending newly arrived turns.
    Never drops or truncates existing message history.
    """
    if not existing_msgs:
        return list(incoming_msgs)
    if not incoming_msgs:
        return list(existing_msgs)

    def _norm(t):
        return re.sub(r'\s+', ' ', (t or '').strip())

    seen_texts = {_norm(m[2]) for m in existing_msgs if len(m) > 2 and m[2]}

    merged = list(existing_msgs)
    for r, ts, txt in incoming_msgs:
        if not txt:
            continue
        n_txt = _norm(txt)
        if n_txt not in seen_texts:
            merged.append((r, ts, txt))
            seen_texts.add(n_txt)

    return merged


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
    def _parse_msg(m):
        if isinstance(m, (list, tuple)):
            r = m[0] if len(m) > 0 else "user"
            timestamp = m[1] if len(m) > 1 and str(m[1]).startswith("20") else None
            t = (m[2] if len(m) > 2 else (m[1] if len(m) > 1 and not str(m[1]).startswith("20") else "")).strip()
            return r, timestamp, t
        elif isinstance(m, dict):
            r = m.get("role", "user")
            t = (m.get("text") or m.get("content") or "").strip()
            timestamp = m.get("ts") or m.get("timestamp") or None
            return r, timestamp, t
        return "user", None, str(m).strip()

    msgs_raw = payload.get("messages") or []
    if not msgs_raw:
        return False, "no messages"

    parsed = [_parse_msg(m) for m in msgs_raw]
    msgs = [(r, ts, txt) for r, ts, txt in parsed if txt]
    if not msgs:
        return False, "no valid message text"

    raw_url = payload.get("url") or ""
    source = payload.get("source") or "gemini"
    # Canonicalize URL: strip query parameters, fragments, and /u/\d+/ account routing
    url = raw_url.split("?")[0].split("#")[0].rstrip("/")
    if source == "gemini" or "gemini.google.com" in url:
        url = re.sub(r'https?://gemini\.google\.com/u/\d+/', 'https://gemini.google.com/', url)

    raw_title = (payload.get("title") or "").strip()
    generic_titles = {"conversation with gemini", "gemini chat", "untitled", "new chat", "chat", ""}
    if raw_title.lower() in generic_titles:
        first_user = next((txt for r, ts, txt in msgs if r == "user"), "")
        title = first_user.strip().splitlines()[0][:90] if first_user.strip() else "Gemini Chat"
    else:
        title = raw_title or (msgs[0][2][:90] if msgs else "Gemini Chat")

    explicit_id = str(payload["id"]) if payload.get("id") else None
    chat_id = None

    # Use deterministic canonical conversation ID for Gemini, Claude, and ChatGPT
    convo_id = None
    if source == "gemini" or "gemini.google.com" in url:
        m = re.search(r'/(?:app|share|task|tasks|prompt|gem/[^/]+)/([a-zA-Z0-9_-]+)', url)
        if m:
            convo_id = m.group(1)
            chat_id = f"gemini-{convo_id}"
            if "/app/" in url:
                url = f"https://gemini.google.com/app/{convo_id}"
            elif "/task/" in url or "/tasks/" in url:
                url = f"https://gemini.google.com/task/{convo_id}"
    elif source == "claude" or "claude.ai" in url:
        m = re.search(r'/chat/([a-zA-Z0-9_-]+)', url)
        if m:
            convo_id = m.group(1)
            chat_id = f"claude-{convo_id}"
            url = f"https://claude.ai/chat/{convo_id}"
    elif source == "chatgpt" or "chatgpt.com" in url or "openai.com" in url:
        m = re.search(r'/(?:c|share)/([a-zA-Z0-9_-]+)', url)
        if m:
            convo_id = m.group(1)
            chat_id = f"chatgpt-{convo_id}"
            url = f"https://chatgpt.com/c/{convo_id}"

    if not chat_id:
        if explicit_id:
            chat_id = explicit_id
        elif url:
            chat_id = f"{source}-" + hashlib.sha1(url.encode()).hexdigest()[:16]
        else:
            chat_id = f"{source}-" + hashlib.sha1(title.encode()).hexdigest()[:16]

    # Check if this chat or URL is censored/blocked
    is_censored = con.execute(
        "SELECT 1 FROM censored_chats WHERE chat_id=? OR (url IS NOT NULL AND url != '' AND url=?) LIMIT 1",
        (chat_id, url)
    ).fetchone()
    if is_censored:
        return True, f"censored-{chat_id}"

    # Fetch existing messages for chat_id
    existing_rows = con.execute(
        "SELECT role, ts, text FROM messages WHERE chat_id=? ORDER BY idx", (chat_id,)
    ).fetchall()
    existing_msgs = [(r["role"], r["ts"], r["text"]) for r in existing_rows]

    # If convo_id is present, absorb any messages from legacy alias rows before retiring the duplicate shell
    alias_ids = []
    if convo_id:
        stale_rows = con.execute(
            "SELECT id FROM chats WHERE id != ? AND url LIKE ?",
            (chat_id, f"%{convo_id}%")
        ).fetchall()
        for s in stale_rows:
            s_id = s["id"]
            alias_ids.append(s_id)
            alias_msgs = con.execute(
                "SELECT role, ts, text FROM messages WHERE chat_id=? ORDER BY idx", (s_id,)
            ).fetchall()
            for am in alias_msgs:
                existing_msgs.append((am["role"], am["ts"], am["text"]))

    # Non-destructive merge: preserves every historical message, appends new ones
    merged_msgs = merge_messages(existing_msgs, msgs)

    mtime = time.time()
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    started = merged_msgs[0][1] if (merged_msgs and merged_msgs[0][1] and str(merged_msgs[0][1]).startswith("20")) else now_iso
    updated = merged_msgs[-1][1] if (merged_msgs and merged_msgs[-1][1] and str(merged_msgs[-1][1]).startswith("20")) else now_iso

    con.execute(
        """INSERT INTO chats(id, source, title, started, updated, n_msgs, src_mtime, url)
           VALUES(?,?,?,?,?,?,?,?)
           ON CONFLICT(id) DO UPDATE SET title=excluded.title, started=excluded.started,
           updated=excluded.updated, n_msgs=excluded.n_msgs, src_mtime=excluded.src_mtime,
           url=excluded.url, emb=NULL""",
        (chat_id, source, title, started, updated, len(merged_msgs), mtime, url),
    )

    # NOW that canonical chat_id exists in chats, safely migrate canvases and retire alias shells
    for s_id in alias_ids:
        con.execute("UPDATE OR IGNORE canvases SET chat_id=? WHERE chat_id=?", (chat_id, s_id))
        con.execute("DELETE FROM canvases WHERE chat_id=?", (s_id,))
        con.execute("DELETE FROM messages WHERE chat_id=?", (s_id,))
        con.execute("DELETE FROM chunks WHERE chat_id=?", (s_id,))
        con.execute("DELETE FROM chats WHERE id=?", (s_id,))

    # Insert or update every message by index without deleting any message history
    for i, (r, ts, tx) in enumerate(merged_msgs):
        con.execute(
            """INSERT INTO messages(chat_id, idx, role, ts, text)
               VALUES(?,?,?,?,?)
               ON CONFLICT(chat_id, idx) DO UPDATE SET
                   role=excluded.role,
                   ts=COALESCE(excluded.ts, messages.ts),
                   text=excluded.text""",
            (chat_id, i, r, ts, tx),
        )

    # Process and save any canvases
    canvases_raw = payload.get("canvases") or []
    if canvases_raw:
        safe_chat_folder = re.sub(r'[\\/*?:"<>|]', '_', title)[:60].strip() or chat_id
        chat_canvas_dir = CANVASES_DIR / safe_chat_folder
        chat_canvas_dir.mkdir(parents=True, exist_ok=True)

        seen_titles = {}
        # Resolve true title from content and keep longest version if duplicates exist
        for cv in canvases_raw:
            raw_title = cv.get("title") or ""
            c_type = (cv.get("type") or "markdown").strip()
            c_content = (cv.get("content") or "").strip()
            if not c_content or len(c_content) < 250:
                continue

            c_title = resolve_canvas_title(raw_title, c_content)
            norm_title = re.sub(r'\s+', ' ', c_title.lower()).strip()

            if norm_title in seen_titles:
                if len(c_content) > len(seen_titles[norm_title]["content"]):
                    seen_titles[norm_title] = {"title": c_title, "type": c_type, "content": c_content}
            else:
                seen_titles[norm_title] = {"title": c_title, "type": c_type, "content": c_content}

        changed_canvases = []
        for norm_title, cv in seen_titles.items():
            c_title = cv["title"]
            c_type = cv["type"]
            c_content = cv["content"]
            c_id = f"{chat_id}-{hashlib.sha1(norm_title.encode()).hexdigest()[:8]}"
            safe_filename = make_safe_canvas_filename(c_title, max_len=120)
            file_path = chat_canvas_dir / f"{safe_filename}.md"
            meta_path = chat_canvas_dir / f"{safe_filename}.meta.json"

            # 1. Pure canvas content with zero metadata pollution
            file_path.write_text(c_content, encoding="utf-8")

            # 2. Sidecar metadata file
            meta_payload = {
                "id": c_id,
                "title": c_title,
                "chat_id": chat_id,
                "chat_title": title,
                "chat_url": url,
                "type": c_type,
                "updated": now_iso,
            }
            meta_path.write_text(json.dumps(meta_payload, indent=2, ensure_ascii=False), encoding="utf-8")

            con.execute(
                """INSERT INTO canvases(id, chat_id, title, content, type, file_path, updated)
                   VALUES(?,?,?,?,?,?,?)
                   ON CONFLICT(id) DO UPDATE SET chat_id=excluded.chat_id, title=excluded.title,
                   content=excluded.content, type=excluded.type, file_path=excluded.file_path,
                   updated=excluded.updated""",
                (c_id, chat_id, c_title, c_content, c_type, str(file_path), now_iso),
            )
            rel_canvas_path = file_path.relative_to(CANVASES_DIR).as_posix()
            changed_canvases.append((c_title, rel_canvas_path))

        if changed_canvases:
            if payload.get("is_manual"):
                for c_title, rel_canvas_path in changed_canvases:
                    cloud_sync.add_change(c_title, rel_path=rel_canvas_path)
                print(f"[canvas-sync] Manual sync requested: triggering immediate sync for {len(changed_canvases)} canvas(es)", flush=True)
                cloud_sync.trigger_immediate()
            else:
                for c_title, rel_canvas_path in changed_canvases:
                    cloud_sync.notify_change(c_title, rel_path=rel_canvas_path)

    con.commit()
    return True, chat_id
