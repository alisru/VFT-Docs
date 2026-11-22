import json

p = r"C:\Users\hungh\.gemini\antigravity\brain\8cad916f-b7f9-4211-80d3-12089758764a\.system_generated\logs\transcript.jsonl"
steps_of_interest = []

with open(p, "r", encoding="utf-8") as f:
    for line in f:
        if '"type":"USER_INPUT"' in line:
            obj = json.loads(line)
            step = obj.get("step_index", 0)
            txt = obj.get("content", "").strip()
            created = obj.get("created_at", "")
            # filter for formatting, contrast, visual bugs
            lower = txt.lower()
            if any(w in lower for w in [
                'black', 'white', 'text', 'contrast', 'tiles', 'details', 'content', 'icons', 'icon',
                'disjointed', 'bar', 'readable', 'fit', 'shrink', 'lag', 'laggier', 'scale', 'scaling',
                'overlap', 'header'
            ]):
                steps_of_interest.append({
                    "step": step,
                    "created": created,
                    "content": txt
                })

print(f"Total filtered steps: {len(steps_of_interest)}")
with open(r"e:\Vector Field Theory\VFT Docs\formatting_bug_prompts.json", "w", encoding="utf-8") as f:
    json.dump(steps_of_interest, f, indent=2)
