import os
import sys
import re
import json
import sqlite3
import time
import argparse
import urllib.request
import urllib.error
from datetime import datetime

# Ensure utf-8 stdout
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 16-Category Tag Matrix from VFT
TAG_MATRIX = {
    "Logic": ["Logic", "Mathematics", "Computation", "Maths", "Order", "Structured Order", "Algorithms", "Systems", "Calculus", "Algebra", "Geometry", "Statistics", "Programming", "Proofs", "Axioms", "Deduction", "Framework", "Hierarchy"],
    "Spirituality": ["Spirituality", "Mysticism", "Transcendence", "Faith", "Esotericism", "Metaphysical", "Occult", "Meditation", "Divinity", "Enlightenment", "Sacred", "Etheric", "Awakening", "Karma"],
    "Religion": ["Religion", "Theology", "Doctrine", "Charity", "Dogma", "Scripture", "Ritual", "Church", "Temple", "Creed", "Orthodoxy", "Worship", "Priesthood", "Canon", "Denomination"],
    "Cognition": ["Cognition", "Reason", "Intellect", "Intelligence", "Hope", "Thought", "Awareness", "Perception", "Sentience", "Rationality", "Neurology", "Neuroscience", "Idea", "Mental", "Focus"],
    "Physics": ["Physics", "Mechanics", "Matter", "Objectivity", "Thermodynamics", "Quantum", "Relativity", "Optics", "Gravity", "Energy", "Kinetics", "Particle", "Forces", "Dynamics", "Astrophysics", "Material"],
    "Metaphysics": ["Metaphysics", "Ontology", "Cosmology", "Imagination", "Existentialism", "Phenomenon", "Abstract", "Aether", "Reality-Theory", "Void", "First-Principles", "Archetypes"],
    "Ethics": ["Ethics", "Morality", "Values", "Emotional-physics", "Temperance", "Philosophy", "Virtue", "Deontology", "Utilitarianism", "Axiology", "Righteousness", "Code", "Integrity", "Moral-Compass", "Dilemma"],
    "Knowledge": ["Knowledge", "Epistemology", "Education", "Learning", "Prudence", "Information", "Data", "Wisdom", "Scholarship", "Academia", "Pedagogy", "Instruction", "Curriculum", "Study", "Literacy"],
    "Society": ["Community", "Civic", "Public", "Society", "Social", "Populace", "Tribe", "Village", "Group", "Collective", "Fellowship", "Network", "Neighborhood", "Cohort", "Population"],
    "Sociology": ["Sociology", "Culture", "Anthropology", "Empathy", "Demographics", "Ethnography", "Social-Structures", "Customs", "Traditions", "Human-Ecology", "Interpersonal", "Norms", "Kinship"],
    "Conscience": ["Conscience", "Judgment", "Principles", "Internal Judgment", "Justice", "Guilt", "Inner-Voice", "Fairness", "Law", "Jurisprudance", "Equity", "Conviction", "Rectitude", "Accountability"],
    "The World": ["Nature", "Ecology", "Environment", "The World", "Fortitude", "Biology", "Zoology", "Botany", "Biosphere", "Earth", "Ecosystem", "Natural-World", "Flora", "Fauna", "Wilderness", "Geology", "Climate"],
    "Psychology": ["Psychology", "Mind", "Behavior", "Understanding", "Psychiatry", "Therapy", "Psychoanalysis", "Emotion", "Trauma", "Personality", "Subconscious", "Mental-Health", "Affect", "Neuroscience"],
    "Communication": ["Communication", "Expression", "Linguistics", "Language", "Connection", "Discourse", "Dialogue", "Semantics", "Syntax", "Rhetoric", "Media", "Transmission", "Interaction", "Speech", "Writing", "Symbology"],
    "History": ["History", "Chronology", "Record", "Context", "Antiquity", "Archives", "Heritage", "Past", "Timeline", "Archaeology", "Paleontology", "Genealogy", "Epoch", "Era", "Annals", "Historiography"],
    "Reality": ["Reality", "Existence", "Actuality", "Truth", "Fact", "Objective-Truth", "Present", "Universe", "Cosmos", "Material-World", "Being", "Verity", "Tangibility", "Substantive"]
}

PLANE_MAP = {
    "Logic": "Q5 HOW",
    "Spirituality": "Q1 WHO",
    "Religion": "Q1 WHO",
    "Cognition": "Q1 WHO",
    "Physics": "Q3 WHERE",
    "Metaphysics": "Q2 WHAT",
    "Ethics": "Q4 WHY",
    "Knowledge": "Q5 HOW",
    "Society": "Q7 EFFECT",
    "Sociology": "Q3 WHERE",
    "Conscience": "Q1 WHO",
    "The World": "Q3 WHERE",
    "Psychology": "Q1 WHO",
    "Communication": "Q2 WHAT",
    "History": "Q6 CAUSE",
    "Reality": "Q2 WHAT"
}

def load_semantic_mapping():
    mapping_path = os.path.join("Semantic_Clusters", "doc_ism_mapping.json")
    if os.path.exists(mapping_path):
        try:
            with open(mapping_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def extract_metadata(content, filepath, semantic_doc_mapping):
    filename = os.path.basename(filepath)
    date_str = datetime.now().strftime("%Y-%m-%d")
    win_path = filepath.replace('/', '\\')

    if filename in semantic_doc_mapping:
        doc_info = semantic_doc_mapping[filename]
        node_name = doc_info.get("node_name", "Reality")
        isms = doc_info.get("isms", [])
        quadrant = doc_info.get("quadrant", "GG")
        sub_vector = doc_info.get("sub_vector", "")
        
        matched_cat = "Reality"
        for cat in TAG_MATRIX.keys():
            if cat.lower() in node_name.lower():
                matched_cat = cat
                break
        
        plane = PLANE_MAP.get(matched_cat, "Q2 WHAT")
        tags = isms + [matched_cat]
        tags_list = sorted(list(set(tags)))
        return {
            "filename": filename,
            "date": date_str,
            "path": win_path,
            "plane": plane,
            "node": matched_cat,
            "tags": tags_list,
            "quadrant": quadrant,
            "sub_vector": sub_vector,
            "status": "complete",
            "needs_redo": False
        }

    content_lower = content.lower()
    best_category = "Reality"
    matched_tags = []
    max_hits = -1

    for category, tags in TAG_MATRIX.items():
        hits = 0
        cat_tags = []
        if category.lower() in content_lower:
            hits += 5
        for tag in tags:
            if tag.lower() in content_lower:
                hits += 1
                cat_tags.append(tag)

        if hits > max_hits:
            max_hits = hits
            best_category = category
            matched_tags = cat_tags

    if not matched_tags:
        matched_tags = TAG_MATRIX[best_category][:3]
    else:
        matched_tags = sorted(list(set(matched_tags)))[:7]

    plane = PLANE_MAP.get(best_category, "Q2 WHAT")
    return {
        "filename": filename,
        "date": date_str,
        "path": win_path,
        "plane": plane,
        "node": best_category,
        "tags": matched_tags,
        "quadrant": "GG",
        "sub_vector": "",
        "status": "complete",
        "needs_redo": False
    }

def extract_headings(content):
    topics = re.findall(r'^#+ (.*)', content, re.MULTILINE)
    topics = [t.strip() for t in topics if t.strip().lower() not in ['works cited', 'references', 'introduction', 'conclusion', 'summary', 'abstract', 'table of contents']]
    if not topics:
        topics = re.findall(r'^\* \*\*(.*?)\*\*', content, re.MULTILINE)
    if not topics:
        topics = re.findall(r'^#### (.*)', content, re.MULTILINE)
    
    seen = set()
    unique_topics = []
    for t in topics:
        clean = re.sub(r'[*_`]', '', t).strip()
        if clean and clean not in seen:
            unique_topics.append(clean)
            seen.add(clean)
    return unique_topics[:5]

def call_local_llm(content, topics, filename, api_url="http://127.0.0.1:1234/v1/chat/completions"):
    truncated_content = content[:6000]
    topics_list_str = "\n".join([f"- {t}" for t in topics]) if topics else "- Core Thesis\n- Key Mechanism"
    
    prompt = f"""Summarize the key findings of this document concisely.

Document Name: {filename}

Key Topics / Sections:
{topics_list_str}

Content:
\"\"\"
{truncated_content}
\"\"\"

Strict Rules:
1. For each topic, write EXACTLY 2 to 3 concise, high-density sentences. Keep sentences crisp and clear, no long run-on clauses.
2. Format each line as:
Topic Name: Sentence 1. Sentence 2. (Optional Sentence 3.)
3. No bullet points (* or -), no introductory chatter, no markdown headers.
"""

    payload = {
        "messages": [
            {"role": "system", "content": "You are a concise analytical summarizer. Output only clean topic lines with exactly 2-3 crisp sentences per topic."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 600
    }

    req = urllib.request.Request(
        api_url,
        data=json.dumps(payload).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            raw_text = data['choices'][0]['message']['content'].strip()
            
            if "<think>" in raw_text:
                raw_text = re.sub(r'<think>.*?</think>', '', raw_text, flags=re.DOTALL).strip()
                
            raw_text = raw_text.replace(r'\n', '\n')
            raw_lines = raw_text.split('\n')
            
            topics_data = []
            for line in raw_lines:
                line_str = line.strip().rstrip('\\').strip()
                if line_str and not line_str.startswith('#'):
                    if ':' in line_str:
                        parts = line_str.split(':', 1)
                        t_name = parts[0].strip().lstrip('*-0123456789. ')
                        t_desc = parts[1].strip()
                        topics_data.append({"topic": t_name, "description": t_desc})
                    else:
                        topics_data.append({"topic": "Core Finding", "description": line_str})
            return topics_data
    except Exception as e:
        print(f"  [Error calling LLM for {filename}]: {e}")
        return [{"topic": t, "description": "Core structural and theoretical analysis of systemic parameters."} for t in topics]

def summarize_file(filepath, semantic_doc_mapping, api_url="http://127.0.0.1:1234/v1/chat/completions"):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    meta = extract_metadata(content, filepath, semantic_doc_mapping)
    topics = extract_headings(content)
    if not topics:
        topics = ["Core Thesis", "Structural Dynamics"]

    topics_summary_list = call_local_llm(content, topics, meta["filename"], api_url)
    meta["summary_topics"] = topics_summary_list

    # Format Markdown
    summary_lines = [f"{item['topic']}: {item['description']}" for item in topics_summary_list]
    summary_md = "\\\n".join(summary_lines)
    tags_str = ", ".join(meta["tags"])

    markdown_entry = f"""### [{meta['filename']}] ({meta['date']})
**Path**: {meta['path']}
**Categories**: Plane: {meta['plane']}; Node: {meta['node']}; Tags: {tags_str}
**Summary**:
{summary_md}"""

    return meta, markdown_entry

def append_to_sqlite(meta_records, db_path="file_summaries.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    for data in meta_records:
        fname = data.get("filename", "")
        cur.execute("SELECT id FROM files WHERE filename = ?", (fname,))
        row = cur.fetchone()
        if row:
            cur.execute("DELETE FROM topics WHERE file_id = ?", (row[0],))
            cur.execute("DELETE FROM files WHERE id = ?", (row[0],))

        cur.execute("""
        INSERT INTO files (filename, date, path, plane, node, tags_json, quadrant, sub_vector, raw_summary, raw_format, status, needs_redo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            fname,
            data.get("date", ""),
            data.get("path", ""),
            data.get("plane", ""),
            data.get("node", ""),
            json.dumps(data.get("tags", []), ensure_ascii=False),
            data.get("quadrant", ""),
            data.get("sub_vector", ""),
            "",
            "block",
            "complete",
            0
        ))

        file_id = cur.lastrowid
        for t in data.get("summary_topics", []):
            cur.execute("""
            INSERT INTO topics (file_id, topic, description)
            VALUES (?, ?, ?)
            """, (file_id, t.get("topic", ""), t.get("description", "")))

    conn.commit()
    conn.close()

def sync_js_file(master_json, js_path="file_summaries_data.js"):
    js_content = "window.VFT_SUMMARIES_DATA = " + json.dumps(master_json, ensure_ascii=False) + ";\n"
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js_content)

def get_gpu_temperature():
    try:
        import subprocess
        res = subprocess.run(
            ['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'],
            capture_output=True, text=True, timeout=2
        )
        return int(res.stdout.strip())
    except Exception:
        return None

def wait_for_gpu_cooldown(cool_temp=50, max_temp=68, check_interval=5):
    temp = get_gpu_temperature()
    if temp is None:
        return
    
    # Trigger thermal throttle only when GPU reaches or exceeds max_temp
    if temp >= max_temp:
        print(f"  [THERMAL THROTTLE] GPU reached {temp}°C (>= {max_temp}°C trigger). Cooling down to <={cool_temp}°C...")
        while temp is not None and temp > cool_temp:
            time.sleep(check_interval)
            temp = get_gpu_temperature()
            if temp is not None:
                print(f"  [COOLING] Current GPU temp: {temp}°C (waiting for <={cool_temp}°C)...")
        if temp is not None:
            print(f"  [READY] GPU cooled to {temp}°C. Resuming processing.")
    else:
        print(f"  [GPU Temp: {temp}°C (OK)]")

def scan_workspace_markdown_files(root_dir="."):
    ignore_dir_names = {
        '.git', '.agents', '.agent', '.gemini', 'drawing_board', 'drawing board',
        '__pycache__', 'node_modules', '.venv', 'venv', 'embedding_checkpoints',
        '$recycle.bin', 'stories', 'fetch', 'raw_fetches', 'sources_archive',
        'sources', 'source_texts', 'archive_sessions_json', 'archive full',
        'full archive', '_archive', 'scratch'
    }
    ignore_files = {
        'file_summaries.md', 'file_summaries_fixed.md', 'file_summaries_handover.md', 
        'discovered_handover.md', 'categorized_file_list.md', 'google_notebooks_file_list.md',
        'walkthrough.md', 'implementation_plan.md'
    }
    found = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [
            d for d in dirs 
            if d.lower() not in ignore_dir_names 
            and not d.startswith('.') 
            and not any(x in d.lower() for x in ['_archive', 'archive', 'fetch', 'source_text', 'stories'])
        ]
        for f in files:
            if f.endswith('.md') and f not in ignore_files and not f.lower().startswith('fetch_') and not f.lower().startswith('search_'):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, start=root_dir)
                win_path = rel_path.replace('/', '\\')
                found.append((f, win_path))
    return found

def main():
    parser = argparse.ArgumentParser(description="Bulk sequential summarizer with SQLite DB + JSON + Markdown + JS output")
    parser.add_argument("--limit", type=int, default=10, help="Number of files to process (default: 10)")
    parser.add_argument("--delay", type=float, default=2.0, help="Minimum baseline delay in seconds between files (default: 2.0)")
    parser.add_argument("--cool-temp", type=int, default=50, help="Target GPU temperature in Celsius to cool down to before next file (default: 50)")
    parser.add_argument("--max-temp", type=int, default=70, help="GPU temperature threshold in Celsius that triggers cooldown (default: 70)")
    parser.add_argument("--no-temp-check", action="store_true", help="Disable automatic GPU temperature throttling")
    parser.add_argument("--dir", default=".", help="Root directory to scan for markdown files (default: .)")
    parser.add_argument("--redo-only", action="store_true", help="Target only entries flagged as needing redo")
    parser.add_argument("--new-only", action="store_true", help="Target only completely new unsummarised files")
    parser.add_argument("--append-master", action="store_true", default=True, help="Update master DB, JSON, JS and MD files")
    parser.add_argument("--api-url", default="http://127.0.0.1:1234/v1/chat/completions", help="LM Studio API URL")

    args = parser.parse_args()

    completed_set = set()
    redo_files = []

    if os.path.exists("file_summaries.db"):
        conn = sqlite3.connect("file_summaries.db")
        cur = conn.cursor()
        cur.execute("SELECT filename, path, needs_redo FROM files")
        for row in cur.fetchall():
            fname, fpath, needs_redo = row[0], row[1], row[2]
            if needs_redo == 1:
                redo_files.append((fname, fpath, "redo"))
            else:
                completed_set.add(fname)
        conn.close()

    # Live dynamic disk scan for all markdown files in workspace
    all_disk_files = scan_workspace_markdown_files(args.dir)
    new_unsummarized_files = []
    seen_new = set()

    for fname, fpath in all_disk_files:
        if fname not in completed_set and not any(fname == r[0] for r in redo_files):
            if fname not in seen_new:
                new_unsummarized_files.append((fname, fpath, "new"))
                seen_new.add(fname)

    # Queue Construction: By default, NEW files first, then REDO files when new are exhausted
    if args.redo_only:
        queue = redo_files
        print(f"Targeting REDO-ONLY mode: {len(queue)} legacy/incomplete files queued.")
    elif args.new_only:
        queue = new_unsummarized_files
        print(f"Targeting NEW-ONLY mode: {len(queue)} unindexed files queued.")
    else:
        # Default: New unsummarized files first, then redo legacy files
        queue = new_unsummarized_files + redo_files
        if new_unsummarized_files:
            print(f"Default Queue: {len(new_unsummarized_files)} NEW unindexed files FIRST, followed by {len(redo_files)} redo files ({len(queue)} total).")
        else:
            print(f"Default Queue: All new files completed! Processing remaining {len(redo_files)} legacy redo files.")

    if not queue:
        print("All files in the queue have already been fully summarized!")
        return

    if args.delay > 0:
        print(f"Throttling: {args.delay}s thermal cooling delay between documents.")
    semantic_mapping = load_semantic_mapping()
    print(f"Semantic Taxonomy: Loaded {len(semantic_mapping)} records from Semantic_Clusters.")

    # Load existing master JSON once into memory
    json_path = "file_summaries.json"
    master_json = {}
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                master_json = json.load(f)
        except Exception:
            master_json = {}

    processed_count = 0

    for idx, item in enumerate(queue[:args.limit]):
        fname, fpath, item_type = item[0], item[1], item[2]
        resolved_path = fpath

        # Resolve disk path
        if not os.path.exists(resolved_path):
            # Check direct in _VFT MD or subfolders
            for root, _, files in os.walk("_VFT MD"):
                if fname in files:
                    resolved_path = os.path.join(root, fname)
                    break

        if not os.path.exists(resolved_path):
            print(f"  [SKIP] File not found on disk: {fname}")
            continue

        type_tag = "[REDO]" if item_type == "redo" else "[NEW]"
        print(f"[{processed_count + 1}/{min(args.limit, len(queue))}] {type_tag} Summarizing: {fname}...")
        try:
            meta_json, md_entry = summarize_file(resolved_path, semantic_mapping, args.api_url)
            processed_count += 1

            # 1. Immediately update SQLite DB
            append_to_sqlite([meta_json], "file_summaries.db")

            # 2. Immediately update JSON database
            master_json[meta_json["filename"]] = meta_json
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(master_json, f, indent=2, ensure_ascii=False)

            # 3. Immediately update JS data for live browser viewer
            sync_js_file(master_json, "file_summaries_data.js")

            # 4. Immediately append to master Markdown
            with open("file_summaries.md", "a", encoding="utf-8") as f:
                f.write(md_entry + "\n\n")

            print(f"  [OK] Saved & Synced: {fname}")
        except Exception as e:
            print(f"  [FAIL] Error on {fname}: {e}")

        # Apply cooling pause and GPU temperature auto-throttling
        if idx < min(args.limit, len(queue)) - 1:
            if args.delay > 0:
                time.sleep(args.delay)
            if not args.no_temp_check:
                wait_for_gpu_cooldown(cool_temp=args.cool_temp, max_temp=args.max_temp, check_interval=5)

    print(f"\nBatch complete: {processed_count} documents successfully summarized and saved.")

if __name__ == "__main__":
    main()
