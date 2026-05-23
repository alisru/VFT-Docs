import os
import sys

# Configure stdout for utf-8
sys.stdout.reconfigure(encoding='utf-8')

audit_file = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hegemonic Audit_ Pauline Hanson tbf.md"

with open(audit_file, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    # 1. Page-level mentions of overall score
    "just under one-third (31.0%) of the nation's": 
    "just under one-third (28.4%) of the nation's",
    
    "just under one-third (**31.0%**) of the nation's": 
    "just under one-third (**28.4%**) of the nation's",
    
    "**Final Alignment Score:** **31.0%** (+108 Net Score out of 349 core vectors)": 
    "**Final Alignment Score:** **28.4%** (+99 Net Score out of 349 core vectors)",
    
    "She is exactly **31% Australian**: the 31% that is terrified of the outside world.": 
    "She is exactly **28.4% Australian**: the 28.4% that is terrified of the outside world.",
    
    # 2. Plane-level Percentage Australian Alignment headers
    " **Percentage Australian Alignment:** 40.4%  ": 
    " **Percentage Australian Alignment:** 34.6%  ",
    
    "**Percentage Australian Alignment:** 16.3%": 
    "**Percentage Australian Alignment:** 14.3%",
    
    "**Percentage Australian Alignment:** 55.1%": 
    "**Percentage Australian Alignment:** 10.2%",
    
    # 3. Totality plane summaries at the bottom of the document
    "**Plane 1: Identity (Who) — 22.0% Aligned**": 
    "**Plane 1: Identity (Who) — 20.0% Aligned**",
    
    "**Plane 3: The Land (Where) — 59.2% Aligned**": 
    "**Plane 3: The Land (Where) — 51.0% Aligned**",
    
    "**Plane 4: The Drive (Why) — 40.4% Aligned**": 
    "**Plane 4: The Drive (Why) — 34.6% Aligned**",
    
    "**Plane 5: Method (How) — 16.3% Aligned**": 
    "**Plane 5: Method (How) — 14.3% Aligned**",
}

replaced_count = 0
for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        replaced_count += 1
    else:
        # Check variations (e.g. carriage returns or spaces)
        old_clean = old.strip()
        new_clean = new.strip()
        if old_clean in content:
            content = content.replace(old_clean, new_clean)
            replaced_count += 1

with open(audit_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully corrected {replaced_count} of {len(replacements)} score mentions in the document.")
