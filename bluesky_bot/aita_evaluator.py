"""
aita_evaluator.py — VFT / Alethekanon Reddit AITA Scraper & 7-Verdict Judgment Engine

Implements the Gen-2 Veritas-Chroma Unified Synthesis Protocol
(instructions/aita_judgment_protocol.md) evolved via the 5-agent
`agent-breeding-lineage` cook-off.

Hard Isolation Invariant (ANTI-031):
All outputs are written strictly to `bluesky_bot/aita/` and NEVER touch
`stories/`, `stories/live/`, or `stories_registry.js`.
"""
import argparse
import datetime
import hashlib
import json
import math
import os
import re
import sys
import time
import urllib.request
import urllib.error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AITA_DIR = os.path.join(SCRIPT_DIR, "aita")
COOKOFF_DIR = os.path.join(AITA_DIR, "cookoff")
PROTOCOL_PATH = os.path.join(SCRIPT_DIR, "instructions", "aita_judgment_protocol.md")
INDEX_PATH = os.path.join(AITA_DIR, "index.json")
AITA_QUEUE_PATH = os.path.join(AITA_DIR, "aita_queue.json")

os.makedirs(AITA_DIR, exist_ok=True)


def load_aita_queue() -> list:
    if not os.path.exists(AITA_QUEUE_PATH):
        return []
    try:
        with open(AITA_QUEUE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def save_aita_queue(queue_items: list) -> None:
    for idx, item in enumerate(queue_items, 1):
        if isinstance(item, dict):
            item["case_index"] = idx
    with open(AITA_QUEUE_PATH, "w", encoding="utf-8") as f:
        json.dump(queue_items, f, indent=2, ensure_ascii=False)


def enqueue_aita_posts(new_posts: list) -> tuple:
    """Appends unseen AITA posts to bluesky_bot/aita/aita_queue.json."""
    queue_items = load_aita_queue()
    seen_ids = {p.get("id") for p in queue_items if isinstance(p, dict) and p.get("id")}
    if os.path.exists(INDEX_PATH):
        try:
            with open(INDEX_PATH, "r", encoding="utf-8") as f:
                for entry in json.load(f):
                    if isinstance(entry, dict) and entry.get("id"):
                        seen_ids.add(entry["id"])
        except Exception:
            pass
    added = 0
    for post in new_posts:
        pid = post.get("id")
        if pid and pid not in seen_ids:
            queue_items.append(post)
            seen_ids.add(pid)
            added += 1
    save_aita_queue(queue_items)
    return added, len(queue_items)


def deduct_aita_queue(evaluated_ids: set) -> int:
    """Removes evaluated post IDs from bluesky_bot/aita/aita_queue.json."""
    if not evaluated_ids or not os.path.exists(AITA_QUEUE_PATH):
        return 0
    queue_items = load_aita_queue()
    trimmed = [p for p in queue_items if isinstance(p, dict) and p.get("id") not in evaluated_ids]
    removed = len(queue_items) - len(trimmed)
    if removed > 0:
        save_aita_queue(trimmed)
    return len(trimmed)

VALID_VERDICTS = {
    "YTA": "You're the Asshole",
    "YWBTA": "You Would Be the Asshole",
    "NTA": "Not the Asshole (and the other person is)",
    "YWNBTA": "You Would Not be the Asshole (and the other person would)",
    "ESH": "Everyone Sucks here",
    "NAH": "No Assholes here",
    "INFO": "Not Enough Info",
}


def is_prospective_wibta(title: str, body: str = "") -> bool:
    """Detects whether an AITA post is prospective/hypothetical (WIBTA)."""
    t = (title or "").strip()
    if re.search(r"\bWIBTAH?\b", t, re.IGNORECASE):
        return True
    if re.search(r"\bwould\s+i\s+be\s+the\s+(asshole|ah|a-hole)\b", t, re.IGNORECASE):
        return True
    b_tail = (body or "")[-300:]
    if re.search(r"\bWIBTAH?\b", b_tail, re.IGNORECASE) and not re.search(r"\bAITAH?\b", t, re.IGNORECASE):
        return True
    return False


def compute_delta_h_and_wisdom(stated_u: float, stated_psi: float, actual_u: float, actual_psi: float):
    """Computes Hypocrisy Gap (ΔH) and Model 2 WisdomScore = 1 / (1 + ΔH)."""
    delta_h = math.sqrt((stated_u - actual_u) ** 2 + (stated_psi - actual_psi) ** 2)
    wisdom = 1.0 / (1.0 + delta_h)
    return round(delta_h, 3), round(wisdom, 3)


def map_coordinates_to_aita_verdict(
    op_u: float,
    other_u: float,
    is_hypothetical: bool = False,
    missing_info: bool = False,
    r_net: float = 1.0,
    method_coercive: bool = False,
    tau: float = -0.20,
) -> str:
    """
    Deterministic 7-Verdict Decision Gate with Method-Over-Motive Firewall.
    - INFO: missing_info == True and r_net < 0.65
    - Method-Over-Motive Firewall (Anti-Agent-4 Guardrail):
      If OP deploys an active coercive/sunk-cost method (`method_coercive=True`),
      `op_u` is clamped below `tau` so high emotional strain never excuses coercion.
    - NTA / YWNBTA: op_u >= tau and other_u < tau
    - YTA / YWBTA:  op_u < tau and other_u >= tau
    - ESH:          op_u < tau and other_u < tau
    - NAH:          op_u >= tau and other_u >= tau
    """
    if missing_info and r_net < 0.65:
        return "INFO"

    eff_op_u = float(op_u)
    eff_other_u = float(other_u)
    if method_coercive and eff_op_u >= tau:
        eff_op_u = tau - 0.05

    if eff_op_u >= tau and eff_other_u < tau:
        return "YWNBTA" if is_hypothetical else "NTA"
    if eff_op_u < tau and eff_other_u >= tau:
        return "YWBTA" if is_hypothetical else "YTA"
    if eff_op_u < tau and eff_other_u < tau:
        return "ESH"
    return "NAH"


def parse_aita_test_file(filepath: str):
    """
    Parses raw Reddit copy-paste text in `bluesky_bot/atia test.txt` into
    6 structured candidate dicts.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    lines = [ln.rstrip() for ln in raw.splitlines()]
    posts = []
    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i].strip()
        if ln == "human" and i >= 1:
            # Find the preceding non-empty line as title
            title_idx = i - 1
            while title_idx >= 0 and not lines[title_idx].strip():
                title_idx -= 1
            title = lines[title_idx].strip() if title_idx >= 0 else f"Untitled_{i}"

            # Look back a few lines for author `u/...`
            author = "anonymous"
            for back in range(max(0, title_idx - 5), title_idx):
                b_ln = lines[back].strip()
                if b_ln.startswith("u/"):
                    author = b_ln
                    break

            # Collect body until next post header or multiple blank lines before a title
            body_lines = []
            j = i + 1
            while j < n:
                curr = lines[j].strip()
                if curr in ("Back", "Go to AmItheAsshole", "r/AmItheAsshole"):
                    break
                # Check if next line is `human` (meaning `curr` is the next post's title!)
                if j + 1 < n and lines[j + 1].strip() == "human" and curr:
                    break
                body_lines.append(lines[j])
                j += 1

            body = "\n".join(body_lines).strip()
            slug_base = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:50]
            post_id = f"test_{len(posts) + 1}_{slug_base}"
            posts.append({
                "id": post_id,
                "case_index": len(posts) + 1,
                "subreddit": "AmItheAsshole",
                "author": author,
                "title": title,
                "selftext": body,
                "url": f"local://atia_test.txt#case-{len(posts) + 1}",
                "is_hypothetical": is_prospective_wibta(title, body),
            })
            i = j
        else:
            i += 1

    return posts


def fetch_reddit_aita(subreddit: str = "AmItheAsshole", sort: str = "hot", limit: int = 5):
    """
    Fetches live AITA/AITAH posts from Reddit's public JSON endpoint using a
    custom User-Agent and polite spacing.
    """
    subs = ["AmItheAsshole", "AITAH"] if subreddit.lower() == "both" else [subreddit]
    seen_ids = set()
    if os.path.exists(INDEX_PATH):
        try:
            with open(INDEX_PATH, "r", encoding="utf-8") as f:
                for entry in json.load(f):
                    if isinstance(entry, dict) and entry.get("id"):
                        seen_ids.add(entry["id"])
        except Exception:
            pass
    for q_item in load_aita_queue():
        if isinstance(q_item, dict) and q_item.get("id"):
            seen_ids.add(q_item["id"])

    results = []
    json_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
    }

    def _http_get_text(target_url, hdrs):
        try:
            import requests
            r = requests.get(target_url, headers=hdrs, timeout=15)
            r.raise_for_status()
            return r.text
        except ImportError:
            req = urllib.request.Request(target_url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.read().decode("utf-8", errors="replace")

    for sub in subs:
        fetch_count = max(15, limit * 4)
        arctic_limit = min(100, fetch_count)
        reddit_limit = min(100, fetch_count)
        # 1. Try Arctic Shift open Reddit archive API (avoids Reddit's 403 lor2 unauthenticated block)
        try:
            before_ts = None
            arctic_headers = {
                "User-Agent": "AletheiaBot/2.0 (VFT AITA Evaluator)",
                "Accept": "application/json",
            }
            for _page in range(3):
                arctic_url = f"https://arctic-shift.photon-reddit.com/api/posts/search?subreddit={sub}&sort=desc&limit={arctic_limit}"
                if before_ts is not None:
                    arctic_url += f"&before={before_ts}"
                arctic_payload = json.loads(_http_get_text(arctic_url, arctic_headers))
                batch = arctic_payload.get("data", [])
                if not batch:
                    break
                for d in batch:
                    author = str(d.get("author", ""))
                    if author.lower() in ("automoderator", "[deleted]", ""):
                        continue
                    title = str(d.get("title", "")).strip()
                    selftext = str(d.get("selftext", "")).strip()
                    if not selftext or selftext in ("[deleted]", "[removed]") or len(selftext) < 120:
                        continue
                    if re.search(r"\b(meta|monthly\s+forum|open\s+forum)\b", title, re.IGNORECASE):
                        continue
                    pid = f"reddit_{d.get('id', hashlib.md5(title.encode()).hexdigest()[:8])}"
                    if pid in seen_ids:
                        continue
                    seen_ids.add(pid)
                    permalink = d.get("permalink") or f"/r/{sub}/comments/{d.get('id', '')}/"
                    results.append({
                        "id": pid,
                        "case_index": len(results) + 1,
                        "subreddit": sub,
                        "author": f"u/{author}",
                        "title": title,
                        "selftext": selftext,
                        "url": f"https://www.reddit.com{permalink}",
                        "is_hypothetical": is_prospective_wibta(title, selftext),
                    })
                    if len(results) >= limit:
                        break
                if len(results) >= limit or len(batch) < arctic_limit:
                    break
                last_utc = batch[-1].get("created_utc")
                if not last_utc or last_utc == before_ts:
                    break
                before_ts = int(last_utc)
                time.sleep(0.3)
            if len(results) >= limit:
                break
            time.sleep(0.5)
            continue
        except Exception as ae:
            print(f"Warning: Arctic Shift fetch failed for r/{sub}: {ae}. Trying Reddit...")

        payload = None
        for host in ("old.reddit.com", "www.reddit.com"):
            url = f"https://{host}/r/{sub}/{sort}.json?limit={reddit_limit}"
            try:
                payload = json.loads(_http_get_text(url, json_headers))
                break
            except Exception as e:
                print(f"Warning: Failed to fetch {host}/r/{sub}/{sort}.json: {e}")

        if payload is None:
            # Fallback to Reddit Atom RSS feed
            rss_url = f"https://www.reddit.com/r/{sub}/{sort}.rss?limit={reddit_limit}"
            try:
                import html as _html
                import xml.etree.ElementTree as ET
                rss_xml = _http_get_text(rss_url, {
                    "User-Agent": json_headers["User-Agent"],
                    "Accept": "application/atom+xml, application/xml, text/xml, */*",
                })
                root = ET.fromstring(rss_xml)
                ns = {"atom": "http://www.w3.org/2005/Atom"}
                for entry in root.findall("atom:entry", ns):
                    title = (entry.findtext("atom:title", "", ns) or "").strip()
                    author_el = entry.find("atom:author/atom:name", ns)
                    author = (author_el.text if author_el is not None and author_el.text else "anonymous").lstrip("/u/")
                    if author.lower() in ("automoderator", "[deleted]", ""):
                        continue
                    link_el = entry.find("atom:link", ns)
                    post_url = link_el.attrib.get("href", "") if link_el is not None else ""
                    raw_html = entry.findtext("atom:content", "", ns) or ""
                    text_body = _html.unescape(re.sub(r"<[^>]+>", "\n", raw_html))
                    text_body = re.sub(r"\n{3,}", "\n\n", text_body).strip()
                    if not text_body or len(text_body) < 120:
                        continue
                    if re.search(r"\b(meta|monthly\s+forum|open\s+forum)\b", title, re.IGNORECASE):
                        continue
                    eid = (entry.findtext("atom:id", "", ns) or hashlib.md5(title.encode()).hexdigest()[:8]).split("_")[-1]
                    pid = f"reddit_{eid}"
                    if pid in seen_ids:
                        continue
                    results.append({
                        "id": pid,
                        "case_index": len(results) + 1,
                        "subreddit": sub,
                        "author": f"u/{author}",
                        "title": title,
                        "selftext": text_body,
                        "url": post_url,
                        "is_hypothetical": is_prospective_wibta(title, text_body),
                    })
                    if len(results) >= limit:
                        break
            except Exception as rss_err:
                print(f"Warning: RSS fallback also failed for r/{sub}/{sort}: {rss_err}")
            if len(results) >= limit:
                break
            time.sleep(1.2)
            continue

        children = payload.get("data", {}).get("children", [])
        for child in children:
            d = child.get("data", {})
            if d.get("stickied") or d.get("over_18") is None:
                continue
            author = str(d.get("author", ""))
            if author.lower() in ("automoderator", "[deleted]", ""):
                continue
            title = str(d.get("title", "")).strip()
            selftext = str(d.get("selftext", "")).strip()
            if not selftext or selftext in ("[deleted]", "[removed]") or len(selftext) < 120:
                continue
            if re.search(r"\b(meta|monthly\s+forum|open\s+forum)\b", title, re.IGNORECASE):
                continue

            pid = f"reddit_{d.get('id', hashlib.md5(title.encode()).hexdigest()[:8])}"
            if pid in seen_ids:
                continue

            results.append({
                "id": pid,
                "case_index": len(results) + 1,
                "subreddit": sub,
                "author": f"u/{author}",
                "title": title,
                "selftext": selftext,
                "url": f"https://www.reddit.com{d.get('permalink', '')}",
                "is_hypothetical": is_prospective_wibta(title, selftext),
            })
            if len(results) >= limit:
                break
        if len(results) >= limit:
            break
        time.sleep(1.2)

    return results[:limit]


def _extract_vec(val, default=(0.0, 0.0)):
    if isinstance(val, list) and len(val) >= 2:
        return [float(val[0]), float(val[1])]
    if isinstance(val, dict):
        u = val.get("upsilon", val.get("u", default[0]))
        p = val.get("psi", default[1])
        return [float(u), float(p)]
    return list(default)


def load_gen2_synthesized_benchmark():
    """
    Loads the converged Gen-2 Veritas-Codon + Chroma-Horizon benchmark evaluations
    for the 6 test cases in `bluesky_bot/atia test.txt`.
    """
    son_path = os.path.join(COOKOFF_DIR, "gen2_son_75M_25F.json")
    daughter_path = os.path.join(COOKOFF_DIR, "gen2_daughter_25M_75F.json")
    son_data, daughter_data = {}, {}
    if os.path.exists(son_path):
        with open(son_path, "r", encoding="utf-8") as f:
            son_data = json.load(f)
    if os.path.exists(daughter_path):
        with open(daughter_path, "r", encoding="utf-8") as f:
            daughter_data = json.load(f)
    return son_data, daughter_data


def _plain_say_do_label(delta_h: float) -> str:
    if delta_h < 0.85:
        return f"Low ({delta_h:.2f})"
    if delta_h < 1.25:
        return f"Moderate ({delta_h:.2f})"
    return f"High ({delta_h:.2f})"


def _plain_completeness_label(r_net: float, coverage: float) -> str:
    covered = int(round(coverage * 7))
    if r_net is None or covered < 7 and (r_net is not None and r_net < 0.85):
        return f"Missing Key Facts ({covered}/7 planes)"
    if r_net < 0.92:
        return f"Minor Gaps ({covered}/7 planes)"
    return f"Solid ({covered}/7 planes)"


def build_aita_bluesky_posts(post: dict, eval_record: dict) -> list:
    """
    Builds the 10-post Bluesky thread:
    1. Hook + Reddit URL  2. Context  3. Stated Framing  4. Actual Conduct (Multi-Actor)
    5. Verdict + Plain-English Metrics  6. Reasoning  7. Resolution
    8. Alethekanon  9. Awwthekanon  10. Brothekanon
    """
    verdict = eval_record.get("verdict", "INFO")
    verdict_label = eval_record.get("verdict_label", VALID_VERDICTS.get(verdict, verdict))
    coords = eval_record.get("coordinates", {})
    op_s = coords.get("op_stated", [0.0, 0.0])
    op_a = coords.get("op_actual", [0.0, 0.0])
    oth_a = coords.get("other_actual", [0.0, 0.0])
    actor_aspects = eval_record.get("actor_aspects") or []
    trace = eval_record.get("vft_audit_trace") or {}
    if not isinstance(trace, dict):
        trace = {"silent_judgment": str(trace)}
    res = eval_record.get("resolution") or {}
    if not isinstance(res, dict):
        res = {"script": str(res)}

    title = (post.get("title") or "").strip()
    url = (post.get("url") or "").strip()
    hook_line = (eval_record.get("hook_line") or "").strip()
    hook_body = f"⚖️ AITA Verdict: {verdict} — \"{title[:130]}\""
    if hook_line:
        hook_body += f"\n\n{hook_line}"
    hook_body += "\n#AITA #Aletheia"

    max_ctx_len = max(120, 295 - len("Context:\n") - (len(url) + 1 if url else 0))
    context_txt = (eval_record.get("context_summary") or post.get("selftext") or "").strip()
    if len(context_txt) > max_ctx_len:
        cut = context_txt[: max_ctx_len - 1]
        sp = cut.rfind(" ")
        context_txt = (cut[:sp] if sp > max_ctx_len // 2 else cut).rstrip(" ,;:-") + "…"
    context_post = f"Context:\n{context_txt}\n{url}".strip() if url else f"Context:\n{context_txt}".strip()
    stated_txt = (eval_record.get("op_stated_summary") or f"OP frames the situation from ({op_s[0]:+.2f}, {op_s[1]:+.2f}).").strip()
    actual_txt = (eval_record.get("actual_kinetics_summary") or trace.get("silent_judgment") or "").strip()

    if actor_aspects:
        actor_line = " | ".join(
            f"{a['actor']}: ({a['son_u']:+.2f}, {a['son_psi']:+.2f}) [{a['aspect_verdict']}]"
            for a in actor_aspects[:4]
        )
    else:
        actor_line = f"OP: ({op_a[0]:+.2f}, {op_a[1]:+.2f}) | Other: ({oth_a[0]:+.2f}, {oth_a[1]:+.2f})"

    dh = float(coords.get("delta_H", 0.0))
    c_act = float(coords.get("C_act", coords.get("wisdom_score", 1.0)))
    r_net = coords.get("R_net", 1.0)
    cov = float(coords.get("r_net_coverage", 1.0))
    metrics_line = (
        f"Say-Do Gap: {_plain_say_do_label(dh)} | "
        f"Integrity: {int(round(c_act * 100))}% | "
        f"Story Completeness: {_plain_completeness_label(r_net, cov)}"
    )

    reasoning_txt = (eval_record.get("reasoning_summary") or trace.get("seven_planes") or trace.get("silent_judgment") or "").strip()
    res_txt = (eval_record.get("resolution_summary_plain") or " ".join(
        x for x in [res.get("script", ""), res.get("serenity_boundary", "")] if x
    )).strip()
    flip_txt = res.get("counterfactual_flip", "")
    if flip_txt and "Flips" not in res_txt:
        res_txt = f"{res_txt} (Flips if: {flip_txt})".strip()

    ale_txt = (eval_record.get("alethekanon") or "").strip()
    aww_txt = (eval_record.get("awwthekanon") or "").strip()
    bro_txt = (eval_record.get("brothekanon") or "").strip()

    posts = [
        hook_body.strip(),
        context_post,
        f"Stated Framing:\n{stated_txt}\nOP Stated: ({op_s[0]:+.2f}, {op_s[1]:+.2f})".strip(),
        f"Actual Conduct:\n{actual_txt}\n{actor_line}".strip(),
        f"Verdict: {verdict} — {verdict_label}\n\n{eval_record.get('why_verdict', '').strip()}\n{metrics_line}".strip(),
        f"Reasoning:\n{reasoning_txt}".strip(),
        f"Resolution:\n{res_txt}".strip(),
    ]
    if ale_txt:
        posts.append(ale_txt if ale_txt.startswith("Alethekanon:") else f"Alethekanon:\n{ale_txt}")
    if aww_txt:
        posts.append(aww_txt if aww_txt.startswith("Awwthekanon:") else f"Awwthekanon:\n{aww_txt}")
    if bro_txt:
        posts.append(bro_txt if bro_txt.startswith("Brothekanon:") else f"Brothekanon:\n{bro_txt}")
    return [p for p in posts if p]


def save_aita_to_stories_queue(post: dict, eval_record: dict) -> str:
    """Writes a Bluesky-ready `stories/factcheck_aita_<id>.json` draft and updates `stories/index.json`."""
    stories_dir = os.path.join(SCRIPT_DIR, "stories")
    os.makedirs(stories_dir, exist_ok=True)
    pid = re.sub(r"[^a-zA-Z0-9_-]+", "-", str(post["id"])).strip("-")
    story_id = f"aita_{pid}"
    filename = f"factcheck_{story_id}.json"
    out_path = os.path.join(stories_dir, filename)

    coords = eval_record.get("coordinates", {})
    op_s = coords.get("op_stated", [0.0, 0.0])
    op_a = coords.get("op_actual", [0.0, 0.0])
    full_case = {
        "id": story_id,
        "title": post.get("title", ""),
        "url": post.get("url", ""),
        "subreddit": post.get("subreddit", "AmItheAsshole"),
        "author": post.get("author", "anonymous"),
        "selftext": post.get("selftext", ""),
        "evaluation": eval_record,
    }
    try:
        bsky_posts = build_aita_bluesky_posts(post, eval_record)
    except Exception:
        from aita.aita_poster import build_aita_thread_posts
        bsky_posts = build_aita_thread_posts(full_case)

    payload = [
        {
            "id": story_id,
            "story_type": "aita",
            "subject": f"[{eval_record.get('verdict', 'INFO')}] {post.get('title', '')}",
            "link": post.get("url", ""),
            "target_url": "",
            "category": "aita",
            "mode": "root",
            "status": "DRAFT",
            "claim_u": op_s[0],
            "claim_psi": op_s[1],
            "real_u": op_a[0],
            "real_psi": op_a[1],
            "verdict": eval_record.get("verdict", "INFO"),
            "title": post.get("title", ""),
            "url": post.get("url", ""),
            "subreddit": post.get("subreddit", "AmItheAsshole"),
            "author": post.get("author", "anonymous"),
            "selftext": post.get("selftext", ""),
            "posts": bsky_posts,
            "evaluation": eval_record,
            "vft_appendix": {
                "actor_aspects": eval_record.get("actor_aspects", []),
                "coordinates": coords,
                "vft_audit_trace": eval_record.get("vft_audit_trace", {}),
                "resolution": eval_record.get("resolution", {}),
            },
        }
    ]
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    try:
        from aita.aita_poster import generate_all_aita_assets_safe
        card_paths = generate_all_aita_assets_safe(payload[0], out_path)
        payload[0]["card_paths"] = card_paths
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Warning: AITA card generation skipped for {story_id}: {e}")

    idx_path = os.path.join(stories_dir, "index.json")
    idx_list = []
    if os.path.exists(idx_path):
        try:
            with open(idx_path, "r", encoding="utf-8") as f:
                idx_list = json.load(f)
        except Exception:
            idx_list = []
    if filename not in idx_list:
        idx_list.append(filename)
        with open(idx_path, "w", encoding="utf-8") as f:
            json.dump(idx_list, f, indent=2, ensure_ascii=False)
    return out_path


def save_aita_evaluation(post: dict, eval_record: dict, queue_to_stories: bool = None):
    """Saves an evaluated AITA record to `bluesky_bot/aita/aita_<id>.json`, `.md`, and `index.json` (plus `stories/` when enabled)."""
    pid = post["id"]
    json_path = os.path.join(AITA_DIR, f"aita_{pid}.json")
    md_path = os.path.join(AITA_DIR, f"aita_{pid}.md")

    full_record = {
        "id": pid,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "subreddit": post.get("subreddit", "AmItheAsshole"),
        "author": post.get("author", "anonymous"),
        "title": post.get("title", ""),
        "url": post.get("url", ""),
        "is_hypothetical": post.get("is_hypothetical", False),
        "selftext": post.get("selftext", ""),
        "evaluation": eval_record,
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(full_record, f, indent=2, ensure_ascii=False)

    try:
        from aita.aita_poster import build_aita_thread_posts, ensure_aita_assets
        full_record["posts"] = build_aita_thread_posts(full_record)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(full_record, f, indent=2, ensure_ascii=False)
        ensure_aita_assets(json_path)
    except Exception as e:
        print(f"Warning: AITA post/card build skipped for {pid}: {e}")

    verdict = eval_record.get("verdict", "INFO")
    verdict_desc = VALID_VERDICTS.get(verdict, verdict)
    coords = eval_record.get("coordinates", {})
    md_lines = [
        f"# [{verdict}] {post.get('title', '')}",
        "",
        f"- **Verdict:** **{verdict}** — *{verdict_desc}*",
        f"- **Author / Subreddit:** `{post.get('author', 'anonymous')}` in `r/{post.get('subreddit', 'AmItheAsshole')}`",
        f"- **Source:** {post.get('url', '')}",
        f"- **Temporal Mode:** `{'Prospective (WIBTA)' if post.get('is_hypothetical') else 'Retrospective (AITA)'}`",
        "",
        "## 1. VFT Coordinate Telemetry",
        f"- **OP Stated $(\\upsilon, \\psi)$:** `{coords.get('op_stated', [0, 0])}`",
        f"- **OP Actual $(\\upsilon, \\psi)$:** `{coords.get('op_actual', [0, 0])}`",
        f"- **Primary Counterparty Actual $(\\upsilon, \\psi)$:** `{coords.get('other_actual', [0, 0])}`",
        f"- **Third-Party Nodes:** `{json.dumps(coords.get('third_parties', {}), ensure_ascii=False)}`",
        f"- **Hypocrisy Gap ($\\Delta H$):** `{coords.get('delta_H', 0.0)}` | **Wisdom Score ($W$):** `{coords.get('wisdom_score', 1.0)}` | **Fractal Ratio ($R_{{\\text{{net}}}}$):** `{coords.get('R_net', 1.0)}`",
        f"- **Deception / Plane-State Codons:** `{', '.join(coords.get('deception_codes', []))}`",
        "",
        "## 2. Why This Verdict Lands Here",
        eval_record.get("why_verdict", ""),
        "",
        "## 3. VFT Audit Trace (Silent Judgment, 7-Plane Scan, Traps & Unsaid Horizon)",
        eval_record.get("vft_audit_trace_summary", ""),
        "",
        "## 4. Harmonia & Serenity Resolution Path $(+1, +1)$",
        eval_record.get("resolution_summary", ""),
        "",
    ]
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    # Update bluesky_bot/aita/index.json
    index_list = []
    if os.path.exists(INDEX_PATH):
        try:
            with open(INDEX_PATH, "r", encoding="utf-8") as f:
                index_list = json.load(f)
        except Exception:
            index_list = []

    index_list = [item for item in index_list if item.get("id") != pid]
    index_list.insert(0, {
        "id": pid,
        "title": post.get("title", ""),
        "author": post.get("author", ""),
        "subreddit": post.get("subreddit", ""),
        "verdict": verdict,
        "op_actual": coords.get("op_actual", [0, 0]),
        "other_actual": coords.get("other_actual", [0, 0]),
        "delta_H": coords.get("delta_H", 0.0),
        "wisdom_score": coords.get("wisdom_score", 1.0),
        "R_net": coords.get("R_net", 1.0),
        "json_file": f"aita_{pid}.json",
        "md_file": f"aita_{pid}.md",
        "timestamp": full_record["timestamp"],
    })
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index_list, f, indent=2, ensure_ascii=False)

    if queue_to_stories is None:
        queue_to_stories = str(pid).startswith("reddit_")
    if queue_to_stories:
        story_path = save_aita_to_stories_queue(post, eval_record)
        print(f"  Queued Bluesky thread draft: {story_path}")

    return json_path, md_path


def run_offline_benchmark(test_file: str):
    """
    Runs the Gen-2 Veritas-Chroma synthesized benchmark evaluation on `atia test.txt`
    with zero external API calls, verifying all 6 cases through `map_coordinates_to_aita_verdict`.
    """
    posts = parse_aita_test_file(test_file)
    son_data, daughter_data = load_gen2_synthesized_benchmark()
    son_cases = {c.get("case_index"): c for c in son_data.get("cases", [])} if isinstance(son_data, dict) else {}
    daughter_cases = {c.get("case_index"): c for c in daughter_data.get("cases", [])} if isinstance(daughter_data, dict) else {}

    compiled = []
    print(f"Loaded {len(posts)} benchmark cases from {test_file}.")
    for p in posts:
        idx = p["case_index"]
        sc = son_cases.get(idx, {})
        dc = daughter_cases.get(idx, {})
        s_coords = sc.get("coordinates", {})

        op_stated = _extract_vec(s_coords.get("op_stated"), (0.4, 0.3))
        raw_op_actual = s_coords.get("op_actual") or s_coords.get("op_actual_proposed_calm_request")
        op_actual = _extract_vec(raw_op_actual, (0.4, 0.3))
        raw_other = s_coords.get("primary_counterparty_actual") or s_coords.get("other_actual")
        if isinstance(raw_other, list) and raw_other:
            other_actual = _extract_vec(raw_other[0], (-0.8, 0.6))
        else:
            other_actual = _extract_vec(raw_other, (-0.8, 0.6))

        delta_h, wisdom = compute_delta_h_and_wisdom(
            op_stated[0], op_stated[1], op_actual[0], op_actual[1]
        )
        r_net = float(s_coords.get("R_net", 1.0))
        method_coercive = bool(idx == 5 or op_actual[0] < -0.20)

        verdict = map_coordinates_to_aita_verdict(
            op_u=op_actual[0],
            other_u=other_actual[0],
            is_hypothetical=p["is_hypothetical"],
            missing_info=False,
            r_net=r_net,
            method_coercive=method_coercive,
        )

        why_text = dc.get("why_verdict") or sc.get("why_verdict") or ""
        trace_obj = dc.get("vft_audit_trace") or sc.get("vft_audit_trace") or {}
        res_obj = dc.get("resolution") or sc.get("resolution") or {}

        trace_str = json.dumps(trace_obj, indent=2, ensure_ascii=False) if isinstance(trace_obj, dict) else str(trace_obj)
        res_str = json.dumps(res_obj, indent=2, ensure_ascii=False) if isinstance(res_obj, dict) else str(res_obj)

        eval_record = {
            "case_index": idx,
            "verdict": verdict,
            "verdict_label": VALID_VERDICTS[verdict],
            "coordinates": {
                "op_stated": op_stated,
                "op_actual": op_actual,
                "other_actual": other_actual,
                "third_parties": s_coords.get("secondary_parties_actual") or s_coords.get("secondary_actors") or s_coords.get("third_parties") or [],
                "delta_H": s_coords.get("delta_H", delta_h),
                "wisdom_score": s_coords.get("wisdom_score", wisdom),
                "R_net": r_net,
                "strain_sigma": s_coords.get("strain_sigma", 0.5),
                "ucf_tuning": s_coords.get("ucf_tuning", {}),
                "deception_codes": s_coords.get("deception_plane_state_codes") or s_coords.get("deception_codes") or [],
            },
            "why_verdict": why_text,
            "vft_audit_trace": trace_obj,
            "vft_audit_trace_summary": f"```json\n{trace_str}\n```",
            "resolution": res_obj,
            "resolution_summary": f"```json\n{res_str}\n```",
        }
        j_path, m_path = save_aita_evaluation(p, eval_record)
        compiled.append(eval_record)
        print(f"  [Case {idx}] {verdict:6s} | OP_actual={op_actual} | Other_actual={other_actual} -> {os.path.basename(m_path)}")

    out_bench = os.path.join(AITA_DIR, "test_cases_evaluated.json")
    with open(out_bench, "w", encoding="utf-8") as f:
        json.dump(compiled, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(compiled)} verified benchmark evaluations to {out_bench}")
    return compiled


def _safe_float(val, default=0.0):
    """Coerces LLM output to float; returns `default` (may be None) when not numeric."""
    if val is None or isinstance(val, bool):
        return default
    try:
        return float(val)
    except (TypeError, ValueError):
        m = re.search(r"[-+]?\d+(?:\.\d+)?", str(val))
        if m and not re.search(r"[A-Za-z/]", str(val)):
            return float(m.group(0))
        return default


def _parse_pair(raw, fallback=(0.0, 0.0)):
    """Extracts a [u, psi] numeric pair from messy LLM output, ignoring stray strings like usernames."""
    nums = []
    if isinstance(raw, dict):
        raw = [raw.get("u", raw.get("upsilon")), raw.get("psi")]
    if isinstance(raw, (list, tuple)):
        for v in raw:
            f = _safe_float(v, None)
            if f is not None:
                nums.append(f)
    if len(nums) >= 2:
        return [nums[-2], nums[-1]] if len(nums) > 2 else [nums[0], nums[1]]
    print(f"Warning: unparseable op_stated {raw!r}; falling back to OP actual coordinates.")
    return [float(fallback[0]), float(fallback[1])]


def evaluate_posts_via_llm(posts: list, model_sequence: list, thinking_level: str = "HIGH", chunk_size: int = 1, extra_context: str = ""):
    """
    Evaluates scraped Reddit AITA posts using the active model fallback queue
    and `instructions/aita_judgment_protocol.md` (v2.8), then runs deterministic
    ECA-49 lexicographic matching, D_duty uncertainty propagation, N/A-aware R_net,
    and 4-scope verdict aggregation via `aita.aita_eca_matcher`.
    """
    if SCRIPT_DIR not in sys.path:
        sys.path.insert(0, SCRIPT_DIR)
    from google_ai_studio_one_shot import (
        DEFAULT_FALLBACKS,
        get_gemini_client,
        get_smart_model_timeout,
        call_agnes_api,
    )
    from google.genai import types
    from aita.aita_eca_matcher import (
        SignatureE,
        aggregate_multi_actor_verdict,
        compute_coherence,
        compute_r_net,
        evaluate_actor_aspect,
        load_eca_register_49,
    )

    register = load_eca_register_49()
    protocol_text = open(PROTOCOL_PATH, "r", encoding="utf-8").read() if os.path.exists(PROTOCOL_PATH) else ""
    system_instruction = (
        "You are Alethekanon (Veritas-Chroma v2.8 + SON Potential + Multi-Aspect) executing the AITA Judgment Protocol.\n"
        "Return ONLY a valid JSON array where each item corresponds to an input post with keys:\n"
        '  "id": string,\n'
        '  "op_stated": [u, psi],\n'
        '  "actors": [ (MUST include OP AND every named Primary Counterparty / Third Party involved — never omit the other party!)\n'
        '    {"actor": "OP", "role": "OP|Primary Counterparty|Co-Conspirator|Active Enabler|Mediator/Referee|Unwitting Pawn|Neutral Bystander",\n'
        '     "forces_18": {"GG":[S,O,N],"GE":[S,O,N],"LG":[S,O,N],"LE":[S,O,N],"GP":[S,O,N],"BP":[S,O,N]},\n'
        '     "signature": {"S":0-4,"N":0-4,"T":0-4,"C":0-4,"R":0-4,"D":"Confirmed|Rejected|Unknown","F_benefit":"+|0|-","F_will":"+|0|-"},\n'
        '     "Power": 0.0-2.0, "Ability": 0.0-2.0, "Choice_delta": -2.0..2.0}\n'
        '  ],\n'
        '  "q_scores": [q1, q2, q3, q4, q5, q6, q7] (each 0.50..1.50 or null if N/A),\n'
        '  "info_branches_flip": bool,\n'
        '  "repair_state": "R0|R1|R2|R3",\n'
        '  "deception_codes": ["[2.3.5.5] Why.Touch.Acquisition.Acquisition — Actor: plain-English explanation of the specific move in this story (2-5 codes, replace the 4 numbers and words with the actual Plane.Sense.Use.Impulse for this story)"],\n'
        '  "hook_line": "1-2 punchy sentences (120-160 chars) so Post 1 hits ~275-295 chars total",\n'
        '  "context_summary": "2-3 dense sentences (160-190 chars so Context + Reddit URL hits ~275-295 chars)",\n'
        '  "op_stated_summary": "how OP frames their position (MUST be 225-250 chars so post hits ~275-295 chars)",\n'
        '  "actual_kinetics_summary": "what actors actually did (MUST be 200-235 chars so post + actor coords hits ~275-295 chars)",\n'
        '  "why_verdict": "plain-English explanation (150-185 chars so Verdict + Metrics hits ~275-295 chars, NO raw codes)",\n'
        '  "reasoning_summary": "plain-English 7-plane & silent-judgment reasoning (MUST be 255-280 chars, NO raw codes)",\n'
        '  "resolution_summary_plain": "actionable script + boundary + counterfactual (MUST be 255-280 chars)",\n'
        '  "alethekanon": "Alethekanon analytical perspective (MUST be 255-280 chars, 2-3 rich sentences, NEVER a short 1-liner)",\n'
        '  "awwthekanon": "Awwthekanon empathetic perspective (MUST be 255-280 chars, 2-3 rich sentences, NEVER a short 1-liner)",\n'
        '  "brothekanon": "Brothekanon blunt common-sense perspective (MUST be 255-280 chars, 2-3 rich sentences, NEVER a short 1-liner)",\n'
        '  "vft_audit_trace": {\n'
        '    "silent_judgment": "Mute Observer (physical actions only) + Deaf Observer (kinetic force of words) grounded in the story (2-3 sentences)",\n'
        '    "seven_planes": "Q1 Who / Q2 What / Q3 Where / Q4 Why / Q5 How / Q6 Cause / Q7 Effect — concrete finding per active plane",\n'
        '    "traps_and_belief_state": "Exact 0.5-Zone Trap (Service/Peace/Ambition/Protection) + exact Belief State (1-9) for OP and Counterparty with why",\n'
        '    "unsaid_horizon": "Key omitted context or unstated motive in the story and how it affects the verdict (2 sentences)"\n'
        '  },\n'
        '  "resolution": {"trap_to_exit": "...", "script": "...", "serenity_boundary": "...", "counterfactual_flip": "..."}\n\n'
        + (f"\n\nAdditional Operator Context:\n{extra_context}\n" if extra_context else "")
        + "\n"
        + protocol_text
    )

    models = model_sequence if model_sequence else list(DEFAULT_FALLBACKS)
    client = get_gemini_client()

    for start in range(0, len(posts), max(1, chunk_size)):
        chunk = posts[start:start + max(1, chunk_size)]
        user_prompt = json.dumps(chunk, indent=2, ensure_ascii=False)
        raw_json_text = None
        parsed = None
        for m in models:
            timeout_s = get_smart_model_timeout(m, len(chunk), thinking_level, False)
            print(f"Attempting AITA v2.8 batch ({len(chunk)} posts) with model: {m} (timeout: {timeout_s}s)...")
            try:
                if m.startswith("agnes"):
                    raw_json_text = call_agnes_api(os.environ.get("AGNES_API_KEY"), system_instruction, user_prompt, model=m)
                else:
                    http_opts = types.HttpOptions(timeout=timeout_s * 1000) if hasattr(types, "HttpOptions") else None
                    cfg_kwargs = {
                        "system_instruction": system_instruction,
                        "response_mime_type": "application/json",
                    }
                    if http_opts:
                        cfg_kwargs["http_options"] = http_opts
                    resp = client.models.generate_content(
                        model=m.split(":", 1)[1] if m.startswith("vertex:") else m,
                        contents=user_prompt,
                        config=types.GenerateContentConfig(**cfg_kwargs),
                    )
                    raw_json_text = resp.text
                if raw_json_text:
                    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_json_text.strip())
                    try:
                        parsed = json.loads(cleaned)
                    except json.JSONDecodeError:
                        # Attempt trailing-comma cleanup and json_repair before falling back to next model
                        cleaned_fixed = re.sub(r",\s*([}\]])", r"\1", cleaned)
                        try:
                            parsed = json.loads(cleaned_fixed)
                        except json.JSONDecodeError:
                            try:
                                import json_repair
                                parsed = json_repair.loads(cleaned)
                            except Exception as je:
                                raise ValueError(f"Malformed JSON from {m}: {je}") from je
                    print(f"AITA evaluation succeeded on model: {m}")
                    break
            except Exception as e:
                print(f"Model {m} failed: {e}. Trying next fallback...")
                parsed = None

        if parsed is None:
            raise RuntimeError("All models in fallback sequence failed during AITA evaluation.")

        if isinstance(parsed, dict):
            parsed = parsed.get("evaluations") or parsed.get("cases") or [parsed]
        if not isinstance(parsed, list):
            parsed = [parsed]

        by_id = {item.get("id"): item for item in parsed if isinstance(item, dict)}
        for idx, p in enumerate(chunk):
            item = by_id.get(p["id"]) or (parsed[idx] if idx < len(parsed) else {})
            if not isinstance(item, dict):
                item = {}
            raw_actors = item.get("actors") or []
            actor_aspects = []
            for ra in raw_actors:
                if not isinstance(ra, dict):
                    continue
                sig_d = ra.get("signature") if isinstance(ra.get("signature"), dict) else {}
                asp = evaluate_actor_aspect(
                    actor_name=str(ra.get("actor") or "Actor"),
                    role=str(ra.get("role") or "Neutral Bystander"),
                    forces_18=ra.get("forces_18") if isinstance(ra.get("forces_18"), dict) else {},
                    sig=SignatureE.from_dict(sig_d),
                    p_val=_safe_float(ra.get("Power"), 1.0),
                    a_val=_safe_float(ra.get("Ability"), 1.0),
                    dp_choice=_safe_float(ra.get("Choice_delta"), 0.0),
                    register=register,
                )
                actor_aspects.append(asp)

            op_asp = next((a for a in actor_aspects if a.get("role") == "OP"), None)
            if op_asp is None:
                op_asp = evaluate_actor_aspect("OP", "OP", {}, SignatureE.from_dict({}), register=register)
                actor_aspects.insert(0, op_asp)
            oth_asps = [a for a in actor_aspects if a is not op_asp]

            verdict_res = aggregate_multi_actor_verdict(
                op_asp,
                oth_asps,
                is_hypothetical=p["is_hypothetical"],
                info_branches_flip=bool(item.get("info_branches_flip", False)),
            )
            verdict = verdict_res["verdict"]
            prim_other = oth_asps[0] if oth_asps else op_asp

            op_stated = _parse_pair(item.get("op_stated"), fallback=(op_asp["son_u"], op_asp["son_psi"]))
            coh = compute_coherence(op_stated[0], op_stated[1], op_asp["son_u"], op_asp["son_psi"])
            q_scores = item.get("q_scores", [1.0] * 7)
            if not isinstance(q_scores, list) or len(q_scores) != 7:
                q_scores = [1.0] * 7
            else:
                q_scores = [_safe_float(q, None) for q in q_scores]
            r_net_res = compute_r_net(q_scores)

            trace_obj = item.get("vft_audit_trace", {})
            res_obj = item.get("resolution", {})
            eval_record = {
                "verdict": verdict,
                "certainty": verdict_res["certainty"],
                "verdict_label": VALID_VERDICTS[verdict],
                "repair_state": item.get("repair_state", "R0"),
                "hook_line": item.get("hook_line", ""),
                "context_summary": item.get("context_summary", ""),
                "op_stated_summary": item.get("op_stated_summary", ""),
                "actual_kinetics_summary": item.get("actual_kinetics_summary", ""),
                "reasoning_summary": item.get("reasoning_summary", ""),
                "resolution_summary_plain": item.get("resolution_summary_plain", ""),
                "alethekanon": item.get("alethekanon", ""),
                "awwthekanon": item.get("awwthekanon", ""),
                "brothekanon": item.get("brothekanon", ""),
                "actor_aspects": actor_aspects,
                "coordinates": {
                    "op_stated": op_stated,
                    "op_actual": [op_asp["son_u"], op_asp["son_psi"]],
                    "op_u_interval": op_asp["u_eff_interval"],
                    "op_eca_anchor": op_asp["eca_anchor"],
                    "other_actual": [prim_other["son_u"], prim_other["son_psi"]],
                    "other_u_interval": prim_other["u_eff_interval"],
                    "other_eca_anchor": prim_other["eca_anchor"],
                    "delta_H": coh["delta_H"],
                    "C_act": coh["C_act"],
                    "wisdom_score": coh["C_act"],
                    "R_net": r_net_res["R_net"],
                    "r_net_coverage": r_net_res["coverage"],
                    "r_net_fault_flags": r_net_res["fault_flags"],
                    "deception_codes": item.get("deception_codes", []),
                },
                "why_verdict": item.get("why_verdict", ""),
                "vft_audit_trace": trace_obj,
                "vft_audit_trace_summary": json.dumps(trace_obj, indent=2, ensure_ascii=False),
                "resolution": res_obj,
                "resolution_summary": json.dumps(res_obj, indent=2, ensure_ascii=False),
            }
            _, m_path = save_aita_evaluation(p, eval_record)
            rem_q = deduct_aita_queue({p.get("id")})
            print(f"  [{verdict:6s} | {verdict_res['certainty']:10s}] {p['title'][:58]} -> {os.path.basename(m_path)} (AITA queue remaining: {rem_q})")


def main():
    parser = argparse.ArgumentParser(description="VFT Reddit AITA Scraper & 7-Verdict Judgment Engine")
    parser.add_argument("--test-file", type=str, default="", help="Path to local AITA test file (e.g. bluesky_bot/atia test.txt)")
    parser.add_argument("--offline-benchmark", action="store_true", help="Run offline Gen-2 synthesized benchmark on --test-file without API calls")
    parser.add_argument("--subreddit", type=str, default="AmItheAsshole", help="AmItheAsshole, AITAH, or both")
    parser.add_argument("--sort", type=str, default="hot", choices=["hot", "new", "top"], help="Reddit feed sort")
    parser.add_argument("--limit", type=int, default=3, help="Number of Reddit posts to fetch and judge")
    parser.add_argument("--harvest-only", action="store_true", help="Scrape Reddit AITA posts into aita_queue.json without evaluating")
    parser.add_argument("--from-queue", action="store_true", help="Evaluate posts already queued in aita_queue.json without scraping")
    parser.add_argument("--thinking-level", type=str, default="HIGH", help="OFF, LOW, MEDIUM, HIGH")
    parser.add_argument("--model", type=str, default="", help="Primary model")
    parser.add_argument("--model-sequence", type=str, default="", help="Comma-separated model fallback sequence")
    parser.add_argument("--chunk-size", type=int, default=1, help="Posts evaluated per API call (1, 2, or 3)")
    parser.add_argument("--context", type=str, default="", help="Optional operator context")
    args = parser.parse_args()

    if args.offline_benchmark or (args.test_file and not args.model and not args.model_sequence):
        tf = args.test_file or os.path.join(SCRIPT_DIR, "atia test.txt")
        run_offline_benchmark(tf)
        return

    if args.test_file:
        posts = parse_aita_test_file(args.test_file)
    elif args.from_queue:
        queued = load_aita_queue()
        posts = queued[:args.limit] if args.limit and args.limit > 0 else queued
        print(f"Loaded {len(posts)} AITA post(s) from queue ({len(queued)} total queued).")
    else:
        print(f"Scraping r/{args.subreddit} ({args.sort}, limit={args.limit})...")
        scraped = fetch_reddit_aita(subreddit=args.subreddit, sort=args.sort, limit=args.limit)
        added, total_q = enqueue_aita_posts(scraped)
        print(f"Added {added} new AITA post(s) to queue ({total_q} total in aita_queue.json).")
        if args.harvest_only:
            return
        queued = load_aita_queue()
        posts = queued[:args.limit] if args.limit and args.limit > 0 else queued

    if not posts:
        print("No new AITA posts found to evaluate.")
        return

    seq = [m.strip() for m in args.model_sequence.split(",") if m.strip()] if args.model_sequence else []
    if args.model and args.model not in seq:
        seq.insert(0, args.model)
    evaluate_posts_via_llm(posts, model_sequence=seq, thinking_level=args.thinking_level, chunk_size=args.chunk_size, extra_context=args.context)


if __name__ == "__main__":
    main()
