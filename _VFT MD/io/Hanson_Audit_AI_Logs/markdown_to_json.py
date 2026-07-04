import re
import json
from pathlib import Path

# Paths
# The audit was split into one file per plane (plus a shared sources file) to avoid
# full-document reads blowing past tool token limits during editing sessions.
# These are concatenated below, in order, to reconstruct the single content string
# the rest of this script's parsing logic expects -- the parsing itself is unchanged.
IO_DIR = Path("e:/Vector Field Theory/VFT Docs/_VFT MD/io")
HANSON_DIR = IO_DIR / "Hanson_Audit"
AUDIT_FILES = [
    HANSON_DIR / "Plane_1_Identity.md",
    HANSON_DIR / "Plane_2_Definition.md",
    HANSON_DIR / "Plane_3_Land.md",
    HANSON_DIR / "Plane_4_Drive.md",
    HANSON_DIR / "Plane_5_Method.md",
    HANSON_DIR / "Plane_6_Foundation.md",
    HANSON_DIR / "Plane_7_Result.md",
]
SOURCES_FILE = HANSON_DIR / "Sources.md"
KANON_DIR = Path("e:/Vector Field Theory/VFT Docs/_VFT MD/WWSUTRU/Australia/Aus Kanon/compact JSON")
OUTPUT_JSON = HANSON_DIR / "Hegemonic Audit_ Pauline Hanson.json"

PLANES = [
    (1, "Identity", "Who"),
    (2, "Definition", "What"),
    (3, "Land", "Where"),
    (4, "Drive", "Why"),
    (5, "Method", "How"),
    (6, "Foundation", "Cause"),
    (7, "Result", "Effect")
]

def load_canonical_kanon():
    # Load all canonical vectors across the 7 planes
    canonical = {}
    for plane_num, plane_name, plane_prefix in PLANES:
        file_name = f"Plane_{plane_num}_{plane_name}_compact.json"
        file_path = KANON_DIR / file_name
        if not file_path.exists():
            raise FileNotFoundError(f"Missing Kanon file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                addr = item["address"]
                if addr not in canonical:
                    canonical[addr] = []
                canonical[addr].append({
                    "name": item["name"],
                    "v": item["coordinates"]["v"],
                    "psi": item["coordinates"]["psi"],
                    "plane": plane_num,
                    "plane_name": plane_name
                })
    return canonical

def parse_audit_to_json():
    print("Loading canonical Kanon...")
    canonical = load_canonical_kanon()

    print("Reading split audit files (7 planes + sources)...")
    parts_content = []
    for audit_file in AUDIT_FILES:
        if not audit_file.exists():
            raise FileNotFoundError(f"Missing plane file: {audit_file}")
        with open(audit_file, 'r', encoding='utf-8') as f:
            parts_content.append(f.read())
    if not SOURCES_FILE.exists():
        raise FileNotFoundError(f"Missing sources file: {SOURCES_FILE}")
    with open(SOURCES_FILE, 'r', encoding='utf-8') as f:
        parts_content.append(f.read())
    content = "\n\n".join(parts_content)

    # Split by plane headers to process plane by plane
    plane_headers = [
        r'# \*\*Plane 1: Who\*\*',
        r'# \*\*Plane 2, Possible What\*\*',
        r'# \*\*Plane 3, Location where\*\*',
        r'# \*\*Plane 4, Lyrical Why\*\*',
        r'# \*\*Plane 5, Logical How\*\*',
        r'# \*\*Plane 6, Historical Cause\*\*',
        r'# \*\*Plane 7, Emotional Effect\*\*'
    ]
    split_pat = '|'.join(plane_headers)
    parts = re.split(split_pat, content)
    
    if len(parts) < 8:
        print(f"Error: Split found only {len(parts)} parts. Check plane headers.")
        return

    # Regex to match vector headers
    header_pattern = r'\*\*\(?([a-zA-Z\.]+)\)?\s+(.+?)\s+\(υ:\s*\\?([\+\-]?\d*\.?\d+),\s*ψ:\s*\\?([\+\-]?\d*\.?\d+)\):\s*([A-Z/]+)\.\*\*(?:\s+\*\*Quote:\*\*\s*(.*))?'

    # Parse source definitions at the end of the document
    sources = {}
    sources_pattern = r'^\[\^([a-zA-Z0-9_\-]+)\]:.*?(https?://\S+?)/?\s*$'
    for m in re.finditer(sources_pattern, content, flags=re.MULTILINE):
        sources[m.group(1)] = m.group(2).strip()

    audit_data = {
        "preface": parts[0].strip(),
        "planes": [],
        "sources": sources
    }

    for plane_idx in range(1, 8):
        plane_num, plane_name, plane_prefix = PLANES[plane_idx - 1]
        plane_text = parts[plane_idx]
        
        # Split out the final verdict section from the vectors section to avoid bleeding into the last vector node
        verdict_split = re.split(r'##\s*\*\*Final Forensic Verdict:', plane_text, flags=re.IGNORECASE)
        vectors_text = verdict_split[0]
        verdict_text = verdict_split[1] if len(verdict_split) > 1 else ""
        
        matches = list(re.finditer(header_pattern, vectors_text))
        plane_vectors = []

        print(f"Parsing Plane {plane_num}: {plane_name} (found {len(matches)} headers)...")

        for idx, match in enumerate(matches):
            address = match.group(1).strip()
            stated_name = match.group(2).strip().replace('\\', '')
            stated_v = float(match.group(3).strip().replace('\\', '').replace('+', ''))
            stated_psi = float(match.group(4).strip().replace('\\', '').replace('+', ''))
            verdict = match.group(5).strip()
            quote_text = match.group(6).strip() if match.group(6) else ""

            start_pos = match.end()
            end_pos = matches[idx + 1].start() if idx + 1 < len(matches) else len(vectors_text)
            block_text = vectors_text[start_pos:end_pos].strip()

            paragraphs = [p.strip() for p in block_text.split('\n\n') if p.strip()]
            
            description_paras = []
            justification_paras = []
            actuality_paras = []

            current_section = "description"
            for p in paragraphs:
                if p.startswith("##") or p.startswith("#"):
                    continue
                if p.startswith("Description:") or p.startswith("Brief:"):
                    current_section = "description"
                    p_cleaned = re.sub(r'^(Description:|Brief:)\s*', '', p)
                    if p_cleaned:
                        description_paras.append(p_cleaned)
                elif p.startswith("Justification:") or p.startswith("**Justification:**"):
                    current_section = "justification"
                    p_cleaned = re.sub(r'^(\*\*Justification:\*\*|Justification:)\s*', '', p)
                    if p_cleaned:
                        justification_paras.append(p_cleaned)
                elif p.startswith("Actuality:") or p.startswith("**Actuality:**"):
                    current_section = "actuality"
                    p_cleaned = re.sub(r'^(\*\*Actuality:\*\*|Actuality:)\s*', '', p)
                    if p_cleaned:
                        actuality_paras.append(p_cleaned)
                else:
                    if current_section == "description":
                        description_paras.append(p)
                    elif current_section == "justification":
                        justification_paras.append(p)
                    elif current_section == "actuality":
                        actuality_paras.append(p)

            description_str = "\n\n".join(description_paras)
            justification_str = "\n\n".join(justification_paras)
            actuality_str = "\n\n".join(actuality_paras)

            canonical_refs = canonical.get(address, [])
            canonical_match = None
            if len(canonical_refs) == 1:
                canonical_match = canonical_refs[0]
            elif len(canonical_refs) > 1:
                # Match based strictly on whether "first nations" or "perspective" is in the header's stated name
                is_stated_fn = "first nations" in stated_name.lower() or "perspective" in stated_name.lower()
                for ref in canonical_refs:
                    ref_name_lower = ref["name"].lower()
                    is_ref_fn = "first nations" in ref_name_lower or "perspective" in ref_name_lower
                    if is_stated_fn == is_ref_fn:
                        canonical_match = ref
                        break
                if not canonical_match:
                    canonical_match = canonical_refs[0]

            canonical_name = canonical_match["name"] if canonical_match else stated_name
            canonical_v = canonical_match["v"] if canonical_match else stated_v
            canonical_psi = canonical_match["psi"] if canonical_match else stated_psi

            vector_obj = {
                "address": address,
                "name": canonical_name,
                "coordinates": {
                    "v": canonical_v,
                    "psi": canonical_psi
                },
                "verdict": verdict,
                "quote": quote_text,
                "description": description_str,
                "justification": justification_str,
                "actuality": actuality_str,
                "meta": {
                    "stated_name": stated_name,
                    "stated_coordinates": {
                        "v": stated_v,
                        "psi": stated_psi
                    },
                    "name_mismatch": canonical_name.lower() != stated_name.lower(),
                    "coord_mismatch": abs(canonical_v - stated_v) > 0.01 or abs(canonical_psi - stated_psi) > 0.01
                }
            }
            plane_vectors.append(vector_obj)
            
        # Parse final verdict properties
        final_verdict_info = {
            "score": "",
            "alignment": "",
            "morality": "",
            "will": "",
            "quadrant": "",
            "statement": ""
        }
        if verdict_text:
            score_match = re.search(r'\*\*Plane\s*\d+\s+\w+\s+Score:\*\*\s*(.+)', verdict_text, re.IGNORECASE)
            align_match = re.search(r'\*\*Percentage\s+Australian\s+Alignment:\*\*\s*(.+)', verdict_text, re.IGNORECASE)
            morality_match = re.search(r'\*\*Average\s+Morality\s+\(υ\):\*\*\s*(.+)', verdict_text, re.IGNORECASE)
            will_match = re.search(r'\*\*Average\s+Will\s+\(ψ\):\*\*\s*(.+)', verdict_text, re.IGNORECASE)
            quad_match = re.search(r'\*\*Quadrant\s+Placement:\*\*\s*(.+)', verdict_text, re.IGNORECASE)
            stmt_match = re.search(r'\*\*Final\s+Statement:\*\*\s*(.+)', verdict_text, re.IGNORECASE)
            
            if score_match: final_verdict_info["score"] = score_match.group(1).strip().replace('\\', '')
            if align_match: final_verdict_info["alignment"] = align_match.group(1).strip().replace('\\', '')
            if morality_match: final_verdict_info["morality"] = morality_match.group(1).strip().replace('\\', '')
            if will_match: final_verdict_info["will"] = will_match.group(1).strip().replace('\\', '')
            if quad_match: final_verdict_info["quadrant"] = quad_match.group(1).strip().replace('\\', '')
            if stmt_match: final_verdict_info["statement"] = stmt_match.group(1).strip().replace('\\', '')

        audit_data["planes"].append({
            "plane_num": plane_num,
            "plane_name": plane_name,
            "vectors": plane_vectors,
            "final_verdict": final_verdict_info
        })

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(audit_data, f, indent=2, ensure_ascii=False)

    print(f"Parsed successfully! JSON saved to: {OUTPUT_JSON}")

if __name__ == "__main__":
    parse_audit_to_json()
