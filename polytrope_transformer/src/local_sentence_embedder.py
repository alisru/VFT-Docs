"""
Local Sentence Embedder (ONNX Runtime + Tokenizers)
Zero-token, 100% offline, CPU-safe dense semantic embedding engine using all-MiniLM-L6-v2.
"""

import os
import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer
from typing import List

MODEL_DIR = r"C:\Users\hungh\.cache\memories\models\Xenova\all-MiniLM-L6-v2"
TOKENIZER_PATH = os.path.join(MODEL_DIR, "tokenizer.json")
ONNX_PATH = os.path.join(MODEL_DIR, "onnx", "model_quantized.onnx")

class LocalSentenceEmbedder:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LocalSentenceEmbedder, cls).__new__(cls)
            cls._instance._init_session()
        return cls._instance

    def _init_session(self):
        if not os.path.exists(TOKENIZER_PATH) or not os.path.exists(ONNX_PATH):
            raise FileNotFoundError(f"Local ONNX model files missing in: {MODEL_DIR}")
            
        self.tokenizer = Tokenizer.from_file(TOKENIZER_PATH)
        self.tokenizer.enable_truncation(max_length=256)
        
        # CPU Session options for high-throughput single-node inference
        opts = ort.SessionOptions()
        opts.intra_op_num_threads = 4
        opts.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
        opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        
        self.session = ort.InferenceSession(ONNX_PATH, sess_options=opts, providers=["CPUExecutionProvider"])

    def embed(self, sentences: List[str], batch_size: int = 32) -> np.ndarray:
        """Embeds a list of sentences into [N, 384] normalized semantic embeddings."""
        if not sentences:
            return np.empty((0, 384), dtype=np.float32)

        all_embs = []
        for i in range(0, len(sentences), batch_size):
            batch = sentences[i:i + batch_size]
            encodings = self.tokenizer.encode_batch(batch)
            
            # Pad batch to max length in this batch
            max_len = max(len(enc.ids) for enc in encodings)
            input_ids = []
            attention_mask = []
            
            for enc in encodings:
                ids = enc.ids + [0] * (max_len - len(enc.ids))
                mask = enc.attention_mask + [0] * (max_len - len(enc.attention_mask))
                input_ids.append(ids)
                attention_mask.append(mask)
                
            input_ids_np = np.array(input_ids, dtype=np.int64)
            attn_mask_np = np.array(attention_mask, dtype=np.int64)
            token_type_np = np.zeros_like(input_ids_np)
            
            out = self.session.run(
                None,
                {
                    "input_ids": input_ids_np,
                    "attention_mask": attn_mask_np,
                    "token_type_ids": token_type_np
                }
            )
            
            # Mean pooling with attention mask
            token_embs = out[0] # [B, seq_len, 384]
            mask_expanded = np.expand_dims(attn_mask_np, -1)
            sum_embs = np.sum(token_embs * mask_expanded, axis=1)
            sum_mask = np.clip(mask_expanded.sum(axis=1), a_min=1e-9, a_max=None)
            mean_pooled = sum_embs / sum_mask # [B, 384]
            
            # L2 normalize
            norms = np.linalg.norm(mean_pooled, axis=1, keepdims=True)
            normalized = mean_pooled / np.clip(norms, a_min=1e-9, a_max=None)
            all_embs.append(normalized)
            
        return np.vstack(all_embs)
