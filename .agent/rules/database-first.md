# USE THE TOOLS WE BUILT (Database-First Semantic Operations)

This rule prevents AI agents from executing redundant or overengineered semantic operations (such as running local vector embeddings, imports of `sentence_transformers`, or starting unnecessary local inference) when pre-computed database assets already exist.

## Rule Constraints

1. **Prioritize Existing Databases**:
   - Always query the pre-computed databases (`cluster_mapping.json`, `topic_ism_mapping.json`) or Qdrant Cloud collections (`vft_paragraphs`, `vft_rcp_lexicon`) first.
   - For any document already inside the repository (e.g., in `_VFT MD`), all semantic mappings, topic IDs, and coordinate alignments have already been computed. Retrieve them directly; do **not** re-calculate them.

2. **No Redundant Inference**:
   - Never import `sentence_transformers` or download any neural network models locally unless the user explicitly requests vectorizing a brand-new, unindexed external document.
   - If a new document needs to be analyzed, prefer lightweight string/regex matching against the keywords listed in `topic_ism_mapping.json` to assign topics, rather than running local embeddings.

3. **Check the Workspace Context First**:
   - Before executing any semantic task (e.g., coherence, centrality, or trajectory mapping), verify if the document or topic is already present in the local database. If it is, use it.
