import re
import os
import glob

SOURCE_DIR = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America"

# Source of Truth for Narratives (with Land fixes)
NARRATIVES = {
    1: {
        "q1": '''> **The Narrative of Authenticity (The Who of the Who):**\n> The American Self is sovereign. We do not accept identity from the State, the Church, or the Ancestors. We build ourselves from scratch. The "Who" is a project, not an inheritance.''',
        "q2": '''> **The Narrative of Citizen (The Where of the Who):**\n> Geography creates Identity. The "Who" is defined by the "Where" (The Frontier, The City, The Suburb). We are not just "Americans" in the abstract; we are "New Yorkers" or "Texans." The Soil colors the Soul.''',
        "q3": '''> **The Narrative of Definition (The What of the Who):**\n> We are defined by what we do. The "Who" is a resume. In Europe, you are your Class; in America, you are your Job. The Definition is functional.''',
        "q4": '''> **The Narrative of Drive (The Why of the Who):**\n> The American is fueled by "More." The pursuit of Happiness is an infinite vector. They are an engine of Optimism that consumes the Future to power the Present. The "Why" is a religious belief in a Better Tomorrow.''',
        "q5": '''> **The Narrative of Character (The How of the Who):**\n> The American is a Pragmatist. They define "Truth" not as a static dogma but as a functional tool for the Identity. The "Who" is revealed in the "How." We care less for abstract "Rightness" than for the integrity of Action. To be American is to prove the Self through the authenticity of the Deed.''',
        "q6": '''> **The Narrative of Origin (The Cause of the Who):**\n> We are a nation of Immigrants. The "Cause" of the Identity is the Choice to Leave. We are defined by the rejection of the Old World. The "Who" begins with a Departure.''',
        "q7": '''> **The Narrative of Individual (The Effect of the Who):**\n> The Result is the Atomized Individual. We are free, but we are alone. The "Effect" of specific identity is the corrosion of community. We are a collection of "I's" struggling to say "We."''',
        "total": '''> **The American Identity is Volitional.**\n> It is not a bloodline; it is a choice. You can *become* American. The "Who" is an open architectural platform.'''
    },
    2: {
        "q1": '''> **The Narrative of Inhabitant (The Who of the Where):**\n> The American Land is populated by the "Frontiersman." Usefulness in the wild supersedes ancestry. The "Where" demands a specific type of "Who": resilient, adaptable, and loosely tethered to the past.''',
        "q2": '''> **The Narrative of Property (The What of the Where):**\n> The Land is not just scenery; it is "Property." The American Definition of "Where" is ownership. Liberty is physically manifested in the fence line. To be free is to hold title.''',
        "q3": '''> **The Narrative of Geography (The Where of the Where):**\n> The "Where" is vast. The sheer scale of the continent enforces a psychology of "Abundance." There is always "West." The Land is defined by the possibility of Exit.''',
        "q4": '''> **The Narrative of Expansion (The Why of the Where):**\n> The Drive of the Land is "Manifest Destiny." The map is not a container but a command. We move to fill the void. Stagnation is death; expansion is the natural law of the Land.''',
        "q5": '''> **The Narrative of Infrastructure (The How of the Where):**\n> We conquer the "Where" through the Grid. The Railroad, the Highway, the Internet. The American Method reduces distance to time. We abolish the tyranny of space with speed.''',
        "q6": '''> **The Narrative of Territory (The Cause of the Where):**\n> The "Where" was bought with blood. The Origin of the Land is Conquest and Purchase. We hold the Land by right of Possession and Defense. The Map is a war trophy.''',
        "q7": '''> **The Narrative of Environment (The Effect of the Where):**\n> The "Where" shapes the Soul. The landscape creates the character. The vastness of the plains created the vastness of the ambition. We are the product of our continent.''',
        "total": '''> **The American Land is a Moving Target.**\n> It is not a fixed geography but a dynamic event. The "Where" is wherever we are. It is the physics of Liberty—space enough to run, space enough to build, space enough to be left alone.'''
    },
    3: {
        "q1": '''> **The Narrative of Author (The Who of the What):**\n> The Law is not divine; it is human. "We the People" are the Source. The Definition is written by the Defined. We are both the Ruler and the Ruled.''',
        "q2": '''> **The Narrative of Text (The What of the What):**\n> America is a Text. We are defined by the Document (Constitution). The "What" is the Word. We trust the Contract more than the King. The Identity is Logos-based.''',
        "q3": '''> **The Narrative of Jurisdiction (The Where of the What):**\n> The Law has specific boundaries. Federal vs State. Public vs Private. The Definition depends on the Domain. Freedom is finding the gap between Jurisdictions.''',
        "q4": '''> **The Narrative of Intent (The Why of the What):**\n> The Purpose of the Law is Liberty, not Order. The Definition exists to secure Rights, not to impose Duties. The "Why" limits the "What."''',
        "q5": '''> **The Narrative of Process (The How of the What):**\n> Due Process. The Definition must ideally be applied evenly. The "How" (Procedure) protects the "Who" (Citizen) from the "What" (State).''',
        "q6": '''> **The Narrative of Enactment (The Cause of the What):**\n> The Definition comes from Ratification. It is a generated consensus. The Cause of the Law is the Agreement of the Governed.''',
        "q7": '''> **The Narrative of Order (The Effect of the What):**\n> The Result is a "Government of Laws, not Men." Stability comes from the predictability of the Definition. We obey the Sign, not the Policeman.''',
        "total": '''> **The American Definition is a Contract.**\n> We exist as a nation only because we agreed to the terms in writing. The "What" is a legal fiction that became a reality through belief. We are a paper-based reality.'''
    },
    4: {
        "q1": '''> **The Narrative of Dreamer (The Who of the Why):**\n> The "Why" is personal. The Dreamer defines the Dream. No State can mandate a "National Purpose" that overrides the Individual's Pursuit. The Will is Sovereign.''',
        "q2": '''> **The Narrative of Ambition (The What of the Why):**\n> The "Why" is "More." A Better Life. A More Perfect Union. The substance of the drive is Improvement. We are allergic to the Status Quo.''',
        "q3": '''> **The Narrative of Destination (The Where of the Why):**\n> The "Why" is located in the Future. The American lives in "Tomorrow." The Present is merely a waiting room for the Future.''',
        "q4": '''> **The Narrative of Motion (The Why of the Why):**\n> We move because we must. Compulsion. The Drive is Autocatalytic. Success is not a resting place; it is a launchpad for the next anxiety.''',
        "q5": '''> **The Narrative of Bootstrap (The How of the Why):**\n> The Method of Drive is Self-Help. You must pull yourself up. No one is coming to save you. The "Why" is powered by the "I."''',
        "q6": '''> **The Narrative of Hunger (The Cause of the Why):**\n> The Drive is born of Lack. We are hungry. The Immigrant's hunger, the Pioneer's hunger. Satisfaction is the enemy of the Drive.''',
        "q7": '''> **The Narrative of Success (The Effect of the Why):**\n> The Proof of the Drive is Wealth/Happiness. The "Effect" validates the "Why." If you are not succeeding, your Drive is suspect. The American Gospel is Prosperity.''',
        "total": '''> **The American Drive is Infinite.**\n> It is the vector of pure Optimism. We believe that the Universe bends towards us if we push hard enough. Entropy is un-American. The "Why" is to win.'''
    },
    5: {
        "q1": '''> **The Narrative of Engineer (The Who of the How):**\n> The American is a Tinkerer. The Intellectual is suspect; the Mechanic is the hero. We trust the hand that builds over the mind that theorizes.''',
        "q2": '''> **The Narrative of Machine (The What of the How):**\n> The Method is Technology. We solve moral problems with machinery. The assembly line, the bulb, the bomb. The "What" is a Tool.''',
        "q3": '''> **The Narrative of Factory (The Where of the How):**\n> The "How" happens in the Shop. The Lab. The Garage. The Land of Method is the workplace. America is a Workshop.''',
        "q4": '''> **The Narrative of Efficiency (The Why of the How):**\n> Speed. Volume. Cost. The "Why" of the Method is "Faster, Cheaper, Better." We optimize existence.''',
        "q5": '''> **The Narrative of System (The How of the How):**\n> Standardization. The Method is replicable. Franchising. Mass Production. The "How" must scale. Uniqueness is inefficient.''',
        "q6": '''> **The Narrative of Invention (The Cause of the How):**\n> Necessity. We invent because we have a problem. The Cause of the Method is Friction. Conflict generates Innovation.''',
        "q7": '''> **The Narrative of Power (The Effect of the How):**\n> Dominance. Mastery over Nature. The Result of the Method is Control. We pave the wilderness and air-condition the desert.''',
        "total": '''> **The American Method is Engineering.**\n> We do not mediate on reality; we reconstruct it. If it is broken, fix it. If it works, scale it. The "How" is the supreme American virtue. We are a nation of Problem Solvers.'''
    },
    6: {
        "q1": '''> **The Narrative of Founder (The Who of the Cause):**\n> Giant Men. We are children of Titans. Washington, Jefferson, Lincoln. The Cause has a Face. We worship the Architects.''',
        "q2": '''> **The Narrative of Principles (The What of the Cause):**\n> Truths. Axioms. The Cause is not a Battle, but an Idea. The Revolution was Mental before it was Physical.''',
        "q3": '''> **The Narrative of Battleground (The Where of the Cause):**\n> Lexington. Yorktown. Gettysburg. The Cause is grounded in Sacred Soil. The History is mapped.''',
        "q4": '''> **The Narrative of Freedom (The Why of the Cause):**\n> Liberty or Death. The Cause is polarized. We fight not for land, but for a state of being. The "Why" is Absolute.''',
        "q5": '''> **The Narrative of Revolt (The How of the Cause):**\n> Rebellion. The Method of the Cause is to say "No." Disobedience is the engine of History. We started by firing on the police (Redcoats).''',
        "q6": '''> **The Narrative of Heritage (The Cause of the Cause):**\n> English Law. Providential History. The Cause stands on the shoulders of the Past. We refine the Western Tradition; we did not invent it ex nihilo.''',
        "q7": '''> **The Narrative of Independence (The Effect of the Cause):**\n> Separation. The Result of the Cause is Autonomy. We stand alone. The "Effect" is the cutting of ties.''',
        "total": '''> **The American Cause is Revolution.**\n> We are the Perpetual Rebels. Our Origin is a break from Authority. The "Cause" is the belief that the Current Order is always provisional and the Individual is always final.'''
    },
    7: {
        "q1": '''> **The Narrative of Star (The Who of the Effect):**\n> The Celebrity. The Icon. The "Who" becomes a Symbol. Determine the culture. The American is the Protagonist of the World Story.''',
        "q2": '''> **The Narrative of Brand (The What of the Effect):**\n> Coke. Hollywood. Democracy. The "What" is the Export. We ship our Culture in containers and MP3s. America is a Product.''',
        "q3": '''> **The Narrative of Empire (The Where of the Effect):**\n> Bases everywhere. The "Where" of the Effect is Global. The Sun never sets on the American Logo. Hegemony.''',
        "q4": '''> **The Narrative of Influence (The Why of the Effect):**\n> Soft Power. We want you to *want* to be like us. The "Why" is Attraction. Cultural Gravity.''',
        "q5": '''> **The Narrative of Media (The How of the Effect):**\n> The Screen. The Speaker. The Method of Impact is Broadcast. We shout louder than anyone else.''',
        "q6": '''> **The Narrative of History (The Cause of the Effect):**\n> The Century. The "Effect" is the result of winning the wars (Hot and Cold). We define the Effect because we survived the Cause.''',
        "q7": '''> **The Narrative of Globalization (The Effect of the Effect):**\n> Homogeneity. The World becomes Us. The Effect of America is the Americanization of Earth. Flattening.''',
        "total": '''> **The American Effect is Visibility.**\n> We are the Loudest Signal in the noise of history. You cannot ignore us. The "Effect" is pervasive. We are the atmosphere of the modern world.'''
    }
}

PLANES_CONFIG = {
    1: {"name": "Identity", "desc": "Who; Values of American Identity", "meta": '''> *"I celebrate myself, and sing myself, And what I assume you shall assume."*\n> — **Walt Whitman**, *Song of Myself*'''},
    2: {"name": "Land", "desc": "Where; Values of American Land", "meta": '''> *"The land was ours before we were the land's."*\n> — **Robert Frost**, *The Gift Outright*'''},
    3: {"name": "Definition", "desc": "What; Values of American Definition", "meta": '''> *"Proclaim Liberty throughout all the land unto all the inhabitants thereof."*\n> — **Leviticus 25:10** (Inscribed on the Liberty Bell)'''},
    4: {"name": "Drive", "desc": "Why; Values of American Drive", "meta": '''> *"Go West, young man, and grow up with the country."*\n> — **Horace Greeley**, 1865'''},
    5: {"name": "Method", "desc": "How; Values of American Method", "meta": '''> *"The difficult we do immediately. The impossible takes a little longer."*\n> — **US Army Corps of Engineers**, Slogan'''},
    6: {"name": "Cause", "desc": "Cause; Values of American Cause", "meta": '''> *"We hold these truths to be self-evident..."*\n> — **The Declaration of Independence**, 1776'''},
    7: {"name": "Effect", "desc": "Effect; Values of American Effect", "meta": '''> *"The world must be made safe for democracy."*\n> — **Woodrow Wilson**, 1917'''},
}

SENSE_INTROS = {
    "q1": "*Scanning the Metaphysical Reality of the Agent.*", # Placeholder options if extraction fails
    "q2": "*Scanning the Physical Reality.*",
    "q3": "*Scanning the Definition.*",
    "q4": "*Scanning the Motivation.*",
    "q5": "*Scanning the Method.*",
    "q6": "*Scanning the History.*",
    "q7": "*Scanning the Result.*"
}

def hard_reset():
    for num, config in PLANES_CONFIG.items():
        filename = f"American_Kanon_Plane_{num}_{config['name']}.md"
        filepath = os.path.join(SOURCE_DIR, filename)
        print(f"Hard Resetting {filename}...")
        
        # 1. Read File for ITEMS Only
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content_raw = f.read()
        else:
            print(f"Missing file {filepath}")
            continue
            
        # Parse items using robust regex
        # Capture: Label. **(Label)[Value]**; Quote... Paragraphs...
        # Identify based on start pattern.
        
        items_by_sense = { f"q{i}": [] for i in range(1,8) }
        
        # Split content into lines to manually process
        lines = content_raw.split('\n')
        
        current_sense = None
        current_item_buffer = []
        capture_buffer = False
        
        # Mapping Intros
        found_intros = {}
        
        for line in lines:
            line = line.replace("Locus", "Land").replace("locus", "land")
            
            # Sense Header
            if line.startswith("### Sense"):
                # Save previous item if any
                if current_item_buffer and current_sense:
                    items_by_sense[current_sense].append("\n".join(current_item_buffer))
                    current_item_buffer = []
                
                # Parse sense qX
                match = re.search(r'q(\d)', line)
                if match:
                    current_sense = f"q{match.group(1)}"
                continue
            
            # Intro Italics
            if line.strip().startswith("*Scanning") and current_sense:
                found_intros[current_sense] = line.strip()
                continue
                
            # Item Start
            # Matches: Word.Word.Word. **(
            item_start_match = re.match(r'^[\w\.]+\.\s*\*\*\([\w\.]+\)\[', line)
            if item_start_match:
                # New item start
                # Save previous item
                if current_item_buffer and current_sense:
                    items_by_sense[current_sense].append("\n".join(current_item_buffer))
                current_item_buffer = [line]
                capture_buffer = True
                continue
            
            # Narrative Start (Discard)
            if line.strip().startswith("> **The Narrative"):
                capture_buffer = False
                continue
            if line.strip().startswith("> **The American"): # Total narrative
                capture_buffer = False
                continue
            if "of Author" in line and "**" in line: # Garbage
                capture_buffer = False
                continue
            
            # If capturing item lines
            if capture_buffer:
                # Check if it's garbage narrative text
                if line.strip().startswith("> "):
                    # Is it a quote inside the item?
                    # Items often have a quote on the first line.
                    # Paragraphs describing items don't usually start with > unless quoting something.
                    # But narratives are ALL >.
                    # Heuristic: If we are deep in buffer and hit >, it's probably narrative trash unless it's short.
                    if "**The Narrative" in line:
                         capture_buffer = False
                         continue
                    # Assume items don't have blockquotes in their description usually?
                    # Actually they do: ; "Quote" ...
                    # But that's usually on the first line.
                    # Checking my items: They have description paragraphs.
                    pass
                
                # Filter specific garbage
                if line.strip().startswith("of ") and "**" in line: continue
                
                current_item_buffer.append(line)
        
        # Save last item
        if current_item_buffer and current_sense:
            items_by_sense[current_sense].append("\n".join(current_item_buffer))
            
        # 2. Rebuild File
        new_lines = []
        new_lines.append("# The American Kanon: ")
        new_lines.append(f"# Plane {config['desc']}")
        new_lines.append("")
        new_lines.append(config['meta'])
        new_lines.append("")
        new_lines.append(f"## THE PLANE OF {config['name'].upper()} ({config['desc'].split(';')[0].strip().upper()})")
        new_lines.append("*The Domain...*") # Default or extract? I'll leave placeholder details or simplistic.
        # Actually I need to keep the Preamble description.
        # It's usually Lines 12-13 in original.
        # "The Domain of the Agent..."
        # Extract it?
        domain_match = re.search(r'\n(## .*?\n\*.*?\*)', content_raw, re.DOTALL)
        if domain_match:
             # Use extracted header/desc
             pass # Already wrote header.
             # Just use the *Italics* part
             desc_lines = domain_match.group(1).split('\n')
             if len(desc_lines) > 1:
                 new_lines[-1] = desc_lines[1].replace("Locus", "Land") # *The Domain...*
        
        new_lines.append("")
        
        for q in range(1, 8):
            q_key = f"q{q}"
            q_header = ""
            # Reconstruct header title? 
            # I don't have the titles in config (e.g. "The Who of the Who").
            # Extract from original content "### Sense q1: ... "
            header_match = re.search(f'(### Sense {q_key}:.*)', content_raw)
            if header_match:
                q_header = header_match.group(1).replace("Locus", "Land")
            else:
                q_header = f"### Sense {q_key}: Unknown"
            
            new_lines.append(q_header)
            
            # Intro
            intro = found_intros.get(q_key, SENSE_INTROS.get(q_key, "")).replace("Locus", "Land")
            new_lines.append(intro)
            new_lines.append("")
            
            # Items
            # Deduplicate items (set of strings)
            unique_items = []
            seen_labels = set()
            for item_block in items_by_sense[q_key]:
                # Extract Label for dedupe
                lbl_match = re.match(r'([\w\.]+)', item_block)
                if lbl_match:
                    lbl = lbl_match.group(1)
                    if lbl not in seen_labels:
                        seen_labels.add(lbl)
                        unique_items.append(item_block.strip())
            
            for item in unique_items:
                new_lines.append(item)
                new_lines.append("")
            
            # Narrative (Correct One)
            if q_key in NARRATIVES[num]:
                new_lines.append(NARRATIVES[num][q_key])
                new_lines.append("")
            
            new_lines.append("")
            
        # Total Narrative
        if "total" in NARRATIVES[num]:
            new_lines.append(NARRATIVES[num]["total"])
            new_lines.append("")
            
        # Write
        final_content = "\n".join(new_lines)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_content)

if __name__ == "__main__":
    hard_reset()
