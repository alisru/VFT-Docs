import sys
import os
import json

sys.path.insert(0, r"E:\Vector Field Theory\VFT Docs\bluesky_bot")
from aletheia_bot import pack_posts

fail_dir = r"E:\Vector Field Theory\VFT Docs\bluesky_bot\stories\fail"

for fname in os.listdir(fail_dir):
    if not fname.endswith(".json"):
        continue
    fpath = os.path.join(fail_dir, fname)
    print("=" * 60)
    print(f"CHECKING: {fname}")
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        cfg = data[0] if isinstance(data, list) else data
        posts = cfg.get("posts", [])
        
        # Check Spirithekanon
        is_spiritual = cfg.get("spiritual") is True or any(
            isinstance(p, str) and p.strip().startswith("Spirithekanon:") for p in posts
        )
        if is_spiritual:
            sp = next((p for p in posts if isinstance(p, str) and p.strip().startswith("Spirithekanon:")), None)
            if not sp:
                print("  [ERROR] is_spiritual but no post starts with Spirithekanon:")
            else:
                import re
                text_to_check = sp.replace("Spirithekanon:", "").strip()
                match = re.search(r'"([^"]+)"', text_to_check)
                if not match:
                    print(f"  [ERROR] Spirithekanon quote regex failed! Text:\n{sp}")
                    
        # Check packed posts
        packed = pack_posts(posts)
        for i, p in enumerate(packed, 1):
            if len(p) > 300:
                print(f"  [ERROR] Packed post {i} > 300 chars ({len(p)}): {p[:60]}...")
                
        # Check mode and target_url
        mode = cfg.get("mode", "").lower()
        target_url = cfg.get("target_url", "")
        if mode == "reply" and not target_url:
            print("  [ERROR] mode == reply but no target_url")
            
        # Check image cards / graphs
        story_id = cfg.get("id", "")
        for char in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']:
            story_id = story_id.replace(char, '')
        graph_dir = r"E:\Vector Field Theory\VFT Docs\bluesky_bot\graph_png"
        v_card = os.path.join(graph_dir, f"{story_id}_info_card_verdict.png")
        a_card = os.path.join(graph_dir, f"{story_id}_info_card_analysis.png")
        print(f"  Verdict card exists: {os.path.exists(v_card)}")
        print(f"  Analysis card exists: {os.path.exists(a_card)}")
        
    except Exception as e:
        print(f"  [EXCEPTION]: {e}")
