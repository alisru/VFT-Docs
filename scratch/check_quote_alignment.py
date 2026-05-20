import os
import re
import sys

# Configure stdout for utf-8
sys.stdout.reconfigure(encoding='utf-8')

audit_file = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hegemonic Audit_ Pauline Hanson tbf.md"

with open(audit_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Loaded {len(lines)} lines from audit file.")

# Let's find all lines that start a vector
# Pattern e.g. **(Who.Who.Who) Mateship (υ: +0.7, ψ: +0.4): FAIL.**
vector_pattern = r'\*\*\((\w+\.\w+\.\w+)\)\s+([^*:\n]+)\s+\(υ:\s*([^,]+),\s*ψ:\s*([^)]+)\):\s*(\w+)\.?\*\*'

vectors = []
for i, line in enumerate(lines):
    match = re.search(vector_pattern, line)
    if match:
        vectors.append((i, line, match.groups()))

print(f"Found {len(vectors)} vectors in the audit.")

# Check each vector block for a quote
missing_quotes = []
improper_formats = []

for idx, (line_num, line_text, groups) in enumerate(vectors):
    v_id, name, u_val, psi_val, status = groups
    
    # The block extends from line_num to the next vector line_num, or EOF
    next_line_num = vectors[idx + 1][0] if idx + 1 < len(vectors) else len(lines)
    block_lines = lines[line_num:next_line_num]
    block_text = "".join(block_lines)
    
    # Check if this block contains "Quote" or "**Quote:**"
    has_quote = False
    if "Quote:" in block_text or "**Quote:**" in block_text or "quote:" in block_text.lower():
        has_quote = True
        
    if not has_quote:
        missing_quotes.append((line_num + 1, v_id, name, status))
        
    # Check for formatting issues like:
    # 1. Brief: or Justification: on the same line or missing double stars
    # 2. Quote on same line as header but without bold stars
    if "Brief:" in block_text and not "**Brief:**" in block_text:
        improper_formats.append((line_num + 1, v_id, name, "Brief lacking stars or separate line"))
    if "Justification:" in block_text and not "**Justification:**" in block_text:
        improper_formats.append((line_num + 1, v_id, name, "Justification lacking stars or separate line"))
    if "Quote:" in block_text and not "**Quote:**" in block_text:
        improper_formats.append((line_num + 1, v_id, name, "Quote lacking bold stars"))

print(f"\nFound {len(missing_quotes)} vectors missing quotes:")
for num, v_id, name, status in missing_quotes:
    print(f"Line {num}: ({v_id}) {name.strip()} ({status})")

print(f"\nFound {len(improper_formats)} vectors with improper formatting:")
for num, v_id, name, msg in improper_formats:
    print(f"Line {num}: ({v_id}) {name.strip()} - {msg}")
