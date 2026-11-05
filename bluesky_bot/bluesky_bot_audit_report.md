# Comprehensive Codebase & Prompt Audit Report: `bluesky_bot`

**Target Components Audited:**
1. `bluesky_bot/harvest_candidates.py`
2. `bluesky_bot/google_ai_studio_one_shot.py`
3. `bluesky_bot/aletheia_bot.py`
4. `bluesky_bot/rebuild_registries.py` & `bluesky_bot/rebuild_registries_son.py`
5. `bluesky_bot/image_card_generator.py` & `bluesky_bot/generate_graph.py`
6. `bluesky_bot/instructions/` (`operational_pipelines.md`, `thread_formatting*.md`, `subagent_spawning*.md`)

---

## 1. Executive Summary & Critical Architectural Vulnerabilities

The `bluesky_bot` pipeline is an operational, multi-stage fact-checking and social-physics evaluation system designed to monitor news, extract ethical vectors, calculate 6-attractor $(u, \psi)$ coordinates, render visual evidence cards, and publish threaded evaluations to Bluesky via AT Protocol.

While the system contains advanced mathematical structures (e.g., attractor force calculus in `rebuild_registries_son.py` and procedural field generation in `generate_graph.py`), the codebase suffers from **three critical architectural vulnerabilities**:

1. **Payload Duplication & Uncontrolled Token Bloat**:
   - The Stage 1 Search Grounding dossier (`extra_context`) is injected **twice** into every LLM request: once in `system_instruction` (line 1261) and once in `user_payload` (line 1776).
   - Raw scraped article bodies are passed un-truncated (often 10,000–50,000 characters per candidate). In multi-source clusters, up to 3 full article bodies are concatenated into `primary_c["cross_source_dossier"]` and sent directly to the model. A 5-story batch easily consumes 80,000–120,000 input tokens where 10,000 tokens would suffice.

2. **Decoupled Trajectory Math vs. Hallucinated Output**:
   - `generate_graph.py` contains the exact deterministic trajectory function `get_path_name(claim_u, claim_psi, real_u, real_psi)`. However, **this function is never called to validate or overwrite LLM post generation** in `google_ai_studio_one_shot.py` or `aletheia_bot.py`.
   - The LLM hallucinates path names freely in `posts[3]` (The Verdict) and `posts[8]` (The Trajectory). There is zero programmatic enforcement preventing the model from labeling a $(+, +) \to (-, -)$ fall as "The Path of Redemption".

3. **Coordinate & Card Synchronization Drift**:
   - When `rebuild_registries_son.py` recalculates coordinates from attractor forces, it mutates `posts[1]` (Claim) and `posts[2]` (Reality), but **fails to update `posts[3]` (The Verdict line) or `posts[8]` (The Trajectory post)**.
   - When `use_multi_aspect` is enabled, a new Sub-Audits Breakdown post is inserted at index 4. `image_card_generator.py` adapts to this, but `aletheia_bot.py` (lines 546–557) uses **hardcoded post indices (`posts[4]`, `posts[5]`, etc.) for generating card alt-text**, shifting all descriptions by 1 and omitting Spirithekanon entirely.

---

## 2. Prompt Engineering & Token Efficiency (Over-sending vs Under-feeding)

### A. Over-Sending (Token Waste & Redundancy)

1. **Double-Dossier Grounding Injection**:
   - **Location**: `google_ai_studio_one_shot.py` (lines 1742–1746, 1261, 1776).
   - **Mechanism**: When `pre_grounded_dossier` or `harvest_search_grounding` returns context, it is stored in `extra_context`. Then:
     - Line 1749 passes `extra_context` to `build_system_instruction()`, which appends:
       `"CRITICAL: You must actively incorporate the following background knowledge..."`
     - Line 1776 then explicitly appends:
       `user_payload.append(f"=== ADDITIONAL CONTEXT / BACKGROUND TO CONSIDER ===\n{extra_context}\n\n")`
   - **Impact**: 100% redundant token consumption on every grounded evaluation call. For a 5-story batch with Tavily/Exa snippets, this wastes 2,000–5,000 tokens per call.

2. **Un-truncated Full Article Scraping in Candidate Payload**:
   - **Location**: `harvest_candidates.py` (lines 1502–1517), `google_ai_studio_one_shot.py` (lines 1755–1769).
   - **Mechanism**: `c["text"]` stores the entire scraped body (`article_text_clean = body.strip()`). When clustered, `dossier_lines` appends full texts of up to 3 sources.
   - **Impact**: Factcheck and social physics evaluation only requires the headline, subheader, key factual claims, and primary quotes (~1,500–2,500 characters). Passing 15k–40k characters per article causes severe input token bloat and increases API latency/timeouts.

3. **Redundant Instruction Injection**:
   - **Location**: `google_ai_studio_one_shot.py` (lines 1770–1781) and `_load_rules()`.
   - **Mechanism**: Both `convergence_rules` (from `.agent/tools/convergence-test/convergence_son_potential.md` - 24KB) and `formatting_rules` (from `instructions/thread_formatting_potential.md` - 17KB) are loaded, minified, and inserted into the user prompt. Simultaneously, `build_system_instruction()` defines `core_concept_directive`, `SOCIAL_PHYSICS_DIRECTIVE`, role definitions, and character limits.
   - **Impact**: Character limit rules (<260 / <275 chars), persona instructions, and coordinate constraints are repeated 3–4 times within the prompt context.

### B. Under-Feeding (Missing Critical Metadata)

1. **Complete Absence of Publication Dates on Bluesky Candidates**:
   - **Location**: `harvest_candidates.py` (lines 1277–1296, 1377–1385, 1429–1436).
   - **Mechanism**: `pub_date` is extracted and normalized **only for RSS candidates** (lines 1176–1222). For Bluesky posts (which constitute the majority of harvested stories: `TARGET_BSKY = 40`), `item.post.record.created_at` or `item.post.indexed_at` is never extracted.
   - **Impact**: When candidates are formatted in `google_ai_studio_one_shot.py`, Bluesky candidates have no `pub_date`. The model is stripped of temporal context, causing historical events, retrospective coverage, or multi-day developments to be evaluated as if they occurred today.

2. **Unstructured Aspect & Source Metadata in Multi-Source Clusters**:
   - **Location**: `harvest_candidates.py` (lines 373–392), `google_ai_studio_one_shot.py` (lines 1755–1768).
   - **Mechanism**: When multiple sources cover a story, publisher names, URLs, and editorial bias tags are serialized into an unstructured plain-text string `cross_source_dossier` inside `c["text"]`.
   - **Impact**: The model is asked to output structured aspect arrays (item[27]), but is fed unstructured markdown blocks instead of clean structured candidate keys:
     ```json
     "sources": [{"publisher": "...", "bias": "...", "url": "..."}]
     ```
     This forces the model to expend reasoning tokens extracting metadata that was already structured in Python.

---

## 3. Objectivity & Biased Results Vulnerabilities

1. **Asymmetrical Source Scraping & Feed Ingestion Bias**:
   - **Location**: `harvest_candidates.py` (lines 1317–1321).
   - **Mechanism**: The candidate harvest relies on three hardcoded Bluesky news feeds:
     - `nickevershed.bsky.social/feed/aaaluca6lksmc` (Data journalism / Australian mainstream)
     - `aendra.com/feed/verified-news` (Bluesky verified news list)
     - `aendra.com/feed/news-2-0`
   - **Bias Vector**: These feeds reflect the demographics of Bluesky (predominantly progressive, center-left, and Western institutional media). Conservative, non-Western, or independent perspectives are rarely surfaced on these feeds.
   - **Flawed Mitigation**: `search_counter_sources_tavily()` attempts active counter-search, but **only triggers if `len(distinct_sources) < 2`**. If a cluster already has two center-left outlets (e.g. *The Guardian* + *ABC Australia*), active counter-search is bypassed entirely, locking the audit into a single ideological framing.

2. **Framing Conflation: Political Punditry vs. Physical Actuality**:
   - **Vulnerability**: Political reporting often frames news around speeches, rhetorical attacks, or legislative positioning.
   - **Mechanism**: When an article covers "Politician X attacks Politician Y over Policy Z", the stated claim is frequently evaluated as the politician's moral intent, while the "reality" is scored based on whether Politician X is being hypocritical. The actual physical event (e.g., whether Policy Z actually built infrastructure, cut emissions, or harmed patients) is displaced by meta-political discourse.
   - **Evidence**: `post_correction.py` demonstrates this failure mode in production: the bot audited a cable news debate regarding Donald Trump and a Cornell rape case, evaluating talking-head claims rather than the actual federal lawsuit and Title IX institutional failures.

3. **Deterministic Trajectory Invariant Compliance**:
   - **Rule**:
     - $\text{GG} \to \text{GE}$ ($(+,+) \to (-,-)$) $\equiv$ `Fall into Destruction`
     - $\text{GG} \to \text{LE}$ ($(+,+) \to (-,+)$) $\equiv$ `Fall into Deception`
     - $\text{GE} \to \text{LG}$ ($(-,-) \to (+,-)$) $\equiv$ `Reckoning into Redemption`
     - $\text{LE} \to \text{GG}$ ($(-,+) \to (+,+)$) $\equiv$ `Revelation into Grace`
     - **Prohibition**: NEVER allow "The Path of Redemption" or "via Constructive" on any vector crossing into $-u$.
   - **Vulnerability**: `thread_formatting_son.md` **omits the Deterministic Trajectory Invariant entirely** (it was only added to `thread_formatting_potential.md`). More critically, there is **zero programmatic verification** in `transpose_flat_to_json()` or `rebuild_registries_son.py`. If Gemini outputs `The Path of Redemption` for a downward trajectory, the system accepts and publishes it without error.

---

## 4. Code Bugs & Error Invariants

1. **Image Card Alt-Text Index Desynchronization (`aletheia_bot.py`)**:
   - **Location**: `aletheia_bot.py` (lines 546–557).
   - **Bug**:
     ```python
     alt_parts = [
         "System Analysis Details:",
         f"Context: {posts[4]...}",
         f"Nuance: {posts[5]...}",
         f"Breakdown: {posts[6]...}",
         f"Social Physics: {posts[7]...}",
         f"Trajectory: {posts[8]...}",
         f"The Unavoidables: {posts[9]...}",
         f"Alethekanon: {posts[10]...}",
         f"Awwthekanon: {posts[11]...}",
         f"Brothekanon: {posts[12]...}"
     ]
     ```
   - When `use_multi_aspect=True`, `posts[4]` contains the Sub-Audits Breakdown. All subsequent indices shift by +1 (`Context` is at `posts[5]`, `Nuance` is at `posts[6]`, etc.).
   - **Consequence**: The generated accessibility alt-text on Bluesky cards displays mismatched labels (e.g., Context shows sub-audits, Nuance shows context, Brothekanon shows Awwthekanon), and `Spirithekanon` (post 14) is never included in the alt-text.

2. **Cascading Post Pollution in `pack_posts()`**:
   - **Location**: `aletheia_bot.py` (lines 107–130).
   - **Bug**:
     ```python
     for p in posts:
         current = (carry_over + " " + p).strip() if carry_over else p.strip()
         carry_over = ""
         if len(current) <= max_len:
             final_posts.append(current)
         else:
             chunks = split_text(current, max_len)
             final_posts.extend(chunks[:-1])
             carry_over = chunks[-1]
     ```
   - If an earlier post (such as Post 0: Hook or Post 1: Claim) slightly exceeds 300 characters, `split_text()` splits it and assigns the trailing fragment to `carry_over`.
   - On the next loop iteration, that fragment is prepended to the *next logical step*.
   - **Consequence**: The Hook text bleeds into the Claim, the Claim bleeds into Reality, and the structural integrity of the 13-post schema breaks down.

3. **Silent URL Dropping in Single-Post Mode**:
   - **Location**: `aletheia_bot.py` (lines 400–408).
   - **Bug**: If `len(final_posts[0]) + len(ref_suffix) > limit` (300 chars), the reference link is silently omitted from the published post.

4. **Missing Network Timeout in Gemini SDK**:
   - **Location**: `google_ai_studio_one_shot.py` (lines 114, 1946–1950).
   - **Bug**: While `GEMINI_TIMEOUT_SECS = 90` is defined in line 114, `genai_client.models.generate_content(...)` does not pass a timeout to the SDK client or call config.
   - **Consequence**: If Google AI Studio encounters API gateway stalls or throttles during batch processing, the Python process hangs indefinitely instead of triggering the fallback models.

5. **Lack of Automated Correction & Retraction Architecture**:
   - **Location**: `bluesky_bot/post_correction.py`, `post_seyfried_correction.py`.
   - **Deficiency**: Corrections are implemented via hardcoded, one-off scripts. There is no generalized command (`python aletheia_bot.py --retract <story_id> --reason <text>`) to:
     - Post a linked reply with an Errata badge to the original root thread.
     - Update the story status to `RETRACTED` or `AMENDED` in `stories/` and `stories_registry.js`.
     - Recalculate historical actor and outlet hypocrisy ratings to reverse unfair penalties.

---

## 5. Actionable Remediation Roadmap

### Priority 1: Critical Code & Invariant Fixes (Immediate)

1. **Enforce Deterministic Trajectories in Code**:
   - Import `get_path_name` from `generate_graph.py` into `google_ai_studio_one_shot.py` and `rebuild_registries_son.py`.
   - In `transpose_flat_to_json()` and `process_and_update_coordinates()`:
     ```python
     expected_path = get_path_name(story["claim_u"], story["claim_psi"], story["real_u"], story["real_psi"])
     # Validate and overwrite trajectory line in posts[3] and posts[8]
     ```
   - Guarantee that no trajectory crossing into $-u$ can contain the word "Redemption".

2. **Fix Image Card Alt-Text Alignment (`aletheia_bot.py`)**:
   - Refactor `alt_parts` extraction in `aletheia_bot.py` to use key-prefix matching (matching `image_card_generator.py::extract_personas_from_posts`) rather than hardcoded array indices (`posts[4]`, `posts[5]`).

3. **Prevent Cascading Text Pollution (`aletheia_bot.py`)**:
   - In compact mode, do not use `carry_over` between distinct logical posts. If a post exceeds 260/280 characters, truncate cleanly with an ellipsis (`...`) within that post's slot rather than spilling content into the next post.

### Priority 2: Token Efficiency & Prompt Optimization (High)

4. **Eliminate Redundant Grounding Injection (`google_ai_studio_one_shot.py`)**:
   - Remove `extra_context` from `system_instruction` in line 1261, retaining it strictly once in `user_payload` (line 1776).

5. **Truncate Harvested Article Text (`harvest_candidates.py`)**:
   - Cap scraped article text at 2,500 characters in `harvest_candidates.py` (capturing title, description, and first 4 substantive paragraphs).
   - In multi-source clusters, limit each secondary source snippet to 1,200 characters.

6. **Preserve Bluesky Timestamps (`harvest_candidates.py`)**:
   - Extract `post.record.created_at` or `post.indexed_at` for all Bluesky candidates and store as ISO `pub_date` in `harvested_candidates.json`.

### Priority 3: Architecture & Reliability (Medium)

7. **Add Client-Side Timeouts to Gemini Calls**:
   - Pass an explicit HTTP timeout parameter to `google-genai` client configurations so network stalls trigger fallback models within 60–90 seconds.

8. **Implement Generalized Correction / Retraction Pipeline**:
   - Create a standardized CLI tool (`bluesky_bot/retract_story.py`) accepting `--story-id`, `--reason`, and `--revised-coords` to automate thread reply posting, card badge re-rendering, and registry state synchronization.

---
*End of Audit Report.*
