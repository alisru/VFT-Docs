
import argparse
import json
import os
import sys
import shutil
import re
from pathlib import Path

# Try to import jsonschema
try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

# --- Configuration ---
SCRIPT_DIR = Path(__file__).parent
TEMPLATE_PATH = SCRIPT_DIR / "7x7x7_kanon_template.json"
SCHEMA_PATH = SCRIPT_DIR / "7x7x7_kanon_schema.json"
INTERROGATIVE_PATH = SCRIPT_DIR.parent / "Actualism/Theology & Spirituality/Planes/interrogative_7x7x7_semantic.md"

PLANES_CONFIG = [
    {"num": 1, "id_label": "Who", "name": "Identity", "file_suffix": "Plane_1_Identity.md"},
    {"num": 2, "id_label": "What", "name": "Definition", "file_suffix": "Plane_2_Definition.md"},
    {"num": 3, "id_label": "Where", "name": "Land", "file_suffix": "Plane_3_Land.md"},
    {"num": 4, "id_label": "Why", "name": "Drive", "file_suffix": "Plane_4_Drive.md"},
    {"num": 5, "id_label": "How", "name": "Method", "file_suffix": "Plane_5_Method.md"},
    {"num": 6, "id_label": "Cause", "name": "Foundation", "file_suffix": "Plane_6_Foundation.md"},
    {"num": 7, "id_label": "Effect", "name": "Result", "file_suffix": "Plane_7_Result.md"},
]

# --- Helper Functions ---

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def count_sentences(text):
    if not text:
        return 0
    # Split by .!? followed by space or end of string
    sentences = re.split(r'[.!?]+(?:\s+|$)', text)
    return len([s for s in sentences if s.strip()])

def load_interrogatives(path):
    """
    Parses the 7x7x7 interrogative markdown file.
    Returns a dict mapping ID (e.g., '1.1.1') to the question text.
    """
    if not path.exists():
        print_warning(f"Interrogative file not found at {path}")
        return {}

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find lines like: - **1.1.1 - Who:** Question text?
    # Pattern: - \*\*(?P<id>\d+\.\d+\.\d+) - .*?:\*\* (?P<question>.*)
    pattern = re.compile(r'- \*\*(?P<id>\d+\.\d+\.\d+) - .*?:\*\* (?P<question>.*)')
    
    mapping = {}
    for line in content.split('\n'):
        match = pattern.search(line)
        if match:
            # Map 1.1.1 to Who.Who.Who semantics
            # Actually, the ID is sufficient if we have a converter or if we just use the ID from the file.
            # But the template uses (Who.Who.Who).
            # We need a mapper: 1=Who, 2=What, 3=Where, 4=Why, 5=How, 6=Cause, 7=Effect.
            
            nid = match.group("id")
            question = match.group("question").strip()
            mapping[nid] = question
            
    return mapping

def numeric_id_to_semantic(nid):
    # 1.1.1 -> Who.Who.Who
    vectors = ["Who", "What", "Where", "Why", "How", "Cause", "Effect"]
    parts = nid.split('.')
    if len(parts) != 3: return nid
    
    try:
        p1 = vectors[int(parts[0]) - 1]
        p2 = vectors[int(parts[1]) - 1]
        p3 = vectors[int(parts[2]) - 1]
        return f"({p1}.{p2}.{p3})"
    except (IndexError, ValueError):
        return nid

def print_error(msg):
    print(f"\033[91m[ERROR]\033[0m {msg}")

def print_success(msg):
    print(f"\033[92m[SUCCESS]\033[0m {msg}")

def print_warning(msg):
    print(f"\033[93m[WARNING]\033[0m {msg}")

# --- Commands ---

def cmd_init(args):
    nation_name = args.nation
    output_filename = f"{nation_name}_Kanon.json"
    output_path = Path(os.getcwd()) / output_filename
    
    if output_path.exists() and not args.force:
        print_error(f"File '{output_filename}' already exists. Use --force to overwrite.")
        return

    if not TEMPLATE_PATH.exists():
        print_error(f"Template file not found at {TEMPLATE_PATH}")
        return

    print(f"Initializing Kanon for '{nation_name}'...")
    
    # Load Interrogatives
    qs = load_interrogatives(INTERROGATIVE_PATH)
    semantic_map = {numeric_id_to_semantic(k): v for k, v in qs.items()}
    
    # Load template
    data = load_json(TEMPLATE_PATH)
    data["nation"] = nation_name
    
    # Inject Questions into Template Data
    for plane in data.get("planes", []):
        for sense in plane.get("senses", []):
            for item in sense.get("items", []):
                iid = item.get("id") # (Who.Who.Who)
                if iid in semantic_map:
                    item["interrogative"] = semantic_map[iid]
                else:
                    item["interrogative"] = "[Question not found in source]"

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        
    print_success(f"Created '{output_filename}' with 343 Interrogatives injected. You can now edit this file.")

def cmd_validate(args):
    file_path = Path(args.file)
    if not file_path.exists():
        print_error(f"File '{file_path}' not found.")
        return

    print(f"Validating '{file_path}'...")
    
    data = load_json(file_path)
    
    # 1. Schema Validation
    if HAS_JSONSCHEMA:
        if SCHEMA_PATH.exists():
            schema = load_json(SCHEMA_PATH)
            try:
                jsonschema.validate(instance=data, schema=schema)
                print_success("JSON Schema Validation Passed.")
            except jsonschema.exceptions.ValidationError as e:
                print_error(f"Schema Validation Failed: {e.message}")
                print(f"Path: {list(e.path)}")
                return
        else:
            print_warning(f"Schema file not found at {SCHEMA_PATH}. Skipping schema validation.")
    else:
        print_warning("jsonschema library not installed. Skipping schema validation.")

    # 2. Semantic Validation (Sentence Counts & Integrity)
    errors = 0
    warnings = 0
    
    nation = data.get("nation", "Unknown")
    planes = data.get("planes", [])
    
    if len(planes) != 7:
        print_error(f"Expected 7 Planes, found {len(planes)}.")
        errors += 1
        
    for p_idx, plane in enumerate(planes):
        pid = plane.get("id", str(p_idx+1))
        pname = plane.get("name", "Unknown")
        
        # Check Plane Narrative
        totality = plane.get("totality_narrative", "")
        if count_sentences(totality) < 2: # Loose check for totality
             print_warning(f"Plane {pid} ({pname}): Totality Narrative is very short ({count_sentences(totality)} sentences).")
             warnings += 1

        senses = plane.get("senses", [])
        if len(senses) != 7:
            print_error(f"Plane {pid} ({pname}): Expected 7 Senses, found {len(senses)}.")
            errors += 1
            
        for s_idx, sense in enumerate(senses):
            sid = sense.get("id", f"q{s_idx+1}")
            
            # Check Sense Narrative
            narrative = sense.get("narrative", "")
            if count_sentences(narrative) < 1:
                print_warning(f"Plane {pid} -> Sense {sid}: Narrative missing or empty.")
                warnings += 1

            items = sense.get("items", [])
            if len(items) != 7:
                print_error(f"Plane {pid} -> Sense {sid}: Expected 7 Items, found {len(items)}.")
                errors += 1
                
            for item in items:
                iid = item.get("id", "Unknown")
                concepts = item.get("concepts", [])
                
                if not concepts:
                     print_error(f"{iid}: No concepts defined.")
                     errors += 1
                     continue

                # We only check the first concept as the primary one for now
                concept = concepts[0]
                cname = concept.get("name", "")
                
                if "[Concept Name]" in cname:
                     print_warning(f"{iid}: Placeholder '{cname}' detected.")
                     warnings += 1

                ctx = concept.get("context_analysis", "")
                meaning = concept.get("meaning_analysis", "")
                
                total_sentences = count_sentences(ctx) + count_sentences(meaning)
                
                if total_sentences < 7:
                    print_error(f"{iid} ({cname}): Insufficient depth. {total_sentences}/7 sentences.")
                    errors += 1
                
                # Check "This establishes..." formula
                if not meaning.strip().startswith("This establishes"):
                    print_warning(f"{iid} ({cname}): Meaning analysis should start with 'This establishes...'.")
                    warnings += 1

    if errors > 0:
        print_error(f"Validation Failed with {errors} errors and {warnings} warnings.")
        sys.exit(1)
    else:
        print_success(f"Validation Passed! ({warnings} warnings)")

def cmd_export(args):
    file_path = Path(args.file)
    if not file_path.exists():
        print_error(f"File '{file_path}' not found.")
        return
        
    # Validate first (unless skipped? No, strict enforcement)
    # Actually, let's allow export even if validation fails slightly, but warn.
    # User might want to see the output.
    
    data = load_json(file_path)
    nation = data.get("nation", "Nation")
    planes = data.get("planes", [])
    
    output_dir = Path(os.getcwd())
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        
    print(f"Exporting Markdown files for '{nation}' to {output_dir}...")
    
    for i, plane in enumerate(planes):
        # Match plane config
        config = PLANES_CONFIG[i]
        
        # Override name from JSON if different (but keeping 1-7 structure)
        p_name = plane.get("name", config["name"])
        p_vector = plane.get("vector", config["id_label"])
        
        filename = f"{nation}_{config['file_suffix']}"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # HEADER
            f.write(f"# The {nation} Kanon:\n")
            f.write(f"# Plane {config['num']}; Values of {nation} {p_name}\n\n")
            
            quote = plane.get('quote', '')
            q_auth = plane.get('quote_author', '')
            q_src = plane.get('quote_source', '')
            
            f.write(f"> *\"{quote}\"*\n")
            f.write(f"> — **{q_auth}**, *{q_src}*\n\n")
            
            f.write(f"## THE PLANE OF {p_name.upper()} ({p_vector.upper()})\n\n")
            
            # SENSES
            for sense in plane.get("senses", []):
                s_id = sense.get("id")
                s_vec = sense.get("vector")
                s_desc = sense.get("description") # "The Who of..."
                
                f.write(f"### Sense {s_id}: {s_desc}\n\n")
                
                for item in sense.get("items", []):
                    item_id = item.get("id") # (Who.Who.Who)
                    
                    # Get primary concept
                    concept = item.get("concepts", [{}])[0]
                    c_name = concept.get("name")
                    
                    # Quotes (Primary)
                    q_list = concept.get("quotes", [{}])
                    main_q = q_list[0] if q_list else {}
                    q_text = main_q.get("text", "")
                    q_auth = main_q.get("author", "")
                    q_src = main_q.get("source", "")
                    q_year = main_q.get("year", "")
                    
                    context = concept.get("context_analysis", "")
                    meaning = concept.get("meaning_analysis", "")
                    
                    context = concept.get("context_analysis", "")
                    meaning = concept.get("meaning_analysis", "")
                    
                    # Format: **(ID) Name**; "Quote" - Author. *Source*, Year
                    f.write(f"**{item_id} {c_name}**; \"{q_text}\" - {q_auth}. *{q_src}*, {q_year}\n\n")
                    
                    # Inject Interrogative Question as a blockquote or bold line?
                    # "I want it to answer these questions" implies visibility.
                    # Let's put it at the start of the context block as a bolded question?
                    # Or as a > blockquote right under the header?
                    q_val = item.get("interrogative")
                    if q_val:
                        f.write(f"> **Q:** *{q_val}*\n\n")

                    # Indented Paragraphs (4 spaces)
                    # Handle multiline strings in JSON safely
                    ctx_lines = context.split('\n')
                    for line in ctx_lines:
                        if line.strip():
                            f.write(f"    {line.strip()}\n")
                    f.write("\n")
                    
                    meaning_lines = meaning.split('\n')
                    for line in meaning_lines:
                        if line.strip():
                            f.write(f"    {line.strip()}\n")
                    f.write("\n")
                    
                # Sense Narrative
                narrative = sense.get("narrative", "")
                f.write("```markdown\n")
                # Add the bold header expected by site generator
                # "> **The Narrative of [Concept] (The [Vector] of the [Plane] ([Vector])):
                # Actually, the site generator looks for `> **The Narrative`
                # We can reconstruct a standard header or just use the narrative text if it includes it.
                # The template usually has the narrative text only. Let's prepend the header if missing?
                # The schema description says: "Summary block...".
                # The site generator uses regex `(> \*\*The Narrative.*?)`.
                # So we MUST start with `> **The Narrative`.
                
                if not narrative.strip().startswith("> **The Narrative"):
                    # Construct header
                    # We need the Sense Name/Concept. Usually buried in description or we make generic.
                    f.write(f"> **The Narrative of Sense {s_id} ({s_desc}):**\n")
                    f.write(f"> {narrative}\n")
                else:
                     f.write(f"{narrative}\n")
                f.write("```\n\n")
            
            # Totality Narrative
            totality = plane.get("totality_narrative", "")
            f.write(f"> **The Totality of {nation} {p_name}** {totality}\n")
            
            print(f"Generated {filename}")

    print_success("Export Complete.")

def main():
    parser = argparse.ArgumentParser(description="Kanon Manager: Manage 343 National Kanon Files")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Init
    parser_init = subparsers.add_parser("init", help="Initialize a new Kanon JSON file")
    parser_init.add_argument("nation", help="Name of the Nation (e.g., Australia, America)")
    parser_init.add_argument("--force", action="store_true", help="Overwrite existing file")
    
    # Validate
    parser_val = subparsers.add_parser("validate", help="Validate a Kanon JSON file")
    parser_val.add_argument("file", help="Path to the JSON file")
    
    # Export
    parser_exp = subparsers.add_parser("export", help="Export JSON to Markdown files")
    parser_exp.add_argument("file", help="Path to the JSON file")
    parser_exp.add_argument("--output", help="Output directory (default: current directory)")
    
    args = parser.parse_args()
    
    if args.command == "init":
        cmd_init(args)
    elif args.command == "validate":
        cmd_validate(args)
    elif args.command == "export":
        cmd_export(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
