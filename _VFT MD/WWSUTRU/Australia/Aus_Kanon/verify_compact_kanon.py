import os
import json
import re
import sys
from pathlib import Path

COMPACT_JSON_DIR = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus Kanon\compact JSON")
PLANES = [
    (1, "Identity"),
    (2, "Definition"),
    (3, "Land"),
    (4, "Drive"),
    (5, "Method"),
    (6, "Foundation"),
    (7, "Result")
]

VECTORS = ["Who", "What", "Where", "Why", "How", "Cause", "Effect"]

def count_sentences(text):
    if not text:
        return 0
    # Split by .!? followed by space or end of string
    sentences = re.split(r'[.!?]+(?:\s+|$)', text)
    return len([s for s in sentences if s.strip()])

def verify_file(file_path, plane_num, plane_name):
    if not file_path.exists():
        print(f"[ERROR] File not found: {file_path}")
        return False, 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to parse JSON in {file_path.name}: {e}")
        return False, 0

    if not isinstance(data, list):
        print(f"[ERROR] Root element in {file_path.name} is not a list.")
        return False, 0

    item_count = len(data)
    if item_count != 49:
        print(f"[ERROR] {file_path.name} has {item_count} items, expected exactly 49.")
        return False, item_count

    errors = 0
    warnings = 0

    for idx, item in enumerate(data):
        address = item.get("address")
        name = item.get("name")
        plane = item.get("plane")
        plane_name_val = item.get("plane_name")
        canonical_quote = item.get("canonical_quote")
        attribution = item.get("attribution")
        source = item.get("source")
        description = item.get("description")
        establishes = item.get("establishes")
        coordinates = item.get("coordinates")
        zone = item.get("zone")
        judgment_rationale = item.get("judgment_rationale")

        item_label = f"Item #{idx+1} ({address or 'No Address'} - {name or 'No Name'})"

        # Check required fields
        for field in ["address", "name", "plane", "plane_name", "canonical_quote", "description", "establishes", "coordinates", "zone", "judgment_rationale"]:
            if item.get(field) is None:
                print(f"[ERROR] {file_path.name} {item_label}: Missing required field '{field}'")
                errors += 1

        # Check plane numbers
        if plane != plane_num:
            print(f"[ERROR] {file_path.name} {item_label}: plane field is {plane}, expected {plane_num}")
            errors += 1
        if plane_name_val != plane_name:
            print(f"[ERROR] {file_path.name} {item_label}: plane_name field is '{plane_name_val}', expected '{plane_name}'")
            errors += 1

        # Check coordinates structure
        if isinstance(coordinates, dict):
            v = coordinates.get("v")
            psi = coordinates.get("psi")
            if v is None or psi is None:
                print(f"[ERROR] {file_path.name} {item_label}: Coordinates must have both 'v' and 'psi'. Got {coordinates}")
                errors += 1
            else:
                if not (-2.0 <= v <= 2.0):
                    print(f"[ERROR] {file_path.name} {item_label}: Coordinate 'v' ({v}) is outside boundary [-2.0, 2.0]")
                    errors += 1
                if not (-2.0 <= psi <= 2.0):
                    print(f"[ERROR] {file_path.name} {item_label}: Coordinate 'psi' ({psi}) is outside boundary [-2.0, 2.0]")
                    errors += 1
        else:
            print(f"[ERROR] {file_path.name} {item_label}: coordinates field is not a dictionary.")
            errors += 1

        # Check address format and validity
        if address:
            parts = address.split('.')
            if len(parts) != 3:
                print(f"[ERROR] {file_path.name} {item_label}: address '{address}' is not in 'Plane.Sense.Vector' format.")
                errors += 1
            else:
                p_part, s_part, v_part = parts
                expected_p = VECTORS[plane_num - 1]
                if p_part != expected_p:
                    print(f"[ERROR] {file_path.name} {item_label}: address plane part '{p_part}' does not match expected '{expected_p}'.")
                    errors += 1
                if s_part not in VECTORS:
                    print(f"[ERROR] {file_path.name} {item_label}: address sense part '{s_part}' is invalid.")
                    errors += 1
                if v_part not in VECTORS:
                    print(f"[ERROR] {file_path.name} {item_label}: address vector part '{v_part}' is invalid.")
                    errors += 1
        
        # Check "This establishes..." formula in establishes field
        if establishes:
            clean_establishes = establishes.strip()
            if not clean_establishes.startswith("This establishes"):
                print(f"[WARNING] {file_path.name} {item_label}: establishes narrative does not start with 'This establishes...'")
                warnings += 1

        # Check sentence density metrics (min 4 sentences for description, min 4 sentences for establishes)
        desc_sentences = count_sentences(description)
        est_sentences = count_sentences(establishes)
        if desc_sentences < 4:
            print(f"[ERROR] {file_path.name} {item_label}: Description field has only {desc_sentences} sentences (Target: min 4).")
            errors += 1
        if est_sentences < 4:
            print(f"[ERROR] {file_path.name} {item_label}: Establishes field has only {est_sentences} sentences (Target: min 4).")
            errors += 1

    if errors > 0:
        print(f"[FAIL] {file_path.name}: {errors} errors, {warnings} warnings.")
        return False, item_count
    else:
        print(f"[PASS] {file_path.name}: All 49 items are compliant. ({warnings} warnings)")
        return True, item_count

def main():
    print("Starting verification of Australian Kanon compact JSON files...")
    all_ok = True
    total_items = 0

    for plane_num, plane_name in PLANES:
        file_name = f"Plane_{plane_num}_{plane_name}_compact.json"
        file_path = COMPACT_JSON_DIR / file_name
        ok, count = verify_file(file_path, plane_num, plane_name)
        total_items += count
        if not ok:
            all_ok = False

    print("---------------------------------------------")
    print(f"Total items processed: {total_items} / 343")
    if all_ok and total_items == 343:
        print("\033[92m[SUCCESS] All Australian Kanon compact JSON files verified successfully!\033[0m")
        sys.exit(0)
    else:
        print("\033[91m[FAILURE] Verification failed. Please check the errors above.\033[0m")
        sys.exit(1)

if __name__ == "__main__":
    main()
