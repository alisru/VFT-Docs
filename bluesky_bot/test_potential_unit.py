import os
import sys
sys.path.insert(0, "bluesky_bot")
from google_ai_studio_one_shot import transpose_flat_to_json

# Test dict parse with potential mode keys
sample_dict = [{
    "thinking": "Phase 1 to 5 potential audit...",
    "id": "test_potential_modal",
    "subject": "Test Story",
    "link": "https://example.com/story",
    "claim_u": 0.5,
    "claim_psi": 0.5,
    "real_u": -0.8,
    "real_psi": -0.9,
    "mode": "root",
    "posts": ["Post 1", "Post 2", "Post 3", "Verdict: FAIL", "Post 5", "Post 6", "Post 7", "Post 8", "Post 9", "Post 10", "Post 11", "Post 12", "Post 13"],
    "actors": ["Actor A"],
    "modal_claim": "will be",
    "modal_real": "is not",
    "modal_vector": "Top-Right to Bottom-Left Inversion",
    "geodesic": "Red Top (The Imperial Trap)",
    "central_is_barrier_crossed": True
}]

import json
json_str = json.dumps(sample_dict)
parsed = transpose_flat_to_json(json_str, use_potential=True)
assert len(parsed) == 1, "Expected 1 parsed story"
p = parsed[0]
print("Parsed modal_claim:", p.get("modal_claim"))
print("Parsed modal_real:", p.get("modal_real"))
print("Parsed modal_vector:", p.get("modal_vector"))
print("Parsed geodesic:", p.get("geodesic"))
print("Parsed central_is_barrier_crossed:", p.get("central_is_barrier_crossed"))
print("Parsed potential_audit:", p.get("potential_audit"))
assert p.get("modal_claim") == "will be"
assert p.get("geodesic") == "Red Top (The Imperial Trap)"
assert p.get("central_is_barrier_crossed") is True
assert p.get("potential_audit") is True

# Test list parse with potential mode keys (32 items)
sample_list = [[
    "thinking", "test_id", "Test Subj", "https://link.com", "",
    0.5, 0.0, -0.8, -0.9, "root",
    ["p1","p2","p3","Verdict: FAIL","p5","p6","p7","p8","p9","p10","p11","p12","p13"],
    ["Actor"], "Macro", None, None, None, None,
    1.0, 12.5, 0, 4, [0]*7, [1,0,0,2,1,0,0], "Absolute Truth", "Severe Deception",
    {"GG":{"S":1,"O":0,"N":0}}, {"GG":{"S":0,"O":1,"N":0}},
    "can be", "Won't be", "Transition Vector", "Pretext Tether", True
]]
list_json_str = json.dumps(sample_list)
parsed_list = transpose_flat_to_json(list_json_str, use_potential=True)
assert len(parsed_list) == 1
pl = parsed_list[0]
print("List parsed modal_claim:", pl.get("modal_claim"))
print("List parsed geodesic:", pl.get("geodesic"))
print("List parsed potential_audit:", pl.get("potential_audit"))
assert pl.get("modal_claim") == "can be"
assert pl.get("geodesic") == "Pretext Tether"
assert pl.get("central_is_barrier_crossed") is True
assert pl.get("potential_audit") is True
print("ALL TESTS PASSED PERFECTLY!")
