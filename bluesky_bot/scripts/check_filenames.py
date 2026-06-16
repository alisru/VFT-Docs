import glob
import os
import re

# Load current ACTOR_MAP aliases to check matches
ACTOR_ALIASES = [
    'trump', 'biden', 'xi', 'kim', 'starmer', 'putin', 'zelensky', 'taylor', 
    'burnham', 'badenoch', 'musk', 'gates', 'hegseth', 'rockliff', 'rinehart', 
    'joyce', 'abbott', 'raman', 'taillon', 'kyrgios', 'spielberg', 'daley', 
    'litherland', 'yabsley', 'walker', 'tickle', 'pratt', 'daniher', 'mihocek', 
    'lieu', 'knight', 'thomas', 'menta', 'creek', 'hobson', 'jaffer', 'bridgers', 
    'brown', 'wiberg', 'royles', 'thornton', 'tossoun', 'sara', 'newmar', 
    'lasso', 'messi', 'clark', 'stevens', 'marks', 'sullivan', 'nowak', 
    'shoebridge', 'chalmers', 'ravbar', 'one_nation', 'ice', 'ndis', 'cfmeu', 
    'wasatch', 'chicago_public_schools', 'cbs', 'nbc', 'abc', 'bbc', 'apple', 
    'google', 'microsoft', 'tesla', 'openai', 'meta', 'amazon', 'afl', 'greens', 
    'labour', 'labor', 'gop', 'republican', 'democrat', 'coalition', 'fifa', 
    'anu', 'waymo', 'nasa', 'nfl', 'high_court', 'federal_court', 
    'fair_work_commission', 'liberal', 'mcg', 'usda', 'snap', 'nhs', 'pwhl', 
    'home_office', 'white_house', 'downing_street', 'la_city_council', 
    'chicago_cubs', 'west_ham', 'knicks', 'doj', 'aukus', 'amnesty'
]

stories = glob.glob('stories/factcheck_*.json') + glob.glob('stories/live/factcheck_*.json')

unmatched_files = []

for p in stories:
    filename = os.path.basename(p).replace('factcheck_', '').replace('.json', '')
    # Check if any alias is a substring of the filename
    matched = False
    for alias in ACTOR_ALIASES:
        # Check matching as underscore separated words
        if re.search(r'\b' + re.escape(alias) + r'\b', filename) or alias in filename:
            matched = True
            break
    
    if not matched:
        unmatched_files.append(filename)

print(f"Total files: {len(stories)}")
print(f"Files with unmatched names (top 100):")
for f in unmatched_files[:100]:
    print(f)
