"""FastAPI server: dashboard API + static UI. Run: python -m ctx.server  (from chat_context/)"""
import threading
from collections import Counter
from pathlib import Path

import numpy as np
from fastapi import Body, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse

from .db import ROOT, connect
from .embed import embed_pending, embed_texts, load_chat_vectors
from .ingest import (
    AI_LOGS_DIR,
    INBOX,
    ingest_antigravity,
    ingest_folder,
    ingest_payload,
)
from .topics import _words, recluster

app = FastAPI(title="Chat Context")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
UI = ROOT / "ui"


def _con():
    return connect()


@app.get("/")
def index():
    return FileResponse(UI / "index.html")


@app.get("/api/tree")
def tree():
    con = _con()
    topics = [dict(r) for r in con.execute("SELECT id, name, user_named FROM topics ORDER BY name")]
    chats = [
        dict(r)
        for r in con.execute(
            """SELECT id, title, source, updated, n_msgs, topic_id, url 
               FROM chats 
               ORDER BY COALESCE(updated, datetime(src_mtime, 'unixepoch'), started) DESC"""
        )
    ]
    by = {}
    for c in chats:
        by.setdefault(c["topic_id"], []).append(c)
    for t in topics:
        t["chats"] = by.get(t["id"], [])
    return {"topics": [t for t in topics if t["chats"]], "unsorted": by.get(None, []), "recent": chats[:30], "all": chats}


@app.get("/api/chat/{cid}")
def chat(cid: str):
    con = _con()
    c = con.execute("SELECT id, title, source, started, updated, topic_id, url FROM chats WHERE id=?", (cid,)).fetchone()
    if not c:
        raise HTTPException(404)
    msgs = [dict(r) for r in con.execute("SELECT idx, role, ts, text FROM messages WHERE chat_id=? ORDER BY idx", (cid,))]
    return {**dict(c), "messages": msgs}


def _chunks(con, cid):
    rows = con.execute("SELECT text, emb FROM chunks WHERE chat_id=? ORDER BY idx", (cid,)).fetchall()
    if not rows:
        return [], np.zeros((0, 384), dtype=np.float32)
    return [r["text"] for r in rows], np.vstack([np.frombuffer(r["emb"], dtype=np.float32) for r in rows])


def _why(a_chunks, b_chunks):
    """Closest passage pair between two chats + the words both passages share."""
    (at, av), (bt, bv) = a_chunks, b_chunks
    if not len(av) or not len(bv):
        return None
    sim = av @ bv.T
    i, j = np.unravel_index(int(np.argmax(sim)), sim.shape)
    wa, wb = Counter(_words(at[i])), Counter(_words(bt[j]))
    shared = sorted(set(wa) & set(wb), key=lambda w: wa[w] + wb[w], reverse=True)[:5]
    return {
        "shared": shared,
        "match": round(float(sim[i, j]), 3),
        "this": at[i][:300],
        "other": bt[j][:300],
    }


@app.get("/api/related/{cid}")
def related(cid: str, k: int = 8):
    con = _con()
    ids, mat = load_chat_vectors(con)
    if cid not in ids:
        return []
    sims = mat @ mat[ids.index(cid)]
    mine = _chunks(con, cid)
    out = []
    for i in np.argsort(-sims):
        if ids[i] == cid:
            continue
        r = con.execute("SELECT id, title, updated FROM chats WHERE id=?", (ids[i],)).fetchone()
        out.append({**dict(r), "score": round(float(sims[i]), 3), "why": _why(mine, _chunks(con, ids[i]))})
        if len(out) >= k:
            break
    return out


def _search(con, q, k=12, chat_ids=None):
    qv = embed_texts([q])[0]
    sql = "SELECT id, chat_id, idx, text, emb FROM chunks"
    rows = con.execute(sql).fetchall()
    if chat_ids:
        s = set(chat_ids)
        rows = [r for r in rows if r["chat_id"] in s]
    if not rows:
        return []
    mat = np.vstack([np.frombuffer(r["emb"], dtype=np.float32) for r in rows])
    sims = mat @ qv
    top = np.argsort(-sims)[:k]
    titles = {r["id"]: r["title"] for r in con.execute("SELECT id, title FROM chats")}
    return [
        {
            "chat_id": rows[i]["chat_id"],
            "title": titles.get(rows[i]["chat_id"]),
            "idx": rows[i]["idx"],
            "text": rows[i]["text"],
            "score": round(float(sims[i]), 3),
        }
        for i in top
    ]


@app.get("/api/search")
def search(q: str, k: int = 12):
    return _search(_con(), q, k)


@app.post("/api/pack")
def pack(body: dict = Body(...)):
    """Build a paste-ready context pack.
    body: {query?: str, chat_ids?: [..], topic_id?: int, max_chars?: int}"""
    con = _con()
    max_chars = int(body.get("max_chars", 12000))
    ids = body.get("chat_ids") or []
    if body.get("topic_id"):
        ids += [r["id"] for r in con.execute("SELECT id FROM chats WHERE topic_id=?", (body["topic_id"],))]
    q = (body.get("query") or "").strip()
    parts, used = [], 0
    header = "Context from my previous chats (use as background; ask if anything is unclear):\n"
    if q:
        hits = _search(con, q, k=40, chat_ids=ids or None)
        for h in hits:
            block = f"--- {h['title']} (chat {h['chat_id'][:8]}, relevance {h['score']}) ---\n{h['text']}\n"
            if used + len(block) > max_chars:
                break
            parts.append(block)
            used += len(block)
    else:
        for cid in ids:
            c = con.execute("SELECT title, started FROM chats WHERE id=?", (cid,)).fetchone()
            if not c:
                continue
            msgs = con.execute("SELECT role, text FROM messages WHERE chat_id=? ORDER BY idx", (cid,)).fetchall()
            block = f"=== {c['title']} ({(c['started'] or '')[:10]}) ===\n" + "\n\n".join(
                f"[{m['role']}] {m['text']}" for m in msgs
            ) + "\n"
            budget = max_chars - used
            if budget <= 200:
                break
            parts.append(block[:budget])
            used += min(len(block), budget)
    return PlainTextResponse(header + "\n".join(parts))


@app.post("/api/topic/rename")
def rename(body: dict = Body(...)):
    con = _con()
    con.execute("UPDATE topics SET name=?, user_named=1 WHERE id=?", (body["name"], body["id"]))
    con.commit()
    return {"ok": True}


@app.post("/api/chat/move")
def move(body: dict = Body(...)):
    con = _con()
    tid = body.get("topic_id")
    if tid is None and body.get("new_topic"):
        tid = con.execute("INSERT INTO topics(name, user_named) VALUES(?,1)", (body["new_topic"],)).lastrowid
    con.execute("UPDATE chats SET topic_id=?, topic_locked=1 WHERE id=?", (tid, body["chat_id"]))
    con.commit()
    return {"ok": True, "topic_id": tid}


STATUS = {"state": "idle", "done": 0, "total": 0, "last": None, "error": None}
_wake = threading.Event()
_threshold = 0.80
AUTO_SECONDS = 120


def _run_once():
    STATUS.update(state="ingesting", done=0, total=0, error=None)
    con = connect()
    try:
        new_ag, skip_ag, fail_ag = ingest_antigravity(con)
        new_ai, skip_ai, fail_ai = ingest_folder(con, AI_LOGS_DIR)
        new_gchat, skip_gchat, fail_gchat = ingest_folder(con, AI_LOGS_DIR / "google_chat_log")
        INBOX.mkdir(parents=True, exist_ok=True)
        new_inbox, skip_inbox, fail_inbox = ingest_folder(con, INBOX)

        new = new_ag + new_ai + new_gchat + new_inbox
        skip = skip_ag + skip_ai + skip_gchat + skip_inbox
        fail = fail_ag + fail_ai + fail_gchat + fail_inbox

        STATUS["state"] = "embedding"
        embedded = embed_pending(con, STATUS)
        if new or embedded or not con.execute("SELECT 1 FROM topics LIMIT 1").fetchone():
            STATUS["state"] = "grouping"
            recluster(con, _threshold)
        STATUS["last"] = {"new": new, "unchanged": skip, "failed": fail, "embedded": embedded}
    except Exception as e:  # log and keep the worker alive
        STATUS["error"] = str(e)
        print(f"[sync error] {e}")
    finally:
        con.close()
        STATUS["state"] = "idle"


def _worker():
    while True:
        _run_once()
        _wake.wait(AUTO_SECONDS)
        _wake.clear()


@app.on_event("startup")
def _start_worker():
    threading.Thread(target=_worker, daemon=True).start()


@app.get("/api/status")
def status():
    return STATUS


@app.post("/api/ingest/chat")
def ingest_chat(payload: dict = Body(...)):
    """Accepts JSON chat payload from browser extension or userscript."""
    con = _con()
    ok, res = ingest_payload(con, payload)
    if not ok:
        raise HTTPException(400, detail=str(res))
    _wake.set()
    return {"ok": True, "chat_id": res}


@app.post("/api/sync")
def sync(threshold: float = 0.80):
    global _threshold
    _threshold = threshold
    _wake.set()
    return {"queued": True}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8765)
