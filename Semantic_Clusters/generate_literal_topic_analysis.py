import os
import json
import re

STOP_WORDS = {
    'the', 'and', 'of', 'to', 'in', 'is', 'that', 'for', 'it', 'on', 'with', 'as', 
    'this', 'was', 'at', 'by', 'an', 'be', 'are', 'from', 'this', 'have', 'were', 
    'which', 'there', 'what', 'their', 'they', 'our', 'your', 'about', 'more', 
    'would', 'their', 'he', 'she', 'his', 'her', 'him', 'its', 'not', 'but', 'we',
    'you', 'has', 'had', 'been', 'or', 'an', 'will', 'who', 'into', 'can', 'one',
    'all', 'also', 'any', 'file', 'docs', 'theory', 'vector', 'field', 'system',
    'actualism', 'psochic', 'hegemony', 'canons', 'kanon', 'plane', 'planes'
}

def clean_and_get_top_words(text, limit=5):
    # Remove markdown formatting and keep words
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    freq = {}
    for w in words:
        if w not in STOP_WORDS:
            freq[w] = freq.get(w, 0) + 1
    
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [w[0] for w in sorted_words[:limit]]

def extract_literal_summary(text):
    # Clean out markdown headers, image embeds, links, etc.
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            continue
        if line_strip.startswith('#') or line_strip.startswith('!') or line_strip.startswith('*') or line_strip.startswith('-'):
            continue
        # Remove markdown link syntax [label](url) -> label
        line_clean = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', line_strip)
        cleaned_lines.append(line_clean)
        if len(cleaned_lines) >= 3: # take first 3 paragraphs/sentences
            break
            
    summary = " ".join(cleaned_lines)
    if len(summary) > 250:
        summary = summary[:247] + "..."
    return summary.strip()

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    
    categories_slugs = {
        "Information Physics & Thermodynamics": "physics-thermodynamics",
        "Metaphysics: Linguistic Relationalism & Psychology": "metaphysics-linguistic-psychology",
        "Metaphysics: Ontological Metaphysics & Theology": "metaphysics-ontological-theology",
        "Ontological Auditing & Geopolitics": "ontological-auditing-geopolitics",
        "System Protocols & Operational Guides": "system-protocols-operational-guides",
        "Unstructured Notes & Chat Logs": "unstructured-notes-chat-logs"
    }

    report_path = os.path.join(script_dir, "notebook_literal_topic_analysis.md")
    print(f"Generating literal topic report at {report_path}...", flush=True)

    with open(report_path, 'w', encoding='utf-8') as rep:
        rep.write("# Literal Topic Analysis of Notebook Documents\n\n")
        rep.write("This report details what each document is literally about (extracting concrete keywords, sub-folder contexts, and opening summaries) to group and organize them by real-world topics.\n\n")

        for notebook_name, slug in categories_slugs.items():
            manifest_path = os.path.join(script_dir, f"notebook-{slug}-filelist.json")
            if not os.path.exists(manifest_path):
                continue
                
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest_data = json.load(f)
                
            files = manifest_data.get("files", [])
            rep.write(f"## {notebook_name} (Count: {len(files)})\n\n")

            # Group files in this notebook by sub-folder (literal macro-topics)
            subfolder_groups = {}
            for file_entry in files:
                rel_path = file_entry["relative_path"]
                full_path = os.path.join(workspace_root, rel_path)
                
                parts = rel_path.split('/')
                # Deduce folder topic
                if len(parts) > 2:
                    sub_topic = " -> ".join(parts[1:-1])
                elif len(parts) == 2:
                    sub_topic = "Root Folder"
                else:
                    sub_topic = "General"
                    
                if sub_topic not in subfolder_groups:
                    subfolder_groups[sub_topic] = []
                    
                # Read content for keywords and summary
                keywords = []
                summary = "No description available."
                if os.path.exists(full_path):
                    try:
                        with open(full_path, 'r', encoding='utf-8', errors='ignore') as doc_f:
                            content = doc_f.read()
                            keywords = clean_and_get_top_words(content)
                            summary = extract_literal_summary(content)
                    except Exception:
                        pass
                
                subfolder_groups[sub_topic].append({
                    "name": os.path.basename(rel_path),
                    "path": rel_path,
                    "keywords": keywords,
                    "summary": summary
                })

            for sub_topic, docs in sorted(subfolder_groups.items()):
                rep.write(f"### Sub-folder Topic: `{sub_topic}` (Count: {len(docs)})\n\n")
                for doc in sorted(docs, key=lambda x: x["name"]):
                    rep.write(f"* **[{doc['name']}](file:///{os.path.join(workspace_root, doc['path']).replace(os.sep, '/')})**\n")
                    if doc['keywords']:
                        kw_str = ", ".join(doc['keywords'])
                        rep.write(f"  - **Literal Keywords:** `{kw_str}`\n")
                    if doc['summary']:
                        rep.write(f"  - **Concept summary:** *{doc['summary']}*\n")
                    rep.write("\n")
                    
            rep.write("---\n\n")

    print("Successfully generated report.")

if __name__ == "__main__":
    main()
