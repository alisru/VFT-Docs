import json
import os

file_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Collapse\Taxonomy\Matrix_Ground_Truth.json"

def sort_dict_by_key_numeric(d):
    # Sorts a dictionary by keys, treating them as hierarchical numbers (e.g. "1.1", "1.10", "2.1")
    # Returns a new dict with sorted keys.
    try:
        # Try to sort by converting to list of ints: "1.2.3" -> [1, 2, 3]
        sorted_keys = sorted(d.keys(), key=lambda k: [int(x) for x in k.split('.')])
    except ValueError:
        # Fallback to string sort if keys are not numeric
        sorted_keys = sorted(d.keys())
    
    return {k: d[k] for k in sorted_keys}

def main():
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. Sort Planes
    if "Tree" in data and "Planes" in data["Tree"]:
        print("Sorting Planes...")
        planes = data["Tree"]["Planes"]
        # Sort Planes (1, 2, 3...)
        planes = sort_dict_by_key_numeric(planes)
        
        # 2. Sort States within Planes
        for p_key, p_val in planes.items():
            if "States" in p_val:
                states = p_val["States"]
                states = sort_dict_by_key_numeric(states)
                
                # 3. Sort Vectors within States
                for s_key, s_val in states.items():
                    if "Vectors" in s_val:
                        vectors = s_val["Vectors"]
                        vectors = sort_dict_by_key_numeric(vectors)
                        s_val["Vectors"] = vectors
                
                p_val["States"] = states
        
        data["Tree"]["Planes"] = planes

    # 4. Sort Index
    if "Index" in data:
        print("Sorting Index...")
        data["Index"] = sort_dict_by_key_numeric(data["Index"])

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print("Ordering correction complete.")

if __name__ == "__main__":
    main()
