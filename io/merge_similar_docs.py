import os
import sys
import difflib
import re

def parse_blocks(text):
    # Split text into manageable blocks (paragraphs or headers + paragraphs)
    blocks = re.split(r'\n\s*\n', text)
    return [b.strip() for b in blocks if b.strip()]

def similarity(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

def is_duplicate(block, winner_blocks, threshold=0.8):
    if len(block) < 20: 
        return True # Ignore very short blocks like headers alone or single words
    
    for w_block in winner_blocks:
        if similarity(block, w_block) > threshold:
            return True
    return False

def merge_files(winner_path, loser_path):
    print(f"Merging {os.path.basename(loser_path)} into {os.path.basename(winner_path)}")
    
    with open(winner_path, 'r', encoding='utf-8') as f:
        winner_text = f.read()
    
    with open(loser_path, 'r', encoding='utf-8') as f:
        loser_text = f.read()
        
    winner_blocks = parse_blocks(winner_text)
    loser_blocks = parse_blocks(loser_text)
    
    unique_blocks = []
    
    for l_block in loser_blocks:
        if not is_duplicate(l_block, winner_blocks):
            unique_blocks.append(l_block)
            
    if unique_blocks:
        print(f"Found {len(unique_blocks)} unique blocks in {os.path.basename(loser_path)}.")
        append_text = f"\n\n---\n\n## ARCHIVED UNIQUE CONTENT FROM: {os.path.basename(loser_path)}\n\n"
        append_text += "\n\n".join(unique_blocks)
        
        with open(winner_path, 'a', encoding='utf-8') as f:
            f.write(append_text)
        print(f"Appended unique content to {os.path.basename(winner_path)}.")
    else:
        print(f"No unique content found in {os.path.basename(loser_path)}. It is fully covered.")
        
    # Rename loser to _DELETEME
    loser_dir = os.path.dirname(loser_path)
    loser_name = os.path.basename(loser_path)
    new_loser_name = loser_name.replace('.md', '_DELETEME.md')
    new_loser_path = os.path.join(loser_dir, new_loser_name)
    
    os.rename(loser_path, new_loser_path)
    print(f"Renamed {loser_name} to {new_loser_name}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python merge_similar_docs.py <winner_path> <loser_path>")
        sys.exit(1)
        
    winner = sys.argv[1]
    loser = sys.argv[2]
    
    if not os.path.exists(winner):
        print(f"Winner not found: {winner}")
        sys.exit(1)
        
    if not os.path.exists(loser):
        print(f"Loser not found: {loser}")
        sys.exit(1)
        
    merge_files(winner, loser)
