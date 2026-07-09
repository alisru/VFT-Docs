#!/usr/bin/env python3
"""Demonstrates the one-query lookup: node address, Kanon ideal, current
(possibly bad) quote, and the full text of its cited source, all in one
SQL call via the nodes <-> hanson_sources join on citation_key."""
import sqlite3

DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

row = conn.execute("""
    SELECT n.address, n.vector_name, n.status, n.og_node_ideal AS kanon_ideal,
           n.quote_in_doc AS current_quote, n.citation_key,
           s.source_type, s.url, s.date_checked, length(s.full_text) AS full_text_len
    FROM nodes n
    LEFT JOIN hanson_sources s ON n.citation_key = s.citation_key
    WHERE n.node_id = 334
""").fetchone()

for k in row.keys():
    print(k, ":", row[k])

print()
print("row count check -- confirm join works across all fabricated nodes:")
rows = conn.execute("""
    SELECT n.node_id, n.address, n.vector_name, s.source_type, length(s.full_text) AS text_len
    FROM nodes n
    LEFT JOIN hanson_sources s ON n.citation_key = s.citation_key
    WHERE n.status = 'fabricated'
    ORDER BY n.plane, n.address
""").fetchall()
for r in rows:
    print(dict(r))
conn.close()
