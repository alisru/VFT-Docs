import os
import re

def normalize_name(filename):
    # Normalize filename for comparisons
    name = filename.lower().replace(".md", "").strip()
    # Replace special punctuation and spaces
    name = re.sub(r"[^\w\s]", "", name)
    return name

def main():
    io_dir = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io"
    summaries_file = r"e:\Vector Field Theory\VFT Docs\file_summaries.md"
    report_file = r"e:\Vector Field Theory\VFT Docs\scratch\missing_io_summaries.txt"
    
    with open(summaries_file, "r", encoding="utf-8") as f:
        summaries_content = f.read()
        
    # Extract all headers from file_summaries.md
    # Formats are usually "### filename.md (date)" or similar
    headers = re.findall(r"###\s*(.*)", summaries_content)
    summarized_names = set()
    for h in headers:
        # Clean header (remove dates, file extensions)
        h_clean = re.sub(r"\s*\(\d{4}-\d{2}-\d{2}\)", "", h).strip()
        summarized_names.add(normalize_name(h_clean))
        
    print(f"Loaded {len(summarized_names)} unique summarized files from file_summaries.md.")
    
    io_files = [f for f in os.listdir(io_dir) if f.endswith(".md")]
    print(f"Found {len(io_files)} markdown files in _VFT MD/io.")
    
    missing_files = []
    matched_files = []
    
    for f in io_files:
        norm_f = normalize_name(f)
        if norm_f in summarized_names:
            matched_files.append(f)
        else:
            # Let's also do a raw substring search in the whole file to be absolutely sure
            clean_name_only = f.replace(".md", "").strip()
            if clean_name_only.lower() in summaries_content.lower():
                matched_files.append(f)
            else:
                missing_files.append(f)
                
    report_lines = []
    report_lines.append("SUMMARY COMPARISON REPORT")
    report_lines.append(f"Total files in _VFT MD/io: {len(io_files)}")
    report_lines.append(f"Matched/Summarized files: {len(matched_files)}")
    report_lines.append(f"Missing summaries: {len(missing_files)}\n")
    
    report_lines.append("MISSING FILES:")
    for i, mf in enumerate(sorted(missing_files)):
        report_lines.append(f"{i+1}. {mf}")
        
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
        
    print(f"Report written to {report_file}")
    print(f"Total missing: {len(missing_files)}")

if __name__ == "__main__":
    main()
