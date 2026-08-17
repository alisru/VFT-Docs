"""memory_store.py — Local SQLite + FTS5 Memory Engine for Aletheia Bot & VFT Archive.

Provides fast, zero-dependency structured memory storage, observation tagging, and
full-text indexing over the 170+ Gemini & Claude discussion transcripts in '_AI files and chat logs/'.
"""
import os
import sys
import glob
import json
import sqlite3
import hashlib
import datetime
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(script_dir)
DB_PATH = os.path.join(script_dir, "memory_store.sqlite")
AI_LOGS_DIR = os.path.join(workspace_dir, "_AI files and chat logs")


def get_db_connection():
    """Create a SQLite connection with WAL mode enabled for high concurrent throughput."""
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA synchronous = NORMAL")
    return conn


def init_database():
    """Initialize tables and FTS5 virtual indices."""
    conn = get_db_connection()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                category TEXT NOT NULL,
                content TEXT NOT NULL,
                tags TEXT,
                coords_u REAL,
                coords_psi REAL,
                session_id TEXT,
                thread_id TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS archive_documents (
                id TEXT PRIMARY KEY,
                filename TEXT UNIQUE,
                filepath TEXT,
                file_hash TEXT,
                chunk_count INTEGER,
                mtime REAL,
                created_at TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS archive_chunks (
                id TEXT PRIMARY KEY,
                doc_id TEXT,
                filename TEXT,
                chunk_index INTEGER,
                content TEXT,
                tokens_est INTEGER,
                FOREIGN KEY (doc_id) REFERENCES archive_documents(id) ON DELETE CASCADE
            )
        """)

        # FTS5 Virtual Tables
        conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS fts_archive USING fts5(
                filename,
                content,
                tokenize = 'porter unicode61'
            )
        """)

        conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS fts_memories USING fts5(
                category,
                content,
                tags,
                tokenize = 'porter unicode61'
            )
        """)
    conn.close()


def _chunk_text(text, target_words=400, overlap_words=50):
    """Chunk text cleanly on paragraph boundaries preserving structure."""
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = []
    current_word_count = 0

    for para in paragraphs:
        p_clean = para.strip()
        if not p_clean:
            continue
        words = p_clean.split()
        p_word_count = len(words)

        if current_word_count + p_word_count > target_words and current_chunk:
            chunk_str = "\n\n".join(current_chunk)
            chunks.append(chunk_str)
            # Keep last paragraph for overlap
            current_chunk = [current_chunk[-1], p_clean] if len(current_chunk) > 1 else [p_clean]
            current_word_count = sum(len(p.split()) for p in current_chunk)
        else:
            current_chunk.append(p_clean)
            current_word_count += p_word_count

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks if chunks else [text]


def index_ai_chat_logs(logs_dir=None):
    """Scan and index all .md and .txt files in '_AI files and chat logs/'."""
    if logs_dir is None:
        logs_dir = AI_LOGS_DIR

    if not os.path.exists(logs_dir):
        return {"status": "error", "message": f"Directory not found: {logs_dir}"}

    init_database()
    conn = get_db_connection()

    indexed_count = 0
    skipped_count = 0
    total_chunks = 0

    # Match .md and .txt files
    files = glob.glob(os.path.join(logs_dir, "*.md")) + glob.glob(os.path.join(logs_dir, "*.txt"))

    for filepath in files:
        filename = os.path.basename(filepath)
        try:
            mtime = os.path.getmtime(filepath)
            # Check existing document
            cur = conn.cursor()
            cur.execute("SELECT file_hash, mtime FROM archive_documents WHERE filename = ?", (filename,))
            row = cur.fetchone()

            # Read file
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(filepath, "r", encoding="latin-1") as f:
                    content = f.read()

            file_hash = hashlib.md5(content.encode("utf-8")).hexdigest()

            if row and row["mtime"] == mtime and row["file_hash"] == file_hash:
                skipped_count += 1
                continue

            doc_id = f"doc_{hashlib.sha256(filename.encode('utf-8')).hexdigest()[:12]}"
            chunks = _chunk_text(content, target_words=400, overlap_words=50)

            with conn:
                # Clear old records if re-indexing
                conn.execute("DELETE FROM archive_chunks WHERE doc_id = ?", (doc_id,))
                conn.execute("DELETE FROM fts_archive WHERE filename = ?", (filename,))
                conn.execute("DELETE FROM archive_documents WHERE filename = ?", (filename,))

                # Insert document
                now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
                conn.execute("""
                    INSERT INTO archive_documents (id, filename, filepath, file_hash, chunk_count, mtime, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (doc_id, filename, filepath, file_hash, len(chunks), mtime, now_str))

                # Insert chunks and FTS
                for idx, ch in enumerate(chunks):
                    chunk_id = f"{doc_id}_{idx}"
                    tokens_est = len(ch.split())
                    conn.execute("""
                        INSERT INTO archive_chunks (id, doc_id, filename, chunk_index, content, tokens_est)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (chunk_id, doc_id, filename, idx, ch, tokens_est))

                    conn.execute("""
                        INSERT INTO fts_archive (rowid, filename, content)
                        VALUES (NULL, ?, ?)
                    """, (filename, ch))

            indexed_count += 1
            total_chunks += len(chunks)

        except Exception as e:
            print(f"[Memory Store] Error indexing {filename}: {e}", file=sys.stderr)

    conn.close()
    return {
        "status": "ok",
        "indexed_files": indexed_count,
        "skipped_files": skipped_count,
        "new_chunks": total_chunks,
        "total_scanned": len(files)
    }


def search_archive_logs(query, limit=5):
    """Search indexed AI discussion transcripts using FTS5 with BM25 ranking."""
    init_database()
    conn = get_db_connection()
    clean_q = re.sub(r'[^\w\s]', ' ', query).strip()
    if not clean_q:
        return []

    words = clean_q.split()
    fts_query = " OR ".join(f'"{w}"*' for w in words if len(w) > 1)
    if not fts_query:
        fts_query = f'"{clean_q}"'

    results = []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT filename, snippet(fts_archive, 1, '<b>', '</b>', '...', 40) as snippet,
                   content, rank
            FROM fts_archive
            WHERE fts_archive MATCH ?
            ORDER BY rank
            LIMIT ?
        """, (fts_query, limit))

        for row in cur.fetchall():
            results.append({
                "filename": row["filename"],
                "snippet": row["snippet"],
                "content": row["content"][:600] + ("..." if len(row["content"]) > 600 else ""),
                "rank": round(float(row["rank"]), 4)
            })
    except Exception as e:
        print(f"[Memory Store] FTS search error: {e}", file=sys.stderr)
    finally:
        conn.close()

    return results


def create_memory(content, category="observation", tags=None, coords_u=None, coords_psi=None, session_id=None, thread_id=None):
    """Save a structured memory observation to the SQLite memory store."""
    init_database()
    conn = get_db_connection()
    mem_id = f"mem_{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d%H%M%S')}_{hashlib.md5(content.encode('utf-8')).hexdigest()[:6]}"
    now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
    tags_str = ", ".join(tags) if isinstance(tags, list) else (tags or "")

    with conn:
        conn.execute("""
            INSERT INTO memories (id, category, content, tags, coords_u, coords_psi, session_id, thread_id, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (mem_id, category, content, tags_str, coords_u, coords_psi, session_id, thread_id, now_str, now_str))

        conn.execute("""
            INSERT INTO fts_memories (rowid, category, content, tags)
            VALUES (NULL, ?, ?, ?)
        """, (category, content, tags_str))

    conn.close()
    return {"id": mem_id, "status": "saved"}


def search_memories(query, category=None, limit=5):
    """Search stored memories using FTS5."""
    init_database()
    conn = get_db_connection()
    clean_q = re.sub(r'[^\w\s]', ' ', query).strip()
    if not clean_q:
        return []

    words = clean_q.split()
    fts_query = " OR ".join(f'"{w}"*' for w in words if len(w) > 1)
    if not fts_query:
        fts_query = f'"{clean_q}"'

    results = []
    try:
        cur = conn.cursor()
        if category:
            cur.execute("""
                SELECT m.id, m.category, m.content, m.tags, m.coords_u, m.coords_psi, m.session_id, m.thread_id, m.created_at
                FROM memories m
                JOIN fts_memories f ON m.content = f.content
                WHERE fts_memories MATCH ? AND m.category = ?
                LIMIT ?
            """, (fts_query, category, limit))
        else:
            cur.execute("""
                SELECT m.id, m.category, m.content, m.tags, m.coords_u, m.coords_psi, m.session_id, m.thread_id, m.created_at
                FROM memories m
                JOIN fts_memories f ON m.content = f.content
                WHERE fts_memories MATCH ?
                LIMIT ?
            """, (fts_query, limit))

        for row in cur.fetchall():
            results.append({
                "id": row["id"],
                "category": row["category"],
                "content": row["content"],
                "tags": row["tags"],
                "coords": f"({row['coords_u']}, {row['coords_psi']})" if row["coords_u"] is not None else None,
                "session_id": row["session_id"],
                "thread_id": row["thread_id"],
                "created_at": row["created_at"]
            })
    except Exception as e:
        print(f"[Memory Store] Memory search error: {e}", file=sys.stderr)
    finally:
        conn.close()

    return results


def get_memory_stats():
    """Get counts of indexed archive files, chunks, and structured memories."""
    init_database()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as c FROM archive_documents")
    docs = cur.fetchone()["c"]
    cur.execute("SELECT COUNT(*) as c FROM archive_chunks")
    chunks = cur.fetchone()["c"]
    cur.execute("SELECT COUNT(*) as c FROM memories")
    mems = cur.fetchone()["c"]
    conn.close()
    return {"archive_documents": docs, "archive_chunks": chunks, "memories": mems}


if __name__ == "__main__":
    print("[Memory Store] Initializing database and indexing archive...")
    stats = index_ai_chat_logs()
    print(f"[Memory Store] Indexing complete: {stats}")
    print("[Memory Store] Testing search for 'fields of judgement'...")
    res = search_archive_logs("fields of judgement", limit=2)
    for r in res:
        print(f" -> Found in {r['filename']}: {r['snippet']}")
