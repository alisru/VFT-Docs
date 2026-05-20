import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

audit_file = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hegemonic Audit_ Pauline Hanson tbf.md"

with open(audit_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the planes and their section ranges in the text
planes = [
    {
        'id': 1,
        'name': 'Who',
        'start_marker': '# **Plane 1: Who**',
        'end_marker': '# **Plane 2, Possible What**'
    },
    {
        'id': 2,
        'name': 'What',
        'start_marker': '# **Plane 2, Possible What**',
        'end_marker': '# **Plane 3, Location where**'
    },
    {
        'id': 3,
        'name': 'Where',
        'start_marker': '# **Plane 3, Location where**',
        'end_marker': '# **Plane 4, Lyrical Why**'
    },
    {
        'id': 4,
        'name': 'Why',
        'start_marker': '# **Plane 4, Lyrical Why**',
        'end_marker': '# **Plane 5, Logical How**'
    },
    {
        'id': 5,
        'name': 'How',
        'start_marker': '# **Plane 5, Logical How**',
        'end_marker': '# **Plane 6, Historical Cause**'
    },
    {
        'id': 6,
        'name': 'Cause',
        'start_marker': '# **Plane 6, Historical Cause**',
        'end_marker': '# **Plane 7, Emotional Effect**'
    },
    {
        'id': 7,
        'name': 'Effect',
        'start_marker': '# **Plane 7, Emotional Effect**',
        'end_marker': '# **In Totality: Pauline Hanson**'
    }
]

# Regex pattern to find vector status headers: e.g. **(Who.Who.Who) Mateship (υ: +0.7, ψ: +0.4): FAIL.**
vector_pattern = r'\*\*\((\w+\.\w+\.\w+)\)\s+([^*:\n]+)\s+\(υ:\s*([^,]+),\s*ψ:\s*([^)]+)\):\s*(\w+)\.?\*\*'

overall_hits = 0
overall_fails = 0
overall_misses = 0

plane_stats = {}

for plane in planes:
    p_id = plane['id']
    start_pos = content.find(plane['start_marker'])
    end_pos = content.find(plane['end_marker'])
    
    if start_pos == -1 or end_pos == -1:
        print(f"Error finding boundaries for Plane {p_id}")
        continue
        
    plane_text = content[start_pos:end_pos]
    
    # Find all vectors in this plane
    vectors = re.findall(vector_pattern, plane_text)
    
    hits = sum(1 for v in vectors if v[4] == 'HIT')
    fails = sum(1 for v in vectors if v[4] == 'FAIL')
    misses = sum(1 for v in vectors if v[4] == 'MISS')
    total = len(vectors)
    
    net = hits - fails
    net_sign = "+" if net >= 0 else ""
    percentage = round((net / total) * 100, 1) if total > 0 else 0.0
    
    plane_stats[p_id] = {
        'hits': hits,
        'fails': fails,
        'misses': misses,
        'total': total,
        'net': net,
        'percentage': percentage,
        'text': plane_text
    }
    
    overall_hits += hits
    overall_fails += fails
    overall_misses += misses

total_vectors = overall_hits + overall_fails + overall_misses
final_net = overall_hits - overall_fails
final_net_sign = "+" if final_net >= 0 else ""
final_percentage = round((final_net / total_vectors) * 100, 1) if total_vectors > 0 else 0.0

print(f"CALCULATED STATS:")
for p_id, stats in plane_stats.items():
    print(f"Plane {p_id}: HIT={stats['hits']}, FAIL={stats['fails']}, MISS={stats['misses']}, Total={stats['total']}, Net={stats['net']}{stats['net']}, %={stats['percentage']}%")

print(f"Total Vectors: {total_vectors}")
print(f"Total Hits: {overall_hits}")
print(f"Total Fails: {overall_fails}")
print(f"Total Misses: {overall_misses}")
print(f"Final Net Score: {final_net_sign}{final_net}")
print(f"Final Percentage: {final_percentage}%")
