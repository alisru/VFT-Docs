import json
import sys

def search(keywords):
    count = 0
    with open('albanese_corpus.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            text = data['text']
            # check if all keywords are in the text
            if all(kw.lower() in text.lower() for kw in keywords):
                print(f"Date: {data['date']} | UniqueID: {data['uniqueID']}")
                print(f"Speaker: {data['speaker_name']}")
                print(f"Snippet: {text[:600]}...")
                print("-" * 80)
                count += 1
                if count >= 10:
                    break

if __name__ == '__main__':
    search(sys.argv[1:])
