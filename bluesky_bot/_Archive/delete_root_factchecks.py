import os
import glob

def delete_root_factchecks():
    bot_dir = r"e:\Vector Field Theory\VFT Docs\bluesky_bot"
    pattern = os.path.join(bot_dir, "factcheck_*.json")
    files = glob.glob(pattern)
    
    print(f"Found {len(files)} factcheck JSON files in the root of bluesky_bot/.")
    for f in files:
        print(f"Deleting root file: {os.path.basename(f)}")
        try:
            os.remove(f)
        except Exception as e:
            print(f"Error deleting {f}: {e}")
            
    print("Done clearing root factcheck files.")

if __name__ == "__main__":
    delete_root_factchecks()
