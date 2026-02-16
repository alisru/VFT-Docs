
target_file = r"E:\Vector Field Theory\VFT Docs\file_summaries_comprehensive.md"

with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Lines are 1-indexed in view_file
# 1485-1808 (inclusive)
# 0-indexed: 1484 to 1807
block_to_move = lines[1484:1808]

# Delete the block
del lines[1484:1808]

# Re-find the marker (it will have moved up)
marker = "## WWSUTRU\n"
insertion_index = -1
for i, line in enumerate(lines):
    if line == marker:
        insertion_index = i
        break

if insertion_index != -1:
    # Insert after the marker
    for i, block_line in enumerate(block_to_move):
        lines.insert(insertion_index + 1 + i, block_line)
    
    with open(target_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Successfully moved WWSUTRU block.")
else:
    print("Marker '## WWSUTRU' not found after deletion.")
