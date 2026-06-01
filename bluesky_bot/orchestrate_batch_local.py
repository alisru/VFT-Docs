import os
import sys
import json

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generate_graph import draw_graph
from aletheia_bot import save_and_sync_story

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cand_path = os.path.join(os.path.dirname(script_dir), "scratch", "harvested_candidates.json")
    
    if os.path.exists(cand_path):
        print(f"Loading harvested candidates from {cand_path}...\n")
        with open(cand_path, "r", encoding="utf-8") as f:
            candidates = json.load(f)
    else:
        print(f"No candidates found at {cand_path}. Run a harvester script first.")
        sys.exit(0)
        
    print("=====================================================================")
    print(" ALIGNMENT & EVALUATION INSTRUCTION MANUAL (LOCAL AGENT MODE)        ")
    print("=====================================================================")
    print("This file acts as an offline template generator. Gen-AI SDKs have ")
    print("been stripped to completely avoid background token consumption.\n")
    
    # Process sequentially 
    for i, candidate in enumerate(candidates, 1):
        post_url = candidate["url"]
        post_text = candidate["text"]
        
        print(f"\n--- STORY {i}/{len(candidates)} ---")
        print(f"URL: {post_url}")
        print(f"TEXT:\n{post_text}\n")
        
        print("AGENT INSTRUCTIONS FOR THIS STORY:")
        print("1. Perform the 5-Phase Convergence Test (Actualism Framework).")
        print("2. Formulate stated/actual coordinates, Path Name, Verdict, and a 14-post thread.")
        print("3. Write the compiled configuration to `e:\\Vector Field Theory\\VFT Docs\\scratch\\factcheck_[subject_slug].json`.")
        print("4. Call `draw_graph` from `generate_graph.py` to create the trajectory graph locally.")
        print("5. Use `save_and_sync_story` from `aletheia_bot.py` to deploy to registries.")
        print("=====================================================================\n")

if __name__ == "__main__":
    main()
