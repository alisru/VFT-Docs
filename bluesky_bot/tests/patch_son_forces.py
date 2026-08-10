import os

filepath = r"e:\Vector Field Theory\VFT Docs\bluesky_bot\google_ai_studio_one_shot.py"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Target 1: expected_len
target_1 = "expected_len = 25 if use_son else 17"
replacement_1 = "expected_len = 27 if use_son else 17"

# Target 2 & 3: We can use a single search and replace targeting the use_son block
target_2 = '    if use_son:\n        output_format += (\n            ",\\n"\n            "    claim_rnet (float),                        // item[17]: stated R_net integrity score\\n"\n            "    real_rnet (float),                         // item[18]: actual R_net integrity score\\n"\n            "    claim_z (int),                             // item[19]: stated uncertainty score (blank count, sum of blank counts across planes)\\n"\n            "    real_z (int),                              // item[20]: actual uncertainty score\\n"\n            "    claim_z_profile (7-number array of ints),  // item[21]: stated blank profile [B_Q1, B_Q2, B_Q3, B_Q4, B_Q5, B_Q6, B_Q7]\\n"\n            "    real_z_profile (7-number array of ints),   // item[22]: actual blank profile\\n"\n            \'    "claim_integrity",                         // item[23]: stated integrity label mapped from claim_rnet\\n\'\n            \'    "real_integrity"                           // item[24]: actual integrity label mapped from real_rnet\\n\'\n        )'

replacement_2 = '    if use_son:\n        output_format += (\n            ",\\n"\n            "    claim_rnet (float),                        // item[17]: stated R_net integrity score\\n"\n            "    real_rnet (float),                         // item[18]: actual R_net integrity score\\n"\n            "    claim_z (int),                             // item[19]: stated uncertainty score (blank count, sum of blank counts across planes)\\n"\n            "    real_z (int),                              // item[20]: actual uncertainty score\\n"\n            "    claim_z_profile (7-number array of ints),  // item[21]: stated blank profile [B_Q1, B_Q2, B_Q3, B_Q4, B_Q5, B_Q6, B_Q7]\\n"\n            "    real_z_profile (7-number array of ints),   // item[22]: actual blank profile\\n"\n            \'    "claim_integrity",                         // item[23]: stated integrity label mapped from claim_rnet\\n\'\n            \'    "real_integrity",                          // item[24]: actual integrity label mapped from real_rnet\\n\'\n            \'    stated_forces (object/dict),               // item[25]: {"GG": {"S": s, "O": o, "N": n}, ...} for stated claim\\n\'\n            \'    actual_forces (object/dict)                // item[26]: {"GG": {"S": s, "O": o, "N": n}, ...} for actual reality\\n\'\n        )'

target_3 = '    if use_son:\n        output_format += (\n            ",\\n"\n            "    1.0,\\n"\n            "    12.5,\\n"\n            "    0,\\n"\n            "    4,\\n"\n            "    [0, 0, 0, 0, 0, 0, 0],\\n"\n            "    [1, 0, 0, 2, 1, 0, 0],\\n"\n            \'    "Absolute Truth",\\n\'\n            \'    "Severe Deception"\'\n        )'

replacement_3 = '    if use_son:\n        output_format += (\n            ",\\n"\n            "    1.0,\\n"\n            "    12.5,\\n"\n            "    0,\\n"\n            "    4,\\n"\n            "    [0, 0, 0, 0, 0, 0, 0],\\n"\n            "    [1, 0, 0, 2, 1, 0, 0],\\n"\n            \'    "Absolute Truth",\\n\'\n            \'    "Severe Deception",\\n\'\n            \'    {"GG": {"S": 1.0, "O": 0.0, "N": 0.0}, "GE": {"S": 0.0, "O": 1.0, "N": 0.0}, "LG": {"S": 0.0, "O": 0.0, "N": 0.5}, "LE": {"S": 0.0, "O": 0.0, "N": 0.5}, "GP": {"S": 1.0, "O": 0.0, "N": 0.0}, "BP": {"S": 1.0, "O": 1.0, "N": 0.0}},\\n\'\n            \'    {"GG": {"S": 0.0, "O": 1.5, "N": 0.0}, "GE": {"S": 1.0, "O": 0.0, "N": 0.0}, "LG": {"S": 0.0, "O": 0.5, "N": 0.0}, "LE": {"S": 1.5, "O": 0.0, "N": 0.0}, "GP": {"S": 0.0, "O": 1.0, "N": 0.0}, "BP": {"S": 1.0, "O": 0.0, "N": 0.0}}\\n\'\n        )'

target_4 = """            if len(item) >= 24 and item[23] is not None:
                story["claim_integrity"] = str(item[23]).strip()
            if len(item) >= 25 and item[24] is not None:
                story["real_integrity"] = str(item[24]).strip()
            evaluations.append(story)"""

replacement_4 = """            if len(item) >= 24 and item[23] is not None:
                story["claim_integrity"] = str(item[23]).strip()
            if len(item) >= 25 and item[24] is not None:
                story["real_integrity"] = str(item[24]).strip()
            if len(item) >= 26 and isinstance(item[25], dict):
                story["stated_forces"] = item[25]
            if len(item) >= 27 and isinstance(item[26], dict):
                story["actual_forces"] = item[26]
            evaluations.append(story)"""

# Debug print which target was not found:
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

print("google_ai_studio_one_shot.py patched successfully for SON forces output!")
