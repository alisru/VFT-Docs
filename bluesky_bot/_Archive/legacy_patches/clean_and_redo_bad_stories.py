import os
import sys
import json
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from generate_graph import enforce_deterministic_trajectory, get_path_name

drafts_dir = os.path.join(script_dir, "stories")
idx_path = os.path.join(drafts_dir, "index.json")

with open(idx_path, "r", encoding="utf-8") as f:
    drafts_index = json.load(f)

# 1. Prune pure meta-fluff stories
fluff_files = [
    "factcheck_pod-save-america-hosts-call-democratic-party-midterm-wins-end-trump-era.json",
    "factcheck_erika_kirk_midterm_message.json",
    "factcheck_charlamagne-tha-god-warns-democrats.json",
    "factcheck_mamdani-chicken-scratch-notes.json"
]

pruned_count = 0
for fn in fluff_files:
    if fn in drafts_index:
        drafts_index.remove(fn)
        pruned_count += 1
        fp = os.path.join(drafts_dir, fn)
        if os.path.exists(fp):
            # Mark status as PRUNED_META_FLUFF
            with open(fp, "r", encoding="utf-8") as f:
                d = json.load(f)
            s = d[0] if isinstance(d, list) else d
            s["status"] = "PRUNED_META_FLUFF"
            with open(fp, "w", encoding="utf-8") as f:
                json.dump([s] if isinstance(d, list) else s, f, indent=2, ensure_ascii=False)
        print(f"[PRUNED FLUFF] Removed from queue: {fn}")

# 2. Re-audit Trump Iran 'Soft War' story accurately into Quadrant II (Deception)
iran_fn = "factcheck_trump-iran-conflict-soft-war-midterms-2026.json"
iran_fp = os.path.join(drafts_dir, iran_fn)
if os.path.exists(iran_fp):
    with open(iran_fp, "r", encoding="utf-8") as f:
        data = json.load(f)
    story = data[0] if isinstance(data, list) else data
    story["claim_u"] = 0.5
    story["claim_psi"] = 0.4
    story["real_u"] = -0.4
    story["real_psi"] = 0.3
    story["status"] = "DRAFT (CALIBRATED)"
    
    if "stated_forces" in story: del story["stated_forces"]
    if "actual_forces" in story: del story["actual_forces"]
    
    posts = story.get("posts", [])
    posts[0] = "Campaign speeches reframe ongoing regional military clashes as economic and diplomatic 'soft war.'\nEvidence: Speech transcripts, regional military reports\n#Diplomacy #USPol #Iran"
    posts[1] = "Political speeches framed Middle Eastern deterrence as an economic 'soft war' where national leadership holds total strategic control.\nStated Judgement: (+0.5, +0.4) - Strategic Leverage"
    posts[2] = "Characterizing active kinetic drone strikes and regional military exchanges as mere 'soft war' downplays physical conflict realities to soothe midterm voter anxiety.\nResulting Judgement: (-0.4, +0.3) - Electoral Framing"
    posts[3] = "Verdict: FAIL - Fall into Deception.\nMinimizing active military hostilities as non-kinetic 'soft war' to protect domestic electoral standing."
    posts[4] = "- Campaign Political Operation: FAIL (-0.5, +0.3) - Downplaying active kinetic regional conflict as mere economic 'soft war' for electoral reassurance.\n- Defense & Geopolitical Analysts: PASS (+0.5, +0.3) - Grounding Middle Eastern security realities in factual military engagements."
    
    story["posts"] = posts
    story = enforce_deterministic_trajectory(story)
    story["path_name"] = get_path_name(story["claim_u"], story["claim_psi"], story["real_u"], story["real_psi"])
    
    with open(iran_fp, "w", encoding="utf-8") as f:
        json.dump([story] if isinstance(data, list) else story, f, indent=2, ensure_ascii=False)
    print(f"[RE-AUDITED] {iran_fn} -> ({story['claim_u']},{story['claim_psi']}) -> ({story['real_u']},{story['real_psi']}) | {story['path_name']}")

# 3. Clean Fox News boilerplate from remaining stories' scraped_text
bp_regex = re.compile(
    r'(?:This material may not be published,\s*broadcast,\s*rewritten,\s*or redistributed[^\n]*|'
    r'Quotes displayed in real-time or delayed[^\n]*|'
    r'Market data provided by[^\n]*|'
    r'You\'ve successfully subscribed[^\n]*|'
    r'All rights reserved\.\s*©[^\n]*)',
    re.I
)

cleaned_count = 0
for fn in drafts_index:
    fp = os.path.join(drafts_dir, fn)
    if not os.path.exists(fp): continue
    with open(fp, "r", encoding="utf-8") as f:
        d = json.load(f)
    s = d[0] if isinstance(d, list) else d
    raw_txt = s.get("scraped_text", "")
    if not raw_txt: continue
    
    new_txt = bp_regex.sub("", raw_txt).strip()
    new_txt = re.sub(r'\n{3,}', '\n\n', new_txt)
    
    if new_txt != raw_txt:
        s["scraped_text"] = new_txt
        with open(fp, "w", encoding="utf-8") as f:
            json.dump([s] if isinstance(d, list) else s, f, indent=2, ensure_ascii=False)
        cleaned_count += 1

print(f"[CLEANED BOILERPLATE] Stripped copyright boilerplate from {cleaned_count} draft stories.")

# 4. Save updated drafts index
with open(idx_path, "w", encoding="utf-8") as f:
    json.dump(drafts_index, f, indent=2, ensure_ascii=False)

print(f"\nUpdated drafts index: {len(drafts_index)} stories pending review.")
