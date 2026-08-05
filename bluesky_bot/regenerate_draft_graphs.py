import glob
import json
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

from generate_graph import draw_graph

def main():
    stories = glob.glob(os.path.join(script_dir, "stories", "factcheck_*.json"))
    for p in stories:
        filename = os.path.basename(p)
        slug = filename[len("factcheck_"):-len(".json")]
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
            cfg = data[0] if isinstance(data, list) else data
            
            graph_path = os.path.join(script_dir, "graph_png", f"{slug}_graph.png")
            print(f"Regenerating graph for {slug}...")
            draw_graph(
                cfg.get("claim_u", 0.0), cfg.get("claim_psi", 0.0),
                cfg.get("real_u", 0.0), cfg.get("real_psi", 0.0),
                cfg.get("subject", "Story"),
                graph_path
            )
        except Exception as e:
            print(f"Error generating graph for {slug}: {e}")

if __name__ == "__main__":
    main()
