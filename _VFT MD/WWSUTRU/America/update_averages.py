import os

base_dir = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America"

planes = [
    "Plane_1_Identity", "Plane_2_Definition", "Plane_3_Land", 
    "Plane_4_Drive", "Plane_5_Method", "Plane_6_Cause", "Plane_7_Effect"
]

total_v = 0.0
total_p = 0.0
total_count = 0

plane_averages = []

for plane in planes:
    trump_file = os.path.join(base_dir, f"Trump_American_Kanon_{plane}.md")
    if not os.path.exists(trump_file): continue
    
    lines = open(trump_file, 'r', encoding='utf-8').read().split('\n')
    
    plane_v = 0.0
    plane_p = 0.0
    plane_count = 0
    plane_score_sum = 0
    
    for line in lines:
        if '|' in line and not '---|' in line and not 'Vector | Entry' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 6:
                try:
                    raw_score = parts[3].replace('+','').replace('−','-').strip()
                    if raw_score.startswith('-1'): score = -1
                    elif raw_score.startswith('1'): score = 1
                    else: score = int(raw_score)
                    
                    v = float(parts[4].replace('+','').replace('−','-'))
                    p = float(parts[5].replace('+','').replace('−','-'))
                    plane_v += v
                    plane_p += p
                    plane_score_sum += score
                    plane_count += 1
                except ValueError:
                    pass
    
    avg_v = plane_v / plane_count if plane_count > 0 else 0
    avg_p = plane_p / plane_count if plane_count > 0 else 0
    
    total_v += plane_v
    total_p += plane_p
    total_count += plane_count
    
    plane_averages.append((plane, avg_v, avg_p, plane_score_sum, plane_count))
    
    new_lines = []
    skip = False
    insert_idx = len(lines)
    for i, line in enumerate(lines):
        if line.startswith('## Plane Average Moral Scores'):
            skip = True
        if skip and line.startswith('---'):
            skip = False
            continue
        if line.startswith('### Plane') and 'Totality:' in line:
            insert_idx = len(new_lines)
            new_lines.append(line)
        elif not skip:
            new_lines.append(line)
            
    avg_block = [
        "## Plane Average Moral Scores",
        f"**Average Trump υ (Morality):** {avg_v:+.2f}",
        f"**Average Trump ψ (Will):** {avg_p:+.2f}",
        "",
        "---",
        ""
    ]
    
    final_lines = new_lines[:insert_idx] + avg_block + new_lines[insert_idx:]
    
    for i, line in enumerate(final_lines):
        if line.startswith('**Plane') and 'Score:' in line:
            plane_num = plane.split('_')[1]
            final_lines[i] = f"**Plane {plane_num} Score: {plane_score_sum:+} / {plane_count}**"
            
    with open(trump_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(final_lines))

print("Updated plane averages.")

final_file = os.path.join(base_dir, "Trump_American_Kanon_Final_Score.md")
final_content = open(final_file, 'r', encoding='utf-8').read()

new_final_lines = []
skip = False
insert_idx = len(final_content.split('\n'))

for line in final_content.split('\n'):
    if line.startswith('### Moral Vectors Averages'):
        skip = True
    if skip and line.startswith('## Synthesis'):
        skip = False
        insert_idx = len(new_final_lines)
        new_final_lines.append(line)
        continue
    if not skip:
        new_final_lines.append(line)

avg_tot_v = total_v / total_count if total_count > 0 else 0
avg_tot_p = total_p / total_count if total_count > 0 else 0

avg_table = [
    "### Moral Vectors Averages (Trump Scores * Kanon Values)",
    "",
    "| Plane | Name | Trump Avg υ | Trump Avg ψ |",
    "| :--- | :--- | :---: | :---: |"
]
for p, avg_v, avg_p, score_sum, count in plane_averages:
    name_parts = p.split('_')
    name = f"Plane {name_parts[1]} ({name_parts[2]})"
    avg_table.append(f"| {name} | | {avg_v:+.2f} | {avg_p:+.2f} |")

avg_table.append(f"| **TOTAL** | **AVERAGE** | **{avg_tot_v:+.2f}** | **{avg_tot_p:+.2f}** |")
avg_table.append("")
avg_table.append("---")
avg_table.append("")

for i, line in enumerate(new_final_lines):
    if line.startswith('## Synthesis'):
        insert_idx = i
        break

new_final_lines = new_final_lines[:insert_idx] + avg_table + new_final_lines[insert_idx:]

with open(final_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_final_lines))
    
print("Updated final score doc.")
