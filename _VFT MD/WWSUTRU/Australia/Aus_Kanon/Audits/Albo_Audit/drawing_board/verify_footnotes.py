import re
import sys

def verify_footnotes():
    with open('Plane_2_Definition_Albanese.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # Split body and sources
    parts = content.split('## **Sources**')
    if len(parts) < 2:
        print("Error: Could not find '## **Sources**' section.")
        return
    
    body = parts[0]
    sources_section = parts[1]

    # Find all footnotes used in body [^key]
    used_markers = set(re.findall(r'\[\^([a-zA-Z0-9_-]+)\]', body))
    
    # Find all footnotes defined in sources section [^key]: content
    defined_markers = {}
    for line in sources_section.splitlines():
        line = line.strip()
        if not line:
            continue
        match = re.match(r'^\[\^([a-zA-Z0-9_-]+)\]:\s*(.*)$', line)
        if match:
            marker = match.group(1)
            source_content = match.group(2)
            defined_markers[marker] = source_content

    print(f"Total markers used in body: {len(used_markers)}")
    print(f"Total markers defined in sources: {len(defined_markers)}")
    print("\n--- Defined but UNUSED in body ---")
    unused = []
    for m in sorted(defined_markers.keys()):
        if m not in used_markers:
            print(f"[^{m}]: {defined_markers[m]}")
            unused.append(m)
    
    print("\n--- Used in body but UNDEFINED in sources ---")
    undefined = []
    for m in sorted(used_markers):
        if m not in defined_markers:
            print(f"[^{m}]")
            undefined.append(m)

if __name__ == '__main__':
    verify_footnotes()
