filepath = r"C:\Users\hungh\.gemini\antigravity\brain\97fd7b60-d4b8-41d0-8f03-65e750998f03\.system_generated\steps\811\content.md"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = list(re.finditer(r'townsvillebulletin\.com\.au|abc\.net\.au', content))
print(f"Found {len(matches)} matches")
for i, m in enumerate(matches[:3]):
    idx = m.start()
    print(f"\n--- Match {i+1} at index {idx} ---")
    print(content[idx-500:idx+1500])
