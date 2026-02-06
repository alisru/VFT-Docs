import re
import os
import glob

SOURCE_DIR = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America"

def reconstruct_planes():
    files = glob.glob(os.path.join(SOURCE_DIR, "American_Kanon_Plane_*.md"))
    
    for filepath in files:
        print(f"Reconstructing {os.path.basename(filepath)}...")
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Extract Meta Info (Preamble)
        # Look for the Quotes at the top
        # > "Quote"
        # > -- Author
        meta_matches = re.findall(r'(> \*"[^"]+"*\n> — \*\*[^(\n]+.*)', content)
        meta_quote = meta_matches[0] if meta_matches else ""
        
        # Extract Title
        # # The American Kanon: ...
        # # Plane X; Values of ...
        title_match = re.search(r'(# The American Kanon:\s*# Plane .*?; Values of American \w+)', content, re.DOTALL)
        title_block = title_match.group(1) if title_match else "# Title Not Found"
        
        # 2. Extract Senses
        # We need to extract:
        # - Header (### Sense qX: ...)
        # - Introduction (*Scanning...*)
        # - Items
        # - Narrative (Last unique one)
        
        # Split by ### Sense q
        # But the file is messy, so we might want to iterate.
        
        senses = {}
        for q in range(1, 8):
            q_key = f"q{q}"
            # Find the header
            header_pattern = f"### Sense {q_key}:.*"
            headers = re.findall(header_pattern, content)
            unique_header = headers[0] if headers else f"### Sense {q_key}: Unknown"
            
            # Find the Italics Intro underneath
            # It's usually the next non-empty line
            
            # Find Items
            # Pattern: Label. **(Label)[Value]**... Meaning Paragraph
            # Regex to find full item blocks
            # We assume items start with "Label." or "Number."
            # My previous scripts changed it to "Label.". 
            # Let's search for "Label. **("
            
            # To avoid capturing duplicates, we should scan the whole file for items belonging to this sense (based on Label)
            # Labels for q1 are Plane.Who.Who, Plane.Who.Where ...
            # Actually easier: Just grep all unique items.
            
            sense_items = []
            # Find all items that look like "Word.Word.Word. **"
            # And extract up to the start of the next item or header.
            
            item_pattern = r'([\w.]+)\.\s*\*\*\(([^)]+)\)\[([^\]]+)\]\*\*;\s*"(.*?)"\s*-\s*(.*?)(\n|$)([\s\S]*?)(?=\n[\w.]+\.\s*\*\*|\n###|\n> \*\*The Narrative|\Z)'
            
            all_items = list(re.finditer(item_pattern, content))
            
            # Filter and dedupe items for this sense
            # We know the specific labels for this sense?
            # Or just dedupe by Label string.
            seen_labels = set()
            for m in all_items:
                label_dot = m.group(1) # Label.
                label_paren = m.group(2) # (Label)
                
                # Check if this item belongs to this sense?
                # The sense is determined by the middle term usually, or just grouping.
                # Plane 1 (Identity): Who.Who.Who (q1), Who.What.Who (q2) ??
                # Wait, Plane 1 q1 is Who.Who.*
                # Plane 1 q2 is Who.What.*
                
                # Let's just grab them from the section if we split by header?
                pass

        # Better strategy: Split by Header, then clean the block.
        chunks = re.split(r'(### Sense q\d:.*)', content)
        
        # chunks[0] is preamble.
        # chunks[1] is header q1, chunks[2] is body q1
        
        new_content_list = []
        new_content_list.append(title_block)
        new_content_list.append("")
        if meta_quote:
            new_content_list.append(meta_quote)
        new_content_list.append("")
        new_content_list.append("")

        if len(chunks) < 2:
            print(f"Error parsing {filepath}")
            continue

        for i in range(1, len(chunks), 2):
            header = chunks[i].strip()
            body = chunks[i+1]
            
            new_content_list.append(header)
            
            # Intro Italics
            # Find first line starting with *
            intro_match = re.search(r'^\s*(\*.*?\*)\s*$', body, re.MULTILINE)
            if intro_match:
                new_content_list.append(intro_match.group(1))
                new_content_list.append("")
            
            # Items
            # Find unique items
            item_matches = list(re.finditer(item_pattern, body))
            seen_items = set()
            unique_items_list = []
            for m in item_matches:
                label = m.group(2)
                if label not in seen_items:
                    seen_items.add(label)
                    # Reconstruct item string
                    full_match = m.group(0)
                    unique_items_list.append(full_match.strip())
            
            new_content_list.append("\n\n".join(unique_items_list))
            new_content_list.append("")
            
            # Narrative
            # Find the Narrative block
            narrative_match = re.search(r'(> \*\*The Narrative.*?)(?=\n###|\Z|\n> \*\*The Narrative)', body, re.DOTALL)
            # If duplicates exist, regex finds the first one.
            # But wait, the file might have malformed narratives "of Environment..."
            # Let's look for known Narrative headers in my previous script?
            # Or just look for "> **The Narrative" and grab until double newline?
            
            # Robust: Find ALL matches of "> **The Narrative" line
            narstart_iter = re.finditer(r'^> \*\*The Narrative.*$', body, re.MULTILINE)
            # Take the last one? Or first? usually last is best if I appended.
            starts = list(narstart_iter)
            if starts:
                last_start = starts[-1]
                # Extract from there until end of block (blank line? or next header?)
                start_idx = last_start.start()
                # Find next blank line after some content?
                # Actually, narrative is usually a blockquote.
                # Let's grab lines starting with > from that point
                
                narrative_lines = []
                remaining_body = body[start_idx:]
                for line in remaining_body.split('\n'):
                    if line.startswith('>') or line.strip() == "":
                        if line.strip() != "": narrative_lines.append(line)
                    else:
                        break # End of block
                new_content_list.append("\n".join(narrative_lines))
                new_content_list.append("")
        
        # Total Narrative (Total Summary)
        # Scan for > **The American [Plane]...
        total_matches = re.findall(r'(> \*\*The American.*?)(?=\n> \*\*The American|\Z)', content, re.DOTALL)
        if total_matches:
            # Clean up newlines in match
            # Pick the last one
            total_block = total_matches[-1]
            # Verify it's a blockquote
            lines = total_block.split('\n')
            clean_total = []
            for line in lines:
                if line.startswith('>'):
                    clean_total.append(line)
                elif line.strip() == "":
                    continue
                else: 
                    break
            new_content_list.append("\n".join(clean_total))
            new_content_list.append("")
            
        # Write back
        final_text = "\n".join(new_content_list)
        # Remove excessive newlines
        final_text = re.sub(r'\n{3,}', '\n\n', final_text)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_text)

if __name__ == "__main__":
    reconstruct_planes()
