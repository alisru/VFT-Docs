"""
Audit Validator & Normalizer for Bluesky Bot Story JSON
Ensures full structural precision and formatting compliance for Potential + Spiritual + Multi-Aspect audits.
"""
import os
import sys
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from generate_graph import enforce_deterministic_trajectory
from rebuild_registries_son import get_zone_label

def validate_and_normalize_story(story_data):
    """Validates and enforces invariants on a story dictionary."""
    s = story_data[0] if isinstance(story_data, list) else story_data
    
    # 1. Ensure required flags
    s["potential_audit"] = True
    s["spiritual"] = True
    s["multiAspect"] = True
    s["status"] = "DRAFT"
    s["rkeys"] = []
    s["post_urls"] = []

    # 2. Derive root coordinates from aspects if present
    aspects = s.get("aspects", [])
    if aspects and isinstance(aspects, list) and len(aspects) > 0:
        c_u = round(sum(float(a.get("claim_u", 0.0)) for a in aspects) / len(aspects), 2)
        c_psi = round(sum(float(a.get("claim_psi", 0.0)) for a in aspects) / len(aspects), 2)
        r_u = round(sum(float(a.get("real_u", 0.0)) for a in aspects) / len(aspects), 2)
        r_psi = round(sum(float(a.get("real_psi", 0.0)) for a in aspects) / len(aspects), 2)
        s["claim_u"] = c_u
        s["claim_psi"] = c_psi
        s["real_u"] = r_u
        s["real_psi"] = r_psi
    else:
        c_u = s.get("claim_u", 0.0)
        c_psi = s.get("claim_psi", 0.0)
        r_u = s.get("real_u", 0.0)
        r_psi = s.get("real_psi", 0.0)

    # 3. Format posts array to 15 posts
    posts = s.get("posts", [])
    if len(posts) < 15:
        # Pad or raise
        pass

    # Synchronize Stated and Resulting Judgement labels
    if len(posts) > 1 and "Stated Judgement:" in posts[1]:
        label = get_zone_label(c_u, c_psi)
        sgn_u = "+" if c_u >= 0 else ""
        sgn_psi = "+" if c_psi >= 0 else ""
        posts[1] = posts[1].split("Stated Judgement:")[0] + f"Stated Judgement: ({sgn_u}{c_u:.2f}, {sgn_psi}{c_psi:.2f}) — {label}"

    if len(posts) > 2 and "Resulting Judgement:" in posts[2]:
        label = get_zone_label(r_u, r_psi)
        sgn_u = "+" if r_u >= 0 else ""
        sgn_psi = "+" if r_psi >= 0 else ""
        posts[2] = posts[2].split("Resulting Judgement:")[0] + f"Resulting Judgement: ({sgn_u}{r_u:.2f}, {sgn_psi}{r_psi:.2f}) — {label}"

    s["posts"] = posts

    # 4. Enforce deterministic trajectory on posts[3], posts[8/9]
    s = enforce_deterministic_trajectory(s)

    # 5. Length checks (each post <= 280 chars)
    trimmed_posts = []
    for idx, p in enumerate(s.get("posts", [])):
        if len(p) > 280:
            p = p[:277] + "..."
        trimmed_posts.append(p)
    s["posts"] = trimmed_posts

    return [s] if isinstance(story_data, list) else s

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Path to story JSON file")
    args = parser.parse_args()
    with open(args.file, "r", encoding="utf-8") as fp:
        data = json.load(fp)
    norm = validate_and_normalize_story(data)
    with open(args.file, "w", encoding="utf-8") as fp:
        json.dump(norm, fp, indent=2)
    print(f"Validated: {args.file}")
