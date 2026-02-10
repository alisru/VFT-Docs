
import json
import re
import os
from pathlib import Path

# --- Configuration ---
SOURCE_DIR = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia")
TARGET_JSON = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia_Kanon.json")

PLANES = [
    {"num": 1, "name": "Identity"},
    {"num": 2, "name": "Definition"},
    {"num": 3, "name": "Land"},
    {"num": 4, "name": "Drive"},
    {"num": 5, "name": "Method"},
    {"num": 6, "name": "Foundation"},
    {"num": 7, "name": "Result"}, 
]

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def parse_plane_markdown(file_path):
    print(f"Parsing Plane: {file_path}")
    if not file_path.exists():
        print(f"Error: File not found {file_path}")
        return {}

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    data = {}

    # 1. Plane Quote
    # > *"Quote"*
    # > — **Author**, *Source*
    quote_match = re.search(r'> \*"?(.*?)"?\*\n> [—-] \*\*(.*?)\*\*, \*(.*?)\*', content)
    if quote_match:
        data['quote'] = quote_match.group(1).strip()
        data['quote_author'] = quote_match.group(2).strip()
        data['quote_source'] = quote_match.group(3).strip()
    
    # 2. Extract Items
    # **(ID) Concept**; "Quote" - Author. *Source*, Year
    # > **Q:** *Question*
    #     Context
    #     Context
    #
    #     Meaning
    #     Meaning
    
    # Regex is tricky across lines. Let's split by "**(" which indicates start of item
    # But wait, Sense headers are ### Sense ...
    
    # Let's clean the content first
    # Remove the header part up to first item?
    
    items = {}
    
    # improved regex for item header
    item_pattern = re.compile(
        r'\*\*(?P<id>\(Run\.?.*?\))\s+(?P<concept>.*?)\*\*;\s+"?(?P<quote>.*?)"?\s+-\s+(?P<author>.*?)\.\s+\*(?P<source>.*?)\*,\s+(?P<year>.*?)\n',
        re.DOTALL
    )
    
    # Actually, let's iterate line by line or chunks
    # The structure is fairly rigid.
    
    # Strategy: Split by `**(` and process chunks
    chunks = content.split('**(')
    
    # We need to map extracted data back to the JSON structure (Planes -> Senses -> Items)
    # The JSON structure uses IDs like (Who.Who.Who). 
    
    extractions = {} # ID -> List of Concept Dicts
    
    for chunk in chunks[1:]: # Skip first chunk (header)
        # Restore the split char
        chunk = "**(" + chunk
        
        # Extract Header
        # Relaxed Regex to capture citation block generically
        # Format: **(ID) Concept**; "Quote" - Citation[, Year]
        # Handle various dashes: - (hyphen), – (en-dash), — (em-dash)
        # Year is optional (e.g. Traditional Consensus)
        header_match = re.match(
            r'\*\*(?P<id>\(.*?\))\s+(?P<concept>.*?)\*\*;\s+"?(?P<quote>[\s\S]*?)"?\s+[-–—]\s+(?P<citation>.*?)(?:,\s+(?P<year>.*?))?\n',
            chunk
        )
        
        if header_match:
            iid = header_match.group("id")
            concept_name = header_match.group("concept").strip()
            
            quote = header_match.group("quote").replace('\n', ' ').strip()
            citation_raw = header_match.group("citation").strip()
            year_raw = header_match.group("year")
            year = year_raw.strip() if year_raw else ""
            
            # Parse Citation (Author. *Source* vs *Source*)
            # Standard: Author. *Source*
            # Source Only: *Source*
            
            if "* " in citation_raw or " *" in citation_raw or citation_raw.startswith("*"):
                 # Has italics, likely source.
                 # Check for dot separator for author
                 if ". *" in citation_raw:
                     parts = citation_raw.split(". *")
                     author = parts[0].strip()
                     source = "*" + parts[1].strip() # Restore *
                     source = source.replace('*', '').strip() # Clean
                 else:
                     # Assume entire citation is source if it starts with * or just generic
                     author = "Unknown/Statement"
                     source = citation_raw.replace('*', '').strip()
            else:
                # No italics?
                author = citation_raw
                source = ""
            
            # Extract Body
            body = chunk[header_match.end():]
            
            # Check for Interrogative block quote and remove it
            body = re.sub(r'> \*\*Q:\*\* \*.*?\*\n', '', body)
            
            # Split Context and Meaning
            parts = [p.strip() for p in re.split(r'\n\s*\n', body) if p.strip()]
            
            context_parts = []
            meaning_parts = []
            found_meaning = False
            
            for p in parts:
                if p.startswith("```"): continue # Narrative block at end
                if p.startswith("###"): continue # Next Sense header
                
                clean_p = p.replace('    ', '').strip()
                if clean_p.startswith("This establishes") or clean_p.startswith("**This establishes"):
                    found_meaning = True
                
                if found_meaning:
                    meaning_parts.append(clean_p)
                else:
                    context_parts.append(clean_p)
            
            concept_data = {
                "name": concept_name,
                "quotes": [{
                    "text": quote,
                    "author": author,
                    "source": source,
                    "year": year
                }],
                "context_analysis": "\n\n".join(context_parts),
                "meaning_analysis": "\n\n".join(meaning_parts),
                "judgement": { # Default structure, to be filled by judgment parser
                    "moral_vector": 0.0,
                    "will_vector": 0.0,
                    "archetype_name": "Neutral",
                    "notes": ""
                }
            }
            
            if iid not in extractions:
                extractions[iid] = []
            extractions[iid].append(concept_data)
            
    # Narrative extraction remains same
    narratives = {}
    code_blocks = re.findall(r'```markdown\n(.*?)\n```', content, re.DOTALL)
    for block in code_blocks:
        if "The Narrative of Sense" in block:
             lines = block.strip().split('\n')
             header = lines[0]
             sid_match = re.search(r'Sense (q\d+)', header)
             if sid_match:
                 sid = sid_match.group(1)
                 text = '\n'.join([l.replace('> ', '', 1) for l in lines[1:]])
                 narratives[sid] = text.strip()
    
    return {
        "items": extractions,
        "narratives": narratives,
        "totality": "",
        "quote": data.get("quote"),
        "quote_author": data.get("quote_author"),
        "quote_source": data.get("quote_source")
    }

def parse_totality(content):
    # > **The Totality of Australia [PlaneName]** ...
    totality_match = re.search(r'> \*\*The Totality of Australia .*?\*\*\s+(.*)', content)
    if totality_match:
        return totality_match.group(1).strip()
    return ""

def parse_judgment_markdown(file_path):
    print(f"Parsing Judgment: {file_path}")
    if not file_path.exists():
        print(f"Warning: Judgment file not found {file_path}")
        return {}
        
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    judgments = {} # ID -> List of judgment dicts (keyed by concept name for matching)
    
    # Table parsing state
    # Look for lines starting with |
    
    for line in lines:
        line = line.strip()
        if not line.startswith('|'): continue
        if '---' in line: continue # Separator line
        if 'Vector' in line and 'Entry' in line: continue # Header line
        
        # Split by pipe
        cols = [c.strip() for c in line.split('|')]
        # cols[0] is empty (before first pipe), cols[1] is Vector ID, cols[2] is Entry...
        if len(cols) < 6: continue
        
        vector_id_raw = cols[1]
        entry_raw = cols[2]
        moral_raw = cols[3]
        will_raw = cols[4]
        judgment_raw = cols[5]
        
        # Process ID: Who.Who.Who -> (Who.Who.Who)
        if not vector_id_raw.startswith('('):
            iid = f"({vector_id_raw})"
        else:
            iid = vector_id_raw
            
        # Process Entry: **Mateship** -> Mateship
        concept_name = entry_raw.replace('*', '').strip()
        
        # Process Vectors
        try:
            # Handle symbols like ± or unicode chars if any?
            # Assuming +0.7, -0.9 etc.
            moral_val = float(re.sub(r'[^\d\.\+\-]', '', moral_raw))
        except:
            moral_val = 0.0
            
        try:
            will_val = float(re.sub(r'[^\d\.\+\-]', '', will_raw))
        except:
            will_val = 0.0
            
        # Process Judgment: **Archetype** — Notes
        # Split by em-dash or dash
        # regex for bold archetype
        arch_match = re.match(r'\*\*(.*?)\*\*', judgment_raw)
        if arch_match:
            archetype = arch_match.group(1)
            # Notes is the rest, extract after ** and -
            notes = judgment_raw[arch_match.end():].lstrip(' —-').strip()
        else:
            archetype = "Neutral"
            notes = judgment_raw
            
        j_obj = {
            "concept_name": concept_name,
            "moral_vector": moral_val,
            "will_vector": will_val,
            "archetype_name": archetype,
            "notes": notes
        }
        
        if iid not in judgments:
            judgments[iid] = []
        judgments[iid].append(j_obj)
        
    return judgments

def main():
    print("Starting Migration...")
    if not TARGET_JSON.exists():
        print("Target JSON not found. Please run 'python kanon_manager.py init Australia' first.")
        return

    kanon_data = load_json(TARGET_JSON)
    
    for p_config in PLANES:
        p_num = p_config["num"]
        p_name = p_config["name"]
        
        # Define file paths
        plane_md = SOURCE_DIR / f"Australian_Kanon_Plane_{p_num}_{p_name}.md"
        judg_md = SOURCE_DIR / f"Australian_Kanon_Plane_{p_num}_{p_name}_JUDGMENT.md"
        
        # Parse data
        plane_data = parse_plane_markdown(plane_md)
        judg_data = parse_judgment_markdown(judg_md)
        if plane_md.exists():
            plane_data["totality"] = parse_totality(open(plane_md, 'r', encoding='utf-8').read())
        
        # Update JSON
        target_plane = None
        for p in kanon_data["planes"]:
            if str(p.get("id")) == str(p_num):
                target_plane = p
                break
        
        if not target_plane:
            print(f"Error: Plane {p_num} not found in JSON.")
            continue
            
        # Update Plane level data
        if plane_data.get("quote"): target_plane["quote"] = plane_data["quote"]
        if plane_data.get("quote_author"): target_plane["quote_author"] = plane_data["quote_author"]
        if plane_data.get("quote_source"): target_plane["quote_source"] = plane_data["quote_source"]
        if plane_data.get("totality"): target_plane["totality_narrative"] = plane_data["totality"]
        
        # Update Items and Concepts
        extracted_items = plane_data.get("items", {}) # ID -> List of Concepts
        extracted_narratives = plane_data.get("narratives", {})
        
        for sense in target_plane.get("senses", []):
            sid = sense.get("id")
            
            # Update Sense Narrative
            if sid in extracted_narratives:
                sense["narrative"] = extracted_narratives[sid]
                
            for item in sense.get("items", []):
                iid = item.get("id")
                
                # Check for updates in extracted items
                if iid in extracted_items:
                    # REPLACE the concepts list with extracted ones
                    # This supports multiple concepts (Standard + FN)
                    item["concepts"] = extracted_items[iid]
                    
                    # Now Merge Judgment Data
                    if iid in judg_data:
                        judgments = judg_data[iid] # List of judgment dicts
                        
                        # For each concept in the item, find matching judgment
                        for concept in item["concepts"]:
                            c_name = concept["name"]
                            
                            # Find match
                            # Try exact match first
                            match = next((j for j in judgments if j["concept_name"] == c_name), None)
                            
                            # Try fuzzy match if exact fails (e.g. handle [FN] tag differences)
                            if not match:
                                # example: "Continuity" vs "Continuity [FN]"
                                match = next((j for j in judgments if j["concept_name"] in c_name or c_name in j["concept_name"]), None)
                            
                            if match:
                                concept["judgement"] = {
                                    "moral_vector": match["moral_vector"],
                                    "will_vector": match["will_vector"],
                                    "archetype_name": match["archetype_name"],
                                    "notes": match["notes"]
                                }
                            else:
                                print(f"Warning: No judgment match for concept '{c_name}' in item {iid}")
                else:
                    # Item not found in markdown (placeholder in JSON?)
                    pass

    save_json(TARGET_JSON, kanon_data)
    print("Migration Complete.")

if __name__ == "__main__":
    main()
