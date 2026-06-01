import json
import os
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
candidates_path = os.path.join(script_dir, 'harvested_candidates.json')

with open(candidates_path, 'r', encoding='utf-8') as f:
    candidates = json.load(f)

clean_candidates = []
seen_texts = set()

# Enhanced English & quality heuristic
for c in candidates:
    text = c["text"].strip()
    url = c["url"]
    
    # Exclude non-English and metadata domain clues
    if any(domain in url for domain in ['zeit.de', 'tijd.be', 'sapo.pt', 'demorgen.be', 'folha.com', 'nu.nl', 'gazeteoksijen.com', 'graze.social']):
        continue
    # Exclude posts with non-English chars/accents prevalent in Portuguese/German/Spanish
    if re.search(r'[ãõéáíóúçüäöß]', text, re.IGNORECASE) and not re.search(r'\b(the|and|of|to|is|in)\b', text, re.IGNORECASE):
        continue
    # Exclude short/meta items
    if len(text) < 45:
        continue
    if text in seen_texts:
        continue
        
    clean_candidates.append(c)
    seen_texts.add(text)

# If we have less than 20, we can add some known clean news stories from the batch or previous runs
# but let's see how many we have first.
print(f"Filtered clean English candidates count: {len(clean_candidates)}")
for idx, c in enumerate(clean_candidates, 1):
    print(f"[{idx}] {c['url']} -> {c['text'][:80]}...")

filtered_path = os.path.join(script_dir, 'filtered_candidates.json')
with open(filtered_path, 'w', encoding='utf-8') as f:
    json.dump(clean_candidates, f, indent=2, ensure_ascii=False)
