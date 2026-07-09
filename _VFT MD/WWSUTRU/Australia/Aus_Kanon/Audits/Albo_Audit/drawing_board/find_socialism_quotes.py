import json
import os

corpus_path = "albanese_corpus.jsonl"
if not os.path.exists(corpus_path):
    corpus_path = "../albanese_corpus.jsonl"

print("Searching corpus for socialism/pragmatism/doctrine keywords...")

keywords = ["democratic socialist", "socialism", "pragmatic", "doctrine", "ideology"]

if os.path.exists(corpus_path):
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            try:
                rec = json.loads(line)
                text = rec.get("text", "")
                date_str = rec.get("date", "")
                uniqueID = rec.get("uniqueID", "")
                
                for kw in keywords:
                    if kw in text.lower():
                        print(f"\nMatch found for '{kw}' at line {line_num} (ID: {uniqueID}, Date: {date_str})")
                        # Print surrounding text
                        idx = text.lower().find(kw)
                        start = max(0, idx - 150)
                        end = min(len(text), idx + 250)
                        print(f"  Snippet: ...{text[start:end].strip()}...")
            except Exception as e:
                pass
else:
    print("Corpus not found.")
