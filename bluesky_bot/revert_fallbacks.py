target_path = r"e:\Vector Field Theory\VFT Docs\bluesky_bot\google_ai_studio_one_shot.py"
with open(target_path, "r", encoding="utf-8") as f:
    content = f.read()

s_curr = 'DEFAULT_FALLBACKS = [\n    "gemini-3.8-flash",\n    "gemini-2.5-flash",\n    "gemini-3.7-flash",'
s_orig = 'DEFAULT_FALLBACKS = [\n    "gemini-3.8-flash",\n    "gemini-3.7-flash",\n    "gemini-2.5-flash",'
if s_curr in content:
    content = content.replace(s_curr, s_orig, 1)

with open(target_path, "w", encoding="utf-8") as f:
    f.write(content)

print("DEFAULT_FALLBACKS reverted to original!")
