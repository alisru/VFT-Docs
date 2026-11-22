import json
import os

p1 = 'bluesky_bot/stories/factcheck_even-girlbosses-cant-stand-the-office-environments-feminism-built.json'
p2 = 'bluesky_bot/stories/live/factcheck_even-girlbosses-cant-stand-the-office-environments-feminism-built.json'

with open(p1, 'r', encoding='utf-8') as f:
    data = json.load(f)

story = data[0] if isinstance(data, list) else data

# 1. Update Core Vectors & Thinking
story['thinking'] = "Phase 1-5 structural scan: Evaluating Jack Danielson op-ed in The Federalist. Stated thesis frames all-male veteran leadership as naturally resilient, chivalrous, and superior to female supervision (-0.4, +0.3). Ground reality reveals an anecdotal culture-war polemic weaponizing personal workplace nostalgia without comparative empirical organizational data (-0.75, -0.5). Direction: (-0.4, +0.3) -> (-0.75, -0.5) = The Path of Deception (FAIL)."
story['claim_u'] = -0.4
story['claim_psi'] = 0.3
story['real_u'] = -0.75
story['real_psi'] = -0.5
story['claim_integrity'] = 'Partisan Defense'
story['real_integrity'] = 'Misleading'
story['claim_rnet'] = 1.0
story['real_rnet'] = 2.1

# 2. Update Posts
story['posts'] = [
    "A personal essay asserts that all-male veteran teams provide superior workplace leadership, claiming female management produces cliquish, micromanaged dysfunction.\nEvidence: Unverified personal anecdotes, demographic citation\n#Workplace #Culture #Opinion",
    "Jack Danielson's Thesis: Male-dominated leadership teams naturally cultivate resilience, protect family life, and offer superior structure compared to female-led management.\nStated Judgement: (-0.4, +0.3) — Greatest Lie",
    "Ground Reality: Anecdotal culture-war polemics weaponize personal workplace nostalgia to justify gender-exclusive hierarchies without empirical supervisory or operational data.\nResulting Judgement: (-0.75, -0.5) — Lesser Evil",
    "Verdict: FAIL — The Path of Deception.\nPartisan op-ed weaponizes subjective anecdotes to rationalize gender-exclusive management, lacking empirical data.\n\nIntegrity: Misleading (Hypocrisy: 2.1, z: 2)",
    "- Jack Danielson: FAIL (-0.75, -0.5) — Unsubstantiated personal anecdotes.\n- The Federalist: FAIL (-0.6, -0.3) — Published polemic as sociological fact.",
    "Writing in The Federalist, Jack Danielson cites his own experience leading an all-male veteran team to argue against women in corporate leadership, despite lacking comparative organizational data.",
    "The Bright Side:\nValidates the universal employee need for clear boundaries, reasonable accommodation for parents, and direct, low-friction communication.",
    "The Breakdown & Plane Error:\nConfusing personal workplace comfort in an all-male cohort (HOW) with an objective rule of organizational management (WHAT).",
    "Social Physics Analysis:\nThe piece executes an ingroup rationalization maneuver, attributing ordinary organizational friction to female leadership while framing male veterans as uniquely noble guardians.",
    "The Trajectory: The Path of Deception.\nMoving from partisan self-justification (-0.4, +0.3) into regressive extraction (-0.75, -0.5), attempting to package personal nostalgia as structural truth.",
    "The Unavoidable Truth: Every workplace struggles with management friction, regardless of gender.\n\nThe Unavoidable Lie: That gender exclusivity inherently produces noble, conflict-free leadership.",
    "Alethekanon:\nAnecdote is not data. Projecting personal nostalgia onto an entire gender is ideological rationalization.",
    "Awwthekanon:\nMothers and fathers alike need workplaces that respect family life, caregiving, and human dignity without culture-war litmus tests.",
    "Brothekanon:\nJust because your military buddies ran a tight ship doesn't mean half the population can't manage an office.",
    "Spirithekanon:\n\"Judge not according to the appearance, but judge righteous judgment.\" John 7:24 FAIL\nRighteous discernment demands empirical fairness, not superficial prejudice born of personal bias."
]

# 3. Update Actor Roles
story['actor_roles'] = [
    {'name': 'Jack Danielson', 'role': 'author'},
    {'name': 'The Federalist', 'role': 'author'},
    {'name': 'Pew Research Center', 'role': 'context'},
    {'name': 'United States', 'role': 'context'}
]

# 4. Update Aspects to match declared actors exactly
story['aspects'] = [
    {
        'aspect': 'Jack Danielson',
        'claim_u': -0.4,
        'claim_psi': 0.3,
        'real_u': -0.75,
        'real_psi': -0.5,
        'verdict': 'FAIL',
        'reason': 'Relies on personal anecdotes rather than comparative organizational data'
    },
    {
        'aspect': 'The Federalist',
        'claim_u': -0.4,
        'claim_psi': 0.3,
        'real_u': -0.6,
        'real_psi': -0.3,
        'verdict': 'FAIL',
        'reason': 'Frames partisan culture-war op-ed as sociological reality'
    }
]

out = [story]
with open(p1, 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
with open(p2, 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

print('Updated story JSONs!')
