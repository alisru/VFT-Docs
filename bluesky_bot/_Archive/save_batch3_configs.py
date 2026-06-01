import sys
import os
import json

# Add the workspace root to python path to allow importing bluesky_bot modules
workspace_root = r"e:\Vector Field Theory\VFT Docs"
sys.path.append(workspace_root)
sys.path.append(os.path.join(workspace_root, "bluesky_bot"))

from bluesky_bot.aletheia_bot import save_and_sync_story

stories = [
    {
        "slug": "train_wifi_improvement",
        "config": {
            "subject": "Train Wi-Fi Improvement",
            "link": "https://www.bbc.com/news/articles/cn8pn4l03r7o",
            "claim_u": 1.0,
            "claim_psi": 0.0,
            "real_u": -0.5,
            "real_psi": -0.5,
            "mode": "reply",
            "target_url": "https://www.bbc.com/news/articles/cn8pn4l03r7o",
            "status": "COMPLETED DRY RUN",
            "verdict": "FAIL — The Path of Deception",
            "graph_img": "train_wifi_improvement_graph.png",
            "posts": [
                "Alethekanon Systemic Analysis & Trinary Synthesis Loop\n\nSubject: Britain's Train Wi-Fi\nTarget Post: https://www.bbc.com/news/articles/cn8pn4l03r7o\nEvidence Standards: Commuter network speeds vs onboard hardware investment.",
                "The Claim:\nWe are upgrading onboard Wi-Fi transmitters to keep modern commuters connected and highly productive.\nStated Judgement: (+1.0, 0.0) — Good Preference",
                "The Reality:\nRail operators are throttling router speeds or removing Wi-Fi to cut costs, forcing passengers onto cellular signals blocked by train glass.\nResulting Judgement: (-0.5, -0.5) — Greater Evil",
                "Verdict: FAIL — The Path of Deception",
                "What's happening:\nUK train operators are facing a backlash as travelers experience abysmal Wi-Fi connections, with companies quietly letting networks decay while telling passengers to use their own data.",
                "The Bright Side:\nThe Wi-Fi blackouts force passengers off corporate laptops, creating silent pockets of offline contemplation and visual connection with the passing countryside.",
                "The Breakdown & Plane Error:\nOperators claim Wi-Fi is a simple, optional utility (HOW).\n\nBut actually, they use network deprivation as a cost-cutting tool to extract more value while delivering less public service (WHO).",
                "The Switch:\nThey lure commuters with promises of a seamless \"rolling office,\" but the second margins shrink, they quietly shift the infrastructure cost onto the passenger's personal data plan.",
                "The Trajectory: The Path of Deception\nWhen you map the gap between high-productivity marketing and the reality of dead zones...",
                "...it plots a direct trajectory toward structural stagnation, where public utilities are hollowed out to protect private balance sheets.",
                "The Unavoidable Truth: Train cars are Faraday cages, making high-speed cellular routing impossible without active onboard repeaters.\n\nThe Unavoidable Lie: That travelers can work productively without public network support.",
                "Brothekanon:\nBro, charging eighty quid for a ticket only to get zero bars and be told to 'just use your hotspot' is absolute comedy. Are we paying for travel or a sensory deprivation chamber?",
                "Aletheia's Synthesis:\nPublic transit is a physical and digital Commons. Wi-Fi must be regulated as a mandatory core operational requirement, not a premium perk that operators can discard to save pennies.",
                "Synthesized Resolution Vector:\nBlended Path: Nationalize transit network standards, mandating fiber-linked trackside cells and free, open-access onboard repeaters.\nFinal Recalculated Coordinates: (0.0, 0.0)"
            ]
        }
    },
    {
        "slug": "news_feed_remixing",
        "config": {
            "subject": "News Feed Remixing",
            "link": "https://bsky.app/profile/aendra.com/post/3miij6e2txc22",
            "claim_u": 1.0,
            "claim_psi": -1.0,
            "real_u": 1.0,
            "real_psi": 1.0,
            "mode": "reply",
            "target_url": "https://bsky.app/profile/aendra.com/post/3miij6e2txc22",
            "status": "COMPLETED DRY RUN",
            "verdict": "PASS — The Path of Grace",
            "graph_img": "news_feed_remixing_graph.png",
            "posts": [
                "Alethekanon Systemic Analysis & Trinary Synthesis Loop\n\nSubject: News Feed Remixing\nTarget Post: https://bsky.app/profile/aendra.com/post/3miij6e2txc22\nEvidence Standards: Decentralized feed customization protocols vs corporate aggregation.",
                "The Claim:\nWe offer users a simple, passive feed to read news and share stories without complex setups.\nStated Judgement: (+1.0, -1.0) — Lesser Good",
                "The Reality:\nThe remix protocol empowers users to actively reconfigure algorithmic streams, converting passive consumers into sovereign information curators.\nResulting Judgement: (+1.0, +1.0) — Greater Good",
                "Verdict: PASS — The Path of Grace",
                "What's happening:\nGraze Social introduced a simple remix button for news feeds, enabling users to copy, modify, and host their own customized algorithmic filters without needing code.",
                "The Poison:\nDecentralized feed remixing can lead to extreme hyper-polarization, as users construct insular information bubbles that filter out all challenging viewpoints.",
                "The Breakdown & Plane Error:\nCorporate platforms claim user freedom is a simple toggle between pre-baked lists (HOW).\n\nBut Graze proves that true agency requires structural permission to remix the code of curation itself (WHO).",
                "The Switch:\nTraditional media locks you in a gilded cage of passive consumption. This tool shatters the cage, shifting the duty of filtering truth directly back to the active user community.",
                "The Trajectory: The Path of Grace\nWhen you map the shift from passive, corporate-curated news feeds to active, community-remixed streams...",
                "...it plots a direct trajectory toward user sovereignty, where informational curation is owned by the network participants rather than private monopolies.",
                "The Unavoidable Truth: Curation is active work; freedom requires effort.\n\nThe Unavoidable Lie: That corporate algorithms can curate a healthy public square without bias.",
                "Awwthekanon:\nI love that we can build these quiet, custom spaces for our friends. It lets us curate news with true gentleness, protecting our communities from toxic outrage while sharing what really matters.",
                "Aletheia's Synthesis:\nDecentralized curation is a major step forward, but absolute isolation breeds radicalization. We need public-interest remix registries that promote diversity and cross-pollination.",
                "Synthesized Resolution Vector:\nBlended Path: Implement cooperative feed peer-reviews where users exchange remix templates to build shared, resilient networks.\nFinal Recalculated Coordinates: (0.0, 0.0)"
            ]
        }
    },
    {
        "slug": "disinformation_drama",
        "config": {
            "subject": "Disinformation Drama",
            "link": "https://www.bbc.com/news/articles/c392erkm3d2o",
            "claim_u": 1.0,
            "claim_psi": 1.0,
            "real_u": -0.5,
            "real_psi": 0.5,
            "mode": "reply",
            "target_url": "https://www.bbc.com/news/articles/c392erkm3d2o",
            "status": "COMPLETED DRY RUN",
            "verdict": "FAIL — The Path of The Fall",
            "graph_img": "disinformation_drama_graph.png",
            "posts": [
                "Alethekanon Systemic Analysis & Trinary Synthesis Loop\n\nSubject: Disinformation Drama\nTarget Post: https://www.bbc.com/news/articles/c392erkm3d2o\nEvidence Standards: Public broadcaster agenda-setting vs independent fact-checking.",
                "The Claim:\nWe are producing a dramatic thriller to educate the public on the systemic threat of online lies and protect democratic discourse.\nStated Judgement: (+1.0, +1.0) — Greater Good",
                "The Reality:\nState-backed media uses prestige drama to pathologize skepticism of official narratives, turning structural systemic distrust into a psychological sickness.\nResulting Judgement: (-0.5, 0.5) — Greatest Lie",
                "Verdict: FAIL — The Path of The Fall",
                "What's happening:\nThe BBC promoted \"Tip Toe,\" a new drama by Russell T Davies exploring the terrifying speed of fake news, aiming to highlight how easily ordinary citizens can be manipulated by online theories.",
                "The Bright Side:\nThe drama features excellent, high-quality acting and genuinely exposes the psychological mechanics of fear-mongering and social media escalation.",
                "The Breakdown & Plane Error:\nThey claim this is a neutral, creative warning about digital hygiene (WHAT).\n\nBut structurally, it uses emotional terror to frame any dissent from state narratives as a threat (WHO).",
                "The Switch:\nThey hook the viewer with concerns about truth, but the second the story unfolds, they substitute institutional consensus for actual verifiable facts, delegitimizing independent investigation.",
                "The Trajectory: The Path of The Fall\nWhen you map the gap between educational storytelling and institutional propaganda...",
                "...it plots a direct trajectory toward a state-monopolized reality, where all disagreement with the official consensus is branded as toxic warfare.",
                "The Unavoidable Truth: Institutions lose trust when they act as gatekeepers rather than open platforms.\n\nThe Unavoidable Lie: That public media is immune to producing its own disinformation.",
                "Brothekanon:\nBro, a state-funded TV station making a scary horror show about how people shouldn't trust anyone but state-funded TV stations is absolutely wild. Talk about marking your own homework with a golden star!",
                "Aletheia's Synthesis:\nTruth is verified by open adversarial debate, not prestige storytelling. Broadcasters must restore public trust by showing their source work rather than scolding the audience.",
                "Synthesized Resolution Vector:\nBlended Path: Establish independent, transparent community audits of public media narratives to verify impartiality.\nFinal Recalculated Coordinates: (0.0, 0.0)"
            ]
        }
    },
    {
        "slug": "obama_center_festival",
        "config": {
            "subject": "Obama Center Festival",
            "link": "https://bsky.app/profile/chicagotribune.com/post/3mn5v6ryhct2t",
            "claim_u": 1.0,
            "claim_psi": 1.0,
            "real_u": -0.5,
            "real_psi": -0.5,
            "mode": "reply",
            "target_url": "https://bsky.app/profile/chicagotribune.com/post/3mn5v6ryhct2t",
            "status": "COMPLETED DRY RUN",
            "verdict": "FAIL — The Path of Deception",
            "graph_img": "obama_center_festival_graph.png",
            "posts": [
                "Alethekanon Systemic Analysis & Trinary Synthesis Loop\n\nSubject: Obama Center Festival\nTarget Post: https://bsky.app/profile/chicagotribune.com/post/3mn5v6ryhct2t\nEvidence Standards: Local community development metrics vs gentrification rates.",
                "The Claim:\nWe are hosting a public, local community festival to celebrate South Side culture and unite the historic neighborhood.\nStated Judgement: (+1.0, +1.0) — Greater Good",
                "The Reality:\nThe massive center is built in a historical public park, funded by public subsidies while driving massive gentrification and displacing local Black residents.\nResulting Judgement: (-0.5, -0.5) — Greater Evil",
                "Verdict: FAIL — The Path of Deception",
                "What's happening:\nThe Obama Presidential Center announced a local community festival on its brand-new Chicago campus, promising neighborhood engagement amidst ongoing gentrification debates.",
                "The Bright Side:\nThe festival provides genuine economic opportunities for local artists, food vendors, and performers who are historically underfunded in the South Side.",
                "The Breakdown & Plane Error:\nThey claim this is a grassroots victory for neighborhood connection (WHERE).\n\nBut structurally, they leverage celebrity prestige to build a private mega-facility on public parkland (WHO).",
                "The Switch:\nThey hook the public with the promise of \"inclusion\" and arts, but actual ground-level land values skyrocket, squeezing out the very working-class community they claim to celebrate.",
                "The Trajectory: The Path of Deception\nWhen you map the gap between high-status philanthropy and the realities of neighborhood displacement...",
                "...it plots a direct trajectory toward premium gentrification, where historical public assets are converted into private monuments at the expense of locals.",
                "The Unavoidable Truth: You cannot build a billion-dollar landmark in a low-income area without causing gentrification.\n\nThe Unavoidable Lie: That a festival makes up for the loss of public parkland.",
                "Awwthekanon:\nIt is so painful to see families who have lived on the South Side for generations being slowly pushed out by rising rents. A true community space must protect its neighbors before building monuments.",
                "Aletheia's Synthesis:\nCultural philanthropy must not act as a cover for predatory gentrification. Presidential libraries should be built on private land and require binding community-benefit housing agreements.",
                "Synthesized Resolution Vector:\nBlended Path: Enforce strict, legally binding rent controls and affordable housing guarantees around any mega-development project.\nFinal Recalculated Coordinates: (0.0, 0.0)"
            ]
        }
    },
    {
        "slug": "ferrari_ev_backlash",
        "config": {
            "subject": "Ferrari EV Backlash",
            "link": "https://www.bbc.com/news/articles/c1l2y7j7454o",
            "claim_u": -0.5,
            "claim_psi": 0.5,
            "real_u": 1.0,
            "real_psi": -1.0,
            "mode": "reply",
            "target_url": "https://www.bbc.com/news/articles/c1l2y7j7454o",
            "status": "COMPLETED DRY RUN",
            "verdict": "PASS — The Path of Redemption",
            "graph_img": "ferrari_ev_backlash_graph.png",
            "posts": [
                "Alethekanon Systemic Analysis & Trinary Synthesis Loop\n\nSubject: Ferrari EV Backlash\nTarget Post: https://www.bbc.com/news/articles/c1l2y7j7454o\nEvidence Standards: Brand equity dynamics vs regulatory compliance targets.",
                "The Claim:\nWe are building a cutting-edge EV to dominate the future electric luxury market while fulfilling emissions mandates.\nStated Judgement: (-0.5, 0.5) — Greatest Lie",
                "The Reality:\nThe silent EV strips away the combustion soul of Ferrari, causing a massive brand backlash, while driving up classic mechanical values.\nResulting Judgement: (+1.0, -1.0) — Lesser Good",
                "Verdict: PASS — The Path of Redemption",
                "What's happening:\nFerrari is facing intense criticism over its debut electric vehicle, the Luce, with traditional enthusiasts claiming the silent powertrain completely betrays the brand's heritage.",
                "The Poison:\nThe massive surge in classic combustion car values increases emissions as wealthy collectors hoard and drive older, less efficient vehicles as a protest.",
                "The Breakdown & Plane Error:\nThey claim a Ferrari can be reduced to a software platform and a battery cell (HOW).\n\nBut structurally, they confuse regulatory compliance with the emotional art that defines luxury (WHO).",
                "The Switch:\nThey tried to use carbon-neutral compliance to hook the Chinese market, but instead they triggered a massive, organic rebellion that restored value to authentic, physical craftsmanship.",
                "The Trajectory: The Path of Redemption\nWhen you map the shift from empty ESG-compliant electric luxury back to genuine mechanical appreciation...",
                "...it plots a direct trajectory toward a renaissance of mechanical preservation, where true value is anchored in tangible heritage rather than virtual carbon compliance.",
                "The Unavoidable Truth: A silent Ferrari is just a premium golf cart.\n\nThe Unavoidable Lie: That prestige brand value can survive total detachment from its physical foundation.",
                "Brothekanon:\nBro, a silent Ferrari EV is like non-alcoholic whiskey. Yes, it does the job, but who the hell wants it? Collectors paying millions are paying for the noise and the grease, not an iPad on wheels!",
                "Aletheia's Synthesis:\nLuxury is an emotional artifact, not a utility. Ferrari must meet emissions standards through carbon-neutral synthetic fuels, preserving the mechanical combustion engine.",
                "Synthesized Resolution Vector:\nBlended Path: Dedicate EV platforms to commuter utility, while reserving classic luxury for high-efficiency, synthetic-fueled combustion craftsmanship.\nFinal Recalculated Coordinates: (0.0, 0.0)"
            ]
        }
    }
]

for s in stories:
    slug = s["slug"]
    config = s["config"]
    config["id"] = slug
    
    # Save the individual JSON directly to scratch/factcheck_[subject_slug].json
    scratch_json_path = os.path.join(workspace_root, "scratch", f"factcheck_{slug}.json")
    print(f"Saving compiled config to {scratch_json_path}...")
    with open(scratch_json_path, "w", encoding="utf-8") as f:
        json.dump([config], f, indent=2, ensure_ascii=False)
        
    # Natively run the project's save_and_sync_story function to update both stories directories and registry files
    print(f"Syncing {slug} using save_and_sync_story...")
    save_and_sync_story(config)

print("All stories compiled, written to scratch/, and synced successfully!")
