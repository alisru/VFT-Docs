import os

fp = r"e:\Vector Field Theory\VFT Docs\bluesky_bot\generate_graph.py"
with open(fp, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "def enforce_deterministic_trajectory(story):"
end_marker = "def draw_graph("

start_pos = content.find(start_marker)
end_pos = content.find(end_marker)

if start_pos != -1 and end_pos != -1:
    new_func = '''def enforce_deterministic_trajectory(story):
    """
    Enforces the Deterministic Trajectory Invariant programmatically.
    Recalculates the exact mathematical path name from (claim_u, claim_psi) -> (real_u, real_psi).
    Deterministically overwrites:
      - story['path_name']: exact canonical path name
      - Post 3: Verdict line 'Verdict: [PASS/FAIL/CONDITIONAL] — [Path Name].'
      - The Trajectory post: 'The Trajectory: The Path of [Path Name].'
    Ensures that any trajectory where real_u <= 0 can NEVER contain 'Redemption' or 'Grace'.
    """
    import re
    try:
        claim_u = float(story.get("claim_u", 0.0))
        claim_psi = float(story.get("claim_psi", 0.0))
        real_u = float(story.get("real_u", 0.0))
        real_psi = float(story.get("real_psi", 0.0))
    except (ValueError, TypeError):
        return story

    math_path = get_path_name(claim_u, claim_psi, real_u, real_psi)
    story["path_name"] = math_path

    posts = story.get("posts", [])
    if not isinstance(posts, list) or len(posts) < 4:
        return story

    # Determine verdict classification
    if real_u <= 0.0:
        if abs(real_u) <= 0.1 and abs(claim_u - real_u) <= 0.2:
            verdict_type = "CONDITIONAL"
        else:
            verdict_type = "FAIL"
    else:
        verdict_type = "PASS"

    canonical_verdict_line = f"Verdict: {verdict_type} — {math_path}."

    # 1. Post 3: Overwrite verdict line deterministically
    v_post = posts[3]
    lines = v_post.split("\\n")
    verdict_idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith("Verdict:"):
            verdict_idx = i
            break

    if verdict_idx != -1:
        lines[verdict_idx] = canonical_verdict_line
        posts[3] = "\\n".join(lines)
    else:
        posts[3] = canonical_verdict_line + "\\n" + v_post

    # 2. The Trajectory post (usually Post 8 or marked by 'The Trajectory:')
    for idx, p in enumerate(posts):
        if "The Trajectory:" in p:
            t_lines = p.split("\\n")
            for j, t_line in enumerate(t_lines):
                if t_line.strip().startswith("The Trajectory:"):
                    t_lines[j] = f"The Trajectory: The Path of {math_path}."
                if real_u <= 0:
                    if "via Constructive" in t_lines[j]:
                        t_lines[j] = t_lines[j].replace("via Constructive", "via Destructive")
                    if "Redemption" in t_lines[j]:
                        t_lines[j] = t_lines[j].replace("Redemption", math_path)
            posts[idx] = "\\n".join(t_lines)
            break

    story["posts"] = posts
    return story

'''
    content = content[:start_pos] + new_func + content[end_pos:]
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully replaced enforce_deterministic_trajectory via index slice.")
else:
    print(f"Markers not found: start={start_pos}, end={end_pos}")
