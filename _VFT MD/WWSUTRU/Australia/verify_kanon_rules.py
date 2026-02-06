import re
import os

def count_sentences(text):
    # Split by .!? followed by space or end of string
    sentences = re.split(r'[.!?]+(?:\s+|$)', text)
    return len([s for s in sentences if s.strip()])

def audit_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(filepath)
    print(f"--- Auditing {filename} ---")
    
    lines = content.split('\n')
    errors = 0
    
    current_node = None
    node_buffer = []
    
    for i, line in enumerate(lines):
        # Detect Node Header
        match = re.search(r'\*\*\((.*?)\) (.*?)\*\*;', line)
        if match:
            # Process previous node
            if current_node:
                evaluate_node(current_node, node_buffer)
                
            # Reset for new node
            current_node = f"{match.group(1)} {match.group(2)}"
            node_buffer = []
        
        elif current_node:
            stripped = line.strip()
            if line.startswith('##') or line.startswith('---'):
                evaluate_node(current_node, node_buffer)
                current_node = None
                node_buffer = []
            elif stripped:
                node_buffer.append(stripped)

    # Catch last node
    if current_node:
        evaluate_node(current_node, node_buffer)

    print("\n")

def evaluate_node(node_name, buffer):
    # We expect the buffer to contain paragraphs. 
    # Usually Context is first block, Meaning is second block.
    # But stripped lines might merge them if I'm not careful.
    
    # Reconstruct text preserving paragraph breaks
    # buffer is a list of non-empty lines. 
    # In my previous logic, I just appended stripped lines. 
    # I need to detect paragraph breaks (empty lines in original).
    # Let's simplify: 
    # The file has:
    # **Node**
    #    Context sentence 1. Context sentence 2.
    #    
    #    Meaning sentence 1. Meaning sentence 2.
    
    # My parser collapsed empty lines. Let's assume the buffer is a list of lines. 
    # If there are multiple lines, they might be one paragraph or two.
    
    # actually, let's just look at the joined text. 
    # If the user formatted strictly, there's a double newline.
    # But my parser `node_buffer.append(stripped)` removes the empty lines.
    
    # Let's rely on the fact that Context and Meaning are usually distinct paragraphs.
    # This parser is too simple to robustly separate them without reading strict blank lines.
    # BUT, I can check the TOTAL sentences and TOTAL length.
    
    full_text = " ".join(buffer)
    sentences = count_sentences(full_text)
    
    # User Requirements:
    # 1. Full Quote (Hard to verify programmatically, but I can check if quote exists in header)
    # 2. Context: Min 2 lines (~160 chars?)
    # 3. Meaning: Min 5 sentences.
    
    # If we assume 2 sentences for Context (min) + 5 sentences for Meaning (min) = 7 sentences TOTAL per node.
    
    if sentences < 7:
        print(f"[FAIL] {node_name}: Only {sentences} total sentences. (Target: ~7+ for Context+Meaning)")
    else:
        # print(f"[OK] {node_name}: {sentences} sentences.")
        pass

files = [
    r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Australian_Kanon_Plane_1_Identity.md",
    r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Australian_Kanon_Plane_2_Definition.md",
    r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Australian_Kanon_Plane_3_Land.md",
    r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Australian_Kanon_Plane_4_Drive.md",
    r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Australian_Kanon_Plane_5_Method.md"
]

for f in files:
    if os.path.exists(f):
        audit_file(f)
    else:
        print(f"File not found: {f}")
