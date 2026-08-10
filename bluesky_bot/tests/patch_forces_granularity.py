import os

filepath = r"e:\Vector Field Theory\VFT Docs\bluesky_bot\google_ai_studio_one_shot.py"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Target 1: detailed thinking instruction in item[0]
target_1 = '    "thinking",                                // item[0]: detailed thinking/scratchpad calculations (Phase 1 to 5 calculations)\\n'
replacement_1 = '    "thinking",                                // item[0]: detailed thinking block. You MUST write down the full 6-Phase Convergence scan here, including scoring the 18 variables of the 6 attractors with high-resolution decimals, and detailing your coordinate equations (u, psi), hypocrisy delta, and trajectory calculations step-by-step before outputting the rest of the array.\\n'

# Target 2: Adding critical granularity rules to the instructions
target_2 = '    if use_son:\n        output_format += (\n            "INTEGRITY TIER MAPPING FOR ITEMS [23] AND [24]:\\n"'
replacement_2 = '    if use_son:\n        output_format += (\n            "FORCE SCORING GRANULARITY CRITICAL RULES:\\n"\n            "- You MUST score the [S, O, N] force magnitudes for the 6 attractors as granular decimals (e.g. 0.2, 0.5, 0.8, 1.2, 1.5, 1.8) based on specific evidence in the text. Do NOT default to binary 0.0 or 1.0 values, as this causes coordinate collapse and loses analytical resolution.\\n"\n            "- Ensure that the forces you output in items[25] and [26] are highly granular and match the math you write down in your thinking block (item[0]).\\n\\n"\n            "INTEGRITY TIER MAPPING FOR ITEMS [23] AND [24]:\\n"'

# Target 3: Granular coordinates in the example block
target_3 = """        "    1.0,\\n"
        "    0.0,\\n"
        "    -1.0,\\n"
        "    -1.0,\\n\""""
# Wait, let's look at lines 1018 to 1021 in python syntax:
#         "    1.0,\n"
#         "    0.0,\n"
#         "    -1.0,\n"
#         "    -1.0,\n"
# In python code:
#         "    1.0,\n"
#         "    0.0,\n"
#         "    -1.0,\n"
#         "    -1.0,\n"
# Let's target the exact string:
target_3 = '        "    1.0,\\n"\n        "    0.0,\\n"\n        "    -1.0,\\n"\n        "    -1.0,\\n"'
replacement_3 = '        "    1.0,\\n"\n        "    1.0,\\n"\n        "    -0.89,\\n"\n        "    -0.87,\\n"'

# Target 4: Forces example update in replacement_3 (which was added in the previous patch)
target_4 = """            '    {"GG": {"S": 1.0, "O": 0.0, "N": 0.0}, "GE": {"S": 0.0, "O": 1.0, "N": 0.0}, "LG": {"S": 0.0, "O": 0.0, "N": 0.5}, "LE": {"S": 0.0, "O": 0.0, "N": 0.5}, "GP": {"S": 1.0, "O": 0.0, "N": 0.0}, "BP": {"S": 1.0, "O": 1.0, "N": 0.0}},\\n'
            '    {"GG": {"S": 0.0, "O": 1.5, "N": 0.0}, "GE": {"S": 1.0, "O": 0.0, "N": 0.0}, "LG": {"S": 0.0, "O": 0.5, "N": 0.0}, "LE": {"S": 1.5, "O": 0.0, "N": 0.0}, "GP": {"S": 0.0, "O": 1.0, "N": 0.0}, "BP": {"S": 1.0, "O": 0.0, "N": 0.0}}\\n'"""

replacement_4 = """            '    {"GG": {"S": 1.2, "O": 0.0, "N": 0.0}, "GE": {"S": 0.0, "O": 1.2, "N": 0.0}, "LG": {"S": 1.0, "O": 0.0, "N": 0.0}, "LE": {"S": 0.0, "O": 0.8, "N": 0.0}, "GP": {"S": 1.2, "O": 0.0, "N": 0.0}, "BP": {"S": 0.0, "O": 1.2, "N": 0.0}},\\n'
            '    {"GG": {"S": 0.0, "O": 1.2, "N": 0.0}, "GE": {"S": 0.8, "O": 0.2, "N": 0.0}, "LG": {"S": 0.0, "O": 0.5, "N": 0.0}, "LE": {"S": 1.5, "O": 0.0, "N": 0.0}, "GP": {"S": 0.0, "O": 1.0, "N": 0.0}, "BP": {"S": 1.0, "O": 0.0, "N": 0.0}}\\n'"""

if target_1 not in content:
    print("Target 1 not found!")
if target_2 not in content:
    print("Target 2 not found!")
if target_3 not in content:
    print("Target 3 not found!")
if target_4 not in content:
    print("Target 4 not found!")

assert target_1 in content
assert target_2 in content
assert target_3 in content
assert target_4 in content

content = content.replace(target_1, replacement_1)
content = content.replace(target_2, replacement_2)
content = content.replace(target_3, replacement_3)
content = content.replace(target_4, replacement_4)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("google_ai_studio_one_shot.py forces granularity rules patched successfully!")
