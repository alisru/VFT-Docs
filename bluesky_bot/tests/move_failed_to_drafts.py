import os
import shutil

fail_dir = r"e:\Vector Field Theory\VFT Docs\bluesky_bot\stories\fail"
stories_dir = r"e:\Vector Field Theory\VFT Docs\bluesky_bot\stories"

moved_count = 0
if os.path.exists(fail_dir):
    for filename in os.listdir(fail_dir):
        if filename.endswith(".json") and filename.startswith("factcheck_"):
            src = os.path.join(fail_dir, filename)
            dst = os.path.join(stories_dir, filename)
            shutil.move(src, dst)
            moved_count += 1

print(f"Moved {moved_count} files from fail/ back to stories/")
