import json

p = r"C:\Users\hungh\.gemini\antigravity\brain\8cad916f-b7f9-4211-80d3-12089758764a\.system_generated\logs\transcript.jsonl"

recent_inputs = []
with open(p, "r", encoding="utf-8") as f:
    for line in f:
        if '"type":"USER_INPUT"' in line:
            obj = json.loads(line)
            step = obj.get("step_index", 0)
            if step >= 8500:
                recent_inputs.append({
                    "step": step,
                    "created": obj.get("created_at", ""),
                    "content": obj.get("content", "").strip()
                })

with open(r"e:\Vector Field Theory\VFT Docs\extracted_steps_8500_plus.json", "w", encoding="utf-8") as f:
    json.dump(recent_inputs, f, indent=2)

print(f"Total steps >= 8500: {len(recent_inputs)}")
for item in recent_inputs:
    print(f"STEP {item['step']} ({item['created']})")
    print(item['content'])
    print("=" * 60)
