import re

path = 'bluesky_bot/google_ai_studio_one_shot.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Post 5 invariant in build_formatting_rules
old_p5 = """            "- Post 5 (index 4 in the posts array: Source Quality Scorecard / Sub-Audits Breakdown) is the dedicated aspect & source breakdown. Format DIRECTLY as concise bullet points (NO header prefix). Each bullet must be 1 short line under 60 chars:\\n"
            "  - [Outlet / Aspect A]: [PASS/FAIL/COND] ([real_u], [real_psi]) — [Brief 1-line framing/omission reason under 60 chars].\\n"
            "  - [Outlet / Aspect B]: [PASS/FAIL/COND] ([real_u], [real_psi]) — [Brief 1-line framing/omission reason under 60 chars].\\n"
            "  *Note: If the story contains multiple reporting sources in the dossier, evaluate each news outlet's editorial integrity and framing bias as individual aspects. Keep the ENTIRE combined Post 5 strictly under 260 characters total.\\n\""""

new_p5 = """            "- Post 5 (index 4 in the posts array: Source Quality Scorecard / Sub-Audits Breakdown) is the dedicated aspect & source breakdown. Format DIRECTLY as concise bullet points (NO header prefix). Each bullet must be 1 short line under 60 chars:\\n"
            "  - [Outlet / Aspect A]: [PASS/FAIL/COND] ([real_u], [real_psi]) — [Brief 1-line framing/omission reason under 60 chars].\\n"
            "  - [Outlet / Aspect B]: [PASS/FAIL/COND] ([real_u], [real_psi]) — [Brief 1-line framing/omission reason under 60 chars].\\n"
            "  *CRITICAL INVARIANT: Every single sub-audit bullet in Post 5 MUST match an entity declared in item[11] (the actors array). NEVER invent floating abstract categories (e.g. 'Corporate Workplace Claims' or 'Managerial Accounts'). Score the actual declared actors (e.g. author, outlet, or institutions).\\n"
            "  *Note: If the story contains multiple reporting sources in the dossier, evaluate each news outlet's editorial integrity and framing bias as individual aspects. Keep the ENTIRE combined Post 5 strictly under 260 characters total.\\n\""""

# 2. Add Speaker Anchor & Evidence Tier Barrier to core_concept_directive
old_core = """        "MEDIA PUNDITRY & ANTI-GOTCHA RULE:\\n"
        "- Never allow the audit to be tricked or hijacked by partisan media arguments, columnist commentary, or television panels.\\n"
        "- If an article focuses on pundits trading blame, television arguments, or partisan 'gotchas' (e.g., arguing over which president was in office during a crime): that media punditry is SELF-INCRIMINATING EXTRACTION. Pundits who exploit real human tragedy, crimes, or institutional breakdown to score tribal political points are running a selfish maneuver to extract attention and moral credit.\\n"
        "- Your audit must cut straight to the underlying crime, event, or institutional failure. Do NOT make a partisan calendar gotcha the central 'Reality' of the story. Expose the real institutional failure, and expose the punditry as a parasitic distraction from the victims and accountability.\\n\\n"
        "ACTOR ENTITIES & 7-ROLE CLASSIFICATION DIRECTIVE:\\n" """

new_core = """        "MEDIA PUNDITRY & ANTI-GOTCHA RULE:\\n"
        "- Never allow the audit to be tricked or hijacked by partisan media arguments, columnist commentary, or television panels.\\n"
        "- If an article focuses on pundits trading blame, television arguments, or partisan 'gotchas' (e.g., arguing over which president was in office during a crime): that media punditry is SELF-INCRIMINATING EXTRACTION. Pundits who exploit real human tragedy, crimes, or institutional breakdown to score tribal political points are running a selfish maneuver to extract attention and moral credit.\\n"
        "- Your audit must cut straight to the underlying crime, event, or institutional failure. Do NOT make a partisan calendar gotcha the central 'Reality' of the story. Expose the real institutional failure, and expose the punditry as a parasitic distraction from the victims and accountability.\\n\\n"
        "SPEAKER ANCHOR INVARIANT (POST 2 - STATED CLAIM):\\n"
        "- Post 2 (Stated Judgement) MUST evaluate the explicit, stated thesis of the primary author, speaker, or outlet publishing the piece.\\n"
        "- NEVER construct a phantom strawman claim attributed to the subject or group being attacked.\\n"
        "- If an author publishes an opinion piece or column attacking an ideology or movement, Post 2 MUST evaluate the author's stated thesis/defense (e.g. Greatest Lie / Partisan Defense), NOT an idealized claim that their opponents might make.\\n\\n"
        "EVIDENCE TIER BARRIER (ANECDOTE VS EMPIRICAL DATA):\\n"
        "- Tier 1 (Empirical / Hard Evidence): Audited financial statements, court filings, peer-reviewed data, official investigations, subpoenaed communications.\\n"
        "- Tier 2 (Attributed Institutional Reporting): On-the-record statements from multiple named witnesses, corroborating journalist investigations.\\n"
        "- Tier 3 (Subjective Opinion / Personal Anecdote): Unverified personal essays, culture-war polemics, anonymous gossip, personal nostalgia.\\n"
        "- RULE: Tier 3 evidence CANNOT be scored as real_u ground truth. If an article relies exclusively on Tier 3 personal anecdotes to make institutional claims, the author's aspect must receive a FAIL for Unsubstantiated Assertion.\\n\\n"
        "ACTOR ENTITIES & 7-ROLE CLASSIFICATION DIRECTIVE:\\n" """

# Strip trailing spaces
old_core = old_core.strip()
new_core = new_core.strip()

# 3. Add Actor-Aspect Invariant and Trajectory Sanity Checker in process_evaluations
old_eval = """            # Topic: store explicitly or extract from hashtags in the first post
            t = topic
            if not t:
                t = extract_topic_from_posts(story.get("posts", []))
            if t:
                story.setdefault("topic", t.strip())

            story.setdefault("event", "")"""

new_eval = """            # Topic: store explicitly or extract from hashtags in the first post
            t = topic
            if not t:
                t = extract_topic_from_posts(story.get("posts", []))
            if t:
                story.setdefault("topic", t.strip())

            story.setdefault("event", "")

            # Strict Actor-Aspect Invariant: Ensure aspects in Post 5 match declared actors
            if story.get("aspects") and story.get("actors"):
                valid_actor_names = {a.lower().strip() for a in story["actors"]}
                for asp in story["aspects"]:
                    asp_name = str(asp.get("aspect") or asp.get("name") or "").strip()
                    if asp_name.lower() not in valid_actor_names:
                        matched = next((a for a in story["actors"] if a.lower() in asp_name.lower() or asp_name.lower() in a.lower()), None)
                        if matched:
                            asp["aspect"] = matched
                        elif len(story["actors"]) > 0:
                            asp["aspect"] = story["actors"][0]

            # Trajectory Sanity Checker: Eliminate False 'Revelation' on moral collapse
            c_u = story.get("claim_u", 0.0)
            r_u = story.get("real_u", 0.0)
            if c_u > 0 and r_u < 0 and abs(c_u - r_u) >= 0.8:
                posts = story.get("posts", [])
                if len(posts) > 3:
                    p3 = posts[3]
                    if "Revelation" in p3 or "COND" in p3:
                        p3 = re.sub(r'Verdict:\\s*COND\\s*—\\s*The Path of Revelation\\.?', 'Verdict: FAIL — The Path of Deception.', p3)
                        p3 = re.sub(r'The Path of Revelation', 'The Path of Deception', p3)
                        p3 = re.sub(r'\\bCOND\\b', 'FAIL', p3)
                        posts[3] = p3"""

text_norm = text.replace('\r\n', '\n')
old_p5_norm = old_p5.replace('\r\n', '\n')
new_p5_norm = new_p5.replace('\r\n', '\n')
old_core_norm = old_core.replace('\r\n', '\n')
new_core_norm = new_core.replace('\r\n', '\n')
old_eval_norm = old_eval.replace('\r\n', '\n')
new_eval_norm = new_eval.replace('\r\n', '\n')

matches = 0
if old_p5_norm in text_norm:
    text_norm = text_norm.replace(old_p5_norm, new_p5_norm)
    matches += 1
else:
    print('Failed to match old_p5')

if old_core_norm in text_norm:
    text_norm = text_norm.replace(old_core_norm, new_core_norm)
    matches += 1
else:
    print('Failed to match old_core')

if old_eval_norm in text_norm:
    text_norm = text_norm.replace(old_eval_norm, new_eval_norm)
    matches += 1
else:
    print('Failed to match old_eval')

if matches == 3:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text_norm.replace('\n', '\r\n'))
    print('Successfully patched google_ai_studio_one_shot.py!')
else:
    print(f'Matched {matches}/3 blocks')
