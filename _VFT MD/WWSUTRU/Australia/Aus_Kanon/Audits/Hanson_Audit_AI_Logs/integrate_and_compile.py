import json
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Paths
JSON_FILE = Path("e:/Vector Field Theory/VFT Docs/_VFT MD/io/Hegemonic Audit_ Pauline Hanson.json")
LOGS_DIR = Path("e:/Vector Field Theory/VFT Docs/_VFT MD/io/Hanson_Audit_AI_Logs")
COMPILER_SCRIPT = Path("C:/Users/hungh/.gemini/antigravity/brain/62295f40-1125-4360-8277-818356de5a12/scratch/json_to_markdown.py")
VERIFY_SCRIPT = Path("C:/Users/hungh/.gemini/antigravity/brain/62295f40-1125-4360-8277-818356de5a12/scratch/verify_hanson_audit.py")

def integrate():
    # Load main JSON database
    print("Loading main JSON database...")
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        main_data = json.load(f)

    # Re-integrate planes 3 to 7
    for p_num in range(3, 8):
        remediated_file = LOGS_DIR / f"remediated_plane_{p_num}.json"
        print(f"Integrating Plane {p_num} from {remediated_file.name}...")
        
        with open(remediated_file, 'r', encoding='utf-8') as f:
            remediated_vectors = json.load(f)
            
        # Ensure all vectors have a meta block matching the format
        for item in remediated_vectors:
            if "meta" not in item:
                item["meta"] = {
                    "stated_name": item["name"],
                    "stated_coordinates": {
                        "v": item["coordinates"]["v"],
                        "psi": item["coordinates"]["psi"]
                    },
                    "name_mismatch": False,
                    "coord_mismatch": False
                }
        
        # Find matching plane in main database
        plane_found = False
        for p in main_data["planes"]:
            if p["plane_num"] == p_num:
                print(f"  Replacing {len(p['vectors'])} vectors with {len(remediated_vectors)} remediated vectors.")
                p["vectors"] = remediated_vectors
                plane_found = True
                break
        
        if not plane_found:
            raise ValueError(f"Plane {p_num} not found in main JSON database!")

    # Save main JSON database
    print("Saving integrated JSON database...")
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(main_data, f, indent=2, ensure_ascii=False)
    
    print("Integration complete!")

if __name__ == "__main__":
    integrate()
