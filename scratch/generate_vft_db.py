import os
import csv
import re

summaries_path = r'e:\Vector Field Theory\VFT Docs\file_summaries.md'
csv_output_path = r'e:\Vector Field Theory\VFT Docs\_AI files and chat logs\vft_io_database.csv'

# Triadic Nodes
virtues = [
    "Maths (Order)", "Spirituality (Faith)", "Religion (Charity)", "Intelligence (Hope)",
    "Physics (Objectivity)", "Meta-Physics (Imagination)", "Emotional-physics (Temperance)", "Learning (Prudence)",
    "Society (Community)", "Sociology (Empathy)", "Internal Judgment (Justice)", "The World (Fortitude)",
    "Psychology (Understanding)", "Language (Connection)", "History (Context)", "Reality (Truth)"
]

vices = [
    "Chaos (Structurelessness)", "Nihilism (Nothing)", "Hatred (Ill-Will)", "Despair (Negative Conviction)",
    "Denial (Rejection of Fact)", "Dogma (Closed Mind)", "Indulgence (Lack of Control)", "Folly (Willful Ignorance)",
    "Anarchy (Dissolution)", "Apathy (Inability to Care)", "Corruption (Perversion)", "Cowardice (Refusal to Facts)",
    "Confusion (Self-Ignorance)", "Deceit (Ill-Will)", "Erasure (Denial of Record)", "Delusion (The Greater Lie)"
]

nodes = virtues + vices

# 7 Planes
planes = ["Q1 WHO", "Q2 WHAT", "Q3 WHERE", "Q4 WHY", "Q5 HOW", "Q6 CAUSE", "Q7 EFFECT"]

def categorize_file(filename, content):
    filename_lower = filename.lower()
    content_lower = content.lower()
    
    assigned_planes = []
    assigned_nodes = []
    tags = []
    
    # Plane logic (Very basic heuristics)
    if any(k in filename_lower for k in ["who", "identity", "prophet", "self", "soul"]): assigned_planes.append("Q1 WHO")
    if any(k in filename_lower for k in ["what", "possible", "potential", "theory", "paper"]): assigned_planes.append("Q2 WHAT")
    if any(k in filename_lower for k in ["where", "physical", "map", "geometry", "levant"]): assigned_planes.append("Q3 WHERE")
    if any(k in filename_lower for k in ["why", "meaning", "purpose", "belief", "goal"]): assigned_planes.append("Q4 WHY")
    if any(k in filename_lower for k in ["how", "method", "protocol", "engine", "calculator"]): assigned_planes.append("Q5 HOW")
    if any(k in filename_lower for k in ["cause", "history", "origin", "vivisection", "archaic"]): assigned_planes.append("Q6 CAUSE")
    if any(k in filename_lower for k in ["effect", "result", "outcome", "emotive", "traversal"]): assigned_planes.append("Q7 EFFECT")
    
    # Node logic (Basic string matches)
    for node in nodes:
        node_core = node.split(' (')[0].lower()
        if node_core in filename_lower or node_core in content_lower[:500]:
            assigned_nodes.append(node)
            
    # Dynamic Tags from folder/keywords
    if "astrology" in filename_lower: tags.append("Astrology")
    if "legal" in filename_lower: tags.append("Legal")
    if "politics" in filename_lower: tags.append("Politics")
    if "consciousness" in filename_lower: tags.append("Consciousness")
    if "economic" in filename_lower or "price" in filename_lower: tags.append("Economics")

    return assigned_planes, assigned_nodes, tags

def process():
    with open(summaries_path, 'r', encoding='utf-8') as f:
        full_text = f.read()
    
    # Split into entries (### [Filename] ([Date]))
    entries = re.split(r'\n(?=### )', full_text)
    
    data = []
    
    for entry in entries:
        if not entry.strip() or not entry.startswith('###'): continue
        
        lines = entry.split('\n')
        header_match = re.search(r'### (.*?) \((.*?)\)', lines[0])
        if not header_match: continue
        
        filename = header_match.group(1).strip()
        date = header_match.group(2).strip()
        
        path = ""
        summary = ""
        is_summary = False
        
        for line in lines:
            if line.startswith('**Path**:'):
                path = line.replace('**Path**: ', '').strip()
            elif line.startswith('**Summary**:'):
                is_summary = True
                continue
            
            if is_summary:
                summary += line.strip() + " "
        
        # Categorize
        assigned_planes, assigned_nodes, tags = categorize_file(filename, summary)
        
        data.append({
            'Filename': filename,
            'CreationDate': date,
            'PlaneCategory': "; ".join(assigned_planes),
            'NodeCategory': "; ".join(assigned_nodes),
            'DetailedTags': "; ".join(tags),
            'Path': path,
            'SummaryAE-C': summary.strip()
        })
        
    # Write CSV
    with open(csv_output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Generated CSV with {len(data)} entries.")

if __name__ == "__main__":
    process()
