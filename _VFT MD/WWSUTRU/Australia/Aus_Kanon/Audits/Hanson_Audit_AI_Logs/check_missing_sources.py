import os
import json
import re
import sys

# Ensure UTF-8 output in Windows terminal
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    json_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Hegemonic Audit_ Pauline Hanson.json"
    archive_dir = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources_Archive"
    
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}")
        return
        
    with open(json_path, "r", encoding="utf-8") as f:
        audit_data = json.load(f)
        
    # Get all text files in the archive directory
    archive_files = {f.lower() for f in os.listdir(archive_dir) if f.endswith(".txt")}
    
    # Extract all citation keys used in the JSON file
    citation_keys = set()
    for plane in audit_data.get("planes", []):
        for vec in plane.get("vectors", []):
            quote = vec.get("quote", "")
            if quote:
                # Find all markers like [^ms96] or [^tvfy]
                keys = re.findall(r'\[\^([^\]]+)\]', quote)
                for k in keys:
                    citation_keys.add(k.strip())
                    
    print("\n--- CITATION KEYS LACKING CORRESPONDING SOURCES ---")
    missing_sources = []
    for key in sorted(citation_keys):
        expected_filename = f"{key.lower()}.txt"
        
        # Check if the filename or a close match exists
        found = False
        if expected_filename in archive_files:
            found = True
        else:
            # Check for close matches
            for f in archive_files:
                if f.startswith(key.lower()) or key.lower() in f:
                    found = True
                    break
                    
        if not found:
            # List some of the vectors using this missing key
            affected_vectors = []
            for plane in audit_data.get("planes", []):
                for vec in plane.get("vectors", []):
                    if f"[^{key}]" in vec.get("quote", ""):
                        affected_vectors.append(f"{vec.get('address')} ({vec.get('meta', {}).get('stated_name')})")
            
            missing_sources.append((key, affected_vectors))
            print(f"[-] Citation Key: [^{key}]")
            print(f"   Expected File: `{key.lower()}.txt` (or similar)")
            print(f"   Used in Vectors: {', '.join(affected_vectors)}")
            print()
            
    print(f"Total citation keys missing files: {len(missing_sources)}")

if __name__ == "__main__":
    main()
