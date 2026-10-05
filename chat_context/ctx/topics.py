"""
Pure Semantic Topic Detection and KeyBERT Representation.
Zero folder heuristics, zero cloud calls, purely dense embeddings and contrastive c-TF-IDF.
"""
import math
import re
import urllib.parse
from collections import Counter
import numpy as np

from .embed import load_chat_vectors, embed_texts

STOP = set(
    "the a an and or to of in on for with is are was be it this that i you we my your me do does can how what why "
    "when where from as at by not no yes so if but just use using make get got want need please file files chat "
    "user_request add new run set let lets will would should could also about into out up all see here there "
    "done check now one two each any every first then after before than them these those have has had been being "
    "which who whom whose their they its our us some more most other another way like well much even back "
    "str int bool true false none null self args kwargs return import def class const let var function type "
    "path dir error docs vft text user assistant code line lines test script scripts running step steps data value".split()
)


def _clean_text(s: str) -> str:
    """Strip URLs, URL encodings (%20), markdown brackets, and code delimiters. Normalize underscores."""
    s = urllib.parse.unquote(s or "")
    s = re.sub(r"https?://\S+", " ", s)
    s = re.sub(r"@\[.*?\]", " ", s)
    s = re.sub(r"`+[^`]*`+", " ", s)
    s = s.replace("_", " ")
    s = re.sub(r"[^a-zA-Z0-9\s-]", " ", s)
    return s.lower()


def _words(s: str):
    clean = _clean_text(s)
    return [
        w for w in re.findall(r"[a-z][a-z0-9-]{2,}", clean)
        if w not in STOP and not w.isdigit() and not re.match(r"^\d+[a-z]+$", w)
    ]


def _extract_candidates(text_list, min_len=3):
    """Extract clean 1-grams and 2-grams."""
    counts = Counter()
    for text in text_list:
        clean = _clean_text(text)
        tokens = [
            w for w in re.findall(r"[a-z][a-z0-9-]{2,}", clean)
            if w not in STOP and not w.isdigit() and not re.match(r"^\d+[a-z]+$", w) and len(w) >= min_len
        ]
        for w in tokens:
            counts[w] += 1
        for i in range(len(tokens) - 1):
            w1, w2 = tokens[i], tokens[i + 1]
            if w1 != w2:
                counts[f"{w1} {w2}"] += 1
    return counts


def agglomerative_cluster(dist_matrix, threshold=0.78):
    """Pure numpy agglomerative clustering with average linkage."""
    n = len(dist_matrix)
    clusters = {i: [i] for i in range(n)}
    active = set(range(n))
    d = dist_matrix.copy()

    while len(active) > 1:
        act_list = sorted(active)
        sub_d = d[np.ix_(act_list, act_list)]
        np.fill_diagonal(sub_d, np.inf)

        min_val = float(np.min(sub_d))
        if min_val > threshold:
            break

        idx = np.unravel_index(np.argmin(sub_d), sub_d.shape)
        c1, c2 = act_list[idx[0]], act_list[idx[1]]

        clusters[c1].extend(clusters[c2])
        del clusters[c2]
        active.remove(c2)

        for other in active:
            if other == c1:
                continue
            pts1, pts2 = clusters[c1], clusters[other]
            avg_dist = float(dist_matrix[np.ix_(pts1, pts2)].mean())
            d[c1, other] = avg_dist
            d[other, c1] = avg_dist

    return list(clusters.values())


def recluster(con, threshold=0.78):
    """
    Cluster chats semantically and assign human-readable KeyBERT topic names.
    - Mean-centers embeddings to eliminate general English/dialogue bias.
    - Runs agglomerative clustering on cosine distance.
    - Names each cluster using contrastive KeyBERT semantic scoring against the cluster centroid.
    - Respects user-named topics and locked topic assignments.
    """
    ids, mat = load_chat_vectors(con)
    if not ids:
        return 0

    locked = {
        r["id"]: r["topic_id"]
        for r in con.execute("SELECT id, topic_id FROM chats WHERE topic_locked=1 AND topic_id IS NOT NULL")
    }

    # Remove unassigned auto topics (keep user-named and locked ones)
    con.execute("UPDATE chats SET topic_id=NULL WHERE topic_locked=0")
    con.execute(
        "DELETE FROM topics WHERE user_named=0 AND id NOT IN (SELECT DISTINCT topic_id FROM chats WHERE topic_id IS NOT NULL)"
    )

    # Anisotropy correction: Mean-center the embeddings
    mean_vec = mat.mean(axis=0, keepdims=True)
    centered = mat - mean_vec
    centered_norms = np.linalg.norm(centered, axis=1, keepdims=True)
    norm_centered = centered / np.clip(centered_norms, 1e-9, None)

    # Cosine distance on centered embeddings
    dist_matrix = np.clip(1.0 - (norm_centered @ norm_centered.T), 0.0, 2.0)
    np.fill_diagonal(dist_matrix, 0.0)

    # Cluster unassigned chats
    clusters_raw = agglomerative_cluster(dist_matrix, threshold=threshold)
    cluster_members = [[ids[idx] for idx in c] for c in clusters_raw]

    # Extract candidate keyphrases for each cluster
    cluster_cands = []
    doc_freq = Counter()
    for mems in cluster_members:
        txts = []
        for mid in mems:
            rows = con.execute("SELECT text FROM chunks WHERE chat_id=? LIMIT 10", (mid,)).fetchall()
            txts.extend([r["text"] for r in rows])
        cands = _extract_candidates(txts)
        cands = {k: v for k, v in cands.items() if v >= 2}
        cluster_cands.append(cands)
        for k in cands:
            doc_freq[k] += 1

    num_clusters = len(cluster_members)

    # Score candidates using KeyBERT + contrastive c-TF-IDF
    for mems, cands in zip(cluster_members, cluster_cands):
        # Check if all members already belong to a locked topic
        locked_topics = [locked[m] for m in mems if m in locked]
        if locked_topics and len(locked_topics) == len(mems) and len(set(locked_topics)) == 1:
            target_topic_id = locked_topics[0]
        else:
            # Cluster centroid in original embedding space
            c_vec = mat[[ids.index(m) for m in mems]].mean(axis=0)
            c_vec = c_vec / np.linalg.norm(c_vec)

            valid = [k for k in cands if doc_freq[k] <= max(num_clusters * 0.30, 2)]
            if not valid:
                valid = list(cands.keys())[:30]
            else:
                valid = sorted(valid, key=lambda k: cands[k], reverse=True)[:50]

            if valid:
                embs = embed_texts(valid)
                sims = embs @ c_vec
                top_k = np.argsort(-sims)[:3]
                topic_name = " / ".join([valid[idx] for idx in top_k])
            else:
                # Fallback to chat titles
                title_row = con.execute("SELECT title FROM chats WHERE id=?", (mems[0],)).fetchone()
                topic_name = (title_row["title"] or "misc")[:40]

            cur = con.execute("INSERT INTO topics(name, user_named) VALUES(?,0)", (topic_name,))
            target_topic_id = cur.lastrowid

        for m in mems:
            if m not in locked:
                con.execute("UPDATE chats SET topic_id=? WHERE id=?", (target_topic_id, m))

    con.commit()
    return num_clusters
