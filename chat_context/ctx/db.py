import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "chats.sqlite"

CANVASES_DIR = ROOT / "canvases"
DRAFTS_DIR = ROOT / "drafts"

SCHEMA = """
CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    user_named INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS chats (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    title TEXT,
    started TEXT,
    updated TEXT,
    n_msgs INTEGER DEFAULT 0,
    src_mtime REAL DEFAULT 0,
    topic_id INTEGER REFERENCES topics(id),
    topic_locked INTEGER DEFAULT 0,
    emb BLOB
);
CREATE TABLE IF NOT EXISTS messages (
    chat_id TEXT NOT NULL,
    idx INTEGER NOT NULL,
    role TEXT NOT NULL,
    ts TEXT,
    text TEXT NOT NULL,
    PRIMARY KEY (chat_id, idx)
);
CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id TEXT NOT NULL,
    idx INTEGER NOT NULL,
    text TEXT NOT NULL,
    emb BLOB
);
CREATE INDEX IF NOT EXISTS chunks_chat ON chunks(chat_id);

CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
    text,
    chat_id UNINDEXED,
    content='chunks',
    content_rowid='id'
);

CREATE TABLE IF NOT EXISTS canvases (
    id TEXT PRIMARY KEY,
    chat_id TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    type TEXT,
    file_path TEXT,
    updated TEXT NOT NULL,
    FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_canvases_chat ON canvases(chat_id);
CREATE TABLE IF NOT EXISTS drafts (
    id TEXT PRIMARY KEY,
    site TEXT NOT NULL,
    url TEXT NOT NULL,
    page_title TEXT,
    context_title TEXT,
    text TEXT NOT NULL,
    char_count INTEGER,
    word_count INTEGER,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    file_path TEXT
);
CREATE INDEX IF NOT EXISTS idx_drafts_site ON drafts(site);
CREATE INDEX IF NOT EXISTS idx_drafts_updated ON drafts(updated_at DESC);

CREATE TABLE IF NOT EXISTS censored_chats (
    chat_id TEXT PRIMARY KEY,
    url TEXT,
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_censored_url ON censored_chats(url);
"""


def init_db():
    """Run once on startup to configure WAL mode, tables, and migrations."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    CANVASES_DIR.mkdir(parents=True, exist_ok=True)
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH, timeout=30) as con:
        con.execute("PRAGMA journal_mode=WAL")
        con.executescript(SCHEMA)
        cols = [r[1] for r in con.execute("PRAGMA table_info(chats)")]
        if "url" not in cols:
            con.execute("ALTER TABLE chats ADD COLUMN url TEXT")
            con.commit()
        # Ensure fragile triggers that cause "database disk image is malformed" are dropped
        con.execute("DROP TRIGGER IF EXISTS chunks_ai")
        con.execute("DROP TRIGGER IF EXISTS chunks_ad")
        con.execute("DROP TRIGGER IF EXISTS chunks_au")
        con.commit()

        # Verify chunks_fts is populated
        try:
            fts_count = con.execute("SELECT count(*) FROM chunks_fts").fetchone()[0]
            chunks_count = con.execute("SELECT count(*) FROM chunks").fetchone()[0]
            if chunks_count > 0 and fts_count == 0:
                con.execute("INSERT INTO chunks_fts(chunks_fts) VALUES('rebuild')")
                con.commit()
        except Exception as e:
            print(f"[db] FTS5 check notice: {e}")



def connect():
    """Fast connection factory for active queries."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH, timeout=30)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con
