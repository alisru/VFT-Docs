import os
import json
import sys
import numpy as np
import torch
from sentence_transformers import SentenceTransformer

def clean_and_truncate_context(title, topic_sent, target_sent):
    if len(topic_sent) > 150:
        topic_sent = topic_sent[:150] + "..."
    if len(target_sent) > 300:
        target_sent = target_sent[:300] + "..."
    return f"{title} | {topic_sent} | {target_sent}"

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    manifest_path = os.path.join(script_dir, "sentence_manifest.json")
    output_path = os.path.join(script_dir, "embeddings_v2.npy")
    checkpoint_dir = os.path.join(script_dir, "embedding_checkpoints")
    
    # Do NOT delete checkpoint_dir on startup to preserve cached chunks
    os.makedirs(checkpoint_dir, exist_ok=True)

    # Force stdout encoding to UTF-8
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')

    if not os.path.exists(manifest_path):
        print(f"Error: manifest file not found at: {manifest_path}")
        sys.exit(1)

    print("Loading sentence manifest...")
    with open(manifest_path, 'r', encoding='utf-8') as f:
        sentences = json.load(f)

    total_sentences = len(sentences)
    if total_sentences == 0:
        print("No sentences found to embed.")
        return

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # Load BAAI/bge-large-en-v1.5
    model_name = 'BAAI/bge-large-en-v1.5'
    print(f"Loading SentenceTransformer model ('{model_name}')...")
    model = SentenceTransformer(model_name, device=device)

    print(f"Generating embeddings for {total_sentences} sentences...")
    
    texts = []
    for s in sentences:
        texts.append(clean_and_truncate_context(
            s["document_title"], 
            s.get("paragraph_topic_sentence", s["raw_text"]),
            s["raw_text"]
        ))
    
    embeddings_list = []
    chunk_size = 20000
    
    for i in range(0, total_sentences, chunk_size):
        chunk_file = os.path.join(checkpoint_dir, f"chunk_{i}.npy")
        if os.path.exists(chunk_file):
            print(f"Loading cached chunk: sentences {i} to {min(i+chunk_size, total_sentences)}")
            chunk_emb = np.load(chunk_file)
            embeddings_list.append(chunk_emb)
        else:
            print(f"Embedding chunk: sentences {i} to {min(i+chunk_size, total_sentences)} on {device}...")
            chunk_texts = texts[i:i+chunk_size]
            chunk_emb = model.encode(
                chunk_texts, 
                show_progress_bar=True, 
                batch_size=128  # Increased batch size to 128 for faster GPU processing
            )
            np.save(chunk_file, chunk_emb)
            embeddings_list.append(chunk_emb)

    print("Concatenating all chunks...")
    all_embeddings = np.vstack(embeddings_list)

    print(f"Embeddings shape: {all_embeddings.shape}")
    print(f"Saving final embeddings matrix to {output_path}...")
    np.save(output_path, all_embeddings)
    
    # Clean up checkpoints
    print("Cleaning up temporary chunk checkpoints...")
    for i in range(0, total_sentences, chunk_size):
        chunk_file = os.path.join(checkpoint_dir, f"chunk_{i}.npy")
        if os.path.exists(chunk_file):
            try:
                os.remove(chunk_file)
            except Exception:
                pass
    try:
        os.rmdir(checkpoint_dir)
    except Exception:
        pass

    print("Embedding process completed successfully.")

if __name__ == "__main__":
    main()
