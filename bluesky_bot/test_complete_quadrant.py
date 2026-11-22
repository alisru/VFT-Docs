import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('stories_registry.js', 'r', encoding='utf-8') as f:
    text = f.read()[len('window.ALETHEIA_STORIES_REGISTRY = '):].rstrip(';\n')

data = json.loads(text)

shorteners = set(['trib.al', 'bit.ly', 'tinyurl.com', 'nbcnews.to', 'ift.tt', 'buff.ly', 'ow.ly', 'dlvr.it'])

commentary_cues = [
    'the article', 'the piece', 'the essay', 'the commentary', 'partisan commentary', 
    'the op-ed', 'this piece', 'the headline', 'partisan media', 'media framing',
    'media weaponized', 'punditry', 'culture war', 'weaponizing', 'romanticizing', 
    'cherry-pick', 'fearmonger', 'manufacture outrage', 'manufacture existential', 
    'manufacture an election crisis', 'sensationalist', 'stoking panic', 'stoke outrage',
    'pundits', 'talking heads', 'partisan narrative'
]

def get_outlet(link):
    try:
        host = link.split('/')[2].replace('www.', '').lower()
        if host in shorteners:
            return None
        return host
    except:
        return None

def audit_story_reporting(s):
    ru = s.get('real_u', 0)
    cu = s.get('claim_u', 0)
    posts = s.get('posts', [])
    p3 = (posts[3] if len(posts) > 3 else '').lower()
    
    # 1. Check if the audit explicitly faulted the article/commentary/media framing
    is_media_faulted = any(c in p3 for c in commentary_cues)
    
    # Check explicit sub-audits if present
    for p in posts[3:6]:
        if 'PASS' in p or 'FAIL' in p:
            for l in p.split('\n'):
                l_lower = l.lower()
                if any(w in l_lower for w in ['reporting', 'coverage', 'journalism', 'investigation', 'editorial', 'article', 'framing']):
                    if 'PASS' in l.upper():
                        return ('PASS', 'EXPOSE' if ru < 0 else 'CONSTRUCTIVE')
                    if 'FAIL' in l.upper():
                        return ('FAIL', 'WHITEWASH' if ru < 0 else 'SMEAR')

    # 2. Quadrant evaluation
    if ru < -0.15: # Bad Event
        if is_media_faulted:
            # Bad event presented with deceptive/weaponized framing (Whitewash/Spin)
            return ('FAIL', 'WHITEWASH')
        else:
            # Bad event exposed truthfully (Expose)
            return ('PASS', 'EXPOSE')
            
    elif ru > 0.15: # Good Event
        if is_media_faulted or cu < -0.2:
            # Good event attacked or smeared (Smear)
            return ('FAIL', 'SMEAR')
        else:
            # Good event reported truthfully (Constructive)
            return ('PASS', 'CONSTRUCTIVE')
            
    else: # Neutral Event
        if is_media_faulted or abs(cu - ru) > 0.8:
            return ('FAIL', 'DISTORTION')
        else:
            return ('PASS', 'NEUTRAL')

outlets = [
    'propublica.org', 'thefederalist.com', 'breitbart.com', 'abc.net.au', 
    'nytimes.com', 'npr.org', 'foxnews.com', 'motherjones.com', 
    'rawstory.com', 'dailymail.com', 'theguardian.com', 'bbc.com'
]

header = f"{'OUTLET':<20} | {'TOTAL':<5} | {'PASS%':<6} | {'EXPOSE':<6} | {'CONSTR':<6} | {'WHITEW':<6} | {'SMEAR':<5}"
print(header)
print('-'*len(header))

for out in outlets:
    stories = [s for s in data if get_outlet(s.get('link', '')) == out]
    if not stories: continue
    counts = {'EXPOSE': 0, 'CONSTRUCTIVE': 0, 'WHITEWASH': 0, 'SMEAR': 0, 'NEUTRAL': 0, 'DISTORTION': 0}
    passes = 0
    fails = 0
    for s in stories:
        verdict, tag = audit_story_reporting(s)
        if verdict == 'PASS': passes += 1
        else: fails += 1
        if tag in counts: counts[tag] += 1
    total = len(stories)
    rate = (passes / total * 100) if total > 0 else 0
    exp = counts['EXPOSE']
    con = counts['CONSTRUCTIVE'] + counts['NEUTRAL']
    whi = counts['WHITEWASH'] + counts['DISTORTION']
    sme = counts['SMEAR']
    print(f"{out:<20} | {total:<5} | {rate:<5.1f}% | {exp:^6} | {con:^6} | {whi:^6} | {sme:^5}")
