import os
import sys
import json

sys.path.append('e:/Vector Field Theory/VFT Docs/bluesky_bot')
from generate_graph import draw_graph
from image_card_generator import generate_compact_info_card
from rebuild_registries_son import rebuild_registries

story_file = 'e:/Vector Field Theory/VFT Docs/bluesky_bot/stories/live/factcheck_amanda-seyfried-elizabeth-holmes-doc.json'

new_story = [
  {
    "thinking": "Phase 1-5 Potential Mode Audit: Fox News manufactures an outrage cycle around Amanda Seyfried appearing in Nathan Fielder documentary 'You Can See Everything' by scraping 3 anonymous tweets from X trolls. Stated claim claims to provide legitimate cultural accountability and expose celebrity defensiveness (+0.50, +0.20). Ground reality is extractive tabloid churn, using anonymous tweets to smear an actress for clicks while completely ignoring the actual $100M+ Theranos wire fraud (-0.75, +0.65). Result: FAIL (The Path of Deception) against Fox News reporting.",
    "id": "amanda-seyfried-elizabeth-holmes-doc",
    "subject": "Fox News manufactures Amanda Seyfried backlash over Elizabeth Holmes documentary using anonymous tweets",
    "link": "https://www.foxnews.com/entertainment/amanda-seyfried-faces-harsh-criticism-viewers-rip-behavior-elizabeth-holmes-documentary",
    "target_url": "",
    "claim_u": 0.50,
    "claim_psi": 0.20,
    "real_u": -0.75,
    "real_psi": 0.65,
    "mode": "root",
    "status": "LIVE POSTED (judgement-bot.bsky.social)",
    "modal_claim": "will be",
    "modal_real": "is not",
    "modal_vector": "Top-Right to Top-Left Inversion",
    "geodesic": "Red Top (The Imperial Trap)",
    "central_is_barrier_crossed": True,
    "claim_rnet": 1.0,
    "real_rnet": 6.8,
    "claim_z": 0,
    "real_z": 2,
    "claim_z_profile": [0, 0, 0, 0, 0, 0, 0],
    "real_z_profile": [1, 0, 0, 0, 1, 0, 0],
    "claim_integrity": "Absolute Truth",
    "real_integrity": "Severe Deception",
    "stated_forces": None,
    "actual_forces": None,
    "posts": [
      "Fox News turns 3 anonymous tweets into a national controversy over Amanda Seyfried in a new Elizabeth Holmes doc.\nEvidence: media reporting, tabloid churn, manufactured outrage #Aletheia #MediaAudit",
      "Fox News frames this piece as holding Hollywood elites accountable for performative empathy and defensiveness.\nStated Judgement: (+0.50, +0.20) — Good Preference",
      "In reality, the outlet launders 3 anonymous Twitter trolls into news, manufacturing a celebrity smear to farm clicks while trivializing actual Theranos fraud.\nResulting Judgement: (-0.75, +0.65) — Greatest Lie",
      "Verdict: FAIL — The Path of Deception.\nLaundering unverified internet comments into news weaponizes mob sentiment for ad revenue while erasing material institutional accountability.\n\nIntegrity: Severe Deception (Hypocrisy: 6.80, z: 2)",
      "Sub-Audits Breakdown:\n- Fox News Smear: FAIL (-0.75, +0.65) — Manufactures scandal from 3 tweets.\n- Amanda Seyfried: PASS (+0.30, -0.20) — Reckons honestly with playing a fraudster.\n- Nathan Fielder Doc: PASS (+0.35, +0.40) — Deconstructs persona.",
      "In Nathan Fielder's documentary 'You Can See Everything,' Seyfried revisits portraying Elizabeth Holmes. Fox News bypassed the film's psychological substance to build a hit piece on cherry-picked tweets.",
      "The Poison:\nElevating anonymous social media vitriol into mainstream news normalizes targeted harassment and rewards low-effort parasitic churn over real investigative journalism.",
      "The Breakdown & Plane Error:\nFox News confuses the WHO (an actress exploring artistic ambiguity) with the WHAT (Holmes' massive federal wire fraud), substituting emotional gossip for material facts.",
      "Social Physics Analysis:\nFox News executes a smart selfish maneuver: wrapping tabloid rage-farming in the pretext of accountability, using an actress as clickbait without doing any actual journalism.",
      "The Trajectory: The Path of Deception.\nModal Dynamics: will be -> is not via Red Top (The Imperial Trap).\nThe coverage promises moral exposure but delivers systemic erasure of nuanced artistic self-reflection.",
      "The Unavoidable Truth: Curating three hostile tweets does not constitute reporting.\n\nThe Unavoidable Lie: Attacking an actress's interview demeanor holds anyone accountable for Theranos.",
      "Alethekanon:\nConflating an actress's honest grappling with a character with the character's criminal fraud is an intellectual abdication designed purely for rage clicks.",
      "Awwthekanon:\nIt is exhausting to see an artist's genuine, vulnerable ambivalence weaponized by tabloids just to feed internet cruelty and division.",
      "Brothekanon:\nElizabeth Holmes stole hundreds of millions, and Fox News wrote an entire hit piece because three randoms on Twitter got mad at Amanda Seyfried.",
      "Spirithekanon:\n\"Do not speak evil against one another, brothers.\" James 4:11 PASS\nTrue discernment distinguishes between human vulnerability and deliberate deceit, refusing to join the mob."
    ],
    "actors": ["Fox News", "Amanda Seyfried", "Elizabeth Holmes", "Nathan Fielder"],
    "actor_roles": [
      {"name": "Fox News", "role": "author"},
      {"name": "Amanda Seyfried", "role": "target"},
      {"name": "Elizabeth Holmes", "role": "subject"},
      {"name": "Nathan Fielder", "role": "collaborator"}
    ],
    "category": "all",
    "topic": "Entertainment",
    "aspects": [
      {
        "aspect": "Fox News Smear",
        "claim_u": 0.50,
        "claim_psi": 0.20,
        "real_u": -0.75,
        "real_psi": 0.65,
        "verdict": "FAIL",
        "reason": "Manufactures scandal from 3 tweets."
      },
      {
        "aspect": "Amanda Seyfried Reflection",
        "claim_u": 0.30,
        "claim_psi": -0.10,
        "real_u": 0.30,
        "real_psi": -0.20,
        "verdict": "PASS",
        "reason": "Reckons honestly with playing a fraudster."
      }
    ],
    "multiAspect": True,
    "spiritual": True,
    "graph_img": "graph_png/amanda-seyfried-elizabeth-holmes-doc_graph.png",
    "rkeys": [
      "3myecae7q7r2e", "3myecaf2sgi26", "3myecah7zbt27", "3myecajenk32d",
      "3myecaljllu2q", "3myecanohpj2b", "3myecaptrht2d", "3myecarylny2n",
      "3myecau5rix2a", "3myecawdhxs2z", "3myecayib5c2z", "3myecb2nnul2o",
      "3myecb4symy2u", "3myecb6ysy42c", "3myecbb5m7i2u"
    ],
    "post_urls": [
      "https://bsky.app/profile/judgement-bot.bsky.social/post/3myecae7q7r2e",
      "https://bsky.app/profile/judgement-bot.bsky.social/post/3myecaf2sgi26",
      "https://bsky.app/profile/judgement-bot.bsky.social/post/3myecah7zbt27",
      "https://bsky.app/profile/judgement-bot.bsky.social/post/3myecajenk32d",
      "https://bsky.app/profile/judgement-bot.bsky.social/post/3myecaljllu2q",
      "https://bsky.app/profile/judgement-bot.bsky.social/post/3myecanohpj2b",
      "https://bsky.app/profile/judgement-bot.bsky.social/post/3myecaptrht2d",
      "https://bsky.app/profile/judgement-bot.bsky.social/post/3myecarylny2n",
      "https://bsky.app/profile/judgement-bot.bsky.social/post/3myecau5rix2a",
      "https://bsky.app/profile/judgement-bot.bsky.social/post/3myecawdhxs2z",
      "https://bsky.app/profile/judgement-bot.bsky.social/post/3myecayib5c2z",
      "https://bsky.app/profile/judgement-bot.bsky.social/post/3myecb2nnul2o",
      "https://bsky.app/profile/judgement-bot.bsky.social/post/3myecb4symy2u",
      "https://bsky.app/profile/judgement-bot.bsky.social/post/3myecb6ysy42c",
      "https://bsky.app/profile/judgement-bot.bsky.social/post/3myecbb5m7i2u"
    ]
  }
]

with open(story_file, 'w', encoding='utf-8') as f:
    json.dump(new_story, f, indent=2, ensure_ascii=False)
print('Updated story JSON file.')

# Regenerate graph and cards
graph_path = 'e:/Vector Field Theory/VFT Docs/bluesky_bot/graph_png/amanda-seyfried-elizabeth-holmes-doc_graph.png'
draw_graph(0.50, 0.20, -0.75, 0.65, new_story[0]['subject'], graph_path)
print('Regenerated graph PNG.')

card_base = 'e:/Vector Field Theory/VFT Docs/bluesky_bot/graph_png/amanda-seyfried-elizabeth-holmes-doc_info_card.png'
generate_compact_info_card(new_story[0], card_base)
print('Regenerated info cards.')

rebuild_registries()
print('Rebuilt registries.')
