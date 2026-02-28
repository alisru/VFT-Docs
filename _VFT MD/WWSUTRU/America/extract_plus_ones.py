import os
import re

base_dir = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America"

planes = [
    ("Plane_1_Identity", "Identity"),
    ("Plane_2_Definition", "Definition"),
    ("Plane_3_Land", "Land"),
    ("Plane_4_Drive", "Drive"),
    ("Plane_5_Method", "Method"),
    ("Plane_6_Cause", "Cause"),
    ("Plane_7_Effect", "Effect")
]

plus_ones = []

for plane_file, plane_name in planes:
    file_path = os.path.join(base_dir, f"Trump_American_Kanon_{plane_file}.md")
    if os.path.exists(file_path):
        lines = open(file_path, 'r', encoding='utf-8').read().split('\n')
        for line in lines:
            if '|' in line and not '---|' in line and not 'Vector | Entry' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 6:
                    score_str = parts[3].replace('+','').replace('−','-').strip()
                    if score_str == '1' or score_str == '+1':
                        vec_id = parts[1]
                        entry = parts[2]
                        trump_v = parts[4]
                        trump_p = parts[5]
                        reasoning = parts[6]
                        plus_ones.append({
                            'plane': plane_name,
                            'id': vec_id,
                            'entry': entry.replace('**', ''),
                            'v': trump_v,
                            'p': trump_p,
                            'reasoning': reasoning
                        })

out_file = os.path.join(base_dir, "Trump_Plus_One_Audit.md")
with open(out_file, 'w', encoding='utf-8') as f:
    f.write("# Trump Kanon: The Mutation Audit\n\n")
    f.write("Reviewing all 153 current `+1` scores to identify where Trump executes the Kanonic action (+ψ) but inverts its civic purpose (-υ). These must be flipped to `-1 (Mutation)`.\n\n")
    
    current_plane = ""
    for item in plus_ones:
        if item['plane'] != current_plane:
            current_plane = item['plane']
            f.write(f"\n## {current_plane}\n\n")
            
        f.write(f"### {item['id']} : {item['entry']}\n")
        f.write(f"- **Current Score:** +1\n")
        f.write(f"- **Trump υ / ψ:** {item['v']} / {item['p']}\n")
        f.write(f"- **Justification:** {item['reasoning'].replace('<br><br>', ' ')}\n\n")
        
print(f"Extracted {len(plus_ones)} '+1' scores for mutation auditing to {out_file}")
