import sys

spec_path = "polytrope_transformer/docs/ARCHITECTURE_SPECIFICATION.md"

with open(spec_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update ASCII diagram bottom
old_block = '                      \u2299 +z (Physical Actuality / "IS")\n                      \u2297 -z (Non-Actuality / "IS NOT")'
new_block = '                      \u2299 +z ("to effect of" / Downstream Yield E)\n                      \u2297 -z ("to cause of" / Upstream Origin A)\n                      \u2299 z=0 (Immediate State on Plane / "IS")'

if old_block in text:
    text = text.replace(old_block, new_block)
    print("Updated ASCII diagram block")
else:
    print("Warning: old diagram block not found")

# 2. Update Intent vectors in diagram
old_i5_i6 = '  I5: Forward Evolution (+z)\n  I6: Historical Grounding (-z)'
new_i5_i6 = '  I5: Forward Effect (+z, "to effect of")\n  I6: Causal Origin (-z, "to cause of")'
if old_i5_i6 in text:
    text = text.replace(old_i5_i6, new_i5_i6)
    print("Updated I5/I6 in diagram")

# 3. Update Intent vectors in section 3.2
old_i5_desc = '* **$I_5$ (Forward Evolution)**: Actualizing novel manifest outcomes ($+z).'
new_i5_desc = '* **$I_5$ (Forward Effect)**: Driving downstream consequences and manifest yields ($+z$, "to effect of").'
if old_i5_desc in text:
    text = text.replace(old_i5_desc, new_i5_desc)
    print("Updated I5 description")

old_i6_desc = '* **$I_6$ (Historical Grounding)**: Anchoring in antecedent conditions and precedent ($-z).'
new_i6_desc = '* **$I_6$ (Causal Origin)**: Anchored in upstream physical antecedents and energetic causes ($-z$, "to cause of").'
if old_i6_desc in text:
    text = text.replace(old_i6_desc, new_i6_desc)
    print("Updated I6 description")

with open(spec_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Spec update finished successfully.")
