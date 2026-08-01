import os
import sys
import json

# Add script's parent directory to path to allow importing from bluesky_bot
script_dir = os.path.dirname(os.path.abspath(__file__))
bot_dir = os.path.dirname(script_dir)
if bot_dir not in sys.path:
    sys.path.append(bot_dir)

from image_card_generator import generate_compact_info_card

def main():
    import glob
    stories_pattern = os.path.join(bot_dir, "stories", "factcheck_*.json")
    story_files = glob.glob(stories_pattern)
    if not story_files:
        print("Error: No factcheck story files found in stories/")
        sys.exit(1)
        
    # Sort by modification time descending
    story_files.sort(key=os.path.getmtime, reverse=True)
    story_path = story_files[0]
    filename = os.path.basename(story_path)
    slug = filename[len("factcheck_"):-len(".json")]

    print(f"Loading most recent story: {story_path}")
    with open(story_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    cfg = data[0] if isinstance(data, list) else data

    output_dir = os.path.join(bot_dir, "graph_png")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{slug}_info_card.png")

    print(f"Rendering info card to: {output_path}")
    try:
        generate_compact_info_card(cfg, output_path)
        print("Success! Test image card generated successfully.")
    except Exception as e:
        print(f"FAILED to render info card: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
