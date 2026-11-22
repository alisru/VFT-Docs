import os
import sys
import io
import json
import time
import argparse
from PIL import Image

_AITA_DIR = os.path.dirname(os.path.abspath(__file__))
_BOT_DIR = os.path.dirname(_AITA_DIR)
if _BOT_DIR not in sys.path:
    sys.path.insert(0, _BOT_DIR)
if _AITA_DIR not in sys.path:
    sys.path.insert(0, _AITA_DIR)

from aita_card_generator import generate_all_aita_assets
from aita_explainer_cards import generate_deception_and_metrics_explainer_card


def _fit_bsky(text, limit=295):
    text = " ".join(str(text).split()) if "\n" not in str(text) else str(text).strip()
    if len(text) <= limit:
        return text
    cut = text[: limit - 1]
    last_space = cut.rfind(" ")
    if last_space > limit // 2:
        cut = cut[:last_space]
    return cut.rstrip(" ,;:-") + "…"


def build_aita_thread_posts(case_data):
    """Builds the canonical 10-post Bluesky thread (1/10..10/10) per aita_thread_formatting.md."""
    existing = case_data.get("posts")
    if isinstance(existing, list) and len(existing) >= 10:
        return existing

    title = case_data.get("title", "AITA Case").strip()
    url = case_data.get("url", "").strip()
    selftext = case_data.get("selftext", "").strip()
    ev = case_data.get("evaluation", {})
    verdict = ev.get("verdict", "INFO")
    verdict_label = ev.get("verdict_label", verdict)
    coords = ev.get("coordinates", {})
    op_s = coords.get("op_stated", [0.0, 0.0])
    op_a = coords.get("op_actual", [0.0, 0.0])
    oth_a = coords.get("other_actual", [0.0, 0.0])
    third_parties = coords.get("third_parties", [])
    delta_h = float(coords.get("delta_H", 0.0))
    wisdom = float(coords.get("wisdom_score", 0.5))
    r_net = float(coords.get("R_net", 1.0))
    why_verdict = ev.get("why_verdict", "").strip()
    trace = ev.get("vft_audit_trace", {})
    res = ev.get("resolution", {})

    def _tag(u):
        return "PASS" if float(u) >= -0.20 else "FAIL"

    # 1/10 — Hook (all 4 images attached here)
    hook_line = why_verdict.split(".")[0].strip() + "." if "." in why_verdict else why_verdict
    p1 = f'⚖️ AITA Verdict: {verdict} — "{title}"\n{hook_line}\n#AITA #Aletheia'
    if len(p1) > 295:
        short_title = _fit_bsky(title, 110)
        short_hook = _fit_bsky(hook_line, 130)
        p1 = f'⚖️ AITA Verdict: {verdict} — "{short_title}"\n{short_hook}\n#AITA #Aletheia'

    # 2/10 — Context + Link
    ctx_body = _fit_bsky(selftext, max(120, 280 - len(url) - 12))
    p2 = f"Context:\n{ctx_body}\n{url}" if url else f"Context:\n{ctx_body}"

    # 3/10 — OP Stated Framing
    stated_line = f"OP Stated: ({float(op_s[0]):+.2f}, {float(op_s[1]):+.2f})"
    p3_body = _fit_bsky(trace.get("zero_point_five_zone_traps", why_verdict), 285 - len(stated_line) - 18)
    p3 = f"Stated Framing:\n{p3_body}\n{stated_line}"

    # 4/10 — Actual Conduct (Multi-Actor)
    actors_summary = [
        f"OP: ({float(op_a[0]):+.2f}, {float(op_a[1]):+.2f}) [{_tag(op_a[0])}]",
        f"Other: ({float(oth_a[0]):+.2f}, {float(oth_a[1]):+.2f}) [{_tag(oth_a[0])}]",
    ]
    for tp in third_parties[:2]:
        tname = tp.get("actor", "3rd").split("(")[0].strip()
        actors_summary.append(f"{tname}: ({float(tp.get('upsilon', 0)):+.2f}, {float(tp.get('psi', 0)):+.2f}) [{_tag(tp.get('upsilon', 0))}]")
    actors_line = " | ".join(actors_summary)
    silent_raw = trace.get("silent_judgment", why_verdict)
    p4_body = _fit_bsky(silent_raw, max(80, 285 - len(actors_line) - 18))
    p4 = f"Actual Conduct:\n{p4_body}\n{actors_line}"

    # 5/10 — Verdict & Plain-English Integrity
    gap_word = "Low" if delta_h < 0.6 else ("Moderate" if delta_h < 1.0 else "High")
    comp_word = "Solid" if r_net >= 0.95 else ("Partial" if r_net >= 0.7 else "Thin")
    metrics_line = f"Say-Do Gap: {gap_word} ({delta_h:.2f}) | Integrity: {round(wisdom * 100)}% | Story Completeness: {comp_word} (R_net {r_net:.2f})"
    v_hdr = f"Verdict: {verdict} — {verdict_label}"
    p5_why = _fit_bsky(why_verdict, max(70, 290 - len(v_hdr) - len(metrics_line) - 4))
    p5 = f"{v_hdr}\n{p5_why}\n{metrics_line}"

    # 6/10 — Reasoning
    reasoning_src = trace.get("unsaid_horizon_and_multi_actor_graph") or why_verdict
    p6 = f"Reasoning:\n{_fit_bsky(reasoning_src, 280)}"

    # 7/10 — Resolution (+1, +1)
    script = res.get("verbatim_script", "").strip()
    patch = res.get("structural_patch", "").strip()
    flip = res.get("counterfactual_flip_thresholds", "").strip()
    res_raw = f'"{script}" {patch}' if script else patch
    if flip:
        res_raw += f" ({flip})"
    p7 = f"Resolution:\n{_fit_bsky(res_raw, 280)}"

    # 8/10, 9/10, 10/10 — Alethekanon, Awwthekanon, Brothekanon
    seven = trace.get("seven_plane_scan", {})
    ale_src = seven.get("Q5_How") or seven.get("Q1_Who") or why_verdict
    aww_src = seven.get("Q7_Effect") or trace.get("zero_point_five_zone_traps") or patch
    bro_src = f"{why_verdict} {patch}".strip()

    p8 = f"Alethekanon:\n{_fit_bsky(ale_src, 278)}"
    p9 = f"Awwthekanon:\n{_fit_bsky(aww_src, 278)}"
    p10 = f"Brothekanon:\n{_fit_bsky(bro_src, 278)}"

    return [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]


def ensure_aita_assets(case_json_path):
    """Ensures all 4 images (story, graph, appendix, explainer) exist for an AITA case."""
    cards_dir = os.path.join(_AITA_DIR, "cards")
    os.makedirs(cards_dir, exist_ok=True)
    story_png, appendix_png, graph_png = generate_all_aita_assets(case_json_path, cards_dir)
    explainer_png = os.path.join(cards_dir, "vft_explainer_deception_traps_card.png")
    if not os.path.exists(explainer_png):
        generate_deception_and_metrics_explainer_card(explainer_png)
    return [story_png, graph_png, appendix_png, explainer_png]


def export_aita_to_stories_queue(case_json_path):
    """Exports an evaluated AITA case into bluesky_bot/stories/aita_<id>.json so it joins the main posting queue."""
    with open(case_json_path, "r", encoding="utf-8") as f:
        case_data = json.load(f)

    posts = build_aita_thread_posts(case_data)
    img_paths = ensure_aita_assets(case_json_path)

    ev = case_data.get("evaluation", {})
    coords = ev.get("coordinates", {})
    op_s = coords.get("op_stated", [0.0, 0.0])
    op_a = coords.get("op_actual", [0.0, 0.0])
    pid = case_data.get("id") or os.path.splitext(os.path.basename(case_json_path))[0]
    if not pid.startswith("aita_"):
        pid = f"aita_{pid}"

    stories_dir = os.path.join(_BOT_DIR, "stories")
    os.makedirs(stories_dir, exist_ok=True)
    out_path = os.path.join(stories_dir, f"{pid}.json")

    queue_payload = {
        "story_type": "aita",
        "subject": case_data.get("title", "AITA Case"),
        "link": case_data.get("url", ""),
        "claim_u": float(op_s[0]),
        "claim_psi": float(op_s[1]),
        "real_u": float(op_a[0]),
        "real_psi": float(op_a[1]),
        "mode": "root",
        "posts": posts,
        "card_paths": img_paths,
        "status": case_data.get("status", "DRAFT"),
        "id": pid,
        "title": case_data.get("title", ""),
        "url": case_data.get("url", ""),
        "subreddit": case_data.get("subreddit", "AmItheAsshole"),
        "author": case_data.get("author", "anonymous"),
        "selftext": case_data.get("selftext", ""),
        "evaluation": ev,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(queue_payload, f, indent=2, ensure_ascii=False)
    print(f"Queued AITA story for posting: {out_path}")
    return out_path


def _encode_for_bsky(img_path, max_bytes=950_000):
    """Reads image bytes, converting/downscaling cleanly if larger than Bluesky's 1MB blob cap."""
    with open(img_path, "rb") as f:
        raw = f.read()
    if len(raw) <= max_bytes:
        return raw
    im = Image.open(img_path).convert("RGB")
    quality = 90
    while quality >= 65:
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=quality, optimize=True)
        data = buf.getvalue()
        if len(data) <= max_bytes:
            return data
        quality -= 10
    im.thumbnail((1200, 1800), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=75, optimize=True)
    return buf.getvalue()


def _load_env():
    env_path = os.path.join(_BOT_DIR, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def generate_all_aita_assets_safe(case_data, case_json_path):
    cards_dir = os.path.join(_AITA_DIR, "cards")
    os.makedirs(cards_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(case_json_path))[0]
    from aita_card_generator import generate_aita_story_card, generate_aita_appendix_card
    from aita_graph_generator import generate_aita_graph
    story_png = os.path.join(cards_dir, f"{base_name}_story_card.png")
    appendix_png = os.path.join(cards_dir, f"{base_name}_appendix_card.png")
    graph_png = os.path.join(cards_dir, f"{base_name}_graph.png")
    generate_aita_story_card(case_data, story_png)
    generate_aita_appendix_card(case_data, appendix_png)
    generate_aita_graph(case_data, graph_png)
    explainer_png = os.path.join(cards_dir, "vft_explainer_deception_traps_card.png")
    if not os.path.exists(explainer_png):
        generate_deception_and_metrics_explainer_card(explainer_png)
    return [story_png, graph_png, appendix_png, explainer_png]


def post_aita_to_bluesky(case_json_path, dry_run=False):
    """Builds 10-post thread + 4 images and posts via aletheia_bot.post_thread()."""
    with open(case_json_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    is_list = isinstance(raw_data, list)
    case_data = raw_data[0] if is_list else raw_data

    posts = build_aita_thread_posts(case_data)
    case_data["posts"] = posts
    saved_cards = case_data.get("card_paths")
    if isinstance(saved_cards, list) and len(saved_cards) == 4 and all(os.path.exists(p) for p in saved_cards):
        img_paths = saved_cards
    else:
        img_paths = generate_all_aita_assets_safe(case_data, case_json_path)
        case_data["card_paths"] = img_paths
    case_data.setdefault("story_type", "aita")
    case_data.setdefault("category", "aita")
    case_data.setdefault("subject", case_data.get("title", "AITA Case"))
    case_data.setdefault("link", case_data.get("url", ""))
    case_data.setdefault("mode", "root")

    client = None
    if not dry_run:
        _load_env()
        handle = os.environ.get("BSKY_HANDLE", "judgement-bot.bsky.social")
        password = os.environ.get("BSKY_PASSWORD")
        if not password:
            raise RuntimeError("BSKY_PASSWORD not found in bluesky_bot/.env")
        from atproto import Client
        client = Client()
        client.login(handle, password)

    from aletheia_bot import post_thread
    post_thread(client, case_data, live=not dry_run)

    with open(case_json_path, "w", encoding="utf-8") as f:
        json.dump([case_data] if is_list else case_data, f, indent=2, ensure_ascii=False)
    return case_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build & post 10-post AITA thread with 4 cards to Bluesky.")
    parser.add_argument("case_json", help="Path to evaluated AITA JSON file")
    parser.add_argument("--dry-run", action="store_true", help="Build posts & 4 cards without posting live")
    args = parser.parse_args()
    post_aita_to_bluesky(args.case_json, dry_run=args.dry_run)
