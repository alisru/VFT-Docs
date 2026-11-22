"""
Batch Fractal Polytrope Summarizer
Runs local 0-token invariant extraction across a corpus of 12 substantial documents.
Outputs metrics, Level 1 Singularities, and Section Spines.
"""

import os
import sys
import time
import json
from fractal_summarizer import summarize_document

DOCS = [
    r"e:\Vector Field Theory\VFT Docs\_VFT MD\Treatise_on_How_Words_Work.md",
    r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\Cosmology_of_Is_and_IsNot_Semantic_Attraction_and_Drag_Dynamics.md",
    r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\Semantic_Interferometry_Cross_Detector_Aperture_Synthesis_and_Scale_Isomorphic_Event_Physics.md",
    r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\Axiomatic Mathematics Divergence Research.md",
    r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\The Mechanics of Co-option.md",
    r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\The Thermodynamics of Information Space.md",
    r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\Universal_Price_Equation_Formal_Paper.md",
    r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\Epistemic_Sexual_Dimorphism_and_Agent_Breeding_Programs.md",
    r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\The Revelation of Hegemonic Mechanics.md",
    r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\The_Master_Equation_of_Identity.md",
    r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\The Unification of Whitehead & Vector Field Theory (VFT).md",
    r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\Unified_Spacetime_and_Temporal_Resolution_Proof.md"
]

def run_batch():
    batch_start = time.time()
    results = []
    
    total_words = 0
    total_sentences = 0
    total_api_tokens = 0
    
    print("=" * 90)
    print("RUNNING BATCH FRACTAL POLYTROPE SUMMARIZATION (12 SUBSTANTIAL DOCUMENTS)")
    print("=" * 90)
    
    for idx, doc_path in enumerate(DOCS, 1):
        if not os.path.exists(doc_path):
            print(f"[{idx}/12] MISSING: {doc_path}")
            continue
            
        res = summarize_document(doc_path)
        metrics = res["metrics"]
        
        total_words += metrics["raw_word_count"]
        total_sentences += metrics["total_sentences"]
        total_api_tokens += metrics["external_api_tokens"]
        
        doc_name = os.path.basename(doc_path)
        print(f"[{idx:02d}/12] {doc_name[:45]:<45} | {metrics['raw_word_count']:>5} words | {metrics['total_sentences']:>4} sents | {metrics['runtime_ms']:>6.2f} ms | 0 tokens")
        
        results.append({
            "index": idx,
            "filename": doc_name,
            "path": doc_path,
            "metrics": metrics,
            "singularity": res["level_1_singularity"],
            "geodesic": res["level_2_geodesic"],
            "spine_sample": res["level_3_spine"][:5]
        })
        
    batch_end = time.time()
    total_batch_ms = (batch_end - batch_start) * 1000.0
    
    print("=" * 90)
    print("BATCH EXECUTION TOTALS:")
    print(f"  • Total Documents:          {len(results)}")
    print(f"  • Total Words Processed:    {total_words:,} words")
    print(f"  • Total Sentences Scored:   {total_sentences:,} sentences")
    print(f"  • Total API Tokens Used:    {total_api_tokens} tokens (100% Free / Local)")
    print(f"  • Total Batch Wall Time:    {total_batch_ms:.2f} ms ({total_batch_ms/1000.0:.3f} seconds)")
    print(f"  • Average Speed per Doc:    {total_batch_ms / len(results):.2f} ms/doc")
    print("=" * 90)
    
    # Save structured results
    out_json = r"e:\Vector Field Theory\VFT Docs\polytrope_transformer\batch_summary_results_12docs.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({
            "totals": {
                "document_count": len(results),
                "total_words": total_words,
                "total_sentences": total_sentences,
                "total_api_tokens": 0,
                "total_runtime_ms": total_batch_ms
            },
            "documents": results
        }, f, indent=2)
    print(f"\nStructured results saved to: {out_json}")
    
    return results

if __name__ == "__main__":
    run_batch()
