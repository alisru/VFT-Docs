#!/usr/bin/env python3
import re
import os
import sqlite3
import datetime
import unicodedata
from collections import Counter

DB_PATH = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"

VERIFIED_THRESHOLD = 0.85
PARAPHRASED_THRESHOLD = 0.50


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def normalize_words(text):
    if not text:
        return []
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"[^\w\s]", " ", text.lower())
    return [w for w in text.split() if w]


def split_sentences(text):
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [p.strip() for p in parts if p.strip()]


def bag_overlap_ratio(quote_words, source_words):
    if not quote_words:
        return 0.0
    q_counts = Counter(quote_words)
    s_counts = Counter(source_words)
    overlap = sum(min(c, s_counts.get(w, 0)) for w, c in q_counts.items())
    return overlap / len(quote_words)


def best_excerpt(quote_words, source_text):
    sentences = split_sentences(source_text)
    best_score = 0.0
    best_sentence = None
    for sent in sentences:
        sent_words = normalize_words(sent)
        score = bag_overlap_ratio(quote_words, sent_words)
        if score > best_score:
            best_score = score
            best_sentence = sent
    return best_sentence, best_score


def classify(ratio, is_literal_quote):
    if ratio >= VERIFIED_THRESHOLD:
        return "verified"
    if ratio >= PARAPHRASED_THRESHOLD:
        return "paraphrased"
    if not is_literal_quote:
        return "paraphrased"
    return "fabricated"


def run(conn):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT node_id, quote_in_doc, citation_key, archive_file, status, is_literal_quote
        FROM nodes
        """
    )
    rows = cur.fetchall()

    counts = Counter()
    for node_id, quote, key, archive_file, old_status, is_literal_quote in rows:
        if key is None:
            counts["no_citation"] += 1
            continue
        if not archive_file or not os.path.exists(archive_file):
            new_status = "needs_hansard"
            conn.execute(
                "UPDATE nodes SET status=?, fuzzy_score=NULL, last_checked=? WHERE node_id=?",
                (new_status, now(), node_id),
            )
            if old_status != new_status:
                conn.execute(
                    "INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at) "
                    "VALUES (?,?,?,?,?,?)",
                    (node_id, old_status, new_status, "fuzzy_check", "no archive file present", now()),
                )
            counts[new_status] += 1
            continue

        with open(archive_file, encoding="utf-8", errors="replace") as f:
            source_text = f.read()

        quote_words = normalize_words(quote)
        source_words = normalize_words(source_text)
        ratio = bag_overlap_ratio(quote_words, source_words)
        excerpt, excerpt_score = best_excerpt(quote_words, source_text)
        new_status = classify(ratio, bool(is_literal_quote))

        conn.execute(
            """
            UPDATE nodes
            SET status=?, fuzzy_score=?, verified_quote=?, last_checked=?
            WHERE node_id=?
            """,
            (new_status, round(ratio, 4), excerpt, now(), node_id),
        )
        if old_status != new_status:
            conn.execute(
                "INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at) "
                "VALUES (?,?,?,?,?,?)",
                (node_id, old_status, new_status, "fuzzy_check",
                 f"bag-of-words overlap ratio={ratio:.2f}", now()),
            )
        counts[new_status] += 1

    conn.commit()
    return counts


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    counts = run(conn)
    conn.close()
    print("fuzzy_check complete:")
    for status, n in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {status:15s} {n}")
