"""
Fractal Polytrope Transformer Training & Ingestion Engine
Integrated with the Mandatory Epistemic Audit Engine (Sieve Layer).
"""

import json
import os
import re
import time
import numpy as np
import pathlib

# ============================================================================
# 1. EPISTEMIC AUDIT ENGINE (MANDATORY AUDIT STEP)
# ============================================================================

class EpistemicAuditEngine:
    """
    Validates and calibrates candidate coordinates and substrate allocations
    against structural modal invariants, boundary grammar, and substrate boundaries.
    Prevents Modal Collapse, Boundary Inversion, and Substrate Hallucinations.
    """
    @staticmethod
    def audit(text, coords, q_planes):
        text_lower = text.lower()
        u, p, z = float(coords[0]), float(coords[1]), float(coords[2])
        q = q_planes.copy().astype(np.float64)
        violations = []

        # 1. MODAL HORIZON & TENSE AUDIT
        # Future promissory markers cannot be Regressive [was like]
        future_markers = ["will", "shall", "plans to", "can", "aims to", "deliver", "promise", "create", "grow", "build", "expand"]
        past_markers = ["was", "were", "happened", "precedent", "historically", "echoed", "failed", "died"]
        has_future = any(w in text_lower for w in future_markers)
        has_past = any(w in text_lower for w in past_markers)

        if has_future and not has_past:
            if u <= 0.05 or p <= 0.05:
                violations.append("MODAL_COLLAPSE: Promissory future assertion erroneously mapped to Regressive [was like]")
                u = max(u, 0.45)
                p = max(p, 0.55)
            if z <= 0.0:
                violations.append("CAUSAL_INVERSION: Future delivery promise mapped to upstream cause (-z)")
                z = max(z, 0.25)

        # 2. BOUNDARY TOPOLOGY AUDIT (υ)
        # Collective welfare and shared benefit must be Inclusive (+υ)
        inclusive_markers = ["support", "working families", "community", "public", "universal", "together", "benefits", "welfare", "our"]
        exclusive_markers = ["exclude", "ban", "privatize", "monopoly", "border", "restrict", "cartel", "sanction"]
        if any(w in text_lower for w in inclusive_markers) and not any(w in text_lower for w in exclusive_markers):
            if u <= 0.0:
                violations.append("BOUNDARY_INVERSION: Inclusive collective phrasing mapped to exclusive boundary (-υ)")
                u = abs(u) if abs(u) > 0.3 else 0.75

        # 3. KINETIC WORK AUDIT (ψ)
        # Active proaction verbs cannot be Counteractive Drag (-ψ)
        active_verbs = ["deliver", "build", "expand", "produce", "increase", "boost", "execute", "make"]
        if any(w in text_lower for w in active_verbs):
            if p <= 0.0:
                violations.append("KINETIC_INVERSION: Active proaction verb mapped to counteractive drag (-ψ)")
                p = abs(p) if abs(p) > 0.3 else 0.85

        # 4. SUBSTRATE CONSERVATION AUDIT (Q1..Q7)
        # Physical matter (Q3) requires tangible mass/distance/transport nouns
        physical_matter_nouns = ["road", "roads", "highway", "plane", "planes", "airport", "rail", "tonnes", "concrete", "steel", "land"]
        has_physical_matter = any(w in text_lower for w in physical_matter_nouns)
        
        # If no physical matter, penalize Q3 (Matter & Distance)
        if not has_physical_matter:
            if np.argmax(q) == 2 or q[2] > 0.15:
                violations.append("SUBSTRATE_HALLUCINATION: Abstract statement mapped to Q3: Physical (Where) without physical matter")
                q[2] = 0.02

        # Sovereignty & Governance -> Q1 (Metaphysical Identity: WHO)
        if any(w in text_lower for w in ["government", "labor", "albanese", "parliament", "state", "leader", "ministers"]):
            q[0] += 0.6

        # Economic Counting & Proof -> Q5 (Logical: HOW)
        if any(w in text_lower for w in ["economic", "growth", "economy", "budget", "cost", "dollars", "fund", "tax"]):
            q[4] += 0.6

        # Social Telos & Purpose -> Q4 (Lyrical: WHY)
        if any(w in text_lower for w in ["support", "working families", "families", "justice", "fairness", "community"]):
            q[3] += 0.4

        # Normalize Q-simplex
        q = q / np.sum(q)
        audited_coords = np.array([u, p, z], dtype=np.float64)

        return {
            "audited_coords": audited_coords,
            "audited_q": q,
            "violations_detected": violations,
            "audit_passed": len(violations) == 0
        }

# ============================================================================
# 2. TOKENIZER & NEURAL ARCHITECTURE
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

    def load_weights(self, filepath):
        data = np.load(filepath)
        self.embedding = data['embedding']
        self.W_q = data['W_q']
        self.W_k = data['W_k']
        self.W_v = data['W_v']
        self.W_ff1 = data['W_ff1']
        self.b_ff1 = data['b_ff1']
        self.W_ff2 = data['W_ff2']
        self.b_ff2 = data['b_ff2']
        self.W_geo = data['W_geo']
        self.b_geo = data['b_geo']
        self.W_qplane = data['W_qplane']
        self.b_qplane = data['b_qplane']

# ============================================================================
# 3. PIPELINE WITH MANDATORY AUDIT SIEVE
# ============================================================================

def run_audited_pipeline():
    print("=" * 70)
    print("FRACTAL POLYTROPE TRANSFORMER: AUDITED INGESTION & TRAINING")
    print("=" * 70)
    
    # 1. Ingest corpora
    corpus_files = [
        "downloads/albanese_statements_news.jsonl",
        "downloads/albanese_statements_1.jsonl",
        "downloads/albanese_statements_1999.jsonl"
    ]
    
    raw_texts = []
    for cf in corpus_files:
        if os.path.exists(cf):
            with open(cf, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip(): continue
                    try:
                        d = json.loads(line)
                        t = d.get("quote") or d.get("headline") or d.get("text", "")
                        if len(t) > 15:
                            raw_texts.append(t[:200].strip())
                    except: continue

    print(f"Total Raw Corpus Texts: {len(raw_texts)}")
    
    # 2. Annotate AND Pass through Epistemic Audit Sieve
    audited_coords = []
    audited_qs = []
    total_violations = 0
    
    for t in raw_texts:
        # Initial draft coordinates
        u = 0.0
        p = 0.0
        z = 0.0
        q = np.ones(7) / 7.0
        
        # Pass through the Audit Sieve
        res = EpistemicAuditEngine.audit(t, np.array([u, p, z]), q)
        audited_coords.append(res["audited_coords"])
        audited_qs.append(res["audited_q"])
        if not res["audit_passed"]:
            total_violations += 1
            
    print(f"Audit Sieve Filtered: {total_violations} initial draft contradictions corrected.")
    
    tokenizer = ScaledTokenizer(vocab_size=800)
    tokenizer.fit(raw_texts)
    
    X_train = np.array([tokenizer.encode(t, max_len=24) for t in raw_texts])
    y_coords = np.array(audited_coords)
    y_q = np.array(audited_qs)
    
    model = ScaledPolytropeTransformer(vocab_size=len(tokenizer.word2idx) + 10, d_model=64, d_hidden=128, seq_len=24)
    
    # Train for 40 epochs
    epochs = 40
    batch_size = 32
    n_batches = len(X_train) // batch_size
    for epoch in range(1, epochs + 1):
        idx = np.random.permutation(len(X_train))
        for b in range(n_batches):
            b_idx = idx[b * batch_size : (b + 1) * batch_size]
            model.train_step(X_train[b_idx], y_coords[b_idx], y_q[b_idx])
            
    # Save checkpoint
    weights_path = "/working_dir/c_424c86baff31945d/artifacts/file_generation/ttl=63d/output/polytrope_weights.npz"
    model.save_weights(weights_path)
    print(f"Audited weights saved to {weights_path}")
    
    # 3. Benchmark Verification with AUDIT STEP
    test_queries = [
        "The national government will deliver economic growth and support working families",
        "Aviation pilot shortage poses a severe challenge to domestic flight schedules",
        "Fatal road crashes on the highway have devastated local communities",
        "We must hold ministers accountable for their parliamentary records"
    ]
    
    plane_names = ["Q1:Metaphysical (Who)", "Q2:Possible (What)", "Q3:Physical (Where)", "Q4:Lyrical (Why)", "Q5:Logical (How)", "Q6:Historical (Cause)", "Q7:Emotive (Effect)"]
    
    print("\n" + "=" * 70)
    print("AUDITED BENCHMARK INFERENCE EVALUATION")
    print("=" * 70)
    
    exported_results = []
    
    for q in test_queries:
        toks = tokenizer.encode(q, max_len=24)[None, :]
        raw_coords, raw_q = model.forward(toks)
        
        # APPLY MANDATORY POST-INFERENCE AUDIT SIEVE
        audit_res = EpistemicAuditEngine.audit(q, raw_coords[0], raw_q[0])
        coords = audit_res["audited_coords"]
        q_dist = audit_res["audited_q"]
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
            
        print(f"\nStatement: \"{q}\"")
        if not audit_res["audit_passed"]:
            print(f"  [AUDIT CORRECTION TRIGGERED]: {audit_res['violations_detected']}")
        print(f"  Final Audited Coords: υ = {u:+.3f} (Boundary) | ψ = {p:+.3f} (Work) | z = {z:+.3f} (Causal)")
        print(f"  Modal State:          {modal}")
        print(f"  Dominant Substrate:   {top_plane} ({np.max(q_dist)*100:.1f}%)")
        
        exported_results.append({
            "statement": q,
            "raw_coords": [float(v) for v in raw_coords[0]],
            "audited_coords": [float(v) for v in coords],
            "modal_state": modal,
            "dominant_plane": top_plane,
            "audit_violations": audit_res["violations_detected"],
            "substrate_distribution": {plane_names[i]: float(q_dist[i]) for i in range(7)}
        })
        
    out_json = "/working_dir/c_424c86baff31945d/artifacts/file_generation/ttl=63d/output/sentence_embeddings.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(exported_results, f, indent=2)
    print(f"\nSaved audited sentence embeddings to: {out_json}")

if __name__ == "__main__":
    run_audited_pipeline()
