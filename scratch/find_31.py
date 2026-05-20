import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

audit_file = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hegemonic Audit_ Pauline Hanson tbf.md"

with open(audit_file, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
found = False

print("Searching for '31' in the audit file:")
for idx, line in enumerate(lines):
    if '31' in line:
        print(f"Line {idx+1}: {line.strip()}")
        found = True

if not found:
    print("No occurrences of '31' found.")
