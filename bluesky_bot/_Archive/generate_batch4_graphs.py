import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bluesky_bot.generate_graph import draw_graph

graphs = [
    {
        "claim_u": 1.0, "claim_psi": 1.0,
        "real_u": -1.0, "real_psi": -1.0,
        "title": "US Cuba Embargo",
        "filename": "cuba_collapses_graph.png"
    },
    {
        "claim_u": 1.0, "claim_psi": 1.0,
        "real_u": -1.0, "real_psi": -1.0,
        "title": "Elimination of Black Voting Districts",
        "filename": "alabama_voting_districts_graph.png"
    },
    {
        "claim_u": 1.0, "claim_psi": 1.0,
        "real_u": -1.0, "real_psi": 1.0,
        "title": "Political Career Ascension",
        "filename": "xavier_becerra_graph.png"
    },
    {
        "claim_u": -1.0, "claim_psi": 1.0,
        "real_u": -1.0, "real_psi": -1.0,
        "title": "Public Violence",
        "filename": "sandy_shooting_graph.png"
    },
    {
        "claim_u": 1.0, "claim_psi": 1.0,
        "real_u": -1.0, "real_psi": -1.0,
        "title": "For-Profit ICE Facility",
        "filename": "ice_facility_utah_graph.png"
    },
    {
        "claim_u": 1.0, "claim_psi": -1.0,
        "real_u": 1.0, "real_psi": 1.0,
        "title": "Open Social Infrastructure",
        "filename": "graze_social_graph.png"
    }
]

scratch_dir = os.path.dirname(__file__)

for g in graphs:
    draw_graph(g['claim_u'], g['claim_psi'], g['real_u'], g['real_psi'], g['title'], os.path.join(scratch_dir, g['filename']))
    print(f"Generated {g['filename']}")

