import json
import os
import sys

# Set standard output to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

corpus_path = "albanese_corpus.jsonl"
if not os.path.exists(corpus_path):
    corpus_path = "../albanese_corpus.jsonl"

queries = {
    "lucky_country": ["lucky country", "make our own luck"],
    "tyranny_distance": ["tyranny of distance"],
    "cultural_cringe": ["cultural cringe", "cringe"]
}

matches = {k: [] for k in queries.keys()}

if os.path.exists(corpus_path):
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            try:
                rec = json.loads(line)
                text = rec.get("text", "")
                date_str = rec.get("date", "")
                uniqueID = rec.get("uniqueID", "")
                
                for k, keywords in queries.items():
                    for kw in keywords:
                        if kw in text.lower():
                            matches[k].append({
                                "line": line_num,
                                "id": uniqueID,
                                "date": date_str,
                                "kw": kw,
                                "text": text
                            })
                            break
            except Exception as e:
                pass

for k, mlist in matches.items():
    print(f"\n==================== Matches for Category: {k} (Count: {len(mlist)}) ====================")
    for m in mlist[:5]:
        print(f"Line {m['line']} | Date: {m['date']} | Keyword: '{m['kw']}'")
        idx = m['text'].lower().find(m['kw'])
        start = max(0, idx - 100)
        end = min(len(m['text']), idx + 300)
        snippet = m['text'][start:end].replace('\n', ' ').strip()
        print(f"  Snippet: ...{snippet}...")
