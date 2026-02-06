import re
import os
import glob

SOURCE_DIR = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America"

PLANES = {
    "Plane_1": "Who",
    "Plane_2": "What", # Definition = What (Corrected)
    "Plane_3": "Where",  # Land = Where (Corrected)
    "Plane_4": "Why",   # Drive = Why
    "Plane_5": "How",   # Method = How
    "Plane_6": "Cause",
    "Plane_7": "Effect"
}

def update_file(filepath):
    filename = os.path.basename(filepath)
    
    # Identify Plane Interrogative
    plane_int = None
    plane_name = None
    
    # Extract Plane Num from filename for lookup
    match_num = re.search(r'Plane_(\d)_([A-Za-z]+)', filename)
    if not match_num:
        print(f"Skipping {filename}: Pattern match failed.")
        return

    p_num = match_num.group(1)
    p_name_raw = match_num.group(2) # e.g. Identity
    
    plane_key = f"Plane_{p_num}"
    plane_int = PLANES.get(plane_key)
    
    # Hardcoded map for Locus/Definition just in case
    if p_name_raw == "Identity": plane_int = "Who"
    elif p_name_raw == "Locus": plane_int = "Where"
    elif p_name_raw == "Definition": plane_int = "What"
    elif p_name_raw == "Drive": plane_int = "Why"
    elif p_name_raw == "Method": plane_int = "How"
    elif p_name_raw == "Cause": plane_int = "Cause" # Or Why? Logic says Cause.
    elif p_name_raw == "Effect": plane_int = "Effect" 
    
    print(f"Processing {filename} (Plane {p_num}: {plane_int})...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    current_sense_int = None
    
    # Header Update Logic
    header_updated = False
    
    for line in lines:
        # Update Main Header
        if line.startswith("# ") and not header_updated:
            # Check if likely the title line
            if "American Kanon" in line:
                line = f"# The American Kanon: Plane {p_num} Values of American {p_name_raw}\n"
                header_updated = True
        
        # Parse Sense Header
        # "### Sense q1: The Who of the Who"
        sense_match = re.match(r'### Sense q\d: The ([A-Za-z]+) of', line)
        if sense_match:
            current_sense_int = sense_match.group(1)
            # Ensure proper capitalization
            current_sense_int = current_sense_int.title()
            
        # Update Item Label
        # 1. **(Who.Who)[Self-Evidence]**
        item_match = re.search(r'(\d+\.\s*\*\*\()([A-Za-z]+)\.([A-Za-z]+)(\)\[.*?\]\*\*)', line)
        if item_match:
            prefix = item_match.group(1)
            old_p1 = item_match.group(2)
            old_p2 = item_match.group(3)
            suffix = item_match.group(4)
            
            # Value is always old_p2 based on analysis
            val_int = old_p2
            
            # Construct new label
            if current_sense_int:
                new_label = f"{plane_int}.{current_sense_int}.{val_int}"
                
                # Replace the exact span
                # We reuse the regex groups to rebuild the string safely
                # But line might contain other things, so use replace on the match
                old_str = f"({old_p1}.{old_p2})"
                new_str = f"({new_label})"
                line = line.replace(old_str, new_str)
            else:
                print(f"Warning: Found item before Sense Header in {filename}: {line.strip()}")

        new_lines.append(line)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

# Run for all Plane files
files = glob.glob(os.path.join(SOURCE_DIR, "American_Kanon_Plane_*.md"))
for f in files:
    update_file(f)
