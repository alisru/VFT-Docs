import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('stories_registry.js', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = 'window.ALETHEIA_STORIES_REGISTRY = '
if text.startswith(prefix):
    text = text[len(prefix):].rstrip(';\n')

data = json.loads(text)

shorteners = set(['trib.al', 'bit.ly', 'tinyurl.com', 'nbcnews.to', 'ift.tt', 'buff.ly', 'ow.ly', 'dlvr.it'])

def get_outlet(link):
    try:
        host = link.split('/')[2].replace('www.', '').lower()
        return host
    except:
        return 'unknown'

def classify_story(s):
    ru = s.get('real_u', 0)
    cu = s.get('claim_u', 0)
    posts = s.get('posts', [])
    p1 = (posts[1] if len(posts) > 1 else '').lower()
    subj = (s.get('subject') or '').lower()
    p0 = (posts[0] if len(posts) > 0 else '').lower()

    # 1. Explicit author sub-audit check
    for p in posts[3:6]:
        if 'PASS' in p or 'FAIL' in p:
            for l in p.split('\n'):
                l_lower = l.lower()
                if any(w in l_lower for w in ['reporting', 'coverage', 'journalism', 'investigation', 'editorial', 'article', 'framing']):
                    if 'PASS' in l.upper(): return 'EXPOSE' if ru < 0 else 'CONSTRUCTIVE'
                    if 'FAIL' in l.upper(): return 'WHITEWASH' if ru < 0 else 'SMEAR'

    # 2. Check if the event is BAD (ru < -0.15)
    if ru < -0.15:
        harm_cues = ['abuse', 'scandal', 'fail', 'fraud', 'corrupt', 'kill', 'death', 'crisis', 'dead', 
                     'collapse', 'lie', 'deceit', 'suppress', 'steal', 'toxic', 'poison', 'crime', 
                     'assault', 'violence', 'bribe', 'slashed', 'lawsuit', 'sue', 'hazard', 'peril', 
                     'harm', 'investigat', 'murder', 'disaster', 'shot', 'plead', 'guilty', 'arrest',
                     'indict', 'charges', 'delay', 'shortage', 'struggle', 'threat', 'warning', 'breach',
                     'dead end', 'fell apart', 'illegal', 'probe', 'allegation', 'cut', 'slams', 'flee',
                     'chaos', 'suffered', 'tragedy', 'slain', 'broken', 'injur', 'controversy', 'fault']
        is_reporting_harm = any(w in subj or w in p0 for w in harm_cues)
        
        target_claim_cues = ['official', 'company', 'contractor', 'executive', 'police', 'spokesman', 'spokesperson',
                             'agency', 'department', 'trump', 'biden', 'administration', 'authorities', 'firm',
                             'hospital', 'leadership', 'board', 'spokeswoman', 'claims that', 'claimed that', 
                             'asserts that', 'insists that', 'argues that', 'contends that', 'denied that']
        is_exposing_target = any(w in p1 for w in target_claim_cues)
        claim_matches_reality = (cu < 0)
        
        if is_reporting_harm or is_exposing_target or claim_matches_reality:
            return 'EXPOSE'
        else:
            return 'WHITEWASH'

    elif ru > 0.15:
        if cu < -0.2:
            return 'SMEAR'
        else:
            return 'CONSTRUCTIVE'
    else:
        if abs(cu - ru) <= 0.75:
            return 'CONSTRUCTIVE'
        else:
            return 'WHITEWASH' if cu > ru else 'SMEAR'

outlets = ['propublica.org', 'thefederalist.com', 'breitbart.com', 'abc.net.au', 'nytimes.com', 'npr.org', 'foxnews.com', 'motherjones.com', 'rawstory.com', 'dailymail.com']

header = f"{'OUTLET':<20} | {'n':<5} | {'PASS%':<6} | {'EXPOSE':<6} | {'CONSTR':<6} | {'WHITEW':<6} | {'SMEAR':<5}"
print(header)
print('-'*len(header))

for out in outlets:
    stories = [s for s in data if get_outlet(s.get('link', '')) == out]
    counts = {'EXPOSE': 0, 'CONSTRUCTIVE': 0, 'WHITEWASH': 0, 'SMEAR': 0}
    for s in stories:
        cat = classify_story(s)
        counts[cat] += 1
    total = len(stories)
    passes = counts['EXPOSE'] + counts['CONSTRUCTIVE']
    rate = (passes / total * 100) if total > 0 else 0
    exp = counts['EXPOSE']
    con = counts['CONSTRUCTIVE']
    whi = counts['WHITEWASH']
    sme = counts['SMEAR']
    print(f"{out:<20} | {total:<5} | {rate:<5.1f}% | {exp:^6} | {con:^6} | {whi:^6} | {sme:^5}")
