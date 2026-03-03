import os
import re

base_dir = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America"

planes = [
    ("Plane_1_Identity", "Identity (Who)", 49),
    ("Plane_2_Definition", "Definition (What)", 49),
    ("Plane_3_Land", "Land (Where)", 49),
    ("Plane_4_Drive", "Drive (Why)", 49),
    ("Plane_5_Method", "Method (How)", 49),
    ("Plane_6_Cause", "Cause (Origin)", 49),
    ("Plane_7_Effect", "Effect (Result)", 49)
]

# 1. Load Base Kanon Coordinates (using _JUDGEMENT files)
base_kanon_morals = {}
for p_file, p_name, max_score in planes:
    k_path = os.path.join(base_dir, f"American_Kanon_{p_file}_JUDGEMENT.md")
    if os.path.exists(k_path):
        with open(k_path, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
            for line in lines:
                if '|' in line and not '---|' in line and not 'Vector | Entry' in line:
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 6 and re.match(r'^[A-Za-z]+\.[A-Za-z]+\.[A-Za-z]+$', parts[1]):
                        vec_id = parts[1]
                        try:
                            # Absolute magnitudes of the Kanonic Ideals
                            v = abs(float(parts[3].replace('+','').replace('−','-').strip()))
                        except:
                            v = 1.0
                        try:
                            # Absolute magnitudes of the Kanonic Ideals
                            p = abs(float(parts[4].replace('+','').replace('−','-').strip()))
                        except:
                            p = 1.0
                        
                        # Store the raw absolute magnitudes of the Base Kanon
                        base_kanon_morals[vec_id] = (v, p)
                        
print(f"Loaded {len(base_kanon_morals)} Base Kanon metrics for Pure Math Injection.")

# 2. Update Trump Files with Pure Math based on his explicit +/- evaluations
for p_file, p_name, max_score in planes:
    t_path = os.path.join(base_dir, f"Trump_American_Kanon_{p_file}.md")
    
    if os.path.exists(t_path):
        with open(t_path, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
            
        new_lines = []
        for line in lines:
            if '|' in line and not '---|' in line and not 'Vector | Entry' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 6 and re.match(r'^[A-Za-z]+\.[A-Za-z]+\.[A-Za-z]+$', parts[1]):
                    vec_id = parts[1]
                    
                    # 1. Parse Trump's evaluated PASS/FAIL status (+1, -1, 0)
                    score_str = parts[3].strip()
                    if score_str.startswith('1') or score_str.startswith('+1'):
                        score = 1
                    elif score_str.startswith('-1'):
                        score = -1
                    else:
                        score = 0
                    
                    # 2. Parse Trump's manually evaluated POLARITIES
                    try:
                        trump_eval_v = float(parts[4].replace('+','').replace('−','-').strip())
                    except:
                        trump_eval_v = 1.0
                        
                    try:
                        trump_eval_p = float(parts[5].replace('+','').replace('−','-').strip())
                    except:
                        trump_eval_p = 1.0
                    
                    # Determine the original polarities (-1 for negative, 1 for positive)
                    polarity_v = -1 if trump_eval_v < 0 else 1
                    polarity_p = -1 if trump_eval_p < 0 else 1
                        
                    # 3. Fetch Base Kanon absolute magnitudes
                    base_mag_v, base_mag_p = base_kanon_morals.get(vec_id, (1.0, 1.0))
                    
                    # 4. Inject exact Kanon magnitudes, snapping to Trump's evaluated polarities
                    if score == 0:
                        # Neutral / Miss -> 0.0 regardless of Kanon magnitude
                        final_v = 0.0
                        final_p = 0.0
                    else:
                        final_v = base_mag_v * polarity_v
                        final_p = base_mag_p * polarity_p
                            
                    # 5. Format and inject
                    parts[4] = f"{final_v:+.1f}".replace('+0.0', '0.0').replace('-0.0', '0.0')
                    parts[5] = f"{final_p:+.1f}".replace('+0.0', '0.0').replace('-0.0', '0.0')
                    
                    new_line = " | ".join(parts).strip()
                    if not new_line.startswith('|'): new_line = '| ' + new_line
                    if not new_line.endswith('|'): new_line = new_line + ' |'
                    new_lines.append(new_line)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
                
        with open(t_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        print(f"Updated {p_file} with Pure Kanon Math (Preserving Polarities)")
