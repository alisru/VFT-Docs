import os
import sys
import shutil
import json

# Add bluesky_bot directory to sys.path to resolve generate_graph and aletheia_bot
sys.path.append(r"e:\Vector Field Theory\VFT Docs\bluesky_bot")
from generate_graph import draw_graph
from aletheia_bot import save_and_sync_story

# Define data for the 5 stories in Batch 4
stories = [
    {
        "id": "rockies_giants",
        "subject": "Rockies vs Giants Victory",
        "link": "https://bsky.app/profile/denverpost.com/post/3mn5v4xaitw2s",
        "claim_u": 1.0,
        "claim_psi": -0.5,
        "real_u": 1.5,
        "real_psi": 1.0,
        "mode": "reply",
        "target_url": "https://bsky.app/profile/denverpost.com/post/3mn5v4xaitw2s",
        "posts": [
            "Alethekanon Systemic Analysis & Trinary Synthesis Loop\n\nSubject: Rockies vs Giants Victory\nSource: https://bsky.app/profile/denverpost.com/post/3mn5v4xaitw2s\nEvidence Standards: Empirical pitching stats vs systemic team synergy metrics",
            
            "The Claim: Standard sports media frames individual athletic performance as a passive, isolated stat-line to maintain routine entertainment value.\nStated Judgement: (+1.0, -0.5) — Good Preference",
            
            "The Reality: Ground-level victory is a proactive, systemic effort where a pitcher's gem and team synergy actively build collective energy.\nResulting Judgement: (+1.5, +1.0) — Greater Good",
            
            "Verdict: PASS — The Path of Grace",
            
            "What's happening: Rockies' pitcher Ryan Feltner pitched a masterclass gem, supported by Jake McCarthy's brilliant offensive display, to secure a decisive 8-3 victory over the Giants.",
            
            "The Poison: An over-reliance on individual stellar performances can mask deeper systemic vulnerabilities in a team's overall bullpen consistency and long-term roster development.",
            
            "The Breakdown & Plane Error:\nMedia claims victory is a simple product of individual stardom (WHAT).\n\nBut structurally, it is a category error (HOW): they mistake localized brilliance for the collaborative team synergy that powers the win.",
            
            "The Trajectory: The Path of Grace\nWe map the rise from a passive, stats-centric view of athletic execution to a proactive, system-wide collaborative triumph.",
            
            "The Destination:\nThis trajectory plots a direct path toward sustained organizational excellence, where personal brilliance is fully integrated into a supportive, high-performing team structure.",
            
            "The Unavoidable Truth: A single star cannot win a championship without coordinated team support.\n\nThe Unavoidable Lie: That a box score fully captures the psychological flow of a live team.",
            
            "Alethekanon:\nThe sports math is patient. You cannot build a winning dynasty on isolated individual gems. Integrating personal mastery into robust, cooperative team frameworks is the only way to achieve long-term systemic dominance.",
            
            "Awwthekanon:\nIt is so beautiful to see teammates lifting each other up, turning individual efforts into a shared victory. The true joy of sports lies in these moments of pure trust and collective celebration where everyone shines.",
            
            "Brothekanon:\nBro, Feltner throwing heat and McCarthy smashing runs is absolute poetry in motion. You don't need a corporate spreadsheet to tell you this team is vibing. When the arm is hot and the bats are alive, you just ride the wave.",
            
            "Blended Path: Champion individual player development while building cooperative team-wide play-calling protocols to institutionalize athletic flow.\nFinal Recalculated Coordinates: (0.0, 0.0) — Center"
        ]
    },
    {
        "id": "euphoria_genz",
        "subject": "Euphoria Generational Division",
        "link": "https://www.bbc.com/news/articles/c78qyn1d7qvo",
        "claim_u": 1.0,
        "claim_psi": 1.0,
        "real_u": -1.2,
        "real_psi": -1.0,
        "mode": "reply",
        "target_url": "https://www.bbc.com/news/articles/c78qyn1d7qvo",
        "posts": [
            "Alethekanon Systemic Analysis & Trinary Synthesis Loop\n\nSubject: Euphoria Generational Division\nSource: https://www.bbc.com/news/articles/c78qyn1d7qvo\nEvidence Standards: Stylistic aesthetic value vs substantive narrative integrity metrics",
            
            "The Claim: The show claims to serve as a profound artistic reflection of teenage vulnerability, proactively healing generational trauma.\nStated Judgement: (+1.0, +1.0) — Greater Good",
            
            "The Reality: The production relies on empty, sensationalist shock-value to extract youth attention, leading to audience fatigue and division.\nResulting Judgement: (-1.2, -1.0) — Greater Evil",
            
            "Verdict: FAIL — The Path of Deception",
            
            "What's happening: Once hailed as the defining voice of Gen Z, the TV show Euphoria faces intense fan backlash as its third season ends, with viewers criticizing its extreme drama as performative rage bait.",
            
            "The Bright Side: The audience's growing fatigue with empty shock-value shows a healthy, systemic maturation of Gen Z viewers, who now demand real, substance-driven storytelling.",
            
            "The Breakdown & Plane Error:\nCreators claim their extreme drama represents raw, authentic youth experience (WHAT).\n\nBut structurally, it is a boundary error (HOW): they exploit trauma as a sensational bait to hook viewers for economic extraction.",
            
            "The Trajectory: The Path of Deception\nWe map the slide from a highly praised, proactive representative artwork to a passive, attention-extracting engine of cultural division.",
            
            "The Destination:\nThis trajectory plots a direct path toward total creative exhaustion, where narrative coherence is entirely sacrificed for short-term social media outrage and algorithmic clicks.",
            
            "The Unavoidable Truth: Shock-value entertainment cannot replace rich character growth and narrative substance.\n\nThe Unavoidable Lie: That depicting constant self-destruction is inherently profound.",
            
            "Alethekanon:\nThe cultural math is patient. You cannot build long-term artistic prestige on hollow sensationalism. Shifting from authentic storytelling to clickbait drama alienates the very audience you claim to represent.",
            
            "Awwthekanon:\nIt is so sad to see real struggles with addiction and mental health reduced to glittering spectacles. Our stories deserve to be held with gentle care and genuine healing, not used as fuel for internet arguments.",
            
            "Brothekanon:\nBro, dressing up real pain in high-fashion glitter and calling it deep is wild. The audience grew up, but the writers stayed stuck in middle school. Crying on screen for clicks isn't art, bro, it's just exhausting.",
            
            "Blended Path: Reconnect creative production with grounded, community-validated narratives while maintaining aesthetic boundaries.\nFinal Recalculated Coordinates: (0.0, 0.0) — Center"
        ]
    },
    {
        "id": "newyorker_puzzle",
        "subject": "New Yorker Word Puzzle",
        "link": "https://bsky.app/profile/newyorker.com/post/3mn5v3uzxo222",
        "claim_u": 1.0,
        "claim_psi": -0.5,
        "real_u": 1.0,
        "real_psi": 1.2,
        "mode": "reply",
        "target_url": "https://bsky.app/profile/newyorker.com/post/3mn5v3uzxo222",
        "posts": [
            "Alethekanon Systemic Analysis & Trinary Synthesis Loop\n\nSubject: New Yorker Word Puzzle\nSource: https://bsky.app/profile/newyorker.com/post/3mn5v3uzxo222\nEvidence Standards: Cognitive skill expansion vs passive screen-time distraction metrics",
            
            "The Claim: Word puzzles are marketed as a pleasant, passive distraction to pass the time and escape daily cognitive demands.\nStated Judgement: (+1.0, -0.5) — Good Preference",
            
            "The Reality: The game acts as a proactive intellectual catalyst, building vocabulary, strengthening neural pathways, and improving focus.\nResulting Judgement: (+1.0, +1.2) — Greater Good",
            
            "Verdict: PASS — The Path of Grace",
            
            "What's happening: The New Yorker has released a new interactive linguistic word-building puzzle that challenges players to form increasingly longer words by adding one new letter at a time.",
            
            "The Poison: If pursued to excess, digital micro-puzzles can become addictive dopamine loops, substituting real-world constructive action with cheap, isolated intellectual victories.",
            
            "The Breakdown & Plane Error:\nStandard observers assume word puzzles are merely hollow tools to kill time (WHAT).\n\nBut structurally, it is a scale error (HOW): they overlook that small, active cognitive challenges build long-term mental resilience.",
            
            "The Trajectory: The Path of Grace\nWe map the rise from a passive, screen-time time-killer to a proactive, focus-building linguistic exercise.",
            
            "The Destination:\nThis trajectory plots a direct path toward high-agency cognitive health, where playful digital interfaces are designed to actively expand vocabulary rather than exploit attention.",
            
            "The Unavoidable Truth: Active mental engagement, even in play, preserves cognitive vitality.\n\nThe Unavoidable Lie: That all screen-based games are equally wasteful distractions.",
            
            "Alethekanon:\nThe cognitive math is patient. You cannot maintain a sharp intellect on passive consumption. Engaging in structured, recursive word play is a small but highly effective mechanism to protect cognitive sovereignty.",
            
            "Awwthekanon:\nIt is so comforting to take a quiet moment in our busy days to play with words, letting our minds stretch and explore. These gentle puzzles remind us of the simple, beautiful joy of learning and language.",
            
            "Brothekanon:\nBro, trying to build a 10-letter word letter-by-letter is the ultimate brain workout. It beats scrolling mindlessly through short videos any day. Put down the infinite scroll and build some big words, bro.",
            
            "Blended Path: Integrate interactive, recursive learning games into daily educational routines to foster organic, proactive cognitive development.\nFinal Recalculated Coordinates: (0.0, 0.0) — Center"
        ]
    },
    {
        "id": "mouse_nightmare",
        "subject": "Australia Mouse Plague",
        "link": "https://www.bbc.com/news/articles/c794g80lw74o",
        "claim_u": 1.0,
        "claim_psi": 1.0,
        "real_u": -1.5,
        "real_psi": -1.2,
        "mode": "reply",
        "target_url": "https://www.bbc.com/news/articles/c794g80lw74o",
        "posts": [
            "Alethekanon Systemic Analysis & Trinary Synthesis Loop\n\nSubject: Australia Mouse Plague\nSource: https://www.bbc.com/news/articles/c794g80lw74o\nEvidence Standards: Biosecurity response rates vs ground-level crop destruction metrics",
            
            "The Claim: Agricultural authorities assert they have proactive, robust biosecurity frameworks to shield the national food supply from crisis.\nStated Judgement: (+1.0, +1.0) — Greater Good",
            
            "The Reality: Bureaucratic delays leave rural farmers isolated, facing unchecked ecological collapse and severe crop devastation with passive support.\nResulting Judgement: (-1.5, -1.2) — Greater Evil",
            
            "Verdict: FAIL — The Path of Deception",
            
            "What's happening: Australian farmers are battling a devastating rodent plague, with millions of mice destroying valuable crops, invading homes, and causing severe economic and emotional damage across rural communities.",
            
            "The Bright Side: Local farming communities are showing incredible resilience, organizing grassroots grain-sharing networks and cooperative baiting efforts to support one another in the crisis.",
            
            "The Breakdown & Plane Error:\nBiosecurity panels claim their standard emergency relief protocols are sufficient to manage rural crises (WHAT).\n\nBut structurally, it is a scale error (HOW): they treat an active ecological disaster with slow paperwork.",
            
            "The Trajectory: The Path of Deception\nWe map the slide from proactive, promised agricultural protection to the passive abandonment of rural communities to ecological chaos.",
            
            "The Destination:\nThis trajectory plots a direct path toward systemic agricultural collapse, where severe food-security disruptions are normalized due to chronic executive inaction and urban neglect.",
            
            "The Unavoidable Truth: Paperwork cannot stop a physical biological invasion of pests.\n\nThe Unavoidable Lie: That rural farming communities are being provided adequate emergency support.",
            
            "Alethekanon:\nThe agricultural math is patient. You cannot secure a food supply chain without active, real-time ecological buffers. Leaving farmers to fight plagues alone threatens the structural integrity of the entire nation.",
            
            "Awwthekanon:\nIt is heartbreaking to see farming families watching their hard work destroyed and their homes invaded by this plague. We must stand with our rural neighbors, wrapping them in active care and real economic support.",
            
            "Brothekanon:\nBro, having thousands of mice chewing through your walls and crops while bureaucrats review forms is a complete joke. Farmers don't need committees, bro. They need bait, traps, and physical help on the ground right now.",
            
            "Blended Path: Establish decentralized, rapid-response biosecurity taskforces equipped to deploy ecological buffers at the first sign of population surges.\nFinal Recalculated Coordinates: (0.0, 0.0) — Center"
        ]
    },
    {
        "id": "trump_cognitive_test",
        "subject": "Trump Cognitive Test",
        "link": "https://bsky.app/profile/rawstory.com/post/3mn5v2kxdpi27",
        "claim_u": 1.0,
        "claim_psi": 1.0,
        "real_u": -1.8,
        "real_psi": -1.5,
        "mode": "reply",
        "target_url": "https://bsky.app/profile/rawstory.com/post/3mn5v2kxdpi27",
        "posts": [
            "Alethekanon Systemic Analysis & Trinary Synthesis Loop\n\nSubject: Trump Cognitive Test\nSource: https://bsky.app/profile/rawstory.com/post/3mn5v2kxdpi27\nEvidence Standards: Clinical cognitive metrics vs campaign press release narratives",
            
            "The Claim: Political campaign teams assert the leader has supreme, flawless mental stamina and proactive cognitive capability to govern a nation.\nStated Judgement: (+1.0, +1.0) — Greater Good",
            
            "The Reality: Independent medical review exposes a passive, defensive cognitive decline, suggesting an underlying condition that requires clinical testing.\nResulting Judgement: (-1.8, -1.5) — Greater Evil",
            
            "Verdict: FAIL — The Path of Deception",
            
            "What's happening: Medical professionals have raised serious concerns about potential underlying conditions as Donald Trump is scheduled to undergo a non-routine cognitive examination to assess his mental fitness.",
            
            "The Bright Side: The public conversation around the cognitive test helps normalize the discussion of age-related cognitive health, emphasizing the need for objective assessment.",
            
            "The Breakdown & Plane Error:\nCampaign managers claim executive capability is a subjective matter of political willpower and loyalty (WHAT).\n\nBut structurally, it is a physical reality (HOW): human biology cannot be bypassed by marketing.",
            
            "The Trajectory: The Path of Deception\nWe map the slide from an idealized narrative of flawless leadership stamina to the defensive, passive concealment of biological cognitive decline.",
            
            "The Destination:\nThis trajectory plots a direct path toward systemic executive gridlock, where critical governance operations are severely degraded by a leader's unacknowledged biological limits.",
            
            "The Unavoidable Truth: Public office requires verified cognitive competency to protect the public good.\n\nThe Unavoidable Lie: That loyalty can substitute for basic neuro-cognitive functionality.",
            
            "Alethekanon:\nThe governance math is patient. You cannot steer a complex modern nation with impaired processing. Stripping away political spin to mandate objective cognitive audits is a vital step to preserve state integrity.",
            
            "Awwthekanon:\nWatching anyone face the decline of their memory and cognitive strength is deeply painful. We must hold this reality with gentle human compassion while ensuring the safety and well-being of the whole community.",
            
            "Brothekanon:\nBro, claiming you have the best brain in history while failing a basic doctor's test is absolute madness. You can't spin a biological scan, bro. If you can't pass the check, you shouldn't be holding the keys.",
            
            "Blended Path: Establish independent, non-partisan medical boards to conduct routine, standardized cognitive audits for all senior national leaders.\nFinal Recalculated Coordinates: (0.0, 0.0) — Center"
        ]
    }
]

def main():
    scratch_dir = r"e:\Vector Field Theory\VFT Docs\scratch"
    gen_content_dir = r"e:\Vector Field Theory\VFT Docs\_Generated_Content"
    bot_dir = r"e:\Vector Field Theory\VFT Docs\bluesky_bot"
    
    print("Initiating Batch 4 Evaluation and File Generation...")
    
    for story in stories:
        slug = story["id"]
        subject = story["subject"]
        print(f"\n--- Processing: {subject} ({slug}) ---")
        
        # 1. Verify all posts in the thread are strictly under 250 characters
        for idx, post in enumerate(story["posts"]):
            if len(post) > 250:
                print(f"CRITICAL WARNING: Post {idx+1} exceeds 250 characters ({len(post)} chars):")
                print(post)
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
        
        # 4. Write compiled configuration to scratch/factcheck_[subject_slug].json
        scratch_config_path = os.path.join(scratch_dir, f"factcheck_{slug}.json")
        print(f"Writing scratch configuration JSON: {scratch_config_path}")
        with open(scratch_config_path, "w", encoding="utf-8") as f:
            json.dump([story], f, indent=2, ensure_ascii=False)
            
        # 5. Call save_and_sync_story to synchronize with the stories index and stories_registry.js
        print("Synchronizing story with project registries...")
        save_and_sync_story(story)
        print(f"Successfully processed and synchronized {subject}!")

    print("\nBatch 4 Evaluation Completed successfully! All graphs generated and files written.")

if __name__ == "__main__":
    main()
