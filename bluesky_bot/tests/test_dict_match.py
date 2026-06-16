import sys
sys.stdout.reconfigure(encoding='utf-8')
import glob
import json
import re

# Define canonical actor mapping (alias -> canonical name)
ACTOR_MAP = {
    # Individuals
    r'\b(?<!Barron\s)(?<!Melania\s)(?<!Ivanka\s)(?:Donald\s+)?Trump\b': "Donald Trump",
    r'\bBarron\s+Trump\b': "Barron Trump",
    r'\b(?:Anthony\s+)?Albanese\b': "Anthony Albanese",
    r'\b(?:Joe\s+)?Biden\b': "Joe Biden",
    r'\bXi\s+Jinping\b|\bXi\b': "Xi Jinping",  # we will handle Xi case-sensitively in the loop
    r'\bKim\s+Jong\s+Un\b|\bKim\s+Jong-un\b': "Kim Jong Un",
    r'\b(?:Keir\s+)?Starmer\b': "Keir Starmer",
    r'\b(?:Vladimir\s+)?Putin\b': "Vladimir Putin",
    r'\b(?:Volodymyr\s+)?Zelensky\b': "Volodymyr Zelensky",
    r'\b(?:Angus\s+)?Taylor\b': "Angus Taylor",
    r'\b(?:Andy\s+)?Burnham\b': "Andy Burnham",
    r'\b(?:Kemi\s+)?Badenoch\b': "Kemi Badenoch",
    r'\b(?:KPMG)\b': "KPMG",
    r'\b(?:Kylie)\b': "Kyle",
    r'\b(?:Bob\s+)?Brown\b': "Bob Brown",
    r'\b(?:Lionel\s+)?Messi\b': "Lionel Messi",
    r'\b(?:Caitlin\s+)?Clark\b': "Caitlin Clark",
    r'\b(?:Melissa\s+)?Menta\b': "Melissa Menta",
    r'\b(?:Martin\s+)?Wiberg\b': "Martin Wiberg",
    r'\b(?:Michael\s+)?Ravbar\b': "Michael Ravbar",
    r'\b(?:Charlie\s+)?Crist\b': "Charlie Crist",
    r'\b(?:Bill\s+)?Gates\b': "Bill Gates",
    
    # Orgs & Parties
    r'\bOne\s+Nation\b': "One Nation",
    r'\bICE\b': "ICE",
    r'\bNDIS\b': "NDIS",
    r'\bCFMEU\b': "CFMEU",
    r'\bWasatch\s+Front\b': "Wasatch Front",
    r'\bChicago\s+Public\s+Schools\b': "Chicago Public Schools",
    r'\bCBS\s+News\b|\bCBS\b': "CBS News",
    r'\bNBC\s+News\b|\bNBC\b': "NBC News",
    r'\bABC\s+News\b|\bABC\b': "ABC News",
    r'\bBBC\b': "BBC",
    r'\bApple\b': "Apple",
    r'\bGoogle\b': "Google",
    r'\bMicrosoft\b': "Microsoft",
    r'\bTesla\b': "Tesla",
    r'\bOpenAI\b': "OpenAI",
    r'\bMeta\b': "Meta",
    r'\bAmazon\b': "Amazon",
    r'\bAFL\b': "AFL",
    r'\bGreens\b': "Greens",
    r'\bLabour\b': "Labour (UK)",
    r'\bLabor\b': "Labor (AU)",
    r'\bGOP\b|\bRepublican\b|\bRepublicans\b': "GOP",
    r'\bDemocrat\b|\bDemocrats\b|\bDemocratic\b': "Democrats",
    
    # Geopolitical entities (major countries/states/cities in corpus)
    r'\bIran\b': "Iran",
    r'\bIsrael\b': "Israel",
    r'\bNorth\s+Korea\b': "North Korea",
    r'\bRussia\b': "Russia",
    r'\bChina\b': "China",
    r'\bUkraine\b': "Ukraine",
    r'\bPhilippines\b': "Philippines",
    r'\bCanada\b': "Canada",
    r'\bAustralia\b': "Australia",
    r'\bFrance\b': "France",
    r'\bBritain\b|\bUK\b|\bBritish\b': "United Kingdom",
    r'\bUS\b|\bUSA\b|\bUnited\s+States\b|\bAmerica\b': "United States",
    r'\bTaiwan\b': "Taiwan",
    r'\bQueensland\b': "Queensland",
    r'\bVictoria\b': "Victoria",
    r'\bTasmania\b': "Tasmania",
    r'\bACT\b': "ACT",
}

stories = glob.glob('stories/factcheck_*.json') + glob.glob('stories/live/factcheck_*.json')

results = []
for p in stories:
    with open(p, 'r', encoding='utf-8') as f:
        d = json.load(f)
        cfg = d[0] if isinstance(d, list) else d
        subject = cfg.get("subject", "")
        
        matched_actors = []
        for pattern, canonical in ACTOR_MAP.items():
            flags = 0 if canonical == "Xi Jinping" else re.IGNORECASE
            if re.search(pattern, subject, flags):
                if canonical not in matched_actors:
                    matched_actors.append(canonical)
        
        results.append((subject, matched_actors))

# Print first 200 matches
for sub, acts in results[:200]:
    if acts:  # Only show those with matched actors to see how clean they are
        print(f"SUBJ: {sub}")
        print(f"ACTS: {acts}")
        print("-" * 50)
