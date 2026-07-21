"""
VFT Semantic & Graph Explorer — Server (v3)
Fully local. No cloud. Sentence-level semantic search.

Data loaded at startup (background thread):
  cluster_mapping.json   → paragraph-level topic_id
  topic_ism_mapping.json → topic metadata (node_name, quadrant, isms, keywords)
  layer_tags.json        → sentence_id → layer tag (Assertion, Definition, etc.)
  sentence_manifest.json → full sentence records (file, para_idx, sent_idx, raw_text)

Indexes built:
  para_lookup      : (norm_file, para_idx) → {topic_id, text}
  sent_file_idx    : norm_file → {para_idx → [{sentence_id, sentence_index, raw_text, layer_tag, topic_id}]}
  sent_topic_idx   : topic_id → [{sentence_id, raw_text, abs_file, para_idx, sent_idx}]
  topic_meta       : str(topic_id) → {node_name, quadrant, isms, keywords}

Endpoints:
  GET  /                             viewer.html
  GET  /api/filetree                 JSON tree of _VFT MD/
  GET  /api/file?path=<rel>          raw file content
  GET  /api/file-sentences?path=<rel> sentence-level data for a file
  POST /api/search                   {sentence_id} → related sentences in same cluster
"""

import sys, json, webbrowser, threading
from pathlib import Path
from collections import defaultdict

import numpy as np
from sentence_transformers import SentenceTransformer
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# ── Config ─────────────────────────────────────────────────────────────────────

PORT        = 8001
SCRIPT_DIR  = Path(__file__).parent.resolve()
VFT_MD_ROOT = Path("E:/Vector Field Theory/VFT Docs/_VFT MD")

CLUSTER_MAP_PATH  = SCRIPT_DIR / "cluster_mapping.json"
TOPIC_ISM_PATH    = SCRIPT_DIR / "topic_ism_mapping.json"
LAYER_TAGS_PATH   = SCRIPT_DIR / "layer_tags.json"
SENTENCE_MAN_PATH = SCRIPT_DIR / "sentence_manifest.json"

READABLE_EXTS = {".md", ".txt", ".js", ".py", ".json", ".html", ".cs"}

# ── App ────────────────────────────────────────────────────────────────────────

app = Flask(__name__, static_folder=str(SCRIPT_DIR))
CORS(app)

# ── Indexes & Models ───────────────────────────────────────────────────────────

para_lookup      = {}              # (norm_file, para_idx) → {topic_id, text}
sent_file_idx    = defaultdict(lambda: defaultdict(list))  # norm_file → para_idx → [sent entries]
sent_topic_idx   = defaultdict(list)  # topic_id → [sent entries]
topic_meta       = {}              # str(topic_id) → metadata
layer_tags       = {}              # sentence_id → tag string
sentence_records = []              # full sentence manifest array
model            = None            # local SentenceTransformer model
embeddings       = None            # mapped numpy array (float32)
_index_ready     = False           # flag so endpoints can return 503 if still loading


def _norm(path: str) -> str:
    return path.replace("\\", "/").lower()


def _load_indexes():
    global _index_ready, model, embeddings, layer_tags, sentence_records

    # 1. Topic ISM metadata
    print("Loading topic_ism_mapping.json ...", flush=True)
    with open(TOPIC_ISM_PATH, "r", encoding="utf-8") as f:
        raw_meta = json.load(f)
    for k, v in raw_meta.items():
        topic_meta[k] = v
    print(f"  {len(topic_meta):,} topics", flush=True)

    # 2. Paragraph → topic_id lookup
    print("Loading cluster_mapping.json ...", flush=True)
    with open(CLUSTER_MAP_PATH, "r", encoding="utf-8") as f:
        paragraphs = json.load(f)
    for p in paragraphs:
        key = (_norm(p["file"]), p["paragraph_index"])
        para_lookup[key] = {"topic_id": p["topic_id"], "text": p.get("text", "")}
    print(f"  {len(para_lookup):,} paragraphs", flush=True)

    # 3. Sentence layer tags (sentence_id → tag string)
    print("Loading layer_tags.json ...", flush=True)
    with open(LAYER_TAGS_PATH, "r", encoding="utf-8") as f:
        loaded_tags = json.load(f)
    layer_tags.update(loaded_tags)
    print(f"  {len(layer_tags):,} sentence tags", flush=True)

    # 4. Sentence manifest — build file + topic indexes
    print("Loading sentence_manifest.json (300MB, ~30s) ...", flush=True)
    with open(SENTENCE_MAN_PATH, "r", encoding="utf-8") as f:
        sentence_records = json.load(f)
    print(f"  {len(sentence_records):,} sentences — building indexes ...", flush=True)

    for s in sentence_records:
        sid      = s["sentence_id"]
        abs_file = s["file_path"]
        norm_f   = _norm(abs_file)
        para_idx = s["paragraph_index"]
        sent_idx = s["sentence_index"]
        raw_text = s["raw_text"]
        layer    = layer_tags.get(sid, "")

        # Topic inherited from parent paragraph
        para_info = para_lookup.get((norm_f, para_idx), {})
        topic_id  = para_info.get("topic_id")

        entry = {
            "sentence_id":    sid,
            "sentence_index": sent_idx,
            "raw_text":       raw_text,
            "layer_tag":      layer,
            "topic_id":       topic_id,
        }

        # File index: norm_file → para_idx → [entries]
        sent_file_idx[norm_f][para_idx].append(entry)

        # Topic index: topic_id → [slim entries for search results]
        if topic_id is not None:
            sent_topic_idx[topic_id].append({
                "sentence_id": sid,
                "raw_text":    raw_text,
                "abs_file":    abs_file,
                "norm_file":   norm_f,
                "para_idx":    para_idx,
                "sent_idx":    sent_idx,
                "layer_tag":   layer,
            })

    # 5. Local Embedding model & numpy matrix mapping
    print("Loading SentenceTransformer model ('all-mpnet-base-v2')...", flush=True)
    model = SentenceTransformer("all-mpnet-base-v2")
    print("Memory-mapping embeddings_v2.npy ...", flush=True)
    embeddings = np.load(SCRIPT_DIR / "embeddings_v2.npy", mmap_mode="r")

    _index_ready = True
    print(f"  Indexes ready. {len(sent_file_idx):,} files, {len(sent_topic_idx):,} topic clusters. Model & Embeddings loaded.", flush=True)


threading.Thread(target=_load_indexes, daemon=True).start()


# ── File tree ──────────────────────────────────────────────────────────────────

def _build_tree(directory: Path, root: Path) -> dict:
    node = {"name": directory.name, "path": str(directory.relative_to(root)).replace("\\", "/"),
            "type": "folder", "children": []}
    try:
        for entry in sorted(directory.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):
            if entry.name.startswith(".") or entry.name.startswith("__"):
                continue
            if entry.is_dir():
                node["children"].append(_build_tree(entry, root))
            elif entry.suffix.lower() in READABLE_EXTS:
                node["children"].append({
                    "name": entry.name, "path": str(entry.relative_to(root)).replace("\\", "/"),
                    "type": "file", "ext": entry.suffix.lower(),
                    "size": entry.stat().st_size,
                })
    except PermissionError:
        pass
    return node

_tree_cache = None
def get_tree():
    global _tree_cache
    if _tree_cache is None:
        _tree_cache = _build_tree(VFT_MD_ROOT, VFT_MD_ROOT)
    return _tree_cache


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(str(SCRIPT_DIR), "viewer.html")

@app.route("/viewer.html")
def viewer():
    return send_from_directory(str(SCRIPT_DIR), "viewer.html")

@app.route("/<path:filename>", methods=["GET", "HEAD"])
def static_files(filename):
    return send_from_directory(str(SCRIPT_DIR), filename)

@app.route("/api/filetree")
def api_filetree():
    return jsonify(get_tree())

@app.route("/api/file")
def api_file():
    rel = request.args.get("path", "").replace("\\", "/")
    if not rel:
        return jsonify({"error": "Missing path"}), 400
    target = (VFT_MD_ROOT / rel).resolve()
    try:
        target.relative_to(VFT_MD_ROOT.resolve())
    except ValueError:
        return jsonify({"error": "Path traversal denied"}), 403
    if not target.exists():
        return jsonify({"error": "Not found"}), 404
    return jsonify({"path": rel, "name": target.name,
                    "content": target.read_text(encoding="utf-8", errors="replace")})


@app.route("/api/file-sentences")
def api_file_sentences():
    """Return all sentences for a file, grouped by paragraph_index.

    Response shape:
    {
      "ready": true,
      "data": {
        "<para_idx>": [
          { sentence_id, sentence_index, raw_text, layer_tag, topic_id,
            node_name, quadrant, quadrant_name, isms }
        ]
      }
    }
    """
    if not _index_ready:
        return jsonify({"ready": False, "data": {}}), 200

    rel = request.args.get("path", "").replace("\\", "/")
    if not rel:
        return jsonify({"error": "Missing path"}), 400

    abs_path = str((VFT_MD_ROOT / rel).resolve())
    norm     = _norm(abs_path)

    file_data = sent_file_idx.get(norm, {})
    result = {}
    for para_idx, sents in file_data.items():
        enriched = []
        for s in sorted(sents, key=lambda x: x["sentence_index"]):
            tid  = s["topic_id"]
            meta = topic_meta.get(str(tid), {}) if tid is not None else {}
            enriched.append({
                "sentence_id":    s["sentence_id"],
                "sentence_index": s["sentence_index"],
                "raw_text":       s["raw_text"],
                "layer_tag":      s["layer_tag"],
                "topic_id":       tid,
                "node_name":      meta.get("node_name", ""),
                "quadrant":       meta.get("quadrant", ""),
                "quadrant_name":  meta.get("quadrant_name", ""),
                "isms":           meta.get("isms", []),
            })
        result[str(para_idx)] = enriched

    return jsonify({"ready": True, "data": result})


@app.route("/api/search", methods=["POST"])
def api_search():
    """Find related sentences by topic cluster OR search by semantic query text.

    Body: { "sentence_id": "0_1_3", "limit": 15 }
       OR { "query": "consciousness", "limit": 25 }

    Returns:
    {
      "is_query": true/false,
      "topic": { id, node_name, quadrant, quadrant_name, isms, keywords },
      "total_in_cluster": N,
      "hits": [ { sentence_id, raw_text, rel_path, abs_file, para_idx, sent_idx, layer_tag, score } ]
    }
    """
    if not _index_ready:
        return jsonify({"error": "Index still loading, try again in a moment"}), 503

    data  = request.get_json(force=True, silent=True) or {}
    limit = min(int(data.get("limit", 15)), 50)

    # Helper to clean relative path
    vft_md_str  = str(VFT_MD_ROOT.resolve()).replace("\\", "/").lower()
    def to_rel(abs_f: str) -> str:
        n = abs_f.replace("\\", "/")
        idx = n.lower().find("_vft md/")
        if idx != -1:
            return n[idx + len("_vft md/"):]
        return n

    # ── Path A: Semantic Query Search ─────────────────────────────────
    if "query" in data:
        query = data["query"].strip()
        if not query:
            return jsonify({"error": "Empty query"}), 400

        # Encode query + compute similarity
        q_vec = model.encode(query, normalize_embeddings=True)
        scores = np.dot(embeddings, q_vec)
        top_idx = np.argsort(scores)[::-1][:limit]

        formatted = []
        for idx in top_idx:
            idx_int = int(idx)
            s = sentence_records[idx_int]
            sid = s["sentence_id"]
            para_idx = s["paragraph_index"]
            norm_f = _norm(s["file_path"])
            
            # Inherited topic info
            para_info = para_lookup.get((norm_f, para_idx), {})
            topic_id = para_info.get("topic_id")
            meta = topic_meta.get(str(topic_id), {}) if topic_id is not None else {}

            formatted.append({
                "sentence_id":    sid,
                "raw_text":       s["raw_text"],
                "abs_file":       s["file_path"],
                "rel_path":       to_rel(s["file_path"]),
                "para_idx":       para_idx,
                "sent_idx":       s["sentence_index"],
                "layer_tag":      layer_tags.get(sid, ""),
                "score":          float(scores[idx_int]),
                "topic_id":       topic_id,
                "node_name":      meta.get("node_name", ""),
                "quadrant":       meta.get("quadrant", ""),
            })

        return jsonify({
            "is_query": True,
            "query": query,
            "hits": formatted
        })

    # ── Path B: Click-to-find cluster siblings ────────────────────────
    topic_id        = None
    exclude_norm    = None
    exclude_sent_id = None

    if "sentence_id" in data:
        sid = data["sentence_id"]
        parts = sid.split("_")
        if len(parts) >= 3:
            for tid, sents in sent_topic_idx.items():
                found = next((s for s in sents if s["sentence_id"] == sid), None)
                if found:
                    topic_id     = tid
                    exclude_norm = found["norm_file"]
                    exclude_sent_id = sid
                    break

    elif "topic_id" in data:
        topic_id     = data["topic_id"]
        exclude_norm = data.get("exclude_norm_file")

    if topic_id is None:
        return jsonify({"error": "Could not resolve topic_id from request"}), 400

    meta = topic_meta.get(str(topic_id), {})
    siblings = sent_topic_idx.get(topic_id, [])

    # Exclude source sentence
    hits = [s for s in siblings if s.get("sentence_id") != exclude_sent_id]

    # Sort files
    source_norm = exclude_norm or ""
    hits.sort(key=lambda s: (s["norm_file"] == source_norm, s["para_idx"], s["sent_idx"]))
    hits = hits[:limit]

    formatted = [{
        "sentence_id":    h["sentence_id"],
        "raw_text":       h["raw_text"],
        "abs_file":       h["abs_file"],
        "rel_path":       to_rel(h["abs_file"]),
        "para_idx":       h["para_idx"],
        "sent_idx":       h["sent_idx"],
        "layer_tag":      h["layer_tag"],
    } for h in hits]

    return jsonify({
        "is_query": False,
        "topic": {
            "id":            topic_id,
            "node_name":     meta.get("node_name", ""),
            "quadrant":      meta.get("quadrant", ""),
            "quadrant_name": meta.get("quadrant_name", ""),
            "isms":          meta.get("isms", []),
            "keywords":      meta.get("keywords", [])[:8],
        },
        "total_in_cluster": len(siblings),
        "hits": formatted,
    })


# ── Launch ─────────────────────────────────────────────────────────────────────

def open_browser():
    import time; time.sleep(1.5)
    webbrowser.open(f"http://localhost:{PORT}/viewer.html")

if __name__ == "__main__":
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding="utf-8")
    print(f"VFT Doc Reader starting on http://localhost:{PORT}", flush=True)
    print("Index loading in background — Doc Reader tab will show 'loading' until ready.", flush=True)
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)
