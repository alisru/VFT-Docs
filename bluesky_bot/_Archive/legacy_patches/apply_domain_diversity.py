import os

path = os.path.join(os.path.dirname(__file__), 'harvest_candidates.py')
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = """    all_final = combined_candidates[:TARGET_RSS + TARGET_BSKY]
    all_final.sort(key=get_sort_key)"""

replacement = """    # Enforce domain diversity capping (prevent any single domain from flooding the batch)
    domain_counts = {}
    diverse_candidates = []
    overflow_candidates = []
    for c in combined_candidates:
        url = c.get("url", "")
        try:
            host = urllib.parse.urlparse(url).hostname or ""
            if host.startswith("www."):
                host = host[4:]
        except Exception:
            host = ""
        domain = host or "unknown"
        if domain_counts.get(domain, 0) < 2:
            diverse_candidates.append(c)
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
        else:
            overflow_candidates.append(c)

    all_final = (diverse_candidates + overflow_candidates)[:TARGET_RSS + TARGET_BSKY]
    all_final.sort(key=get_sort_key)"""

text_norm = text.replace('\r\n', '\n')
target_norm = target.replace('\r\n', '\n')
replacement_norm = replacement.replace('\r\n', '\n')

if target_norm in text_norm:
    text_norm = text_norm.replace(target_norm, replacement_norm)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text_norm)
    print("Successfully added domain diversity capping in harvest_candidates.py")
else:
    print("Target not found in harvest_candidates.py")
