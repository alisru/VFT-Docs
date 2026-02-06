import os
import glob
import re

SOURCE_DIR = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America"

def replace_locus():
    files = glob.glob(os.path.join(SOURCE_DIR, "American_Kanon_Plane_*.md"))
    
    for filepath in files:
        print(f"Processing {os.path.basename(filepath)}...")
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace "Locus" with "Land"
        # Case sensitive? "Locus" -> "Land"
        # "locus" -> "land"
        
        new_content = content.replace("Locus", "Land")
        new_content = new_content.replace("locus", "land")
        new_content = new_content.replace("LOCUS", "LAND")
        
        # Special fix for header if it says "Plane Where" or "Plane Locus"
        # "Plane Locus" -> "Plane Land"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

if __name__ == "__main__":
    replace_locus()
