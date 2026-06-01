import os
import json
import glob

def clean_duplicate_files():
    # Directories
    bot_stories_dir = r"e:\Vector Field Theory\VFT Docs\bluesky_bot\stories"
    gen_stories_dir = r"e:\Vector Field Theory\VFT Docs\_Generated_Content\stories"
    
    # We want to find exact duplicates and clean them up
    # Standard non-live story files vs live story files
    # First: find duplicates in bot_stories_dir and gen_stories_dir
    for s_dir in [bot_stories_dir, gen_stories_dir]:
        if not os.path.exists(s_dir):
            continue
            
        print(f"\nProcessing directory: {s_dir}")
        pattern = os.path.join(s_dir, "**", "factcheck_*.json")
        files = glob.glob(pattern, recursive=True)
        
        # Maps subject/url -> files
        url_map = {}
        for f_path in files:
            try:
                with open(f_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                cfg = data[0] if isinstance(data, list) else data
                link = cfg.get("link")
                subject = cfg.get("subject", "").lower().strip()
                
                # Check for live versus non-live paths
                is_live = "live" in f_path.lower()
                
                if link:
                    url_map.setdefault(link, []).append((f_path, is_live))
            except Exception as e:
                print(f"Error reading {f_path}: {e}")
                
        # Resolve duplicates
        for url, paths_info in url_map.items():
            if len(paths_info) > 1:
                print(f"\nDuplicate found for URL: {url}")
                # Separate into live and non-live files
                live_files = [p for p, is_l in paths_info if is_l]
                non_live_files = [p for p, is_l in paths_info if not is_l]
                
                # Rule:
                # If there are live files and non-live files:
                # We KEEP only the live files (they have posting status, rkeys, etc.). Delete all non-live files.
                # If there are multiple live files:
                # Keep the one with the cleaner name/correct structure, delete others.
                # If there are multiple non-live files:
                # Keep the one with the cleaner/more complete name, delete others.
                
                if live_files and non_live_files:
                    for nlf in non_live_files:
                        print(f"  Deleting non-live duplicate in favor of live file: {os.path.basename(nlf)}")
                        try:
                            os.remove(nlf)
                        except Exception as e:
                            print(f"  Error deleting: {e}")
                
                # Clean up name clashes in the same subfolder
                # Let's group remaining files in same subdirectory
                subfolder_files = {}
                for p, is_l in paths_info:
                    if os.path.exists(p): # Check if already deleted
                        parent = os.path.dirname(p)
                        subfolder_files.setdefault(parent, []).append(p)
                        
                for subfolder, sub_paths in subfolder_files.items():
                    if len(sub_paths) > 1:
                        # Duplicates inside the SAME folder! (e.g. factcheck_volvo.json vs factcheck_volvo_ev_target_retreat.json)
                        # We keep the one that matches our standard naming convention or is more descriptive,
                        # or if one is factcheck_volvo.json and another is factcheck_volvo_ev_target_retreat.json,
                        # we keep factcheck_volvo_ev_target_retreat.json because it matches the ID/slug better.
                        # Let's sort by length of filename - longer is usually more descriptive/correct!
                        sub_paths_sorted = sorted(sub_paths, key=lambda x: len(os.path.basename(x)), reverse=True)
                        keep_file = sub_paths_sorted[0]
                        delete_files = sub_paths_sorted[1:]
                        
                        print(f"  Clash inside same folder {os.path.basename(subfolder)}:")
                        print(f"    Keeping: {os.path.basename(keep_file)}")
                        for df in delete_files:
                            print(f"    Deleting: {os.path.basename(df)}")
                            try:
                                os.remove(df)
                            except Exception as e:
                                print(f"    Error deleting: {e}")

    # Let's clean up index.json in stories folders too so they don't reference deleted files
    for s_dir in [bot_stories_dir, gen_stories_dir]:
        for sub in ["", "live"]:
            target_dir = os.path.join(s_dir, sub) if sub else s_dir
            index_path = os.path.join(target_dir, "index.json")
            if os.path.exists(index_path):
                print(f"\nCleaning index.json at {index_path}...")
                try:
                    with open(index_path, "r", encoding="utf-8") as f:
                        filenames = json.load(f)
                    
                    cleaned_filenames = []
                    for fn in filenames:
                        if os.path.exists(os.path.join(target_dir, fn)):
                            cleaned_filenames.append(fn)
                        else:
                            print(f"  Removing orphaned index reference: {fn}")
                            
                    with open(index_path, "w", encoding="utf-8") as f:
                        json.dump(cleaned_filenames, f, indent=2, ensure_ascii=False)
                except Exception as e:
                    print(f"  Error cleaning index.json: {e}")

if __name__ == "__main__":
    clean_duplicate_files()
