import glob, json

files = glob.glob('bluesky_bot/stories/live/*.json')

events = []
for fpath in files:
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        story = data[0] if isinstance(data, list) else data
        cu, cpsi = story.get('claim_u'), story.get('claim_psi')
        ru, rpsi = story.get('real_u'), story.get('real_psi')
        if None in (cu, cpsi, ru, rpsi): continue
        
        # High impact metric: delta >= 1.4 or macro_event present
        delta_u = ru - cu
        delta_psi = rpsi - cpsi
        total_delta = (delta_u**2 + delta_psi**2)**0.5
        
        link = story.get('link', '')
        pub = 'Other'
        if 'foxnews.com' in link: pub = 'Fox News'
        elif 'breitbart.com' in link: pub = 'Breitbart'
        elif 'nypost.com' in link: pub = 'NY Post'
        elif 'abc.net.au' in link: pub = 'ABC Australia'
        elif 'bbc.com' in link or 'bbc.co.uk' in link: pub = 'BBC'
        elif 'theguardian.com' in link: pub = 'The Guardian'
        elif 'washingtonexaminer.com' in link: pub = 'Washington Examiner'
        elif 'npr.org' in link: pub = 'NPR'
        elif 'techcrunch.com' in link: pub = 'TechCrunch'
        
        events.append({
            'subject': story.get('subject', ''),
            'pub': pub,
            'cu': cu, 'cpsi': cpsi,
            'ru': ru, 'rpsi': rpsi,
            'delta_u': delta_u,
            'delta_psi': delta_psi,
            'total_delta': total_delta,
            'rnet': story.get('real_rnet', 1.0)
        })
    except Exception:
        continue

# Sort by delta
events.sort(key=lambda x: x['total_delta'], reverse=True)
high_impact = [e for e in events if e['total_delta'] >= 1.5]

print(f"Total stories: {len(events)}, High-Impact (Delta >= 1.5): {len(high_impact)} ({len(high_impact)/len(events)*100:.1f}%)")

# Distribution of outlets in high-impact events
pub_hi = {}
for e in high_impact:
    p = e['pub']
    pub_hi[p] = pub_hi.get(p, 0) + 1

print("\nOutlet share in Extreme Divergence (Delta >= 1.5):")
for p, c in sorted(pub_hi.items(), key=lambda x: x[1], reverse=True):
    print(f"  {p:<20}: {c:>4} stories")

# Rising Hearts in High Impact
rh_hi = [e for e in high_impact if 0.2 <= e['cu'] <= 0.8 and 0.1 <= e['cpsi'] <= 0.8]
print(f"\nOf {len(high_impact)} high-impact events, {len(rh_hi)} ({len(rh_hi)/len(high_impact)*100:.1f}%) originated in the Rising Hearts zone (0.5, 0.5)!")
right_drift_hi = [e for e in rh_hi if e['ru'] < 0]
print(f"Of those Rising Hearts high-impact stories, {len(right_drift_hi)} ({len(right_drift_hi)/len(rh_hi)*100:.1f}%) collapsed directly to the right into the Exclusive (-u) quadrant!")
