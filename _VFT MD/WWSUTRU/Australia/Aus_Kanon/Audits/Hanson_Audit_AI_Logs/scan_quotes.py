import os
import json
import re

def clean_text(text):
    """Normalize whitespace and punctuation for robust matching."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return " ".join(text.split())

def main():
    json_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Hegemonic Audit_ Pauline Hanson.json"
    archive_dir = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources_Archive"
    report_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit_AI_Logs\quote_verification_report.md"
    
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}")
        return
        
    with open(json_path, "r", encoding="utf-8") as f:
        audit_data = json.load(f)
        
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
                
    verified_count = 0
    missing_count = 0
    
    report_lines = [
        "# Quote Verification Report",
        f"**Target Audit JSON:** `{os.path.basename(json_path)}`",
        f"**Sources Archive Directory:** `{os.path.basename(archive_dir)}`",
        "",
        "## Summary",
        "| Status | Count |",
        "| --- | --- |",
        "| Verified | {verified_placeholder} |",
        "| Missing / Mismatched | {missing_placeholder} |",
        "",
        "## Detailed Verification Log",
        ""
    ]
    
    for plane in audit_data.get("planes", []):
        plane_num = plane.get("plane_num")
        plane_name = plane.get("plane_name")
        
        plane_section = []
        plane_section.append(f"### Plane {plane_num}: {plane_name}")
        plane_section.append("")
        plane_section.append("| Vector Address | Stated Name | Status | Expected Source | Quote Excerpt / Notes |")
        plane_section.append("| --- | --- | --- | --- | --- |")
        
        has_vectors = False
        for vec in plane.get("vectors", []):
            address = vec.get("address")
            stated_name = vec.get("meta", {}).get("stated_name", "Unknown")
            verdict = vec.get("verdict")
            quote = vec.get("quote", "")
            
            if not quote or verdict == "FAIL":
                continue
                
            has_vectors = True
            quote_match = re.search(r'^\\?"(.*?)\\?"\s*-(.*)$', quote.strip())
            if not quote_match:
                quote_match = re.search(r'^"(.*?)"\s*-(.*)$', quote.strip())
                
            if quote_match:
                quote_text = quote_match.group(1)
                citation = quote_match.group(2)
            else:
                quote_text = quote
                citation = "Unknown Source"
                
            src_key_match = re.search(r'\[\^(.*?)\]', citation)
            src_file = None
            if src_key_match:
                src_key = src_key_match.group(1)
                src_file = f"{src_key}.txt"
                
            clean_quote = clean_text(quote_text)
            
            matched_sources = []
            if src_file in sources:
                if clean_quote in sources[src_file]["clean"]:
                    matched_sources.append(src_file)
            else:
                for fname, src_info in sources.items():
                    if clean_quote in src_info["clean"]:
                        matched_sources.append(fname)
                        
            if matched_sources:
                status = "✅ Verified"
                notes = f"Matched in {', '.join(matched_sources)}"
                verified_count += 1
            else:
                status = "❌ Missing/Mismatched"
                notes = f"Quote text: `{quote_text[:80]}`"
                missing_count += 1
                
            plane_section.append(f"| {address} | {stated_name} | {status} | {src_file or 'Any'} | {notes} |")
            
        plane_section.append("")
        if has_vectors:
            report_lines.extend(plane_section)
            
    # Replace placeholders with final counts
    report_content = "\n".join(report_lines)
    report_content = report_content.replace("{verified_placeholder}", str(verified_count))
    report_content = report_content.replace("{missing_placeholder}", str(missing_count))
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print(f"Report successfully written to {report_path}")

if __name__ == "__main__":
    main()
