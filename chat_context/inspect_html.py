import re
import sys
from pathlib import Path

html_path = Path("html base/Failed Markdown Canvas Generation - Google Gemini.html")
if not html_path.exists():
    print("File not found:", html_path)
    sys.exit(1)

content = html_path.read_text(encoding="utf-8", errors="ignore")
print(f"Loaded HTML, length: {len(content)} characters")

# Find conversation / message containers
message_tags = set(re.findall(r'<([a-zA-Z0-9\-_]+)[^>]*?message[^>]*?>', content, re.IGNORECASE))
print("Message-related tags:", message_tags)

# Find all custom elements (tags with a hyphen)
custom_tags = set(re.findall(r'<([a-z0-9]+-[a-z0-9\-]+)', content, re.IGNORECASE))
print("\nCustom HTML elements with hyphens:")
for t in sorted(custom_tags):
    if any(k in t.lower() for k in ['canvas', 'artifact', 'panel', 'editor', 'card', 'item', 'response', 'content', 'immersive', 'code']):
        print(f"  <{t}>")

sys.stdout.reconfigure(encoding='utf-8')

# Search for immersive-entry-chip and immersive-editor
print("\n--- IMMERSIVE-ENTRY-CHIP STRUCTURE ---")
chip_match = re.search(r'<immersive-entry-chip[\s\S]*?</immersive-entry-chip>', content, re.IGNORECASE)
if chip_match:
    chip = chip_match.group(0)
    print("Full length:", len(chip))
    # Replace long text content but keep tag hierarchy
    tags = re.findall(r'<([a-zA-Z0-9\-_]+)[^>]*?>', chip)
    print("Tag hierarchy:", tags[:50])
    
    # Check for preview content or text containers
    preview_match = re.search(r'<div[^>]*?class="[^"]*?content[^"]*?"[\s\S]*?</div>', chip)
    if preview_match:
        print("Content div preview:", preview_match.group(0)[:800])
    else:
        print("No content div matched, printing raw text of chip:")
        clean_text = re.sub(r'<[^>]+>', ' ', chip)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        print("Chip clean text:", clean_text[:1000])

print("\n--- SIMULATED JS EXTRACTOR ---")
# Selectors:
# 'immersive-entry-chip, immersive-editor, immersive-panel, [data-test-id*="immersive"], [data-test-id*="canvas"], .immersive-container, .canvas-container, [aria-label*="Canvas" i], aside[class*="immersive"]'

containers = []
# Find immersive-entry-chip
for m in re.finditer(r'<immersive-entry-chip[\s\S]*?</immersive-entry-chip>', content, re.IGNORECASE):
    containers.append(('immersive-entry-chip', m.group(0)))

# Find immersive-editor not inside chip
for m in re.finditer(r'<immersive-editor[\s\S]*?</immersive-editor>', content, re.IGNORECASE):
    # check if already inside a chip
    if not any(m.group(0) in c[1] for c in containers):
        containers.append(('immersive-editor', m.group(0)))

print(f"Total canvas containers identified: {len(containers)}")

for tag, panel in containers:
    # 1. Title extraction
    title = ''
    t_match = re.search(r'class="[^"]*?title[^"]*?"[^>]*?>([^<]+)</div>', panel)
    if t_match:
        title = t_match.group(1).strip()
    if not title:
        h_match = re.search(r'<h[1-3][^>]*?>([^<]+)</h[1-3]>', panel)
        if h_match:
            title = h_match.group(1).strip()
    if not title:
        title = "Untitled Canvas"
        
    print(f"Extracted Canvas Title: '{title}'")
    
    # 2. Content extraction
    # Check for ProseMirror
    pm = re.search(r'class="[^"]*?ProseMirror[^"]*?"[^>]*?>([\s\S]*?)</div>\s*</div>', panel)
    if pm:
        raw_html = pm.group(1)
        print(f"  Found ProseMirror content! (Length: {len(raw_html)})")
        # Check headings and lists in raw_html
        headings = re.findall(r'<h[1-6][^>]*?>([^<]+)</h[1-6]>', raw_html)
        print(f"  Headings: {headings}")




