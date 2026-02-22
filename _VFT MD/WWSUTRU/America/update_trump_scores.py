import os
import re

base_dir = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America"

planes = [
    "Plane_1_Identity",
    "Plane_2_Definition",
    "Plane_3_Land",
    "Plane_4_Drive",
    "Plane_5_Method",
    "Plane_6_Cause",
    "Plane_7_Effect"
]

total_v = 0.0
total_p = 0.0
total_vectors = 0
plane_summaries = []

for plane in planes:
    kanon_file = os.path.join(base_dir, f"American_Kanon_{plane}_JUDGEMENT.md")
    trump_file = os.path.join(base_dir, f"Trump_American_Kanon_{plane}.md")
    
    try:
        with open(kanon_file, 'r', encoding='utf-8') as f:
            kanon_content = f.read()
    except Exception as e:
        print(f"Failed to read {kanon_file}: {e}")
        continue
        
    kanon_vals = {}
    for line in kanon_content.split('\n'):
        if '|' in line and not '--|--' in line and not 'Vector | Entry' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 5 and re.match(r'^[A-Za-z]+\.[A-Za-z]+\.[A-Za-z]+$', parts[1]):
                vec_id = parts[1]
                try:
                    v = float(parts[3].replace('+','').replace('−','-').strip())
                    p = float(parts[4].replace('+','').replace('−','-').strip())
                    kanon_vals[vec_id] = (v, p)
                except ValueError:
                    pass

    try:
        with open(trump_file, 'r', encoding='utf-8') as f:
            trump_content = f.read()
    except Exception as e:
        print(f"Failed to read {trump_file}: {e}")
        continue
        
    new_trump_lines = []
    plane_v = 0.0
    plane_p = 0.0
    plane_v_count = 0
    skip = False
    
    for line in trump_content.split('\n'):
        if line.startswith('## Plane Average Moral Scores'):
            skip = True
            
        if skip:
            if line.startswith('### Plane') or line.startswith('---'):
                if line.startswith('### Plane'):
                    skip = False
                    new_trump_lines.append(line)
                continue
            else:
                continue
            
        if not skip:
            if '|' in line and not '---|' in line and not 'Vector | Entry | Trump Score' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 4 and re.match(r'^[A-Za-z]+\.[A-Za-z]+\.[A-Za-z]+$', parts[1]):
                    vec_id = parts[1]
                    score_str = parts[3]
                    try:
                        score = int(score_str.replace('+','').replace('−','-'))
                        if vec_id in kanon_vals:
                            base_v, base_p = kanon_vals[vec_id]
                            trump_v = base_v * score
                            trump_p = base_p * score
                            
                            plane_v += trump_v
                            plane_p += trump_p
                            plane_v_count += 1
                            
                            total_v += trump_v
                            total_p += trump_p
                            total_vectors += 1
                            
                            new_line = f"| {vec_id} | {parts[2]} | {score_str} | {trump_v:+.1f} | {trump_p:+.1f} | {parts[4] if len(parts)>4 else parts[-2]} |"
                            new_trump_lines.append(new_line)
                        else:
                            new_trump_lines.append(line)
                    except ValueError:
                        new_trump_lines.append(line)
                else:
                    new_trump_lines.append(line)
            elif 'Vector | Entry | Trump Score' in line and 'Trump υ' not in line:
                new_trump_lines.append("| Vector | Entry | Trump Score | Trump υ | Trump ψ | Reasoning |")
            elif '---|---|' in line and len(line.split('|')) < 8:
                new_trump_lines.append("|--------|-------|-------------|---------|---------|-----------|")
            else:
                new_trump_lines.append(line)
        
    avg_v = plane_v / plane_v_count if plane_v_count > 0 else 0
    avg_p = plane_p / plane_v_count if plane_v_count > 0 else 0
    
    insert_idx = len(new_trump_lines)
    for i, line in enumerate(new_trump_lines):
        if line.startswith('### Plane') and 'Totality:' in line:
            insert_idx = i
            break
            
    avg_block = [
        "## Plane Average Moral Scores",
        f"**Average Trump υ (Morality):** {avg_v:+.2f}",
        f"**Average Trump ψ (Will):** {avg_p:+.2f}",
        "",
        "---",
        ""
    ]
    
    new_trump_lines = new_trump_lines[:insert_idx] + avg_block + new_trump_lines[insert_idx:]
    
    plane_summaries.append((plane, plane_v, plane_p, plane_v_count))
    
    with open(trump_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_trump_lines))

print("Updated individual planes.")

final_file = os.path.join(base_dir, "Trump_American_Kanon_Final_Score.md")
with open(final_file, 'r', encoding='utf-8') as f:
    final_content = f.read()

new_final_lines = []
skip = False
for line in final_content.split('\n'):
    if line.startswith('### Moral Vectors Averages'):
        skip = True
    if skip and line.startswith('## Synthesis'):
        skip = False
        new_final_lines.append(line)
        continue
    
    if not skip:
        new_final_lines.append(line)

insert_idx = len(new_final_lines)
for i, line in enumerate(new_final_lines):
    if line.startswith('## Synthesis'):
        insert_idx = i
        break

avg_tot_v = total_v / total_vectors if total_vectors > 0 else 0
avg_tot_p = total_p / total_vectors if total_vectors > 0 else 0

avg_table = [
    "### Moral Vectors Averages (Trump Scores * Kanon Values)",
    "",
    "| Plane | Name | Trump Avg υ | Trump Avg ψ |",
    "| :--- | :--- | :---: | :---: |"
]
for p, pv, pp, pcount in plane_summaries:
    name_parts = p.split('_')
    name = f"Plane {name_parts[1]} ({name_parts[2]})"
    avg_v = pv / pcount if pcount > 0 else 0
    avg_p = pp / pcount if pcount > 0 else 0
    avg_table.append(f"| {name} | | {avg_v:+.2f} | {avg_p:+.2f} |")

avg_table.append(f"| **TOTAL** | **AVERAGE** | **{avg_tot_v:+.2f}** | **{avg_tot_p:+.2f}** |")
avg_table.append("")
avg_table.append("---")
avg_table.append("")

new_final_lines = new_final_lines[:insert_idx] + avg_table + new_final_lines[insert_idx:]

with open(final_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_final_lines))

print("Updated final score file.")
