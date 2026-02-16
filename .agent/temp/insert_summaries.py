
import os

target_file = r"E:\Vector Field Theory\VFT Docs\file_summaries_comprehensive.md"
source_file = r"E:\Vector Field Theory\VFT Docs\.agent\temp\wwsutru_filtered_chunk6.md"

with open(source_file, 'r', encoding='utf-8') as f:
    new_content = f.read()

with open(target_file, 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# Find the insertion point: before "## WWSUTRU"
insertion_index = -1
for i, line in enumerate(lines):
    if line.strip() == "## WWSUTRU":
        insertion_index = i
        break

if insertion_index != -1:
    # Check if there's enough space
    insertion_point = insertion_index - 1 if insertion_index > 0 and lines[insertion_index-1].strip() == "" else insertion_index
    
    lines.insert(insertion_point, "\n" + new_content + "\n\n")
    
    with open(target_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"Successfully inserted content at line {insertion_point + 1}")
else:
    print("Error: Could not find insertion point '## WWSUTRU'")
