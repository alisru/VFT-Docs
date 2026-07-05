import json, sys
sys.stdout.reconfigure(encoding="utf-8")
with open(r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Plane_1_Identity.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("=== Section 1.6: Who.Cause (Origin) ===")
for n in [n for n in data if n.get("address","").startswith("Who.Cause")]:
    print(n["address"] + " | " + n["name"] + " (v: " + str(n["coordinates"]["v"]) + ", psi: " + str(n["coordinates"]["psi"]) + ")")

print("\n=== Section 1.7: Who.Effect (Destination) ===")
for n in [n for n in data if n.get("address","").startswith("Who.Effect")]:
    print(n["address"] + " | " + n["name"] + " (v: " + str(n["coordinates"]["v"]) + ", psi: " + str(n["coordinates"]["psi"]) + ")")
