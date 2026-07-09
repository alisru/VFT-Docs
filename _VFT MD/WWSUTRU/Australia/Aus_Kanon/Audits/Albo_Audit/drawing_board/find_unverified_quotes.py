import re
import os

files = ["Plane_1_Identity_albanese.md", "Plane_2_Definition_Albanese.md"]
failed_tags = [
    "alboadelaide23",
    "alborepublictrans25",
    "alburyvisit26",
    "alp_platform_2022",
    "alpoleadership13",
    "eurekaballarat23",
    "jscemelectoral24",
    "loopholes23",
    "nrfpass23",
    "voicesenate23"
]

print("Target footnote usages in the text:")
for fn in files:
    if os.path.exists(fn):
        with open(fn, "r", encoding="utf-8") as f:
            content = f.read()
        for tag in failed_tags:
            # Search for occurrences of [^tag] in the text
            # Find the paragraph containing it
            pattern = re.compile(rf'.*?\[\^{tag}\].*?\n', re.MULTILINE)
            matches = pattern.findall(content)
            if matches:
                print(f"\n--- Tag: {tag} ({fn}) ---")
                for m in matches:
                    print(f"  Usage: {m.strip()}")
