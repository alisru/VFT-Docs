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
    
    if os.path.exists(file_path):
        lines = open(file_path, 'r', encoding='utf-8').read().split('\n')
        for line in lines:
            if '|' in line and not '---|' in line and not 'Vector | Entry' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 6:
                    try:
                        raw_score = parts[3].replace('+','').replace('−','-').strip()
                        if raw_score.startswith('-1'): score = -1
                        elif raw_score.startswith('1'): score = 1
                        else: score = int(raw_score)
                        
                        score_sum += score
                        if score == 1: plus_one += 1
                        elif score == -1: minus_one += 1
                        else: zeros += 1
                    except ValueError:
                        pass
    
    align_pct = ((plus_one) / max_score) * 100
    
    plane_stats[plane_file] = {
        "score": score_sum,
        "plus": plus_one,
        "minus": minus_one,
        "zeros": zeros,
        "pct": align_pct,
        "name": plane_name,
        "max": max_score
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

# Update Trump_American_Kanon_Final_Score.md
final_score_file = os.path.join(base_dir, "Trump_American_Kanon_Final_Score.md")
with open(final_score_file, 'r', encoding='utf-8') as f:
    final_lines = f.read().split('\n')

new_final = []
skip = False
for i, line in enumerate(final_lines):
    if line.startswith("| Plane | Name | Trump Score | Max Score"):
        skip = True
    if skip and line.startswith("---"):
        skip = False
        new_final.extend(table_lines)
        new_final.append("")
        new_final.append(line)
        continue
    if not skip:
        new_final.append(line)

final_text = '\n'.join(new_final)

# Also update the summary text in Final Score
final_text = re.sub(r'achieves a final score of \*\*[+-]?\d+\*\* out of a possible 343', f'achieves a final score of **{total_score:+}** out of a possible 343', final_text)
final_text = re.sub(r'exactly \*\*\d+(\.\d+)?% alignment\*\* to the American Kanon', f'exactly **{total_pct:.1f}% alignment** to the American Kanon', final_text)
final_text = re.sub(r'\d+ direct alignments \(\+1\), \d+ direct violations \(\-1\), and \d+ neutral vectors', f'{total_plus} direct alignments (+1), {total_minus} direct violations (-1), and {total_zeros} neutral vectors', final_text)

with open(final_score_file, 'w', encoding='utf-8') as f:
    f.write(final_text)

print("Totals updated in Trump_Manual_Score_Review.md and Trump_American_Kanon_Final_Score.md")
