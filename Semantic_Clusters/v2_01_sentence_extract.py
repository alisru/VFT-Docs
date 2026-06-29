import os
import json
import sys
import spacy

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    manifest_path = os.path.join(script_dir, "corpus_manifest.json")
    output_path = os.path.join(script_dir, "sentence_manifest.json")

    # Force stdout encoding to UTF-8
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')

    if not os.path.exists(manifest_path):
        print(f"Error: manifest file not found at: {manifest_path}")
        sys.exit(1)

    print("Loading spaCy model...")
    try:
        nlp = spacy.load("en_core_web_sm", disable=["ner", "tagger", "lemmatizer"])
    except OSError:
        print("spaCy model 'en_core_web_sm' not found. Installing now...")
        import subprocess
        subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
        nlp = spacy.load("en_core_web_sm", disable=["ner", "tagger", "lemmatizer"])

    # Add sentencizer component
    if "sentencizer" not in nlp.pipe_names:
        nlp.add_pipe("sentencizer")

    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    sentence_manifest = []
    total_docs = len(manifest)

    print(f"Processing {total_docs} files for sentence extraction...")

    for doc_idx, doc in enumerate(manifest):
        file_path = doc["file_path"]
        title = doc["title"]
        
        if not os.path.exists(file_path):
            continue

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue

        # Split into paragraphs
        paragraphs = [p.strip() for p in content.split('\n\n') if len(p.strip()) > 15]

        for p_idx, para in enumerate(paragraphs):
            # Parse paragraph with spaCy to extract sentences
            doc_spacy = nlp(para)
            sentences = [sent.text.strip() for sent in doc_spacy.sents if len(sent.text.strip()) > 10]
            
            if not sentences:
                continue

            # First sentence is the topic sentence
            topic_sentence = sentences[0]

            for s_idx, sent in enumerate(sentences):
                # Contextualized sentence format
                contextualized_text = f"{title} | {topic_sentence} | {sent}"
                
                sentence_manifest.append({
                    "sentence_id": f"{doc_idx}_{p_idx}_{s_idx}",
                    "file_path": file_path,
                    "relative_path": doc["relative_path"],
                    "document_title": title,
                    "paragraph_index": p_idx,
                    "sentence_index": s_idx,
                    "raw_text": sent,
                    "contextualized_text": contextualized_text
                })

        if (doc_idx + 1) % 50 == 0 or (doc_idx + 1) == total_docs:
            print(f"Processed {doc_idx + 1}/{total_docs} files. Total sentences: {len(sentence_manifest)}")

    print(f"Writing {len(sentence_manifest)} sentence entries to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sentence_manifest, f, indent=2, ensure_ascii=False)
        
    print("Sentence extraction completed successfully.")

if __name__ == "__main__":
    main()
