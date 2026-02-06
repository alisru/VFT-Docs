import re
import os
import glob

SOURCE_DIR = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America"

def cleanup_duplicates():
    files = glob.glob(os.path.join(SOURCE_DIR, "American_Kanon_Plane_*.md"))
    
    for filepath in files:
        print(f"Cleaning {os.path.basename(filepath)}...")
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Clean Meta Quote Duplicates (if any, though script checks for header)
        # Actually header duplication was protected by "header_updated" flag in refine script but let's see.
        # Lines 1-13 in Plane 2 looked partially duped?
        # "1: # The American Kanon: \n 2: # The American Kanon:"
        
        # Strategy:
        # Split into blocks by Sense.
        # Inside each sense, finding duplicate narratives.
        # Total summary at the end.
        
        # Let's do a line-based deduplication for sequential duplicates?
        # No, the narratives are blocks.
        
        # Regex to find:
        # (> \*\*The Narrative of .*?)(?=\n> \*\*The Narrative|\n###|\Z)
        # If we find two identical consecutive blocks, remove one.
        
        # Better: Parse the file structure and rewrite it cleanly.
        
        # Preamble
        # Sense q1
        # ...
        # Sense q7
        # Summary
        
        sense_blocks = re.split(r'(### Sense q\d:)', content)
        
        cleaned_content = []
        
        # Preamble (sense_blocks[0])
        preamble = sense_blocks[0]
        # Clean Preamble duplicates
        # Remove duplicate # The American Kanon lines
        lines = preamble.split('\n')
        unique_lines = []
        last_line = None
        for line in lines:
            if line.strip() == "":
                unique_lines.append(line)
                continue
            if line.strip() != last_line:
                unique_lines.append(line)
                last_line = line.strip()
            # Special case for quote blocks being duped?
            # The preview showed:
            # > "Quote"
            # > -- Author
            # ...
            # > "Quote"
            # > -- Author
            # Simple dedup might work if exact match.
        
        # Actually, simpler approach for Preamble:
        # Keep only the FIRST instance of the Meta Quote if duped.
        # Keep only the LAST "# The American Kanon" header combo.
        
        # Let's blindly dedup CONSECUTIVE identical non-empty lines in preamble?
        # No, quotes have > lines.
        
        # Let's normalize Preamble:
        # Find the header. Find the Quote. 
        # Whatever. Let's fix the Narratives first.
        
        cleaned_content.append(preamble)
        
        for i in range(1, len(sense_blocks), 2):
            header = sense_blocks[i] # ### Sense qX:
            body = sense_blocks[i+1]
            
            # Remove duplicate narratives in body
            # Matches > **The Narrative... up to end or next headers
            narratives = re.findall(r'(> \*\*The Narrative.*?(?:\n(?:>.*|\s*))*)', body, re.DOTALL)
            
            # If multiple narratives found, keep only the unique ones (or just the last one?)
            # Usually they are identical.
            if len(narratives) > 1:
                # Deduplicate list
                unique_narratives = sorted(list(set(narratives)), key=narratives.index)
                
                # Replace the whole block of narratives with just the unique one
                # This is tricky because they might be interleaved? 
                # In my view_file output, they were sequential at the end.
                
                # Remove ALL narratives from body
                body_no_narrative = re.sub(r'> \*\*The Narrative.*?(?:\n(?:>.*|\s*))*', '', body, flags=re.DOTALL)
                
                # Append ONE narrative back
                # Check if unique_narratives[0] is the right one.
                final_narrative = unique_narratives[-1] # Take the last one just in case
                
                body = body_no_narrative.strip() + "\n\n" + final_narrative.strip() + "\n\n"
            
            cleaned_content.append(header)
            cleaned_content.append(body)
            
        # Join back
        new_full_content = "".join(cleaned_content)
        
        # Now fix the Total Summary at the end
        # Matches > **The American [Locus/Land/etc]...
        # and ### **Summary...
        
        # Find all occurrences
        summaries = re.findall(r'((?:> \*\*The American.*|### \*\*Summary.*)(?:\n(?:>.*|\s*))*)', new_full_content, re.MULTILINE)
        
        if len(summaries) > 1:
             # Remove all, append last
             new_full_content = re.sub(r'(?:> \*\*The American.*|### \*\*Summary.*)(?:\n(?:>.*|\s*))*', '', new_full_content)
             new_full_content = new_full_content.strip() + "\n\n" + summaries[-1].strip() + "\n"

        # Global cleanup of double headers in preamble
        new_full_content = re.sub(r'(# The American Kanon: \n)+', '# The American Kanon: \n', new_full_content)
        
        # Fix duplicated Preamble quotes
        # Regex for quote block
        quote_pattern = r'(> \*"[^"]+"*\n> — \*\*.*?\*\*.*?\n)'
        quotes = re.findall(quote_pattern, new_full_content, re.DOTALL)
        if len(quotes) > 1:
            # Remove all, insert one after header
            new_full_content = re.sub(quote_pattern, '', new_full_content, flags=re.DOTALL)
            # Find header end
            header_end = new_full_content.find("Values of American")
            if header_end != -1:
                # Find end of that line
                line_end = new_full_content.find('\n', header_end)
                new_full_content = new_full_content[:line_end+1] + "\n" + quotes[0] + "\n" + new_full_content[line_end+1:]

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_full_content)

if __name__ == "__main__":
    cleanup_duplicates()
