import os
import hashlib
import json
from collections import defaultdict

# Configuration
ROOT_DIR = r"e:\Vector Field Theory\VFT Docs"
INDEX_PATH = r"e:\Vector Field Theory\VFT Docs\index_data.json"
REPORT_PATH = r"e:\Vector Field Theory\VFT Docs\audit_report.md"

# Ignore these directories for the "content" scan (we want to check source vs destination)
# Actually, we want to scan everything to find where duplicates are hiding.
# But we might want to exclude system folders.
EXCLUDE_DIRS = {'.git', '.agent', '.gemini', '.vscode', 'node_modules', '__pycache__'}
# We explicitly WANT to scan _VFT MD, root folders (Actualism, Physics, etc.).

def get_file_hash(filepath):
    """Calculates MD5 hash of a file."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read(65536)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(65536)
        return hasher.hexdigest()
    except Exception as e:
        return None

def scan_files(root_dir):
    """Scans files and builds a hash map."""
    hash_map = defaultdict(list)
    file_count = 0
    
    print(f"Scanning {root_dir}...")
    
    for root, dirs, files in os.walk(root_dir):
        # Filter exclusions efficiently
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            filepath = os.path.join(root, file)
            
            # Skip temp files or obvious ignores based on extension/name if needed
            if file.startswith('~$') or file == 'index_data.json' or file == 'audit_report.md':
                continue
                
            file_hash = get_file_hash(filepath)
            if file_hash:
                hash_map[file_hash].append(filepath)
                file_count += 1
                if file_count % 100 == 0:
                    print(f"Scanned {file_count} files...", end='\r')
                    
    print(f"\nScan complete. Total files: {file_count}")
    return hash_map

def generate_report(hash_map):
    """Generates a markdown report of the findings."""
    
    timestamp = os.path.getmtime(ROOT_DIR) # Just a placeholder/dynamic would be better
    
    report_lines = []
    report_lines.append(f"# Deep Scan Audit Report")
    report_lines.append(f"**Root**: `{ROOT_DIR}`")
    report_lines.append(f"**Total Unique Contents**: {len(hash_map)}")
    
    duplicate_sets = [paths for paths in hash_map.values() if len(paths) > 1]
    total_duplicates = sum(len(paths) - 1 for paths in duplicate_sets)
    
    report_lines.append(f"**Duplicate Instances**: {total_duplicates} (files that are copies of something else)")
    report_lines.append("\n## Executive Summary")
    
    if total_duplicates == 0:
        report_lines.append("✅ No duplicates found.")
    else:
        report_lines.append(f"⚠️ **Found {len(duplicate_sets)} sets of duplicates.**")
        report_lines.append("This confirms the user's suspicion of 'fucked up' structure.")
        
    report_lines.append("\n## Detailed Duplicate Analysis")
    report_lines.append("| Status | Count | File Name (Representative) | Loctions |")
    report_lines.append("|:---|:---|:---|:---|")
    
    # Categorization logic
    
    # We want to know:
    # 1. Is it in _VFT MD? (The "Canonical" location)
    # 2. Is it in a Content Root? (e.g. Physics, Actualism - The "Source" we are trying to clean)
    # 3. Is it in IO? (Input)
    
    # Canonical Paths
    VFT_MD_DIR = os.path.join(ROOT_DIR, "_VFT MD")
    
    for paths in duplicate_sets:
        # Determine status
        in_vft_md = any("_VFT MD" in p for p in paths)
        in_io = any(r"\io" in p or "/io/" in p for p in paths)
        
        # Get filename (take the first one)
        filename = os.path.basename(paths[0])
        
        # Shorten paths for display
        short_paths = []
        for p in paths:
            rel = os.path.relpath(p, ROOT_DIR)
            short_paths.append(rel)
            
        locations_str = "<br>".join([f"`{p}`" for p in short_paths])
        
        status = "❓ Unknown"
        if in_vft_md:
            # If it's in VFT MD and somewhere else, the "somewhere else" is likely the debris.
            # Check if multiple are in VFT MD?
            vft_md_count = sum(1 for p in short_paths if "_VFT MD" in p)
            if vft_md_count > 1:
                 status = "🔴 **INTERNAL DUPE** (_VFT MD)"
            else:
                 status = "🟡 **SAFE DUPE** (Canon + Stray)"
        else:
             status = "🟠 **ORPHAN DUPE** (No Canon Copy)"
             
        report_lines.append(f"| {status} | {len(paths)} | {filename} | {locations_str} |")

    report_lines.append("\n## File Integrity Check (Leading Spaces)")
    # Check for filenames with leading spaces
    bad_filenames = []
    all_files = [p for paths in hash_map.values() for p in paths]
    for p in all_files:
        name = os.path.basename(p)
        if name.startswith(" ") or name.startswith("_ ") or "  " in name:
            bad_filenames.append(os.path.relpath(p, ROOT_DIR))
            
    if bad_filenames:
        report_lines.append(f"\n⚠️ **Found {len(bad_filenames)} files with bad naming (leading/double spaces):**")
        for f in bad_filenames[:50]: # Cap output
             report_lines.append(f"- `{f}`")
        if len(bad_filenames) > 50:
            report_lines.append(f"- ... and {len(bad_filenames)-50} more.")
    else:
        report_lines.append("\n✅ No naming issues found.")

    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_lines))
        
    print(f"Report generated at {REPORT_PATH}")

if __name__ == "__main__":
    hash_map = scan_files(ROOT_DIR)
    generate_report(hash_map)
