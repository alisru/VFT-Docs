import os
import json
import re

PHILOSOPHICAL_TAGS_PATTERNS = {
    "Epistemology": [
        r'\bepistem[o|i]\w*', r'\bknowledge\b', r'\btruth\b', r'\bfidelity\b', r'\bbelief\b', 
        r'\bjustification\b', r'\bskeptic[i|y]\w*', r'\bcognitive\b', r'\bcognition\b'
    ],
    "Ontology": [
        r'\bontolog\w*', r'\bbeing\b', r'\bexist\w*', r'\bsubstance\b', r'\breality\b', 
        r'\bactualism\b', r'\bactualist\b', r'\bessence\b', r'\bmanifold\b'
    ],
    "Metaphysics": [
        r'\bmetaphys\w*', r'\btranscend[e|e]\w*', r'\bidealism\b', r'\bmonism\b', 
        r'\bdualism\b', r'\bimmaterial\b', r'\bpossibility space\b'
    ],
    "Hermeneutics": [
        r'\bhermeneut\w*', r'\bexeges\w*', r'\binterpret\w*', r'\bscriptur\w*', 
        r'\btranslat\w*', r'\bbiblic\w*', r'\btextual\b', r'\bverse\w*', r'\bgematria\b'
    ],
    "Eschatology": [
        r'\beschatolog\w*', r'\bend times\b', r'\bjudgment\b', r'\bresurrection\b', 
        r'\bapocalypse\b', r'\bapocalyptic\b', r'\bfinal destiny\b', r'\bstasis\b'
    ],
    "Cosmology": [
        r'\bcosmolog\w*', r'\buniverse\b', r'\bcreation\b', r'\borigin\b', 
        r'\bspacetim\w*', r'\bthermodynam\w*', r'\bentropy\b'
    ],
    "Phenomenology": [
        r'\bphenomenolog\w*', r'\bsubjective\b', r'\bexperience\b', r'\bperception\b', 
        r'\bawareness\b', r'\bqualia\b', r'\bsensation\b'
    ],
    "Ethics": [
        r'\bethic\w*', r'\bmoral\w*', r'\bgood\b', r'\bevil\b', r'\bjustice\b', 
        r'\brighteous\w*', r'\bvirtue\b', r'\bvice\b', r'\bduty\b'
    ],
    "Axiology": [
        r'\baxiolog\w*', r'\bvalue\b', r'\bworth\b', r'\bpreference\b', r'\butility\b', 
        r'\bprice\b', r'\bscarcity\b'
    ],
    "Gnosticism": [
        r'\bgnost[i|y]\w*', r'\bgnosis\b', r'\bsecret knowledge\b', r'\bdemiurge\b', 
        r'\barchon\w*', r'\bdivine spark\b', r'\besoteric\b'
    ],
    "Teleology": [
        r'\bteleolog\w*', r'\bpurpose\b', r'\bgoal\b', r'\bdesign\b', r'\bintention\w*', 
        r'\bend\b'
    ],
    "Soteriology": [
        r'\bsoteriolog\w*', r'\bsalvation\b', r'\bredempt\w*', r'\batonement\b', 
        r'\bgrace\b', r'\bsavior\b'
    ]
}

def tag_document(text):
    text_lower = text.lower()
    matched_tags = []
    
    for tag, patterns in PHILOSOPHICAL_TAGS_PATTERNS.items():
        match_count = 0
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            match_count += len(matches)
            
        # If the key philosophical indicators appear enough times, assign the tag
        if match_count >= 3:
            matched_tags.append((tag, match_count))
            
    # Sort tags by match frequency
    matched_tags.sort(key=lambda x: x[1], reverse=True)
    return [t[0] for t in matched_tags[:4]] # Limit to top 4 tags

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

    report_path = os.path.join(script_dir, "notebook_philosophical_tags.md")
    print(f"Generating philosophical tags report at {report_path}...", flush=True)

    with open(report_path, 'w', encoding='utf-8') as rep:
        rep.write("# Philosophical Tag Index of Notebook Documents\n\n")
        rep.write("This index categorizes your repository files by traditional philosophical disciplines (e.g., Epistemology, Ontology, Hermeneutics, Gnosticism, Eschatology) to help contextualize the philosophical foundations of your Vector Field Theory and Actualism documents.\n\n")

        for notebook_name, slug in categories_slugs.items():
            manifest_path = os.path.join(script_dir, f"notebook-{slug}-filelist.json")
            if not os.path.exists(manifest_path):
                continue
                
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest_data = json.load(f)
                
            files = manifest_data.get("files", [])
            rep.write(f"## {notebook_name} (Count: {len(files)})\n\n")

            # Store tags count for summary
            tag_distribution = {}
            tagged_docs = []

            for file_entry in files:
                rel_path = file_entry["relative_path"]
                full_path = os.path.join(workspace_root, rel_path)
                
                tags = []
                if os.path.exists(full_path):
                    try:
                        with open(full_path, 'r', encoding='utf-8', errors='ignore') as doc_f:
                            content = doc_f.read()
                            tags = tag_document(content)
                    except Exception:
                        pass
                
                if not tags:
                    tags = ["General"]
                    
                for t in tags:
                    tag_distribution[t] = tag_distribution.get(t, 0) + 1
                    
                tagged_docs.append({
                    "name": os.path.basename(rel_path),
                    "path": rel_path,
                    "tags": tags
                })

            # Print Tag distribution summary for this notebook
            rep.write("### Tag Distribution:\n")
            sorted_dist = sorted(tag_distribution.items(), key=lambda x: x[1], reverse=True)
            dist_str = ", ".join(f"`{t}` ({c})" for t, c in sorted_dist)
            rep.write(f"{dist_str}\n\n")

            # Group files by primary tag
            tag_groups = {}
            for doc in tagged_docs:
                primary = doc["tags"][0]
                if primary not in tag_groups:
                    tag_groups[primary] = []
                tag_groups[primary].append(doc)

            for tag, docs in sorted(tag_groups.items()):
                rep.write(f"### Tag: `{tag}` (Count: {len(docs)})\n\n")
                for doc in sorted(docs, key=lambda x: x["name"]):
                    other_tags = [t for t in doc["tags"] if t != tag]
                    other_tags_str = f" (Also: {', '.join(other_tags)})" if other_tags else ""
                    rep.write(f"* **[{doc['name']}](file:///{os.path.join(workspace_root, doc['path']).replace(os.sep, '/')})**{other_tags_str}\n")
                rep.write("\n")
                
            rep.write("---\n\n")

    print("Successfully generated philosophical tags report.")

if __name__ == "__main__":
    main()
