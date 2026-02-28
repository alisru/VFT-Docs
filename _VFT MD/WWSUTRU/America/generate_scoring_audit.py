import os
import re

SOURCE_DIR = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America"
OUTPUT_FILE = os.path.join(SOURCE_DIR, "Trump_Scoring_Audit_V3.md")

PLANES = [
    {"num": 1, "name": "Identity", "file": "Trump_American_Kanon_Plane_1_Identity.md"},
    {"num": 2, "name": "Definition", "file": "Trump_American_Kanon_Plane_2_Definition.md"},
    {"num": 3, "name": "Land", "file": "Trump_American_Kanon_Plane_3_Land.md"},
    {"num": 4, "name": "Drive", "file": "Trump_American_Kanon_Plane_4_Drive.md"},
    {"num": 5, "name": "Method", "file": "Trump_American_Kanon_Plane_5_Method.md"},
    {"num": 6, "name": "Cause", "file": "Trump_American_Kanon_Plane_6_Cause.md"},
    {"num": 7, "name": "Effect", "file": "Trump_American_Kanon_Plane_7_Effect.md"}
]

def generate_audit_doc():
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        out.write("# Trump Kanon Evaluation - Comprehensive Audit Document V3\n\n")
        out.write("This document compiles every single vector score and its justification across all 7 planes for review. **Mark any required changes or notes directly below each entry.**\n\n")
        out.write("---\n\n")

        total_vectors = 0
        
        for p in PLANES:
            filepath = os.path.join(SOURCE_DIR, p["file"])
            if not os.path.exists(filepath):
                continue
                
            out.write(f"## Plane {p['num']}: {p['name']}\n\n")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            current_sense = ""
            for line in content.split('\n'):
                # Track sense headers
                sense_match = re.match(r'^## (\d\.\d.*?) \((.*?)\)', line)
                if sense_match:
                    current_sense = f"### {sense_match.group(1)} ({sense_match.group(2)})"
                    out.write(f"\n{current_sense}\n\n")
                    
                if line.startswith('|') and not '---|' in line and not 'Vector | Entry' in line:
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 7 and re.match(r'^[A-Za-z]+\.[A-Za-z]+\.[A-Za-z]+$', parts[1]):
                        vec_id = parts[1]
                        val = parts[2]
                        trump_score = parts[3]
                        trump_v = parts[4]
                        trump_p = parts[5]
                        reasoning = parts[6]
                        
                        out.write(f"#### {vec_id} : {val}\n")
                        out.write(f"- **Current Score:** `{trump_score}` | **Trump Coords (υ, ψ):** `{trump_v}, {trump_p}`\n")
                        out.write(f"- **Justification:** {reasoning}\n")
                        out.write("- **[ ] REVIEW NOTES:** \n\n")
                        total_vectors += 1
            
            out.write("---\n\n")
            
        out.write(f"\n**Total Vectors Extracted:** {total_vectors}\n")

if __name__ == "__main__":
    generate_audit_doc()
    print(f"Audit document generated at {OUTPUT_FILE}")
