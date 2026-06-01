import os
import shutil
import sys

# Ensure bluesky_bot is in sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(os.path.join(parent_dir, 'bluesky_bot'))

from generate_graph import draw_graph

stories_data = [
    {
        "slug": "nicola_sturgeon",
        "title": "Assessment: Nicola Sturgeon",
        "claim_u": 1.0, "claim_psi": 1.0,
        "real_u": -1.0, "real_psi": -1.0
    },
    {
        "slug": "ferrari_ev_backlash",
        "title": "Assessment: Ferrari EV Backlash",
        "claim_u": 1.0, "claim_psi": 1.0,
        "real_u": -0.5, "real_psi": -0.5
    },
    {
        "slug": "sturgeon_power_loss",
        "title": "Assessment: Sturgeon Loss of Power",
        "claim_u": 1.0, "claim_psi": 1.0,
        "real_u": -1.0, "real_psi": -1.0
    },
    {
        "slug": "camp_east_montana_abuse",
        "title": "Assessment: Camp East Montana",
        "claim_u": 1.0, "claim_psi": 1.0,
        "real_u": -1.5, "real_psi": -1.5
    },
    {
        "slug": "champions_league_riots",
        "title": "Assessment: Champions League Riots",
        "claim_u": 1.0, "claim_psi": 1.0,
        "real_u": -1.0, "real_psi": -2.0
    }
]

for s in stories_data:
    filename = f"{s['slug']}_graph.png"
    scratch_path = os.path.join(parent_dir, "scratch", filename)
    gen_content_path = os.path.join(parent_dir, "_Generated_Content", filename)
    bot_path = os.path.join(parent_dir, "bluesky_bot", filename)
    
    print(f"Generating graph for {s['slug']}...")
    draw_graph(s['claim_u'], s['claim_psi'], s['real_u'], s['real_psi'], s['title'], scratch_path)
    
    # Copy to _Generated_Content/
    print(f"Copying to _Generated_Content/...")
    shutil.copy(scratch_path, gen_content_path)
    
    # Copy to bluesky_bot/
    print(f"Copying to bluesky_bot/...")
    shutil.copy(scratch_path, bot_path)
    
print("All graphs successfully generated and copied!")
