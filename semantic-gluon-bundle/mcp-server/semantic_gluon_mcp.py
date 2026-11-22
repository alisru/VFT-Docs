#!/usr/bin/env python3
"""
Semantic Gluon Project & Desire Tracking Engine (FastMCP Server)
Built on the official 'mcp' SDK using FastMCP.
Implements the 8-vertex modal topology, comparative goal anchoring,
dual SQLite + JSON synchronization, and topological contradiction cancellation.
"""

import sys
import os
import json
from typing import List, Optional

# Ensure sibling directory or root can import semantic_project_db
BUNDLE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BUNDLE_DIR not in sys.path:
    sys.path.insert(0, BUNDLE_DIR)

from semantic_project_db import SemanticProjectDB
from mcp.server.fastmcp import FastMCP

DEFAULT_DB_PATH = os.path.join(BUNDLE_DIR, "semantic_project.db")
DEFAULT_JSON_PATH = os.path.join(BUNDLE_DIR, "project_desires.json")

mcp = FastMCP("semantic-gluon")
db = SemanticProjectDB(DEFAULT_DB_PATH)


def _sync(project_id: str):
    try:
        db.export_json(project_id, DEFAULT_JSON_PATH)
    except Exception:
        pass


@mcp.tool()
def gluon_init_project(project_id: str, name: str, description: str, ground_truth_is: str = "Project initialized in active working state") -> str:
    """Initialize a new Semantic Gluon project tracking store with 8-vertex topology."""
    res = db.init_project(project_id, name, description, ground_truth_is)
    _sync(project_id)
    return json.dumps(res, indent=2)


@mcp.tool()
def gluon_list_projects() -> str:
    """List all active projects tracked in the Semantic Gluon database."""
    projects = db.list_projects()
    return json.dumps({"projects": projects}, indent=2)


@mcp.tool()
def gluon_add_desire(project_id: str, title: str, vertex: str = "can_be", tags: Optional[List[str]] = None, rationale: str = "") -> str:
    """Add a desired goal, feature, or target outcome. Automatically checks vector opposition."""
    desire_id = db.add_desire(project_id, title, vertex, tags, rationale)
    conflicts = db.detect_conflicts(project_id)
    _sync(project_id)
    return json.dumps({
        "status": "created",
        "desire_id": desire_id,
        "project_id": project_id,
        "active_conflicts": [c for c in conflicts if c["desire_id"] == desire_id]
    }, indent=2)


@mcp.tool()
def gluon_add_anti_desire(project_id: str, title: str, vertex: str = "is_not", severity: str = "hard_invariant", reason_to_avoid: str = "", tags: Optional[List[str]] = None) -> str:
    """Add an anti-desire (what NOT to achieve / invariant constraint / boundary taboo / deprecated legacy)."""
    anti_id = db.add_anti_desire(project_id, title, vertex, severity, reason_to_avoid, tags)
    conflicts = db.detect_conflicts(project_id)
    _sync(project_id)
    return json.dumps({
        "status": "created",
        "anti_desire_id": anti_id,
        "project_id": project_id,
        "active_conflicts": [c for c in conflicts if c["anti_desire_id"] == anti_id]
    }, indent=2)


@mcp.tool()
def gluon_anchor_comparative(project_id: str, desire_id: str, predicate: str, target_dimension: str, baseline_was_like: str, boundary_is_not: str, reference_is_like: str = "") -> str:
    """Ground vague comparative goals (e.g. 'better', 'faster', 'cleaner') into falsifiable criteria against baselines and boundaries."""
    comp_id = db.anchor_comparative_goal(project_id, desire_id, predicate, target_dimension, baseline_was_like, boundary_is_not, reference_is_like)
    _sync(project_id)
    return json.dumps({
        "status": "anchored",
        "comp_id": comp_id,
        "desire_id": desire_id,
        "predicate": predicate,
        "target_dimension": target_dimension
    }, indent=2)


@mcp.tool()
def gluon_verify_comparative(comp_id: str, achieved_metric_desc: str, breached_boundary: bool, surpassed_baseline: bool) -> str:
    """Empirically evaluate whether a comparative goal ('better') succeeded without violating boundary guardrails."""
    res = db.verify_comparative_goal(comp_id, achieved_metric_desc, breached_boundary, surpassed_baseline)
    cursor = db.conn.cursor()
    cursor.execute("SELECT project_id FROM comparative_goals WHERE id = ?", (comp_id,))
    row = cursor.fetchone()
    if row:
        _sync(row["project_id"])
    return json.dumps(res, indent=2)


@mcp.tool()
def gluon_add_task(desire_id: str, title: str, vertex: str = "can_be") -> str:
    """Attach a concrete executable task to an existing desire."""
    task_id = db.add_task(desire_id, title, vertex)
    cursor = db.conn.cursor()
    cursor.execute("SELECT project_id FROM desires WHERE id = ?", (desire_id,))
    row = cursor.fetchone()
    if row:
        _sync(row["project_id"])
    return json.dumps({"status": "created", "task_id": task_id, "desire_id": desire_id}, indent=2)


@mcp.tool()
def gluon_update_task(task_id: str, status: str) -> str:
    """Update task execution status (pending, in_progress, completed, cancelled, blocked)."""
    res = db.update_task_status(task_id, status)
    cursor = db.conn.cursor()
    cursor.execute("SELECT project_id FROM desires WHERE id = ?", (res["desire_id"],))
    row = cursor.fetchone()
    if row:
        _sync(row["project_id"])
    return json.dumps(res, indent=2)


@mcp.tool()
def gluon_supersede_desire(old_desire_id: str, new_desire_id: str, rationale: str) -> str:
    """Mark an old desire as superseded by a new desire, retiring it into was_like history while maintaining lineage."""
    res = db.supersede_desire(old_desire_id, new_desire_id, rationale)
    cursor = db.conn.cursor()
    cursor.execute("SELECT project_id FROM desires WHERE id = ?", (new_desire_id,))
    row = cursor.fetchone()
    if row:
        _sync(row["project_id"])
    return json.dumps(res, indent=2)


@mcp.tool()
def gluon_detect_conflicts(project_id: str) -> str:
    """Evaluate all cross-vertex opposition lines and auto-cancel conflicting desires."""
    conflicts = db.detect_conflicts(project_id)
    _sync(project_id)
    return json.dumps({"project_id": project_id, "conflict_count": len(conflicts), "conflicts": conflicts}, indent=2)


@mcp.tool()
def gluon_run_process(project_id: str, process_type: str, item_id: str, context_notes: str = "") -> str:
    """Execute one of 4 Parables dynamic operations: productive (can_be->will_be), reductive (cant_be->is_not), constructive (may_be->is_like), regressive (wont_be->was_like)."""
    res = db.run_gluon_process(project_id, process_type, item_id, context_notes)
    _sync(project_id)
    return json.dumps(res, indent=2)


@mcp.tool()
def gluon_render_board(project_id: str) -> str:
    """Render a rich Markdown dashboard of all 8 vertices, collisions, comparative goals, and task statuses."""
    board_md = db.render_markdown_dashboard(project_id)
    return board_md


@mcp.tool()
def gluon_export_json(project_id: str, output_path: str = "") -> str:
    """Synchronize and export the project database to portable JSON format."""
    out_path = output_path or DEFAULT_JSON_PATH
    doc = db.export_json(project_id, out_path)
    return json.dumps({"status": "exported", "project_id": project_id, "path": out_path, "summary": f"{len(doc['desires'])} desires, {len(doc['anti_desires'])} anti-desires"}, indent=2)


if __name__ == "__main__":
    mcp.run()
