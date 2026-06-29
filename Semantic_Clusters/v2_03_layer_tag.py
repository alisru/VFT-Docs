import os
import json
import sys
import re

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    manifest_path = os.path.join(script_dir, "sentence_manifest.json")
    output_path = os.path.join(script_dir, "layer_tags.json")

    # Force stdout encoding to UTF-8
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')

    if not os.path.exists(manifest_path):
        print(f"Error: manifest file not found at: {manifest_path}")
        sys.exit(1)

    print("Loading sentence manifest for layer tagging...")
    with open(manifest_path, 'r', encoding='utf-8') as f:
        sentences = json.load(f)

    # Heuristic definitions
    def_patterns = [
        r"\b(?:is defined as|refers to|means|denotes|represents)\b",
        r"\b(?:upsilon|psi|qualia|hegemonikon|hēgemonikon|TEF|TEV|attractor|rNet|possibility space)\b"
    ]
    cond_patterns = [
        r"\b(?:if|when|unless|provided that|given that|requires|threshold|activation)\b"
    ]
    ex_patterns = [
        r"\b(?:for example|for instance|applied to|specifically|such as)\b",
        r"\b(?:Hanson|Dutton|Albanese|Abbott|Howard|Taylor|US Election|Australia|China|Taiwan)\b"
    ]

    def_regexes = [re.compile(p, re.IGNORECASE) for p in def_patterns]
    cond_regexes = [re.compile(p, re.IGNORECASE) for p in cond_patterns]
    ex_regexes = [re.compile(p, re.IGNORECASE) for p in ex_patterns]

    layer_tags = {}
    print(f"Categorizing {len(sentences)} sentences into VFT layers...")

    for idx, s in enumerate(sentences):
        text = s["raw_text"]
        sid = s["sentence_id"]

        # Simple hierarchical checks
        is_def = any(rx.search(text) for rx in def_regexes)
        is_cond = any(rx.search(text) for rx in cond_regexes)
        is_ex = any(rx.search(text) for rx in ex_regexes)

        if is_def:
            category = "Definition"
        elif is_cond:
            category = "Conditional"
        elif is_ex:
            category = "Example"
        else:
            category = "Assertion"

        layer_tags[sid] = category

    print(f"Saving categorized layer tags to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(layer_tags, f, indent=2, ensure_ascii=False)
    
    print("Layer tagging completed successfully.")

if __name__ == "__main__":
    main()
