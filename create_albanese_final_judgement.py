import os
import re

out_dir = "_VFT MD/Actualism/Hegemony/Kanon_Audits/Albanese_Audit_Detailed"
planes = range(1, 8)

total_vectors = 0
hits = 0
fails = 0
misses = 0
v_total = 0.0
p_total = 0.0

for p_num in planes:
    filepath = os.path.join(out_dir, f"Plane_{p_num}_Albanese_Audit.md")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Matching: | Who.Who.Who | Mateship | (0.7, 0.4) | +1 | Hit. ... |
    pattern = re.compile(r'\|\s*[A-Za-z0-9\.]+\s*\|\s*[^\*\|]+\s*\|\s*\(\s*([+-]?[0-9\.]+)\s*,\s*([+-]?[0-9\.]+)\s*\)\s*\|\s*([+-]?[0-9]+)\s*\|')

    for match in pattern.finditer(content):
        v = float(match.group(1))
        p = float(match.group(2))
        score = int(match.group(3))

        total_vectors += 1
        if score == 1:
            hits += 1
            v_total += v
            p_total += p
        elif score == -1:
            fails += 1
            v_total -= v
            p_total -= p
        else:
            misses += 1

percentage = (hits / total_vectors) * 100

active_count = hits + fails
if active_count > 0:
    avg_v = v_total / active_count
    avg_p = p_total / active_count
else:
    avg_v = 0
    avg_p = 0

final_out = os.path.join(out_dir, "Final_Judgement_Albanese_Audit.md")
with open(final_out, 'w', encoding='utf-8') as f:
    f.write("### HEGEMONIC AUDIT REPORT: ANTHONY ALBANESE'S AUSTRALIANISM INDEX\n\n")
    f.write("#### 1. Executive Summary\n")
    f.write("This audit evaluates Prime Minister Anthony Albanese against the 343-vector Australian Kanon.\n\n")
    f.write(f"- **Total Vectors Evaluated:** {total_vectors}\n")
    f.write(f"- **Hits (+1):** {hits}\n")
    f.write(f"- **Misses (0):** {misses}\n")
    f.write(f"- **Fails (-1):** {fails}\n\n")
    f.write(f"- **Australianism Percentage:** {percentage:.2f}%\n\n")
    f.write("#### 2. Psochic Vector Averages\n")
    f.write(f"- **Average Morality (υ):** {avg_v:.2f}\n")
    f.write(f"- **Average Will (ψ):** {avg_p:.2f}\n\n")
    f.write("#### 3. Trajectory Projection\n")
    f.write("Albanese operates primarily in the **Top-Left Quadrant (Grace)** of the Psochic Hegemony. His strong alignment with the 'Battler' archetype and 'Egalitarianism' (+υ) is matched by a pragmatic, incremental approach to Will (+ψ). His most significant deviation from traditional Labor Prime Ministers is his careful moderation of the 'Larrikin' vector, choosing institutional stability over populist combativeness.\n\n")
    f.write("His legacy trajectory hinges on balancing the 'Forgotten People' (cost of living/middle-class stability) with the 'First Nations Correction' (the Voice), demonstrating a willingness to expend political capital (+ψ) for structural 'Fair Go' (+υ).\n")

print("Created Final Judgement.")
