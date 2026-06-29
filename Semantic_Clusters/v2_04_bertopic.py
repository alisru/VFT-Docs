import os
import json
import sys
import numpy as np
from bertopic import BERTopic
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    manifest_path = os.path.join(script_dir, "sentence_manifest.json")
    embeddings_path = os.path.join(script_dir, "embeddings_v2.npy")
    output_path = os.path.join(script_dir, "topic_assignments.json")

    # Force stdout encoding to UTF-8
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')

    if not os.path.exists(manifest_path) or not os.path.exists(embeddings_path):
        print("Error: Missing sentence manifest or embeddings binary.")
        sys.exit(1)

    print("Loading manifests and embeddings...")
    with open(manifest_path, 'r', encoding='utf-8') as f:
        sentences = json.load(f)
    embeddings = np.load(embeddings_path)

    # Use raw_text for generating c-TF-IDF keyword summaries,
    # but cluster using the contextualized embeddings!
    raw_texts = [s["raw_text"] for s in sentences]

    print("Initializing UMAP & HDBSCAN components for BERTopic...")
    umap_model = UMAP(
        n_neighbors=15, 
        n_components=5, 
        min_dist=0.0, 
        metric='cosine', 
        random_state=42
    )
    
    hdbscan_model = HDBSCAN(
        min_cluster_size=50, 
        min_samples=10, 
        metric='euclidean', 
        cluster_selection_method='eom',
        prediction_data=True
    )

    vectorizer_model = CountVectorizer(stop_words="english")

    print("Running BERTopic fit_transform (using precomputed contextualized embeddings)...")
    topic_model = BERTopic(
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer_model,
        calculate_probabilities=False, # Set to False to run faster; we can still map topic IDs
        verbose=True
    )

    topics, _ = topic_model.fit_transform(raw_texts, embeddings=embeddings)

    # Get topic information and labels
    print("Extracting generated topics and auto-labels...")
    topic_info = topic_model.get_topic_info()
    
    # Create cluster ID to auto-label mapping
    topic_labels = {}
    for idx, row in topic_info.iterrows():
        tid = int(row["Topic"])
        name = row["Name"]
        # Name is usually "Topic_Word1_Word2_Word3" - let's extract words
        # e.g., Topic -1 or Topic 0
        words = [w[0] for w in topic_model.get_topic(tid)] if tid != -1 else ["Noise"]
        clean_label = ", ".join(words[:4])
        topic_labels[tid] = {
            "full_name": name,
            "label": clean_label
        }

    # Map each sentence to its topic and label
    sentence_topics = {}
    for idx, s in enumerate(sentences):
        sid = s["sentence_id"]
        tid = int(topics[idx])
        label_info = topic_labels.get(tid, {"full_name": "Noise", "label": "Noise"})
        
        sentence_topics[sid] = {
            "topic_id": tid,
            "topic_name": label_info["full_name"],
            "topic_label": label_info["label"]
        }

    print(f"Saving BERTopic topic assignments to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sentence_topics, f, indent=2, ensure_ascii=False)

    # Save the topic info dataframe/dict for downstream reference
    info_path = os.path.join(script_dir, "topic_info_registry.json")
    with open(info_path, 'w', encoding='utf-8') as f:
        # Convert df to clean serializable dict
        registry = topic_info.to_dict(orient="records")
        json.dump(registry, f, indent=2, ensure_ascii=False)

    print(f"BERTopic processing completed. Found {len(topic_info) - 1} distinct topics.")

if __name__ == "__main__":
    main()
