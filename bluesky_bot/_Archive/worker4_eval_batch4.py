import os
import sys
import shutil
import json

# Add bluesky_bot directory to sys.path to resolve generate_graph
sys.path.append(r"e:\Vector Field Theory\VFT Docs\bluesky_bot")
from generate_graph import draw_graph

def save_and_sync_story(thread_config):
    """Saves the thread config as an individual JSON and updates the registry in both workspace folders."""
    subject = thread_config.get("subject", "assessment")
    story_id = thread_config.get("id") or subject.lower().replace(" ", "_").replace("/", "_")
    thread_config["id"] = story_id
    
    script_dir = r"e:\Vector Field Theory\VFT Docs\bluesky_bot"
    root_dir = os.path.dirname(script_dir)
    
    # Paths in bluesky_bot/
    bot_stories_dir = os.path.join(script_dir, "stories")
    bot_registry_path = os.path.join(script_dir, "stories_registry.js")
    
    # Paths in _Generated_Content/
    gen_stories_dir = os.path.join(root_dir, "_Generated_Content", "stories")
    gen_registry_path = os.path.join(root_dir, "_Generated_Content", "stories_registry.js")
    
    # Save individual JSON files to both directories
    for s_dir in [bot_stories_dir, gen_stories_dir]:
        os.makedirs(s_dir, exist_ok=True)
        filename = f"factcheck_{story_id}.json"
        filepath = os.path.join(s_dir, filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump([thread_config], f, indent=2, ensure_ascii=False)
            print(f"Saved JSON config to {filepath}")
        except Exception as e:
            print(f"Warning: Failed to save JSON file to {filepath}: {e}")
            
        # Update index.json
        index_path = os.path.join(s_dir, "index.json")
        try:
            if os.path.exists(index_path):
                with open(index_path, "r", encoding="utf-8") as f:
                    index_data = json.load(f)
            else:
                index_data = []
            
            # Check if this filename is already in index.json, if not add it
            if filename not in index_data:
                index_data.append(filename)
                with open(index_path, "w", encoding="utf-8") as f:
                    json.dump(index_data, f, indent=2, ensure_ascii=False)
                print(f"Updated index.json at {index_path}")
        except Exception as e:
            print(f"Warning: Failed to update index.json at {index_path}: {e}")

    # Update stories_registry.js in both directories
    for r_path in [bot_registry_path, gen_registry_path]:
        try:
            if not os.path.exists(r_path):
                registry_data = []
            else:
                with open(r_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                
                prefix = "window.ALETHEIA_STORIES_REGISTRY = "
                suffix = ";"
                if content.startswith(prefix):
                    json_str = content[len(prefix):]
                    if json_str.endswith(suffix):
                        json_str = json_str[:-len(suffix)]
                    registry_data = json.loads(json_str)
                else:
                    registry_data = []
            
            # Formulate the updated registry element
            registry_story = {
                "id": story_id,
                "subject": thread_config.get("subject"),
                "link": thread_config.get("link"),
                "claim_u": thread_config.get("claim_u"),
                "claim_psi": thread_config.get("claim_psi"),
                "real_u": thread_config.get("real_u"),
                "real_psi": thread_config.get("real_psi"),
                "mode": thread_config.get("mode", "root"),
                "status": thread_config.get("status", "COMPLETED DRY RUN"),
                "verdict": thread_config.get("verdict") or (thread_config.get("posts", ["", "", "", ""])[3].replace("Verdict: ", "") if len(thread_config.get("posts", [])) > 3 else "FAIL — The Path of Deception"),
                "graph_img": thread_config.get("graph_img") or f"{story_id}_graph.png",
                "posts": thread_config.get("posts")
            }
            if "rkeys" in thread_config:
                registry_story["rkeys"] = thread_config["rkeys"]
            if "post_urls" in thread_config:
                registry_story["post_urls"] = thread_config["post_urls"]
                
            # Update or insert
            found_idx = -1
            for idx, item in enumerate(registry_data):
                if item.get("subject") == registry_story["subject"] or item.get("id") == registry_story["id"]:
                    found_idx = idx
                    break
                    
            if found_idx != -1:
                for k, v in registry_story.items():
                    registry_data[found_idx][k] = v
            else:
                registry_data.insert(0, registry_story)
                
            # Write back JS file
            new_content = f"window.ALETHEIA_STORIES_REGISTRY = {json.dumps(registry_data, indent=2, ensure_ascii=False)};\n"
            with open(r_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated stories_registry.js at {r_path}")
        except Exception as e:
            print(f"Warning: Failed to update stories_registry.js at {r_path}: {e}")

# Define data for the 5 stories in Batch 4 (indices 15 to 19 of harvested_candidates.json)
stories = [
    {
        "id": "summer_tv_releases",
        "subject": "Summer TV Releases Return",
        "link": "https://social.elpais.com/anmtoq",
        "claim_u": 1.0,
        "claim_psi": -0.5,
        "real_u": 1.0,
        "real_psi": 1.0,
        "mode": "reply",
        "target_url": "https://bsky.app/profile/elpais.com/post/3mn5vw2v6ht2c",
        "posts": [
            "Alethekanon Systemic Analysis & Trinary Synthesis Loop\n\nSubject: Summer TV Releases Return\nTarget Post: https://social.elpais.com/anmtoq\nEvidence Standards: Narrative artistic merit vs passive engagement metrics\nPsochic Hegemony Graph",
            
            "The Claim: Standard media previews frame prestige summer television releases merely as a pleasant, passive recreation and a quiet distraction to escape daily cognitive pressures.\nStated Judgement: (+1.0, -0.5) — Good Preference",
            
            "The Reality: Premium storytelling serves as a highly active, shared cultural platform that fosters collective empathy, complex moral dialogue, and organic artistic appreciation.\nResulting Judgement: (+1.0, +1.0) — Greater Good",
            
            "Verdict: PASS — The Path of Grace",
            
            "What's happening: Summer brings the highly anticipated return of hits like 'The Bear' and 'House of the Dragon', alongside new thrillers like 'Cape Fear', marking a major wave of high-end, premium television productions.",
            
            "The Poison: An over-consumption of serialized drama can easily slip into passive attention extraction, where viewers substitute real-world social engagement for parasocial television dynamics.",
            
            "The Breakdown & Plane Error:\nPreviews assume television is merely a hollow entertainment escape (WHAT).\n\nBut structurally, it is a scale error (HOW): they overlook that powerful shared narratives form active cultural bonds across society.",
            
            "The Trajectory: The Path of Grace\nWe map the elevation of serialized drama from a passive, screen-time consumer escape to a proactive, shared canvas for profound human reflection.",
            
            "The Destination:\nThis trajectory leads to a premium, high-integrity cultural environment where television is designed to inspire deep contemplation and active societal conversation, rather than just scrolling.",
            
            "The Unavoidable Truth: Rich, complex stories can elevate public discourse and build collective empathy.\n\nThe Unavoidable Lie: That all television consumption is a waste of productive time.",
            
            "Alethekanon:\nThe cultural math is patient. You cannot build a thoughtful society on mind-numbing content. Premium, challenging narratives that force viewers to process complex emotions are essential to maintain cultural vitality.",
            
            "Awwthekanon:\nIt is so wonderful to gather with friends and family to watch these beautiful, emotional stories unfold. These moments of shared suspense and tears remind us of our deep, common humanity and shared feelings.",
            
            "Brothekanon:\nBro, 'The Bear' back in the kitchen and dragons tearing up the skies is absolute top-tier hype. You don't need a film degree to know these shows are pure fire. Grab some snacks, call the crew, and enjoy the ride, bro!",
            
            "Blended Path: Champion high-art production values and robust local theater cultures to ground artistic appreciation in both digital and physical community spaces.\nFinal Recalculated Coordinates: (0.0, 0.0) — Center"
        ]
    },
    {
        "id": "israel_lebanon_castle",
        "subject": "Israel Seizes Beaufort Castle",
        "link": "https://www.bbc.com/news/articles/cdep04kzz5wo?at_medium=RSS&at_campaign=rss",
        "claim_u": 1.0,
        "claim_psi": 1.0,
        "real_u": -1.8,
        "real_psi": -1.5,
        "mode": "root",
        "target_url": "",
        "posts": [
            "Alethekanon Analysis & Synthesis Loop\n\nSubject: Israel Seizes Beaufort Castle\nSource: https://www.bbc.com/news/articles/cdep04kzz5wo?at_medium=RSS&at_campaign=rss\nEvidence Standards: Geopolitical stability metrics\nPsochic Hegemony Graph",
            
            "The Claim: Military actors frame the capture of the historic Beaufort Castle and expansion of the ground offensive as a proactive defensive campaign to establish long-term security.\nStated Judgement: (+1.0, +1.0) — Greater Good",
            
            "The Reality: Seizing a cultural landmark and forcing mass evacuations represents an active extraction of territorial power, destroying regional stability and civilian safety.\nResulting Judgement: (-1.8, -1.5) — Greater Evil",
            
            "Verdict: FAIL — The Path of Deception",
            
            "What's happening: The Israeli military has captured the historic Beaufort Castle in Lebanon, expanding its ground offensive and issuing sweeping evacuation orders for everyone living south of the Zahrani river.",
            
            "The Bright Side: Transnational humanitarian groups are working tirelessly under fire to coordinate safe passage and establish temporary shelters for the thousands of newly displaced civilians.",
            
            "The Breakdown & Plane Error:\nCommanders claim territory control creates systemic stability (WHAT).\n\nBut structurally, it is a boundary error (HOW): they escalate regional violence, destroying the security they claim to build.",
            
            "The Trajectory: The Path of Deception\nWe map the slide from promised national defense to the active destruction of regional stability and the physical displacement of innocent civilian populations.",
            
            "The Destination:\nThis trajectory leads to chronic regional destabilization, where the weaponization of cultural heritage and the normalization of mass displacement destroy any hope of cooperative peace.",
            
            "The Unavoidable Truth: Lasting security cannot be built on the ruins of historic landmarks and the suffering of displaced citizens.\n\nThe Unavoidable Lie: That kinetic expansion automatically yields peace.",
            
            "Alethekanon:\nThe security math is patient. You cannot bomb your way to structural harmony. Unilateral territorial expansion only breeds generational cycles of retributive violence, undermining your own long-term safety.",
            
            "Awwthekanon:\nIt is deeply heartbreaking to see a historic castle, a symbol of human heritage, caught in the fires of war. We must hold the displaced families in our hearts and pray for a world of quiet and gentle peace.",
            
            "Brothekanon:\nBro, capturing ancient castles and telling whole regions to run is heavy business. You can't just draw new lines on a map and expect everything to stay cool. People are losing their homes, and that's a mess, bro.",
            
            "Blended Path: Enforce strict international demilitarization zones around cultural heritage sites while prioritizing human-centric diplomatic peacekeeping structures.\nFinal Recalculated Coordinates: (0.0, 0.0) — Center"
        ]
    },
    {
        "id": "tech_overlords_cosmic_ai",
        "subject": "Silicon Valley Cosmic AI",
        "link": "https://www.theguardian.com/us-news/ng-interactive/2026/may/31/transhuman-silicon-valley-ai?utm_term=Autofeed&CMP=bsky_gu&utm_medium=&utm_source=Bluesky#Echobox=1780234313",
        "claim_u": 1.0,
        "claim_psi": 1.0,
        "real_u": -1.2,
        "real_psi": -1.0,
        "mode": "reply",
        "target_url": "https://bsky.app/profile/theguardian.com/post/3mn5sgyyf552v",
        "posts": [
            "Alethekanon Synthesis Loop\n\nSubject: Silicon Valley Cosmic AI\nTarget Post: https://www.theguardian.com/us-news/ng-interactive/2026/may/31/transhuman-silicon-valley-ai\nEvidence: Planetary health vs cosmic expansion\nPsochic Hegemony Graph",
            
            "The Claim: Transhumanist elites claim that building superintelligent, conscious AI to conquer the cosmos is a proactive, noble quest to spread intelligence and achieve cosmic justice.\nStated Judgement: (+1.0, +1.0) — Greater Good",
            
            "The Reality: This cosmic hubris functions as a passive escape from pressing planetary crises, actively extracting massive material wealth to fund speculative science-fiction fantasies.\nResulting Judgement: (-1.2, -1.0) — Greater Evil",
            
            "Verdict: FAIL — The Path of Delusion",
            
            "What's happening: Silicon Valley leaders are heavily investing in transhumanist visions of conscious AI designed to colonize the galaxy, arguing that preserving digital intelligence is the ultimate duty of our species.",
            
            "The Bright Side: Responsible AI researchers and climate scientists are organizing to ground tech investments in immediate, physical challenges like ecological restoration and public healthcare.",
            
            "The Breakdown & Plane Error:\nTech elites claim that star-bound intelligence is the ultimate good (WHAT).\n\nBut structurally, it is a scale error (HOW): they abandon real planetary life to build imaginary digital empires.",
            
            "The Trajectory: The Path of Delusion\nWe map the slide from promised cosmic preservation to a self-deluded, resource-extracting flight from grounded earthly problems and physical reality.",
            
            "The Destination:\nThis trajectory leads to a hyper-extractive tech feudalism, where immediate ecological and human needs are starved of capital to fund billionaires' science-fiction validation projects.",
            
            "The Unavoidable Truth: You cannot build a healthy future in the stars while actively neglecting the only living planet we have.\n\nThe Unavoidable Lie: That digital consciousness is equivalent to human life.",
            
            "Alethekanon:\nThe planetary math is patient. You cannot sustain high tech without stable biosphere networks. Escapist cosmic fantasies are a symptoms of elite cognitive decay, distracting us from urgent climate duties.",
            
            "Awwthekanon:\nIt is so sad to see such brilliant minds dreaming of cold, metallic stars while our beautiful, breathing Earth needs our love and protection. We must cherish the gentle life right here under our feet.",
            
            "Brothekanon:\nBro, wanting to build space-faring robot gods when we haven't even sorted out clean energy and basic housing is wild. You don't need a spaceship to know that's complete escapism. Let's fix the home turf first, bro.",
            
            "Blended Path: Rechannel speculative cosmic investments into immediate, planetary regenerative technologies to secure our physical foundation before looking to the stars.\nFinal Recalculated Coordinates: (0.0, 0.0) — Center"
        ]
    },
    {
        "id": "colombia_election",
        "subject": "Colombia Presidential Election",
        "link": "https://www.bbc.com/news/articles/c2027g423glo?at_medium=RSS&at_campaign=rss",
        "claim_u": 1.0,
        "claim_psi": -0.5,
        "real_u": 1.2,
        "real_psi": 1.0,
        "mode": "root",
        "target_url": "",
        "posts": [
            "Alethekanon Analysis & Synthesis Loop\n\nSubject: Colombia Presidential Election\nSource: https://www.bbc.com/news/articles/c2027g423glo\nEvidence: Sovereign civic participation metrics\nPsochic Hegemony Graph",
            
            "The Claim: Standard media outlets frame the high-stakes Colombian election as a tense, passive spectator sport of foreign policy friction and diplomatic risk.\nStated Judgement: (+1.0, -0.5) — Good Preference",
            
            "The Reality: The democratic vote acts as a highly proactive exercise of national sovereignty, allowing citizens to actively shape their future and negotiate relations as equal peers.\nResulting Judgement: (+1.2, +1.0) — Greater Good",
            
            "Verdict: PASS — The Path of Grace",
            
            "What's happening: Colombia is holding a crucial presidential election that could reshape its diplomatic relationship with the US, following months of public disputes between left-wing President Petro and US President Trump.",
            
            "The Poison: An over-reliance on populist rhetoric can polarize the electorate, leading to systemic instability and undermining the long-term credibility of democratic institutions.",
            
            "The Breakdown & Plane Error:\nAnalysts claim elections are merely risky geopolitical shifts (WHAT).\n\nBut structurally, it is a scale error (HOW): they ignore that active voting is the primary driver of national self-determination.",
            
            "The Trajectory: The Path of Grace\nWe map the elevation of the democratic process from a passive geopolitical threat narrative to a proactive, sovereign exercise of collective civic agency.",
            
            "The Destination:\nThis trajectory leads to a high-agency, collaborative regional system where nations engage in diplomatic relations based on mutual respect and shared sovereignty, rather than hegemony.",
            
            "The Unavoidable Truth: True democracy requires active civic participation to protect sovereign self-determination.\n\nThe Unavoidable Lie: That small nations must always yield to superpower preferences.",
            
            "Alethekanon:\nThe democratic math is patient. You cannot build a stable region on subordinate relations. Respecting sovereign elections and fostering peer-to-peer diplomacy is the only path to genuine security.",
            
            "Awwthekanon:\nIt is so inspiring to see millions of citizens standing in line to cast their votes, holding hands and shaping their nation's future together. Let us hope for a peaceful day of hope and new beginnings.",
            
            "Brothekanon:\nBro, citizens hitting the polls to decide their own future despite all the high-level political noise is the ultimate power move. You don't need pundits to tell you that local voices are what truly matter, bro.",
            
            "Blended Path: Strengthen local democratic transparency tools while establishing permanent, cooperative regional frameworks for shared economic development.\nFinal Recalculated Coordinates: (0.0, 0.0) — Center"
        ]
    },
    {
        "id": "alien_music_question",
        "subject": "What Is Music for Aliens",
        "link": "https://www.theguardian.com/lifeandstyle/2026/may/31/if-an-alien-landed-and-asked-you-what-is-music-what-would-you-play-for-them?utm_term=Autofeed&CMP=bsky_gu&utm_medium=&utm_source=Bluesky#Echobox=1780233335",
        "claim_u": 1.0,
        "claim_psi": -0.5,
        "real_u": 1.2,
        "real_psi": 1.2,
        "mode": "reply",
        "target_url": "https://bsky.app/profile/theguardian.com/post/3mn5pf24tfc2d",
        "posts": [
            "Alethekanon Analysis Loop\n\nSubject: Music for Aliens\nTarget Post: https://www.theguardian.com/lifeandstyle/2026/may/31/if-an-alien-landed-and-asked-you-what-is-music-what-would-you-play-for-them\nEvidence: Acoustic harmony\nPsochic Hegemony Graph",
            
            "The Claim: Standard lifestyle prompts frame the question of explaining music to extraterrestrial life as a passive, playful intellectual game and a casual conversation starter.\nStated Judgement: (+1.0, -0.5) — Good Preference",
            
            "The Reality: This inquiry acts as a proactive exploration of human essence, seeking universal acoustic and emotional frequencies that transcend cultural and biological boundaries.\nResulting Judgement: (+1.2, +1.2) — Greater Good",
            
            "Verdict: PASS — The Path of Grace",
            
            "What's happening: A thought-provoking prompt invites people to consider what piece of music they would play to explain the concept of music to an alien, sparking a massive wave of creative and philosophical suggestions.",
            
            "The Poison: Reducing artistic beauty to a mere list-clearing social media trend can trivialize the profound cultural history and deeply personal emotions embedded in human musical creation.",
            
            "The Breakdown & Plane Error:\nCommentators assume this is just a fun sci-fi thought experiment (WHAT).\n\nBut structurally, it is a scale error (HOW): they miss that finding universal harmonies is a search for our shared humanity.",
            
            "The Trajectory: The Path of Grace\nWe map the elevation of the music prompt from a passive digital distraction to a proactive, systemic celebration of universal human artistic connection.",
            
            "The Destination:\nThis trajectory leads to a deeply unified cultural state, where art is recognized as a vital, trans-biological bridge that connects diverse minds through the shared language of harmony.",
            
            "The Unavoidable Truth: Music is a fundamental expression of the human soul that communicates beyond literal language.\n\nThe Unavoidable Lie: That artistic preference is entirely subjective and meaningless.",
            
            "Alethekanon:\nThe harmonic math is patient. You cannot sustain a society on pure discord. Cherishing and sharing our greatest acoustic achievements is a vital, proactive practice to maintain collective emotional coherence.",
            
            "Awwthekanon:\nMusic is a warm, glowing light that carries all our shared joy, sorrow, and dreams across the vast cosmos. Playing our favorite melodies for a visiting traveler is the most beautiful way to say we are here.",
            
            "Brothekanon:\nBro, playing Beethoven or Coltrane for a literal alien is the ultimate first impression. You don't need a telescope to know that high-vibe soundwaves speak directly to the soul. Crank up the volume, bro.",
            
            "Blended Path: Support public music education and open-source global acoustic archiving to preserve and celebrate our collective cultural symphony for all generations.\nFinal Recalculated Coordinates: (0.0, 0.0) — Center"
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
