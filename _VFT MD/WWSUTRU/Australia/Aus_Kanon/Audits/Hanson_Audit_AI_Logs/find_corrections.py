import os
import re

def clean_text(text):
    # Remove timestamps like "3:483 minutes, 48 seconds" or "4:124 minutes, 12 seconds"
    # Even if glued to a word (e.g., "secondschange" -> "change")
    text = re.sub(r'\d+:\d+\d*\s+minutes?,\s+\d+\s+seconds?', ' ', text)
    text = re.sub(r'seconds([a-zA-Z])', r' \1', text)
    
    text = text.replace("--", " ").replace("—", " ").replace("–", " ").replace("-", " ")
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return " ".join(text.split())

def clean_target_quote(quote):
    # Strip bracketed positions first, but keep reference keys for now
    quote = re.sub(r'\[Documented position:[^\]]*\]', '', quote)
    quote_match = re.search(r'^\\?"(.*?)\\?"\s*-(.*)$', quote.strip())
    if not quote_match:
        quote_match = re.search(r'^"(.*?)"\s*-(.*)$', quote.strip())
        
    if quote_match:
        return quote_match.group(1), quote_match.group(2)
    return quote, ""

def verify_segments_exist(quote_text, sources):
    clean_quote = re.sub(r'\[\^[^\]]+\]', '', quote_text)
    segments = [s.strip() for s in re.split(r'\.\.\.+', clean_quote) if s.strip()]
    if not segments:
        return False, "Empty quote"
        
    # Check if all segments exist in at least one source file
    all_segs_found = True
    unmatched_info = ""
    
    for seg in segments:
        seg_words = clean_text(seg).split()
        if len(seg_words) <= 2:
            continue
            
        found_seg = False
        for fname, src_info in sources.items():
            src_words = src_info["clean"].split()
            
            # Search for the sequence of seg_words in src_words allowing some distance/timestamps
            # We look for a window in src_words that contains all (or 90%) of the seg_words in order
            first_word = seg_words[0]
            start_indices = [i for i, w in enumerate(src_words) if w == first_word]
            
            for start_i in start_indices:
                window_size = len(seg_words) + 40
                sub_src = src_words[start_i:start_i + window_size]
                
                seg_i = 0
                sub_i = 0
                matches = 0
                while seg_i < len(seg_words) and sub_i < len(sub_src):
                    if seg_words[seg_i] == sub_src[sub_i]:
                        matches += 1
                        seg_i += 1
                    sub_i += 1
                
                if matches >= len(seg_words) * 0.9:
                    found_seg = True
                    break
            
            if found_seg:
                break
                
        if not found_seg:
            all_segs_found = False
            unmatched_info = f"segment not found in any source: \"{' '.join(seg_words[:8])}...\""
            break
            
    if all_segs_found:
        return True, ""
    return False, unmatched_info

def main():
    audit_dir = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit"
    archive_dir = os.path.join(audit_dir, "Sources_Archive")
    proposal_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit_AI_Logs\proposed_quote_corrections.md"
    
    # Load all sources
    sources = {}
    for filename in os.listdir(archive_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(archive_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                sources[filename] = {
                    "raw": content,
                    "clean": clean_text(content)
                }
                
    proposal_lines = [
        "# Flagged Quotes — Needs Manual Corpus Search",
        "Quotes where no segment passes the 90%-words-in-order check against any source file.",
        "For each entry: check the citation key → find the actual source file → grep/search for a real quote.",
        "",
        "## Flagged Entries",
        ""
    ]
    
    mismatch_count = 0
    
    # Plane files to scan
    plane_files = [
        "Plane_1_Identity.md",
        "Plane_2_Definition.md",
        "Plane_3_Land.md",
        "Plane_4_Industry.md",
        "Plane_5_Society.md",
        "Plane_6_Sovereignty.md",
        "Plane_7_Sovereignty.md"
    ]
    
    for plane_file in plane_files:
        filepath = os.path.join(audit_dir, plane_file)
        if not os.path.exists(filepath):
            continue
            
        plane_proposal = []
        plane_proposal.append(f"### {plane_file}")
        plane_proposal.append("")
        
        has_proposals = False
        
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for line_num, line in enumerate(lines, 1):
            # Find lines that contain: **(Address) Name ...: HIT.** **Quote:** "..."
            # or FAIL / MISS
            if "**Quote:**" in line:
                # Find the text after **Quote:**
                match = re.search(r'\*\*Quote:\*\*\s*(.*)$', line)
                if match:
                    quote = match.group(1).strip()
                    
                    # Extract key like [^ms96] from the raw quote string first before clean
                    key_match = re.search(r'(\[\^[^\]]+\])', quote)
                    citation_key = key_match.group(1) if key_match else "None"
                    
                    quote_text, citation = clean_target_quote(quote)
                    if not quote_text.strip():
                        continue
                        
                    # Clean off footnote keys from the display fields
                    quote_text_display = re.sub(r'\[\^[^\]]+\]', '', quote_text).strip()
                    citation_display = re.sub(r'\[\^[^\]]+\]', '', citation).strip()
                    
                    is_valid, unmatched_info = verify_segments_exist(quote_text, sources)
                    if is_valid:
                        continue
                        
                    mismatch_count += 1
                    has_proposals = True
                    
                    # Extract the vector name/address from the line
                    addr_match = re.search(r'\*\*\(([^)]+)\)\s*([^(*]+)', line)
                    vec_info = addr_match.group(0).replace("**", "") if addr_match else f"Line {line_num}"
                    
                    plane_proposal.append(f"#### ❌ {vec_info} (Line {line_num})")
                    plane_proposal.append(f"- **Quote in doc:** \"{quote_text_display}\"")
                    plane_proposal.append(f"- **Citation key:** `{citation_key}` → `{citation_display}`")
                    plane_proposal.append(f"- **Reason:** {unmatched_info}")
                    plane_proposal.append("")
                    
        if has_proposals:
            proposal_lines.extend(plane_proposal)
            
    proposal_lines.insert(5, f"- **Total flagged:** {mismatch_count}")
    proposal_lines.insert(6, "")
    
    with open(proposal_path, "w", encoding="utf-8") as f:
        f.write("\n".join(proposal_lines))
        
    print(f"Proposal written to {proposal_path}")

if __name__ == "__main__":
    main()
