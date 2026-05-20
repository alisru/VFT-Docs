import os
import re
import sys

# Configure stdout for utf-8
sys.stdout.reconfigure(encoding='utf-8')

audit_file = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hegemonic Audit_ Pauline Hanson tbf.md"

with open(audit_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

doubled = []
for i, line in enumerate(lines):
    if line.count("**Quote:**") > 1 or line.count("Quote:") > 1:
        doubled.append((i + 1, line))

print(f"Found {len(doubled)} lines with doubled quotes:")
for num, content in doubled:
    print(f"Line {num}: {content.strip()}")
