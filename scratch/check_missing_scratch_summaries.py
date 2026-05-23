import os
import re

def main():
    scratch_dir = r"e:\Vector Field Theory\VFT Docs\scratch"
    summaries_file = r"e:\Vector Field Theory\VFT Docs\file_summaries.md"
    report_file = r"e:\Vector Field Theory\VFT Docs\scratch\missing_report.txt"
    
    with open(summaries_file, "r", encoding="utf-8") as f:
        summaries_content = f.read()
        
    all_files = os.listdir(scratch_dir)
    batch_files = sorted([f for f in all_files if f.startswith("batch_") and f.endswith(".txt")])
    
    report_lines = []
    report_lines.append(f"Scanning scratch directory for batch files in {scratch_dir}")
    report_lines.append(f"Matching against {summaries_file}\n")
    
    for bf in batch_files:
        bf_path = os.path.join(scratch_dir, bf)
        with open(bf_path, "r", encoding="utf-8") as f:
            bf_content = f.read()
            
        # Parse individual headers from the batch file
        headers = re.findall(r"###\s*(.*)", bf_content)
        if not headers:
            headers = [line.strip() for line in bf_content.split("\n")[:5] if line.strip()]
            
        report_lines.append(f"File: {bf} (size: {os.path.getsize(bf_path)} bytes)")
        
        found_headers = []
        missing_headers = []
        for h in headers:
            # Clean header (remove dates, file extensions, etc. to search robustly)
            h_clean = re.sub(r"\s*\(\d{4}-\d{2}-\d{2}\)", "", h).strip()
            h_clean = h_clean.replace(".md", "").replace("###", "").strip()
            
            if h_clean:
                # Search case-insensitively
                match = re.search(re.escape(h_clean), summaries_content, re.IGNORECASE)
                if match:
                    found_headers.append(h)
                else:
                    missing_headers.append(h)
                    
        report_lines.append(f"  Total headers: {len(headers)}")
        report_lines.append(f"  Matched headers: {len(found_headers)}")
        report_lines.append(f"  Missing headers: {len(missing_headers)}")
        if missing_headers:
            report_lines.append("  MISSING HEADERS:")
            for mh in missing_headers:
                report_lines.append(f"    - {mh}")
        report_lines.append("") # blank line
        
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
        
    print(f"Report written to {report_file}")

if __name__ == "__main__":
    main()
