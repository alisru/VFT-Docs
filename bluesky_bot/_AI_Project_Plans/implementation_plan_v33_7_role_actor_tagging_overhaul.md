# Implementation Plan: 7-Role Actor Tagging System Overhaul

## 1. Executive Summary & Problem Diagnosis
The current actor tagging system has caused severe attribution errors and ranking inversions:
1. **Observer vs Target Inversion**: Outlets exposing corruption (e.g. ProPublica, BBC) are tagged as generic actors, inheriting the target agency's deception delta ($\Delta\upsilon = +1.49$, ranking ProPublica #4 in hypocrisy).
2. **Multi-Headline Roundup Bleed**: Aggregator URLs (e.g., Squirrel News) append unrelated headlines from trailing slugs (e.g., tagging England & Wales in Beijing air pollution stories).
3. **Passive Context Conflation**: Geographic locations, affected victims, and courts are tagged identically to primary moral violators.

This plan outlines a deterministic, phased migration to upgrade the actor system from a flat string array to a **7-Role Taxonomy** (`instigator`, `acted_upon`, `beneficiary`, `author`, `regulator`, `context`, `misc`).

---

## 2. The 7-Role Actor Taxonomy

| Role Key | Name | Definition & Real-World Examples | Leaderboard Action |
| :--- | :--- | :--- | :--- |
| **`instigator`** | **Prime Mover / Agent** | The active person or institution executing the audited action, statement, or extraction *(e.g., Donald Trump, ICE, Elon Musk, EPA)*. | **Primary Actor Hypocrisy Leaderboard** ($\overline{\Delta\upsilon}, \text{real}\_\upsilon$). |
| **`acted_upon`** | **Target / Victim / Population** | The people, victims, consumers, or groups who absorb the effects of the action *(e.g., 500 Detained Citizens, Patients, Students)*. | **Excluded from Hypocrisy**; eligible for Impact/Harm metrics. |
| **`beneficiary`** | **Extractor / Recipient** | A third party profiting or gaining advantage from the instigator's action without executing it *(e.g., For-profit voucher schools, defense contractors)*. | **Excluded from Instigator Board**; tracked under Collusion/Extraction. |
| **`author`** | **Reporter / Expositor** | The journalist, news outlet, or whistleblower uncovering the story *(e.g., ProPublica, BBC, The Guardian, FOIA requester)*. | **Excluded from Actor Board**; evaluated on Outlet Slant Leaderboard. |
| **`regulator`** | **Oversight / Arbiter / Judge** | Legal or institutional body reviewing, blocking, or ruling on the action *(e.g., Federal Judiciary, Supreme Court, QCAT, EPA oversight)*. | **Excluded from Instigator Board**; tracked under Regulatory Enforcement. |
| **`context`** | **Geography / Venue / Setting** | Country, city, physical venue, or tournament setting *(e.g., England, Wimbledon, Red Sea, Texas, Beijing)*. | **Excluded from Hypocrisy**; tracked under Geopolitical/Regional trends. |
| **`misc`** | **Tangential / Passing Mention** | Named entities mentioned in passing or background context without driving moral vector *(e.g., celebrity cameos, historical references)*. | **Searchable in Archive**, but excluded from all leaderboard aggregations. |

---

## 3. Data Schema Architecture

### 3.1 Backwards-Compatible Storage (`story.json` & `stories_registry.js`)
To ensure total backwards compatibility with external search tools, bots, and legacy scripts:
```json
{
  "actors": [
    "U.S. Immigration and Customs Enforcement",
    "Department of Homeland Security",
    "500 U.S. Citizens",
    "ProPublica",
    "United States"
  ],
  "actor_roles": [
    { "name": "U.S. Immigration and Customs Enforcement", "role": "instigator" },
    { "name": "Department of Homeland Security", "role": "instigator" },
    { "name": "500 U.S. Citizens", "role": "acted_upon" },
    { "name": "ProPublica", "role": "author" },
    { "name": "United States", "role": "context" }
  ]
}
```
*Note*: `actors` remains a list of strings so existing text indexing and queries do not break. `actor_roles` provides typed metadata.

---

## 4. Phase-by-Phase Implementation Roadmap

### Phase 1: Rule Engine & Known Entity Dictionaries (`actor_extract.py`)
1. **Curate Known Media Outlets & Publishers**:
   - `OUTLETS = {'propublica', 'bbc', 'fox news', 'cnn', 'nytimes', 'reuters', 'bloomberg', 'the guardian', 'politico', 'the hill', 'scmp', 'sixth tone', ...}`
   - Any entity matching the story's domain or this set is automatically assigned `role: "author"`.
2. **Curate Geopolitical Contexts**:
   - `GEOGRAPHY = {'england', 'wales', 'scotland', 'united kingdom', 'united states', 'australia', 'china', 'texas', 'california', 'beijing', ...}`
   - Assigned `role: "context"` unless explicitly framed as an active government body (`"UK Government"`, `"State of Texas"`).
3. **Curate Legal & Regulatory Arbiters**:
   - `REGULATORS = {'federal court', 'supreme court', 'qcat', 'high court', 'fair work commission', 'doj', 'cfpb', ...}`
   - Assigned `role: "regulator"`.
4. **Multi-Headline Roundup Truncation**:
   - Detect URLs from `squirrel-news.net`, `what-went-right`, etc. Strip secondary headline slugs before extracting entities to avoid trailing bleed.

### Phase 2: Ingest Existing Sub-Audits (2,648 Stories)
1. For stories with `Sub-Audits Breakdown:` in Post 5:
   - Extract the entity and its explicit verdict (`PASS`/`FAIL`/`COND`).
   - If an entity was audited with `PASS (+0.9, +0.8) — Exposes hidden citizen detentions`, classify as `author` or `regulator` with its own positive coordinate.
   - If an entity was audited with `FAIL (-0.9, -0.9) — Denies documented civil rights abuses`, classify as `instigator`.

### Phase 3: Offline Migration Script (`migrate_actor_roles.py`)
1. Create a non-destructive offline script to process:
   - All `stories/live/*.json` and `stories/*.json`
   - Classify existing actors into `actor_roles`.
   - Default unclassified entities to `instigator` if they appear in the headline subject action verb, or `misc` if peripheral.
2. Re-run `rebuild_registries.py` to compile `actor_roles` into `stories_registry.js`.

### Phase 4: Leaderboard & UI Engine Update (`control_panel.html` & `aletheia_mcp_server.py`)
1. Update `_getStatsForTable()`:
   - For `actor`: filter strictly to `role === 'instigator'` (or fallback to entities not flagged as `author`, `context`, or `misc`).
   - Add a role filter dropdown in the Actor Leaderboard: `[All Roles | Instigators Only | Targets/Victims | Regulators | Media]`.
2. Update the dropdown preview to display role badges (e.g. `[Instigator]`, `[Author]`, `[Target]`).

### Phase 5: Regeneration & Static Site Sync
1. Run `python export_audit_site.py` to regenerate `dist_audit_site/`.
2. Verify in Chrome Devtools that:
   - ProPublica disappears from the top of the Actor Hypocrisy Leaderboard and moves to the Outlet/Author section.
   - England in the Beijing air pollution story is flagged as `context` and does not inherit the PM2.5 verdict.
   - Page responsiveness remains $<300\text{ ms}$.

---

## 5. Verification Metrics & Guardrails
- **No data loss**: `actors` string array is preserved for zero breaking changes.
- **Top Actor Sanity Check**: Top hypocrisy ranks must consist strictly of institutional violators, fraudulent corporations, or corrupt officials (ICE, Kushner, Federalist, Blanche, Hegseth), with 0 news publishers or passive populations in the top 20.
- **Morality-Will Coordinate**: $(\upsilon=+2.0, \psi=+2.0)$ — Structural justice in epistemological attribution.
