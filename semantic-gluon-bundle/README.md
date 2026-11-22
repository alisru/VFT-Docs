# Semantic Gluon Project & Desire Tracking System

A complete 8-vertex semiotic modal topology for AI task planning, comparative goal anchoring, and natural contradiction cancellation (based on the Parables modal dynamics).

---

## 📦 What's Inside

- **`semantic_project_db.py`**: High-integrity dual SQLite + JSON relational database engine & CLI. Handles persistence, opposition detection, and 4 Parables modal dynamic transitions (`productive`, `reductive`, `constructive`, `regressive`).
- **`mcp-server/semantic_gluon_mcp.py`**: Production-grade JSON-RPC 2.0 stdio Model Context Protocol (MCP) server. Exposes 13 project management and topological audit tools.
- **`skills/gemini-project-manager/SKILL.md`**: Project manager skill specification (also synced to `.agents/skills/gemini-project-manager/SKILL.md`).
- **`project_desires.json`**: Real-time portable JSON export synchronized on every mutation.
- **`semantic_project.db`**: Local SQLite database with full ACID compliance and WAL mode.

---

## 🛠️ MCP Tools Exposed

| Tool | Parameters | Description |
| :--- | :--- | :--- |
| `gluon_init_project` | `project_id`, `name`, `description`, `ground_truth_is` | Initialize or update a project workspace. |
| `gluon_list_projects` | *(none)* | List all tracked projects and their update timestamps. |
| `gluon_add_desire` | `project_id`, `title`, `vertex`, `tags`, `rationale` | Register a positive goal (`will_be`, `can_be`, `may_be`, `is_like`). |
| `gluon_add_anti_desire` | `project_id`, `title`, `vertex`, `severity`, `reason_to_avoid`, `tags` | Register a hard taboo or boundary (`is_not`, `cant_be`, `wont_be`, `was_like`). |
| `gluon_anchor_comparative` | `project_id`, `desire_id`, `predicate`, `target_dimension`, `baseline_was_like`, `boundary_is_not`, `reference_is_like` | Ground qualitative goals like *"better"* or *"faster"* against baselines and boundaries. |
| `gluon_verify_comparative` | `comp_id`, `achieved_metric_desc`, `breached_boundary`, `surpassed_baseline` | Test whether an empirical measurement verified the comparative claim without boundary breach. |
| `gluon_add_task` | `desire_id`, `title`, `vertex` | Attach an actionable work item to a desire. |
| `gluon_update_task` | `task_id`, `status` | Update execution status (`pending`, `in_progress`, `completed`, `cancelled`, `blocked`). |
| `gluon_supersede_desire` | `old_desire_id`, `new_desire_id`, `rationale` | Retire an old design into `was_like` history while preserving lineage. |
| `gluon_detect_conflicts` | `project_id` | Audit opposition lines and auto-cancel conflicting desires. |
| `gluon_run_process` | `project_id`, `process_type`, `item_id`, `context_notes` | Execute a Parables dynamic transition (`productive`, `reductive`, `constructive`, `regressive`). |
| `gluon_render_board` | `project_id` | Render a full scannable Markdown status board. |
| `gluon_export_json` | `project_id`, `output_path` | Export project state to JSON. |

---

## ⚡ Natural Contradiction Cancellation

The topology enforces 4 opposition lines:
- **`will_be` vs `cant_be` (Red Primary - Fatal Contradiction)**: Target Goal breaches an Invariant Constraint. The desire and attached tasks are automatically marked `cancelled`.
- **`can_be` vs `is_not` (Green Primary - Boundary Violation)**: Actionable step enters a taboo boundary. The desire is marked `conflicted` and halted.
- **`is_like` vs `wont_be` (Red Secondary - False Analogy)**: Design mimics an explicitly rejected pattern.
- **`may_be` vs `was_like` (Green Secondary - Regression Risk)**: Speculative probe duplicates an obsolete legacy failure.

---

## 🚀 Usage

### 1. In Antigravity / Gemini
The server is registered in `~/.gemini/config/mcp_config.json` as `semantic-gluon`. The agent can invoke any of the `gluon_*` tools natively or lazily.

### 2. Standalone CLI
```bash
python semantic_project_db.py init --id PRJ-001 --name "My Project" --desc "Description"
python semantic_project_db.py add-desire --project PRJ-001 --title "Optimized storage" --vertex will_be
python semantic_project_db.py add-anti --project PRJ-001 --title "No cloud API dependencies" --vertex is_not
python semantic_project_db.py anchor-comparative --project PRJ-001 --desire DES-001 --predicate better --dimension latency --baseline "50ms" --boundary "Zero cloud APIs"
python semantic_project_db.py board --project PRJ-001
```
