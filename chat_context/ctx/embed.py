"""Chunking + local embeddings (fastembed / ONNX, runs offline after first model download)."""
import gc
import threading
import numpy as np

MODEL_NAME = "BAAI/bge-small-en-v1.5"
CHUNK_CHARS = 1500
MODEL_IDLE_SECONDS = 60.0

_model = None
_model_lock = threading.Lock()
_unload_timer = None


def unload_model():
    """Release the ONNX embedding model from RAM when idle."""
    global _model, _unload_timer
    with _model_lock:
        if _unload_timer is not None:
            _unload_timer.cancel()
            _unload_timer = None
        if _model is not None:
            _model = None
            gc.collect()


def _schedule_unload():
    global _unload_timer
    if _unload_timer is not None:
        _unload_timer.cancel()
    _unload_timer = threading.Timer(MODEL_IDLE_SECONDS, unload_model)
    _unload_timer.daemon = True
    _unload_timer.start()


def model():
    global _model
    with _model_lock:
        if _model is None:
            from fastembed import TextEmbedding
            # Limit worker threads to 2 to prevent ONNX Runtime from allocating
            # unbounded thread arenas across all 12 CPU cores (cuts memory from 5GB+ to <450MB)
            _model = TextEmbedding(model_name=MODEL_NAME, threads=2)
        _schedule_unload()
        return _model


def embed_texts(texts):
    if not texts:
        return np.zeros((0, 384), dtype=np.float32)
    # Constrain batch_size to 32 to cap ONNX intermediate tensor buffer allocations
    vecs = np.array(list(model().embed(texts, batch_size=32)), dtype=np.float32)
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    return vecs / np.clip(norms, 1e-9, None)


QUERY_PREFIX = "Represent this sentence for searching relevant passages: "


def embed_query(query: str):
    """Embed search query with asymmetric retrieval instruction for BGE model family."""
    q = (query or "").strip()
    if not q:
        return np.zeros((384,), dtype=np.float32)
    return embed_texts([f"{QUERY_PREFIX}{q}"])[0]


def chunk_messages(msgs, chat_title: str = ""):
    """msgs: list of (role, text). Returns list of chunk strings (<= ~CHUNK_CHARS) with context framing."""
    chunks, cur = [], ""
    title_prefix = f"[{chat_title}]\n" if chat_title and len(chat_title) < 120 else ""
    for role, text in msgs:
        block = f"[{role}] {text}"
        paras = block.split("\n\n")
        for p in paras:
            while len(p) > CHUNK_CHARS:
                if cur:
                    chunks.append(cur)
                    cur = ""
                chunks.append(p[:CHUNK_CHARS])
                p = p[CHUNK_CHARS:]
            if len(cur) + len(p) + 2 > CHUNK_CHARS and cur:
                chunks.append(cur)
                cur = ""
            cur = (cur + "\n\n" + p) if cur else (title_prefix + p if not chunks else p)
    if cur:
        chunks.append(cur)
    return chunks


def embed_pending(con, progress=None):
    """Chunk + embed every chat that has no embedding yet. Returns number of chats done."""
    rows = con.execute("SELECT id, title FROM chats WHERE emb IS NULL").fetchall()
    if progress is not None:
        progress.update(done=0, total=len(rows))
    embedded_count = 0
    for n, r in enumerate(rows):
        if progress is not None:
            progress["done"] = n
        cid = r["id"]
        title = r["title"] or ""
        msgs = con.execute(
            "SELECT role, text FROM messages WHERE chat_id=? ORDER BY idx", (cid,)
        ).fetchall()
        chunks = chunk_messages([(m["role"], m["text"]) for m in msgs], chat_title=title)
        if not chunks:
            # Mark empty chats with b"" so they are not continually re-selected
            con.execute("UPDATE chats SET emb=? WHERE id=?", (b"", cid))
            con.commit()
            continue
        vecs = embed_texts(chunks)
        con.execute("DELETE FROM chunks WHERE chat_id=?", (cid,))
        con.executemany(
            "INSERT INTO chunks(chat_id, idx, text, emb) VALUES(?,?,?,?)",
            [(cid, i, c, vecs[i].tobytes()) for i, c in enumerate(chunks)],
        )
        mean = vecs.mean(axis=0)
        mean = mean / max(np.linalg.norm(mean), 1e-9)
        con.execute("UPDATE chats SET emb=? WHERE id=?", (mean.astype(np.float32).tobytes(), cid))
        con.commit()
        embedded_count += 1
    if embedded_count > 0:
        con.execute("INSERT INTO chunks_fts(chunks_fts) VALUES('rebuild')")
        con.commit()
        gc.collect()
    return embedded_count


_vectors_cache = {"rev": None, "ids": [], "mat": None}
_vectors_lock = threading.Lock()


def invalidate_vectors_cache():
    global _vectors_cache
    with _vectors_lock:
        _vectors_cache = {"rev": None, "ids": [], "mat": None}


def load_chat_vectors(con, rev=None):
    global _vectors_cache
    with _vectors_lock:
        if rev is not None and _vectors_cache["rev"] == rev and _vectors_cache["mat"] is not None:
            return _vectors_cache["ids"], _vectors_cache["mat"]

        n = con.execute("SELECT count(*) FROM chats WHERE emb IS NOT NULL AND length(emb) == 1536").fetchone()[0]
        if not n:
            mat = np.zeros((0, 384), dtype=np.float32)
            ids = []
        else:
            ids = []
            mat = np.empty((n, 384), dtype=np.float32)
            cur = con.execute("SELECT id, emb FROM chats WHERE emb IS NOT NULL AND length(emb) == 1536")
            i = 0
            while True:
                batch = cur.fetchmany(500)
                if not batch:
                    break
                for r in batch:
                    if i >= n:
                        break
                    ids.append(r["id"])
                    mat[i] = np.frombuffer(r["emb"], dtype=np.float32)
                    i += 1
            if i < n:
                mat = mat[:i]

        if rev is not None:
            _vectors_cache = {"rev": rev, "ids": ids, "mat": mat}
        return ids, mat
