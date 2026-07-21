import re

p = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Hegemonic_Audit_Pauline_Hanson_FINAL.md"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

print("File length (chars):", len(text))
print()
print("Plane headers present:")
for i, name in enumerate(["Identity", "Definition", "Land", "Drive", "Method", "Foundation", "Result"], start=1):
    marker = f"Plane {i}, "
    print(f"  Plane_{i}_{name}:", marker in text or name in text)

print()
print("Sources.md section present:", "[^ms96]:" in text or "AGPS Copy" in text or "Sources" in text[-3000:])
print()

node_count = len(re.findall(r"\): (HIT|FAIL)\.", text))
print("Approx node HIT/FAIL headers found:", node_count)
