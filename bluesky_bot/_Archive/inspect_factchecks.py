import os
import json
import glob

def inspect_files():
    stories_dir = r"e:\Vector Field Theory\VFT Docs\bluesky_bot\stories"
    pattern = os.path.join(stories_dir, "**", "factcheck_*.json")
    files = glob.glob(pattern, recursive=True)
    
    print(f"Total files found: {len(files)}")
    corrupted = []
    valid = []
    
    for f_path in files:
        try:
            with open(f_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            cfg = data[0] if isinstance(data, list) else data
            
            # Check required keys
            required_keys = ["claim_u", "claim_psi", "real_u", "real_psi", "subject", "posts", "link"]
            missing = [k for k in required_keys if k not in cfg]
            
            # Also check if any key has null value when it shouldn't
            null_vals = []
            if not missing:
                for k in ["claim_u", "claim_psi", "real_u", "real_psi"]:
                    if cfg[k] is None:
                        null_vals.append(k)
            
            if missing or null_vals:
                corrupted.append((f_path, missing, null_vals, cfg.keys()))
            else:
                valid.append(f_path)
        except Exception as e:
            corrupted.append((f_path, ["LOAD_ERROR"], [str(e)], []))
            
    print(f"\n--- VALID FILES ({len(valid)}) ---")
    for v in valid[:5]:
        print(f"  {os.path.basename(v)}")
    if len(valid) > 5:
        print(f"  ... and {len(valid) - 5} more")
        
    print(f"\n--- CORRUPTED/INVALID FILES ({len(corrupted)}) ---")
    for path, missing, nulls, keys in corrupted:
        print(f"File: {os.path.basename(path)}")
        if missing:
            print(f"  Missing keys: {missing}")
        if nulls:
            print(f"  Null values: {nulls}")
        print(f"  Available keys: {list(keys)}")
        print("-" * 40)

if __name__ == "__main__":
    inspect_files()
