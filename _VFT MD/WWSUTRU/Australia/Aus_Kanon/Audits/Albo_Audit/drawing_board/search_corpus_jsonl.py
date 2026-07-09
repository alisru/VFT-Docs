import json
import os

corpus_path = "albanese_corpus.jsonl"
if not os.path.exists(corpus_path):
    # Try looking one directory up
    corpus_path = "../albanese_corpus.jsonl"

print(f"Searching corpus: {corpus_path}")

targets = [
    ("alboadelaide23", "Adelaide", "30 August 2023", "14 October"),
    ("nrfpass23", "National Reconstruction Fund", "28 March 2023", "passes"),
    ("alborepublictrans25", "republic", "28 September 2025", "King Charles")
]

if os.path.exists(corpus_path):
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            try:
                rec = json.loads(line)
                body = rec.get("body", "")
                title = rec.get("title", "")
                date_str = rec.get("date", "")
                
                # Check for matches
                for key, kw1, date_kw, kw2 in targets:
                    if kw1.lower() in body.lower() or kw1.lower() in title.lower():
                        if date_kw in date_str or date_kw in body or date_kw in title:
                            if kw2.lower() in body.lower():
                                print(f"\nFOUND MATCH FOR {key} at line {line_num}!")
                                print(f"  Title: {title}")
                                print(f"  Date: {date_str}")
                                print(f"  Snippet: {body[:300].strip()}...")
                                # Print first 100 characters of matching sentence
                                sentences = body.split(".")
                                for s in sentences:
                                    if kw2.lower() in s.lower() and kw1.lower() in s.lower():
                                        print(f"  Matching Sentence: {s.strip()}.")
                                        break
            except Exception as e:
                pass
else:
    print("Corpus file not found.")
