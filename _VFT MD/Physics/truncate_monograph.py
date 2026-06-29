import sys

file_path = r'e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\The Geometry of Definition Monograph.md'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
except Exception as e:
    print(f"Error reading: {e}")
    sys.exit(1)

# Find the start of Chapter 2
cut_index = -1
for i, line in enumerate(lines):
    if "## CHAPTER 2: PHONETIC ARCHITECTURES" in line:
        cut_index = i
        break

if cut_index != -1:
    # Back up a bit to remove the horizontal rule before it if it exists
    if cut_index > 1 and "---" in lines[cut_index - 2]:
        cut_index -= 2
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines[:cut_index])
    print(f"Truncated file at line {cut_index}, removing Chapter 2 and 3.")
else:
    print("Could not find Chapter 2 marker.")
