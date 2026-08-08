import os
import json
import datetime
from pathlib import Path

def scan_gdrive():
    gdrive_root = r"F:\My Drive"
    output_path = Path(__file__).parent / "gdrive_creation_dates.json"
    
    print(f"Scanning '{gdrive_root}' recursively for markdown files...", flush=True)
    if not os.path.exists(gdrive_root):
        print(f"Error: Google Drive path '{gdrive_root}' not found. Make sure Google Drive for Desktop is running and mounted.", flush=True)
        return
        
    gdrive_dates = {}
    scanned_count = 0
    
    # Extensions that represent source documents on Google Drive
    doc_extensions = {'.gdoc', '.docx', '.doc', '.pdf', '.md', '.txt'}
    
    # Recursively scan the drive for documents
    for root, dirs, files in os.walk(gdrive_root):
        # Skip Google Drive cache/hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            name, ext = os.path.splitext(file)
            if ext.lower() not in doc_extensions:
                continue
                
            abs_path = os.path.join(root, file)
            # Use the extension-stripped base name as the key
            file_base_lower = name.lower()
            
            try:
                # Get the remote creation timestamp
                ctime = os.path.getctime(abs_path)
                cdate = datetime.datetime.fromtimestamp(ctime)
                iso_date = cdate.isoformat()
                
                # Deduplication: keep the oldest creation date
                if file_base_lower in gdrive_dates:
                    existing_iso = gdrive_dates[file_base_lower]
                    existing_date = datetime.datetime.fromisoformat(existing_iso)
                    if cdate < existing_date:
                        gdrive_dates[file_base_lower] = iso_date
                else:
                    gdrive_dates[file_base_lower] = iso_date
                    
                scanned_count += 1
                if scanned_count % 100 == 0:
                    print(f"Processed {scanned_count} document files...", flush=True)
                    
            except Exception as e:
                # Avoid failing on individual virtual file errors
                continue

    # Save to the JSON file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(gdrive_dates, f, indent=2, ensure_ascii=False)
        print(f"\nScan complete! Found {len(gdrive_dates)} unique files.", flush=True)
        print(f"Metadata lookup written to: {output_path}", flush=True)
    except Exception as e:
        print(f"Error writing output file: {e}", flush=True)

if __name__ == "__main__":
    scan_gdrive()
