import os
import sys

# Add bluesky_bot directory to the path so we can import generate_graph
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
bot_dir = os.path.join(parent_dir, "bluesky_bot")
sys.path.append(bot_dir)

from generate_graph import draw_graph

# 1. Generate Heatwave Graph
claim_u_1 = 0.54
claim_psi_1 = 0.93
real_u_1 = 1.0
real_psi_1 = 1.0
title_1 = "Gosport Heatwave Provisional Record"
output_path_1 = os.path.join(bot_dir, "graph_png", "uk-heatwave-temperature-record_graph.png")
draw_graph(
    claim_u_1, claim_psi_1, real_u_1, real_psi_1, title_1, output_path_1,
    macro_event="UK June Heatwave 2026",
    macro_claim_u=claim_u_1, macro_claim_psi=claim_psi_1,
    macro_real_u=real_u_1, macro_real_psi=real_psi_1
)
print("Generated Heatwave Graph!")

# 2. Generate Supreme Court Border Asylum Graph
claim_u_2 = 0.69
claim_psi_2 = 0.91
real_u_2 = -0.63
real_psi_2 = -0.86
title_2 = "Supreme Court Border Asylum Ruling"
output_path_2 = os.path.join(bot_dir, "graph_png", "supreme-court-border-asylum-ruling_graph.png")
draw_graph(
    claim_u_2, claim_psi_2, real_u_2, real_psi_2, title_2, output_path_2,
    macro_event="US Immigration Policy 2026",
    macro_claim_u=claim_u_2, macro_claim_psi=claim_psi_2,
    macro_real_u=real_u_2, macro_real_psi=real_psi_2
)
print("Generated Supreme Court Graph!")
