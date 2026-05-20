import os
import sys

# Configure stdout for utf-8
sys.stdout.reconfigure(encoding='utf-8')

audit_file = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hegemonic Audit_ Pauline Hanson tbf.md"

with open(audit_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

cleaned_count = 0
for i, line in enumerate(lines):
    if line.count("**Quote:**") > 1:
        # Split by **Quote:**
        parts = line.split("**Quote:**")
        # Keep only the header and the first quote
        new_line = parts[0] + "**Quote:**" + parts[1]
        # Make sure it ends with a newline if the original did
        if not new_line.endswith('\n'):
            new_line += '\n'
        lines[i] = new_line
        cleaned_count += 1

with open(audit_file, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"Successfully cleaned {cleaned_count} duplicated lines.")
