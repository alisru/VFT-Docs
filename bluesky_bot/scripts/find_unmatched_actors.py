import sys
sys.stdout.reconfigure(encoding='utf-8')
import glob
import json
import re
from collections import Counter

# Our current ACTOR_MAP keys (patterns)
ACTOR_PATTERNS = [
    r'\b(?<!Barron\s)(?<!Melania\s)(?<!Ivanka\s)(?:Donald\s+)?Trump\b',
    r'\bBarron\s+Trump\b',
    r'\b(?:Anthony\s+)?Albanese\b',
    r'\b(?:Joe\s+)?Biden\b',
    r'\bXi\s+Jinping\b|\bXi\b',
    r'\bKim\s+Jong\s+Un\b|\bKim\s+Jong-un\b',
    r'\b(?:Keir\s+)?Starmer\b',
    r'\b(?:Vladimir\s+)?Putin\b',
    r'\b(?:Volodymyr\s+)?Zelensky\b',
    r'\b(?:Angus\s+)?Taylor\b',
    r'\b(?:Andy\s+)?Burnham\b',
    r'\b(?:Kemi\s+)?Badenoch\b',
    r'\b(?:Elon\s+)?Musk\b',
    r'\b(?:Bill\s+)?Gates\b',
    r'\bOne\s+Nation\b',
    r'\bICE\b',
    r'\bNDIS\b',
    r'\bCFMEU\b',
    r'\bWasatch\s+Front\b',
    r'\bChicago\s+Public\s+Schools\b',
    r'\bCBS\s+News\b|\bCBS\b',
    r'\bNBC\s+News\b|\bNBC\b',
    r'\bABC\s+News\b|\bABC\b',
    r'\bBBC\b',
    r'\bApple\b',
    r'\bGoogle\b',
    r'\bMicrosoft\b',
    r'\bTesla\b',
    r'\bOpenAI\b',
    r'\bMeta\b',
    r'\bAmazon\b',
    r'\bAFL\b',
    r'\bGreens\b',
    r'\bLabour\b',
    r'\bLabor\b',
    r'\bGOP\b|\bRepublican\b|\bRepublicans\b',
    r'\bDemocrat\b|\bDemocrats\b|\bDemocratic\b',
    r'\bCoalition\b',
    r'\bIran\b',
    r'\bIsrael\b',
    r'\bNorth\s+Korea\b',
    r'\bRussia\b',
    r'\bChina\b',
    r'\bUkraine\b',
    r'\bPhilippines\b',
    r'\bCanada\b',
    r'\bAustralia\b',
    r'\bFrance\b',
    r'\bBritain\b|\bUK\b|\bBritish\b',
    r'\bUS\b|\bUSA\b|\bUnited\s+States\b|\bAmerica\b',
    r'\bTaiwan\b',
    r'\bQueensland\b',
    r'\bVictoria\b',
    r'\bTasmania\b',
    r'\bACT\b',
]

# Compile patterns
regexes = []
for p in ACTOR_PATTERNS:
    flags = re.IGNORECASE
    if 'Xi Jinping' in p or 'Xi' in p:
        # We checked Xi Jinping case-sensitively before, let's keep it case-sensitive
        flags = 0
    regexes.append(re.compile(p, flags))

stories = glob.glob('stories/factcheck_*.json') + glob.glob('stories/live/factcheck_*.json')

unmatched_words = Counter()

# Match capitalized phrases (2 or more words, or acronyms of 3+ letters)
proper_noun_pattern = re.compile(r'\b([A-Z][a-zA-Z.\'\-]+(?:\s+[A-Z][a-zA-Z.\'\-]+)+|[A-Z]{3,})\b')

# Words to ignore (months, days, etc.)
IGNORE_WORDS = {
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
    'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December', 'Today', 'Yesterday', 'Tomorrow',
    'The', 'This', 'That', 'These', 'Those', 'What', 'When', 'Where', 'Why', 'How', 'Who',
    'Here', 'There', 'Exclusive', 'Opinion', 'Editorial', 'BREAKING'
}

for p in stories:
    with open(p, 'r', encoding='utf-8') as f:
        d = json.load(f)
        cfg = d[0] if isinstance(d, list) else d
        subject = cfg.get("subject", "")
        
        # Check if matched by any pattern in ACTOR_MAP
        matched = False
        for rx in regexes:
            if rx.search(subject):
                matched = True
                break
        
        if not matched:
            # Extract proper nouns from unmatched subject
            candidates = proper_noun_pattern.findall(subject)
            for cand in candidates:
                # Filter out single ignore words or phrases starting with ignore words
                words = cand.split()
                if any(w in IGNORE_WORDS for w in words):
                    continue
                unmatched_words[cand] += 1

# Print the top 150 unmatched proper noun phrases
print("Top 150 Unmatched Proper Noun Phrases:")
for noun, count in unmatched_words.most_common(150):
    print(f"{count:<5} : {noun}")
