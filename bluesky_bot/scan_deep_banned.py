import os
import json
import glob

live_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stories", "live")
files = glob.glob(os.path.join(live_dir, "*.json"))

banned = ["tavily.com", "wikipedia.org", "britannica.com", "dictionary.com"]

found = []
for fp in files:
    try:
        with open(fp, "r", encoding="utf-8") as f:
            text = f.read()
        for b in banned:
            if b in text:
                data = json.loads(text)
                s = data[0] if isinstance(data, list) else data
                rkeys = s.get("rkeys", [])
                found.append({
                    "file": os.path.basename(fp),
                    "id": s.get("id"),
                    "subject": s.get("subject"),
                    "matched": b,
                    "rkeys_count": len(rkeys),
                    "rkeys": rkeys
                })
                break
    except Exception as e:
        pass

print(f"TOTAL_FOUND: {len(found)}")
for item in found:
    print(f"- {item['file']} | Banned: {item['matched']} | Rkeys: {item['rkeys_count']}")

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "deep_banned_results.json"), "w", encoding="utf-8") as out:
    json.dump(found, out, indent=2)
