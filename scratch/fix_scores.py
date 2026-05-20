import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

audit_file = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hegemonic Audit_ Pauline Hanson tbf.md"

with open(audit_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's define the exact replacements for the bottom scorecard to ensure perfect alignment with 224 Hits and 125 Fails (28.4% score)
replacements = {
    "**Hits (Alignments):** \t223": "**Hits (Alignments):** \t224",
    "**Hits (Alignments):** 	223": "**Hits (Alignments):** 	224",
    "**Fails (Violations):** \t115": "**Fails (Violations):** \t125",
    "**Fails (Violations):** 	115": "**Fails (Violations):** 	125",
    "**Percentage Australian Alignment:** 51%": "**Percentage Australian Alignment:** 51.0%"
}

replaced = 0
for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        print(f"Replaced:\n{old}\nWITH:\n{new}\n")
        replaced += 1
    else:
        print(f"Not found: {old}")

with open(audit_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Done. Replaced {replaced} lines.")
