"""
Polytrope Embedding Inspector:
Extracts and visualizes the exact embeddings (32-dim latent vector, 3D phase space, 7D Q-planes)
produced by the Polytrope Transformer Kernel for any input sentence.
"""

import json
import re
import numpy as np
import pathlib

class SimpleTokenizer:
    def __init__(self, vocab_size=350):
        self.vocab_size = vocab_size
        self.word2idx = {"<PAD>": 0, "<UNK>": 1, "<BOS>": 2, "<EOS>": 3}
        self.idx2word = {0: "<PAD>", 1: "<UNK>", 2: "<BOS>", 3: "<EOS>"}
        
    def fit(self, texts):
        word_counts = {}
        for text in texts:
            words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
            for w in words:
                word_counts[w] = word_counts.get(w, 0) + 1
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        for w, _ in sorted_words[:self.vocab_size - len(self.word2idx)]:
            if w not in self.word2idx:
                idx = len(self.word2idx)
                self.word2idx[w] = idx
                self.idx2word[idx] = w

    def encode(self, text, max_len=16):
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        tokens = [self.word2idx.get(w, 1) for w in words[:max_len]]
        if len(tokens) < max_len:
            tokens = tokens + [0] * (max_len - len(tokens))
        return np.array(tokens, dtype=np.int32)

class PolytropeTransformer:
    def __init__(self, vocab_size=350, d_model=32, d_hidden=64, seq_len=16):
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.d_hidden = d_hidden
        self.seq_len = seq_len
        
        np.random.seed(42)
        self.embedding = np.random.randn(vocab_size, d_model) * 0.1
        self.W_q = np.random.randn(d_model, d_model) * 0.1
        self.W_k = np.random.randn(d_model, d_model) * 0.1
        self.W_v = np.random.randn(d_model, d_model) * 0.1
        
        self.W_ff1 = np.random.randn(d_model, d_hidden) * 0.1
        self.b_ff1 = np.zeros(d_hidden)
        self.W_ff2 = np.random.randn(d_hidden, d_model) * 0.1
        self.b_ff2 = np.zeros(d_model)
        
        self.W_geo = np.random.randn(d_model, 3) * 0.1
        self.b_geo = np.zeros(3)
        self.W_qplane = np.random.randn(d_model, 7) * 0.1
        self.b_qplane = np.zeros(7)

    def softmax(self, x, axis=-1):
        e_x = np.exp(x - np.max(x, axis=axis, keepdims=True))
        return e_x / np.sum(e_x, axis=axis, keepdims=True)

    def embed_sentence(self, token_ids):
        E = self.embedding[token_ids]
        Q = E @ self.W_q
        K = E @ self.W_k
        V = E @ self.W_v
        scores = (Q @ K.transpose(0, 2, 1)) / np.sqrt(self.d_model)
        attn = self.softmax(scores, axis=-1)
        ctx = attn @ V
        
        post_attn = E + ctx
        H_ff = np.tanh(post_attn @ self.W_ff1 + self.b_ff1)
        ff_out = H_ff @ self.W_ff2 + self.b_ff2
        H_out = post_attn + ff_out
        
        latent_embedding_32d = np.mean(H_out, axis=1)[0]
        coords_3d = 2.0 * np.tanh(latent_embedding_32d @ self.W_geo + self.b_geo)
        q_planes_7d = self.softmax(latent_embedding_32d @ self.W_qplane + self.b_qplane, axis=-1)
        manifold_state_10d = np.concatenate([coords_3d, q_planes_7d])
        
        return {
            "latent_vector_32d": latent_embedding_32d,
            "coords_3d": coords_3d,
            "q_planes_7d": q_planes_7d,
            "manifold_state_10d": manifold_state_10d,
            "attention_matrix": attn[0]
        }

def inspect_embeddings():
    sentences = [
        "It produces economic benefits as well as the spread of best practice",
        "The problem is training enough Australian pilots to fulfil domestic needs",
        "We need to make sure we can keep our planes in the air"
    ]
    
    tokenizer = SimpleTokenizer(vocab_size=200)
    tokenizer.fit(sentences)
    model = PolytropeTransformer(vocab_size=len(tokenizer.word2idx) + 10)
    
    plane_labels = [
        "Q1:Metaphysical (Who)", "Q2:Possible (What)", "Q3:Physical (Where)",
        "Q4:Lyrical (Why)", "Q5:Logical (How)", "Q6:Historical (Cause)", "Q7:Emotive (Effect)"
    ]
    
    exported_data = []
    for text in sentences:
        tokens = tokenizer.encode(text, max_len=16)
        res = model.embed_sentence(tokens[None, :])
        exported_data.append({
            "sentence": text,
            "latent_vector_32d": res["latent_vector_32d"].tolist(),
            "phase_space_coords_3d": {
                "upsilon": float(res["coords_3d"][0]),
                "psi": float(res["coords_3d"][1]),
                "z": float(res["coords_3d"][2])
            },
            "substrate_q_planes_7d": {plane_labels[i]: float(res["q_planes_7d"][i]) for i in range(7)},
            "manifold_state_vector_10d": res["manifold_state_10d"].tolist()
        })
        
    out_file = pathlib.Path("sentence_embeddings.json")
    out_file.write_text(json.dumps(exported_data, indent=2), encoding="utf-8")
    print(f"Exported complete numerical embedding vectors to {out_file}")

if __name__ == "__main__":
    inspect_embeddings()
