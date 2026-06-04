import os
import sys
import json

# Setup sys.path to allow importing from bluesky_bot
workspace_root = r"e:\Vector Field Theory\VFT Docs"
sys.path.append(workspace_root)
sys.path.append(os.path.join(workspace_root, "bluesky_bot"))

from generate_graph import draw_graph
from aletheia_bot import save_and_sync_story

# Define Batch 3 (Stories 9-12, indices 8-11 from harvested_candidates.json)
stories = [
    {
        "id": "strawberry_beds_landslide",
        "subject": "Strawberry Beds Landslide",
        "link": "https://www.dublininquirer.com/council-looking-into-causes-of-small-landslide-in-strawberry-beds-earlier-this-year/",
        "claim_u": 1.0,
        "claim_psi": 1.0,
        "real_u": -1.0,
        "real_psi": -1.0,
        "mode": "reply",
        "target_url": "https://bsky.app/profile/dublininquirer.com/post/3mnem6jkjp42q",
        "rkeys": [],
        "post_urls": [],
        "status": "COMPLETED DRY RUN",
        "posts": [
            "Bureaucracy moves slower than gravity. A classic case of public safety framed as a proactive study while residents live with physical risk.\n\nStrawberry Beds Landslide Investigation\nEvidence: active study, passive risk, resolved hazard",
            "The council claims they are actively investigating the landslide's cause to ensure the road is safe for all residents.\nStated Judgement: (+1.0, +1.0) — Greater Good",
            "In reality, the study is a slow administrative reaction months after the event, leaving residents to bear the ongoing structural danger.\nResulting Judgement: (-1.0, -1.0) — Greater Evil",
            "Verdict: FAIL — The Path of Deception.\nAssurances of safety act as a phantom fill, hiding the lack of material intervention to secure the physical road.",
            "Following a landslide at Strawberry Beds earlier this year, Fine Gael Councillor Ted Leddy demanded safety assurances. The council is currently studying the cause, but residents remain anxious over the delay.",
            "The Bright Side:\nInvestigating the geological cause prevents ineffective, superficial repairs and ensures long-term engineering viability.",
            "The Breakdown & Plane Error:\nThey treat geological safety as an administrative study (WHAT). Structurally, it is a Will (WHO) error—using procedural delays to defer physical liability while public risk persists.",
            "The Trajectory: The Path of Deception.\nWhen a public authority uses administrative investigations to defer physical safety repairs...",
            "...it plots a direct trajectory toward Greater Evil. Intersecting u=-1.0 and psi=-1.0, this pathway normalizes danger by substituting studies for physical engineering.",
            "The Unavoidable Truth: Paperwork cannot reinforce a sliding hillside.\n\nThe Unavoidable Lie: That calling for a study is the same as securing the road.",
            "Alethekanon:\nAdministrative delay is a form of negative extraction. When a public body studies a hazard without securing the site, it externalizes the safety cost onto the citizens.",
            "Awwthekanon:\nResidents deserve peace of mind in their own homes. It is unfair to make families live in constant fear of the earth moving while waiting for a council report.",
            "Brothekanon:\nSo the hill fell down months ago and they're still 'looking into' why? Bro, gravity isn't waiting for the council meeting. Clear the dirt and fix the road.",
            "Synthesized Resolution Vector:\nBlended Path: The Path of Deception — Aletheia blends Bro's gravity check with Aww's peace of mind, concluding that procedural study collapses to Greater Evil.\nFinal Recalculated Coordinates: (-1.0, -1.0)"
        ]
    },
    {
        "id": "sf_election_turnout",
        "subject": "SF Election Turnout",
        "link": "https://bit.ly/4e1w5mf",
        "claim_u": 1.0,
        "claim_psi": 1.0,
        "real_u": -1.0,
        "real_psi": -1.0,
        "mode": "reply",
        "target_url": "https://bsky.app/profile/sfstandard.com/post/3mnem4iwatm2f",
        "rkeys": [],
        "post_urls": [],
        "status": "COMPLETED DRY RUN",
        "posts": [
            "Democracy by default is not democracy. A classic case of structural atrophy where citizen apathy collapses representative legitimacy.\n\nSF Election Turnout\nEvidence: active participation, minority rule, collective voice",
            "Voting is framed as a collective, representative decision-making process where the city's future is shaped by the active will of its citizens.\nStated Judgement: (+1.0, +1.0) — Greater Good",
            "In reality, an abysmal 25% turnout means a tiny, active interest group decides outcomes for the passive 75%, hollowing out democratic legitimacy.\nResulting Judgement: (-1.0, -1.0) — Greater Evil",
            "Verdict: FAIL — The Path of Deception.\nThe democratic container remains, but its actual representation is a phantom fill, hiding the collapse of civic engagement.",
            "Early results show turnout in San Francisco's Tuesday election hovering around an abysmally low 25%. A small fraction of the electorate is making crucial decisions for the entire city.",
            "The Bright Side:\nLow turnout highlights areas of friction, prompting calls to simplify voting access, align election dates, and improve voter education.",
            "The Breakdown & Plane Error:\nThey treat low turnout as a personal choice or individual voter fatigue (WHAT). Structurally, it is a system-level Will (HOW) failure that allows minority control.",
            "The Trajectory: The Path of Deception.\nWhen a democratic system maintains its procedural machinery while losing its participatory substance...",
            "...it plots a direct trajectory toward Greater Evil. Intersecting u=-1.0 and psi=-1.0, the system ceases to be representative and becomes an oligarchy by default.",
            "The Unavoidable Truth: A 25% turnout is not a mandate; it is a structural failure of representation.\n\nThe Unavoidable Lie: That a low-turnout election is still a healthy democracy.",
            "Alethekanon:\nDecentralized systems degrade when interaction costs exceed perceived benefits. If voting feels structurally pointless, citizens withdraw their participation.",
            "Awwthekanon:\nCivic apathy is often the result of feeling unheard and disconnected from power. We must rebuild community trust and make every citizen feel that their voice truly matters.",
            "Brothekanon:\nSo 75% of the city just decided to skip the vote? Bro, you can't complain about the laws if you don't even show up to the game. If you don't vote, someone else is picking your rules.",
            "Synthesized Resolution Vector:\nBlended Path: The Path of Deception — Aletheia blends Bro's showing up rule with Aww's trust building, concluding that passive apathy collapses to Greater Evil.\nFinal Recalculated Coordinates: (-1.0, -1.0)"
        ]
    },
    {
        "id": "kuwait_airport_drone_attack",
        "subject": "Kuwait Airport Drone Attack",
        "link": "https://n.pr/4vuDj9w",
        "claim_u": 1.0,
        "claim_psi": 1.0,
        "real_u": -1.5,
        "real_psi": -1.5,
        "mode": "reply",
        "target_url": "https://bsky.app/profile/npr.org/post/3mnekbzpigg2m",
        "rkeys": [],
        "post_urls": [],
        "status": "COMPLETED DRY RUN",
        "posts": [
            "Airspace safety is a polite fiction. A classic boundary collapse where geopolitical proxy wars directly spill into neutral civilian transport hubs.\n\nKuwait Suspends Flights After Drone Attack\nEvidence: safe transit, kinetic spillover, secure travel",
            "Civilian aviation is framed as an internationally protected domain, insulated from state conflicts by treaty and sovereign air boundaries.\nStated Judgement: (+1.0, +1.0) — Greater Good",
            "In reality, regional proxy missile exchanges routinely target or hit neutral civilian hubs, shutting down flights and causing human casualties.\nResulting Judgement: (-1.5, -1.5) — Greater Evil",
            "Verdict: FAIL — The Path of Deception.\nThe illusion of protected civilian zones collapses when state actors use deniable proxy drones to strike neutral sovereign territory.",
            "Kuwait suspended commercial flights after an Iranian drone hit its airport, causing injuries. This followed a series of missile strikes between Iran and the U.S., dragging neutral nations into the crossfire.",
            "The Bright Side:\nSuspension of flights prevents catastrophic civilian air disasters by preemptively removing targets from active kinetic corridors.",
            "The Breakdown & Plane Error:\nThey treat the drone strike as a localized airspace violation (WHERE). Structurally, it is a category error (WHO): treating a civilian aviation hub as a military battlefield.",
            "The Trajectory: The Path of Deception.\nWhen a nation's airspace safety guarantees are shown to be powerless against unilateral proxy warfare...",
            "...it plots a direct trajectory toward Greater Evil. Intersecting u=-1.5 and psi=-1.5, civilian infrastructure is normalized as a legitimate target in proxy conflicts.",
            "The Unavoidable Truth: Drones do not respect sovereign boundaries or civilian status.\n\nThe Unavoidable Lie: That third-party nations can remain safe from regional escalation.",
            "Alethekanon:\nGeopolitical deterrence must be absolute. When proxy attacks on civilian airports go unpunished, the threshold for attacking global transport hubs is permanently lowered.",
            "Awwthekanon:\nIt is terrifying for innocent travelers to be injured in a place of transit. We must protect civilian lives and keep these essential spaces free from the violence of war.",
            "Brothekanon:\nBro, shutting down a whole airport because a drone hit it is a massive warning. If you can't even fly without worrying about missiles, the global rules are completely broken.",
            "Synthesized Resolution Vector:\nBlended Path: The Path of Deception — Aletheia blends Bro's warning with Aww's civilian protection, concluding that proxy escalation collapses to Greater Evil.\nFinal Recalculated Coordinates: (-1.5, -1.5)"
        ]
    },
    {
        "id": "santos_sotu_betting_investigation",
        "subject": "Santos SOTU Betting Investigation",
        "link": "https://nyti.ms/4dKwU3Q",
        "claim_u": 1.0,
        "claim_psi": 1.0,
        "real_u": -2.0,
        "real_psi": 1.0,
        "mode": "reply",
        "target_url": "https://bsky.app/profile/nytimes.com/post/3mneavdvdck2z",
        "rkeys": [],
        "post_urls": [],
        "status": "COMPLETED DRY RUN",
        "posts": [
            "Constitutional duty as a betting slip. A classic case of public office being reduced to a private insider-trading mechanism for personal profit.\n\nGeorge Santos SOTU Betting Investigation\nEvidence: public duty, insider betting, public office",
            "Stated Claim:\nPublic officials attend official state proceedings, like the State of the Union, to represent their office and engage in governance.\nStated Judgement: (+1.0, +1.0) — Greater Good",
            "In reality, Santos allegedly used private knowledge of his own attendance to bet on it, converting a solemn state function into a personal casino.\nResulting Judgement: (-2.0, +1.0) — Greatest Lie",
            "Verdict: FAIL — The Path of The Fall.\nUsing public office to place insider bets is a direct collapse of representative trust into pure self-extraction.",
            "Federal authorities are investigating former Representative George Santos for potential insider trading. He allegedly placed financial bets on whether he would attend the State of the Union address.",
            "The Poison:\nNormalizing the monetization of an official's basic presence reduces democratic institutions to mere props for personal financial speculation.",
            "The Breakdown & Plane Error:\nHe claims this is simply personal finance or entertainment (WHAT). Structurally, it is a Will (WHO) error: converting public trust into a private, extractive arbitrage play.",
            "The Trajectory: The Path of The Fall.\nWhen public representatives treat their constitutional attendance as an asset class to bet on...",
            "...it plots a direct trajectory toward Greatest Lie. Intersecting u=-2.0 and psi=1.0, the representative function is fully hollowed out for purely selfish profit.",
            "The Unavoidable Truth: Public office is a trust, not a casino game.\n\nThe Unavoidable Lie: That betting on your own attendance is harmless personal speculation.",
            "Alethekanon:\nInsider trading rules must apply to all actions of representatives. Allowing officials to trade on their own official schedules destroys institutional integrity.",
            "Awwthekanon:\nIt is deeply disappointing when public service is treated with such disrespect. We need leaders who honor their responsibilities and serve their communities with integrity.",
            "Brothekanon:\nBro, betting on whether you're gonna show up to your own job is the ultimate hustle. It's a complete joke, but you gotta admit, the sheer audacity of insider trading your own body is wild.",
            "Synthesized Resolution Vector:\nBlended Path: The Path of The Fall — Aletheia blends Bro's hustle comment with Aww's plea for respect, concluding that personal betting collapses trust to Greatest Lie.\nFinal Recalculated Coordinates: (-2.0, +1.0)"
        ]
    }
]

# Validation
errors = 0
for s in stories:
    story_id = s["id"]
    print(f"\nValidating post lengths for {story_id}...")
    for idx, p in enumerate(s["posts"], 1):
        p_len = len(p)
        if p_len >= 250:
            print(f"  ERROR: Post {idx} exceeds or equals 250 characters ({p_len} chars):")
            print(f"  {repr(p)}")
            errors += 1
        else:
            print(f"  Post {idx}: {p_len} chars (OK)")

if errors > 0:
    print(f"\nValidation FAILED with {errors} length errors. Correct before proceeding.")
    sys.exit(1)
else:
    print("\nAll posts validated successfully! Proceeding to generate graphs and configurations...")

for s in stories:
    story_id = s["id"]
    subject = s["subject"]
    
    # 1. Generate local graph
    graph_base_filename = f"{story_id}_graph.png"
    graph_dir = os.path.join(workspace_root, "bluesky_bot", "graph_png")
    os.makedirs(graph_dir, exist_ok=True)
    graph_path = os.path.join(graph_dir, graph_base_filename)
    
    print(f"\nGenerating graph for {story_id} at {graph_path}...")
    draw_graph(
        s["claim_u"], s["claim_psi"],
        s["real_u"], s["real_psi"],
        f"Assessment: {subject}",
        graph_path
    )
    
    # Copy graph image to _Generated_Content/graph_png/
    gen_graph_dir = os.path.join(workspace_root, "_Generated_Content", "graph_png")
    os.makedirs(gen_graph_dir, exist_ok=True)
    import shutil
    shutil.copy2(graph_path, os.path.join(gen_graph_dir, graph_base_filename))
    print(f"Copied graph image to _Generated_Content/graph_png/")
    
    # Update config with correct graph image reference
    s["graph_img"] = f"graph_png/{graph_base_filename}"
    
    # 2. Synchronize using save_and_sync_story helper
    print(f"Syncing story: {story_id}...")
    save_and_sync_story(s)

print("\nSUCCESS: All 4 Batch 3 stories processed, graphs plotted, and registries synced successfully!")
