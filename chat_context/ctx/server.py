import datetime
import gc
import json
import re
import threading
import time
from collections import Counter
from pathlib import Path
from typing import Optional

import numpy as np
from fastapi import Body, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles

from .db import DRAFTS_DIR, ROOT, connect, init_db
from .embed import embed_pending, embed_texts, embed_query, load_chat_vectors
from .export import (
    chat_to_html,
    chat_to_markdown,
    chat_to_txt,
    export_chats_to_zip,
    fetch_all_chats,
    fetch_full_chat,
    sanitize_filename,
)
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


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)


def get_con():
    con = connect()
    try:
        yield con
    finally:
        con.close()


@app.get("/")
def index():
    return FileResponse(UI / "index.html")


@app.get("/api/tree")
def tree(con=Depends(get_con)):
    topics = [dict(r) for r in con.execute("SELECT id, name, user_named FROM topics ORDER BY name")]
    chats = [
        dict(r)
        for r in con.execute(
            """SELECT c.id, c.title, c.source, c.updated, c.n_msgs, c.topic_id, c.url,
                      (SELECT COUNT(*) FROM canvases cv WHERE cv.chat_id = c.id) as n_canvases
               FROM chats c
               ORDER BY COALESCE(c.updated, datetime(c.src_mtime, 'unixepoch'), c.started) DESC"""
        )
    ]
    by = {}
    for c in chats:
        by.setdefault(c["topic_id"], []).append(c)
    for t in topics:
        member_chats = by.get(t["id"], [])
        t["chats"] = member_chats
        t["count"] = len(member_chats)
        t["updated"] = member_chats[0]["updated"] if member_chats else ""
    unsorted_chats = by.get(None, [])
    unsorted_updated = unsorted_chats[0]["updated"] if unsorted_chats else ""
    return {
        "topics": [t for t in topics if t["chats"]],
        "unsorted": unsorted_chats,
        "unsorted_updated": unsorted_updated,
        "recent": chats[:30],
        "all": chats,
    }


@app.get("/api/chat/{cid}")
def chat(cid: str, con=Depends(get_con)):
    c = con.execute("SELECT id, title, source, started, updated, topic_id, url FROM chats WHERE id=?", (cid,)).fetchone()
    if not c:
        raise HTTPException(404)
    msgs = [dict(r) for r in con.execute("SELECT idx, role, ts, text FROM messages WHERE chat_id=? ORDER BY idx", (cid,))]
    canvases = [
        dict(r)
        for r in con.execute(
            "SELECT id, title, type, file_path, updated, content FROM canvases WHERE chat_id=? ORDER BY updated DESC",
            (cid,),
        )
    ]
    return {**dict(c), "messages": msgs, "canvases": canvases}


@app.get("/api/export/chat/{cid}")
def export_single_chat(cid: str, format: str = "markdown", con=Depends(get_con)):
    """Export a single conversation in Markdown, HTML, JSON, TXT, or ZIP format."""
    c = fetch_full_chat(con, cid)
    if not c:
        raise HTTPException(404, detail="Chat not found")

    fmt = format.lower()
    base_name = sanitize_filename(c.get("title") or c["id"], max_len=60)

    if fmt in ("md", "markdown"):
        content = chat_to_markdown(c)
        return Response(
            content=content,
            media_type="text/markdown; charset=utf-8",
            headers={"Content-Disposition": f'attachment; filename="{base_name}.md"'}
        )
    elif fmt == "html":
        content = chat_to_html(c)
        return Response(
            content=content,
            media_type="text/html; charset=utf-8",
            headers={"Content-Disposition": f'attachment; filename="{base_name}.html"'}
        )
    elif fmt == "json":
        content = json.dumps(c, ensure_ascii=False, indent=2)
        return Response(
            content=content,
            media_type="application/json; charset=utf-8",
            headers={"Content-Disposition": f'attachment; filename="{base_name}.json"'}
        )
    elif fmt in ("txt", "text"):
        content = chat_to_txt(c)
        return Response(
            content=content,
            media_type="text/plain; charset=utf-8",
            headers={"Content-Disposition": f'attachment; filename="{base_name}.txt"'}
        )
    elif fmt == "zip":
        zip_bytes = export_chats_to_zip([c], format_type="markdown", group_by_topic=False)
        return Response(
            content=zip_bytes,
            media_type="application/zip",
            headers={"Content-Disposition": f'attachment; filename="{base_name}.zip"'}
        )
    else:
        raise HTTPException(400, detail=f"Unsupported format: {format}")


@app.get("/api/export/all")
def export_all(
    format: str = "zip",
    group_by: str = "topic",
    ids: Optional[str] = None,
    con=Depends(get_con)
):
    """Export all conversations (or comma-separated list of IDs) as ZIP or JSON bundle."""
    chat_ids = [i.strip() for i in ids.split(",") if i.strip()] if ids else None
    chats = fetch_all_chats(con, chat_ids=chat_ids)
    if not chats:
        raise HTTPException(404, detail="No chats found to export")

    fmt = format.lower()
    now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    group_topic = (group_by.lower() != "flat")

    if fmt == "zip":
        zip_bytes = export_chats_to_zip(chats, format_type="markdown", group_by_topic=group_topic)
        prefix = "chat_context_selected" if chat_ids else "chat_context_all_chats"
        return Response(
            content=zip_bytes,
            media_type="application/zip",
            headers={"Content-Disposition": f'attachment; filename="{prefix}_{now_str}.zip"'}
        )
    elif fmt == "json":
        content = json.dumps(chats, ensure_ascii=False, indent=2)
        prefix = "chat_context_selected" if chat_ids else "chat_context_all_chats"
        return Response(
            content=content,
            media_type="application/json; charset=utf-8",
            headers={"Content-Disposition": f'attachment; filename="{prefix}_{now_str}.json"'}
        )
    else:
        raise HTTPException(400, detail=f"Bulk export only supports 'zip' or 'json' (got {format})")


@app.post("/api/export/selected")
def export_selected(body: dict = Body(...), con=Depends(get_con)):
    """Export an array of selected chat IDs as a ZIP or JSON bundle."""
    ids = body.get("ids") or []
    if not ids:
        raise HTTPException(400, detail="No chat IDs provided")
    chats = fetch_all_chats(con, chat_ids=ids)
    if not chats:
        raise HTTPException(404, detail="No matching chats found")

    fmt = (body.get("format") or "zip").lower()
    group_topic = (body.get("group_by") or "topic").lower() != "flat"
    now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    if fmt == "zip":
        zip_bytes = export_chats_to_zip(chats, format_type="markdown", group_by_topic=group_topic)
        return Response(
            content=zip_bytes,
            media_type="application/zip",
            headers={"Content-Disposition": f'attachment; filename="chat_context_selected_{now_str}.zip"'}
        )
    elif fmt == "json":
        content = json.dumps(chats, ensure_ascii=False, indent=2)
        return Response(
            content=content,
            media_type="application/json; charset=utf-8",
            headers={"Content-Disposition": f'attachment; filename="chat_context_selected_{now_str}.json"'}
        )
    else:
        raise HTTPException(400, detail=f"Unsupported format: {fmt}")


@app.post("/api/export/sync-git")
def api_sync_chats_git():
    """Trigger on-demand export and push of all chats to Git."""
    from .export import sync_chats_to_git
    res = sync_chats_to_git()
    if not res.get("ok"):
        raise HTTPException(status_code=500, detail=res.get("message"))
    return res


@app.post("/api/export/sync-gdrive")
def api_sync_chats_gdrive():
    """Trigger on-demand export and sync of all chats to Google Drive via rclone."""
    from .export import sync_chats_to_gdrive
    res = sync_chats_to_gdrive()
    if not res.get("ok"):
        raise HTTPException(status_code=500, detail=res.get("message"))
    return res


@app.post("/api/chat/censor")
def censor_chat(body: dict = Body(...), con=Depends(get_con)):
    """Censors a chat: deletes it completely from database & canvases, and blacklists it from future ingestion."""
    chat_id = body.get("chat_id")
    url = body.get("url") or ""
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # If chat_id not provided, try resolving from url
    if not chat_id and url:
        row = con.execute("SELECT id FROM chats WHERE url=?", (url,)).fetchone()
        if row:
            chat_id = row["id"]

    if not chat_id and not url:
        raise HTTPException(400, detail="Must provide chat_id or url to censor")

    # 1. Fetch canvas file paths to delete physical markdown files
    if chat_id:
        canvas_rows = con.execute("SELECT file_path FROM canvases WHERE chat_id=?", (chat_id,)).fetchall()
        for cr in canvas_rows:
            fp = cr["file_path"]
            if fp:
                try:
                    p = Path(fp)
                    if p.exists():
                        p.unlink()
                    meta_p = p.with_name(p.stem + ".meta.json")
                    if meta_p.exists():
                        meta_p.unlink()
                except Exception:
                    pass

        # 2. Delete all records from database tables
        con.execute("DELETE FROM canvases WHERE chat_id=?", (chat_id,))
        con.execute("DELETE FROM messages WHERE chat_id=?", (chat_id,))
        con.execute("DELETE FROM chunks WHERE chat_id=?", (chat_id,))
        con.execute("DELETE FROM chats WHERE id=?", (chat_id,))

    # 3. Add to censored_chats blacklist
    resolved_id = chat_id or f"censored-{hashlib.sha1(url.encode()).hexdigest()[:16]}"
    con.execute(
        """INSERT INTO censored_chats(chat_id, url, created_at)
           VALUES(?,?,?)
           ON CONFLICT(chat_id) DO UPDATE SET url=COALESCE(excluded.url, censored_chats.url)""",
        (resolved_id, url, now_iso)
    )
    con.commit()
    _bump_rev()
    return {"ok": True, "chat_id": resolved_id, "censored": True}


@app.get("/api/chat/is-censored")
def check_is_censored(chat_id: Optional[str] = None, url: Optional[str] = None, con=Depends(get_con)):
    """Check if a chat or URL is currently censored."""
    if not chat_id and not url:
        return {"censored": False}
    row = con.execute(
        "SELECT 1 FROM censored_chats WHERE (chat_id IS NOT NULL AND chat_id=?) OR (url IS NOT NULL AND url != '' AND url=?) LIMIT 1",
        (chat_id or "", url or "")
    ).fetchone()
    return {"censored": bool(row)}


@app.get("/api/canvas/{canvas_id}")
def canvas_detail(canvas_id: str, con=Depends(get_con)):
    row = con.execute("SELECT id, chat_id, title, content, type, file_path, updated FROM canvases WHERE id=?", (canvas_id,)).fetchone()
    if not row:
        raise HTTPException(404)
    return dict(row)


@app.get("/api/canvases/recent")
def recent_canvases(k: int = 30, con=Depends(get_con)):
    rows = con.execute(
        """SELECT cv.id, cv.chat_id, cv.title, cv.type, cv.file_path, cv.updated,
                  SUBSTR(cv.content, 1, 300) as preview,
                  c.title as chat_title
           FROM canvases cv
           LEFT JOIN chats c ON cv.chat_id = c.id
           ORDER BY cv.updated DESC LIMIT ?""",
        (k,),
    ).fetchall()
    return [dict(r) for r in rows]


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
def related(cid: str, k: int = 8, con=Depends(get_con)):
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


@app.post("/api/related_live")
def related_live(body: dict = Body(...), con=Depends(get_con)):
    """Find related chats for a given chat_id, url, or free-text query from Gemini."""
    cid = body.get("chat_id")
    url = body.get("url")
    text = (body.get("text") or "").strip()
    k = int(body.get("k", 8))

    # Resolve chat_id if only url is provided
    if not cid and url:
        r = con.execute("SELECT id FROM chats WHERE url=?", (url,)).fetchone()
        if r:
            cid = r["id"]

    ids, mat = load_chat_vectors(con)

    # 1. If we have a recognized chat in our vectors, use standard chat vector similarity
    if cid and cid in ids and len(mat):
        sims = mat @ mat[ids.index(cid)]
        mine = _chunks(con, cid)
        out = []
        for i in np.argsort(-sims):
            if ids[i] == cid:
                continue
            row = con.execute("SELECT id, title, updated FROM chats WHERE id=?", (ids[i],)).fetchone()
            if not row:
                continue
            out.append({**dict(row), "score": round(float(sims[i]), 3), "why": _why(mine, _chunks(con, ids[i]))})
            if len(out) >= k:
                break
        if out:
            return out

    # 2. Otherwise, if text or title was passed (or extracted from chat), embed and search
    if text and len(mat):
        qv = embed_texts([text[:1000]])[0]
        sims = mat @ qv
        out = []
        for i in np.argsort(-sims):
            if cid and ids[i] == cid:
                continue
            row = con.execute("SELECT id, title, updated FROM chats WHERE id=?", (ids[i],)).fetchone()
            if not row:
                continue
            # Get closest chunk as explanation
            chunks_other = _chunks(con, ids[i])
            best_chunk = ""
            if len(chunks_other[1]):
                sim_c = chunks_other[1] @ qv
                best_chunk = chunks_other[0][int(np.argmax(sim_c))][:300]
            out.append({
                **dict(row),
                "score": round(float(sims[i]), 3),
                "why": {"shared": [], "match": round(float(sims[i]), 3), "this": text[:200], "other": best_chunk}
            })
            if len(out) >= k:
                break
        if out:
            return out

    # 3. Fallback to recent chats if no matches or no text
    recent = con.execute("SELECT id, title, updated FROM chats ORDER BY updated DESC LIMIT ?", (k,)).fetchall()
    return [{"id": r["id"], "title": r["title"], "updated": r["updated"], "score": 0.0, "why": None} for r in recent if r["id"] != cid]


_chunks_cache = {"rev": None, "mat": None, "meta": []}


def _get_chunk_index(con):
    global _chunks_cache
    current_rev = STATUS.get("rev", 1)
    if _chunks_cache["rev"] == current_rev and _chunks_cache["mat"] is not None:
        return _chunks_cache["mat"], _chunks_cache["meta"]

    # Single fast joined query with topics and source metadata
    sql = """
        SELECT k.id, k.chat_id, k.idx, k.text, k.emb, c.title, c.source, c.topic_id, t.name as topic_name,
               COALESCE(c.updated, datetime(c.src_mtime, 'unixepoch'), c.started, '') as updated
        FROM chunks k
        JOIN chats c ON k.chat_id = c.id
        LEFT JOIN topics t ON c.topic_id = t.id
        WHERE k.emb IS NOT NULL AND length(k.emb) == 1536
    """
    rows = con.execute(sql).fetchall()
    if not rows:
        _chunks_cache = {"rev": current_rev, "mat": None, "meta": []}
        return None, []

    mat = np.vstack([np.frombuffer(r["emb"], dtype=np.float32) for r in rows])
    meta = [
        {
            "id": r["id"],
            "chat_id": r["chat_id"],
            "idx": r["idx"],
            "text": r["text"],
            "title": r["title"] or r["chat_id"],
            "source": r["source"] or "gemini",
            "topic_id": r["topic_id"],
            "topic_name": r["topic_name"] or "",
            "updated": r["updated"],
        }
        for r in rows
    ]
    _chunks_cache = {"rev": current_rev, "mat": mat, "meta": meta}
    return mat, meta


def _search(
    con,
    q: str,
    k: int = 25,
    sort: str = "relevance",
    mode: str = "hybrid",
    group_by: str = "chat",
    must_contain: str = "",
    min_score: float = 0.0,
    topic_id: int = None,
    source: str = None,
    chat_ids=None,
):
    q = (q or "").strip()
    if not q:
        return []

    # Parse quoted terms in query as mandatory: e.g. "god" "goal" -> must_contain
    quoted = re.findall(r'"([^"]+)"', q)
    clean_q = re.sub(r'"[^"]+"', ' ', q).strip() or q
    must_list = list(quoted)
    if must_contain:
        must_list.extend([w.strip() for w in re.split(r'[,; ]+', must_contain) if w.strip()])
    must_words = [w.lower() for w in must_list if len(w) > 1]

    # Asymmetric BGE query embedding
    qv = embed_query(clean_q)
    mat, meta = _get_chunk_index(con)
    if mat is None or len(meta) == 0:
        return []

    # FTS5 matches
    clean_tokens = [w for w in re.findall(r"[a-zA-Z0-9]+", q.lower()) if len(w) > 2]
    fts_dict = {}
    if clean_tokens and mode in ("hybrid", "exact"):
        fts_query = " OR ".join(clean_tokens)
        try:
            fts_rows = con.execute(
                "SELECT rowid, bm25(chunks_fts) as rank FROM chunks_fts WHERE chunks_fts MATCH ? LIMIT 1000",
                (fts_query,)
            ).fetchall()
            fts_dict = {r[0]: r[1] for r in fts_rows}
        except Exception:
            pass

    # Filtering mask
    allowed_cids = set(chat_ids) if chat_ids else None

    # Dense vector dot products across all chunks in memory (<1ms)
    sims = mat @ qv

    candidates = []
    for i, m in enumerate(meta):
        # 1. Filters
        if allowed_cids and m["chat_id"] not in allowed_cids:
            continue
        if topic_id is not None and m["topic_id"] != topic_id:
            continue
        if source and m["source"].lower() != source.lower():
            continue

        t_lower = (m["text"] + " " + m["title"]).lower()
        if must_words and not all(w in t_lower for w in must_words):
            continue

        sim = float(sims[i])
        bm = fts_dict.get(m["id"])

        if mode == "exact":
            if bm is None:
                continue
            final_score = max(0.0, 1.0 / (1.0 + abs(bm)))
        elif mode == "semantic":
            final_score = sim
        else:  # hybrid
            bm_score = max(0.0, 1.0 / (1.0 + abs(bm))) if bm is not None else 0.0
            token_hits = sum(1 for w in clean_tokens if w in t_lower)
            token_ratio = token_hits / max(len(clean_tokens), 1)
            # 65% dense semantic similarity + 20% BM25 keyword score + 15% token presence
            final_score = (sim * 0.65) + (bm_score * 0.20) + (token_ratio * 0.15)
            # Bonus if all search terms appear
            if token_ratio == 1.0 and len(clean_tokens) >= 2:
                final_score += 0.08

        final_score = round(final_score, 3)
        if min_score > 0 and final_score < min_score:
            continue

        candidates.append({
            "id": m["id"],
            "chat_id": m["chat_id"],
            "title": m["title"],
            "idx": m["idx"],
            "text": m["text"],
            "updated": m["updated"],
            "source": m["source"],
            "topic_id": m["topic_id"],
            "topic_name": m["topic_name"],
            "score": final_score,
            "sim": round(sim, 3),
            "has_fts": bm is not None,
        })

    if group_by == "chat":
        # Group candidates by conversation
        chats_map = {}
        for c in candidates:
            cid = c["chat_id"]
            if cid not in chats_map:
                chats_map[cid] = {
                    "chat_id": cid,
                    "title": c["title"],
                    "updated": c["updated"],
                    "source": c["source"],
                    "topic_id": c["topic_id"],
                    "topic_name": c["topic_name"],
                    "best_chunk": c,
                    "matching_chunks": 1,
                    "max_score": c["score"],
                }
            else:
                chats_map[cid]["matching_chunks"] += 1
                if c["score"] > chats_map[cid]["max_score"]:
                    chats_map[cid]["max_score"] = c["score"]
                    chats_map[cid]["best_chunk"] = c

        chat_results = []
        for cid, data in chats_map.items():
            best = data["best_chunk"]
            # Small boost for multiple matching passages in the same chat
            multi_boost = min(0.04, (data["matching_chunks"] - 1) * 0.01)
            final_score = round(min(1.0, data["max_score"] + multi_boost), 3)
            chat_results.append({
                "chat_id": cid,
                "title": data["title"],
                "text": best["text"],
                "idx": best["idx"],
                "updated": data["updated"],
                "source": data["source"],
                "topic_id": data["topic_id"],
                "topic_name": data["topic_name"],
                "score": final_score,
                "matching_chunks": data["matching_chunks"],
            })

        if sort == "recent":
            chat_results.sort(key=lambda x: (x["updated"] or "", x["score"]), reverse=True)
        else:
            chat_results.sort(key=lambda x: x["score"], reverse=True)
        return chat_results[:k]
    else:
        if sort == "recent":
            candidates.sort(key=lambda x: (x["updated"] or "", x["score"]), reverse=True)
        else:
            candidates.sort(key=lambda x: x["score"], reverse=True)
        return candidates[:k]


@app.get("/api/search")
def search(
    q: str,
    k: int = 25,
    sort: str = "relevance",
    mode: str = "hybrid",
    group_by: str = "chat",
    must_contain: str = "",
    min_score: float = 0.0,
    topic_id: int = None,
    source: str = None,
    con=Depends(get_con),
):
    return _search(
        con,
        q,
        k=k,
        sort=sort,
        mode=mode,
        group_by=group_by,
        must_contain=must_contain,
        min_score=min_score,
        topic_id=topic_id,
        source=source,
    )


@app.get("/api/topics")
def list_topics(con=Depends(get_con)):
    rows = con.execute("""
        SELECT t.id, t.name, count(c.id) as count
        FROM topics t
        LEFT JOIN chats c ON t.id = c.topic_id
        GROUP BY t.id
        HAVING count > 0
        ORDER BY count DESC, t.name ASC
    """).fetchall()
    return [dict(r) for r in rows]


@app.get("/api/sources")
def list_sources(con=Depends(get_con)):
    rows = con.execute("SELECT DISTINCT source FROM chats WHERE source IS NOT NULL ORDER BY source").fetchall()
    return [r[0] for r in rows]



@app.post("/api/pack")
def pack(body: dict = Body(...), con=Depends(get_con)):
    """Build a paste-ready context pack.
    body: {query?: str, chat_ids?: [..], topic_id?: int, max_chars?: int}"""
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
def rename(body: dict = Body(...), con=Depends(get_con)):
    con.execute("UPDATE topics SET name=?, user_named=1 WHERE id=?", (body["name"], body["id"]))
    con.commit()
    return {"ok": True}


@app.post("/api/chat/move")
def move(body: dict = Body(...), con=Depends(get_con)):
    tid = body.get("topic_id")
    if tid is None and body.get("new_topic"):
        tid = con.execute("INSERT INTO topics(name, user_named) VALUES(?,1)", (body["new_topic"],)).lastrowid
    con.execute("UPDATE chats SET topic_id=?, topic_locked=1 WHERE id=?", (tid, body["chat_id"]))
    con.commit()
    return {"ok": True, "topic_id": tid}


STATUS = {"state": "idle", "done": 0, "total": 0, "last": None, "error": None, "rev": 1}
_wake = threading.Event()
_threshold = 0.80
AUTO_SECONDS = 120


def _bump_rev():
    STATUS["rev"] = STATUS.get("rev", 1) + 1


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
        if new or embedded:
            _bump_rev()
    except Exception as e:  # log and keep the worker alive
        STATUS["error"] = str(e)
        print(f"[sync error] {e}")
    finally:
        con.close()
        STATUS["state"] = "idle"
        gc.collect()


_last_run = 0.0
_MIN_INTERVAL = 30.0  # minimum seconds between background ingests
_force_now = threading.Event()


def _worker():
    global _last_run
    while True:
        _run_once()
        _last_run = time.time()
        # Wait up to AUTO_SECONDS or until woken by sync trigger
        _wake.wait(AUTO_SECONDS)
        _wake.clear()
        
        # If triggered manually via force_now, bypass the minimum interval delay
        if _force_now.is_set():
            _force_now.clear()
        else:
            elapsed = time.time() - _last_run
            if elapsed < _MIN_INTERVAL:
                time.sleep(_MIN_INTERVAL - elapsed)


@app.on_event("startup")
def _start_worker():
    init_db()
    threading.Thread(target=_worker, daemon=True).start()


@app.get("/api/status")
def status():
    return STATUS


@app.post("/api/ingest/chat")
def ingest_chat(payload: dict = Body(...), con=Depends(get_con)):
    """Accepts JSON chat payload from browser extension or userscript."""
    ok, res = ingest_payload(con, payload)
    if not ok:
        raise HTTPException(400, detail=str(res))
    _bump_rev()
    _wake.set()
    return {"ok": True, "chat_id": res}


@app.post("/api/sync")
def sync(threshold: float = 0.80):
    global _threshold
    _threshold = threshold
    _force_now.set()
    _wake.set()
    # Trigger cloud canvas sync immediately without 30s delay
    try:
        from .cloud_sync import cloud_sync
        cloud_sync.trigger_immediate()
    except Exception:
        pass
    return {"queued": True}


def find_available_port(start_port: int = 8767, max_tries: int = 20) -> int:
    """Scans for an available TCP port on localhost starting at start_port."""
    import socket
    for port in range(start_port, start_port + max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return start_port


if __name__ == "__main__":
    import uvicorn
    import webbrowser

    port = find_available_port(start_port=8767, max_tries=20)
    print(f"\n[chat_context] Server starting on http://127.0.0.1:{port}")

    # Write active port to file so local launchers, scripts, and extension can read it
    port_file = ROOT / "data" / "server_port.txt"
    try:
        port_file.parent.mkdir(parents=True, exist_ok=True)
        port_file.write_text(str(port), encoding="utf-8")
    except Exception:
        pass

    # Open dashboard in default browser automatically on start
    threading.Thread(target=lambda: (time.sleep(1.2), webbrowser.open(f"http://127.0.0.1:{port}")), daemon=True).start()

    uvicorn.run(app, host="127.0.0.1", port=port)
