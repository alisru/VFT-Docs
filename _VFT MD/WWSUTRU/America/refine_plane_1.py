import re

FILE_PATH = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America\American_Kanon_Plane_1_Identity.md"

# Narratives for each Sense (q1-q7) and Total
NARRATIVES = {
    "q1": """\n> **The Narrative of Agent (The Who of the Who):**\n> The American Identity begins as an assertion of Sovereignty. The American is not a subject but a source of authority. By declaring the self "Self-Evident," they deny the power of the State to define them. The Soul is a pre-political axiom.\n""",
    "q2": """\n> **The Narrative of Role (The What of the Who):**\n> The American becomes a "Citizen" not by blood, but by Contract and Competence. "What" they are is defined by "Value Created," not "Status Inherited." The American is a machine for Merit, defined by the "High" of their Ambition and the "Low" of their Origins.\n""",
    "q3": """\n> **The Narrative of Tribe (The Where of the Who):**\n> The American is a Paradox of Unity. They are solitary frontiersmen who bind themselves into a Union. The Tribe is not a hive, but a voluntary association of free atoms. We are "Many" in origin, but "One" in Locus.\n""",
    "q4": """\n> **The Narrative of Drive (The Why of the Who):**\n> The American is fueled by "More." The pursuit of Happiness is an infinite vector. They are an engine of Optimism that consumes the Future to power the Present. The "Why" is a religious belief in a Better Tomorrow.\n""",
    "q5": """\n> **The Narrative of Character (The How of the Who):**\n> The American is a Pragmatist. They care less for "Truth" than for "what works." Their character is built on the efficiency of honesty and simple, strenuous action. To be "American" is to be "Busy."\n""",
    "q6": """\n> **The Narrative of Origin (The Cause of the Who):**\n> The American is the eternal Immigrant. Even if born on the soil, they identify as one who "Left the Old World." They are born from a Revolution against the Past. Our Tradition is the overthrow of Tradition.\n""",
    "q7": """\n> **The Narrative of Status (The Effect of the Who):**\n> The American is a Beacon. Their existence forces a choice on the rest of the world: to emulate or to reject. To be American is to be Visible; we are the "Proof of Concept" for human liberty.\n""",
    "total": """\n---\n\n### **Summary of the Identity**\n> **The American is a Sovereign Agent who defines themselves through Action.** They reject the fatality of history in favor of the plasticity of the future. The "Who" is a self-made construct, validated by its Utility and sanctified by its Liberty. We are not who we *are*; we are who we *make ourselves*.\n"""
}

META_QUOTE = """
> *"I celebrate myself, and sing myself, And what I assume you shall assume."*  
> — **Walt Whitman**, *Song of Myself*

"""

def refine_plane():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    new_lines = []
    
    # Insert Meta Quote after Header
    header_found = False
    
    current_sense = None
    
    for line in lines:
        # Check for Sense Header
        sense_match = re.match(r'### Sense (q\d):', line)
        if sense_match:
            # If we were in a sense, append its narrative (handling end of previous block)
            # Actually, standard parsing: The narrative goes at the END of the block.
            # So if we hit a new HEADER, we should have appended the previous narrative.
            # But simpler: Just append Narrative immediately before the NEXT Sense Header? 
            # Or insert at the end of the file/block logic.
             if current_sense:
                 new_lines.append(NARRATIVES[current_sense])
                 new_lines.append("") # Spacer
            
             current_sense = sense_match.group(1)
             new_lines.append(line)
             continue
             
        # Check for Item Number to Replace
        # Pattern: 1. **(Who.Who.Who)[label]**
        # User wants: Who.Who.Who. **(Who.Who.Who)[label]**
        # The regex needs to capture the label inside the parens
        item_match = re.search(r'^\d+\.\s*\*\*\(([^)]+)\)(\[.*?\])\*\*', line)
        if item_match:
            label = item_match.group(1) # Who.Who.Who
            rest = item_match.group(2) # [Self-Evidence]
            # Reconstruct
            # Find the position of the bold start
            # actually just replace the start
            new_line = re.sub(r'^\d+\.\s*', f'{label}. ', line)
            new_lines.append(new_line)
            continue
            
        # Add Meta Quote after Title
        if line.startswith("# Plane Who") and not header_found:
            new_lines.append(line)
            new_lines.append(META_QUOTE)
            header_found = True
            continue

        new_lines.append(line)
    
    # Append final sense narrative
    if current_sense:
        new_lines.append(NARRATIVES[current_sense])
    
    # Append Total Summary
    new_lines.append(NARRATIVES["total"])
    
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(new_lines))

if __name__ == "__main__":
    refine_plane()
