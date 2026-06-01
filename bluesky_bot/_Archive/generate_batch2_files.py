import os
import sys
import json

# Add workspace directory to python path
workspace_dir = r"e:\Vector Field Theory\VFT Docs"
sys.path.append(workspace_dir)

try:
    from bluesky_bot.generate_graph import draw_graph
    print("Successfully imported draw_graph from bluesky_bot.generate_graph!")
except ImportError as e:
    print(f"Failed to import draw_graph: {e}")
    sys.exit(1)

stories = [
    {
        "id": "bob_waldmire_route_66",
        "subject": "Route 66 Bob Waldmire",
        "link": "https://myfox8.com/news/i-try-to-cling-to-yesterday-how-route-66-artist-bob-waldmire-became-an-icon-of-the-mother-road/",
        "claim_u": 1.0,
        "claim_psi": 1.0,
        "real_u": 1.0,
        "real_psi": -1.0,
        "mode": "reply",
        "target_url": "https://bsky.app/profile/myfox8.com/post/3mn5w7ut6h22d",
        "status": "COMPLETED DRY RUN",
        "graph_img": "bob_waldmire_route_66_graph.png",
        "posts": [
            "Alethekanon Systemic Analysis & Trinary Synthesis Loop\n\nSubject: Route 66 Bob Waldmire\nTarget Post: https://myfox8.com/news/i-try-to-cling-to-yesterday-how-route-66-artist-bob-waldmire-became-an-icon-of-the-mother-road/\nEvidence Standards: Personal artistic choices vs regional economic changes.\nPsochic Hegemony Graph",
            "The Claim: Living as a nomadic artist on Route 66 preserves historical Americana and community heritage through simple, creative freedom.\nStated Judgement: (+1.0, +1.0) — Greater Good",
            "The Reality: Clinging to a museumified past is a beautiful but passive withdrawal, protecting personal memory while failing to engage with active structural renewal.\nResulting Judgement: (+1.0, -1.0) — Lesser Good",
            "Verdict: FAIL — The Path of Empty Mass (The Fall)",
            "What's happening: Route 66 artist Bob Waldmire became a legendary icon of the Mother Road, living in a customized school bus and drawing intricate maps, embodying a past era that modern highways have bypassed.",
            "The Bright Side: Waldmire's nostalgic art keeps local history alive and inspires travelers to value physical craftsmanship over modern standardized highways.",
            "The Breakdown & Plane Error:\nWaldmire frames his lifestyle as pure individual freedom and geographic travel (WHERE).\n\nBut structurally, it is a withdrawal from cooperative labor into a static, passive archive of the past (WHO).",
            "The Switch: It is a quiet bait-and-switch. He hooks us with the romance of the open road, but the lifestyle is an elite, non-replicable escape that leaves structural economic decay untouched.",
            "The Trajectory: The Path of Empty Mass (The Fall)\nWhen you map the massive gap between active community building and nostalgic, passive isolation...",
            "...it plots a direct trajectory toward stagnation. An entire regional culture is reduced to a roadside attraction rather than a thriving local economy.",
            "The Unavoidable Truth: You cannot build a future by living in a museum.\n\nThe Unavoidable Lie: That escaping modern problems is the same as solving them.",
            "Brothekanon:\nBro, living in a decorated school bus and drawing maps for fifty years is a legendary vibe, but it's a solo quest. You can't run a whole economy on roadside postcards and nostalgia.",
            "Aletheia's Synthesis:\nWe must combine historic preservation with active economic utility. Local communities should fund living workshops that teach traditional crafts to ensure heritage remains active.",
            "Synthesized Resolution Vector:\nBlended Path: Integrate historic preservation into active, cooperative local trade networks.\nFinal Recalculated Coordinates: (+1.0, 0.0)"
        ]
    },
    {
        "id": "disinformation_drama",
        "subject": "Disinformation Drama",
        "link": "https://www.bbc.com/news/articles/c392erkm3d2o",
        "claim_u": 1.0,
        "claim_psi": 1.0,
        "real_u": -0.5,
        "real_psi": 0.5,
        "mode": "root",
        "target_url": "",
        "status": "COMPLETED DRY RUN",
        "graph_img": "disinformation_drama_graph.png",
        "posts": [
            "Alethekanon Systemic Analysis & Trinary Synthesis Loop\n\nSubject: Disinformation Drama\nSource: https://www.bbc.com/news/articles/c392erkm3d2o\nEvidence Standards: Public broadcaster agenda-setting vs independent fact-checking.\nPsochic Hegemony Graph",
            "The Claim: We are producing a dramatic thriller to educate the public on the systemic threat of online lies and protect democratic discourse.\nStated Judgement: (+1.0, +1.0) — Greater Good",
            "The Reality: State-backed media uses prestige drama to pathologize skepticism of official narratives, turning structural systemic distrust into a psychological sickness.\nResulting Judgement: (-0.5, 0.5) — Greatest Lie",
            "Verdict: FAIL — The Path of The Fall",
            "What's happening: The BBC promoted \"Tip Toe,\" a new drama by Russell T Davies exploring the terrifying speed of fake news, aiming to highlight how easily ordinary citizens can be manipulated by online theories.",
            "The Bright Side: The drama features excellent, high-quality acting and genuinely exposes the psychological mechanics of fear-mongering and social media escalation.",
            "The Breakdown & Plane Error:\nThey claim this is a neutral, creative warning about digital hygiene (WHAT).\n\nBut structurally, it uses emotional terror to frame any dissent from state narratives as a threat (WHO).",
            "The Switch: They hook the viewer with concerns about truth, but the second the story unfolds, they substitute institutional consensus for actual verifiable facts, delegitimizing independent investigation.",
            "The Trajectory: The Path of The Fall\nWhen you map the gap between educational storytelling and institutional propaganda...",
            "...it plots a direct trajectory toward a state-monopolized reality, where all disagreement with the official consensus is branded as toxic warfare.",
            "The Unavoidable Truth: Institutions lose trust when they act as gatekeepers rather than open platforms.\n\nThe Unavoidable Lie: That public media is immune to producing its own disinformation.",
            "Brothekanon:\nBro, a state-funded TV station making a scary horror show about how people shouldn't trust anyone but state-funded TV stations is absolutely wild. Talk about marking your own homework with a golden star!",
            "Aletheia's Synthesis:\nTruth is verified by open adversarial debate, not prestige storytelling. Broadcasters must restore public trust by showing their source work rather than scolding the audience.",
            "Synthesized Resolution Vector:\nBlended Path: Establish independent, transparent community audits of public media narratives to verify impartiality.\nFinal Recalculated Coordinates: (0.0, 0.0)"
        ]
    },
    {
        "id": "cat_dna_forensics_landmark",
        "subject": "Cat DNA Forensics Landmark",
        "link": "https://www.thestar.com/news/insight/a-murder-a-cat-a-breakthrough-how-canadian-police-found-new-potential-in-dna-testing/article_9b414a3b-ee28-4811-9058-1a7941e72289.html",
        "claim_u": 1.0,
        "claim_psi": -1.0,
        "real_u": 1.5,
        "real_psi": 1.5,
        "mode": "reply",
        "target_url": "https://bsky.app/profile/thestar.com/post/3mn5w77ga4k2p",
        "status": "COMPLETED DRY RUN",
        "graph_img": "cat_dna_forensics_landmark_graph.png",
        "posts": [
            "Aletheia Loop\nSubject: Cat DNA Forensics Landmark\nTarget Post: https://www.thestar.com/news/insight/a-murder-a-cat-a-breakthrough-how-canadian-police-found-new-potential-in-dna-testing/article_9b414a3b-ee28-4811-9058-1a7941e72289.html\nPsochic Hegemony Graph",
            "The Claim: Solving cold cases using innovative forensic DNA technologies is standard, routine police work aimed at establishing factual guilt.\nStated Judgement: (+1.0, -1.0) — Lesser Good",
            "The Reality: A pioneer scientific breakthrough using cat DNA successfully solved a cold murder case, establishing a historic legal precedent for universal justice.\nResulting Judgement: (+1.5, +1.5) — Greater Good",
            "Verdict: PASS — The Path of Grace",
            "What's happening: The 1994 murder of Shirley Ann Duguay was solved using cat DNA found on a discarded jacket—the first time non-human DNA secured a murder conviction, opening a new frontier in forensic science.",
            "The Poison: The over-reliance on trace biological DNA in courts can lead to cognitive bias and false convictions if physical chain of custody or sample purity is compromised.",
            "The Breakdown & Plane Error:\nDefense lawyers framed the genetic evidence as unproven, speculative junk science (WHAT).\n\nBut structurally, the forensic lab proved direct, physical causality linking the suspect to the crime scene (CAUSE).",
            "The Switch: There is no bait-and-switch. Forensic science delivers on its promise, converting trace biological material into load-bearing, physical proof that vindicates the victim.",
            "The Trajectory: The Path of Grace\nWhen you map the shift from stagnant, unsolved cold cases to dynamic, high-integrity scientific breakthroughs...",
            "...it plots a direct trajectory toward Justice, where universal truth is established by physical science rather than bureaucratic box-checking.",
            "The Unavoidable Truth: Nature leaves an indelible physical record of our actions.\n\nThe Unavoidable Lie: That a criminal can completely erase their physical presence.",
            "Brothekanon:\nBro, catching a murderer because his victim's cat shed a few hairs on his jacket is some next-level Sherlock Holmes stuff. You can clean the blood, but you can't tell the cat not to shed!",
            "Aletheia's Synthesis:\nSystemic justice requires standardizing non-human DNA databases. We must establish independent forensic verification protocols to ensure trace biological evidence remains robust in courts.",
            "Synthesized Resolution Vector:\nBlended Path: Establish independent national registries for forensic non-human DNA standards.\nFinal Recalculated Coordinates: (+1.5, +1.5)"
        ]
    },
    {
        "id": "ferrari_ev_backlash",
        "subject": "Ferrari EV Backlash",
        "link": "https://www.bbc.com/news/articles/c1l2y7j7454o",
        "claim_u": -0.5,
        "claim_psi": 0.5,
        "real_u": 1.0,
        "real_psi": -1.0,
        "mode": "root",
        "target_url": "",
        "status": "COMPLETED DRY RUN",
        "graph_img": "ferrari_ev_backlash_graph.png",
        "posts": [
            "Alethekanon Systemic Analysis & Trinary Synthesis Loop\n\nSubject: Ferrari EV Backlash\nSource: https://www.bbc.com/news/articles/c1l2y7j7454o\nEvidence Standards: Brand equity dynamics vs regulatory compliance targets.\nPsochic Hegemony Graph",
            "The Claim: We are building a cutting-edge EV to dominate the future electric luxury market while fulfilling emissions mandates.\nStated Judgement: (-0.5, 0.5) — Greatest Lie",
            "The Reality: The silent EV strips away the combustion soul of Ferrari, causing a massive brand backlash, while driving up classic mechanical values.\nResulting Judgement: (+1.0, -1.0) — Lesser Good",
            "Verdict: PASS — The Path of Redemption",
            "What's happening: Ferrari is facing intense criticism over its debut electric vehicle, the Luce, with traditional enthusiasts claiming the silent powertrain completely betrays the brand's heritage.",
            "The Poison: The massive surge in classic combustion car values increases emissions as wealthy collectors hoard and drive older, less efficient vehicles as a protest.",
            "The Breakdown & Plane Error:\nThey claim a Ferrari can be reduced to a software platform and a battery cell (HOW).\n\nBut structurally, they confuse regulatory compliance with the emotional art that defines luxury (WHO).",
            "The Switch: They tried to use carbon-neutral compliance to hook markets, but instead they triggered a massive, organic rebellion that restored value to authentic, physical craftsmanship.",
            "The Trajectory: The Path of Redemption\nWhen you map the shift from empty ESG-compliant electric luxury back to genuine mechanical appreciation...",
            "...it plots a direct trajectory toward a renaissance of mechanical preservation, where true value is anchored in tangible heritage rather than virtual carbon compliance.",
            "The Unavoidable Truth: A silent Ferrari is just a premium golf cart.\n\nThe Unavoidable Lie: That prestige brand value can survive total detachment from its physical foundation.",
            "Brothekanon:\nBro, a silent Ferrari EV is like non-alcoholic whiskey. Yes, it does the job, but who the hell wants it? Collectors paying millions are paying for the noise and the grease, not an iPad on wheels!",
            "Aletheia's Synthesis:\nLuxury is an emotional artifact, not a utility. Ferrari must meet emissions standards through carbon-neutral synthetic fuels, preserving the mechanical combustion engine.",
            "Synthesized Resolution Vector:\nBlended Path: Dedicate EV platforms to commuter utility, while reserving classic luxury for high-efficiency, synthetic-fueled combustion craftsmanship.\nFinal Recalculated Coordinates: (0.0, 0.0)"
        ]
    },
    {
        "id": "global_sumud_flotilla_repression",
        "subject": "Global Sumud Flotilla Repression",
        "link": "https://www.democracynow.org/2026/5/26/global_sumud_flotilla_activists_violent_repression",
        "claim_u": -0.5,
        "claim_psi": 0.5,
        "real_u": -1.5,
        "real_psi": -1.5,
        "mode": "reply",
        "target_url": "https://bsky.app/profile/democracynow.org/post/3mn5w2feyv32r",
        "status": "COMPLETED DRY RUN",
        "graph_img": "global_sumud_flotilla_repression_graph.png",
        "posts": [
            "Aletheia Loop\nSubject: Global Sumud Flotilla Repression\nTarget Post: https://www.democracynow.org/2026/5/26/global_sumud_flotilla_activists_violent_repression\nPsochic Hegemony Graph",
            "The Claim: Security forces maintain national borders, sovereignty, and order against unauthorized political provocations and maritime crossings.\nStated Judgement: (-0.5, 0.5) — Greatest Lie",
            "The Reality: Excessive physical abuse and beating of peaceful aid flotilla participants represent active suppression and violent destruction of humanitarian efforts.\nResulting Judgement: (-1.5, -1.5) — Greater Evil",
            "Verdict: FAIL — The Path of Delusion",
            "What's happening: Peace activists traveling on the Global Sumud Flotilla to deliver humanitarian aid were subjected to severe physical beatings and abuse by military forces trying to halt their maritime journey.",
            "The Bright Side: The violent repression has backfired, drawing global media attention and renewing international diplomatic focus on the blockaded populations.",
            "The Breakdown & Plane Error:\nMilitary spokespersons frame the boarding as a standard border security action (WHAT).\n\nBut structurally, it is a violent extraction of human rights to preserve absolute state dominance (WHO).",
            "The Switch: It is a classic bait-and-switch. State actors promise security and law, but deploy raw physical terror and lawless violence to silence peaceful civil observers.",
            "The Trajectory: The Path of Delusion\nWhen you map the shift from border protection rhetoric to lawless, violent abuse...",
            "...it plots a direct trajectory toward Chaos, where state actors destroy their own international legitimacy by attacking unarmed humanitarians.",
            "The Unavoidable Truth: Violence against humanitarians exposes systemic fear, not systemic strength.\n\nThe Unavoidable Lie: That security can be achieved by beating peaceful observers.",
            "Brothekanon:\nBro, sending armed soldiers to beat up peaceful volunteers on an aid boat isn't 'sovereign defense.' It's just a raw show of force because you don't want anyone watching what you do. It's incredibly messy.",
            "Aletheia's Synthesis:\nHumanitarian corridors must be legally declared neutral international zones. We must establish independent maritime monitoring teams to safeguard aid deliveries from unilateral state violence.",
            "Synthesized Resolution Vector:\nBlended Path: Enforce independent, UN-sanctioned naval escorts for certified humanitarian flotillas.\nFinal Recalculated Coordinates: (0.0, 0.0)"
        ]
    }
]

scratch_dir = r"e:\Vector Field Theory\VFT Docs\scratch"

for s in stories:
    # Save json to scratch/factcheck_[slug].json
    # Note: the prompt says the json file contains the compiled configuration, which is a LIST with the story object!
    # Wait, let's verify if the list is correct.
    # In `factcheck_nicola_sturgeon.json`, the structure is a JSON list containing a single object!
    # Let's save as [s] to match that format!
    json_path = os.path.join(scratch_dir, f"factcheck_{s['id']}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump([s], f, indent=2, ensure_ascii=False)
    print(f"Saved {json_path}")

    # Draw graph and save to scratch/[slug]_graph.png
    graph_path = os.path.join(scratch_dir, f"{s['id']}_graph.png")
    
    # We must call draw_graph. Let's see: generate_graph handles X-axis inversion and plotting
    try:
        draw_graph(
            s['claim_u'], s['claim_psi'],
            s['real_u'], s['real_psi'],
            f"Assessment: {s['subject']}",
            graph_path
        )
        print(f"Generated graph {graph_path}")
    except Exception as e:
        print(f"Error drawing graph for {s['id']}: {e}")

print("All Batch 2 files successfully generated!")
