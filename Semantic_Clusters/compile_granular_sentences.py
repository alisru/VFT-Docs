import os
import json
import re
import sys
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Try loading spaCy
nlp = None
try:
    import spacy
    nlp = spacy.load("en_core_web_sm", disable=["ner"])
    print("spaCy and en_core_web_sm loaded successfully (NER disabled for speed).", flush=True)
except Exception as e:
    print(f"spaCy not available or model not loaded (using fallback regex parser): {e}", flush=True)

# Define 16 Hegemony points and their descriptions for cosine similarity mapping
HEGEMONY_POINTS = {
    "gg-gg": "Reality, History, Realism, Historicism. Objective reality, facts, historical trajectory, and structural evolution.",
    "gg-le": "Language, Psychology, Relationalism, Understanding. Communication, relational meaning, intersubjective understanding.",
    "gg-ge": "Sociology, Society, Collectivism, Communitarianism. Empathy, community, social cohesion, collective systems.",
    "gg-lg": "Internal Judgment, Religion, Prudence, Charity. Wisdom, careful judgment, benevolence, moral law, selfless love.",
    "lg-gg": "Learning, Emotional-physics, Empiricism, Stoicism. Learning, temperance, emotional resilience, empirical observation.",
    "lg-le": "Meta-Physics, Physics, Imagination, Objectivity. Relationship between abstract ideas and physical laws, creative imagination.",
    "lg-ge": "Spirituality, Maths, Faith, Order. Spiritual connection, divine mathematical order, structural symmetry.",
    "lg-lg": "Intelligence, Religion, Hope, Charity. Hopeful intelligence, spiritual aspiration, divine charity.",
    "le-gg": "Maths, Spirituality, Chaos, Nihilism. Mathematical chaos, active rejection of meaning, nihilistic worldview.",
    "le-le": "Religion, Intelligence, Hatred, Despair. Active malice, ideological hatred, despair, hopelessness.",
    "le-ge": "Emotional-physics, Learning, Indulgence, Folly. Lack of self-control, folly, immediate gratification, emotional volatility.",
    "le-lg": "Physics, Meta-Physics, Denial, Dogma. Denial of facts, rigid dogma, closed-mindedness, ideological blindness.",
    "ge-gg": "Society, Sociology, Anarchy, Apathy. Societal apathy, passive allowance of harm, anarchy, social collapse.",
    "ge-le": "Internal Judgment, The World, Corruption, Cowardice. Systemic corruption, personal cowardice, compromise, ethical failure.",
    "ge-ge": "History, Reality, Erasure, Delusion. Historical erasure, self-delusion, complete denial of reality, revisionism.",
    "ge-lg": "Psychology, Language, Confusion, Deceit. Deliberate deceit, manipulation, mental confusion, lying, gaslighting."
}

# Advanced NLP + POS Classification
def classify_doc_nlp(doc, text):
    try:
        text_lower = text.lower().strip()
        
        # 1. Reference Check
        if re.search(r'\[\d+\]|\(see ref\.?|\bref\b\.?\s+\d+|\b(figure|fig|table)\s+\d+', text_lower):
            return "reference"
            
        # 2. Example Check
        if (text_lower.startswith("for example") or 
            text_lower.startswith("for instance") or 
            text_lower.startswith("such as") or
            "e.g." in text_lower or 
            "specifically" in text_lower):
            return "example"
            
        # 3. Conditional / Logical Rule
        has_conditional_conjunction = False
        has_modal = False
        for token in doc:
            # Check for modal verbs (should, must, implies, resolves)
            if token.pos_ == "AUX" and token.lemma_ in ["should", "must", "could", "would", "shall"]:
                has_modal = True
            if token.lemma_ in ["imply", "resolve", "lead", "yield", "necessitate"]:
                has_modal = True
            # Check for conditional conjunctions
            if token.dep_ == "mark" and token.lemma_ in ["if", "when", "unless", "because", "since", "whenever"]:
                has_conditional_conjunction = True
                
        if has_conditional_conjunction or has_modal or " therefore " in text_lower or " implies " in text_lower:
            return "conditional"
            
        # 4. Definition / Axiom (Noun + defining verb + complement)
        has_defining_verb = False
        for token in doc:
            if token.pos_ in ["VERB", "AUX"] and token.lemma_ in ["be", "define", "represent", "formalize", "denote", "constitute", "refer"]:
                # Verify it has a subject and complement
                has_subj = any(t.dep_ in ["nsubj", "nsubjpass"] for t in token.children)
                has_comp = any(t.dep_ in ["attr", "dobj", "prep", "acomp"] for t in token.children)
                if has_subj and has_comp:
                    has_defining_verb = True
                    break
                    
        if has_defining_verb or text_lower.startswith("axiom:") or "is defined as" in text_lower:
            return "definition"
            
        return "assertion"
    except Exception as e:
        return classify_sentence_fallback(text)

def classify_sentence_fallback(text):
    text_lower = text.lower().strip()
    
    if re.search(r'\[\d+\]|\(see ref\.?|\bref\b\.?\s+\d+|\b(figure|fig|table)\s+\d+', text_lower):
        return "reference"
        
    if (text_lower.startswith("for example") or 
        text_lower.startswith("for instance") or 
        text_lower.startswith("such as") or
        "e.g." in text_lower or 
        "specifically" in text_lower):
        return "example"
        
    if (text_lower.startswith("if ") or 
        " implies " in text_lower or 
        " leads to " in text_lower or 
        " therefore " in text_lower or
        " then " in text_lower or 
        " resolves to " in text_lower or
        " because " in text_lower):
        return "conditional"
        
    if (re.search(r'\b(is|are) defined as\b', text_lower) or 
        re.search(r'\b(refers|refer) to\b', text_lower) or 
        re.search(r'\bformalizes\b', text_lower) or
        re.search(r'\b(is|are) the study of\b', text_lower) or
        re.search(r'\b(represents|represent) the\b', text_lower) or
        text_lower.startswith("the definition of") or
        text_lower.startswith("axiom:") or
        " means " in text_lower):
        return "definition"
        
    return "assertion"

def split_into_sentences(text):
    # Standard sentence boundary detector that ignores decimals/abbreviations
    sentence_end = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')
    return [s.strip() for s in sentence_end.split(text) if len(s.strip()) > 8]

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    md_folder = os.path.join(workspace_root, "_VFT MD")
    output_path = os.path.join(script_dir, "granular_sentence_index.json")

    # Force stdout encoding to UTF-8
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')

    if not os.path.exists(md_folder):
        print(f"Error: _VFT MD folder not found at: {md_folder}", flush=True)
        return

    # Check for existing index for incremental update
    indexed_files = set()
    existing_by_file = {}
    if os.path.exists(output_path):
        try:
            print("Loading existing granular index for incremental update...", flush=True)
            with open(output_path, 'r', encoding='utf-8') as f:
                existing_records = json.load(f)
            for r in existing_records:
                f_name = r["file"]
                if f_name not in existing_by_file:
                    existing_by_file[f_name] = []
                existing_by_file[f_name].append(r)
            indexed_files = set(existing_by_file.keys())
            print(f"Loaded existing index with {len(existing_records)} sentences across {len(indexed_files)} files.", flush=True)
        except Exception as e:
            print(f"Could not load existing index (rebuilding from scratch): {e}", flush=True)

    print("Scanning markdown files...", flush=True)
    files_on_disk = []
    for root, dirs, files in os.walk(md_folder):
        for file in files:
            if file.endswith('.md') and not file.startswith('index_'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, md_folder)
                files_on_disk.append((rel_path, full_path))

    print(f"Found {len(files_on_disk)} markdown files on disk.", flush=True)

    final_sentence_records = []
    new_files_to_process = []
    
    for rel_path, full_path in files_on_disk:
        if rel_path in indexed_files:
            # Re-use existing records
            final_sentence_records.extend(existing_by_file[rel_path])
        else:
            new_files_to_process.append((rel_path, full_path))

    print(f"Incremental Update: Keeping {len(final_sentence_records)} sentences from {len(files_on_disk) - len(new_files_to_process)} already indexed files.", flush=True)
    print(f"Processing {len(new_files_to_process)} new/modified files...", flush=True)

    if len(new_files_to_process) == 0:
        print("No new or modified files to process. Index is up to date.", flush=True)
        return

    # Loading model only when we actually have new files to process!
    print("Loading SentenceTransformer model...", flush=True)
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Encode Hegemony Point description vectors
    print("Encoding Hegemony coordinates vectors...", flush=True)
    points_keys = list(HEGEMONY_POINTS.keys())
    points_desc = list(HEGEMONY_POINTS.values())
    points_embeddings = model.encode(points_desc)

    new_sentence_records = []
    for file_idx, (rel_path, full_path) in enumerate(new_files_to_process):
        if (file_idx + 1) % 10 == 0 or file_idx == len(new_files_to_process) - 1:
            print(f"Parsing new file {file_idx + 1}/{len(new_files_to_process)}: {rel_path}", flush=True)
            
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Chunk to Paragraphs
        paragraphs = [p.strip() for p in content.split('\n\n') if len(p.strip()) > 15]
        
        for p_idx, p_text in enumerate(paragraphs):
            # Split Paragraph into Sentences
            sentences = split_into_sentences(p_text)
            
            for s_idx, s_text in enumerate(sentences):
                new_sentence_records.append({
                    "file": rel_path,
                    "paragraph": p_idx,
                    "sentence": s_idx,
                    "text": s_text,
                    "type": "assertion", # placeholder
                    "topic_id": -1,
                    "hegemony_mappings": {}
                })

    total_new_sentences = len(new_sentence_records)
    print(f"Found {total_new_sentences} new sentences. Starting classification...", flush=True)
    
    if total_new_sentences > 0:
        # Batch process linguistic classification using spaCy nlp.pipe
        if nlp is not None:
            print("Running batch spaCy NLP pipeline (this is fast)...", flush=True)
            texts = [r["text"] for r in new_sentence_records]
            # Process sentences in batches with nlp.pipe
            docs = list(nlp.pipe(texts, batch_size=512))
            
            print("Running parse tree classifications...", flush=True)
            for i, doc in enumerate(docs):
                new_sentence_records[i]["type"] = classify_doc_nlp(doc, new_sentence_records[i]["text"])
        else:
            print("Using fallback regex parser...", flush=True)
            for r in new_sentence_records:
                r["type"] = classify_sentence_fallback(r["text"])

        # Batch embedding of all new sentences
        print("Generating sentence embeddings (this may take a few moments)...", flush=True)
        sentence_texts = [r["text"] for r in new_sentence_records]
        sentence_embeddings = model.encode(sentence_texts, show_progress_bar=True)

        print("Mapping sentences to Hegemony coordinates...", flush=True)
        # Calculate cosine similarity matrix
        sim_matrix = cosine_similarity(sentence_embeddings, points_embeddings)

        for i in range(total_new_sentences):
            mappings = {}
            for p_idx, key in enumerate(points_keys):
                sim = float(sim_matrix[i][p_idx])
                mappings[key] = round(sim, 4)
                
            new_sentence_records[i]["hegemony_mappings"] = mappings

        # Combine existing and new records
        final_sentence_records.extend(new_sentence_records)

    # Save granular sentence index
    print(f"Writing granular index ({len(final_sentence_records)} sentences) to: {output_path}", flush=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_sentence_records, f, indent=2, ensure_ascii=False)

    print("Success! Sentence-level index compiled.", flush=True)

if __name__ == "__main__":
    main()
