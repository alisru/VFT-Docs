import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "chats.sqlite"

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
"""


def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH, timeout=30)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    con.executescript(SCHEMA)
    cols = [r[1] for r in con.execute("PRAGMA table_info(chats)")]
    if "url" not in cols:
        con.execute("ALTER TABLE chats ADD COLUMN url TEXT")
        con.commit()
    return con
