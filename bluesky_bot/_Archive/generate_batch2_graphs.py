import os
import shutil
import sys

# Add bluesky_bot/ to path to import draw_graph
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "bluesky_bot")))
from generate_graph import draw_graph

stories = [
    {
        "slug": "tech_ceos_ai_psychosis",
        "title": "Tech CEOs AI Psychosis",
        "claim_u": 1.5,
        "claim_psi": 1.5,
        "real_u": -1.0,
        "real_psi": -1.5
    },
    {
        "slug": "putin_image_reinvention",
        "title": "Putin Image Reinvention",
        "claim_u": 1.0,
        "claim_psi": 1.0,
        "real_u": -1.8,
        "real_psi": -1.8
    },
    {
        "slug": "trump_freedom_250_cancel",
        "title": "Trump Freedom 250 Cancel",
        "claim_u": 1.0,
        "claim_psi": 1.0,
        "real_u": -1.5,
        "real_psi": -0.5
    },
    {
        "slug": "ksi_quits_sidemen",
        "title": "KSI Quits Sidemen",
        "claim_u": 1.0,
        "claim_psi": 1.0,
        "real_u": -0.5,
        "real_psi": 0.5
    },
    {
        "slug": "emily_blunt_refused_ai",
        "title": "Emily Blunt Refused AI",
        "claim_u": 1.0,
        "claim_psi": 1.0,
        "real_u": -0.5,
        "real_psi": -0.5
    }
]

scratch_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(scratch_dir)

generated_content_dir = os.path.join(root_dir, "_Generated_Content")
bluesky_bot_dir = os.path.join(root_dir, "bluesky_bot")

os.makedirs(generated_content_dir, exist_ok=True)
os.makedirs(bluesky_bot_dir, exist_ok=True)

for story in stories:
    slug = story["slug"]
    title = f"Assessment: {story['title']}"
    graph_name = f"{slug}_graph.png"
    
    # Target path in scratch
    scratch_path = os.path.join(scratch_dir, graph_name)
    
    print(f"Generating graph for {slug}...")
    draw_graph(
        story["claim_u"], 
        story["claim_psi"], 
        story["real_u"], 
        story["real_psi"], 
        title, 
        scratch_path
    )
    
    # Copy to _Generated_Content/
    gen_path = os.path.join(generated_content_dir, graph_name)
    shutil.copy(scratch_path, gen_path)
    print(f"Copied to {gen_path}")
    
    # Copy to bluesky_bot/
    bot_path = os.path.join(bluesky_bot_dir, graph_name)
    shutil.copy(scratch_path, bot_path)
    print(f"Copied to {bot_path}")

print("All graphs generated and copied successfully!")
