import os
import re

def normalize_name(filename):
    name = filename.lower().replace(".md", "").strip()
    name = re.sub(r"[^\w\s]", "", name)
    return name

def main():
    scratch_dir = r"e:\Vector Field Theory\VFT Docs\scratch"
    appdata_scratch_dir = r"C:\Users\hungh\.gemini\antigravity\brain\44f19dea-857b-4620-9363-cef56bb6dbab\scratch"
    summaries_file = r"e:\Vector Field Theory\VFT Docs\file_summaries.md"
    report_file = r"e:\Vector Field Theory\VFT Docs\scratch\batch_missing_report.txt"
    
    with open(summaries_file, "r", encoding="utf-8") as f:
        summaries_content = f.read()
        
    headers = re.findall(r"###\s*(.*)", summaries_content)
    summarized_names = set()
    for h in headers:
        h_clean = re.sub(r"\s*\(\d{4}-\d{2}-\d{2}\)", "", h).strip()
        summarized_names.add(normalize_name(h_clean))
        
    print(f"Loaded {len(summarized_names)} unique summarized files from file_summaries.md.")
    
    # Let's search both scratch directories for any file containing potential summaries
    # We want to look for ### [filename] or similar patterns in any .txt or .py file in scratch
    all_extracted_summaries = {}
    
    dirs_to_scan = [scratch_dir, appdata_scratch_dir]
    for d in dirs_to_scan:
        if not os.path.exists(d):
            continue
        for file in os.listdir(d):
            if file.endswith((".txt", ".py")) and not file.startswith("check_"):
                fpath = os.path.join(d, file)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        text = f.read()
                except Exception:
                    continue
                
                # Find all occurrences of ### [filename]
                found = re.findall(r"###\s*([a-zA-Z0-9_\-\.\s\u2014]+(?:\.md|\.cs|\.py)?)(?:\s*\(\d{4}-\d{2}-\d{2}\))?", text)
                for item in found:
                    item_clean = item.strip()
                    if item_clean and not item_clean.endswith(".py") and not item_clean.endswith(".pyc") and "summaries" not in item_clean.lower():
                        norm_item = normalize_name(item_clean)
                        if norm_item not in all_extracted_summaries:
                            all_extracted_summaries[norm_item] = {
                                "original": item_clean,
                                "source_file": file,
                                "source_dir": d
                            }
                            
    print(f"Extracted {len(all_extracted_summaries)} potential summarized file names from all scratch scripts and texts.")
    
    missing_items = []
    for norm_name, info in all_extracted_summaries.items():
        if norm_name not in summarized_names:
            # Substring check
            if info["original"].lower() not in summaries_content.lower():
                missing_items.append(info)
                
    print(f"Found {len(missing_items)} missing items from scratch files.")
    
    report_lines = []
    report_lines.append("SCRATCH FILES EXTRACTION & MISSING SUMMARIES REPORT")
    report_lines.append(f"Total potential summaries found in scratch files: {len(all_extracted_summaries)}")
    report_lines.append(f"Missing from file_summaries.md: {len(missing_items)}\n")
    
    if missing_items:
        report_lines.append("MISSING ITEMS DETAILS:")
        for idx, item in enumerate(missing_items):
            report_lines.append(f"{idx+1}. {item['original']}")
            report_lines.append(f"   Source file: {item['source_file']}")
            report_lines.append(f"   Source directory: {item['source_dir']}")
            report_lines.append("")
            
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
        
    print(f"Report written to {report_file}")

if __name__ == "__main__":
    main()
