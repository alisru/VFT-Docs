import re
import sys
import json
import hashlib

def calculate_moral_will_vectors(text):
    # simple heuristic based on Alethekanon dictionary
    psi = 0.0 # Will
    up = 0.0 # Moral
    text_lower = text.lower()
    
    # +psi (Proactive/Create)
    psi += text_lower.count('free') * 0.2
    psi += text_lower.count('liberty') * 0.2
    psi += text_lower.count('right') * 0.1
    psi += text_lower.count('power') * 0.2
    psi += text_lower.count('build') * 0.1
    psi += text_lower.count('create') * 0.1
    psi += text_lower.count('drive') * 0.1
    psi -= text_lower.count('prevent') * 0.2
    psi -= text_lower.count('stop') * 0.1
    psi -= text_lower.count('limit') * 0.1
    psi -= text_lower.count('restrict') * 0.1
    
    # +up (Universal Benefit)
    up += text_lower.count('all') * 0.1
    up += text_lower.count('equal') * 0.2
    up += text_lower.count('justice') * 0.2
    up += text_lower.count('union') * 0.1
    up += text_lower.count('public') * 0.1
    up -= text_lower.count('self') * 0.1
    up -= text_lower.count(' me ') * 0.1
    up -= text_lower.count(' my ') * 0.1
    up -= text_lower.count('private') * 0.1
    
    psi = max(-2.0, min(2.0, psi))
    up = max(-2.0, min(2.0, up))
    return up, psi

def analyze_item(plane_tuple, title, quote, author, desc):
    up, psi = calculate_moral_will_vectors(desc)
    
    # Model 2: Wisdom Metric (Wisdom = 1 / (1 + ΔH))
    # ΔH = Hypocrisy Gap
    delta_h = abs(psi - up) * 0.3
    wisdom = 1.0 / (1.0 + delta_h)
    
    # Model 9: Quadrant
    quadrant = "TL (Greater Good)" if up >= 0 and psi >= 0 else \
               "TR (Greatest Lie)" if up < 0 and psi >= 0 else \
               "BL (Lesser Good)" if up >= 0 and psi < 0 else \
               "BR (Greater Evil)"
               
    # Protocol formatting
    analysis = f"### {plane_tuple} {title}\n"
    analysis += f"> *{quote}* - {author}\n\n"
    
    analysis += "**[DIAGNOSTICS]**\n"
    analysis += f"- **Mode**: ANALYSE\n"
    analysis += f"- **Model 1 (Vectors)**: υ={up:.2f} (Moral), ψ={psi:.2f} (Will) -> Quadrant: {quadrant}\n"
    analysis += f"- **Model 2 (Wisdom)**: {wisdom:.2f} (ΔH={delta_h:.2f})\n"
    if wisdom < 0.7:
         analysis += f"- **Model 4 (Deception)**: High Strain detected. Possible Bait & Switch.\n"
    else:
         analysis += f"- **Model 4 (Deception)**: Low Strain. Structural Integrity Maintained.\n"
         
    # Synthesis -> Mechanics -> Implication
    analysis += "\n**Synthesis**: "
    plane_parts = plane_tuple.split('.')
    if len(plane_parts) >= 3:
        analysis += f"The {plane_parts[0]} plane interlocks with the {plane_parts[1]} sense via {plane_parts[2]} use. This text grounds American identity in a specific vector of operation.\n\n"
    else:
        analysis += f"The {plane_tuple} vector establishes a core condition of American realism.\n\n"
        
    analysis += "**Mechanics**:\n"
    analysis += f"- **Driver**: The text exhibits a Will (ψ) of {psi:.2f}, indicating a {'proactive' if psi >=0 else 'suppressive'} force.\n"
    analysis += f"- **Beneficiary**: The Moral (υ) vector of {up:.2f} points toward {'universal' if up >=0 else 'self'} benefit.\n"
    analysis += f"- **Coherence**: The Wisdom metric ({wisdom:.2f}) indicates the degree of alignment between stated purpose and actual function.\n\n"
    
    analysis += "**Implication**: "
    analysis += f"When the system operates with υ={up:.2f} and ψ={psi:.2f}, the inevitable result is {quadrant}. "
    if up >= 0:
        analysis += "The structure supports the collective without immediately crushing the individual. "
    else:
        analysis += "The abstraction serves the individual at the cost of the collective. "
        
    analysis += "The agent who internalizes this definition acts as a sovereign node within the republic.\n\n"
    analysis += "---\n\n"
    return analysis
    
def main():
    try:
        with open(r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America\American_Kanon_Full_343.md", "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print("Error reading file:", e)
        return

    # Regex to match items: (Who.Who.Who) Self-Evidence; "We hold these truths..." - Thomas Jefferson. Declaration...
    pattern = re.compile(r"^\(([A-Za-z.]+)\)\s+(.*?);\s+\"(.*?)\"\s+-\s+(.*?)$", re.MULTILINE)
    
    items = []
    lines = content.split('\n')
    current_item = None
    
    for line in lines:
        match = pattern.match(line)
        if match:
            if current_item:
                items.append(current_item)
            current_item = {
                'plane': match.group(1),
                'title': match.group(2),
                'quote': match.group(3),
                'author': match.group(4),
                'desc': ""
            }
        elif current_item and (line.startswith(' ') or line.startswith('\t')):
            current_item['desc'] += line.strip() + " "
            
    if current_item:
        items.append(current_item)
        
    out_path = r"e:\Vector Field Theory\VFT Docs\_AI files and chat logs\American_Kanon_343_Analysis.md"
    
    with open(out_path, "w", encoding="utf-8") as out:
        out.write("# Alethekanon Full Spectrum Scan: American Kanon 343\n\n")
        out.write("> *[DIAGNOSTICS] MODE=ANALYSE, MODELS=1,2,4,9, DEPTH=MAX*\n\n")
        out.write("This document contains the automated Alethekanon extraction and judgment of all identified Kanon items.\n\n")
        
        for item in items:
            analysis = analyze_item(item['plane'], item['title'], item['quote'], item['author'], item['desc'])
            out.write(analysis)
            
    print(f"Processed {len(items)} items. Output saved to {out_path}.")
    
if __name__ == '__main__':
    main()
