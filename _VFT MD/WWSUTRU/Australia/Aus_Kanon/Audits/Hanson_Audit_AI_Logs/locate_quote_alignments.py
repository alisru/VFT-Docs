import os
import re

def clean_text(text):
    text = text.replace("--", " ").replace("—", " ").replace("–", " ").replace("-", " ")
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return " ".join(text.split())

def clean_target_quote(quote):
    quote = re.sub(r'\[Documented position:[^\]]*\]', '', quote)
    quote_match = re.search(r'^\\?"(.*?)\\?"\s*-(.*)$', quote.strip())
    if not quote_match:
        quote_match = re.search(r'^"(.*?)"\s*-(.*)$', quote.strip())
    if quote_match:
        return quote_match.group(1), quote_match.group(2)
    return quote, ""

def main():
    audit_dir = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit"
    archive_dir = os.path.join(audit_dir, "Sources_Archive")
    
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
                
    plane_files = [
        "Plane_1_Identity.md",
        "Plane_2_Definition.md",
        "Plane_3_Land.md",
        "Plane_4_Industry.md",
        "Plane_5_Society.md",
        "Plane_6_Sovereignty.md",
        "Plane_7_Sovereignty.md"
    ]
    
    print("--- SCANNING FOR PORTIONS OF MISMATCHED QUOTES IN SOURCES ---")
    for plane_file in plane_files:
        filepath = os.path.join(audit_dir, plane_file)
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for line_num, line in enumerate(lines, 1):
            if "**Quote:**" in line:
                match = re.search(r'\*\*Quote:\*\*\s*(.*)$', line)
                if match:
                    quote = match.group(1).strip()
                    quote_text, citation = clean_target_quote(quote)
                    if not quote_text.strip():
                        continue
                        
                    clean_quote = re.sub(r'\[\^[^\]]+\]', '', quote_text)
                    segments = [s.strip() for s in re.split(r'\.\.\.+', clean_quote) if s.strip()]
                    if not segments:
                        continue
                    
                    first_seg = segments[0]
                    words = first_seg.split()
                    if len(words) < 3:
                        continue
                        
                    # First 3 words search
                    search_words = " ".join(words[:3])
                    clean_search = clean_text(search_words)
                    
                    found_matches = []
                    for fname, src_info in sources.items():
                        if clean_search in src_info["clean"]:
                            # Find position of match and extract context
                            idx = src_info["clean"].find(clean_search)
                            # Get 150 chars of context around it
                            start_idx = max(0, idx - 50)
                            end_idx = min(len(src_info["clean"]), idx + 200)
                            context = src_info["clean"][start_idx:end_idx]
                            found_matches.append((fname, context))
                            
                    if found_matches:
                        # Extract the vector name
                        addr_match = re.search(r'\*\*\(([^)]+)\)\s*([^(*]+)', line)
                        vec_info = addr_match.group(0).replace("**", "") if addr_match else f"Line {line_num}"
                        
                        print(f"\nVector: {vec_info} ({plane_file}:{line_num})")
                        print(f"Quote in MD: \"{quote_text[:80]}...\"")
                        print(f"Search Query (First 3 words): '{search_words}'")
                        for fname, context in found_matches:
                            print(f"  -> Match in `{fname}`:")
                            print(f"     Context: ...{context}...")
                            
if __name__ == "__main__":
    main()
