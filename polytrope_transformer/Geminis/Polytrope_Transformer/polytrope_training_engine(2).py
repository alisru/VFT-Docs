"""
Scaled Training & Ingestion Run on Expanded Corpus (500+ Statements)
Canonical Seven Planes & Antipodal Fulcrum Aligned.
"""

import json
import os
import re
import time
import numpy as np
import pathlib

# ============================================================================
# 1. EXPANDED DATASET INGESTION
# ============================================================================

def load_all_corpora():
    corpus_files = [
        ("downloads/albanese_statements_news.jsonl", "news"),
        ("downloads/albanese_statements_1.jsonl", "news"),
        ("downloads/albanese_statements_1999.jsonl", "hansard")
    ]
    
    statements = []
    
    for filepath, ctype in corpus_files:
        if not os.path.exists(filepath):
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    if ctype == "news":
                        quote = data.get("quote", "").strip()
                        headline = data.get("headline", "").strip()
                        text = quote if len(quote) > 20 else headline
                    else: # hansard
                        text = data.get("text", "").strip()
                        # Take first substantial sentence or paragraph
                        if len(text) > 250:
                            sentences = re.split(r'(?<=[.!?]) +', text)
                            text = " ".join(sentences[:2])
                            
                    if text and len(text) > 15:
                        statements.append({
                            "text": text,
                            "type": ctype,
                            "source": data.get("outlet") or data.get("debate_title") or "Hansard"
                        })
                except Exception:
                    continue
                    
    return statements

# ============================================================================
# 2. SEVEN PLANES ANNOTATION SIEVE
# ============================================================================

def annotate_statement(text):
    text_lower = text.lower()
    
    # 1. Kinetic Work: Action (+psi) vs Counteraction/Drag (-psi)
    action_words = ["build", "produce", "train", "keep", "increase", "make", "create", "spread", "invest", "support", "reform", "deliver", "fund"]
    drag_words = ["problem", "shortage", "fail", "fatal", "crash", "dying", "toll", "decline", "urgent", "crisis", "cut", "loss", "danger", "threat"]
    action_score = sum(w in text_lower for w in action_words)
    drag_score = sum(w in text_lower for w in drag_words)
    psi = float(np.clip((action_score - drag_score) * 0.6, -1.9, 1.9))
    
    # 2. Boundary Topology: Inclusive (+upsilon) vs Exclusive (-upsilon)
    inc_words = ["benefits", "economic", "best practice", "domestic", "community", "national", "our", "families", "public", "workers", "australians", "together"]
    exc_words = ["foreign", "tension", "restriction", "chineseowned", "visas", "threat", "privatize", "monopoly", "border", "exclude", "cartel", "alien"]
    inc_score = sum(w in text_lower for w in inc_words)
    exc_score = sum(w in text_lower for w in exc_words)
    upsilon = float(np.clip((inc_score - exc_score) * 0.6, -1.9, 1.9))
    
    # 3. Causal Depth: Cause (-z) vs Effect (+z)
    cause_words = ["why", "explanation", "reassessment", "training", "needs", "because", "root", "foundation", "origin", "basis", "source"]
    effect_words = ["produces", "consequences", "dying", "benefits", "planes in the air", "spread", "yield", "outcome", "result", "toll", "impact"]
    cause_score = sum(w in text_lower for w in cause_words)
    effect_score = sum(w in text_lower for w in effect_words)
    z = float(np.clip((effect_score - cause_score) * 0.5, -1.8, 1.8))
    
    # 4. Canonical Seven Planes Simplex Allocation:
    # Q1: Metaphysical Identity (WHO — Will & Direction / Leadership)
    # Q2: Possible (WHAT — Faith & Probability / Potential)
    # Q3: Physical (WHERE — Matter & Distance / Transport / Geography)
    # Q4: Lyrical (WHY — Meaning & Resonance / Telos / Ethics)
    # Q5: Logical (HOW — Count & Consistency / Economics / Procedures)
    # Q6: Historical (CAUSE — Sequence & Causality / Precedents)
    # Q7: Emotive (EFFECT — Passion & Consequence / Community Grief)
    q = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], dtype=np.float64)
    
    # Q1: Metaphysical (Who)
    if any(w in text_lower for w in ["government", "labor", "albanese", "minister", "prime minister", "leader", "we", "parliament", "authority", "opposition"]):
        q[0] += 0.7
    # Q2: Possible (What)
    if any(w in text_lower for w in ["could", "possible", "potential", "opportunity", "shortage", "future", "needs", "may", "option"]):
        q[1] += 0.6
    # Q3: Physical (Where)
    if any(w in text_lower for w in ["planes", "air", "flights", "road", "roads", "crash", "airport", "kempsey", "princes hwy", "infrastructure", "rail"]):
        q[2] += 0.9
    # Q4: Lyrical (Why)
    if any(w in text_lower for w in ["fairness", "justice", "meaning", "purpose", "why", "best practice", "integrity", "values"]):
        q[3] += 0.5
    # Q5: Logical (How)
    if any(w in text_lower for w in ["economic", "economy", "benefits", "dollars", "fund", "funding", "budget", "count", "percent", "tax", "cost"]):
        q[4] += 0.7
    # Q6: Historical (Cause)
    if any(w in text_lower for w in ["history", "precedent", "record", "since", "years", "past", "decade", "sequence", "hansard", "review"]):
        q[5] += 0.6
    # Q7: Emotive (Effect)
    if any(w in text_lower for w in ["dying", "fatal", "tragic", "carnage", "consequences", "families", "grief", "mourn", "fear", "tension", "crisis"]):
        q[6] += 0.8
        
    q = q / np.sum(q)
    return np.array([upsilon, psi, z], dtype=np.float64), q

# ============================================================================
# 3. EXPANDED TOKENIZER & MODEL
# ============================================================================

class ScaledTokenizer:
    def __init__(self, vocab_size=1000):
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

    def encode(self, text, max_len=24):
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        tokens = [self.word2idx.get(w, 1) for w in words[:max_len]]
        if len(tokens) < max_len:
            tokens = tokens + [0] * (max_len - len(tokens))
        return np.array(tokens, dtype=np.int32)

class Adam:
    def __init__(self, params, lr=0.008, beta1=0.9, beta2=0.999, eps=1e-8):
        self.params = params
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.m = [np.zeros_like(p) for p in params]
        self.v = [np.zeros_like(p) for p in params]
        self.t = 0

    def step(self, grads):
        self.t += 1
        for i in range(len(self.params)):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * grads[i]
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * (grads[i] ** 2)
            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            v_hat = self.v[i] / (1 - self.beta2 ** self.t)
            self.params[i] -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)

class ScaledPolytropeTransformer:
    def __init__(self, vocab_size=1000, d_model=64, d_hidden=128, seq_len=24):
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.d_hidden = d_hidden
        self.seq_len = seq_len
        
        np.random.seed(42)
        self.embedding = np.random.randn(vocab_size, d_model) * 0.08
        self.W_q = np.random.randn(d_model, d_model) * 0.08
        self.W_k = np.random.randn(d_model, d_model) * 0.08
        self.W_v = np.random.randn(d_model, d_model) * 0.08
        
        self.W_ff1 = np.random.randn(d_model, d_hidden) * 0.08
        self.b_ff1 = np.zeros(d_hidden)
        self.W_ff2 = np.random.randn(d_hidden, d_model) * 0.08
        self.b_ff2 = np.zeros(d_model)
        
        self.W_geo = np.random.randn(d_model, 3) * 0.08
        self.b_geo = np.zeros(3)
        self.W_qplane = np.random.randn(d_model, 7) * 0.08
        self.b_qplane = np.zeros(7)
        
        self.params = [
            self.embedding,
            self.W_q, self.W_k, self.W_v,
            self.W_ff1, self.b_ff1, self.W_ff2, self.b_ff2,
            self.W_geo, self.b_geo,
            self.W_qplane, self.b_qplane
        ]
        self.optimizer = Adam(self.params, lr=0.008)

    def softmax(self, x, axis=-1):
        e_x = np.exp(x - np.max(x, axis=axis, keepdims=True))
        return e_x / np.sum(e_x, axis=axis, keepdims=True)

    def forward(self, token_ids):
        B, L = token_ids.shape
        self.E = self.embedding[token_ids]
        self.Q = self.E @ self.W_q
        self.K = self.E @ self.W_k
        self.V = self.E @ self.W_v
        
        scale = np.sqrt(self.d_model)
        self.scores = (self.Q @ self.K.transpose(0, 2, 1)) / scale
        self.attn_weights = self.softmax(self.scores, axis=-1)
        self.ctx = self.attn_weights @ self.V
        
        self.post_attn = self.E + self.ctx
        self.H_ff = np.tanh(self.post_attn @ self.W_ff1 + self.b_ff1)
        self.ff_out = self.H_ff @ self.W_ff2 + self.b_ff2
        self.H_out = self.post_attn + self.ff_out
        
        self.pooled = np.mean(self.H_out, axis=1)
        self.pred_coords = 2.0 * np.tanh(self.pooled @ self.W_geo + self.b_geo)
        self.pred_q = self.softmax(self.pooled @ self.W_qplane + self.b_qplane, axis=-1)
        return self.pred_coords, self.pred_q

    def train_step(self, token_ids, target_coords, target_q, lambda_modal=0.5, lambda_plane=0.5):
        B = len(token_ids)
        pred_coords, pred_q = self.forward(token_ids)
        
        loss_coords = np.mean((pred_coords - target_coords) ** 2)
        grad_coords = 2.0 * (pred_coords - target_coords) / B
        
        # Modal Fulcrum Balance Loss
        loss_modal = 0.0
        grad_modal = np.zeros_like(pred_coords)
        if B >= 4:
            can_be = pred_coords[0, :2]
            was_like = pred_coords[1, :2]
            is_not = pred_coords[2, :2]
            is_like = pred_coords[3, :2]
            loss_modal = float(np.sum((can_be + was_like) ** 2) + np.sum((is_not + is_like) ** 2))
            grad_modal[0, :2] += 2.0 * (can_be + was_like)
            grad_modal[1, :2] += 2.0 * (can_be + was_like)
            grad_modal[2, :2] += 2.0 * (is_not + is_like)
            grad_modal[3, :2] += 2.0 * (is_not + is_like)

        loss_q = -np.mean(np.sum(target_q * np.log(pred_q + 1e-12), axis=-1))
        grad_q_logits = (pred_q - target_q) / B
        total_loss = loss_coords + lambda_modal * loss_modal + lambda_plane * loss_q
        
        grad_coords_total = grad_coords + lambda_modal * grad_modal
        dtanh = (1.0 - (pred_coords / 2.0) ** 2) * 2.0
        grad_coords_pre = grad_coords_total * dtanh
        grad_W_geo = self.pooled.T @ grad_coords_pre
        grad_b_geo = np.sum(grad_coords_pre, axis=0)
        grad_W_qplane = self.pooled.T @ grad_q_logits
        grad_b_qplane = np.sum(grad_q_logits, axis=0)
        
        grad_pooled = grad_coords_pre @ self.W_geo.T + grad_q_logits @ self.W_qplane.T
        grad_H_out = np.tile(grad_pooled[:, None, :] / self.seq_len, (1, self.seq_len, 1))
        grad_ff_out = grad_H_out
        grad_post_attn = grad_H_out.copy()
        
        grad_W_ff2 = np.sum(self.H_ff.transpose(0, 2, 1) @ grad_ff_out, axis=0)
        grad_b_ff2 = np.sum(grad_ff_out, axis=(0, 1))
        grad_H_ff = grad_ff_out @ self.W_ff2.T
        grad_pre_ff = grad_H_ff * (1.0 - self.H_ff ** 2)
        grad_W_ff1 = np.sum(self.post_attn.transpose(0, 2, 1) @ grad_pre_ff, axis=0)
        grad_b_ff1 = np.sum(grad_pre_ff, axis=(0, 1))
        grad_post_attn += grad_pre_ff @ self.W_ff1.T
        
        grad_E = grad_post_attn.copy()
        grad_ctx = grad_post_attn
        grad_W_v = np.sum(self.E.transpose(0, 2, 1) @ (self.attn_weights.transpose(0, 2, 1) @ grad_ctx), axis=0)
        grad_V = self.attn_weights.transpose(0, 2, 1) @ grad_ctx
        grad_attn_weights = grad_ctx @ self.V.transpose(0, 2, 1)
        grad_scores = (self.attn_weights * (grad_attn_weights - np.sum(grad_attn_weights * self.attn_weights, axis=-1, keepdims=True))) / np.sqrt(self.d_model)
        grad_Q = grad_scores @ self.K
        grad_K = grad_scores.transpose(0, 2, 1) @ self.Q
        grad_W_q = np.sum(self.E.transpose(0, 2, 1) @ grad_Q, axis=0)
        grad_W_k = np.sum(self.E.transpose(0, 2, 1) @ grad_K, axis=0)
        grad_E += grad_Q @ self.W_q.T + grad_K @ self.W_k.T + grad_V @ self.W_v.T
        
        grad_embedding = np.zeros_like(self.embedding)
        for b in range(B):
            for l in range(self.seq_len):
                tok = token_ids[b, l]
                grad_embedding[tok] += grad_E[b, l]
                
        grads = [
            grad_embedding,
            grad_W_q, grad_W_k, grad_W_v,
            grad_W_ff1, grad_b_ff1, grad_W_ff2, grad_b_ff2,
            grad_W_geo, grad_b_geo,
            grad_W_qplane, grad_b_qplane
        ]
        self.optimizer.step(grads)
        return float(total_loss), float(loss_coords), float(loss_modal), float(loss_q)

    def save_weights(self, filepath):
        np.savez(filepath,
                 embedding=self.embedding,
                 W_q=self.W_q, W_k=self.W_k, W_v=self.W_v,
                 W_ff1=self.W_ff1, b_ff1=self.b_ff1,
                 W_ff2=self.W_ff2, b_ff2=self.b_ff2,
                 W_geo=self.W_geo, b_geo=self.b_geo,
                 W_qplane=self.W_qplane, b_qplane=self.b_qplane)

# ============================================================================
# 4. RUN SCALED EXPERIMENT
# ============================================================================

def execute_scaled_experiment():
    print("=" * 70)
    print("HOURLY R&D EXECUTION: SCALED KERNEL EXPERIMENT (500+ STATEMENTS)")
    print("=" * 70)
    
    raw_corpus = load_all_corpora()
    print(f"Total Ingested Corpus Statements: {len(raw_corpus)}")
    
    texts = [item["text"] for item in raw_corpus]
    annotations = [annotate_statement(t) for t in texts]
    
    tokenizer = ScaledTokenizer(vocab_size=800)
    tokenizer.fit(texts)
    print(f"Active Tokenizer Vocabulary: {len(tokenizer.word2idx)} subwords.")
    
    X_train = np.array([tokenizer.encode(t, max_len=24) for t in texts])
    y_coords = np.array([ann[0] for ann in annotations])
    y_q = np.array([ann[1] for ann in annotations])
    
    model = ScaledPolytropeTransformer(vocab_size=len(tokenizer.word2idx) + 10,
                                      d_model=64, d_hidden=128, seq_len=24)
    
    epochs = 40
    batch_size = 32
    n_batches = len(X_train) // batch_size
    print(f"Executing Training Run: {epochs} epochs | {n_batches} batches/epoch (Batch Size: {batch_size})")
    
    t0 = time.time()
    initial_loss = None
    final_loss = None
    
    for epoch in range(1, epochs + 1):
        indices = np.random.permutation(len(X_train))
        epoch_loss = 0.0
        
        for b in range(n_batches):
            b_idx = indices[b * batch_size : (b + 1) * batch_size]
            b_X = X_train[b_idx]
            b_coords = y_coords[b_idx]
            b_q = y_q[b_idx]
            
            loss, lc, lm, lq = model.train_step(b_X, b_coords, b_q)
            epoch_loss += loss
            
        avg_loss = epoch_loss / max(n_batches, 1)
        if epoch == 1:
            initial_loss = avg_loss
        if epoch % 10 == 0:
            print(f"  Epoch {epoch:2d}/{epochs} | Loss: {avg_loss:.5f} (Coords MSE: {lc:.4f}, Modal: {lm:.4f}, Q-Plane: {lq:.4f})")
        final_loss = avg_loss
        
    duration = time.time() - t0
    loss_delta = ((initial_loss - final_loss) / initial_loss) * 100.0
    print(f"\nOptimization Finished in {duration:.2f}s | Loss: {initial_loss:.4f} -> {final_loss:.4f} (-{loss_delta:.2f}%)")
    
    # Save model weights checkpoint
    weights_path = "/working_dir/c_424c86baff31945d/artifacts/file_generation/ttl=63d/output/polytrope_weights.npz"
    model.save_weights(weights_path)
    print(f"Checkpoint saved to: {weights_path}")
    
    # Export representative embeddings to JSON
    benchmark_queries = [
        "The national government will deliver economic growth and support working families",
        "Aviation pilot shortage poses a severe challenge to domestic flight schedules",
        "Fatal road crashes on the highway have devastated local communities",
        "We must hold ministers accountable for their parliamentary records"
    ]
    
    plane_names = ["Q1:Metaphysical (Who)", "Q2:Possible (What)", "Q3:Physical (Where)", "Q4:Lyrical (Why)", "Q5:Logical (How)", "Q6:Historical (Cause)", "Q7:Emotive (Effect)"]
    
    exported_results = []
    print("\nBenchmark Inference Evaluation on Canonical Planes:")
    print("-" * 70)
    for q in benchmark_queries:
        toks = tokenizer.encode(q, max_len=24)[None, :]
        p_coords, p_q = model.forward(toks)
        
        coords = p_coords[0]
        q_dist = p_q[0]
        top_plane = plane_names[np.argmax(q_dist)]
        
        u, p, z = coords
        if u >= 0 and p >= 0:
            modal = "PRODUCTIVE [can be] (+υ, +ψ)"
        elif u < 0 and p >= 0:
            modal = "REDUCTIVE [is not] (-υ, +ψ)"
        elif u < 0 and p < 0:
            modal = "REGRESSIVE [was like] (-υ, -ψ)"
        else:
            modal = "CONSTRUCTIVE [is like] (+υ, -ψ)"
            
        print(f"Query: \"{q[:60]}...\"")
        print(f"  Coordinates: υ={u:+.3f}, ψ={p:+.3f}, z={z:+.3f} -> {modal}")
        print(f"  Dominant Substrate: {top_plane} ({np.max(q_dist)*100:.1f}%)")
        
        exported_results.append({
            "statement": q,
            "latent_vector_64d": model.pooled[0].tolist(),
            "coords_3d": {
                "upsilon": float(u),
                "psi": float(p),
                "z": float(z)
            },
            "substrate_q_planes_7d": {plane_names[i]: float(q_dist[i]) for i in range(7)},
            "modal_quadrant": modal
        })
        
    out_json = "/working_dir/c_424c86baff31945d/artifacts/file_generation/ttl=63d/output/sentence_embeddings.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(exported_results, f, indent=2)
    print(f"\nExported updated embeddings JSON: {out_json}")

if __name__ == "__main__":
    execute_scaled_experiment()
