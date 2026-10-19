import os
import json
import re

bot_dir = os.path.dirname(os.path.abspath(__file__))
live_dir = os.path.join(bot_dir, "stories", "live")
report_file = os.path.join(bot_dir, "live_partisan_screening_report.json")

RIGHT_WING_DOMAINS = [
    'foxnews.com', 'nypost.com', 'breitbart.com', 'washingtonexaminer.com',
    'dailywire.com', 'freebeacon.com', 'thefederalist.com', 'theblaze.com',
    'newsmax.com', 'oann.com', 'dailycaller.com', 'westernjournal.com'
]

OPPO_MARKERS = [
    r'\bunearthed\b', r'\bresurfaced\b', r'\bfirst on fox\b', r'\byears ago\b',
    r'\bpast comments\b', r'\bslams\b', r'\bblasts\b', r'\bunder fire\b',
    r'\berupts\b', r'\bsatanic\b', r'\bsodomized\b', r'\bdrag queen\b',
    r'\battack on\b', r'\bcaught on tape\b', r'\bleaked audio\b'
]

CULTURE_WAR_MARKERS = [
    r'\bwoke\b', r'\bdei\b', r'\btransgender\b', r'\billegal immigrant\b',
    r'\bsocialist\b', r'\bradical left\b', r'\bgender identity\b', r'\btax bomb\b',
    r'\bweaponization\b', r'\bindoctrination\b', r'\bdefund\b'
]

CAMPAIGN_MARKERS = [
    r'\btalarico\b', r'\bpaxton\b', r'\bsenate race\b', r'\bmidterm\b',
    r'\belection\b', r'\bcampaign\b', r'\bprimary\b', r'\bgovernor race\b'
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

def screen_story(data, filename):
    subject = data.get("subject", "")
    url = data.get("link") or data.get("url") or ""
    posts = data.get("posts", [])
    all_text = (subject + " " + " ".join(posts)).lower()

    domain = get_domain(url)
    real_u = data.get("real_u", 0.0)
    real_psi = data.get("real_psi", 0.0)
    rnet = data.get("real_rnet", 1.0)
    aspects = data.get("aspects", [])
    actors = data.get("actors", [])
    rkeys = data.get("rkeys", [])
    post_urls = data.get("post_urls", [])

    has_oppo = any(re.search(pat, all_text) for pat in OPPO_MARKERS)
    has_cw = any(re.search(pat, all_text) for pat in CULTURE_WAR_MARKERS)
    has_campaign = any(re.search(pat, all_text) for pat in CAMPAIGN_MARKERS)

    # Check if outlet was audited as a separate aspect
    audited_outlet = False
    if aspects:
        for a in aspects:
            a_name = str(a.get("aspect", "")).lower()
            if any(d.replace('.com', '') in a_name for d in RIGHT_WING_DOMAINS) or "media" in a_name or "framing" in a_name:
                audited_outlet = True
                break

    # Classification logic
    classification = "CLEAN"
    risk_reasons = []

    if has_oppo:
        risk_reasons.append("Contains opposition dump markers (unearthed/resurfaced/first on fox/slams)")
    if has_campaign:
        risk_reasons.append("Directly targets active election/campaign candidate")
    if has_cw:
        risk_reasons.append("Relies on culture-war wedge triggers")

    if has_oppo and has_campaign:
        classification = "CRITICALLY_COMPROMISED"
        risk_reasons.append("High probability of laundered campaign oppo-dump")
    elif has_oppo and not audited_outlet:
        classification = "CRITICALLY_COMPROMISED"
        risk_reasons.append("Oppo-dump evaluated without auditing media framing")
    elif (has_cw or has_campaign) and real_u < -0.3 and not audited_outlet:
        classification = "SUSPECT"
        risk_reasons.append("Candidate/topic failed under partisan framing without separate outlet audit")
    elif has_cw:
        classification = "SUSPECT"
    else:
        classification = "CLEAN"

    return {
        "file": filename,
        "id": data.get("id", filename.replace("factcheck_", "").replace(".json", "")),
        "domain": domain,
        "subject": subject,
        "classification": classification,
        "risk_reasons": risk_reasons,
        "claim_u": data.get("claim_u"),
        "claim_psi": data.get("claim_psi"),
        "real_u": real_u,
        "real_psi": real_psi,
        "rnet": rnet,
        "audited_outlet": audited_outlet,
        "actors": actors,
        "url": url,
        "rkeys": rkeys,
        "thread_url": post_urls[0] if post_urls else ""
    }

def main():
    print(f"Scanning {live_dir} for right-wing media stories...")
    files = [f for f in os.listdir(live_dir) if f.startswith("factcheck_") and f.endswith(".json")]
    
    screened = []
    for f in files:
        filepath = os.path.join(live_dir, f)
        try:
            with open(filepath, "r", encoding="utf-8") as fp:
                data = json.load(fp)[0]
            url = data.get("link") or data.get("url") or ""
            if is_rw(url):
                res = screen_story(data, f)
                screened.append(res)
        except Exception:
            pass

    # Save complete JSON report
    with open(report_file, "w", encoding="utf-8") as out:
        json.dump(screened, out, indent=2, ensure_ascii=False)
    print(f"Detailed report saved to {report_file}")

    # Summary Stats
    total = len(screened)
    critical = [s for s in screened if s["classification"] == "CRITICALLY_COMPROMISED"]
    suspect = [s for s in screened if s["classification"] == "SUSPECT"]
    clean = [s for s in screened if s["classification"] == "CLEAN"]

    print("\n" + "=" * 80)
    print("LIVE DATABASE PARTISAN SCREENING SUMMARY")
    print("=" * 80)
    print(f"Total Right-Wing Media Live Stories: {total}")
    print(f"  - CRITICALLY COMPROMISED: {len(critical)} ({len(critical)/total*100:.1f}%)")
    print(f"  - SUSPECT (Needs Review):  {len(suspect)} ({len(suspect)/total*100:.1f}%)")
    print(f"  - CLEAN (Factual Reports):  {len(clean)} ({len(clean)/total*100:.1f}%)")

    # Outlet breakdown
    print("\nOutlet Breakdown:")
    by_dom = {}
    for s in screened:
        d = s["domain"]
        by_dom.setdefault(d, {"total": 0, "critically_compromised": 0, "suspect": 0, "clean": 0})
        by_dom[d]["total"] += 1
        by_dom[d][s["classification"].lower()] += 1
    
    for d, stats in sorted(by_dom.items(), key=lambda x: -x[1]["total"]):
        print(f"  {d:<22} Total: {stats['total']:<4} | Critical: {stats['critically_compromised']:<3} | Suspect: {stats['suspect']:<3} | Clean: {stats['clean']:<3}")

    print("\n" + "=" * 80)
    print(f"TOP 15 CRITICALLY COMPROMISED CANDIDATES (SAMPLE)")
    print("=" * 80)
    for idx, s in enumerate(critical[:15], 1):
        print(f"{idx}. [{s['domain']}] {s['subject']}")
        print(f"   Coords: ({s['real_u']}, {s['real_psi']}) | R_net: {s['rnet']}")
        print(f"   Reasons: {', '.join(s['risk_reasons'])}")
        print(f"   Thread: {s['thread_url']}")
        print(f"   File:   {s['file']}\n")

if __name__ == "__main__":
    main()
