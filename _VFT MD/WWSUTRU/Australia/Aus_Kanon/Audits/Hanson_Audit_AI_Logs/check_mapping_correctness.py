import json

compact_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus Kanon\compact JSON\Plane_7_Result_compact.json"
hanson_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hegemonic Audit_ Pauline Hanson.json"

with open(compact_path, "r", encoding="utf-8") as f:
    c_data = json.load(f)

with open(hanson_path, "r", encoding="utf-8") as f:
    h_data = json.load(f)

h_plane7 = next(p for p in h_data["planes"] if p["plane_num"] == 7)
h_vectors = h_plane7["vectors"]

# We will map each canonical vector address to the Hanson vector that represents it.
# Let's write out the mapping of address -> hanson_index
# based on our analysis:
mapping = {
    # 7.1 Who
    "Effect.Who.Who": 6,     # The Quiet Australian (meta stated_name in slot 6)
    "Effect.Who.What": 0,    # The Multicultural Citizen (meta stated_name in slot 0)
    "Effect.Who.Where": 2,   # The Coastal Dweller (meta stated_name Retiree in slot 2)
    "Effect.Who.Why": 1,     # The Aspirational (meta stated_name Aspirational in slot 1)
    "Effect.Who.How": 4,     # The Sports Fanatic (meta stated_name Rent-Seeker in slot 4)
    "Effect.Who.Cause": 5,   # The Digger's Heir (meta stated_name New Australian in slot 5)
    "Effect.Who.Effect": 3,  # The Citizen (meta stated_name First Nations Elder in slot 3)

    # 7.2 Where (canonical Sense 7.2)
    "Effect.Where.Who": 14,  # The Australian Diaspora (meta stated_name Pacific Family in slot 14)
    "Effect.Where.What": 15, # The Commodity (meta stated_name Alliance US/UK in slot 15)
    "Effect.Where.Where": 16,# The Alliance (meta stated_name Sprawl in slot 16)
    "Effect.Where.Why": 17,  # The Middle Power (meta stated_name Closed Border in slot 17)
    "Effect.Where.How": 18,  # Soft Power (meta stated_name Asian Market in slot 18)
    "Effect.Where.Cause": 19,# The Pacific (meta stated_name Dispossession in slot 19)
    "Effect.Where.Effect": 20,# The Asian Century (meta stated_name Regional Divide in slot 20)

    # 7.3 What (canonical Sense 7.3)
    "Effect.What.Who": 11,   # The Home Owner (meta stated_name Negative Gearing in slot 11) - wait!
    # Wait, in slot 11, name is "The Renewable Transition", stated_name is "Negative Gearing".
    # In compact, "The Home Owner" is Effect.What.Who.
    # In Hanson, Negative Gearing (slot 11) is about housing wealth. So yes, it maps to The Home Owner!
    "Effect.What.What": 8,   # The Superannuation Balance (meta stated_name Superannuation in slot 8)
    "Effect.What.Where": 9,  # The University Sector (meta stated_name Detention Centre in slot 9)
    "Effect.What.Why": 7,    # The Medicare Card (meta stated_name Medicare in slot 7)
    "Effect.What.How": 22,   # The Renewable Transition (meta stated_name The Energy Transition in slot 22) - wait!
    # Wait, in slot 22, name is "Sustainability vs. Extraction", stated_name is "The Energy Transition".
    # The Energy Transition is about coal vs renewables, which matches "The Renewable Transition" (Effect.What.How)!
    "Effect.What.Cause": 12, # Biodiversity (meta stated_name The NDIS in slot 12)
    "Effect.What.Effect": 13,# Stability (meta stated_name ABC in slot 13)

    # 7.4 Why
    "Effect.Why.Who": 21,    # Egalitarianism vs. Aspiration (meta stated_name Treaty/Voice in slot 21)
    "Effect.Why.What": 47,   # Sustainability vs. Extraction (meta stated_name The Extractive Economy in slot 47) - wait!
    # Wait, in slot 47, stated_name is "The Extractive Economy (Commodity)".
    # This matches Sustainability vs. Extraction!
    "Effect.Why.Where": 23,  # Urban vs. Regional (meta stated_name The Housing Crisis in slot 23) - wait!
    # In slot 23, stated_name is "The Housing Crisis".
    # Wait! In compact, Effect.Why.Where is Urban vs. Regional.
    "Effect.Why.Why": 24,    # Fair Go vs. Market (meta stated_name The Culture War in slot 24)
    "Effect.Why.How": 25,    # Reconciliation vs. Denial (meta stated_name The Republic Debate in slot 25)
    "Effect.Why.Cause": 26,  # Luck vs. Effort (meta stated_name Climate Anxiety in slot 26)
    "Effect.Why.Effect": 27, # Unity vs. Division (meta stated_name National Pride vs Cringe in slot 27)

    # 7.5 How
    "Effect.How.Who": 28,    # The Vote (meta stated_name Royal Commission in slot 28) - wait!
    "Effect.How.What": 29,   # The Royal Commission (meta stated_name Social Media Populism in slot 29)
    "Effect.How.Where": 30,  # The High Court (meta stated_name The Protest / Rally in slot 30)
    "Effect.How.Why": 31,    # The Media (meta stated_name Media Monopoly in slot 31)
    "Effect.How.How": 32,    # The ABS (meta stated_name The Referendum in slot 32)
    "Effect.How.Cause": 33,  # The Pub Test (meta stated_name The Strike in slot 33)
    "Effect.How.Effect": 34, # The Treasury (meta stated_name Compulsory Voting in slot 34)

    # 7.6 Cause
    "Effect.Cause.Who": 35,   # The Next Generation (meta stated_name The Apology in slot 35)
    "Effect.Cause.What": 36,  # The Energy Transition (meta stated_name Australia Day in slot 36) - wait!
    "Effect.Cause.Where": 37, # Northern Australia (meta stated_name ANZAC Day in slot 37)
    "Effect.Cause.Why": 38,   # The Republic (meta stated_name Tampa in slot 38)
    "Effect.Cause.How": 39,   # Treaty [First Nations] (meta stated_name Gun Control in slot 39)
    "Effect.Cause.Cause": 40, # Asia (meta stated_name Mabo in slot 40)
    "Effect.Cause.Effect": 41,# The Good Life (meta stated_name The Dismissal in slot 41)

    # 7.7 Effect
    "Effect.Effect.Who": 42,   # The Fair Go (meta stated_name Mateship in slot 42)
    "Effect.Effect.What": 43,  # The Lifestyle (meta stated_name Complacency/Apathy in slot 43)
    "Effect.Effect.Where": 44, # Girt By Sea (meta stated_name The Fair Go in slot 44)
    # Effect.Effect.Why has two canonical:
    # "The Second Chance" and "Dispossession [First Nations Perspective]"
    # Let's see: in Hanson, Slot 45 has stated_name "Paranoia / Security Obsession", which is the only Effect.Effect.Why.
    # We should map Slot 45 to both or one of them?
    # Actually, Slot 45 is "Dispossession [First Nations Perspective]" in Hanson JSON.
    # What about "The Second Chance"?
    # Is there a slot for "The Second Chance"?
    # Wait, let's look at slot 45. In Hanson, slot 45 is named "Dispossession [First Nations Perspective]" with coords -0.8, -0.7.
    # Let's map slot 45 to the canonical "Dispossession [First Nations Perspective]".
    # What about "The Second Chance" (canonical coords 0.8, 0.5)?
    # Is there a Hanson slot for it?
    # No, it's missing. We can create it or copy/adjust.
    "Effect.Effect.How": 46,   # She'll Be Right (meta stated_name Solidarity in Crisis in slot 46)
    "Effect.Effect.Cause": 47, # The Land (meta stated_name The Extractive Economy in slot 47) - wait, we already mapped 47 to Effect.Why.What?
    # Let's check! Slot 47 has stated_name "The Extractive Economy (Commodity)".
    # Canonical Effect.Effect.Cause is "The Land".
    # Canonical Effect.Why.What is "Sustainability vs. Extraction".
    # Wait, slot 47 was mapped to Effect.Effect.Cause in Hanson JSON (it has address Effect.Effect.Cause).
    # So slot 47 should go to Effect.Effect.Cause ("The Land").
    # If slot 47 goes to Effect.Effect.Cause, then what goes to Effect.Why.What ("Sustainability vs. Extraction")?
    # Wait! In Hanson, is there a slot for Effect.Why.What?
    # Yes, Slot 22 has address Effect.Why.What! Its name in Hanson is "Sustainability vs. Extraction".
    # Stated name in slot 22 is "The Energy Transition".
    # So Slot 22 content goes to Effect.Why.What!
    # Wait, then what goes to Effect.Cause.What ("The Energy Transition")?
    # In Hanson, Slot 36 has address Effect.Cause.What! Stated name is "Australia Day (Jan 26)".
    # So Slot 36 goes to Effect.Cause.What!
    # Yes, this is correct!
    "Effect.Effect.Effect": 48 # Australia (meta stated_name Sovereign Independence in slot 48)
}

# Let's print out what mappings are missing or duplicated
mapped_indices = list(mapping.values())
print(f"Mapped indices count: {len(mapped_indices)} / 49")
print(f"Duplicates: {set([x for x in mapped_indices if mapped_indices.count(x) > 1])}")
print(f"Missing from 49: {set(range(49)) - set(mapped_indices)}")
