import os
import sys
import shutil
import json

# Add bluesky_bot directory to sys.path to resolve generate_graph and aletheia_bot
sys.path.append(r"e:\Vector Field Theory\VFT Docs\bluesky_bot")
from generate_graph import draw_graph
from aletheia_bot import save_and_sync_story

# Define data for the 5 stories in Batch 1
stories = [
    {
        "id": "nicola_sturgeon",
        "subject": "Nicola Sturgeon",
        "link": "https://www.bbc.com/news/articles/c2027k1ev3zo",
        "claim_u": 1.0,
        "claim_psi": 1.0,
        "real_u": -1.0,
        "real_psi": -1.0,
        "mode": "root",
        "target_url": "",
        "posts": [
            "Nicola Sturgeon represents a classic case of saying one thing but building another under the cover of a grand political cause.\n\nSubject: Nicola Sturgeon\nSource: https://www.bbc.com/news/articles/c2027k1ev3zo\nPsochic Hegemony Graph",
            
            "The Claim: Sturgeon maintains her innocence, stating her leadership was a selfless, proactive service dedicated purely to Scottish independence and public welfare.\nStated Judgement: (+1.0, +1.0) — Greater Good",
            
            "The Reality: A deep embezzlement investigation into SNP finances has shattered her political armor, exposing structural decay and severe misuse of collective resources.\nResulting Judgement: (-1.0, -1.0) — Greater Evil",
            
            "Verdict: FAIL — The Path of Deception",
            
            "What's happening: Scotland's former first minister faced intense questioning over the SNP fundraising scandal. While pleading her innocence on TV, the loss of her once-unshakeable authority was plain to see.",
            
            "The Bright Side: The investigation proves that Scotland's legal and democratic oversight systems remain robust enough to challenge even the most powerful leaders when integrity lapses.",
            
            "The Breakdown & Plane Error:\nSturgeon frames her defense as a purely personal struggle against unfair allegations. But structurally, it is a boundary failure to protect the basic fiduciary trust of her supporters.",
            
            "The Trajectory: The Path of Deception\nWhen you map the massive gap between her polished public rhetoric and the grimy reality of police raids and financial audits...",
            
            "...it plots a direct trajectory toward structural stagnation. A once-potent political movement is now paralyzed by legal defense and intense internal finger-pointing.",
            
            "The Unavoidable Truth: Political charisma cannot bypass financial transparency.\n\nThe Unavoidable Lie: That a grand cause justifies sloppy accountability and lack of oversight.",
            
            "Alethekanon:\nThe civic math is clear. You cannot sustain a political movement without strict internal checks. When leadership escapes accountability, the movement's structural foundation inevitably decays.",
            
            "Awwthekanon:\nIt is deeply painful to see supporters who poured their hearts and hard-earned savings into a cause feel let down. Trust is fragile, and true leadership must guard that collective hope with absolute care.",
            
            "Brothekanon:\nBro, she spent years sounding like the most organized leader in Europe, and now she is on TV because of a luxury camper van parked in her mother-in-law's driveway. You literally cannot make this up!",
            
            "Blended Path: Enforce independent, real-time financial auditing for all political parties as a constitutional safeguard.\nFinal Recalculated Coordinates: (0.0, 0.0) — Center"
        ]
    },
    {
        "id": "rotterdam_fire",
        "subject": "Rotterdam House Fire",
        "link": "https://www.rtl.nl/nieuws/binnenland/artikel/5607766/dode-woningbrand-rotterdam-lijnzaadstraat",
        "claim_u": 1.0,
        "claim_psi": 1.0,
        "real_u": 1.0,
        "real_psi": -0.5,
        "mode": "reply",
        "target_url": "https://bsky.app/profile/rtl.nl/post/3mn5wa54fxd2p",
        "posts": [
            "A tragic house fire in Rotterdam highlights the severe gap between idealized safety promises and actual physical limits on the ground.\n\nSubject: Rotterdam House Fire\nTarget Post: https://www.rtl.nl/nieuws/binnenland/artikel/5607766/dode-woningbrand-rotterdam-lijnzaadstraat\nPsochic Hegemony Graph",
            
            "The Claim: Modern municipal safety codes assert that urban emergency services deliver absolute, proactive protection, shielding all lives perfectly.\nStated Judgement: (+1.0, +1.0) — Greater Good",
            
            "The Reality: Responders bravely evacuated over sixty homes to prevent disaster, yet a tragic fatality occurred, exposing the physical limits of rapid intervention.\nResulting Judgement: (+1.0, -0.5) — Lesser Good",
            
            "Verdict: FAIL — The Path of Empty Mass (The Fall)",
            
            "What's happening: A devastating house fire erupted in Rotterdam, forcing the immediate evacuation of sixty neighboring homes. Firefighters contained the blaze, but one resident tragically lost their life.",
            
            "The Bright Side: The swift, courageous response of firefighters and neighbors prevented the fire from spreading, saving dozens of other lives in the dense residential block.",
            
            "The Breakdown & Plane Error:\nThe system treats safety as a purely logical compliance checklist. But physically, dense housing creates unpredictable combustion vectors that regulatory checklists cannot completely stop.",
            
            "The Trajectory: The Path of Empty Mass (The Fall)\nWe map the slide from the high-minded promise of total systemic safety to the tragic, localized containment of a physical disaster.",
            
            "...it plots a trajectory toward localized vulnerability, proving that even heroic emergency actions face hard biological and physical barriers in dense cities.",
            
            "The Unavoidable Truth: Fire does not respect regulatory compliance or planning papers.\n\nThe Unavoidable Lie: That municipal zoning can completely design out physical, tragic accidents.",
            
            "Alethekanon:\nUrban density requires redundant physical safety loops. We cannot rely solely on rapid response times; building layouts must feature passive containment zones to isolate thermal hazards early.",
            
            "Awwthekanon:\nA home is where we should feel safest, and losing a neighbor in this way is a profound collective grief. We must wrap the evacuated families in deep love and practical community support.",
            
            "Brothekanon:\nBro, saving sixty homes while tackling a massive blaze is a serious shift by those firefighters. But it is a heavy reminder that no matter how fast you roll out, some physical dangers are just brutal.",
            
            "Blended Path: Retrofit older high-density buildings with advanced fire suppression systems and localized neighborhood escape routes.\nFinal Recalculated Coordinates: (0.0, 0.0) — Center"
        ]
    },
    {
        "id": "champions_league_riots",
        "subject": "Champions League Riots France",
        "link": "https://www.bbc.com/news/articles/c0r2ejg1w9xo",
        "claim_u": 1.0,
        "claim_psi": 1.0,
        "real_u": -1.0,
        "real_psi": -2.0,
        "mode": "root",
        "target_url": "",
        "posts": [
            "A massive sports tournament transforms into street warfare, showing the gap between luxury branding and actual public safety failures.\n\nSubject: Champions League Riots France\nSource: https://www.bbc.com/news/articles/c0r2ejg1w9xo\nPsochic Hegemony Graph",
            
            "The Claim: Sports authorities assert the tournament represents a proactive celebration of global unity, community passion, and athletic achievement.\nStated Judgement: (+1.0, +1.0) — Greater Good",
            
            "The Reality: Severe riots, 800 arrests, and 219 injuries expose a total breakdown of civic order, externalizing security costs onto local communities.\nResulting Judgement: (-1.0, -2.0) — Greater Evil",
            
            "Verdict: FAIL — The Path of Deception",
            
            "What's happening: The French Champions League matches were overwhelmed by violent clashes. Fans and police fought in the streets, turning public squares into riot zones and injuring dozens of officers.",
            
            "The Bright Side: Peaceful fans actively tried to defuse tensions, and emergency medical teams worked tirelessly to treat the injured amidst tear gas.",
            
            "The Breakdown & Plane Error:\nOrganizers claim this is a secure, high-prestige spectacle. But structurally, they dump the heavy physical security costs and violent risks directly onto local taxpayers and public spaces.",
            
            "The Trajectory: The Path of Deception\nWe map the shift from high-minded marketing of sporting unity to the grimy, passive negligence that lets mass events dissolve into violent chaos.",
            
            "...it plots a trajectory toward public space collapse, where private sports organizations pocket billions while public infrastructure absorbs the physical damage.",
            
            "The Unavoidable Truth: Huge commercial sporting events are highly volatile tribal gatherings that require rigorous, active physical safety architecture.\n\nThe Unavoidable Lie: That corporate sports branding guarantees civic peace.",
            
            "Alethekanon:\nSports monopolies must be held financially liable for the entire security footprint. You cannot extract massive media revenues while leaving local city resources to manage crowd-control failures.",
            
            "Awwthekanon:\nPublic streets should be safe spaces for families to enjoy, not battlegrounds. We must restore community-led, welcoming host systems that prioritize human care and gentle de-escalation over riot gear.",
            
            "Brothekanon:\nBro, UEFA and the clubs make bank, but they act like a crowd of this size is a total surprise! 800 arrests is a military operation, not a football match. Fix the plan or play behind closed doors, bro.",
            
            "Blended Path: Enforce strict profit-sharing laws where private sports associations co-fund non-militarized public safety networks.\nFinal Recalculated Coordinates: (0.0, 0.0) — Center"
        ]
    },
    {
        "id": "great_lakes_plastics",
        "subject": "Great Lakes Plastics",
        "link": "https://www.chicagotribune.com/2026/05/31/plastics-clog-the-great-lakes/",
        "claim_u": 1.0,
        "claim_psi": 1.0,
        "real_u": -1.5,
        "real_psi": -1.5,
        "mode": "reply",
        "target_url": "https://bsky.app/profile/chicagotribune.com/post/3mn5w7xkd5w2r",
        "posts": [
            "Industrial extraction clogs our freshwaters while corporations downplay the threat, showing the divide between green marketing and plastic reality.\n\nSubject: Great Lakes Plastics\nTarget Post: https://www.chicagotribune.com/2026/05/31/plastics-clog-the-great-lakes/\nPsochic Hegemony Graph",
            
            "The Claim: The plastics industry asserts that its circular economy campaigns and advanced recycling technology actively protect global resources.\nStated Judgement: (+1.0, +1.0) — Greater Good",
            
            "The Reality: Corporations lobby to boost virgin plastic output and downplay severe microplastic hazards, extracting profit while polluting public waters.\nResulting Judgement: (-1.5, -1.5) — Greater Evil",
            
            "Verdict: FAIL — The Path of Deception",
            
            "What's happening: A major analysis reveals that despite extreme plastic clogging in the Great Lakes, chemical giants are pressing to expand production and aggressively downplaying the toxic ecological impacts.",
            
            "The Bright Side: Local citizen science teams and grassroots clean-up crews are stepping up, gathering water samples to expose microplastics and defend their home ecosystems.",
            
            "The Breakdown & Plane Error:\nThe industry markets plastic as a circular recycling triumph. But this is a bait-and-switch: they hook the public with green slogans while actively blocking laws to restrict virgin output.",
            
            "The Trajectory: The Path of Deception\nWe map the slide from proactive, promised ecological responsibility to the aggressive, passive externalization of toxic chemical plastic waste onto public waters.",
            
            "...it plots a trajectory toward biospheric breakdown, where chemical companies extract trillions while local lakes are permanently poisoned by non-biodegradable plastics.",
            
            "The Unavoidable Truth: Less than ten percent of plastic is recycled, making endless production growth ecologically unsustainable.\n\nThe Unavoidable Lie: That consumer sorting can solve a systemic production crisis.",
            
            "Alethekanon:\nThe ecological math is absolute. Circularity cannot exist without capping virgin plastic production. Shifting the waste burden onto consumers while expanding chemical output is a mathematical lie.",
            
            "Awwthekanon:\nWater is the lifeblood of our communities, and seeing our beautiful lakes choked with waste is deeply wounding. We must protect our waters as a sacred trust, keeping them clean for our children.",
            
            "Brothekanon:\nBro, making millions of tons of plastic and telling us to 'just recycle' is the ultimate gaslight. If it doesn't degrade, stop making more of it. You can't clean up a lake with a corporate press release.",
            
            "Blended Path: Enforce strict producer-responsibility laws that penalize virgin plastic creation and fund biodegradable alternatives.\nFinal Recalculated Coordinates: (0.0, 0.0) — Center"
        ]
    },
    {
        "id": "train_wifi_improvement",
        "subject": "Train Wi-Fi Improvement",
        "link": "https://www.bbc.com/news/articles/cn8pn4l03r7o",
        "claim_u": 1.0,
        "claim_psi": 0.0,
        "real_u": -0.5,
        "real_psi": -0.5,
        "mode": "root",
        "target_url": "",
        "posts": [
            "Commuters get promises of a seamless \"rolling office,\" but operators quietly let the infrastructure decay to protect their balance sheets.\n\nSubject: Train Wi-Fi Improvement\nSource: https://www.bbc.com/news/articles/cn8pn4l03r7o\nPsochic Hegemony Graph",
            
            "The Claim: Rail operators assert they are upgrading onboard Wi-Fi transmitters to keep commuters connected, passive, and highly productive.\nStated Judgement: (+1.0, 0.0) — Good Preference",
            
            "The Reality: Rail operators are throttling speeds or removing Wi-Fi to cut costs, forcing passengers onto cellular signals blocked by train glass.\nResulting Judgement: (-0.5, -0.5) — Greater Evil",
            
            "Verdict: FAIL — The Path of Deception",
            
            "What's happening: UK train operators face passenger backlash as travelers experience terrible onboard Wi-Fi. Companies are quietly letting networks rot while advising travelers to use their own phone data.",
            
            "The Bright Side: The Wi-Fi blackouts force commuters off their laptops, allowing them a quiet space for offline contemplation and reading while looking at the countryside.",
            
            "The Breakdown & Plane Error:\nOperators claim Wi-Fi is an optional, minor convenience. Structurally, they use network deprivation as a cost-cutting tactic, charging high fares while shifting infrastructure costs to users.",
            
            "The Trajectory: The Path of Deception\nWe map the gap between high-end digital office marketing and the reality of dead zones, proving how public utilities are hollowed out for private margins.",
            
            "...it plots a trajectory toward civic stagnation, where essential transit systems become less functional and force citizens to buy their own redundant data solutions.",
            
            "The Unavoidable Truth: Train cars act as Faraday cages, making reliable high-speed cellular routing impossible without active, onboard repeaters.\n\nThe Unavoidable Lie: That travelers can work productively without public network support.",
            
            "Alethekanon:\nDigital access is a core transit requirement in the modern age. Allowing private operators to let onboard infrastructure decay under the guise of an optional perk is a failure of public utility regulations.",
            
            "Awwthekanon:\nA long train commute is stressful enough without the frustration of losing touch with loved ones or work. We deserve public spaces that are supportive and help us stay connected with ease and comfort.",
            
            "Brothekanon:\nBro, charging a fortune for a train ticket only to get zero bars and be told to 'just use your hotspot' is comedy gold. Are we paying for a modern commute or a sensory deprivation chamber?",
            
            "Blended Path: Establish mandatory national transit network standards that fund trackside cell repeaters and free, open-access onboard Wi-Fi.\nFinal Recalculated Coordinates: (0.0, 0.0) — Center"
        ]
    }
]

def main():
    scratch_dir = r"e:\Vector Field Theory\VFT Docs\scratch"
    gen_content_dir = r"e:\Vector Field Theory\VFT Docs\_Generated_Content"
    bot_dir = r"e:\Vector Field Theory\VFT Docs\bluesky_bot"
    
    print("Initiating Worker 1 Batch 1 Evaluation and File Generation...")
    
    for story in stories:
        slug = story["id"]
        subject = story["subject"]
        print(f"\n--- Processing: {subject} ({slug}) ---")
        
        # 1. Verify all posts in the thread are strictly under 250 characters
        for idx, post in enumerate(story["posts"]):
            if len(post) > 250:
                print(f"CRITICAL WARNING: Post {idx+1} exceeds 250 characters ({len(post)} chars):")
                print(repr(post))
                sys.exit(1)
        print("Pre-flight character-count check: PASS (All posts < 250 chars).")
        
        # 2. Generate Trajectory Graph in scratch/
        graph_filename = f"{slug}_graph.png"
        scratch_graph_path = os.path.join(scratch_dir, graph_filename)
        
        print(f"Generating graph: {scratch_graph_path}")
        draw_graph(
            story["claim_u"], story["claim_psi"],
            story["real_u"], story["real_psi"],
            f"Assessment: {subject}",
            scratch_graph_path
        )
        
        # 3. Copy graph to _Generated_Content/ and bluesky_bot/
        gen_graph_path = os.path.join(gen_content_dir, graph_filename)
        bot_graph_path = os.path.join(bot_dir, graph_filename)
        
        print(f"Copying graph to {gen_graph_path}")
        shutil.copy(scratch_graph_path, gen_graph_path)
        
        print(f"Copying graph to {bot_graph_path}")
        shutil.copy(scratch_graph_path, bot_graph_path)
        
        story["graph_img"] = graph_filename
        story["status"] = "COMPLETED DRY RUN"
        
        # Determine verdict string
        v_label = story["posts"][3].replace("Verdict: ", "")
        story["verdict"] = v_label
        
        # 4. Write compiled configuration to scratch/factcheck_[subject_slug].json
        scratch_config_path = os.path.join(scratch_dir, f"factcheck_{slug}.json")
        print(f"Writing scratch configuration JSON: {scratch_config_path}")
        with open(scratch_config_path, "w", encoding="utf-8") as f:
            json.dump([story], f, indent=2, ensure_ascii=False)
            
        # 5. Call save_and_sync_story to synchronize with the stories index and stories_registry.js
        print("Synchronizing story with project registries...")
        save_and_sync_story(story)
        print(f"Successfully processed and synchronized {subject}!")

    print("\nBatch 1 Evaluation Completed successfully! All graphs generated and files written.")

if __name__ == "__main__":
    main()
