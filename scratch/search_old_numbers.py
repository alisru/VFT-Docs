import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

audit_file = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hegemonic Audit_ Pauline Hanson tbf.md"

with open(audit_file, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()

old_numbers = ['223', '115', '108', '31%']
print("Searching for old audit numbers:")
for idx, line in enumerate(lines):
    for num in old_numbers:
        if num in line:
            print(f"Line {idx+1} ({num}): {line.strip()}")
