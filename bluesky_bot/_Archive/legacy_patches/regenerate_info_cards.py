import glob
import json
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

from image_card_generator import generate_compact_info_card

def main():
    stories = glob.glob(os.path.join(script_dir, "stories", "factcheck_*.json"))
    for p in stories:
        filename = os.path.basename(p)
        slug = filename[len("factcheck_"):-len(".json")]
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
            cfg = data[0] if isinstance(data, list) else data
            
            base_path = os.path.join(script_dir, "graph_png", f"{slug}_info_card.png")
            print(f"Regenerating info cards for {slug}...")
            generate_compact_info_card(cfg, base_path)
        except Exception as e:
            print(f"Error generating info cards for {slug}: {e}")

if __name__ == "__main__":
    main()
