import sys
sys.stdout.reconfigure(encoding='utf-8')
import glob
import json
import re
from collections import Counter

# Read all stories
stories = glob.glob('stories/factcheck_*.json') + glob.glob('stories/live/factcheck_*.json')

proper_noun_counter = Counter()

# Regex to capture sequences of title-cased words (2 or more words, or 1 word if it's completely uppercase like GOP, CFMEU)
# Also capture single capitalized words that might be names
pattern = re.compile(r'\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)\b')

for p in stories:
    with open(p, 'r', encoding='utf-8') as f:
        d = json.load(f)
        cfg = d[0] if isinstance(d, list) else d
        subject = cfg.get("subject", "")
        # Find all proper noun phrases
        matches = pattern.findall(subject)
        for m in matches:
            proper_noun_counter[m] += 1

# Print the top 300 most frequent proper noun phrases
print("Top 300 Proper Noun Phrases:")
for noun, count in proper_noun_counter.most_common(300):
    print(f"{count:<5} : {noun}")
