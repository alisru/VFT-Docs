import re
import os

BASE_DIR = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America"

PLANES = {
    1: {"name": "Identity", "interrogative": "Who"},
    2: {"name": "Land", "interrogative": "Where"},
    3: {"name": "Definition", "interrogative": "What"},
    4: {"name": "Drive", "interrogative": "Why"},
    5: {"name": "Method", "interrogative": "How"},
    6: {"name": "Cause", "interrogative": "Cause"},
    7: {"name": "Effect", "interrogative": "Effect"}
}

META_QUOTES = {
    2: '''> *"The land was ours before we were the land's."*\n> — **Robert Frost**, *The Gift Outright*''',
    3: '''> *"Proclaim Liberty throughout all the land unto all the inhabitants thereof."*\n> — **Leviticus 25:10** (Inscribed on the Liberty Bell)''',
    4: '''> *"The only thing we have to fear is fear itself."*\n> — **Franklin D. Roosevelt**, *First Inaugural Address*''',
    5: '''> *"The business of America is business."*\n> — **Calvin Coolidge**, *Address to Newspaper Editors*''',
    6: '''> *"The earth belongs in usufruct to the living... the dead have neither powers nor rights over it."*\n> — **Thomas Jefferson**, *Letter to James Madison*''',
    7: '''> *"We shall be as a city upon a hill, the eyes of all people are upon us."*\n> — **John Winthrop**, *A Model of Christian Charity*'''
}

NARRATIVES = {
    2: {
        "q1": '''> **The Narrative of Inhabitant (The Who of the Where):**\n> The American Locus is populated by the "Frontiersman." Usefulness in the wild supersedes ancestry. The "Where" demands a specific type of "Who": resilient, adaptable, and loosely tethered to the past.\n''',
        "q2": '''> **The Narrative of Property (The What of the Where):**\n> The Land is not just scenery; it is "Property." The American Definition of "Where" is ownership. Liberty is physically manifested in the fence line. To be free is to hold title.\n''',
        "q3": '''> **The Narrative of Geography (The Where of the Where):**\n> The "Where" is vast. The sheer scale of the continent enforces a psychology of "Abundance." There is always "West." The Locus is defined by the possibility of Exit.\n''',
        "q4": '''> **The Narrative of Expansion (The Why of the Where):**\n> The Drive of the Locus is "Manifest Destiny." The map is not a container but a command. We move to fill the void. Stagnation is death; expansion is the natural law of the Locus.\n''',
        "q5": '''> **The Narrative of Infrastructure (The How of the Where):**\n> We conquer the "Where" through the Grid. The Railroad, the Highway, the Internet. The American Method reduces distance to time. We abolish the tyranny of space with speed.\n''',
        "q6": '''> **The Narrative of Territory (The Cause of the Where):**\n> The "Where" was bought with blood. The Origin of the Land is Conquest and Purchase. We hold the Locus by right of Possession and Defense. The Map is a war trophy.\n''',
        "q7": '''> **The Narrative of Environment (The Effect of the Where):**\n> The "Where" shapes the Soul. The landscape creates the character. The vastness of the plains created the vastness of the ambition. We are the product of our continent.\n''',
        "total": '''> **The American Land is a Moving Target.**\n> It is not a fixed geography but a dynamic event. The "Where" is wherever we are. It is the physics of Liberty—space enough to run, space enough to build, space enough to be left alone.\n'''
    },
    3: {
        "q1": '''> **The Narrative of Author (The Who of the What):**\n> The Law is not divine; it is human. "We the People" are the Source. The Definition is written by the Defined. We are both the Ruler and the Ruled.\n''',
        "q2": '''> **The Narrative of Text (The What of the What):**\n> America is a Text. We are defined by the Document (Constitution). The "What" is the Word. We trust the Contract more than the King. The Identity is Logos-based.\n''',
        "q3": '''> **The Narrative of Jurisdiction (The Where of the What):**\n> The Law has specific boundaries. Federal vs State. Public vs Private. The Definition depends on the Domain. Freedom is finding the gap between Jurisdictions.\n''',
        "q4": '''> **The Narrative of Intent (The Why of the What):**\n> The Purpose of the Law is Liberty, not Order. The Definition exists to secure Rights, not to impose Duties. The "Why" limits the "What."\n''',
        "q5": '''> **The Narrative of Process (The How of the What):**\n> Due Process. The Definition must ideally be applied evenly. The "How" (Procedure) protects the "Who" (Citizen) from the "What" (State).\n''',
        "q6": '''> **The Narrative of Enactment (The Cause of the What):**\n> The Definition comes from Ratification. It is a generated consensus. The Cause of the Law is the Agreement of the Governed.\n''',
        "q7": '''> **The Narrative of Order (The Effect of the What):**\n> The Result is a "Government of Laws, not Men." Stability comes from the predictability of the Definition. We obey the Sign, not the Policeman.\n''',
        "total": '''> **The American Definition is a Contract.**\n> We exist as a nation only because we agreed to the terms in writing. The "What" is a legal fiction that became a reality through belief. We are a paper-based reality.\n'''
    },
    4: {
        "q1": '''> **The Narrative of Dreamer (The Who of the Why):**\n> The "Why" is personal. The Dreamer defines the Dream. No State can mandate a "National Purpose" that overrides the Individual's Pursuit. The Will is Sovereign.\n''',
        "q2": '''> **The Narrative of Ambition (The What of the Why):**\n> The "Why" is "More." A Better Life. A More Perfect Union. The substance of the drive is Improvement. We are allergic to the Status Quo.\n''',
        "q3": '''> **The Narrative of Destination (The Where of the Why):**\n> The "Why" is located in the Future. The American lives in "Tomorrow." The Present is merely a waiting room for the Future.\n''',
        "q4": '''> **The Narrative of Motion (The Why of the Why):**\n> We move because we must. Compulsion. The Drive is Autocatalytic. Success is not a resting place; it is a launchpad for the next anxiety.\n''',
        "q5": '''> **The Narrative of Bootstrap (The How of the Why):**\n> The Method of Drive is Self-Help. You must pull yourself up. No one is coming to save you. The "Why" is powered by the "I."\n''',
        "q6": '''> **The Narrative of Hunger (The Cause of the Why):**\n> The Drive is born of Lack. We are hungry. The Immigrant's hunger, the Pioneer's hunger. Satisfaction is the enemy of the Drive.\n''',
        "q7": '''> **The Narrative of Success (The Effect of the Why):**\n> The Proof of the Drive is Wealth/Happiness. The "Effect" validates the "Why." If you are not succeeding, your Drive is suspect. The American Gospel is Prosperity.\n''',
        "total": '''> **The American Drive is Infinite.**\n> It is the vector of pure Optimism. We believe that the Universe bends towards us if we push hard enough. Entropy is un-American. The "Why" is to win.\n'''
    },
    5: {
        "q1": '''> **The Narrative of Engineer (The Who of the How):**\n> The American is a Tinkerer. The Intellectual is suspect; the Mechanic is the hero. We trust the hand that builds over the mind that theorizes.\n''',
        "q2": '''> **The Narrative of Machine (The What of the How):**\n> The Method is Technology. We solve moral problems with machinery. The assembly line, the bulb, the bomb. The "What" is a Tool.\n''',
        "q3": '''> **The Narrative of Factory (The Where of the How):**\n> The "How" happens in the Shop. The Lab. The Garage. The Locus of Method is the workplace. America is a Workshop.\n''',
        "q4": '''> **The Narrative of Efficiency (The Why of the How):**\n> Speed. Volume. Cost. The "Why" of the Method is "Faster, Cheaper, Better." We optimize existence.\n''',
        "q5": '''> **The Narrative of System (The How of the How):**\n> Standardization. The Method is replicable. Franchising. Mass Production. The "How" must scale. Uniqueness is inefficient.\n''',
        "q6": '''> **The Narrative of Invention (The Cause of the How):**\n> Necessity. We invent because we have a problem. The Cause of the Method is Friction. Conflict generates Innovation.\n''',
        "q7": '''> **The Narrative of Power (The Effect of the How):**\n> Dominance. Mastery over Nature. The Result of the Method is Control. We pave the wilderness and air-condition the desert.\n''',
        "total": '''> **The American Method is Engineering.**\n> We do not mediate on reality; we reconstruct it. If it is broken, fix it. If it works, scale it. The "How" is the supreme American virtue. We are a nation of Problem Solvers.\n'''
    },
    6: {
        "q1": '''> **The Narrative of Founder (The Who of the Cause):**\n> Giant Men. We are children of Titans. Washington, Jefferson, Lincoln. The Cause has a Face. We worship the Architects.\n''',
        "q2": '''> **The Narrative of Principles (The What of the Cause):**\n> Truths. Axioms. The Cause is not a Battle, but an Idea. The Revolution was Mental before it was Physical.\n''',
        "q3": '''> **The Narrative of Battleground (The Where of the Cause):**\n> Lexington. Yorktown. Gettysburg. The Cause is grounded in Sacred Soil. The History is mapped.\n''',
        "q4": '''> **The Narrative of Freedom (The Why of the Cause):**\n> Liberty or Death. The Cause is polarized. We fight not for land, but for a state of being. The "Why" is Absolute.\n''',
        "q5": '''> **The Narrative of Revolt (The How of the Cause):**\n> Rebellion. The Method of the Cause is to say "No." Disobedience is the engine of History. We started by firing on the police (Redcoats).\n''',
        "q6": '''> **The Narrative of Heritage (The Cause of the Cause):**\n> English Law. Providential History. The Cause stands on the shoulders of the Past. We refine the Western Tradition; we did not invent it ex nihilo.\n''',
        "q7": '''> **The Narrative of Independence (The Effect of the Cause):**\n> Separation. The Result of the Cause is Autonomy. We stand alone. The "Effect" is the cutting of ties.\n''',
        "total": '''> **The American Cause is Revolution.**\n> We are the Perpetual Rebels. Our Origin is a break from Authority. The "Cause" is the belief that the Current Order is always provisional and the Individual is always final.\n'''
    },
    7: {
        "q1": '''> **The Narrative of Star (The Who of the Effect):**\n> The Celebrity. The Icon. The "Who" becomes a Symbol. Determine the culture. The American is the Protagonist of the World Story.\n''',
        "q2": '''> **The Narrative of Brand (The What of the Effect):**\n> Coke. Hollywood. Democracy. The "What" is the Export. We ship our Culture in containers and MP3s. America is a Product.\n''',
        "q3": '''> **The Narrative of Empire (The Where of the Effect):**\n> Bases everywhere. The "Where" of the Effect is Global. The Sun never sets on the American Logo. Hegemony.\n''',
        "q4": '''> **The Narrative of Influence (The Why of the Effect):**\n> Soft Power. We want you to *want* to be like us. The "Why" is Attraction. Cultural Gravity.\n''',
        "q5": '''> **The Narrative of Media (The How of the Effect):**\n> The Screen. The Speaker. The Method of Impact is Broadcast. We shout louder than anyone else.\n''',
        "q6": '''> **The Narrative of History (The Cause of the Effect):**\n> The Century. The "Effect" is the result of winning the wars (Hot and Cold). We define the Effect because we survived the Cause.\n''',
        "q7": '''> **The Narrative of Globalization (The Effect of the Effect):**\n> Homogeneity. The World becomes Us. The Effect of America is the Americanization of Earth. Flattening.\n''',
        "total": '''> **The American Effect is Visibility.**\n> We are the Loudest Signal in the noise of history. You cannot ignore us. The "Effect" is pervasive. We are the atmosphere of the modern world.\n'''
    }
}

def refine_planes():
    for plane_num in range(2, 8): # Skip Plane 1 as it is done
        plane_name = PLANES[plane_num]["name"]
        plane_interrogative = PLANES[plane_num]["interrogative"]
        
        filename = f"American_Kanon_Plane_{plane_num}_{plane_name}.md"
        filepath = os.path.join(BASE_DIR, filename)
        
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            continue
            
        print(f"Refining Plane {plane_num}: {plane_name}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')
        new_lines = []
        
        header_updated = False
        current_sense = None
        
        for line in lines:
             # Header Update: # The American Kanon: Plane X Values of American Name
            if line.startswith("# ") and "Values of American" in line and not header_updated:
                 new_lines.append(f"# The American Kanon: ")
                 new_lines.append(f"# Plane {plane_interrogative}; Values of American {plane_name}")
                 # Insert Meta Quote
                 if plane_num in META_QUOTES:
                     new_lines.append("")
                     new_lines.append(META_QUOTES[plane_num])
                     new_lines.append("")
                 header_updated = True
                 continue
            
            # Sense Header Check
            sense_match = re.match(r'### Sense (q\d):', line)
            if sense_match:
                 # Append narrative for PREVIOUS sense
                 if current_sense and plane_num in NARRATIVES and current_sense in NARRATIVES[plane_num]:
                     new_lines.append(NARRATIVES[plane_num][current_sense])
                     new_lines.append("")
                
                 current_sense = sense_match.group(1)
                 new_lines.append(line)
                 continue
            
            # Item Replacement
            # Pattern: 15. **(Label)[Value]** -> Label. **(Label)[Value]**
            item_match = re.search(r'^\d+\.\s*\*\*\(([^)]+)\)(\[.*?\])\*\*', line)
            if item_match:
                label = item_match.group(1)
                new_line = re.sub(r'^\d+\.\s*', f'{label}. ', line)
                new_lines.append(new_line)
                continue
            
            # Keep other lines as is (unless it's the old header)
            if line.startswith("# ") and "Values of American" in line:
                continue # Skip old header if not matched exactly above (safety)
            
            new_lines.append(line)
        
        # Append final sense narrative
        if current_sense and plane_num in NARRATIVES and current_sense in NARRATIVES[plane_num]:
            new_lines.append(NARRATIVES[plane_num][current_sense])
            
        # Append Total Summary
        if plane_num in NARRATIVES and "total" in NARRATIVES[plane_num]:
            new_lines.append("")
            new_lines.append(NARRATIVES[plane_num]["total"])
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(new_lines))

if __name__ == "__main__":
    refine_planes()
