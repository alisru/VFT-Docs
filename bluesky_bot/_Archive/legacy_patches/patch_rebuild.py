fp = r"e:\Vector Field Theory\VFT Docs\bluesky_bot\rebuild_registries_son.py"
with open(fp, "r", encoding="utf-8") as f:
    content = f.read()

if "import shutil" not in content:
    content = "import shutil\n" + content
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)
    print("Added import shutil")
else:
    print("shutil already imported")
