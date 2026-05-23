import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

vft_root = r"e:\Vector Field Theory\VFT Docs"
vft_md_io_dir = os.path.join(vft_root, "_VFT MD", "io")
summaries_file = os.path.join(vft_root, "file_summaries.md")

# 1. Read existing summaries and extract the file paths
existing_paths = set()
if os.path.exists(summaries_file):
    with open(summaries_file, "r", encoding="utf-8") as f:
        content = f.read()
    # Find all path entries: **Path**: path
    matches = re.findall(r"\*\*Path\*\*:\s*([^\r\n]+)", content)
    for m in matches:
        # Standardize path separators
        clean_path = m.strip().replace("/", "\\")
        existing_paths.add(clean_path.lower())

print(f"Loaded {len(existing_paths)} existing file summaries.")

# 2. Walk _VFT MD\io to find all .md files
missing_io_files = []
all_io_files = []
if os.path.exists(vft_md_io_dir):
    for root, dirs, files in os.walk(vft_md_io_dir):
        if "_Archive" in root or ".git" in root:
            continue
        for file in files:
            if file.lower().endswith(".md"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, vft_root)
                all_io_files.append(rel_path)
                
                # Check if rel_path is in existing_paths
                if rel_path.lower() not in existing_paths:
                    missing_io_files.append(rel_path)

print(f"Total .md files in _VFT MD\\io: {len(all_io_files)}")
print(f"Missing from file_summaries.md: {len(missing_io_files)}")
if missing_io_files:
    print("\nMissing IO files:")
    for f in missing_io_files:
        print(f"- {f}")
else:
    print("\nAll files in _VFT MD\\io are fully summarized!")
