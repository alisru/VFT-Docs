import json
import os

# Configuration
json_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Collapse\Taxonomy\Matrix_Ground_Truth.json"
output_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Collapse\Taxonomy\The_7x7x7_Collapse_Matrix.md"

def load_data():
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_markdown(data):
    lines = []
    
    # Header with Explanation
    lines.append("# The 7x7x7 Matrix of State Failure: The Geometry of Ruin (Master)")
    lines.append("")
    lines.append("**Analyst:** Alethekanon")
    lines.append("**Resolution:** Level 3 (343 Vectors)")
    lines.append("**Structure:** The Fractal Decomposition of Collapse via the 7 Interrogatives.")
    lines.append("")
    lines.append("The following matrix maps the disintegration of a civilization across 7 Planes of Reality (The Context), 7 Scales of Governance (The State), and 7 Descriptions of Ruin (The Vector).")
    lines.append("Using the Interrogative Ontology (Who, What, Where, Why, How, Cause, Effect), we diagnose the precise 'Mechanism of Ruin' at every level of the fractal stack.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Sort Planes by Canonical ID (1-7)
    planes = data["Tree"]["Planes"]
    sorted_plane_ids = sorted(planes.keys(), key=lambda x: int(x))

    # Canonical Titles Map
    plane_titles = {
        "1": "WHO? (The Bio-Physical/Identity Foundation)",
        "2": "WHAT? (The Possible/Definitional Foundation)",
        "3": "WHERE? (The Physical/Territorial Foundation)",
        "4": "WHY? (The Lyrical/Moral Foundation)",
        "5": "HOW? (The Logical/Methodological Foundation)",
        "6": "CAUSE? (The Historical Foundation)",
        "7": "EFFECT? (The Emotive/Global Foundation)"
    }

    for p_id in sorted_plane_ids:
        # Get the title from our map to ensure sticking to the rules
        full_title = plane_titles.get(p_id, f"Plane {p_id}")
        
        lines.append(f"## Plane {p_id}: {full_title}")
        
        # Add basic plane metadata from JSON if available, or static
        plane_data = planes[p_id]
        # We can try to infer Core Force/Collapse Inversion from the data or just let the user edit them later since they were not structurally consistent in the JSON source due to varied parsing.
        # However, for now, we will rebuild the structure based on the vectors.
        
        lines.append("")
        
        # Sort States
        states = plane_data["States"]
        sorted_state_ids = sorted(states.keys(), key=lambda x: float(x))
        
        for s_id in sorted_state_ids:
            state = states[s_id]
            state_name = state["Name"]
            
            lines.append(f"### {s_id} {state_name}")
            
            # Table Header
            lines.append("| Code | Interrogative | Collapse Vector | Detailed Definition (The Mechanism of Ruin) | Historical Anchor |")
            lines.append("| :--- | :--- | :--- | :--- | :--- |")
            
            # Sort Vectors
            vectors = state["Vectors"]
            sorted_vector_ids = sorted(vectors.keys(), key=lambda x: [int(n) for n in x.split('.')])
            
            for v_id in sorted_vector_ids:
                vec = vectors[v_id]
                
                name = f"**{vec['Name']}**"
                interrogative_str = f"**{vec['Interrogative']}?**"
                code_str = f"**{v_id}**"
                anchor = f"*{vec['Anchor']}*"
                definition = vec['Definition']
                
                row = f"| {code_str} | {interrogative_str} | {name} | {definition} | {anchor} |"
                lines.append(row)
            
            lines.append("") # Newline after table
        
        lines.append("---")
        lines.append("")

    lines.append("**End of Master Matrix**")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    
    print(f"Generated Markdown at {output_path}")

if __name__ == "__main__":
    data = load_data()
    generate_markdown(data)
