import glob, json, os

files = glob.glob('bluesky_bot/stories/live/*.json')
outlets_stats = {}

for fpath in files:
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list) and len(data) > 0:
            story = data[0]
        elif isinstance(data, dict):
            story = data
        else:
            continue
        
        cu = story.get('claim_u')
        cpsi = story.get('claim_psi')
        ru = story.get('real_u')
        rpsi = story.get('real_psi')
        if cu is None or ru is None or cpsi is None or rpsi is None:
            continue
        
        # Determine publisher/outlet
        sources = story.get('cluster_sources', [])
        pub = ''
        if sources and isinstance(sources, list) and isinstance(sources[0], dict):
            pub = sources[0].get('publisher', '').strip()
        if not pub:
            link = story.get('link', '')
            if 'foxnews.com' in link: pub = 'Fox News'
            elif 'breitbart.com' in link: pub = 'Breitbart'
            elif 'nypost.com' in link: pub = 'NY Post'
            elif 'abc.net.au' in link: pub = 'ABC Australia'
            elif 'bbc.com' in link or 'bbc.co.uk' in link: pub = 'BBC'
            elif 'theguardian.com' in link: pub = 'The Guardian'
            elif 'washingtonexaminer.com' in link: pub = 'Washington Examiner'
            elif 'nytimes.com' in link: pub = 'NY Times'
            elif 'reuters.com' in link: pub = 'Reuters'
            elif 'apnews.com' in link: pub = 'AP News'
            elif 'aljazeera.com' in link: pub = 'Al Jazeera'
            elif 'dailywire.com' in link: pub = 'Daily Wire'
            elif 'techcrunch.com' in link: pub = 'TechCrunch'
            elif 'npr.org' in link: pub = 'NPR'
            elif 'bloomberg.com' in link: pub = 'Bloomberg'
            elif 'theage.com.au' in link or 'smh.com.au' in link: pub = 'SMH/Age'
            else: pub = 'Other'
        
        if pub not in outlets_stats:
            outlets_stats[pub] = {
                'count': 0, 'cu': 0, 'cpsi': 0, 'ru': 0, 'rpsi': 0,
                'drift_right': 0, 'high_impact': 0, 'rising_heart_density': 0,
                'greatest_lie_density': 0
            }
        
        s = outlets_stats[pub]
        s['count'] += 1
        s['cu'] += cu
        s['cpsi'] += cpsi
        s['ru'] += ru
        s['rpsi'] += rpsi
        # Drift right = ru < cu (moving towards exclusive -u)
        if ru < cu:
            s['drift_right'] += 1
        # High impact = macro_event exists or abs(claim - real) is large (> 1.2)
        if abs(cu - ru) + abs(cpsi - rpsi) >= 1.2:
            s['high_impact'] += 1
        # Rising Hearts initial zone: claim around (0.5, 0.5)
        if 0.2 <= cu <= 0.8 and 0.1 <= cpsi <= 0.8:
            s['rising_heart_density'] += 1
        # Greatest Lie actual landing zone: real_u < 0 and real_psi > 0 (-1, +1 quadrant)
        if ru < 0 and rpsi > 0:
            s['greatest_lie_density'] += 1
    except Exception:
        continue

sorted_outlets = sorted([k for k, v in outlets_stats.items() if v['count'] >= 100], key=lambda k: outlets_stats[k]['count'], reverse=True)

print(f"{'Outlet':<20} | {'Count':<5} | {'Claim (u, psi)':<16} | {'Real (u, psi)':<16} | {'Right-Drift':<11} | {'Hi-Delta':<8} | {'RisingHearts':<12} | {'GreatestLie'}")
print('-'*115)
for k in sorted_outlets:
    st = outlets_stats[k]
    n = st['count']
    m_cu = st['cu'] / n
    m_cpsi = st['cpsi'] / n
    m_ru = st['ru'] / n
    m_rpsi = st['rpsi'] / n
    r_pct = (st['drift_right'] / n) * 100
    hi_pct = (st['high_impact'] / n) * 100
    rh_pct = (st['rising_heart_density'] / n) * 100
    gl_pct = (st['greatest_lie_density'] / n) * 100
    print(f"{k:<20} | {n:<5} | ({m_cu:+.2f}, {m_cpsi:+.2f})     | ({m_ru:+.2f}, {m_rpsi:+.2f})     | {r_pct:>6.1f}%     | {hi_pct:>6.1f}%   | {rh_pct:>6.1f}%       | {gl_pct:>6.1f}%")
