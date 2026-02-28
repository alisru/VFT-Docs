import os
import re

SOURCE_DIR = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America"

plane_files = [
    {"num": 1, "file": "Trump_American_Kanon_Plane_1_Identity.md"},
    {"num": 2, "file": "Trump_American_Kanon_Plane_2_Definition.md"},
    {"num": 3, "file": "Trump_American_Kanon_Plane_3_Land.md"},
    {"num": 4, "file": "Trump_American_Kanon_Plane_4_Drive.md"},
    {"num": 5, "file": "Trump_American_Kanon_Plane_5_Method.md"},
    {"num": 6, "file": "Trump_American_Kanon_Plane_6_Cause.md"},
    {"num": 7, "file": "Trump_American_Kanon_Plane_7_Effect.md"}
]

BASE_KANON_MORALS = {}

def load_base_kanon_morals():
    for i in range(1, 8):
        if i == 1:
            filepath1 = os.path.join(SOURCE_DIR, "American_Kanon_Plane_1_Identity_JUDGEMENT.md")
            filepath_alt = os.path.join(SOURCE_DIR, "American_Kanon_Plane_1_Judgement_Batch_1.md")
            if os.path.exists(filepath1):
                parse_base_judgement_file(filepath1)
            elif os.path.exists(filepath_alt):
                parse_base_judgement_file(filepath_alt)
        else:
            filename = plane_files[i-1]["file"].replace("Trump_", "").replace(".md", "_JUDGEMENT.md")
            filepath = os.path.join(SOURCE_DIR, filename)
            if os.path.exists(filepath):
                parse_base_judgement_file(filepath)

def parse_base_judgement_file(filepath):
    global BASE_KANON_MORALS
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for line in content.split('\n'):
        if '|' in line and not '---|' in line and not 'Vector | Entry' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 6 and re.match(r'^[A-Za-z]+\.[A-Za-z]+\.[A-Za-z]+$', parts[1]):
                vec_id = parts[1]
                v_score = parts[3]
                p_score = parts[4]
                BASE_KANON_MORALS[vec_id] = {"v": v_score, "p": p_score}

load_base_kanon_morals()

mutation_count = 0

for plane in plane_files:
    filename = os.path.join(SOURCE_DIR, plane["file"])
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        continue
        
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # We can use regex to find the table rows since we are manipulating the table
    # Wait, the Trump docs use a table block! Let's split by lines to be exact.
    # We can also parse the blocks if they exist.
    
    # Actually, the most robust way is to just replace in the table rows
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        if '|' in line and not '---|' in line and not 'Vector | Entry' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 6 and re.match(r'^[A-Za-z]+\.[A-Za-z]+\.[A-Za-z]+$', parts[1]):
                vec_id = parts[1]
                score_str = parts[3].replace('+','').replace('−','-').strip()
                trump_v_str = parts[4].replace('+','').replace('−','-').strip()
                
                if score_str == '1' or score_str == '+1':
                    try:
                        trump_v = float(trump_v_str)
                    except ValueError:
                        trump_v = 0.0
                        
                    if trump_v < 0:
                        # Check base Kanon
                        base_data = BASE_KANON_MORALS.get(vec_id, {"v": "1", "p": "1"})
                        base_v_str = base_data.get("v", "1").replace('+','').replace('−','-').strip()
                        try:
                            base_v = float(base_v_str)
                        except ValueError:
                            base_v = 0.0
                            
                        # Only apply mutation if base Kanon is not negative (or strictly > 0? Let's say >= 0 to be safe)
                        if base_v >= 0:
                            # It's a mutation!
                            parts[3] = '-1 (Mutation)'
                            
                            # Update justification with an automated note if it doesn't already have one
                            justification = parts[6]
                            mutation_note = ' **[MUTATION AUDIT]: Score changed from +1 to -1. Trump executes the Kanonic action (+ψ) but inverts its civic purpose (-υ), functioning as a failed mutation of the ideal.**'
                            if "[MUTATION AUDIT]" not in justification:
                                parts[6] = justification + mutation_note
                            
                            line = '| ' + ' | '.join(parts[1:-1]) + ' |'
                            mutation_count += 1
                            print(f"Mutated: {vec_id} in Plane {plane['num']} (Trump u={trump_v}, Base u={base_v})")
                        else:
                            print(f"Skipped negative Kanon element pass: {vec_id} (Trump u={trump_v}, Base u={base_v})")
        new_lines.append(line)
        
    new_content = '\n'.join(new_lines)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)

print(f"\nTotal Mutations Identified and Flipped: {mutation_count}")
