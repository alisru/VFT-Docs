CREATE TABLE IF NOT EXISTS nodes (
    node_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    plane           INTEGER NOT NULL,
    plane_name      TEXT,
    address         TEXT NOT NULL,
    vector_name     TEXT NOT NULL,
    upsilon         REAL,
    psi             REAL,
    hit_fail        TEXT,
    original_node   TEXT NOT NULL,
    og_node_ideal   TEXT,
    source_file     TEXT NOT NULL,
    line            INTEGER NOT NULL,
    quote_in_doc    TEXT,
    is_literal_quote INTEGER DEFAULT 1,
    source_context  TEXT,
    citation_key    TEXT,
    archive_file    TEXT,
    status          TEXT NOT NULL DEFAULT 'unchecked',
    fuzzy_score     REAL,
    verified_quote  TEXT,
    legacy_status   TEXT,
    legacy_note     TEXT,
    notes           TEXT,
    last_checked    TEXT,
    UNIQUE(address, vector_name, source_file)
);

CREATE INDEX IF NOT EXISTS idx_nodes_status ON nodes(status);
CREATE INDEX IF NOT EXISTS idx_nodes_citation ON nodes(citation_key);
CREATE INDEX IF NOT EXISTS idx_nodes_plane ON nodes(plane);

-- Named hanson_sources (actor-scoped) rather than a generic "sources" table,
-- so a future actor's audit gets its own equivalent table (e.g. albanese_sources)
-- instead of one shared table needing an actor column.
CREATE TABLE IF NOT EXISTS hanson_sources (
    citation_key    TEXT PRIMARY KEY,
    archive_file    TEXT,
    url             TEXT,             -- source URL, parsed from Sources.md
    date_checked    TEXT,             -- date the archive file was fetched (from file mtime)
    full_text       TEXT,             -- full text of the archived source, read from archive_file
    source_type     TEXT,             -- primary_speech_hansard / party_platform /
                                       -- voting_record_aggregator / news_article /
                                       -- reference_encyclopedia / court_judgment
    status          TEXT NOT NULL DEFAULT 'unchecked',
    legacy_status   TEXT,
    legacy_note     TEXT,
    node_count      INTEGER DEFAULT 0,
    notes           TEXT,
    last_checked    TEXT
);

CREATE TABLE IF NOT EXISTS status_history (
    history_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    node_id         INTEGER NOT NULL,
    old_status      TEXT,
    new_status      TEXT,
    changed_by      TEXT,
    note            TEXT,
    changed_at      TEXT NOT NULL,
    FOREIGN KEY(node_id) REFERENCES nodes(node_id)
);
