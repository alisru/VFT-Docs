import os
import re
import sys

# Configure stdout for utf-8
sys.stdout.reconfigure(encoding='utf-8')

# Paths
kanon_dir = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus Kanon"
audit_file = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hegemonic Audit_ Pauline Hanson tbf.md"

def normalize_coord(val):
    val = val.replace('\\', '').strip()
    if val in ['0.0', '0', '±0.0', '±0']:
        return '0.0'
    if not val.startswith('+') and not val.startswith('-'):
        return '+' + val
    return val

# 1. Parse official coordinates from Kanon sheets
official_coords = {}
judgment_files = [f for f in os.listdir(kanon_dir) if f.endswith('_JUDGMENT.md')]
print(f"Loading official coordinates from {len(judgment_files)} files...")

for f_name in judgment_files:
    path = os.path.join(kanon_dir, f_name)
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Table row pattern: | Vector | Entry | u | psi | ...
    # e.g., | Who.Who.Who | **Mateship** | +0.7 | +0.4 | ...
    rows = re.findall(r'\|\s*([\w.]+)\s*\|\s*\*\*([^*]+)\*\*\s*\|\s*([^|]+)\|\s*([^|]+)\|', content)
    for r in rows:
        v_id = r[0].strip()
        name = r[1].strip().lower()
        u_val = normalize_coord(r[2])
        psi_val = normalize_coord(r[3])
        
        # Store by both ID and Name to handle duplicates correctly
        # Also clean name from First Nations suffixes to make it easier to match
        clean_name = re.sub(r'\[first nations perspective\]', '', name).strip()
        clean_name = re.sub(r'\(fn\)', '', clean_name).strip()
        
        official_coords.setdefault(v_id, []).append({
            'name': name,
            'clean_name': clean_name,
            'u': u_val,
            'psi': psi_val
        })

print(f"Loaded {sum(len(v) for v in official_coords.values())} official vector facets.")

# 2. Read the active audit file
with open(audit_file, 'r', encoding='utf-8') as f:
    audit_content = f.read()

# 3. Find and update vector headers in the audit body
# Pattern: **(X.Y.Z) Name (υ: ..., ψ: ...): STATUS.**
header_pattern = r'\*\*\((\w+\.\w+\.\w+)\)\s+([^*:\n]+)\s+\(υ:\s*([^,]+),\s*ψ:\s*([^)]+)\):\s*(\w+)\.?\*\*'

updated_count = 0
miss_to_fail_count = 0
not_found_count = 0

def replace_header(match):
    global updated_count, miss_to_fail_count, not_found_count
    v_id, name, u_orig, psi_orig, status = match.groups()
    
    # Clean the audit name for matching
    clean_audit_name = name.strip().lower()
    clean_audit_name = re.sub(r'\[first nations perspective\]', '', clean_audit_name).strip()
    clean_audit_name = re.sub(r'\(fn\)', '', clean_audit_name).strip()
    clean_audit_name = re.sub(r'/.*', '', clean_audit_name).strip() # handles "The Telegraph / NBN" -> "the telegraph"
    
    # Determine the status
    new_status = status
    if v_id == "Why.How.Effect" and clean_audit_name.startswith("volunteering"):
        new_status = "FAIL"
        miss_to_fail_count += 1
        print("Changing (Why.How.Effect) Volunteering to FAIL in body.")
    elif v_id == "How.What.Where" and clean_audit_name.startswith("the black box"):
        new_status = "FAIL"
        miss_to_fail_count += 1
        print("Changing (How.What.Where) The Black Box to FAIL in body.")
        
    # Find matching official coordinate
    u_new, psi_new = u_orig, psi_orig
    if v_id in official_coords:
        facets = official_coords[v_id]
        best_match = None
        # Try matching by clean name
        for f in facets:
            if f['clean_name'] in clean_audit_name or clean_audit_name in f['clean_name']:
                best_match = f
                break
        if not best_match:
            # Default to first facet
            best_match = facets[0]
            
        u_new = best_match['u']
        psi_new = best_match['psi']
    else:
        not_found_count += 1
        
    # Format coordinates with correct backslashes for markdown
    # Note: the original file has: (υ: \+0.7, ψ: \+0.4)
    def format_coord(val):
        if val.startswith('+'):
            return r'\+' + val[1:]
        elif val.startswith('-'):
            return r'\-' + val[1:]
        return val
        
    u_formatted = format_coord(u_new)
    psi_formatted = format_coord(psi_new)
    
    if u_orig != u_new or psi_orig != psi_new or status != new_status:
        updated_count += 1
        
    return f"**({v_id}) {name} (υ: {u_formatted}, ψ: {psi_formatted}): {new_status}.**"

# Perform replacement in the audit file
new_audit_content = re.sub(header_pattern, replace_header, audit_content)

# 4. Modify the specific brief/justification text for the two misses
new_audit_content = new_audit_content.replace(
    "This is a miss because her mechanical trajectory bypasses the profound, communal rescue reflex of the Australian culture.",
    "This is a fail because her trajectory actively rejects and undermines the profound, communal rescue reflex of the Australian culture in favor of top-down political grievance."
)
new_audit_content = new_audit_content.replace(
    "She misses the vector because her methodology is inherently ideological, completely bypassing the objective diagnostic tools of the Kanon.",
    "She fails the vector because her methodology is inherently ideological, explicitly and actively rejecting the objective diagnostic tools of the Kanon in favor of populist grievance."
)

print(f"Completed body pass. Updated {updated_count} vector lines. Changed {miss_to_fail_count} MISS -> FAIL.")

# 5. Recalculate and update summaries for all 7 planes
plane_sections = [
    ('Plane 1', r'# \*\*Plane 1: Who\*\*', r'# \*\*Plane 2, Possible What\*\*'),
    ('Plane 2', r'# \*\*Plane 2, Possible What\*\*', r'# \*\*Plane 3, Location where\*\*'),
    ('Plane 3', r'# \*\*Plane 3, Location where\*\*', r'# \*\*Plane 4, Lyrical Why\*\*'),
    ('Plane 4', r'# \*\*Plane 4, Lyrical Why\*\*', r'# \*\*Plane 5, Logical How\*\*'),
    ('Plane 5', r'# \*\*Plane 5, Logical How\*\*', r'# \*\*Plane 6, Historical Cause\*\*'),
    ('Plane 6', r'# \*\*Plane 6, Historical Cause\*\*', r'# \*\*Plane 7, Emotional Effect\*\*'),
    ('Plane 7', r'# \*\*Plane 7, Emotional Effect\*\*', r'# \*\*In Totality: Pauline Hanson\*\*')
]

overall_hits = 0
overall_fails = 0
overall_misses = 0

for name, start_pat, end_pat in plane_sections:
    start_match = re.search(start_pat, new_audit_content)
    end_match = re.search(end_pat, new_audit_content)
    if start_match and end_match:
        section = new_audit_content[start_match.start():end_match.start()]
        
        # Parse vectors in this section
        v_matches = re.findall(r'\*\*\((\w+\.\w+\.\w+)\)\s+([^*:\n]+)\s+\(υ:\s*([^,]+),\s*ψ:\s*([^)]+)\):\s*(\w+)\.?\*\*', section)
        hits = sum(1 for m in v_matches if m[4] == 'HIT')
        fails = sum(1 for m in v_matches if m[4] == 'FAIL')
        misses = sum(1 for m in v_matches if m[4] == 'MISS')
        
        overall_hits += hits
        overall_fails += fails
        overall_misses += misses
        
        net_score = hits - fails
        net_sign = "+" if net_score >= 0 else ""
        
        # Update Plane summary line in new_audit_content
        # Summary line pattern: **Plane X [Name] Score:** \+Y Net Score (A HIT, B FAIL, C MISS)
        # First we extract the Plane index
        plane_idx = name.split()[-1]
        sum_pattern = rf'\*\*Plane {plane_idx} [^*:\n]+ Score:\*\*\s*[^\n]+'
        
        # Determine format depending on if there are misses
        if misses > 0 or plane_idx in ['2', '3', '4', '5', '6', '7']:
            new_sum_line = f"**Plane {plane_idx} Score:** {net_sign}{net_score} Net Score ({hits} HIT, {fails} FAIL, {misses} MISS)"
        else:
            new_sum_line = f"**Plane {plane_idx} Score:** {net_sign}{net_score} Net Score ({hits} HIT, {fails} FAIL)"
            
        # Re-fetch the specific plane designation from the old text to preserve names if any
        old_sum_match = re.search(rf'\*\*Plane {plane_idx} ([^*:\n]+) Score:\*\*\s*[^\n]+', new_audit_content)
        if old_sum_match:
            designation = old_sum_match.group(1).strip()
            new_sum_line = f"**Plane {plane_idx} {designation} Score:** {net_sign}{net_score} Net Score ({hits} HIT, {fails} FAIL, {misses} MISS)"
            
        new_audit_content = re.sub(sum_pattern, new_sum_line, new_audit_content)
        print(f"Updated summary for {name}: HIT={hits}, FAIL={fails}, MISS={misses}, Net={net_sign}{net_score}")
    else:
        print(f"Error: {name} section bounds not found!")

# 6. Recalculate top-line metrics
total_vectors = overall_hits + overall_fails + overall_misses
final_net = overall_hits - overall_fails
final_net_sign = "+" if final_net >= 0 else ""
final_percentage = round((final_net / total_vectors) * 100, 1)

print(f"\nFinal Totals recalculated:")
print(f"Overall Hits: {overall_hits}")
print(f"Overall Fails: {overall_fails}")
print(f"Overall Misses: {overall_misses}")
print(f"Total Vectors: {total_vectors}")
print(f"Final Net Score: {final_net_sign}{final_net}")
print(f"Final Alignment Score %: {final_percentage}%")

# Update top-line scorecard
# Pattern to find:
# **Final Alignment Score: 27.8%** (+97 Net Score out of 349 core vectors)
# 
# * 	
# 	**Hits 	(Structural Alignments):** 	223  
# * 	
# 	**Fails 	(Systemic Violations):** 	126  
# * 	
# 	**Misses 	(Ignored Vectors):** 	0

scorecard_top_pattern = r'\*\*Final Alignment Score:[^*]+\*\* \([^\n]+\)'
new_scorecard_top = f"**Final Alignment Score: {final_percentage}%** ({final_net_sign}{final_net} Net Score out of {total_vectors} core vectors)"
new_audit_content = re.sub(scorecard_top_pattern, new_scorecard_top, new_audit_content)

new_audit_content = re.sub(r'\*\*Hits \t\(Structural Alignments\):\*\*\s*\d+', f"**Hits \t(Structural Alignments):** \t{overall_hits}", new_audit_content)
new_audit_content = re.sub(r'\*\*Fails \t\(Systemic Violations\):\*\*\s*\d+', f"**Fails \t(Systemic Violations):** \t{overall_fails}", new_audit_content)
new_audit_content = re.sub(r'\*\*Misses \t\(Ignored Vectors\):\*\*\s*\d+', f"**Misses \t(Ignored Vectors):** \t{overall_misses}", new_audit_content)

# Update "In Totality" and bottom scorecard if they exist
new_audit_content = re.sub(r'\*\*Misses \(Ignored\):\*\*\s*\d+', f"**Misses (Ignored):** \t{overall_misses}", new_audit_content)

# 7. Write the updated content back to the audit file
with open(audit_file, 'w', encoding='utf-8') as f:
    f.write(new_audit_content)

print(f"\nSuccessfully updated {audit_file} with synchronized coordinates and corrected scores!")
