import glob
import json

files = sorted(glob.glob('bluesky_bot/stories/factcheck_*.json'))
print(f'Checking verification sources across {len(files)} stories:\n')

for p in files:
    fname = p.replace('\\', '/').split('/')[-1]
    data = json.load(open(p, encoding='utf-8'))
    item = data[0] if isinstance(data, list) and len(data) > 0 else data
    link = item.get('link', '')
    g_url = item.get('grounding_url') or 'NONE'
    clusters = item.get('cluster_sources') or []
    aspects = item.get('aspects') or []
    dossier = item.get('cross_source_dossier') or ''
    
    print(f'=== {fname} ===')
    print(f'  Target/Claim Link: {link}')
    print(f'  Grounding URL:     {g_url}')
    if clusters:
        print(f'  Cluster Sources ({len(clusters)}):')
        for c in clusters:
            b = c.get('bias', 'Unknown')
            o = c.get('outlet', '')
            u = c.get('url', '')
            print(f'    - [{b}] {o} -> {u}')
    else:
        print('  Cluster Sources: NONE (Single Source)')
    if aspects:
        print(f'  Aspects ({len(aspects)}):')
        for a in aspects:
            name = a.get('name', '')
            v = a.get('verdict', '')
            print(f'    - [{name}] Verdict: {v}')
    if dossier:
        print(f'  Has Dossier: Yes ({len(dossier)} chars)')
    print()
