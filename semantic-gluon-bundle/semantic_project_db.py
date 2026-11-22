#!/usr/bin/env python3
"""
Semantic Gluon Project Management Database & JSON Engine
Architecture: 8-Vertex Semiotic Modal Topology (Parables Engine)
Features:
- Dual SQLite (relational ACID) + JSON synchronization
- Comparative Goal Resolution: Grounds vague goals like 'better' against 'was like' baselines and 'is not' boundaries
- Cross-Vertex Vector Opposition & Automatic Contradiction Cancellation
- Evolutionary Lineage & Task Supersession Tracking
- 4 Parables Dynamic Modal Operations (Productive, Reductive, Constructive, Regressive)
- Full CLI & Python API
"""

import sys
import os
import json
import sqlite3
import re
import datetime
import argparse
from typing import Dict, List, Optional, Any, Tuple

VALID_VERTICES = {
    # Solution Space (Inclusive / Productive)
    "will_be": "Target Goal / Definitive Future (solution outer)",
    "can_be": "Active Capability / Feasible Potential (solution inner)",
    "may_be": "Hypothesis / Speculative Probe (constructive inner)",
    "is_like": "Analogy / Precedent / Reference Pattern (constructive outer)",
    # Problem & Constraint Space (Exclusive / Reductive)
    "is_not": "Hard Anti-Goal / Taboo Boundary (problem outer)",
    "cant_be": "Invariant Constraint / Impossibility (problem inner)",
    "wont_be": "Explicitly Rejected / Pruned Scope (regressive inner)",
    "was_like": "Obsolete Legacy / Deprecated Precedent (regressive outer)",
    # Center
    "is": "Current Ground Truth / Active Reality"
}

OPPOSITION_VECTORS = {
    ("will_be", "cant_be"): {
        "type": "RED_PRIMARY",
        "severity": "FATAL_CONTRADICTION",
        "name": "Target Goal breaches Invariant Constraint",
        "rule": "If you target 'will_be' but it 'can't be', the desire is fundamentally invalid and is automatically cancelled."
    },
    ("can_be", "is_not"): {
        "type": "GREEN_PRIMARY",
        "severity": "BOUNDARY_VIOLATION",
        "name": "Active Action breaches Anti-Goal Boundary",
        "rule": "If an actionable task 'can be' done but enters 'is not', it must be immediately halted and flagged as conflicted."
    },
    ("is_like", "wont_be"): {
        "type": "RED_SECONDARY",
        "severity": "FALSE_ANALOGY",
        "name": "Design references an Explicitly Rejected Precedent",
        "rule": "Modeling after a pattern marked 'won't be' imports rejected architectural debt."
    },
    ("may_be", "was_like"): {
        "type": "GREEN_SECONDARY",
        "severity": "REGRESSION_RISK",
        "name": "Hypothesis loops back into Obsolete Legacy",
        "rule": "Exploring an idea that matches 'was like' duplicates a known obsolete failure."
    }
}


def _default_db_path() -> str:
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
    return os.environ.get("SEMANTIC_DB_PATH", os.path.join(bundle_dir, "semantic_project.db"))


class SemanticProjectDB:
    def __init__(self, db_path: str = None):
        if not db_path:
            db_path = _default_db_path()
        self.db_path = db_path

        db_dir = os.path.dirname(os.path.abspath(self.db_path))
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.execute("PRAGMA journal_mode = WAL")
            self.conn.row_factory = sqlite3.Row
            self._init_schema()
        except sqlite3.OperationalError:
            # Fallback to local user temp if directory permissions block WAL
            temp_db = os.path.join(os.environ.get("TEMP", "C:\\temp"), "semantic_project.db")
            os.makedirs(os.path.dirname(temp_db), exist_ok=True)
            self.db_path = temp_db
            self.conn = sqlite3.connect(self.db_path)
            self.conn.execute("PRAGMA journal_mode = MEMORY")
            self.conn.row_factory = sqlite3.Row
            self._init_schema()

    def _init_schema(self):
        with self.conn:
            self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                ground_truth_is TEXT DEFAULT 'Project initialized',
                created_at TEXT,
                updated_at TEXT
            );

            CREATE TABLE IF NOT EXISTS desires (
                id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                title TEXT NOT NULL,
                vertex TEXT NOT NULL,
                status TEXT DEFAULT 'active', -- active, completed, cancelled, superseded, conflicted
                rationale TEXT,
                superseded_by TEXT,
                supersedes TEXT,
                cancellation_reason TEXT,
                tags TEXT, -- JSON array
                created_at TEXT,
                updated_at TEXT,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            );

            CREATE TABLE IF NOT EXISTS anti_desires (
                id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                title TEXT NOT NULL,
                vertex TEXT NOT NULL,
                severity TEXT DEFAULT 'hard_invariant', -- hard_invariant, boundary_taboo, pruned_scope, deprecated_legacy
                reason_to_avoid TEXT,
                tags TEXT, -- JSON array
                created_at TEXT,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            );

            CREATE TABLE IF NOT EXISTS comparative_goals (
                id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                desire_id TEXT NOT NULL,
                predicate TEXT NOT NULL, -- e.g. 'better', 'faster', 'more lightweight', 'more scalable'
                target_dimension TEXT NOT NULL, -- e.g. 'latency', 'memory footprint', 'code complexity'
                baseline_was_like TEXT NOT NULL, -- The concrete past benchmark from was_like
                boundary_is_not TEXT NOT NULL, -- The constraint threshold from is_not that invalidates the claim
                reference_is_like TEXT, -- Working exemplar/template from is_like
                verification_status TEXT DEFAULT 'pending', -- pending, verified_true, refuted_false, invalidated_by_boundary
                verification_notes TEXT,
                created_at TEXT,
                FOREIGN KEY (project_id) REFERENCES projects(id),
                FOREIGN KEY (desire_id) REFERENCES desires(id)
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                desire_id TEXT NOT NULL,
                title TEXT NOT NULL,
                vertex TEXT DEFAULT 'can_be',
                status TEXT DEFAULT 'pending', -- pending, in_progress, completed, cancelled, blocked
                created_at TEXT,
                updated_at TEXT,
                FOREIGN KEY (desire_id) REFERENCES desires(id)
            );

            CREATE TABLE IF NOT EXISTS conflicts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id TEXT NOT NULL,
                desire_id TEXT NOT NULL,
                anti_desire_id TEXT NOT NULL,
                vector_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                rule TEXT,
                overlap_terms TEXT,
                detected_at TEXT,
                FOREIGN KEY (project_id) REFERENCES projects(id),
                FOREIGN KEY (desire_id) REFERENCES desires(id),
                FOREIGN KEY (anti_desire_id) REFERENCES anti_desires(id)
            );

            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT,
                timestamp TEXT
            );

            CREATE TABLE IF NOT EXISTS process_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id TEXT NOT NULL,
                process_type TEXT NOT NULL,
                item_id TEXT NOT NULL,
                transition TEXT NOT NULL,
                formula TEXT NOT NULL,
                notes TEXT,
                timestamp TEXT
            );
            """)

    def _log_audit(self, project_id: str, action: str, details: str):
        now = datetime.datetime.now().isoformat()
        self.conn.execute("INSERT INTO audit_log (project_id, action, details, timestamp) VALUES (?, ?, ?, ?)",
                          (project_id, action, details, now))

    def init_project(self, project_id: str, name: str, description: str, ground_truth_is: str = "Active working state") -> Dict[str, Any]:
        now = datetime.datetime.now().isoformat()
        with self.conn:
            self.conn.execute("""
            INSERT OR REPLACE INTO projects (id, name, description, ground_truth_is, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (project_id, name, description, ground_truth_is, now, now))
            self._log_audit(project_id, "INIT_PROJECT", f"Project {name} ({project_id}) initialized.")
        return {"status": "ok", "project_id": project_id, "name": name, "ground_truth_is": ground_truth_is}

    def list_projects(self) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM projects ORDER BY updated_at DESC")
        return [dict(row) for row in cursor.fetchall()]

    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def add_desire(self, project_id: str, title: str, vertex: str = "can_be", tags: List[str] = None, rationale: str = "") -> str:
        if vertex not in ["will_be", "can_be", "may_be", "is_like"]:
            raise ValueError(f"Invalid desire vertex '{vertex}'. Must be in [will_be, can_be, may_be, is_like]")
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM desires")
        existing_ids = {row[0] for row in cursor.fetchall()}
        count = 1
        while f"DES-{count:03d}" in existing_ids:
            count += 1
        desire_id = f"DES-{count:03d}"
        now = datetime.datetime.now().isoformat()
        
        with self.conn:
            self.conn.execute("""
            INSERT INTO desires (id, project_id, title, vertex, status, rationale, tags, created_at, updated_at)
            VALUES (?, ?, ?, ?, 'active', ?, ?, ?, ?)
            """, (desire_id, project_id, title, vertex, rationale, json.dumps(tags or []), now, now))
            self._log_audit(project_id, "ADD_DESIRE", f"Added desire {desire_id}: {title} at vertex {vertex}")
        
        self.detect_conflicts(project_id)
        return desire_id

    def add_anti_desire(self, project_id: str, title: str, vertex: str = "is_not", severity: str = "hard_invariant", reason_to_avoid: str = "", tags: List[str] = None) -> str:
        if vertex not in ["is_not", "cant_be", "wont_be", "was_like"]:
            raise ValueError(f"Invalid anti-desire vertex '{vertex}'. Must be in [is_not, cant_be, wont_be, was_like]")
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM anti_desires")
        existing_ids = {row[0] for row in cursor.fetchall()}
        count = 1
        while f"ANTI-{count:03d}" in existing_ids:
            count += 1
        anti_id = f"ANTI-{count:03d}"
        now = datetime.datetime.now().isoformat()

        with self.conn:
            self.conn.execute("""
            INSERT INTO anti_desires (id, project_id, title, vertex, severity, reason_to_avoid, tags, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (anti_id, project_id, title, vertex, severity, reason_to_avoid, json.dumps(tags or []), now))
            self._log_audit(project_id, "ADD_ANTI_DESIRE", f"Added anti-desire {anti_id}: {title} at vertex {vertex}")

        self.detect_conflicts(project_id)
        return anti_id

    def anchor_comparative_goal(self, project_id: str, desire_id: str, predicate: str, target_dimension: str,
                                baseline_was_like: str, boundary_is_not: str, reference_is_like: str = "") -> str:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM comparative_goals")
        existing_ids = {row[0] for row in cursor.fetchall()}
        count = 1
        while f"CMP-{count:03d}" in existing_ids:
            count += 1
        comp_id = f"CMP-{count:03d}"
        now = datetime.datetime.now().isoformat()

        with self.conn:
            self.conn.execute("""
            INSERT INTO comparative_goals (id, project_id, desire_id, predicate, target_dimension, baseline_was_like, boundary_is_not, reference_is_like, verification_status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?)
            """, (comp_id, project_id, desire_id, predicate, target_dimension, baseline_was_like, boundary_is_not, reference_is_like, now))
            self._log_audit(project_id, "ANCHOR_COMPARATIVE", f"Anchored vague predicate '{predicate}' for {desire_id} on dimension '{target_dimension}'")

        return comp_id

    def verify_comparative_goal(self, comp_id: str, achieved_metric_desc: str, breached_boundary: bool, surpassed_baseline: bool) -> Dict[str, Any]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM comparative_goals WHERE id = ?", (comp_id,))
        row = cursor.fetchone()
        if not row:
            raise KeyError(f"Comparative goal {comp_id} not found")

        desire_id = row["desire_id"]
        project_id = row["project_id"]

        if breached_boundary:
            status = "invalidated_by_boundary"
            notes = f"Refuted: Achieved '{achieved_metric_desc}' but breached boundary '{row['boundary_is_not']}'. The claim of '{row['predicate']}' is invalid."
            desire_status = "conflicted"
        elif surpassed_baseline:
            status = "verified_true"
            notes = f"Verified: Successfully advanced beyond baseline '{row['baseline_was_like']}' to '{achieved_metric_desc}' while respecting boundary '{row['boundary_is_not']}'."
            desire_status = "active"
        else:
            status = "refuted_false"
            notes = f"Refuted: Result '{achieved_metric_desc}' failed to decisively surpass baseline '{row['baseline_was_like']}'."
            desire_status = "active"

        with self.conn:
            self.conn.execute("""
            UPDATE comparative_goals
            SET verification_status = ?, verification_notes = ?
            WHERE id = ?
            """, (status, notes, comp_id))
            if status == "invalidated_by_boundary":
                self.conn.execute("UPDATE desires SET status = 'conflicted' WHERE id = ?", (desire_id,))
            self._log_audit(project_id, "VERIFY_COMPARATIVE", f"Evaluated {comp_id}: {status}")

        return {"comp_id": comp_id, "status": status, "notes": notes, "desire_status": desire_status}

    def add_task(self, desire_id: str, title: str, vertex: str = "can_be") -> str:
        cursor = self.conn.cursor()
        cursor.execute("SELECT project_id FROM desires WHERE id = ?", (desire_id,))
        row = cursor.fetchone()
        if not row:
            raise KeyError(f"Desire {desire_id} not found")
        project_id = row["project_id"]

        cursor.execute("SELECT COUNT(*) FROM tasks WHERE desire_id = ?", (desire_id,))
        count = cursor.fetchone()[0] + 1
        task_id = f"{desire_id}-T{count}"
        now = datetime.datetime.now().isoformat()

        with self.conn:
            self.conn.execute("""
            INSERT INTO tasks (id, desire_id, title, vertex, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, 'pending', ?, ?)
            """, (task_id, desire_id, title, vertex, now, now))
            self._log_audit(project_id, "ADD_TASK", f"Added task {task_id} to {desire_id}: {title}")

        return task_id

    def update_task_status(self, task_id: str, status: str) -> Dict[str, Any]:
        now = datetime.datetime.now().isoformat()
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT desire_id, title, vertex FROM tasks WHERE id = ?", (task_id,))
            t_row = cursor.fetchone()
            if not t_row:
                raise KeyError(f"Task {task_id} not found")
            desire_id = t_row["desire_id"]

            self.conn.execute("UPDATE tasks SET status = ?, updated_at = ? WHERE id = ?", (status, now, task_id))
            
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE desire_id = ? AND status != 'completed'", (desire_id,))
            remaining = cursor.fetchone()[0]
            desire_status = "active"
            if remaining == 0:
                self.conn.execute("UPDATE desires SET status = 'completed', updated_at = ? WHERE id = ?", (now, desire_id))
                desire_status = "completed"

        return {"task_id": task_id, "status": status, "desire_id": desire_id, "desire_status": desire_status}

    def supersede_desire(self, old_desire_id: str, new_desire_id: str, rationale: str) -> Dict[str, Any]:
        now = datetime.datetime.now().isoformat()
        with self.conn:
            self.conn.execute("""
            UPDATE desires
            SET status = 'superseded', vertex = 'was_like', superseded_by = ?, updated_at = ?
            WHERE id = ?
            """, (new_desire_id, now, old_desire_id))
            self.conn.execute("UPDATE desires SET supersedes = ?, updated_at = ? WHERE id = ?", (old_desire_id, now, new_desire_id))
            self.conn.execute("UPDATE tasks SET status = 'cancelled', updated_at = ? WHERE desire_id = ? AND status IN ('pending', 'in_progress')",
                              (now, old_desire_id))
            
            cursor = self.conn.cursor()
            cursor.execute("SELECT project_id FROM desires WHERE id = ?", (new_desire_id,))
            project_id = cursor.fetchone()[0]
            self._log_audit(project_id, "SUPERSEDE_DESIRE", f"Desire {old_desire_id} superseded by {new_desire_id}. Rationale: {rationale}")

        return {"old_desire_id": old_desire_id, "new_desire_id": new_desire_id, "status": "superseded", "rationale": rationale}

    def detect_conflicts(self, project_id: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM conflicts WHERE project_id = ?", (project_id,))

        cursor.execute("SELECT * FROM desires WHERE project_id = ? AND status NOT IN ('completed', 'superseded')", (project_id,))
        desires = cursor.fetchall()
        cursor.execute("SELECT * FROM anti_desires WHERE project_id = ?", (project_id,))
        anti_desires = cursor.fetchall()

        def extract_keywords(text: str) -> set:
            words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
            stop_words = {"the", "and", "for", "with", "this", "that", "from", "have", "what", "must", "not", "make", "need", "into"}
            return {w for w in words if w not in stop_words}

        detected = []
        now = datetime.datetime.now().isoformat()

        for d in desires:
            d_tags = set(t.lower() for t in json.loads(d["tags"] or "[]"))

            for a in anti_desires:
                a_tags = set(t.lower() for t in json.loads(a["tags"] or "[]"))
                
                # If explicit tags are provided on both, match strictly on tags; otherwise fall back to word token overlap
                if d_tags and a_tags:
                    overlap = d_tags.intersection(a_tags)
                else:
                    d_words = extract_keywords(d["title"])
                    a_words = extract_keywords(a["title"])
                    overlap = d_words.intersection(a_words)

                vector_key = (d["vertex"], a["vertex"])
                if overlap and vector_key in OPPOSITION_VECTORS:
                    rule_info = OPPOSITION_VECTORS[vector_key]
                    record = {
                        "project_id": project_id,
                        "desire_id": d["id"],
                        "anti_desire_id": a["id"],
                        "vector_type": rule_info["type"],
                        "severity": rule_info["severity"],
                        "rule": rule_info["rule"],
                        "overlap_terms": list(overlap)
                    }
                    detected.append(record)
                    with self.conn:
                        self.conn.execute("""
                        INSERT INTO conflicts (project_id, desire_id, anti_desire_id, vector_type, severity, rule, overlap_terms, detected_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (project_id, d["id"], a["id"], rule_info["type"], rule_info["severity"], rule_info["rule"], json.dumps(list(overlap)), now))
                        
                        if rule_info["severity"] == "FATAL_CONTRADICTION":
                            cancellation_reason = f"Naturally cancelled out by Anti-Desire {a['id']} ({rule_info['name']}): '{a['title']}'"
                            self.conn.execute("UPDATE desires SET status = 'cancelled', cancellation_reason = ?, updated_at = ? WHERE id = ?",
                                              (cancellation_reason, now, d["id"]))
                            self.conn.execute("UPDATE tasks SET status = 'cancelled', updated_at = ? WHERE desire_id = ? AND status IN ('pending', 'in_progress')",
                                              (now, d["id"]))
                        elif rule_info["severity"] == "BOUNDARY_VIOLATION":
                            self.conn.execute("UPDATE desires SET status = 'conflicted', updated_at = ? WHERE id = ?", (now, d["id"]))

        return detected

    def run_gluon_process(self, project_id: str, process_type: str, item_id: str, context_notes: str = "") -> Dict[str, Any]:
        process_type = process_type.lower()
        if process_type not in ["productive", "reductive", "constructive", "regressive"]:
            raise ValueError(f"Unknown process type '{process_type}'. Must be productive, reductive, constructive, or regressive.")

        now = datetime.datetime.now().isoformat()
        cursor = self.conn.cursor()
        res = {"process": process_type, "item_id": item_id, "project_id": project_id, "notes": context_notes}

        if process_type == "productive":
            cursor.execute("SELECT vertex FROM desires WHERE id = ? AND project_id = ?", (item_id, project_id))
            row = cursor.fetchone()
            if not row:
                raise KeyError(f"Desire {item_id} not found in project {project_id}")
            old_v = row["vertex"]
            with self.conn:
                self.conn.execute("UPDATE desires SET vertex = 'will_be', updated_at = ? WHERE id = ?", (now, item_id))
            res["transition"] = f"{old_v} -> will_be"
            res["formula"] = "Productive: defined as 'will be' using 'is not' & 'is like' opposing 'was like' until 'can be' committed to 'will be'."

        elif process_type == "reductive":
            cursor.execute("SELECT vertex FROM anti_desires WHERE id = ? AND project_id = ?", (item_id, project_id))
            row = cursor.fetchone()
            if not row:
                raise KeyError(f"Anti-desire {item_id} not found in project {project_id}")
            old_v = row["vertex"]
            with self.conn:
                self.conn.execute("UPDATE anti_desires SET vertex = 'is_not' WHERE id = ?", (item_id,))
            res["transition"] = f"{old_v} -> is_not"
            res["formula"] = "Reductive: defined as 'can't be' collapsed into 'is not' using 'was like' and 'can be' opposing 'is like'."

        elif process_type == "constructive":
            cursor.execute("SELECT vertex FROM desires WHERE id = ? AND project_id = ?", (item_id, project_id))
            row = cursor.fetchone()
            if not row:
                raise KeyError(f"Desire {item_id} not found in project {project_id}")
            old_v = row["vertex"]
            with self.conn:
                self.conn.execute("UPDATE desires SET vertex = 'is_like', updated_at = ? WHERE id = ?", (now, item_id))
            res["transition"] = f"{old_v} -> is_like"
            res["formula"] = "Constructive: hypothesis 'may be' synthesized into stable working precedent 'is like' using 'can be' & 'was like'."

        elif process_type == "regressive":
            cursor.execute("SELECT vertex FROM anti_desires WHERE id = ? AND project_id = ?", (item_id, project_id))
            row = cursor.fetchone()
            if row:
                old_v = row["vertex"]
                with self.conn:
                    self.conn.execute("UPDATE anti_desires SET vertex = 'was_like' WHERE id = ?", (item_id,))
                res["transition"] = f"{old_v} -> was_like"
                res["formula"] = "Regressive: scope rejection 'won't be' retired into archive 'was like' using 'is not' & 'is like' to oppose 'can be'."
            else:
                cursor.execute("SELECT vertex FROM desires WHERE id = ? AND project_id = ?", (item_id, project_id))
                drow = cursor.fetchone()
                if not drow:
                    raise KeyError(f"Item {item_id} not found in project {project_id}")
                old_v = drow["vertex"]
                with self.conn:
                    self.conn.execute("UPDATE desires SET vertex = 'was_like', status = 'superseded', updated_at = ? WHERE id = ?", (now, item_id))
                res["transition"] = f"{old_v} -> was_like (superseded)"
                res["formula"] = "Regressive retirement: desire retired into historical precedent 'was like'."

        with self.conn:
            self.conn.execute("""
            INSERT INTO process_logs (project_id, process_type, item_id, transition, formula, notes, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (project_id, process_type, item_id, res["transition"], res["formula"], context_notes, now))
            self._log_audit(project_id, "RUN_GLUON_PROCESS", f"{process_type}: {res['transition']}")

        self.detect_conflicts(project_id)
        return res

    def export_json(self, project_id: str, output_path: str = "project_desires.json"):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        p = cursor.fetchone()
        if not p:
            raise KeyError(f"Project {project_id} not found")

        doc = {
            "project_id": p["id"],
            "name": p["name"],
            "description": p["description"],
            "ground_truth_is": p["ground_truth_is"],
            "last_updated": p["updated_at"],
            "desires": {},
            "anti_desires": {},
            "comparative_goals": {},
            "conflicts": [],
            "process_logs": [],
            "audit_trail": []
        }

        cursor.execute("SELECT * FROM desires WHERE project_id = ?", (project_id,))
        for d in cursor.fetchall():
            cursor.execute("SELECT * FROM tasks WHERE desire_id = ?", (d["id"],))
            tasks = [{"id": t["id"], "title": t["title"], "vertex": t["vertex"], "status": t["status"]} for t in cursor.fetchall()]
            doc["desires"][d["id"]] = {
                "id": d["id"],
                "title": d["title"],
                "vertex": d["vertex"],
                "status": d["status"],
                "rationale": d["rationale"],
                "superseded_by": d["superseded_by"],
                "supersedes": d["supersedes"],
                "cancellation_reason": d["cancellation_reason"],
                "tags": json.loads(d["tags"] or "[]"),
                "tasks": tasks
            }

        cursor.execute("SELECT * FROM anti_desires WHERE project_id = ?", (project_id,))
        for a in cursor.fetchall():
            doc["anti_desires"][a["id"]] = {
                "id": a["id"],
                "title": a["title"],
                "vertex": a["vertex"],
                "severity": a["severity"],
                "reason_to_avoid": a["reason_to_avoid"],
                "tags": json.loads(a["tags"] or "[]")
            }

        cursor.execute("SELECT * FROM comparative_goals WHERE project_id = ?", (project_id,))
        for c in cursor.fetchall():
            doc["comparative_goals"][c["id"]] = {
                "id": c["id"],
                "desire_id": c["desire_id"],
                "predicate": c["predicate"],
                "target_dimension": c["target_dimension"],
                "baseline_was_like": c["baseline_was_like"],
                "boundary_is_not": c["boundary_is_not"],
                "reference_is_like": c["reference_is_like"],
                "verification_status": c["verification_status"],
                "verification_notes": c["verification_notes"]
            }

        cursor.execute("SELECT * FROM conflicts WHERE project_id = ?", (project_id,))
        for conf in cursor.fetchall():
            doc["conflicts"].append({
                "desire_id": conf["desire_id"],
                "anti_desire_id": conf["anti_desire_id"],
                "vector_type": conf["vector_type"],
                "severity": conf["severity"],
                "rule": conf["rule"],
                "overlap_terms": json.loads(conf["overlap_terms"] or "[]")
            })

        cursor.execute("SELECT * FROM process_logs WHERE project_id = ? ORDER BY timestamp DESC", (project_id,))
        for pl in cursor.fetchall():
            doc["process_logs"].append(dict(pl))

        cursor.execute("SELECT * FROM audit_log WHERE project_id = ? ORDER BY timestamp DESC LIMIT 50", (project_id,))
        for al in cursor.fetchall():
            doc["audit_trail"].append(dict(al))

        out_dir = os.path.dirname(os.path.abspath(output_path))
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=2)

        return doc

    def render_markdown_dashboard(self, project_id: str) -> str:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        p = cursor.fetchone()
        if not p:
            return f"❌ Project '{project_id}' not found."

        lines = []
        lines.append(f"# 🌌 Semantic Gluon Project Board: {p['name']}")
        lines.append(f"**Project ID**: `{p['id']}` | **Updated**: `{p['updated_at']}`")
        lines.append(f"> **Ground Truth (IS)**: {p['ground_truth_is']}\n")

        vertex_buckets = {k: [] for k in VALID_VERTICES if k != "is"}
        cursor.execute("SELECT id, title, vertex, status FROM desires WHERE project_id = ?", (project_id,))
        for d in cursor.fetchall():
            vertex_buckets[d["vertex"]].append(f"[Desire {d['id']}] {d['title']} ({d['status']})")
        cursor.execute("SELECT id, title, vertex, severity FROM anti_desires WHERE project_id = ?", (project_id,))
        for a in cursor.fetchall():
            vertex_buckets[a["vertex"]].append(f"[Anti {a['id']}] {a['title']} ({a['severity']})")

        lines.append("## 🌌 8-Vertex Semantic Topology")
        lines.append("| Solution Space (Inclusive / Productive) | Problem & Constraint Space (Exclusive / Reductive) |")
        lines.append("| :--- | :--- |")
        lines.append(f"| **`will_be` (Target Goal)**: {len(vertex_buckets['will_be'])} items<br>" + "<br>".join(vertex_buckets['will_be'] or ['*(empty)*']) +
                     f" | **`is_not` (Hard Anti-Goal)**: {len(vertex_buckets['is_not'])} items<br>" + "<br>".join(vertex_buckets['is_not'] or ['*(empty)*']) + " |")
        lines.append(f"| **`can_be` (Active Capability)**: {len(vertex_buckets['can_be'])} items<br>" + "<br>".join(vertex_buckets['can_be'] or ['*(empty)*']) +
                     f" | **`cant_be` (Invariant Constraint)**: {len(vertex_buckets['cant_be'])} items<br>" + "<br>".join(vertex_buckets['cant_be'] or ['*(empty)*']) + " |")
        lines.append(f"| **`may_be` (Hypothesis Probe)**: {len(vertex_buckets['may_be'])} items<br>" + "<br>".join(vertex_buckets['may_be'] or ['*(empty)*']) +
                     f" | **`wont_be` (Pruned Scope)**: {len(vertex_buckets['wont_be'])} items<br>" + "<br>".join(vertex_buckets['wont_be'] or ['*(empty)*']) + " |")
        lines.append(f"| **`is_like` (Precedent / Template)**: {len(vertex_buckets['is_like'])} items<br>" + "<br>".join(vertex_buckets['is_like'] or ['*(empty)*']) +
                     f" | **`was_like` (Legacy / Archive)**: {len(vertex_buckets['was_like'])} items<br>" + "<br>".join(vertex_buckets['was_like'] or ['*(empty)*']) + " |")

        # Comparative Goals Verification (Testing 'better')
        cursor.execute("SELECT * FROM comparative_goals WHERE project_id = ?", (project_id,))
        comps = cursor.fetchall()
        lines.append("\n## ⚖️ Comparative Goal Resolution (Testing 'Better' & 'Faster')")
        if not comps:
            lines.append("*(No comparative goals registered yet. Use `anchor-comparative` to ground subjective claims.)*")
        else:
            for c in comps:
                badge = {
                    "verified_true": "✅ Verified True",
                    "refuted_false": "❌ Refuted (Did not beat baseline)",
                    "invalidated_by_boundary": "🛑 Invalidated (Breached Anti-Goal)",
                    "pending": "⏳ Pending Empirical Data"
                }.get(c["verification_status"], c["verification_status"])
                lines.append(f"### {c['id']}: Predicate '{c['predicate']}' for Desire `{c['desire_id']}` — {badge}")
                lines.append(f"- **Target Dimension**: `{c['target_dimension']}`")
                lines.append(f"- **Baseline (`was_like`)**: {c['baseline_was_like']}")
                lines.append(f"- **Boundary Guardrail (`is_not`)**: {c['boundary_is_not']}")
                if c["reference_is_like"]:
                    lines.append(f"- **Reference Model (`is_like`)**: {c['reference_is_like']}")
                if c["verification_notes"]:
                    lines.append(f"- **Verification Verdict**: {c['verification_notes']}")

        # Active Conflicts
        cursor.execute("SELECT * FROM conflicts WHERE project_id = ?", (project_id,))
        confs = cursor.fetchall()
        lines.append("\n## ⚡ Vector Collisions & Natural Cancellations")
        if not confs:
            lines.append("✅ *Zero vector collisions detected. All active desires are topologically clear.*")
        else:
            for c in confs:
                terms = json.loads(c["overlap_terms"] or "[]")
                lines.append(f"- **[{c['vector_type']} - {c['severity']}]**: Desire `{c['desire_id']}` collides with Anti-Desire `{c['anti_desire_id']}`")
                lines.append(f"  - **Rule**: {c['rule']}")
                lines.append(f"  - **Overlapping Tokens**: `{', '.join(terms)}`")

        # Itemized Desires & Tasks
        lines.append("\n## 🎯 Desires & Tasks")
        cursor.execute("SELECT * FROM desires WHERE project_id = ?", (project_id,))
        for d in cursor.fetchall():
            badge = {
                "active": "🟢 Active",
                "completed": "✅ Completed",
                "conflicted": "⚠️ Conflicted",
                "cancelled": "🛑 Cancelled (Auto-Neutralized)",
                "superseded": "🔄 Superseded"
            }.get(d["status"], d["status"])
            lines.append(f"### {d['id']}: {d['title']} — {badge}")
            lines.append(f"- **Vertex**: `{d['vertex']}`")
            if d["superseded_by"]:
                lines.append(f"- **Superseded by**: `{d['superseded_by']}`")
            if d["cancellation_reason"]:
                lines.append(f"- **Cancellation Reason**: {d['cancellation_reason']}")
            cursor.execute("SELECT * FROM tasks WHERE desire_id = ?", (d["id"],))
            tasks = cursor.fetchall()
            if tasks:
                for t in tasks:
                    t_icon = "✓" if t["status"] == "completed" else "✗" if t["status"] == "cancelled" else "•"
                    lines.append(f"  - [{t_icon}] `{t['id']}` {t['title']} (`{t['status']}` | `{t['vertex']}`)")
            else:
                lines.append("  - *(No sub-tasks attached)*")

        return "\n".join(lines)


# ==============================================================================
# CLI Entry Point
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="Semantic Gluon Project Database CLI")
    parser.add_argument("--db", default=None, help="Database file path (defaults to semantic_project.db in bundle)")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # init-project
    init_p = subparsers.add_parser("init", help="Initialize a project")
    init_p.add_argument("--id", required=True, help="Project ID")
    init_p.add_argument("--name", required=True, help="Project name")
    init_p.add_argument("--desc", default="", help="Description")
    init_p.add_argument("--is", dest="ground_truth_is", default="Active state", help="Ground truth reality")

    # list-projects
    subparsers.add_parser("list-projects", help="List all projects")

    # add-desire
    des_p = subparsers.add_parser("add-desire", help="Add a desire")
    des_p.add_argument("--project", required=True)
    des_p.add_argument("--title", required=True)
    des_p.add_argument("--vertex", default="can_be", choices=["will_be", "can_be", "may_be", "is_like"])
    des_p.add_argument("--tags", nargs="*", default=[])
    des_p.add_argument("--rationale", default="")

    # add-anti-desire
    anti_p = subparsers.add_parser("add-anti", help="Add an anti-desire")
    anti_p.add_argument("--project", required=True)
    anti_p.add_argument("--title", required=True)
    anti_p.add_argument("--vertex", default="is_not", choices=["is_not", "cant_be", "wont_be", "was_like"])
    anti_p.add_argument("--severity", default="hard_invariant")
    anti_p.add_argument("--reason", default="")
    anti_p.add_argument("--tags", nargs="*", default=[])

    # anchor-comparative
    cmp_p = subparsers.add_parser("anchor-comparative", help="Anchor a vague goal (e.g. 'better')")
    cmp_p.add_argument("--project", required=True)
    cmp_p.add_argument("--desire", required=True)
    cmp_p.add_argument("--predicate", required=True, help="Predicate (better, faster, simpler)")
    cmp_p.add_argument("--dimension", required=True, help="Target dimension (latency, RAM, etc)")
    cmp_p.add_argument("--baseline", required=True, help="Baseline was_like metric")
    cmp_p.add_argument("--boundary", required=True, help="Boundary is_not threshold")
    cmp_p.add_argument("--reference", default="", help="Reference is_like template")

    # verify-comparative
    ver_p = subparsers.add_parser("verify-comparative", help="Evaluate if 'better' holds true")
    ver_p.add_argument("--id", required=True, help="Comparative goal ID")
    ver_p.add_argument("--achieved", required=True, help="Achieved empirical result")
    ver_p.add_argument("--breached-boundary", action="store_true", help="Did it breach the is_not threshold?")
    ver_p.add_argument("--surpassed-baseline", action="store_true", help="Did it beat the was_like baseline?")

    # add-task
    tsk_p = subparsers.add_parser("add-task", help="Add a task to a desire")
    tsk_p.add_argument("--desire", required=True)
    tsk_p.add_argument("--title", required=True)
    tsk_p.add_argument("--vertex", default="can_be")

    # update-task
    utsk_p = subparsers.add_parser("update-task", help="Update task status")
    utsk_p.add_argument("--task", required=True)
    utsk_p.add_argument("--status", required=True, choices=["pending", "in_progress", "completed", "cancelled", "blocked"])

    # supersede
    sup_p = subparsers.add_parser("supersede", help="Supersede an old desire")
    sup_p.add_argument("--old", required=True)
    sup_p.add_argument("--new", required=True)
    sup_p.add_argument("--rationale", default="")

    # board
    board_p = subparsers.add_parser("board", help="Render Markdown dashboard")
    board_p.add_argument("--project", required=True)
    board_p.add_argument("--out", default=None, help="Save dashboard directly to markdown file")

    # export
    exp_p = subparsers.add_parser("export", help="Export to JSON")
    exp_p.add_argument("--project", required=True)
    exp_p.add_argument("--out", default="project_desires.json")

    args = parser.parse_args()
    db = SemanticProjectDB(args.db)

    if args.command == "init":
        res = db.init_project(args.id, args.name, args.desc, args.ground_truth_is)
        print(f"Project initialized: {res}")
    elif args.command == "list-projects":
        projs = db.list_projects()
        print(f"Found {len(projs)} projects:")
        for p in projs:
            print(f"- [{p['id']}] {p['name']} (updated {p['updated_at']})")
    elif args.command == "add-desire":
        did = db.add_desire(args.project, args.title, args.vertex, args.tags, args.rationale)
        print(f"Created desire: {did}")
    elif args.command == "add-anti":
        aid = db.add_anti_desire(args.project, args.title, args.vertex, args.severity, args.reason, args.tags)
        print(f"Created anti-desire: {aid}")
    elif args.command == "anchor-comparative":
        cid = db.anchor_comparative_goal(args.project, args.desire, args.predicate, args.dimension, args.baseline, args.boundary, args.reference)
        print(f"Anchored comparative goal: {cid}")
    elif args.command == "verify-comparative":
        res = db.verify_comparative_goal(args.id, args.achieved, args.breached_boundary, args.surpassed_baseline)
        print(f"Verification result: {json.dumps(res, indent=2)}")
    elif args.command == "add-task":
        tid = db.add_task(args.desire, args.title, args.vertex)
        print(f"Created task: {tid}")
    elif args.command == "update-task":
        res = db.update_task_status(args.task, args.status)
        print(f"Task updated: {res}")
    elif args.command == "supersede":
        res = db.supersede_desire(args.old, args.new, args.rationale)
        print(f"Desire {args.old} superseded by {args.new}")
    elif args.command == "board":
        board_text = db.render_markdown_dashboard(args.project)
        if getattr(args, "out", None):
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(board_text)
            print(f"Board saved to {args.out}")
        else:
            sys.stdout.buffer.write(board_text.encode("utf-8") + b"\n")
    elif args.command == "export":
        db.export_json(args.project, args.out)
        print(f"Exported project {args.project} to {args.out}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
