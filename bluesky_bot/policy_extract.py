"""policy_extract.py \u2014 Deterministic (non-LLM) policy extraction for Aletheia stories.

Detects policy domain mentions from story subjects and posts using a curated
regex map \u2014 same pattern as actor_extract.py but for policy areas.

Also manages the policy_ledger.json: auto-updating entries whenever a new
story is evaluated, tracking running averages of moral coordinates per policy.
"""
import re
import os
import json
import datetime
import tempfile

script_dir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LEDGER_PATH = os.path.join(script_dir, "policy_ledger.json")


# ── Policy map (regex -> canonical name) ─────────────────────────────────────
# All patterns matched case-insensitively.
POLICY_MAP = {
    # Housing
    r"\bhousing\s*(crisis|affordability|affordabe|policy|plan|reform|supply|shortage|market)\b": "Housing Policy",
    r"\brenters?(\s+rights?)?\b|\blandlord\b|\brevent\s+freeze\b|\bnegative\s+gearing\b": "Housing Policy",

    # Trade & Tariffs
    r"\btariff[s]?\b|\btrade\s+war\b|\bprotectionism\b|\btrade\s+barrier[s]?\b": "Trade Tariffs",
    r"\btrade\s+(deal|agreement|dispute|war|policy|sanction[s]?)\b": "Trade Policy",

    # Climate & Energy
    r"\bclimate\s*(change|action|policy|plan|target[s]?|crisis)\b": "Climate Policy",
    r"\bnet\s+zero\b|\bcarbon\s+(tax|credit|offset[s]?|neutral)\b|\bemissions?\s+(target[s]?|reduction)\b": "Climate Policy",
    r"\brenewable\s+(energy|target[s]?|policy|transition)\b|\bclean\s+energy\b|\bsolar\s+(farm|panel[s]?)\b|\bwind\s+(farm|turbine[s]?)\b": "Renewable Energy",
    r"\bcoal\s+(mine|power|plant|phase.out|subsidies?)\b|\bfossil\s+fuel[s]?\b": "Fossil Fuels Policy",

    # Immigration & Border
    r"\bimmigration\s*(policy|reform|bill|plan|cap|cut[s]?|wave)\b": "Immigration Policy",
    r"\bborder\s+(policy|wall|control|security|crossing[s]?)\b|\bborder\s+force\b": "Immigration Policy",
    r"\brefugee[s]?\b|\basylum\s+seeker[s]?\b|\bvisa\s+(policy|rule[s]?|change[s]?)\b": "Immigration Policy",

    # NDIS & Disability
    r"\bndis\b|\bdisability\s+(scheme|insurance|policy|funding|support|reform)\b": "NDIS",

    # Healthcare
    r"\bhealth\s*(care|policy|funding|reform|system|spending)\b|\bnhs\b|\bmedicare\b": "Healthcare Policy",
    r"\bhospital\s*(funding|capacity|waitlist[s]?|bed[s]?)\b|\bmental\s+health\s*(funding|system|services?)\b": "Healthcare Policy",

    # Tax
    r"\btax\s*(cut[s]?|rise[s]?|reform|policy|break[s]?|hike|relief|haven[s]?)\b|\bincome\s+tax\b|\bcapital\s+gains\b": "Tax Policy",
    r"\bstage\s+3\s+tax\b|\bfringe\s+benefits\s+tax\b|\bgst\b": "Tax Policy",

    # Defence
    r"\bdefence\s*(policy|spending|budget|capability|force[s]?)\b|\bmilitary\s+(budget|spending|policy|force[s]?)\b": "Defence Policy",
    r"\baukus\b|\banmzus\b|\bquad\b|\bfive\s+eyes\b": "AUKUS",

    # Foreign Aid
    r"\bforeign\s+aid\b|\baid\s+(budget|cut[s]?|package|program[s]?)\b|\boverseas\s+development\b": "Foreign Aid",

    # First Nations / Indigenous
    r"\bvoice\s+to\s+parliament\b|\bindigenous\s+(voice|referendum|rights?|treaty|land\s+rights?)\b": "First Nations Policy",
    r"\baboriginal\s+(rights?|land|policy|funding|community)\b|\btreaty\b": "First Nations Policy",
    r"\bclose\s+the\s+gap\b|\bindigenous\s+(health|housing|education)\b": "First Nations Policy",

    # Welfare
    r"\bwelfare\s*(reform|cut[s]?|policy|payment[s]?|system)\b|\bsocial\s+security\b|\bjobseeker\b|\bjobkeeper\b": "Welfare Policy",
    r"\bunemployment\s*(benefit[s]?|rate|payment[s]?)\b|\bcentrelink\b": "Welfare Policy",

    # Education
    r"\beducation\s*(policy|funding|reform|cut[s]?|system|budget)\b|\buniversity\s+(funding|fee[s]?|cut[s]?)\b": "Education Policy",
    r"\bschool\s*(funding|policy|curriculum|system)\b|\bhecs\b|\bhecs.help\b": "Education Policy",

    # Industrial Relations
    r"\bworkers?\s+(rights?|conditions?|pay|wages?|exploitation)\b|\bindustrial\s+relations\b|\bfair\s+work\b": "Industrial Relations",
    r"\bminimum\s+wage\b|\bgig\s+(economy|worker[s]?)\b|\bunion[s]?\b|\bcfmeu\b": "Industrial Relations",

    # Cost of Living
    r"\bcost\s+of\s+living\b|\binflation\b|\binterest\s+rate[s]?\b|\bcpi\b": "Cost of Living",
    r"\bgrocery\s+(price[s]?|cost[s]?)\b|\bpower\s+bill[s]?\b|\benergy\s+(price[s]?|bill[s]?|cost[s]?)\b": "Cost of Living",

    # AI Regulation
    r"\bai\s+(regulation|safety|policy|bill|act|governance|law[s]?)\b": "AI Regulation",
    r"\bartificial\s+intelligence\s+(policy|regulation|governance|safety)\b": "AI Regulation",

    # Supreme Court / Judicial
    r"\bscotus\b|\bsupreme\s+court\b|\bhigh\s+court\b": "Judicial Policy",

    # Media / Disinformation
    r"\bmedia\s+(regulation|policy|law[s]?|reform|ownership)\b|\bfake\s+news\b|\bmisinformation\b|\bdisinformation\b": "Media & Information Policy",

    # Housing (catch-all for price mentions with property)
    r"\bproperty\s+(price[s]?|market|tax|bubble|boom)\b": "Housing Policy",
}


def slugify(name: str) -> str:
    """Convert 'Housing Policy' -> 'housing-policy'."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def extract_policies(text: str, max_policies: int = 4) -> list:
    """Return a de-duplicated list of detected policy names from text.

    Args:
        text: Story subject line, post text, or any article text.
        max_policies: Maximum number of distinct policies to return.

    Returns:
        List of canonical policy name strings (e.g. ['Housing Policy', 'Cost of Living']).
    """
    if not text:
        return []

    matched = []
    for pattern, canonical in POLICY_MAP.items():
        if re.search(pattern, text, re.IGNORECASE):
            if canonical not in matched:
                matched.append(canonical)

    return matched[:max_policies]


def _load_ledger(ledger_path: str) -> dict:
    """Load policy_ledger.json or return a fresh structure."""
    if os.path.exists(ledger_path):
        try:
            with open(ledger_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"version": 1, "last_updated": "", "policies": {}}


def _save_ledger(ledger: dict, ledger_path: str):
    """Write ledger atomically."""
    tmp_fd, tmp_path = tempfile.mkstemp(dir=os.path.dirname(ledger_path), suffix=".tmp")
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, ledger_path)
    except Exception:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass
        raise


def update_policy_ledger(story_config: dict, ledger_path: str = DEFAULT_LEDGER_PATH) -> list:
    """Auto-update the policy ledger with a newly evaluated story.

    Extracts policies from the story's subject + first 3 posts, then upserts
    each detected policy into the ledger. Recalculates running averages of
    real_u and real_psi for each policy.

    Args:
        story_config: The evaluated story config dict (factcheck JSON content[0]).
        ledger_path: Path to policy_ledger.json.

    Returns:
        List of canonical policy names detected in this story.
    """
    # Build text to scan
    subject = story_config.get("subject", "") or ""
    posts = story_config.get("posts", []) or []
    scan_text = subject + " " + " ".join(posts[:3])

    policies_found = extract_policies(scan_text)
    if not policies_found:
        return []

    # Story identifiers
    story_id = story_config.get("id", "") or story_config.get("slug", "")
    real_u = story_config.get("real_u")
    real_psi = story_config.get("real_psi")
    today = datetime.date.today().isoformat()

    # Verdict
    verdict = "PASS"
    if real_u is not None and real_psi is not None:
        verdict = "PASS" if (real_u >= 0 and real_psi >= 0) else "FAIL"

    ledger = _load_ledger(ledger_path)
    ledger["last_updated"] = today

    for canonical in policies_found:
        slug = slugify(canonical)

        if slug not in ledger["policies"]:
            # New entry
            ledger["policies"][slug] = {
                "name": canonical,
                "slug": slug,
                "first_seen": today,
                "last_updated": today,
                "story_count": 0,
                "stories": [],
                "avg_real_u": None,
                "avg_real_psi": None,
                "verdicts": [],
                "pass_count": 0,
                "fail_count": 0,
            }

        entry = ledger["policies"][slug]

        # Avoid double-counting if story already in ledger
        if story_id and story_id in entry["stories"]:
            continue

        # Update counts
        entry["story_count"] += 1
        entry["last_updated"] = today
        if story_id:
            entry["stories"].append(story_id)

        # Running average of coordinates
        if real_u is not None and real_psi is not None:
            prev_u = entry["avg_real_u"]
            prev_psi = entry["avg_real_psi"]
            n = entry["story_count"]
            if prev_u is None:
                entry["avg_real_u"] = round(real_u, 4)
                entry["avg_real_psi"] = round(real_psi, 4)
            else:
                # Incremental mean: new_avg = old_avg + (new_val - old_avg) / n
                entry["avg_real_u"] = round(prev_u + (real_u - prev_u) / n, 4)
                entry["avg_real_psi"] = round(prev_psi + (real_psi - prev_psi) / n, 4)

        entry["verdicts"].append(verdict)
        if verdict == "PASS":
            entry["pass_count"] += 1
        else:
            entry["fail_count"] += 1

    _save_ledger(ledger, ledger_path)
    return policies_found


if __name__ == "__main__":
    import sys
    test_text = sys.argv[1] if len(sys.argv) > 1 else "Housing affordability crisis deepens as interest rates rise"
    found = extract_policies(test_text)
    print(f"Detected policies: {found}")
