filepath = r"C:\Users\hungh\.gemini\antigravity\brain\97fd7b60-d4b8-41d0-8f03-65e750998f03\.system_generated\steps\811\content.md"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Let's search for "Facebook" or "Followers" and print surrounding text/html
import re

matches = list(re.finditer(r'(?i)facebook|followers', content))
print(f"Found {len(matches)} matches of facebook/followers")

# Print first 5 matches with context
for i, m in enumerate(matches[:10]):
    start = max(0, m.start() - 100)
    end = min(len(content), m.end() + 200)
    print(f"\nMatch {i+1} at index {m.start()}:")
    print(content[start:end])
