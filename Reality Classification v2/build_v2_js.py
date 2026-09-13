"""
build_v2_js.py
Compiles aec_dictionary.json into aec_dictionary.js with zero comment prefix
to guarantee flawless, CORS-free loading in any browser.
"""

import json
import os

V2_DIR = os.path.dirname(__file__)
JSON_PATH = os.path.join(V2_DIR, "aec_dictionary.json")
JS_PATH = os.path.join(V2_DIR, "aec_dictionary.js")

def build():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    json_str = json.dumps(data, ensure_ascii=False)
    # Write directly starting with window.AEC_DICT (no leading single-line comment)
    js_content = f"window.AEC_DICT = {json_str};\n"

    with open(JS_PATH, "w", encoding="utf-8") as f:
        f.write(js_content)

    print(f"[SUCCESS] Built {JS_PATH} (Size: {len(js_content)} chars). Starts cleanly with window.AEC_DICT.")

if __name__ == "__main__":
    build()
