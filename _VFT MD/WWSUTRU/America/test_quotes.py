import re
import os
import glob

# Test parsing quotes from base Kanon
filepaths = glob.glob('E:\\Vector Field Theory\\VFT Docs\\_VFT MD\\WWSUTRU\\America\\American_Kanon_Plane_4_*.md')
filepath = [f for f in filepaths if 'JUDGEMENT' not in f][0]

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

quotes = {}
for line in content.split('\n'):
    match = re.search(r'^\(([A-Za-z]+\.[A-Za-z]+\.[A-Za-z]+)\)\s+[^;]+;\s*(.*)$', line.strip())
    if match:
        vec_id = match.group(1)
        quote_text = match.group(2).strip()
        quotes[vec_id] = f'{quote_text}'

print(f'Found {len(quotes)} quotes in Plane 4.')
for i, k in enumerate(list(quotes.keys())):
    if i < 2:
        print(f'{k}: {quotes[k]}')
