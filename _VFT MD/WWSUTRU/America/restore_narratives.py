import re
import os
import glob

SOURCE_DIR = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America"

# Source of Truth from previous step
NARRATIVES = {
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

PLANES_INFO = {
    2: "Land",
    3: "Definition",
    4: "Drive",
    5: "Method",
    6: "Cause",
    7: "Effect"
}

def restore_narratives():
    for num, name in PLANES_INFO.items():
        filename = f"American_Kanon_Plane_{num}_{name}.md"
        filepath = os.path.join(SOURCE_DIR, filename)
        
        print(f"Restoring {filename}...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split by Header like before, but this time we are aggressive
        chunks = re.split(r'(### Sense q\d:.*)', content)
        
        new_chunks = []
        new_chunks.append(chunks[0]) # Preamble (assuming it was fixed by reconstruct_planes or we trust it)
        
        for i in range(1, len(chunks), 2):
            header = chunks[i]
            body = chunks[i+1]
            
            # Extract the 'q' number from header
            q_num = header.split(':')[0].split(' ')[-1] # q1
            
            # Target Narrative Lines
            target_narrative = NARRATIVES[num].get(q_num, "")
            target_lines = [l.strip() for l in target_narrative.split('\n') if l.strip().startswith('>')]
            
            lines = body.split('\n')
            clean_lines = []
            
            # We want to keep Items (Label....) and Intro (*Scanning...*) and spacing.
            # We want to remove lines that look like Narrative Headers OR Narrative Text.
            
            for line in lines:
                s_line = line.strip()
                if s_line == "": 
                    clean_lines.append(line)
                    continue
                
                # Check for explicit garbage
                if ("of Author" in s_line and "**" in s_line) or \
                   ("of Inhabitant" in s_line and "**" in s_line) or \
                   ("of Property" in s_line and "**" in s_line) or \
                   ("of Geography" in s_line and "**" in s_line) or \
                   ("of Expansion" in s_line and "**" in s_line) or \
                   ("of Infrastructure" in s_line and "**" in s_line) or \
                   ("of Territory" in s_line and "**" in s_line) or \
                   ("of Environment" in s_line and "**" in s_line) or \
                   ("of Text" in s_line and "**" in s_line) or \
                   ("of Jurisdiction" in s_line and "**" in s_line) or \
                   ("of Intent" in s_line and "**" in s_line) or \
                   ("of Process" in s_line and "**" in s_line) or \
                   ("of Enactment" in s_line and "**" in s_line) or \
                   ("of Order" in s_line and "**" in s_line) or \
                   ("> **The Narrative" in s_line):
                    continue
                
                # Check for loose narrative body duplicates
                # If the line matches one of the target_lines exactly (ignoring whitespace), skip it.
                # BUT be careful not to skip items if they look like narratives (unlikely).
                is_duplicate_text = False
                for t_line in target_lines:
                    if s_line == t_line or s_line == t_line.replace('> ', '>'): # Flexible matching
                        is_duplicate_text = True
                        break
                if is_duplicate_text:
                    continue
                
                clean_lines.append(line)
            
            new_body = "\n".join(clean_lines).strip()
            
            new_chunks.append(header)
            new_chunks.append("\n" + new_body + "\n\n" + target_narrative + "\n")

        # Total Narrative
        # Append at the very end
        new_last_block = new_chunks[-1]
        
        # Clean up any existing total narrative traces in the last chunk?
        # The item extraction logic above stops at EOF, so it might capture the total narrative as part of the last item description if we aren't careful.
        # But we replaced "> The American..." so it should be gone.
        
        # Checking last item of last sense...
        # If the last item's description captured the garbage, it's still there.
        # We need to aggressively prune the end of the last item.
        
        final_text = "".join(new_chunks)
        
        # Add Total
        if "total" in NARRATIVES[num]:
            final_text += "\n\n" + NARRATIVES[num]["total"] + "\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_text)

if __name__ == "__main__":
    restore_narratives()
