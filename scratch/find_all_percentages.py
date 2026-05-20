import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

audit_file = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hegemonic Audit_ Pauline Hanson tbf.md"

with open(audit_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find all occurrences of % or percentage-like patterns
# and print their line number and some surrounding context.
lines = content.splitlines()
found = False

print("Searching for percentages in the audit file:")
for idx, line in enumerate(lines):
    # Find anything with % or "percent" or "score" or similar
    if '%' in line or 'percent' in line.lower() or 'alignment' in line.lower() or 'aligned' in line.lower() or 'score' in line.lower():
        # But let's filter out standard headers unless they have numbers/percentages to keep output readable
        has_num = any(char.isdigit() for char in line)
        if has_num or '%' in line:
            print(f"Line {idx+1}: {line.strip()}")
            found = True

if not found:
    print("No percentages or score-like patterns found.")
