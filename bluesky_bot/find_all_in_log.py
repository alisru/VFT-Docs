import json, os, urllib.parse

log_file = os.path.join("bluesky_bot", "harvested_stories_log.jsonl")

entries = []
with open(log_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            try: entries.append(json.loads(line))
            except Exception: pass

print(f"Loaded {len(entries)} entries from log.")

target_slugs = [
    ("face_screening", "ai_police_face_screening_trial_sparks_privacy_concern_107009644"),
    ("amazon", "amazon_deforestation_hits_13_year_low"),
    ("apple", "apple-external-link-commission"),
    ("methamphetamine", "act-recriminalising-methamphetamine-ignores-evidence-advocates"),
    ("fired-employee", "ai_store_manager_fires_employee"),
    ("aukus", "aukus_sovereignty_audit"),
    ("anthropic", "anthropic-export-ban"),
    ("alzheimers", "alzheimers-sleep-restoration-breakthrough"),
    ("aluminium", "aluminium_smelter_bailout_2026"),
    ("aipac", "aipac-didnt-always-spend-on-campaigns-now-it-faces-criticism-over-money-in-politics")
]

for slug, name in target_slugs:
    matches = [e for e in entries if slug in e.get("url", "").lower() or slug in e.get("title", "").lower() or slug in e.get("id", "").lower()]
    print(f"Slug '{slug}' ({name}): {len(matches)} matches in log")
    if matches:
        m = matches[0]
        print(f"  -> Title: {m.get('title', '')[:40]} | URL: {m.get('url', '')[:45]} | Text length: {len(m.get('text', m.get('content', '')))}")