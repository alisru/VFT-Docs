import os
import glob
import re

plane_files = glob.glob('Trump_American_Kanon_Plane_*.md')

def clean_text(text):
    # Pass 1: Remove specifically "**CRITICAL AI CORRECTION:** "
    text = text.replace("**CRITICAL AI CORRECTION:** ", "")
    
    # Pass 2: Remove sentences like "The original 0 score misunderstood the depth of the contradiction."
    # Matches "The original [anything] score [anything]." followed by an optional " However," or just a space.
    patterns = [
        r"The original [0-9+-]+ score [^\.]+\.\s*(?:However,\s*)?",
        r"The original score of [0-9+-]+ [^\.]+\.\s*(?:However,\s*)?",
        r"The original [0-9+-]+ score [^\.]+\.\s*"
    ]
    
    for pattern in patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
        
    return text

for file_path in plane_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    cleaned_content = clean_text(content)
    
    if content != cleaned_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        print(f"Cleaned {file_path}")

print("Done cleaning AI meta-commentary.")
