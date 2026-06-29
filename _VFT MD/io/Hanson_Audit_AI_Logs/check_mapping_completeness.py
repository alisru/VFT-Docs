import json

compact_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus Kanon\compact JSON\Plane_7_Result_compact.json"
hanson_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hegemonic Audit_ Pauline Hanson.json"

with open(compact_path, "r", encoding="utf-8") as f:
    c_data = json.load(f)

with open(hanson_path, "r", encoding="utf-8") as f:
    h_data = json.load(f)

h_plane7 = next(p for p in h_data["planes"] if p["plane_num"] == 7)
h_vectors = h_plane7["vectors"]

# Mapping from canonical address and name to Hanson JSON vector index
# We need to distinguish between the two Effect.Effect.Why vectors by name.
address_name_to_hanson_idx = {
    # 7.1 Who
    ("Effect.Who.Who", "The Quiet Australian"): 6,
    ("Effect.Who.What", "The Multicultural Citizen"): 0,
    ("Effect.Who.Where", "The Coastal Dweller"): 2,
    ("Effect.Who.Why", "The Aspirational"): 1,
    ("Effect.Who.How", "The Sports Fanatic"): 4,
    ("Effect.Who.Cause", "The Digger's Heir"): 5,
    ("Effect.Who.Effect", "The Citizen"): 3,

    # 7.2 Where (Geographies)
    ("Effect.Where.Who", "The Australian Diaspora"): 14,
    ("Effect.Where.What", "The Commodity"): 15,
    ("Effect.Where.Where", "The Alliance"): 16,
    ("Effect.Where.Why", "The Middle Power"): 17,
    ("Effect.Where.How", "Soft Power"): 18,
    ("Effect.Where.Cause", "The Pacific"): 19,
    ("Effect.Where.Effect", "The Asian Century"): 20,

    # 7.3 What (Institutions)
    ("Effect.What.Who", "The Home Owner"): 11,
    ("Effect.What.What", "The Superannuation Balance"): 8,
    ("Effect.What.Where", "The University Sector"): 9,
    ("Effect.What.Why", "The Medicare Card"): 7,
    ("Effect.What.How", "The Renewable Transition"): 10,
    ("Effect.What.Cause", "Biodiversity"): 12,
    ("Effect.What.Effect", "Stability"): 13,

    # 7.4 Why
    ("Effect.Why.Who", "Egalitarianism vs. Aspiration"): 21,
    ("Effect.Why.What", "Sustainability vs. Extraction"): 22,
    ("Effect.Why.Where", "Urban vs. Regional"): 23,
    ("Effect.Why.Why", "Fair Go vs. Market"): 24,
    ("Effect.Why.How", "Reconciliation vs. Denial"): 25,
    ("Effect.Why.Cause", "Luck vs. Effort"): 26,
    ("Effect.Why.Effect", "Unity vs. Division"): 27,

    # 7.5 How
    ("Effect.How.Who", "The Vote"): 28,
    ("Effect.How.What", "The Royal Commission"): 29,
    ("Effect.How.Where", "The High Court"): 30,
    ("Effect.How.Why", "The Media"): 31,
    ("Effect.How.How", "The ABS"): 32,
    ("Effect.How.Cause", "The Pub Test"): 33,
    ("Effect.How.Effect", "The Treasury"): 34,

    # 7.6 Cause
    ("Effect.Cause.Who", "The Next Generation"): 35,
    ("Effect.Cause.What", "The Energy Transition"): 36,
    ("Effect.Cause.Where", "Northern Australia"): 37,
    ("Effect.Cause.Why", "The Republic"): 38,
    ("Effect.Cause.How", "Treaty [First Nations Perspective]"): 39,
    ("Effect.Cause.Cause", "Asia"): 40,
    ("Effect.Cause.Effect", "The Good Life"): 41,

    # 7.7 Effect
    ("Effect.Effect.Who", "The Fair Go"): 42,
    ("Effect.Effect.What", "The Lifestyle"): 43,
    ("Effect.Effect.Where", "Girt By Sea"): 44,
    ("Effect.Effect.Why", "The Second Chance"): None, # missing in Hanson, will be custom-generated
    ("Effect.Effect.Why", "Dispossession [First Nations Perspective]"): 45,
    ("Effect.Effect.How", "She'll Be Right"): 46,
    ("Effect.Effect.Cause", "The Land"): 47,
    ("Effect.Effect.Effect", "Australia"): 48
}

used_indices = set(x for x in address_name_to_hanson_idx.values() if x is not None)
all_indices = set(range(49))
print("Unmapped Hanson indices:", all_indices - used_indices)
