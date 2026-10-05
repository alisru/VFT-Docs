"""Chunking + local embeddings (fastembed / ONNX, runs offline after first model download)."""
import numpy as np

MODEL_NAME = "BAAI/bge-small-en-v1.5"
CHUNK_CHARS = 1500

_model = None


def model():
    global _model
    if _model is None:
        from fastembed import TextEmbedding
        _model = TextEmbedding(model_name=MODEL_NAME)
    return _model


def embed_texts(texts):
    if not texts:
        return np.zeros((0, 384), dtype=np.float32)
    vecs = np.array(list(model().embed(texts)), dtype=np.float32)
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    return vecs / np.clip(norms, 1e-9, None)


def chunk_messages(msgs):
    """msgs: list of (role, text). Returns list of chunk strings (<= ~CHUNK_CHARS)."""
    chunks, cur = [], ""
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
            cur = (cur + "\n\n" + p) if cur else p
    if cur:
        chunks.append(cur)
    return chunks


def embed_pending(con, progress=None):
    """Chunk + embed every chat that has no embedding yet. Returns number of chats done."""
    rows = con.execute("SELECT id FROM chats WHERE emb IS NULL").fetchall()
    if progress is not None:
        progress.update(done=0, total=len(rows))
    for n, r in enumerate(rows):
        if progress is not None:
            progress["done"] = n
        cid = r["id"]
        msgs = con.execute(
            "SELECT role, text FROM messages WHERE chat_id=? ORDER BY idx", (cid,)
        ).fetchall()
        chunks = chunk_messages([(m["role"], m["text"]) for m in msgs])
        if not chunks:
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
        print(f"[embed] {cid[:8]} {len(chunks)} chunks")
    return len(rows)


def load_chat_vectors(con):
    rows = con.execute("SELECT id, emb FROM chats WHERE emb IS NOT NULL").fetchall()
    ids = [r["id"] for r in rows]
    mat = (
        np.vstack([np.frombuffer(r["emb"], dtype=np.float32) for r in rows])
        if rows
        else np.zeros((0, 384), dtype=np.float32)
    )
    return ids, mat
