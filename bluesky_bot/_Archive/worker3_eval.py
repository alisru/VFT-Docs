import os
import sys
import json

# Setup sys.path to allow importing from bluesky_bot
workspace_root = r"e:\Vector Field Theory\VFT Docs"
sys.path.append(workspace_root)
sys.path.append(os.path.join(workspace_root, "bluesky_bot"))

from generate_graph import draw_graph
from aletheia_bot import save_and_sync_story

# Let's define the 5 stories in our batch (Stories 11-15, indices 10-14 from harvested_candidates.json)
stories = [
    {
        "slug": "mouse_nightmare",
        "config": {
            "subject": "Australia Mouse Plague",
            "link": "https://www.bbc.com/news/articles/c794g80lw74o?at_medium=RSS&at_campaign=rss",
            "claim_u": 1.0,
            "claim_psi": 1.0,
            "real_u": -1.5,
            "real_psi": -1.2,
            "mode": "root",
            "target_url": "",
            "status": "COMPLETED DRY RUN",
            "verdict": "FAIL — The Path of Deception",
            "graph_img": "mouse_nightmare_graph.png",
            "posts": [
                "Alethekanon Systemic Analysis & Trinary Synthesis Loop\n\nSubject: Australia Mouse Plague\nSource: https://www.bbc.com/news/articles/c794g80lw74o?at_medium=RSS&at_campaign=rss\nEvidence: Biosecurity metrics vs crop loss.\n\nPsochic Hegemony Graph",
                "The Claim:\nAgricultural agencies assert they have proactive, robust biosecurity frameworks to shield the national food supply from crisis.\nStated Judgement: (+1.0, +1.0) — Greater Good",
                "The Reality:\nBureaucratic delays leave rural farmers isolated, facing unchecked ecological collapse and severe crop devastation with passive support.\nResulting Judgement: (-1.5, -1.2) — Greater Evil",
                "Verdict: FAIL — The Path of Deception",
                "What's happening:\nAustralian farmers are battling a devastating rodent plague, with millions of mice destroying valuable crops, invading homes, and causing severe economic and emotional damage across rural communities.",
                "The Bright Side:\nLocal farming communities are showing incredible resilience, organizing grassroots grain-sharing networks and cooperative baiting efforts to support one another in the crisis.",
                "The Breakdown & Plane Error:\nBiosecurity panels claim emergency relief protocols are sufficient to manage rural crises (WHAT).\n\nBut structurally, it is a scale error (HOW): they treat active ecological disaster with slow paperwork.",
                "The Trajectory: The Path of Deception\nWe map the slide from proactive, promised agricultural protection to the passive abandonment of rural communities to ecological chaos.",
                "The Destination:\nThis trajectory plots a direct path toward systemic agricultural collapse, where severe food-security disruptions are normalized due to chronic executive inaction and urban neglect.",
                "The Unavoidable Truth: Paperwork cannot stop a physical biological invasion of pests.\n\nThe Unavoidable Lie: That rural farming communities are being provided adequate emergency support.",
                "Alethekanon:\nThe agricultural math is patient. You cannot secure a food supply chain without active, real-time ecological buffers. Leaving farmers to fight plagues alone threatens the structural integrity of the entire nation.",
                "Awwthekanon:\nIt is heartbreaking to see farming families watching their hard work destroyed and their homes invaded by this plague. We must stand with our rural neighbors, wrapping them in active care and real economic support.",
                "Brothekanon:\nBro, having thousands of mice chewing through your walls and crops while bureaucrats review forms is a complete joke. Farmers don't need committees, bro. They need bait, traps, and physical help on the ground right now.",
                "Blended Path: Establish decentralized, rapid-response biosecurity taskforces equipped to deploy ecological buffers at the first sign of population surges.\nFinal Recalculated Coordinates: (0.0, 0.0) — Center"
            ]
        }
    },
    {
        "slug": "us_strike_drug_boat",
        "config": {
            "subject": "US Strike on Drug Boat",
            "link": "https://www.theguardian.com/us-news/2026/may/31/us-strike-boat-kills-three-eastern-pacific?utm_source=dlvr.it&utm_medium=bluesky&CMP=bsky_gu",
            "claim_u": 1.0,
            "claim_psi": 1.0,
            "real_u": -1.5,
            "real_psi": -1.5,
            "mode": "reply",
            "target_url": "https://bsky.app/profile/theguardian.com/post/3mn5vz3kal225",
            "status": "COMPLETED DRY RUN",
            "verdict": "FAIL — The Path of Deception",
            "graph_img": "us_strike_drug_boat_graph.png",
            "posts": [
                "Alethekanon Analysis\nSubject: US Strike on Drug Boat\nTarget Post: https://www.theguardian.com/us-news/2026/may/31/us-strike-boat-kills-three-eastern-pacific?utm_source=dlvr.it&utm_medium=bluesky&CMP=bsky_gu\nEvidence: Force vs law.\n\nPsochic Hegemony Graph",
                "The Claim:\nThe US military is executing targeted maritime interdiction of illicit drug vessels to protect national security and uphold international law.\nStated Judgement: (+1.0, +1.0) — Greater Good",
                "The Reality:\nA lethal military strike on a suspect boat kills three individuals without due process, transforming a law enforcement interdiction into extrajudicial executions.\nResulting Judgement: (-1.5, -1.5) — Greater Evil",
                "Verdict: FAIL — The Path of Deception",
                "What's happening:\nA US Navy strike on an alleged drug boat in the Eastern Pacific Ocean resulted in three fatalities, sparking significant concern over the militarization of international drug interdiction operations.",
                "The Poison:\nNormalizing lethal military force on suspect vessels in international waters bypasses civilian judicial trial, replacing legal due process with executive execution under the banner of security.",
                "The Breakdown & Plane Error:\nCommanders claim they are acting under defense mandate (WHY).\n\nBut structurally, it is a category error (WHO): applying lethal warfare protocols to a civilian policing and law enforcement issue.",
                "The Switch:\nThey secure public support with anti-trafficking rhetoric, but structurally replace civilian justice with military destruction, eliminating transparency in international waters.",
                "The Trajectory: The Path of Deception\nWe map the slide from rule of law and international policing to unilateral military strikes that treat suspected criminals as combatants to be liquidated.",
                "The Destination:\nA dystopian maritime landscape where international waters become a due-process-free zone, allowing unchecked military execution based on unverified intelligence.",
                "The Unavoidable Truth: Executing suspects at sea without a trial is a human rights violation.\n\nThe Unavoidable Lie: That killing suspects without judicial review makes the homeland safer.",
                "Alethekanon:\nJustice must be structural. A state that bypasses its own legal foundations to enforce law becomes the lawbreaker. Maritime interdictions must secure suspects for civilian trial, not execution.",
                "Brothekanon:\nBro, blowing up a suspect boat in the middle of the ocean and killing three guys without a trial is absolutely wild. If you're a cop, you arrest them. Turning drug policing into a hot war zone is pure extraction.",
                "Blended Path: Enforce strict rules of engagement restricting maritime forces to non-lethal disabling tactics and mandating prompt civilian judicial review.\nFinal Recalculated Coordinates: (0.0, 0.0) — Center"
            ]
        }
    },
    {
        "slug": "pcos_renaming",
        "config": {
            "subject": "PCOS Renaming",
            "link": "https://www.bbc.com/news/articles/cd9p50j3ljko?at_medium=RSS&at_campaign=rss",
            "claim_u": 1.0,
            "claim_psi": 1.0,
            "real_u": 0.5,
            "real_psi": -0.5,
            "mode": "root",
            "target_url": "",
            "status": "COMPLETED DRY RUN",
            "verdict": "FAIL — The Path of Empty Mass (The Fall)",
            "graph_img": "pcos_renaming_graph.png",
            "posts": [
                "Alethekanon Systemic Analysis\nSubject: PCOS Renaming\nSource: https://www.bbc.com/news/articles/cd9p50j3ljko?at_medium=RSS&at_campaign=rss\nEvidence: Research funding vs semantic changes.\n\nPsochic Hegemony Graph",
                "The Claim:\nRenaming Polycystic Ovary Syndrome (PCOS) will increase public awareness, reduce diagnostic confusion, and help millions of women secure better healthcare.\nStated Judgement: (+1.0, +1.0) — Greater Good",
                "The Reality:\nWhile a name change clarifies medical taxonomy, the actual bottleneck is institutional underfunding and gender bias in gynecological research, making renaming a passive symbolic substitute.\nResulting: (+0.5, -0.5) — Lesser Good",
                "Verdict: FAIL — The Path of Empty Mass (The Fall)",
                "What's happening:\nPatient advocates are calling to rename PCOS, arguing the current name is inaccurate and delays diagnosis for over 170 million women globally who face systemic neglect in healthcare systems.",
                "The Bright Side:\nUpdating medical terminology to reflect systemic metabolic realities can reduce patient stigma, validate symptoms, and guide doctors toward more comprehensive diagnostic frameworks.",
                "The Breakdown & Plane Error:\nAdvocates claim renaming directly cures institutional neglect (WHAT).\n\nBut structurally, it's a category error (HOW): they treat a material deficit in research funding as a semantic issue.",
                "The Switch:\nThey hook the public with valid struggles of millions of women, but switch the focus from demand for material research budgets to a symbolic debate over letters and nomenclature.",
                "The Trajectory: The Path of Empty Mass (The Fall)\nWe map the slide from active demands for medical funding to passive, symbolic victories in nomenclature that do not build new clinics or research.",
                "The Destination:\nA system that boasts progressive, perfectly-inclusive terminology while leaving the actual medical treatment, funding, and clinical diagnostic rates completely unchanged.",
                "The Unavoidable Truth: A new name cannot cure an underfunded laboratory.\n\nThe Unavoidable Lie: That changing the label on a medical file is the same as funding a cure.",
                "Awwthekanon:\nWomen living with PCOS deserve true care. We need to surround them with active listening, research that honors their pain, and clinical support that heals, not just semantic updates that look nice on paper.",
                "Aletheia's Synthesis:\nSemantics matter for coordination, but must never substitute for material allocation. Renaming must be coupled with mandatory federal research funding matching the disease burden scale.",
                "Blended Path: Pair nomenclature updates with legally mandated increases in gynecological research funding budgets and decentralized diagnostic access.\nFinal Recalculated Coordinates: (0.0, 0.0) — Center"
            ]
        }
    },
    {
        "slug": "faberge_anniversary",
        "config": {
            "subject": "Fabergé 180th Anniversary",
            "link": "https://www.thetimes.com/life-style/luxury/article/faberge-180-times-luxury-nlrs5kz6k?utm_term=Autofeed&utm_medium=Social&utm_source=Bluesky#Echobox=1780241697",
            "claim_u": 1.0,
            "claim_psi": -1.0,
            "real_u": -1.2,
            "real_psi": 1.0,
            "mode": "reply",
            "target_url": "https://bsky.app/profile/thetimes.com/post/3mn5vx75q5r2s",
            "status": "COMPLETED DRY RUN",
            "verdict": "FAIL — The Path of The Fall",
            "graph_img": "faberge_anniversary_graph.png",
            "posts": [
                "Alethekanon Analysis\nSubject: Fabergé 180th Anniversary\nTarget Post: https://www.thetimes.com/life-style/luxury/article/faberge-180-times-luxury-nlrs5kz6k?utm_term=Autofeed&utm_medium=Social&utm_source=Bluesky#Echobox=1780241697\n\nPsochic Hegemony Graph",
                "The Claim:\nCelebrating 180 years of Fabergé, highlighting how imperial craftsmanship and luxury legacy are preserved as timeless, culturally valuable heirlooms.\nStated Judgement: (+1.0, -1.0) — Lesser Good",
                "The Reality:\nFabergé is owned by Gemfields, a multi-billion dollar colored gemstone mining conglomerate, transforming historical art into an extraction mechanism for elite wealth.\nResulting Judgement: (-1.2, +1.0) — Greatest Lie",
                "Verdict: FAIL — The Path of The Fall",
                "What's happening:\nFabergé marks its 180th anniversary, transitioning from historic imperial Easter eggs designed for Tsars to a modern high-luxury brand owned by a massive multinational mining corporation.",
                "The Poison:\nThis luxury legacy masking commodifies national heritage, utilizing historical romance to obscure the extractive reality of gemstone mining operations in developing countries.",
                "The Breakdown & Plane Error:\nCorporate owners claim they are preserving historical heritage (WHAT).\n\nBut structurally, they run a extraction game (WHO), using imperial nostalgia to sell mining profits.",
                "The Switch:\nThey hook the consumer with stories of imperial artisans, but switch the actual value to corporate gemstone extraction, leveraging brand prestige to justify astronomical markups.",
                "The Trajectory: The Path of The Fall\nWe map the slide from preservation of delicate local craftsmanship to the hyper-financialization of heritage, serving only as investment assets for elites.",
                "The Destination:\nA hyper-capitalized luxury landscape where art is completely hollowed out, existing solely as a marketing front for corporate resource extraction and elite wealth storage.",
                "The Unavoidable Truth: Imperial eggs were always elite wealth symbols, but modern corporate extraction is a financialized engine.\n\nThe Unavoidable Lie: That buying modern luxury preserves historic craft.",
                "Aletheia's Synthesis:\nArtistic heritage must be decoupled from speculative extraction. True craft preservation requires supporting independent artisan cooperatives, not buying corporate-branded luxury.",
                "Brothekanon:\nBro, hyping up 'imperial heritage' when you're just a giant gemstone mining conglomerate is ultimate marketing delusion. Real art is made by hand in local studios, not corporate boardrooms.",
                "Blended Path: Establish fair-trade, transparent mining standards coupled with direct funding for independent traditional jewelry craftsmanship programs.\nFinal Recalculated Coordinates: (0.0, 0.0) — Center"
            ]
        }
    },
    {
        "slug": "uk_heatwave_ends",
        "config": {
            "subject": "UK Heatwave Ends",
            "link": "https://www.bbc.com/news/articles/c4g0djwjy9no?at_medium=RSS&at_campaign=rss",
            "claim_u": 1.0,
            "claim_psi": 1.0,
            "real_u": -1.0,
            "real_psi": -1.0,
            "mode": "root",
            "target_url": "",
            "status": "COMPLETED DRY RUN",
            "verdict": "FAIL — The Path of Deception",
            "graph_img": "uk_heatwave_ends_graph.png",
            "posts": [
                "Alethekanon Systemic Analysis\nSubject: UK Heatwave Ends\nSource: https://www.bbc.com/news/articles/c4g0djwjy9no?at_medium=RSS&at_campaign=rss\nEvidence: Climate baseline shifts vs weather reporting.\n\nPsochic Hegemony Graph",
                "The Claim:\nPublic weather reports present temperature changes and weather patterns as natural, cyclical meteorological events to keep the public informed.\nStated Judgement: (+1.0, +1.0) — Greater Good",
                "The Reality:\nThe return of cooler rain is welcomed as relief, but structurally obscures the escalating baseline of record-breaking heatwaves driven by climate disruption.\nResulting Judgement: (-1.0, -1.0) — Greater Evil",
                "Verdict: FAIL — The Path of Deception",
                "What's happening:\nThe UK heatwave has broken, with rain and cooler air replacing a week of record-breaking temperatures that saw the hottest May day, offering relief while climate concerns loom.",
                "The Poison:\nTreating extreme climate anomalies as simple, passing weather events normalizes rising global temperatures, creating a false sense of security that delays aggressive environmental action.",
                "The Breakdown & Plane Error:\nBroadcasters claim they are delivering neutral daily updates (WHAT).\n\nBut structurally, it's a framing error (HOW): they treat long-term climate breakdown as short-term news.",
                "The Switch:\nThey hook viewers with daily comfort, but switch the focus away from structural ecological limits, treating the end of a heatwave as a return to safety rather than a warning sign.",
                "The Trajectory: The Path of Deception\nWe map the slide from active environmental awareness to passive acceptance of climate degradation, framed by corporate media as simple weather variations.",
                "The Destination:\nA normalized future where extreme, biosphere-threatening heatwaves are treated as standard seasonal trends, leaving the public passive as ecological foundations collapse.",
                "The Unavoidable Truth: The weather is breaking, but the climate is breaking permanently.\n\nThe Unavoidable Lie: That a rainy day means the environmental emergency is temporarily over.",
                "Alethekanon:\nInformation must connect to systemic reality. Weather reporting must integrate historical climate baseline anomalies, ensuring the public understands that today's hot day is part of a trend.",
                "Brothekanon:\nBro, celebrating the end of a heatwave while ignoring that every single year breaks temperature records is wild coping. Rain doesn't wash away carbon, bro. We need systemic energy upgrades now.",
                "Blended Path: Integrate moving 30-year climate averages directly into all public daily weather broadcasts to provide constant systemic context.\nFinal Recalculated Coordinates: (0.0, 0.0) — Center"
            ]
        }
    }
]

# Run validation and output generations
errors = 0
for s in stories:
    slug = s["slug"]
    cfg = s["config"]
    cfg["id"] = slug
    
    print(f"\nValidating post lengths for {slug}...")
    for idx, p in enumerate(cfg["posts"], 1):
        p_len = len(p)
        if p_len >= 250:
            print(f"  WARNING: Post {idx} exceeds 250 characters ({p_len} chars):")
            print(f"  {repr(p)}")
            errors += 1
        else:
            print(f"  Post {idx}: {p_len} chars (OK)")

if errors > 0:
    print(f"Validation FAILED with {errors} length errors. Correct before proceeding.")
    sys.exit(1)
else:
    print("All posts validated successfully! Proceeding to generate graphs and configurations...")

for s in stories:
    slug = s["slug"]
    cfg = s["config"]
    
    # 1. Save individual config json to scratch/
    scratch_json_path = os.path.join(workspace_root, "scratch", f"factcheck_{slug}.json")
    print(f"\nWriting compiled config to {scratch_json_path}...")
    with open(scratch_json_path, "w", encoding="utf-8") as f:
        json.dump([cfg], f, indent=2, ensure_ascii=False)
        
    # 2. Draw trajectory graph and save it in scratch/
    graph_path = os.path.join(workspace_root, "scratch", f"{slug}_graph.png")
    print(f"Generating graph at {graph_path}...")
    draw_graph(cfg["claim_u"], cfg["claim_psi"], cfg["real_u"], cfg["real_psi"], f"Assessment: {cfg['subject']}", graph_path)
    
    # 3. Synchronize story using native save_and_sync_story helper
    print(f"Syncing story: {slug}...")
    save_and_sync_story(cfg)

print("\nSUCCESS: All 5 stories processed, files written, and registries updated successfully!")
