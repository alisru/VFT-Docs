filepath = r"C:\Users\hungh\.gemini\antigravity\brain\97fd7b60-d4b8-41d0-8f03-65e750998f03\.system_generated\steps\811\content.md"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = list(re.finditer(r'(?i)theaustralian|the\s+australian', content))
print(f"Found {len(matches)} matches")
for i, m in enumerate(matches):
    start = max(0, m.start() - 200)
    end = min(len(content), m.end() + 500)
    print(f"\n--- Match {i+1} at index {m.start()} ---")
    print(content[start:end])
