import re
import os

def get_order_index(label):
    order = {
        'Who': 1,
        'What': 2,
        'Where': 3,
        'Why': 4,
        'How': 5,
        'Cause': 6,
        'Effect': 7
    }
    # Handle "Land" or "Def" if they still exist (though they shouldn't)
    mapping = {
        'Land': 'Where',
        'Def': 'What',
        'Drive': 'Why',
        'Method': 'How',
        'Origin': 'Cause',
        'Impact': 'Effect'
    }
    
    clean_label = label.replace("(", "").replace(")", "").replace(".", " ").strip()
    parts = clean_label.split()
    
    # We are looking for the 'Sense' part for Sense sorting, 
    # and 'Node' part for Node sorting.
    # Format: Plane.Sense.Node
    # Or just Plane.Sense for headers.
    
    if len(parts) == 2: # Section Header e.g. Who.Where
        key = parts[1]
    elif len(parts) == 3: # Node e.g. Who.Where.What
        key = parts[2]
    else:
        return 99
        
    if key in mapping:
        key = mapping[key]
        
    return order.get(key, 99)

def reorder_file(filepath, plane_number):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split preamble and valid content chunks (Senses)
    # Regex to find "## X.X Title (Label)"
    section_pattern = re.compile(r'## \d+\.\d+ .*?\((.*?)\)')
    
    # Isolate preamble
    first_match = section_pattern.search(content)
    if not first_match:
        print(f"No sections found in {filepath}")
        return

    preamble = content[:first_match.start()]
    rest = content[first_match.start():]
    
    # Split into sections
    # usage of split with capture group keeps delimiters, 
    # making it hard to reconstruct. 
    # Better to find all start indices.
    matches = list(section_pattern.finditer(content))
    start_indices = [m.start() for m in matches]
    end_indices = start_indices[1:] + [len(content)]
    
    sections = []
    
    for i, start in enumerate(start_indices):
        end = end_indices[i]
        section_text = content[start:end]
        match = matches[i]
        label = match.group(1)
        sort_index = get_order_index(label)
        
        # Parse Nodes within section
        # Finds **(Label) Title**
        node_pattern = re.compile(r'\*\*(\(.*\)) .*?\*\*;')
        
        # Split section into Header+Intro, Nodes, Narrative (if any)
        # We need to find the start of the first node
        first_node = node_pattern.search(section_text)
        
        if first_node:
            header_intro = section_text[:first_node.start()]
            nodes_and_narrative = section_text[first_node.start():]
            
            # Find Narrative start
            narrative_match = re.search(r'### Narrative:', nodes_and_narrative)
            
            if narrative_match:
                nodes_text = nodes_and_narrative[:narrative_match.start()]
                narrative_text = nodes_and_narrative[narrative_match.start():]
            else:
                nodes_text = nodes_and_narrative
                narrative_text = ""
                # Check for "---" at end
                footer_match = re.search(r'\n---\n', nodes_text)
                if footer_match:
                     narrative_text = nodes_text[footer_match.start():]
                     nodes_text = nodes_text[:footer_match.start()]
            
            # Parse individual nodes
            # We can use split but need to keep delimiters
            node_matches = list(node_pattern.finditer(nodes_text))
            if node_matches:
                node_starts = [nm.start() for nm in node_matches]
                node_ends = node_starts[1:] + [len(nodes_text)]
                
                parsed_nodes = []
                for j, n_start in enumerate(node_starts):
                    n_end = node_ends[j]
                    n_text = nodes_text[n_start:n_end]
                    n_label_match = node_pattern.match(n_text)
                    if n_label_match:
                        n_label = n_label_match.group(1)
                        n_sort = get_order_index(n_label)
                        parsed_nodes.append((n_sort, n_text))
                
                # Sort nodes
                parsed_nodes.sort(key=lambda x: x[0])
                sorted_nodes_text = "".join([n[1] for n in parsed_nodes])
            else:
                sorted_nodes_text = nodes_text
            
            final_section_text = header_intro + sorted_nodes_text + narrative_text
            
        else:
            final_section_text = section_text # No nodes found?
            
        sections.append((sort_index, final_section_text))

    # Sort sections
    sections.sort(key=lambda x: x[0])
    
    # Renumber sections
    new_content = preamble
    for i, (idx, text) in enumerate(sections):
        # find the Header line and replace 1.X with 1.{i+1}
        # e.g. ## 1.4 -> ## 1.{i+1}
        # or ## 2.X -> ## 2.{i+1}
        
        # pattern matching start of text
        text = re.sub(r'## \d+\.\d+', f'## {plane_number}.{i+1}', text, count=1)
        new_content += text

    # Remove extra newlines or separators at the very end to be clean
    new_content = new_content.strip() + "\n"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Reordered {filepath}")

if __name__ == "__main__":
    reorder_file(r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Australian_Kanon_Plane_1_Identity.md", 1)
    reorder_file(r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Australian_Kanon_Plane_2_Definition.md", 2)
    reorder_file(r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Australian_Kanon_Plane_3_Land.md", 3)
    reorder_file(r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Australian_Kanon_Plane_4_Drive.md", 4)
    reorder_file(r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Australian_Kanon_Plane_5_Method.md", 5)
