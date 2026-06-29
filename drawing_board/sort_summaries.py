import os
import re
import shutil

repo_root = r"E:\Vector Field Theory\VFT Docs"
io_dir = os.path.join(repo_root, "_VFT MD", "io")
summaries_file = os.path.join(repo_root, "file_summaries.md")

# Parse file_summaries.md to build a map of filename -> relative destination path
filename_dest_map = {}

# We look for lines like:
# ### Filename.docx (or .md, etc.)
# **Path**: Relative\Path\To\File.docx
# Or matching from the markdown tables
# e.g., | File Name | ... | Classification | -> mapping to directories

with open(summaries_file, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# 1. Parse from Round 16 style sections:
# ### File Name.docx
# **Path**: Actualism\Consciousness\The Geometry of Cognition...
matches = re.findall(r"###\s*(.+?)\r?\n\*\*Path\*\*:\s*`?(.+?)`?\r?\n", content)
for file_header, rel_path in matches:
    # Get base name without extension
    base_name = os.path.splitext(file_header.strip())[0].strip()
    # Normalize path
    rel_path = rel_path.strip().replace("`", "")
    filename_dest_map[base_name] = rel_path

# Normalize the keys by stripping weird quotes and characters
cleaned_map = {}
for k, v in filename_dest_map.items():
    clean_k = k.replace("：", ":").replace("＂", '"').strip()
    cleaned_map[clean_k] = v

print(f"Parsed {len(cleaned_map)} file paths from summaries.")

# Scan _VFT MD\io for files and move them to their corresponding location
io_files = os.listdir(io_dir)
moved_count = 0

for f in io_files:
    if not os.path.isfile(os.path.join(io_dir, f)):
        continue
        
    f_base, f_ext = os.path.splitext(f)
    # Check exact match, check fuzzy clean match
    match_key = None
    if f_base in cleaned_map:
        match_key = f_base
    else:
        # Check fuzzy match by stripping non-alphanumeric chars
        def fuzzy(s):
            return re.sub(r'[^a-zA-Z0-9]', '', s).lower()
        for k in cleaned_map.keys():
            if fuzzy(k) == fuzzy(f_base):
                match_key = k
                break
                
    if match_key:
        rel_dest = cleaned_map[match_key]
        # Swap extension of destination to match the file we are moving (.md / .cs)
        dest_base, _ = os.path.splitext(rel_dest)
        dest_rel_file = dest_base + f_ext
        dest_abs_path = os.path.join(repo_root, dest_rel_file)
        
        # Ensure target directory exists
        os.makedirs(os.path.dirname(dest_abs_path), exist_ok=True)
        
        print(f"Moving {f} -> {dest_rel_file}")
        try:
            shutil.move(os.path.join(io_dir, f), dest_abs_path)
            moved_count += 1
        except Exception as e:
            print(f"  Error moving {f}: {e}")
            
print(f"\nSuccessfully sorted {moved_count} files into their classification folders.")
