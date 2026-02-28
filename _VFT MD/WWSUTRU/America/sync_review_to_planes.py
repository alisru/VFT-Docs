import os
import re

base_dir = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America"

with open(os.path.join(base_dir, "Trump_Manual_Score_Review.md"), 'r', encoding='utf-8') as f:
    review_content = f.read()

blocks = review_content.split("\n#### ")
updates = {}

for block in blocks[1:]:
    lines = block.strip().split('\n')
    header_match = re.search(r'^\d+:\s*([A-Za-z]+\.[A-Za-z]+\.[A-Za-z]+)', lines[0])
    if not header_match:
        continue
    vec_id = header_match.group(1)
    
    score_str = ""
    v_str = ""
    p_str = ""
    justification = ""
    
    for line in lines[1:]:
        if line.startswith('*   **Updated Score:**'):
            raw_score = line.split('**Updated Score:**')[1].strip()
            m = re.match(r'^([+-]?\d+)', raw_score)
            if m:
                score_str = m.group(1)
                if not score_str.startswith('-') and not score_str.startswith('+') and score_str != '0':
                    score_str = "+" + score_str
        elif line.startswith('*   **Updated Trump υ / ψ:**') or line.startswith('*   **Updated Trump \u03c5 / \u03c8:**'):
            try:
                v_p_raw = line.split(':**')[1].strip()
                v_str, p_str = [x.strip() for x in v_p_raw.split('/')]
            except Exception:
                pass
        elif line.startswith('*   **Justification:**'):
            justification = line.split('**Justification:**')[1].strip()
            
    if score_str and justification:
        updates[vec_id] = {
            "score": score_str,
            "v": v_str,
            "p": p_str,
            "justification": justification
        }

print(f"Extracted {len(updates)} updated vectors from the review document.")

planes = [
    "Plane_1_Identity", "Plane_2_Definition", "Plane_3_Land", 
    "Plane_4_Drive", "Plane_5_Method", "Plane_6_Cause", "Plane_7_Effect"
]

for plane in planes:
    trump_file = os.path.join(base_dir, f"Trump_American_Kanon_{plane}.md")
    if not os.path.exists(trump_file):
        continue
    
    with open(trump_file, 'r', encoding='utf-8') as f:
        trump_content = f.read()
        
    new_trump_lines = []
    
    for line in trump_content.split('\n'):
        if '|' in line and not '---|' in line and not 'Vector | Entry | Trump Score' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 7 and re.match(r'^[A-Za-z]+\.[A-Za-z]+\.[A-Za-z]+$', parts[1]):
                vec_id = parts[1]
                if vec_id in updates:
                    # parts format: ['', 'Who.Who.Who', '**Name**', '+1', '+1.0', '+0.9', '**Quote:**...<br><br>Reasoning', '']
                    
                    parts[3] = updates[vec_id]['score']
                    if updates[vec_id]['v']:
                        parts[4] = updates[vec_id]['v']
                    if updates[vec_id]['p']:
                        parts[5] = updates[vec_id]['p']
                    
                    old_reasoning = parts[6]
                    if "<br><br>" in old_reasoning:
                        quote_part, desc_part = old_reasoning.split("<br><br>", 1)
                        new_reasoning = f"{quote_part}<br><br>{updates[vec_id]['justification']}"
                    else:
                        new_reasoning = updates[vec_id]['justification']
                        
                    parts[6] = new_reasoning
                    
                    # Reconstruct the line correctly
                    new_line = "| " + " | ".join(parts[1:-1]) + " |"
                    new_trump_lines.append(new_line)
                else:
                    new_trump_lines.append(line)
            else:
                new_trump_lines.append(line)
        else:
            new_trump_lines.append(line)
            
    with open(trump_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_trump_lines))
        
print("Successfully synchronized all Plane documents with the Review document.")
