import urllib.request, re, json, os
from html import unescape

def extract_full_clean_article(html):
    # Remove script, style, head, nav, footer, header, svg, noscript
    html = re.sub(r'<(script|style|head|nav|footer|header|svg|noscript|form|aside)[^>]*>.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
    # Convert block elements to newlines
    html = re.sub(r'<(p|br|div|h[1-6]|li|article|section)[^>]*>', '\n', html, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', html)
    text = unescape(text)
    # Keep substantive lines
    lines = [line.strip() for line in text.splitlines() if len(line.strip()) > 25]
    # Filter out common UI boilerplate lines
    clean_lines = []
    for l in lines:
        l_lower = l.lower()
        if any(skip in l_lower for skip in ['skip to navigation', 'cookie policy', 'privacy policy', 'terms of service', 'sign up for our newsletter', 'all rights reserved']):
            continue
        clean_lines.append(l)
    return '\n\n'.join(clean_lines)

target_files = [
    'factcheck_ai_police_face_screening_trial_sparks_privacy_concern_107009644.json',
    'factcheck_amazon_deforestation_hits_13_year_low.json',
    'factcheck_apple-external-link-commission.json',
    'factcheck_act-recriminalising-methamphetamine-ignores-evidence-advocates.json',
    'factcheck_ai_store_manager_fires_employee.json',
    'factcheck_aukus_sovereignty_audit.json',
    'factcheck_anthropic-export-ban.json',
    'factcheck_alzheimers-sleep-restoration-breakthrough.json',
    'factcheck_aluminium_smelter_bailout_2026.json',
    'factcheck_aipac-didnt-always-spend-on-campaigns-now-it-faces-criticism-over-money-in-politics.json'
]

for idx, fname in enumerate(target_files, 1):
    fpath = os.path.join("bluesky_bot", "stories", "live", fname)
    with open(fpath, "r", encoding="utf-8") as f:
        d = json.load(f)
        if isinstance(d, list): d = d[0]
    url = d.get("link", "")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            full_txt = extract_full_clean_article(html)
            print(f"[{idx}/10] Full clean text: {len(full_txt)} chars | First 60: {full_txt[:60].replace(chr(10), ' ')} | Last 60: {full_txt[-60:].replace(chr(10), ' ')}")
    except Exception as e:
        print(f"[{idx}/10] ERROR: {e}")