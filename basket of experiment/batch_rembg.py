import os
import sys
from pathlib import Path
from PIL import Image
import warnings

# Suppress onnxruntime warnings
warnings.filterwarnings("ignore")

from rembg import remove, new_session

def main():
    src_dir = Path(r"e:\Vector Field Theory\VFT Docs\basket of experiment")
    out_dir = src_dir / "nobg"
    out_dir.mkdir(exist_ok=True)

    print("Initializing U2Net session on CPU...")
    session = new_session("u2net", providers=["CPUExecutionProvider"])

    extensions = {".jpg", ".jpeg", ".png"}
    files = [
        f for f in sorted(src_dir.iterdir())
        if f.suffix.lower() in extensions and f.is_file() and not f.name.startswith("hegemony")
    ]

    total = len(files)
    print(f"Found {total} images to process.")

    processed = 0
    skipped = 0

    for i, file_path in enumerate(files, 1):
        target_name = f"{file_path.stem}.png"
        out_path = out_dir / target_name

        if out_path.exists() and out_path.stat().st_size > 1000:
            print(f"[{i}/{total}] Skipping (already exists): {file_path.name}")
            skipped += 1
            continue

        print(f"[{i}/{total}] Processing: {file_path.name} -> {target_name}...")
        try:
            with Image.open(file_path) as img:
                res = remove(img, session=session)
                res.save(out_path, format="PNG")
                processed += 1
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")

    print(f"\nDone! Processed: {processed}, Skipped: {skipped}, Total: {total}")

if __name__ == "__main__":
    main()
