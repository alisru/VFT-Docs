import os
import json

bot_dir = os.path.dirname(os.path.abspath(__file__))
RIGHT_WING_DOMAINS = [
    'foxnews.com', 'nypost.com', 'breitbart.com', 'washingtonexaminer.com',
    'dailywire.com', 'freebeacon.com', 'thefederalist.com', 'theblaze.com',
    'newsmax.com', 'oann.com', 'dailycaller.com', 'westernjournal.com'
]

def is_rw(url):
    u = (url or '').lower()
    return any(d in u for d in RIGHT_WING_DOMAINS)

def get_domain(url):
    u = (url or '').lower()
    for d in RIGHT_WING_DOMAINS:
        if d in u:
            return d
    return 'other'

def main():
    # 1. Scan Queue (stories/ excluding live/ and darkroom/)
    queue_dir = os.path.join(bot_dir, 'stories')
    queue_files = [f for f in os.listdir(queue_dir) if f.startswith('factcheck_') and f.endswith('.json')]

    queue_rw = []
    for f in queue_files:
        try:
            with open(os.path.join(queue_dir, f), 'r', encoding='utf-8') as fp:
                d = json.load(fp)[0]
                url = d.get('link') or d.get('url') or ''
                if is_rw(url):
                    queue_rw.append({
                        'file': f,
                        'domain': get_domain(url),
                        'subject': d.get('subject', ''),
                        'claim_u': d.get('claim_u'),
                        'claim_psi': d.get('claim_psi'),
                        'real_u': d.get('real_u'),
                        'real_psi': d.get('real_psi'),
                        'rnet': d.get('real_rnet'),
                        'url': url
                    })
        except Exception:
            pass

    print('=== PRIORITY 1: THE QUEUE (STAGED STORIES) ===')
    print(f'Total staged stories: {len(queue_files)}')
    print(f'Right-Wing / Fox News staged stories: {len(queue_rw)}\n')
    for idx, s in enumerate(queue_rw, 1):
        print(f"{idx}. [{s['domain']}] {s['subject']}")
        print(f"   Coords: Stated ({s['claim_u']}, {s['claim_psi']}) -> Actual ({s['real_u']}, {s['real_psi']}) | R_net: {s['rnet']}")
        print(f"   File: {s['file']}")
        print(f"   URL:  {s['url']}\n")

    # 2. Scan Live (stories/live/)
    live_dir = os.path.join(bot_dir, 'stories', 'live')
    live_files = [f for f in os.listdir(live_dir) if f.startswith('factcheck_') and f.endswith('.json')]

    live_rw = []
    for f in live_files:
        try:
            with open(os.path.join(live_dir, f), 'r', encoding='utf-8') as fp:
                d = json.load(fp)[0]
                url = d.get('link') or d.get('url') or ''
                if is_rw(url):
                    live_rw.append({
                        'file': f,
                        'domain': get_domain(url),
                        'subject': d.get('subject', ''),
                        'claim_u': d.get('claim_u'),
                        'claim_psi': d.get('claim_psi'),
                        'real_u': d.get('real_u'),
                        'real_psi': d.get('real_psi'),
                        'rnet': d.get('real_rnet'),
                        'rkeys': d.get('rkeys', []),
                        'post_urls': d.get('post_urls', []),
                        'url': url
                    })
        except Exception:
            pass

    print('\n=== PRIORITY 2: LIVE POSTS AUDIT ===')
    print(f'Total live stories: {len(live_files)}')
    print(f'Right-Wing / Fox News live stories: {len(live_rw)}')
    by_dom = {}
    for s in live_rw:
        by_dom[s['domain']] = by_dom.get(s['domain'], 0) + 1
    for d, count in sorted(by_dom.items(), key=lambda x: -x[1]):
        print(f'  - {d}: {count} stories')

if __name__ == '__main__':
    main()
