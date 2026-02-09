import os
import hashlib
import json
import shutil
import subprocess
from collections import defaultdict

# --- Configuration ---
ROOT_DIR = r"e:\Vector Field Theory\VFT Docs"
VFT_MD_DIR = os.path.join(ROOT_DIR, "_VFT MD")
AI_DIR = os.path.join(ROOT_DIR, "_AI files and chat logs")
REPORT_PATH = r"e:\Vector Field Theory\VFT Docs\cleanup_report.md"

# Rule: "graph and ai chat text files are meant to be in ai files"
# Rule: "files like temp_ingest_ac030525.json are to be moved int ai files"
AI_MOVE_PATTERNS = [
    (".graph.json", AI_DIR),
    (".chat.txt", AI_DIR), # Assuming chat logs are .chat.txt or similar? Or just .txt in weird places?
    # User said: "ai chat text files". I'll be careful with .txt.
    # User example: "temp_ingest_ac030525.json"
    ("temp_ingest_", AI_DIR),
]

# Rule: "files like ... moved int ai files" -> implicitly Create AI/graphs folders if needed?
# User convo summary 1: "Move all *graph.json files to _AI files and chat logs/graphs"
AI_SUBDIRS = {
    ".graph.json": os.path.join(AI_DIR, "graphs"),
    "temp_ingest_": AI_DIR, # Root of AI dir?
}

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

def is_git_tracked(filepath):
    """Checks if a file is tracked by git."""
    try:
        # Check if ignored (standard check)
        # But user asked about "untracked changes".
        # `git ls-files` shows tracked files.
        result = subprocess.run(
            ["git", "ls-files", filepath],
            cwd=ROOT_DIR,
            capture_output=True,
            text=True,
            check=False
        )
        return bool(result.stdout.strip())
    except Exception:
        return False

def get_preferred_path(paths):
    """
    Decides which path to keep among duplicates.
    Returns: (keep_path, list_of_delete_paths)
    """
    # 1. Git Tracked vs Untracked
    tracked = [p for p in paths if is_git_tracked(p)]
    untracked = [p for p in paths if p not in tracked]
    
    if tracked and not untracked:
        # All tracked. Use heuristics.
        candidates = tracked
    elif untracked and not tracked:
        # All untracked. Use heuristics.
        candidates = untracked
    elif tracked and untracked:
        # Mixed. Prefer tracked.
        candidates = tracked
        if len(candidates) > 1:
            # Tie-break among tracked
            pass
    else:
        # Should not happen
        candidates = paths

    # Heuristic Tie-Breaker (for "Least Sensical")
    # Prefer: Physics, Actualism, WWSUTRU (in that order?) No, "Sensical" matches filename.
    # Or just shortest path? Or longest (more specific)?
    # Usually `_VFT MD\Physics` is better than `_VFT MD\Actualism\Physics_Stuff` if title is Physics.
    
    # Simple Heuristic: Choose the one that matches the filename "theme"? Too hard.
    # Fallback: Alphabetical sort of parent folder?
    # Let's pick the SHORTEST path (closest to root of category).
    candidates.sort(key=lambda p: len(p))
    keep = candidates[0]
    
    return keep, [p for p in paths if p != keep]

def scan_and_clean():
    hash_map = defaultdict(list)
    actions_log = []

    print("Scanning files...")
    for root, dirs, files in os.walk(ROOT_DIR):
        if ".git" in dirs: dirs.remove(".git")
        if ".agent" in dirs: dirs.remove(".agent")
        if ".gemini" in dirs: dirs.remove(".gemini")
        
        for file in files:
            path = os.path.join(root, file)
            fhash = get_file_hash(path)
            if fhash:
                hash_map[fhash].append(path)

    print(f"Found {len(hash_map)} unique files. Processing...")

    # --- Deduplication & User Rules ---
    for fhash, paths in hash_map.items():
        # 1. AI Files Move (Rule: temp_ingest, graphs)
        # Check filename of first path (assume identical names basically)
        filename = os.path.basename(paths[0])
        
        dest_folder = None
        if filename.startswith("temp_ingest_") and filename.endswith(".json"):
             dest_folder = AI_SUBDIRS["temp_ingest_"]
        elif filename.endswith(".graph.json"):
             dest_folder = AI_SUBDIRS[".graph.json"]
        
        if dest_folder:
            # Move ALL instances to dest_folder (deduplicating if multiple)
            target_path = os.path.join(dest_folder, filename)
            
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
                
            # If target already exists and is same hash, delete sources.
            # If target doesn't exist, move one source, delete others.
            
            if os.path.exists(target_path):
                 target_hash = get_file_hash(target_path)
                 if target_hash == fhash:
                     # Already safely there. Delete all sources (unless source IS target)
                     for p in paths:
                         if os.path.abspath(p) != os.path.abspath(target_path):
                             os.remove(p)
                             actions_log.append(f"Deleted duplicate {p} (exists in {target_path})")
                 else:
                     # Conflict!
                     actions_log.append(f"CONFLICT: {filename} exists in destination but hash differs. Skipping.")
            else:
                # Move first one, delete rest
                shutil.move(paths[0], target_path)
                actions_log.append(f"Moved {paths[0]} to {target_path}")
                for p in paths[1:]:
                    os.remove(p)
                    actions_log.append(f"Deleted duplicate {p} (merged to {target_path})")
            continue # Done with this file

        # 2. General Deduplication and Specific Logic
        # Separate paths into _VFT MD and Others
        vft_md_paths = [p for p in paths if "_VFT MD" in p]
        other_paths = [p for p in paths if "_VFT MD" not in p]
        
        # Rule: .bat in Root deleted if in _VFT MD
        if filename.endswith(".bat"):
            if vft_md_paths and other_paths:
                # Delete others
                for p in other_paths:
                    os.remove(p)
                    actions_log.append(f"Deleted root .bat {p} (kept {vft_md_paths[0]})")
                continue

        # Rule: .py in Root deleted if in _VFT MD
        if filename.endswith(".py"):
            if vft_md_paths and other_paths:
                for p in other_paths:
                    os.remove(p)
                    actions_log.append(f"Deleted root .py {p} (kept {vft_md_paths[0]})")
                continue

        # Rule: .docx NOT in _VFT MD
        if filename.endswith(".docx"):
            if vft_md_paths:
                # Move out or Delete
                if other_paths:
                    # Already exists outside. Delete VFT MD version
                    for p in vft_md_paths:
                         os.remove(p)
                         actions_log.append(f"Deleted _VFT MD .docx {p} (exists as {other_paths[0]})")
                else:
                    # Only in VFT MD. Move to "Regular Version".
                    # Try to reconstruct path?
                    # e.g. _VFT MD\Actualism\Doc.docx -> Actualism\Doc.docx
                    for p in vft_md_paths:
                        rel = os.path.relpath(p, VFT_MD_DIR)
                        new_path = os.path.join(ROOT_DIR, rel)
                        new_dir = os.path.dirname(new_path)
                        
                        if not os.path.exists(new_dir):
                            os.makedirs(new_dir)
                            
                        shutil.move(p, new_path)
                        actions_log.append(f"Moved .docx from {p} to {new_path}")
                continue

        # Rule: Internal Duplicates in _VFT MD (Default Logic)
        if len(vft_md_paths) > 1:
             keep, deletes = get_preferred_path(vft_md_paths)
             for p in deletes:
                 os.remove(p)
                 actions_log.append(f"Deleted internal duplicate {p} (kept {keep})")
                 
        # Rule: _VFT MD vs Root Mirror (for MD files)
        # If hash is same, Root is duplicate.
        if filename.endswith(".md") and vft_md_paths and other_paths:
             for p in other_paths:
                 os.remove(p)
                 actions_log.append(f"Deleted root duplicate {p} (kept {vft_md_paths[0]})")

    # Generate Log
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write("# Cleanup Action Log\n\n")
        if not actions_log:
            f.write("No actions taken.\n")
        else:
            for line in actions_log:
                f.write(f"- {line}\n")
    
    print(f"Cleanup complete. Actions logged to {REPORT_PATH}")

if __name__ == "__main__":
    scan_and_clean()
