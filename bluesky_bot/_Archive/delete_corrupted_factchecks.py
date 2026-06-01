import os
import json
import glob
import sys

def delete_corrupted_and_rebuild():
    stories_dir = r"e:\Vector Field Theory\VFT Docs\bluesky_bot\stories"
    pattern = os.path.join(stories_dir, "**", "factcheck_*.json")
    files = glob.glob(pattern, recursive=True)
    
    deleted_count = 0
    
    for f_path in files:
        try:
            with open(f_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            cfg = data[0] if isinstance(data, list) else data
            required_keys = ["claim_u", "claim_psi", "real_u", "real_psi", "subject", "posts", "link"]
            missing = [k for k in required_keys if k not in cfg]
            
            null_vals = []
            if not missing:
                for k in ["claim_u", "claim_psi", "real_u", "real_psi"]:
                    if cfg[k] is None:
                        null_vals.append(k)
                        
            if missing or null_vals:
                print(f"Deleting corrupted file: {os.path.basename(f_path)}")
                os.remove(f_path)
                deleted_count += 1
        except Exception as e:
            print(f"Deleting load-error file {os.path.basename(f_path)}: {e}")
            try:
                os.remove(f_path)
                deleted_count += 1
            except Exception as delete_error:
                print(f"Failed to delete {f_path}: {delete_error}")
                
    print(f"\nDeleted {deleted_count} corrupted factcheck configurations.")
    
    # Now run rebuild_registries.py logic!
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    sys.path.append(os.path.join(parent_dir, "scratch"))
    
    import rebuild_registries
    print("Rebuilding registries...")
    rebuild_registries.rebuild_registries()

if __name__ == "__main__":
    delete_corrupted_and_rebuild()
