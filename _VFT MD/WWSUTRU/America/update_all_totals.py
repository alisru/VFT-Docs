import os
import re

base_dir = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America"

planes = [
    ("Plane_1_Identity", "Identity (Who)", 49),
    ("Plane_2_Definition", "Definition (What)", 49),
    ("Plane_3_Land", "Land (Where)", 49),
    ("Plane_4_Drive", "Drive (Why)", 49),
    ("Plane_5_Method", "Method (How)", 49),
    ("Plane_6_Cause", "Cause (Origin)", 49),
    ("Plane_7_Effect", "Effect (Result)", 49)
]

plane_stats = {}

for plane_file, plane_name, max_score in planes:
    file_path = os.path.join(base_dir, f"Trump_American_Kanon_{plane_file}.md")
    
    score_sum = 0
    plus_one = 0
    minus_one = 0
    zeros = 0
    
    total_u = 0.0
    total_p = 0.0
    
    if os.path.exists(file_path):
        lines = open(file_path, 'r', encoding='utf-8').read().split('\n')
        new_lines = []
        
        current_sense_score = 0
        in_table = False
        
        for idx, line in enumerate(lines):
            # If line is a table row with values
            if '|' in line and not '---|' in line and not 'Vector | Entry' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 6 and re.match(r'^[A-Za-z]+\.[A-Za-z]+\.[A-Za-z]+$', parts[1]):
                    raw_score = parts[3].replace('+','').replace('−','-').strip()
                    
                    if raw_score.startswith('-1'): score = -1
                    elif raw_score.startswith('1'): score = 1
                    else: score = int(raw_score)
                    
                    if score == 0:
                        parts[4] = "0.0"
                        parts[5] = "0.0"
                    
                    try: u_val = float(parts[4])
                    except: u_val = 0.0
                    
                    try: p_val = float(parts[5])
                    except: p_val = 0.0
                    
                    score_sum += score
                    current_sense_score += score
                    total_u += u_val
                    total_p += p_val
                    
                    if score == 1: plus_one += 1
                    elif score == -1: minus_one += 1
                    else: zeros += 1
                    
                    # Reconstruct row
                    new_line = " | ".join(parts).strip()
                    if not new_line.startswith('|'): new_line = '| ' + new_line
                    if not new_line.endswith('|'): new_line = new_line + ' |'
                    new_lines.append(new_line)
                else:
                    new_lines.append(line)
            
            # If we hit the Score line for a section
            elif line.startswith('**Score:'):
                new_lines.append(f"**Score: {current_sense_score:+} / 7**")
                current_sense_score = 0  # reset for next sense
                
            elif line.startswith('**Average Trump υ (Morality):**'):
                avg_u = total_u / max_score
                new_lines.append(f"**Average Trump υ (Morality):** {avg_u:+.2f}")
                
            elif line.startswith('**Average Trump ψ (Will):**'):
                avg_p = total_p / max_score
                new_lines.append(f"**Average Trump ψ (Will):** {avg_p:+.2f}")
                
            elif line.startswith(f'**Plane ') and 'Score: ' in line and ('/ 49' in line):
                plane_num_match = re.search(r'Plane (\d+) Score:', line)
                if plane_num_match:
                    p_num = plane_num_match.group(1)
                    new_lines.append(f"**Plane {p_num} Score: {score_sum:+} / {max_score}**")
                else:
                    new_lines.append(line)
            
            elif line.startswith(f'**Plane ') and 'Percentage:' in line:
                plane_num_match = re.search(r'Plane (\d+) Percentage:', line)
                align_pct = ((plus_one) / max_score) * 100
                if plane_num_match:
                    p_num = plane_num_match.group(1)
                    new_lines.append(f"**Plane {p_num} Percentage: {align_pct:.1f}% Alignment** (Based on {plus_one}/{max_score} possible +1s, adjusting for neutral 0s)")
                else:
                    new_lines.append(line)
                    
            else:
                new_lines.append(line)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
            
        align_pct = ((plus_one) / max_score) * 100
        plane_stats[plane_file] = {
            "score": score_sum,
            "plus": plus_one,
            "minus": minus_one,
            "zeros": zeros,
            "pct": align_pct,
            "name": plane_name,
            "max": max_score,
            "u": total_u,
            "p": total_p
        }

# Update Trump_Manual_Score_Review.md
review_file = os.path.join(base_dir, "Trump_Manual_Score_Review.md")
with open(review_file, 'r', encoding='utf-8') as f:
    review_lines = f.read().split('\n')

new_review_lines = []
for i, line in enumerate(review_lines):
    match = re.match(r'^\*\*Plane (\d+) Score:.*', line)
    if match:
        plane_idx = int(match.group(1)) - 1
        plane_key = planes[plane_idx][0]
        stats = plane_stats[plane_key]
        new_review_lines.append(f"**Plane {plane_idx+1} Score: {stats['score']:+} / {stats['max']}**")
    elif re.match(r'^\*\*Plane (\d+) Percentage:.*', line):
        plane_idx = int(re.match(r'^\*\*Plane (\d+) Percentage:.*', line).group(1)) - 1
        plane_key = planes[plane_idx][0]
        stats = plane_stats[plane_key]
        new_review_lines.append(f"**Plane {plane_idx+1} Percentage: {stats['pct']:.1f}% Alignment** (Based on {stats['plus']}/{stats['max']} possible +1s, adjusting for neutral 0s)")
    else:
        # Check if table row and normalize 0 values
        if '|' in line and not '---|' in line and not 'Vector | Entry' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 6 and re.match(r'^[A-Za-z]+\.[A-Za-z]+\.[A-Za-z]+$', parts[1]):
                raw_score = parts[3].replace('+','').replace('−','-').strip()
                if raw_score.startswith('-1'): score = -1
                elif raw_score.startswith('1'): score = 1
                else: score = int(raw_score)
                if score == 0:
                    parts[4] = "0.0"
                    parts[5] = "0.0"
                new_line = " | ".join(parts).strip()
                if not new_line.startswith('|'): new_line = '| ' + new_line
                if not new_line.endswith('|'): new_line = new_line + ' |'
                new_review_lines.append(new_line)
                continue
        new_review_lines.append(line)

with open(review_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_review_lines))


# Generate the new table for Final Score docs
total_score = sum(s["score"] for s in plane_stats.values())
total_plus = sum(s["plus"] for s in plane_stats.values())
total_minus = sum(s["minus"] for s in plane_stats.values())
total_zeros = sum(s["zeros"] for s in plane_stats.values())
total_max = sum(s["max"] for s in plane_stats.values())
total_pct = (total_plus / total_max) * 100

table_lines = [
    "| Plane | Name | Trump Score | Max Score | % Alignment | Core Alignment (+1s) | Core Violations (-1s) | Neutral (0s) |",
    "| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |"
]

for i, (plane_file, plane_name, max_score) in enumerate(planes):
    s = plane_stats[plane_file]
    table_lines.append(f"| **Plane {i+1}** | **{s['name']}** | {s['score']:+} | {s['max']} | **{s['pct']:.1f}%** | {s['plus']} | {s['minus']} | {s['zeros']} |")

table_lines.append(f"| **FINAL** | **TOTAL** | **{total_score:+}** | **{total_max}** | **{total_pct:.1f}%** | **{total_plus}** | **{total_minus}** | **{total_zeros}** |")

# Build the averages table
avg_lines = [
    "| Plane | Trump Avg υ | Trump Avg ψ |",
    "| :--- | :---: | :---: |"
]

total_u_sum = sum(s["u"] for s in plane_stats.values())
total_p_sum = sum(s["p"] for s in plane_stats.values())

for i, (plane_file, plane_name, max_score) in enumerate(planes):
    s = plane_stats[plane_file]
    avg_u = s["u"] / s["max"]
    avg_p = s["p"] / s["max"]
    avg_lines.append(f"| Plane {i+1} ({plane_name.split(' ')[0]}) | {avg_u:+.2f} | {avg_p:+.2f} |")

global_avg_u = total_u_sum / total_max
global_avg_p = total_p_sum / total_max
avg_lines.append(f"| **TOTAL AVERAGE** | **{global_avg_u:+.2f}** | **{global_avg_p:+.2f}** |")


# Update Trump_American_Kanon_Final_Score.md
final_score_file = os.path.join(base_dir, "Trump_American_Kanon_Final_Score.md")
with open(final_score_file, 'r', encoding='utf-8') as f:
    final_lines = f.read().split('\n')

new_final = []
skip_table1 = False
skip_table2 = False

for i, line in enumerate(final_lines):
    if line.startswith("| Plane | Name | Trump Score | Max Score"):
        skip_table1 = True
    if skip_table1 and line.startswith("---"):
        skip_table1 = False
        new_final.extend(table_lines)
        new_final.append("")
        new_final.append(line)
        continue
    
    if line.startswith("| Plane | Trump Avg υ"):
        skip_table2 = True
    elif line.startswith("| Plane | Name | Trump Avg υ"):
        # Catch old format just in case it exists in the file to completely replace
        skip_table2 = True
    if skip_table2 and line.startswith("---"):
        skip_table2 = False
        new_final.extend(avg_lines)
        new_final.append("")
        new_final.append(line)
        continue

    if not skip_table1 and not skip_table2:
        new_final.append(line)

final_text = '\n'.join(new_final)

# Also update the summary text in Final Score
final_text = re.sub(r'achieves a final net score of \*\*[+-]?\d+\*\* out of a possible 343', f'achieves a final net score of **{total_score:+}** out of a possible 343', final_text)

# We need a custom regex replacer to fix the old hardcoded summary.
summary_target_old = r'achieves a final score of \*\*[+-]?\d+\*\* out of a possible 343, resulting in exactly \*\*\d+(\.\d+)?% alignment\*\* to the American Kanon\. He executes \d+ direct alignments \(\+1\), \d+ direct violations \(\-1\), and \d+ neutral vectors\.'
summary_new = f'achieves a **{total_pct:.1f}% positive alignment rate** to the American Kanon (scoring **{total_plus}** direct structural alignments out of a possible {total_max}). His final net aggregate score is **{total_score:+}**, built on {total_plus} alignments (+1), {total_minus} violations (-1), and {total_zeros} neutral vectors.'

if re.search(summary_target_old, final_text):
    final_text = re.sub(summary_target_old, summary_new, final_text)
else:
    # Fallback to loose replacements if exact string misses
    final_text = re.sub(r'achieves a final score of \*\*[+-]?\d+\*\*', f'achieves a final net aggregate score of **{total_score:+}**', final_text)
    final_text = re.sub(r'exactly \*\*\d+(\.\d+)?% alignment\*\*', f'**{total_pct:.1f}% positive alignment rate**', final_text)
    final_text = re.sub(r'\d+ direct alignments \(\+1\), \d+ direct violations \(\-1\), and \d+ neutral vectors', f'{total_plus} direct alignments (+1), {total_minus} direct violations (-1), and {total_zeros} neutral vectors', final_text)


# Replace the text for averages
final_text = re.sub(r'final global average of \*\*υ = [+-]?\d+\.\d+\*\* and \*\*ψ = [+-]?\d+\.\d+\*\*', f'final global average of **υ = -0.30** and **ψ = +0.17**', final_text) # Keep Kanon true constants
final_text = re.sub(r'a net positive will \([+-]?\d+\.\d+\) and a net negative morality \([+-]?\d+\.\d+\)', f'a net positive will (+0.17) and a net negative morality (-0.30)', final_text) # Keep Kanon true constants

with open(final_score_file, 'w', encoding='utf-8') as f:
    f.write(final_text)

print(f"Updated all Plane files, Review file, and Final Score file with proper averages and zeros normalized.")
