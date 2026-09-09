import json, os

log_file = os.path.join("bluesky_bot", "harvested_stories_log.jsonl")

# Index log
log_by_id = {}
log_by_url = {}

with open(log_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line: continue
        try:
            d = json.loads(line)
            sid = d.get("id", "").strip()
            url = d.get("url", "").strip()
            if sid: log_by_id[sid] = d
            if url: log_by_url[url] = d
        except Exception:
            pass

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
        data = json.load(f)
        d = data[0] if isinstance(data, list) else data
    sid = d.get("id", "")
    url = d.get("link", "")
    
    found_entry = log_by_id.get(sid) or log_by_url.get(url)
    if found_entry:
        txt = found_entry.get("text", found_entry.get("content", ""))
        print(f"[{idx}/10] FOUND in log: {sid[:35]} | Full Text Length: {len(txt)} chars")
    else:
        print(f"[{idx}/10] NOT in log: {sid[:35]} | URL: {url[:50]}")