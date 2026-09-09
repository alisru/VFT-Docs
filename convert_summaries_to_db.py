import os
import sys
import re
import json
import sqlite3

# Ensure utf-8 stdout
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def parse_markdown_summaries(md_path):
    if not os.path.exists(md_path):
        print(f"File not found: {md_path}")
        return {}

    with open(md_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    entries = {}
    current_entry = None
    in_summary = False
    current_summary_lines = []

    def finalize_entry():
        nonlocal current_entry, current_summary_lines, in_summary
        if not current_entry:
            return

        raw_summary = "\n".join(current_summary_lines).strip()
        summary_topics = []
        needs_redo = False

        # Determine if summary is in structured Topic: format
        topic_items = re.split(r'\\\s*\n|\n', raw_summary)
        has_colon_topics = False

        for item in topic_items:
            item = item.strip().rstrip('\\').strip()
            if not item or item.startswith('#') or item.startswith('**Path**') or item.startswith('**Categories**') or item.startswith('**Classification**') or item.startswith('**Secondary Themes**'):
                continue
            if ':' in item and not item.lower().startswith('http'):
                parts = item.split(':', 1)
                t_name = parts[0].strip().lstrip('*-0123456789. ')
                t_desc = parts[1].strip()
                summary_topics.append({"topic": t_name, "description": t_desc})
                has_colon_topics = True
            else:
                summary_topics.append({"topic": "Summary", "description": item})

        # Check if this needs redoing
        if not summary_topics or not has_colon_topics or not current_entry["plane"] or current_entry.get("format") == "table" or any("[Description for" in t["description"] for t in summary_topics):
            needs_redo = True

        current_entry["raw_summary"] = raw_summary
        current_entry["summary_topics"] = summary_topics
        current_entry["needs_redo"] = needs_redo
        current_entry["status"] = "needs_redo" if needs_redo else "complete"

        fname = current_entry["filename"]
        if fname:
            entries[fname] = current_entry

        current_entry = None
        current_summary_lines = []
        in_summary = False

    for line in lines:
        line_str = line.strip()

        if line.startswith('### '):
            finalize_entry()
            header_content = line[4:].strip()

            date_str = ""
            date_match = re.search(r'\((20\d\d(?:-\d\d-\d\d)?)\)\s*$', header_content)
            if date_match:
                date_str = date_match.group(1)
                header_content = header_content[:date_match.start()].strip()

            clean_filename = header_content
            if clean_filename.startswith('[') and clean_filename.endswith(']'):
                clean_filename = clean_filename[1:-1].strip()

            current_entry = {
                "filename": clean_filename,
                "date": date_str,
                "path": "",
                "plane": "",
                "node": "",
                "tags": [],
                "summary_topics": [],
                "raw_summary": "",
                "format": "block",
                "needs_redo": False,
                "status": "complete"
            }
            continue

        if current_entry is not None:
            if line_str.startswith('**Path**:') or line_str.startswith('**Path:**'):
                current_entry["path"] = line_str.split(':', 1)[1].strip().strip('`')
                continue
            elif line_str.startswith('**Categories**:') or line_str.startswith('**Categories:**'):
                cat_str = line_str.split(':', 1)[1].strip()
                p_match = re.search(r'Plane:\s*([^;]+)', cat_str, re.IGNORECASE)
                n_match = re.search(r'Node:\s*([^;]+)', cat_str, re.IGNORECASE)
                t_match = re.search(r'Tags:\s*(.+)', cat_str, re.IGNORECASE)

                if p_match:
                    current_entry["plane"] = p_match.group(1).strip()
                if n_match:
                    current_entry["node"] = n_match.group(1).strip()
                if t_match:
                    current_entry["tags"] = [t.strip() for t in t_match.group(1).split(',') if t.strip()]
                continue
            elif line_str.startswith('**Classification**:') or line_str.startswith('**Classification:**'):
                current_entry["node"] = line_str.split(':', 1)[1].strip()
                continue
            elif line_str.startswith('**Secondary Themes**:') or line_str.startswith('**Secondary Themes:**'):
                st = line_str.split(':', 1)[1].strip()
                current_entry["tags"].extend([t.strip() for t in st.split(',') if t.strip()])
                continue
            elif line_str.startswith('**Summary**:'):
                # May have inline text: **Summary**: The text...
                inline_text = line_str[12:].strip()
                if inline_text:
                    current_summary_lines.append(inline_text)
                in_summary = True
                continue
            elif line.startswith('## '):
                finalize_entry()
                continue
            elif in_summary:
                current_summary_lines.append(line.rstrip('\r\n'))

    finalize_entry()

    # Parse Table rows as well
    table_row_pattern = re.compile(r'^\|\s*`?([^`|\n]+)`?\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$', re.MULTILINE)
    full_text = "".join(lines)
    for match in table_row_pattern.finditer(full_text):
        fname = match.group(1).strip()
        theme = match.group(2).strip()
        classification = match.group(3).strip()

        if fname.lower() in ["file name", ":---", "---", "name"]:
            continue

        if fname not in entries:
            theme_parts = theme.split('<br>')
            topics = []
            for part in theme_parts:
                part = part.strip()
                if not part:
                    continue
                m = re.match(r'\*\*(.*?)\*\*:\s*(.*)', part)
                if m:
                    topics.append({"topic": m.group(1).strip(), "description": m.group(2).strip()})
                else:
                    topics.append({"topic": "Key Finding", "description": part})

            entries[fname] = {
                "filename": fname,
                "date": "",
                "path": "",
                "plane": "",
                "node": classification,
                "tags": [classification] if classification else [],
                "summary_topics": topics,
                "raw_summary": theme,
                "format": "table",
                "needs_redo": True,
                "status": "needs_redo"
            }

    return entries

def save_to_json(entries, json_path):
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(entries)} records to JSON: {json_path}")

def save_to_js(entries, js_path):
    js_content = "window.VFT_SUMMARIES_DATA = " + json.dumps(entries, ensure_ascii=False) + ";\n"
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"Saved {len(entries)} records to JS: {js_path}")

def save_to_sqlite(entries, db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS topics")
    cur.execute("DROP TABLE IF EXISTS files")

    cur.execute("""
    CREATE TABLE files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT UNIQUE,
        date TEXT,
        path TEXT,
        plane TEXT,
        node TEXT,
        tags_json TEXT,
        quadrant TEXT,
        sub_vector TEXT,
        raw_summary TEXT,
        raw_format TEXT,
        status TEXT,
        needs_redo INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id INTEGER,
        topic TEXT,
        description TEXT,
        FOREIGN KEY (file_id) REFERENCES files (id) ON DELETE CASCADE
    )
    """)

    cur.execute("CREATE INDEX idx_files_filename ON files (filename)")
    cur.execute("CREATE INDEX idx_files_plane ON files (plane)")
    cur.execute("CREATE INDEX idx_files_node ON files (node)")
    cur.execute("CREATE INDEX idx_files_status ON files (status)")
    cur.execute("CREATE INDEX idx_topics_file_id ON topics (file_id)")

    for fname, data in entries.items():
        cur.execute("""
        INSERT INTO files (filename, date, path, plane, node, tags_json, quadrant, sub_vector, raw_summary, raw_format, status, needs_redo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("filename", fname),
            data.get("date", ""),
            data.get("path", ""),
            data.get("plane", ""),
            data.get("node", ""),
            json.dumps(data.get("tags", []), ensure_ascii=False),
            data.get("quadrant", ""),
            data.get("sub_vector", ""),
            data.get("raw_summary", ""),
            data.get("format", "block"),
            data.get("status", "complete"),
            1 if data.get("needs_redo") else 0
        ))

        file_id = cur.lastrowid

        for t in data.get("summary_topics", []):
            cur.execute("""
            INSERT INTO topics (file_id, topic, description)
            VALUES (?, ?, ?)
            """, (file_id, t.get("topic", ""), t.get("description", "")))

    conn.commit()
    conn.close()
    print(f"Saved {len(entries)} records to SQLite database: {db_path}")

def main():
    md_path = "file_summaries.md"
    json_path = "file_summaries.json"
    js_path = "file_summaries_data.js"
    db_path = "file_summaries.db"

    print(f"Parsing {md_path}...")
    entries = parse_markdown_summaries(md_path)
    
    needs_redo_count = sum(1 for e in entries.values() if e.get("needs_redo"))
    complete_count = len(entries) - needs_redo_count
    print(f"Total entries: {len(entries)} (Complete: {complete_count}, Needs Redo: {needs_redo_count})")

    save_to_json(entries, json_path)
    save_to_js(entries, js_path)
    save_to_sqlite(entries, db_path)

if __name__ == "__main__":
    main()
