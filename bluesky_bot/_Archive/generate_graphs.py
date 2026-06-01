import sys
import os
import shutil

# Add the workspace root to python path to allow importing bluesky_bot modules
workspace_root = r"e:\Vector Field Theory\VFT Docs"
sys.path.append(workspace_root)

from bluesky_bot.generate_graph import draw_graph

stories = [
    {
        "slug": "train_wifi_improvement",
        "subject": "Train Wi-Fi Improvement",
        "claim_u": 1.0,
        "claim_psi": 0.0,
        "real_u": -0.5,
        "real_psi": -0.5
    },
    {
        "slug": "news_feed_remixing",
        "subject": "News Feed Remixing",
        "claim_u": 1.0,
        "claim_psi": -1.0,
        "real_u": 1.0,
        "real_psi": 1.0
    },
    {
        "slug": "disinformation_drama",
        "subject": "Disinformation Drama",
        "claim_u": 1.0,
        "claim_psi": 1.0,
        "real_u": -0.5,
        "real_psi": 0.5
    },
    {
        "slug": "obama_center_festival",
        "subject": "Obama Center Festival",
        "claim_u": 1.0,
        "claim_psi": 1.0,
        "real_u": -0.5,
        "real_psi": -0.5
    },
    {
        "slug": "ferrari_ev_backlash",
        "subject": "Ferrari EV Backlash",
        "claim_u": -0.5,
        "claim_psi": 0.5,
        "real_u": 1.0,
        "real_psi": -1.0
    }
]

for s in stories:
    title = f"Assessment: {s['subject']}"
    filename = f"{s['slug']}_graph.png"
    
    # Paths to save
    scratch_path = os.path.join(workspace_root, "scratch", filename)
    gen_content_path = os.path.join(workspace_root, "_Generated_Content", filename)
    bot_path = os.path.join(workspace_root, "bluesky_bot", filename)
    
    print(f"Generating graph for {s['subject']}...")
    
    # 1. Draw into scratch first
    draw_graph(s['claim_u'], s['claim_psi'], s['real_u'], s['real_psi'], title, scratch_path)
    
    # 2. Copy to other directories
    shutil.copy(scratch_path, gen_content_path)
    shutil.copy(scratch_path, bot_path)
    
    print(f"Saved to:")
    print(f"  - {scratch_path}")
    print(f"  - {gen_content_path}")
    print(f"  - {bot_path}")

print("All graphs generated successfully!")
