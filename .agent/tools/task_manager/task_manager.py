#!/usr/bin/env python3
"""
No More Fuckups Task Engine v5
==============================
A hegemonic, class-based Task & Compliance Engine.
Features:
- Project-based folder structure
- Contextual Start (future awareness, pitfall scan)
- Tag-Based Semantic Error Linking (auto-propagation)
- Reasoning Trace & Postmortem Analysis
- Global Mistakes Registry (cross-conversation learning)
- Mandatory Pre-flight with Lessons Surfacing
"""

import json
import argparse
import sys
import os
from datetime import datetime
from typing import List, Dict, Any, Optional, Set
from enum import Enum
from pathlib import Path

# Add script directory to path to allow importing sibling modules
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.append(str(SCRIPT_DIR))

try:
    from conversation_archaeology import ChatLogAnalyzer, ConversationArchaeologist
except ImportError as e:
    print(f"[WARN] conversation_archaeology.py not importable: {e}. Friction analysis disabled.")
    ChatLogAnalyzer = None
    ConversationArchaeologist = None

# Base paths
AGENT_DIR = Path(__file__).parent.parent.parent  # .agent/
PROJECTS_DIR = AGENT_DIR / 'projects'
GLOBAL_REGISTRY_PATH = AGENT_DIR / 'global_mistakes.json'
CURRENT_PROJECT_FILE = AGENT_DIR / 'current_project.txt'

def get_current_project() -> Optional[str]:
    """Get the currently active project name."""
    if CURRENT_PROJECT_FILE.exists():
        return CURRENT_PROJECT_FILE.read_text().strip()
    return None

def set_current_project(name: str):
    """Set the currently active project."""
    CURRENT_PROJECT_FILE.write_text(name)

def get_project_path(project_name: str = None) -> Path:
    """Get path to a project folder. Uses current project if none specified."""
    if project_name is None:
        project_name = get_current_project()
    if project_name is None:
        # Fallback to workspace root for backwards compatibility
        return Path('.')
    return PROJECTS_DIR / project_name

def get_db_path(project_name: str = None) -> Path:
    """Get tasks.json path for a project."""
    return get_project_path(project_name) / 'tasks.json'

def get_markdown_path(project_name: str = None) -> Path:
    """Get task.md path for a project."""
    return get_project_path(project_name) / 'task.md'

def get_lessons_path(project_name: str = None) -> Path:
    """Get lessons_learned.md path for a project."""
    return get_project_path(project_name) / 'lessons_learned.md'

def get_goals_path(project_name: str = None) -> Path:
    """Get goal_analysis.md path for a project."""
    return get_project_path(project_name) / 'goal_analysis.md'


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    FAILED = "failed"
    SKIPPED = "skipped"
    BLOCKED = "blocked"

class Task:
    def __init__(self, 
                 index: int, 
                 description: str, 
                 task_id: Optional[str] = None,
                 status: TaskStatus = TaskStatus.TODO,
                 data: Optional[Dict] = None,
                 validation: Optional[Dict] = None,
                 rules: Optional[List[str]] = None,
                 logs: Optional[List[str]] = None,
                 lessons_learned: Optional[List[str]] = None,
                 depends_on: Optional[List[int]] = None,
                 priority: int = 0,
                 tags: Optional[List[str]] = None,
                 reasoning_trace: Optional[List[str]] = None,
                 auto_linked_mistakes: Optional[List[str]] = None,
                 postmortem: Optional[Dict] = None):
        
        self.index = index
        self.id = task_id or f"task_{index}"
        self.description = description
        self.status = status if isinstance(status, TaskStatus) else TaskStatus(status)
        self.data = data
        self.validation = validation or {"criteria": [], "examples": []}
        self.rules = rules or []
        self.logs = logs or []
        self.lessons_learned = lessons_learned or []
        self.depends_on = depends_on or []
        self.priority = priority
        self.tags = tags or []
        self.reasoning_trace = reasoning_trace or []
        self.auto_linked_mistakes = auto_linked_mistakes or []
        self.postmortem = postmortem or {"passes": [], "root_cause": None}

    def log(self, message: str):
        timestamp = datetime.now().isoformat()
        self.logs.append(f"[{timestamp}] {message}")

    def reason(self, message: str):
        """Log a reasoning/decision trace entry."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.reasoning_trace.append(f"[{timestamp}] {message}")

    def to_dict(self) -> Dict:
        return {
            "index": self.index,
            "id": self.id,
            "description": self.description,
            "status": self.status.value,
            "data": self.data,
            "validation": self.validation,
            "rules": self.rules,
            "logs": self.logs,
            "lessons_learned": self.lessons_learned,
            "depends_on": self.depends_on,
            "priority": self.priority,
            "tags": self.tags,
            "reasoning_trace": self.reasoning_trace,
            "auto_linked_mistakes": self.auto_linked_mistakes,
            "postmortem": self.postmortem
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        return cls(
            index=data.get("index", 0),
            description=data.get("description", ""),
            task_id=data.get("id"),
            status=data.get("status", TaskStatus.TODO),
            data=data.get("data"),
            validation=data.get("validation"),
            rules=data.get("rules"),
            logs=data.get("logs"),
            lessons_learned=data.get("lessons_learned"),
            depends_on=data.get("depends_on"),
            priority=data.get("priority", 0),
            tags=data.get("tags"),
            reasoning_trace=data.get("reasoning_trace"),
            auto_linked_mistakes=data.get("auto_linked_mistakes"),
            postmortem=data.get("postmortem")
        )


class TaskEngine:
    def __init__(self, project_name: str = None):
        """Initialize engine for a specific project or current project."""
        self.project_name = project_name or get_current_project()
        self.project_path = get_project_path(self.project_name)
        self.db_path = get_db_path(self.project_name)
        self.markdown_path = get_markdown_path(self.project_name)
        
        self.global_context: Dict = {
            "project_name": "New Project",
            "project_rules": [],
            "current_focus": "Initialization",
            "current_task_index": None,
            "mistakes_registry": [],
            "fuckup_prevention_checklist": [
                "Did I read the requirements fully?",
                "Did I check the mistake registry?",
                "Did I validate the output format?",
                "Did I log my reasoning?"
            ]
        }
        self.tasks: List[Task] = []

    def load(self):
        if not os.path.exists(self.db_path):
            print(f"[WARN] No database found at {self.db_path}. Initializing new.", file=sys.stderr)
            return
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
                self.global_context = raw_data.get("global_context", self.global_context)
                self.tasks = [Task.from_dict(t) for t in raw_data.get("tasks", [])]
        except Exception as e:
            print(f"[ERROR] Loading database: {e}", file=sys.stderr)
            sys.exit(1)

    def save(self):
        self._auto_link_mistakes()  # Run semantic linking before save
        data = {
            "global_context": self.global_context,
            "tasks": [t.to_dict() for t in self.tasks]
        }
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        self.render_markdown()

    # ========== SEMANTIC ERROR LINKING ==========

    def _auto_link_mistakes(self):
        """Auto-link mistakes to tasks based on tag overlap."""
        for task in self.tasks:
            task_tags = set(task.tags)
            linked = []
            for m in self.global_context.get("mistakes_registry", []):
                mistake_tags = set(m.get("tags", []))
                if task_tags & mistake_tags:  # Intersection
                    if m["id"] not in linked:
                        linked.append(m["id"])
            task.auto_linked_mistakes = linked

    def add_mistake(self, name: str, structure: str, example: str, tags: List[str] = None):
        mid = f"M{len(self.global_context['mistakes_registry']) + 1:03d}"
        entry = {
            "id": mid,
            "name": name,
            "structure": structure,
            "example": example,
            "tags": tags or [],
            "linked_tasks": [],
            "timestamp": datetime.now().isoformat()
        }
        self.global_context["mistakes_registry"].append(entry)
        self.save()
        print(f"[OK] Registered mistake {mid}: {name}")
        if tags:
            print(f"     Tags: {', '.join(tags)}")

    def link_mistake_to_task(self, mistake_id: str, task_idx: int):
        """Explicitly link a mistake to a task."""
        for m in self.global_context["mistakes_registry"]:
            if m["id"] == mistake_id:
                if task_idx not in m["linked_tasks"]:
                    m["linked_tasks"].append(task_idx)
                break
        self.save()

    def get_mistakes_for_task(self, task: Task) -> List[Dict]:
        """Get all mistakes linked to a task (explicit + auto via tags)."""
        result = []
        for m in self.global_context.get("mistakes_registry", []):
            if m["id"] in task.auto_linked_mistakes:
                result.append(m)
            elif task.index in m.get("linked_tasks", []):
                result.append(m)
        return result

    # ========== CONTEXTUAL START ==========

    def start_task(self, index: int):
        """Contextual Start: Shows future context, pitfall scan, and pre-flight checklist."""
        task = self.get_task(index)
        if not task:
            print(f"[ERROR] Invalid task index: {index}", file=sys.stderr)
            return

        task.status = TaskStatus.IN_PROGRESS
        task.log("Started work.")
        self.global_context["current_task_index"] = index
        self.global_context["current_focus"] = task.description
        self.save()

        # === CONTEXTUAL START OUTPUT ===
        print("\n" + "="*60)
        print(f"[STARTING TASK {index}] {task.description}")
        print("="*60)

        # Future Context
        downstream = self._get_downstream_tasks(index)
        if downstream:
            print("\n[FUTURE CONTEXT] Downstream tasks that depend on this:")
            for dt in downstream:
                print(f"   [{dt.index}] {dt.description}")

        # Pitfall Scan
        linked_mistakes = self.get_mistakes_for_task(task)
        if linked_mistakes:
            print("\n[PITFALL SCAN] Watch for these based on tags/history:")
            for m in linked_mistakes:
                print(f"   [X] {m['name']}: {m['structure']}")

        # Pre-flight Checklist
        print("\n[PRE-FLIGHT CHECKLIST]")
        for item in self.global_context.get("fuckup_prevention_checklist", []):
            print(f"   [ ] {item}")

        print("="*60 + "\n")

    def _get_downstream_tasks(self, index: int) -> List[Task]:
        """Get tasks that depend on the given task."""
        return [t for t in self.tasks if index in t.depends_on]

    # ========== REASONING TRACE ==========

    def add_reasoning(self, index: int, message: str):
        """Add a reasoning trace entry to a task."""
        task = self.get_task(index)
        if task:
            task.reason(message)
            self.save()
            print(f"[TRACE] Logged: {message}")

    def view_reasoning(self, index: int):
        """View the reasoning trace for a task."""
        task = self.get_task(index)
        if task:
            print(f"\n[REASONING TRACE] Task {index}: {task.description}")
            if task.reasoning_trace:
                for entry in task.reasoning_trace:
                    print(f"   {entry}")
            else:
                print("   (No reasoning logged)")

    # ========== POSTMORTEM ANALYSIS ==========

    def postmortem(self, index: int, hypothesis: str = None):
        """Run or add to postmortem analysis for a failed task."""
        task = self.get_task(index)
        if not task:
            print(f"[ERROR] Task {index} not found", file=sys.stderr)
            return

        if hypothesis:
            # Add a new analysis pass
            pass_num = len(task.postmortem["passes"]) + 1
            task.postmortem["passes"].append({
                "depth": pass_num,
                "hypothesis": hypothesis,
                "timestamp": datetime.now().isoformat()
            })
            task.log(f"Postmortem pass {pass_num}: {hypothesis}")
            self.save()
            print(f"[POSTMORTEM] Added pass {pass_num}: {hypothesis}")
        else:
            # Display postmortem
            print(f"\n[POSTMORTEM ANALYSIS] Task {index}: {task.description}")
            print(f"Status: {task.status.value}")
            
            if task.reasoning_trace:
                print("\n[REASONING TRACE]")
                for entry in task.reasoning_trace:
                    print(f"   {entry}")

            if task.postmortem["passes"]:
                print("\n[ANALYSIS PASSES]")
                for p in task.postmortem["passes"]:
                    print(f"   Pass {p['depth']}: {p['hypothesis']}")
            
            if task.postmortem.get("root_cause"):
                print(f"\n[ROOT CAUSE] {task.postmortem['root_cause']}")
            else:
                print("\n[ROOT CAUSE] Not yet determined")

    def set_root_cause(self, index: int, cause: str):
        """Set the root cause for a failed task."""
        task = self.get_task(index)
        if task:
            task.postmortem["root_cause"] = cause
            task.log(f"Root cause identified: {cause}")
            self.save()
            print(f"[OK] Root cause set: {cause}")

    # ========== TASK CRUD ==========

    def add_task(self, description: str, data: Optional[str] = None, 
                 priority: int = 0, tags: List[str] = None, depends_on: List[int] = None):
        next_idx = len(self.tasks)
        new_task = Task(
            index=next_idx, 
            description=description, 
            data={"raw": data} if data else None,
            priority=priority,
            tags=tags or [],
            depends_on=depends_on or []
        )
        new_task.log("Task created.")
        self.tasks.append(new_task)
        self.save()
        print(f"[OK] Added task [{next_idx}] {description}")
        if tags:
            print(f"     Tags: {', '.join(tags)}")
        if new_task.auto_linked_mistakes:
            print(f"     [!] Auto-linked to mistakes: {', '.join(new_task.auto_linked_mistakes)}")
        return new_task

    def tag_task(self, index: int, tags: List[str]):
        """Add tags to a task."""
        task = self.get_task(index)
        if task:
            task.tags.extend([t for t in tags if t not in task.tags])
            self.save()
            print(f"[OK] Task {index} tagged: {', '.join(task.tags)}")
            if task.auto_linked_mistakes:
                print(f"     [!] Now linked to: {', '.join(task.auto_linked_mistakes)}")

    def complete_task(self, index: int, lessons: Optional[str] = None):
        task = self.get_task(index)
        if task:
            task.status = TaskStatus.DONE
            task.log("Marked as DONE.")
            if lessons:
                task.lessons_learned.append(lessons)
                task.log(f"Lesson learned: {lessons}")
            self.save()
            print(f"[OK] Task {index} completed.")
        else:
            print(f"[ERROR] Invalid task index: {index}", file=sys.stderr)

    def fail_task(self, index: int, reason: str):
        task = self.get_task(index)
        if task:
            task.status = TaskStatus.FAILED
            task.log(f"FAILED: {reason}")
            self.save()
            print(f"[FAIL] Task {index} failed: {reason}")
            print("       Use 'postmortem <idx> \"hypothesis\"' to analyze.")

    def block_task(self, index: int, reason: str):
        task = self.get_task(index)
        if task:
            task.status = TaskStatus.BLOCKED
            task.log(f"BLOCKED: {reason}")
            self.save()
            print(f"[BLOCKED] Task {index}: {reason}")

    # ========== GETTERS ==========

    def get_task(self, index: int) -> Optional[Task]:
        if 0 <= index < len(self.tasks):
            return self.tasks[index]
        return None

    def get_next(self) -> Optional[Task]:
        done_indices = {t.index for t in self.tasks if t.status == TaskStatus.DONE}
        for task in sorted(self.tasks, key=lambda t: (-t.priority, t.index)):
            if task.status == TaskStatus.TODO:
                if all(dep in done_indices for dep in task.depends_on):
                    return task
        return None

    def get_current(self) -> Optional[Task]:
        idx = self.global_context.get("current_task_index")
        if idx is not None:
            return self.get_task(idx)
        for task in self.tasks:
            if task.status == TaskStatus.IN_PROGRESS:
                return task
        return None

    def get_future_tasks(self) -> List[Task]:
        return [t for t in self.tasks if t.status == TaskStatus.TODO]

    def get_past_tasks(self) -> List[Task]:
        return [t for t in self.tasks if t.status == TaskStatus.DONE]

    def get_failed_tasks(self) -> List[Task]:
        return [t for t in self.tasks if t.status == TaskStatus.FAILED]

    def get_blocked_tasks(self) -> List[Task]:
        return [t for t in self.tasks if t.status == TaskStatus.BLOCKED]

    def get_mistakes(self) -> List[Dict]:
        return self.global_context.get("mistakes_registry", [])

    def get_rules(self) -> List[str]:
        return self.global_context.get("project_rules", [])

    # ========== RULES & FOCUS ==========

    def add_rule(self, rule: str):
        self.global_context["project_rules"].append(rule)
        self.save()
        print(f"[OK] Added rule: {rule}")

    def set_focus(self, focus: str):
        self.global_context["current_focus"] = focus
        self.save()
        print(f"[OK] Focus set to: {focus}")

    # ========== PRIORITY REORDERING ==========

    def reorder_by_dependencies(self):
        """
        Auto-reprioritize tasks based on dependency graph.
        
        Priority calculation:
        - Base: original priority
        - Bonus: +10 for each task that depends on this one (critical path)
        - Bonus: +5 if no unresolved dependencies (ready to start)
        - Penalty: -20 if blocked or failed
        - Penalty: -10 per unresolved dependency
        """
        print("\n[REORDER] Analyzing dependency graph...")
        
        done_indices = {t.index for t in self.tasks if t.status == TaskStatus.DONE}
        
        # Count how many tasks depend on each task
        dependents_count = {t.index: 0 for t in self.tasks}
        for task in self.tasks:
            for dep in task.depends_on:
                if dep in dependents_count:
                    dependents_count[dep] += 1
        
        changes = []
        for task in self.tasks:
            if task.status in [TaskStatus.DONE, TaskStatus.SKIPPED]:
                continue  # Skip completed tasks
            
            old_priority = task.priority
            new_priority = old_priority
            
            # Bonus: Critical path (many tasks depend on this)
            deps_on_me = dependents_count[task.index]
            if deps_on_me > 0:
                new_priority += deps_on_me * 10
            
            # Bonus: Ready to start (all dependencies resolved)
            unresolved = [d for d in task.depends_on if d not in done_indices]
            if len(unresolved) == 0 and task.depends_on:
                new_priority += 5  # Was blocked, now unblocked
            elif len(unresolved) == 0:
                new_priority += 3  # No dependencies at all
            
            # Penalty: Unresolved dependencies
            new_priority -= len(unresolved) * 10
            
            # Penalty: Blocked or failed
            if task.status == TaskStatus.BLOCKED:
                new_priority -= 20
            elif task.status == TaskStatus.FAILED:
                new_priority -= 20
            
            if new_priority != old_priority:
                changes.append({
                    "index": task.index,
                    "desc": task.description[:40],
                    "old": old_priority,
                    "new": new_priority,
                    "reason": f"deps_on_me={deps_on_me}, unresolved={len(unresolved)}"
                })
                task.priority = new_priority
                task.log(f"Priority adjusted: {old_priority} → {new_priority}")
        
        self.save()
        
        # Report changes
        print(f"[REORDER] Adjusted {len(changes)} task priorities:")
        for c in sorted(changes, key=lambda x: -x["new"])[:10]:
            direction = "^" if c["new"] > c["old"] else "v"
            print(f"   [{c['index']}] {c['desc']}... {c['old']} {direction} {c['new']}")
        
        # Show new recommended order
        print("\n[RECOMMENDED ORDER]")
        ready = [t for t in self.tasks if t.status == TaskStatus.TODO]
        ready_sorted = sorted(ready, key=lambda t: (-t.priority, t.index))
        for i, t in enumerate(ready_sorted[:5], 1):
            deps_str = f" (blocked by {t.depends_on})" if any(d not in done_indices for d in t.depends_on) else ""
            print(f"   {i}. [{t.index}] {t.description[:50]}... (P:{t.priority}){deps_str}")
        
        print()

    # ========== STATE DUMP & STATUS ==========

    def dump_state(self) -> Dict:
        return {
            "global_context": self.global_context,
            "tasks": [t.to_dict() for t in self.tasks],
            "summary": {
                "total": len(self.tasks),
                "todo": len(self.get_future_tasks()),
                "done": len(self.get_past_tasks()),
                "failed": len(self.get_failed_tasks()),
                "blocked": len(self.get_blocked_tasks()),
                "mistakes_count": len(self.get_mistakes()),
                "rules_count": len(self.get_rules())
            }
        }

    def print_status(self):
        state = self.dump_state()
        summary = state["summary"]
        
        print("\n" + "="*60)
        print(f"[PROJECT] {self.global_context.get('project_name', 'Unknown')}")
        print(f"[FOCUS] {self.global_context.get('current_focus', 'None')}")
        print("="*60)
        print(f"\n[TASK SUMMARY]")
        print(f"   Total: {summary['total']}")
        print(f"   [DONE] {summary['done']}")
        print(f"   [TODO] {summary['todo']}")
        print(f"   [FAIL] {summary['failed']}")
        print(f"   [BLOCK] {summary['blocked']}")
        
        current = self.get_current()
        if current:
            print(f"\n[CURRENT] [{current.index}] {current.description}")
        
        next_task = self.get_next()
        if next_task:
            print(f"[NEXT] [{next_task.index}] {next_task.description}")
        
        print(f"\n[WARN] Mistakes Registered: {summary['mistakes_count']}")
        print(f"[RULES] Active: {summary['rules_count']}")
        print("="*60 + "\n")

    def scan_links(self):
        """Re-scan all tasks and show auto-linked mistakes."""
        self._auto_link_mistakes()
        self.save()
        print("[SCAN COMPLETE] Auto-linked mistakes by tag overlap:")
        for task in self.tasks:
            if task.auto_linked_mistakes:
                print(f"   [{task.index}] {task.description}")
                print(f"       Linked: {', '.join(task.auto_linked_mistakes)}")

    # ========== GLOBAL REGISTRY (CROSS-CONVERSATION) ==========

    def load_global_registry(self) -> Dict:
        """Load the global mistakes registry (persists across conversations)."""
        if GLOBAL_REGISTRY_PATH.exists():
            try:
                with open(GLOBAL_REGISTRY_PATH, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {"mistakes": [], "lessons": [], "patterns": [], "rules": []}

    def save_global_registry(self, registry: Dict):
        """Save the global mistakes registry."""
        registry["last_updated"] = datetime.now().isoformat()
        registry["mistake_count"] = len(registry.get("mistakes", []))
        with open(GLOBAL_REGISTRY_PATH, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=4)

    def global_sync(self):
        """Sync local mistakes/lessons to global registry."""
        global_reg = self.load_global_registry()
        
        # Get existing IDs to avoid duplicates
        existing_ids = {m.get("id") for m in global_reg.get("mistakes", [])}
        
        # Sync local mistakes
        added = 0
        for m in self.global_context.get("mistakes_registry", []):
            if m.get("id") not in existing_ids:
                global_reg["mistakes"].append({
                    "id": m["id"],
                    "name": m["name"],
                    "structure": m["structure"],
                    "example": m.get("example", ""),
                    "tags": m.get("tags", []),
                    "source_project": self.global_context.get("project_name", "Unknown"),
                    "synced_at": datetime.now().isoformat()
                })
                existing_ids.add(m["id"])
                added += 1
        
        # Sync error analysis lessons if present
        error_analysis = self.global_context.get("error_analysis", {})
        for lesson in error_analysis.get("lessons_learned", []):
            lesson_text = lesson.get("lesson", "")
            if lesson_text and lesson_text not in [l.get("text") for l in global_reg.get("lessons", [])]:
                global_reg["lessons"].append({
                    "text": lesson_text,
                    "category": lesson.get("from_category", "general"),
                    "source_project": self.global_context.get("project_name", "Unknown"),
                    "synced_at": datetime.now().isoformat()
                })
        
        self.save_global_registry(global_reg)
        print(f"[SYNC] Added {added} new mistakes to global registry")
        print(f"       Total global mistakes: {len(global_reg['mistakes'])}")
        print(f"       Total global lessons: {len(global_reg['lessons'])}")

    def import_from_global(self):
        """Import global mistakes into local registry for this project."""
        global_reg = self.load_global_registry()
        existing_ids = {m.get("id") for m in self.global_context.get("mistakes_registry", [])}
        
        imported = 0
        for m in global_reg.get("mistakes", []):
            if m.get("id") not in existing_ids:
                self.global_context["mistakes_registry"].append({
                    "id": m["id"],
                    "name": m["name"],
                    "structure": m["structure"],
                    "example": m.get("example", ""),
                    "tags": m.get("tags", []),
                    "linked_tasks": [],
                    "timestamp": m.get("synced_at", datetime.now().isoformat())
                })
                imported += 1
        
        self.save()
        print(f"[IMPORT] Imported {imported} mistakes from global registry")

    # ========== PRE-FLIGHT & LESSONS ==========

    def preflight(self):
        """Mandatory pre-flight check: displays lessons, warnings, and checklist."""
        print("\n" + "="*60)
        print("[PRE-FLIGHT CHECK] Review before starting ANY work")
        print("="*60)
        
        # 1. Global Lessons
        global_reg = self.load_global_registry()
        lessons = global_reg.get("lessons", [])
        if lessons:
            print("\n[LESSONS FROM PAST PROJECTS]")
            for i, lesson in enumerate(lessons[:5], 1):
                cat = lesson.get("category", "general").upper()
                print(f"   {i}. [{cat}] {lesson['text']}")
        
        # 2. Local Error Analysis
        error_analysis = self.global_context.get("error_analysis", {})
        if error_analysis.get("recommendations"):
            print("\n[RECOMMENDATIONS FOR THIS PROJECT]")
            for rec in error_analysis["recommendations"][:3]:
                cat = rec.get("category", "").upper()
                print(f"   -> [{cat}] {rec['recommendation']}")
        
        # 3. Mistake Count Warning
        local_mistakes = len(self.get_mistakes())
        global_mistakes = len(global_reg.get("mistakes", []))
        if local_mistakes > 0 or global_mistakes > 0:
            print(f"\n[WARNING] Mistake registries active:")
            print(f"   Local: {local_mistakes} | Global: {global_mistakes}")
        
        # 4. Pre-flight Checklist
        print("\n[CHECKLIST]")
        for item in self.global_context.get("fuckup_prevention_checklist", []):
            print(f"   [ ] {item}")
        
        print("\n[TIP] Use 'start <idx>' to begin with full context awareness")
        print("="*60 + "\n")

    def show_lessons(self):
        """Display all lessons from local and global sources."""
        print("\n[LESSONS LEARNED]")
        
        # Local lessons from error analysis
        error_analysis = self.global_context.get("error_analysis", {})
        local_lessons = error_analysis.get("lessons_learned", [])
        if local_lessons:
            print("\n--- This Project ---")
            for lesson in local_lessons:
                cat = lesson.get("from_category", "general")
                print(f"   [{cat.upper()}] {lesson['lesson']}")
        
        # Global lessons
        global_reg = self.load_global_registry()
        global_lessons = global_reg.get("lessons", [])
        if global_lessons:
            print("\n--- From All Projects ---")
            for lesson in global_lessons:
                cat = lesson.get("category", "general")
                src = lesson.get("source_project", "Unknown")[:20]
                print(f"   [{cat.upper()}] {lesson['text']}")
        
        if not local_lessons and not global_lessons:
            print("   (No lessons recorded yet)")

    def show_goals(self):
        """Display goal analysis from registry with status tracking."""
        goal_analysis = self.global_context.get("goal_analysis", {})
        
        if not goal_analysis or not goal_analysis.get("primary_goal"):
            print("[INFO] No goal analysis found. Run archaeology first.")
            return
        
        print("\n" + "="*60)
        print("[GOAL ANALYSIS]")
        print("="*60)
        
        print(f"\n[PRIMARY GOAL] {goal_analysis['primary_goal']}")
        print(f"[TYPE] {goal_analysis.get('goal_type', 'general')}")
        print(f"[COMPLEXITY] {goal_analysis.get('complexity_score', 0)}/10")
        
        # Sub-goals with status
        if goal_analysis.get("sub_goals"):
            print("\n[SUB-GOALS]")
            done = 0
            total = len(goal_analysis["sub_goals"])
            for i, sg in enumerate(goal_analysis["sub_goals"], 1):
                status = sg.get("status", "pending")
                checkbox = {"pending": "[ ]", "in_progress": "[/]", "done": "[x]", "failed": "[-]"}.get(status, "[ ]")
                linked = f" (tasks: {sg['linked_tasks']})" if sg.get("linked_tasks") else ""
                print(f"   {checkbox} {i}. {sg['description']}{linked}")
                if status == "done":
                    done += 1
            print(f"\n   Progress: {done}/{total} sub-goals complete")
        
        # Success criteria with status
        if goal_analysis.get("success_criteria"):
            print("\n[SUCCESS CRITERIA]")
            for i, criterion in enumerate(goal_analysis["success_criteria"]):
                if isinstance(criterion, dict):
                    status = criterion.get("status", "pending")
                    checkbox = {"pending": "[ ]", "met": "[x]", "failed": "[-]"}.get(status, "[ ]")
                    print(f"   {checkbox} {criterion.get('text', criterion)}")
                else:
                    print(f"   [ ] {criterion}")
        
        if goal_analysis.get("predicted_pitfalls"):
            print("\n[PREDICTED PITFALLS]")
            for pitfall in goal_analysis["predicted_pitfalls"][:5]:
                triggered = " <- TRIGGERED" if pitfall.get("triggered") else ""
                print(f"   [!] {pitfall['name']}: {pitfall['description']}{triggered}")
        
        if goal_analysis.get("scope_guards"):
            print("\n[SCOPE GUARDS]")
            for guard in goal_analysis["scope_guards"][:3]:
                print(f"   ? {guard}")
        
        print("="*60 + "\n")

    def update_subgoal(self, index: int, status: str, linked_tasks: List[int] = None):
        """Update a sub-goal's status and optionally link tasks."""
        goal_analysis = self.global_context.get("goal_analysis", {})
        sub_goals = goal_analysis.get("sub_goals", [])
        
        if index < 1 or index > len(sub_goals):
            print(f"[ERROR] Sub-goal {index} not found. Valid: 1-{len(sub_goals)}")
            return
        
        sg = sub_goals[index - 1]
        old_status = sg.get("status", "pending")
        sg["status"] = status
        
        if linked_tasks is not None:
            sg["linked_tasks"] = linked_tasks
        
        self.save()
        print(f"[OK] Sub-goal {index}: '{sg['description'][:40]}...'")
        print(f"     Status: {old_status} -> {status}")
        if linked_tasks:
            print(f"     Linked to tasks: {linked_tasks}")

    def link_task_to_subgoal(self, task_index: int, subgoal_index: int):
        """Link a task to a sub-goal for automatic status updates."""
        goal_analysis = self.global_context.get("goal_analysis", {})
        sub_goals = goal_analysis.get("sub_goals", [])
        
        if subgoal_index < 1 or subgoal_index > len(sub_goals):
            print(f"[ERROR] Sub-goal {subgoal_index} not found.")
            return
        
        task = self.get_task(task_index)
        if not task:
            print(f"[ERROR] Task {task_index} not found.")
            return
        
        sg = sub_goals[subgoal_index - 1]
        if "linked_tasks" not in sg:
            sg["linked_tasks"] = []
        
        if task_index not in sg["linked_tasks"]:
            sg["linked_tasks"].append(task_index)
        
        self.save()
        print(f"[OK] Linked task [{task_index}] to sub-goal {subgoal_index}")
        print(f"     Task: {task.description[:40]}...")
        print(f"     Sub-goal: {sg['description'][:40]}...")

    def sync_subgoal_status(self):
        """Auto-update sub-goal status based on linked task completion."""
        goal_analysis = self.global_context.get("goal_analysis", {})
        sub_goals = goal_analysis.get("sub_goals", [])
        
        updates = 0
        for sg in sub_goals:
            linked = sg.get("linked_tasks", [])
            if not linked:
                continue
            
            # Check linked task statuses
            statuses = []
            for task_idx in linked:
                task = self.get_task(task_idx)
                if task:
                    statuses.append(task.status)
            
            if not statuses:
                continue
            
            # Derive sub-goal status from task statuses
            if all(s == TaskStatus.DONE for s in statuses):
                new_status = "done"
            elif any(s == TaskStatus.FAILED for s in statuses):
                new_status = "failed"
            elif any(s == TaskStatus.IN_PROGRESS for s in statuses):
                new_status = "in_progress"
            else:
                new_status = "pending"
            
            if sg.get("status") != new_status:
                sg["status"] = new_status
                updates += 1
        
        if updates > 0:
            self.save()
            print(f"[SYNC] Updated {updates} sub-goal statuses from linked tasks")
        
        return updates

    def show_subgoals(self):
        """Show sub-goals with detailed status and linked tasks."""
        goal_analysis = self.global_context.get("goal_analysis", {})
        sub_goals = goal_analysis.get("sub_goals", [])
        
        if not sub_goals:
            print("[INFO] No sub-goals found. Run archaeology with --title first.")
            return
        
        # Sync status before display
        self.sync_subgoal_status()
        
        print("\n[SUB-GOALS STATUS]")
        print("-"*60)
        
        for i, sg in enumerate(sub_goals, 1):
            status = sg.get("status", "pending")
            checkbox = {"pending": "[ ]", "in_progress": "[/]", "done": "[x]", "failed": "[-]"}.get(status, "[ ]")
            print(f"\n{checkbox} {i}. {sg['description']}")
            
            linked = sg.get("linked_tasks", [])
            if linked:
                print(f"   Linked Tasks:")
                for task_idx in linked:
                    task = self.get_task(task_idx)
                    if task:
                        t_status = {"todo": "[ ]", "done": "[x]", "in_progress": "[/]", "failed": "[-]"}.get(task.status.value, "[ ]")
                        print(f"      {t_status} [{task.index}] {task.description[:40]}...")
            else:
                print(f"   (No linked tasks - use 'link <task_idx> <subgoal_idx>')")
        
        # Summary
        done = len([sg for sg in sub_goals if sg.get("status") == "done"])
        failed = len([sg for sg in sub_goals if sg.get("status") == "failed"])
        in_prog = len([sg for sg in sub_goals if sg.get("status") == "in_progress"])
        pending = len([sg for sg in sub_goals if sg.get("status", "pending") == "pending"])
        
        print("\n" + "-"*60)
        print(f"[SUMMARY] Done: {done} | In Progress: {in_prog} | Pending: {pending} | Failed: {failed}")
        print()

    def diagnose_friction(self, log_path: str):
        """Analyze a chat log and update tasks with friction data."""
        if not ChatLogAnalyzer:
            print("[ERROR] Conversation Archaeology module not available.")
            return
            
        path = Path(log_path)
        if not path.exists():
            print(f"[ERROR] Chat log file not found: {log_path}")
            return
            
        print(f"[DIAGNOSE] Analyzing chat log: {path.name}...")
        analyzer = ChatLogAnalyzer()
        
        # Parse turns
        turns = analyzer.parse_log(path)
        print(f"   Turns Parsed: {len(turns)}")
        if not turns:
            print("[WARN] No turns found. Check log format (User:/Model:).")
            return
            
        # Detect friction
        friction_events = analyzer.detect_friction(turns)
        print(f"   Friction Events: {len(friction_events)}")
        if not friction_events:
            print("[OK] No significant friction detected.")
            return
            
        # Correlate to current tasks
        print(f"[DIAGNOSE] Correlating to {len(self.tasks)} tasks...")
        simple_tasks = [{"index": t.index, "description": t.description} for t in self.tasks]
        correlations = analyzer.correlate_tasks(friction_events, simple_tasks)
        print(f"   Correlated Events: {len(correlations)}")
        
        # Update tasks
        updates = 0
        for corr in correlations:
            idx = corr["task_index"]
            event = corr["event"]
            task = self.get_task(idx)
            
            if not task: continue
            
            # Add log entry
            log_entry = f"[FRICTION] Turn {event['turn_index']} (Score: {event['score']}): {event['text']}..."
            
            # Check if this exact log already exists to avoid duplicates
            if log_entry not in task.logs:
                task.logs.append(log_entry)
                updates += 1
                
            # If high score, mark as struggled
            if event["score"] >= 2:
                if "struggled" not in task.tags:
                    task.tags.append("struggled")
                    updates += 1
                    
        if updates > 0:
            self.save()
            print(f"[OK] Updated {updates} tasks with friction logs.")
            print("   (Check task.md for '[!]' indicators)")
        else:
            print("[INFO] No new friction maps to current tasks.")

    def catchup(self, log_path: str, conv_id: str = None, brain_path: str = None):
        """Full state catch-up: Analyze artifacts + chat log -> Regenerate tasks.json."""
        if not ConversationArchaeologist:
            print("[ERROR] Conversation Archaeology module not available.")
            return

        path = Path(log_path)
        if not path.exists():
            print(f"[ERROR] Chat log file not found: {log_path}")
            return
            
        print(f"[CATCHUP] Starting full state reconstruction from {path.name}...")
        
        # Determine brain dir
        brain_dir = Path(brain_path) if brain_path else None
        if not brain_dir or not brain_dir.exists():
             brain_dir = self.project_dir.parent.parent.parent # .agent/projects/.. -> root
             if "brain" not in str(brain_dir) and "VFT Docs" in str(self.project_dir):
                  # Heuristic for VFT Docs root vs brain dir
                  brain_dir = Path(os.getcwd())
        
        # Initialize Archaeologist
        archaeologist = ConversationArchaeologist(str(brain_dir))
        
        # Determine Conversation ID
        if not conv_id:
             conv_id = Path.cwd().name # Assume current folder is the conversation
        
        # Run bootstrap
        print(f"[CATCHUP] Bootstrap analyzing {conv_id}...")
        registry = archaeologist.bootstrap_from_conversation(
            conversation_id=conv_id, 
            conversation_title=self.global_context.get("project_name"),
            chat_log_path=str(path),
            output_path="tasks.json" # Overwrite current tasks.json
        )
        
        # Reload engine
        self.load()
        print(f"[SUCCESS] Caught up! State synchronized with chat log & artifacts.")
        print(f"Tasks: {len(self.tasks)} | Friction events logged.")

    def render_markdown(self):
        lines = []
        lines.append(f"# {self.global_context.get('project_name', 'Task List')}")
        lines.append("")
        
        focus = self.global_context.get('current_focus')
        if focus:
            lines.append(f"**Current Focus**: {focus}")
            lines.append("")

        summary = self.dump_state()["summary"]
        lines.append(f"**Progress**: {summary['done']}/{summary['total']} complete")
        lines.append("")

        lines.append("## Task List")
        for task in self.tasks:
            checkbox = {"todo": "[ ]", "done": "[x]", "in_progress": "[/]", 
                       "failed": "[-]", "blocked": "[!]", "skipped": "[~]"}.get(task.status.value, "[ ]")
            tag_str = f" `{' '.join(task.tags)}`" if task.tags else ""
            friction = " ⚠️" if "struggled" in task.tags else ""
            line = f"- {checkbox} {task.description}{tag_str}{friction} <!-- id: {task.index} -->"
            lines.append(line)
        
        rules = self.get_rules()
        if rules:
            lines.append("")
            lines.append("## Project Rules")
            for r in rules:
                lines.append(f"- {r}")

        lines.append("")
        lines.append("## Mistake Registry")
        for m in self.get_mistakes():
            mid = m.get('id', 'LEGACY')
            tag_str = f" [{', '.join(m.get('tags', []))}]" if m.get('tags') else ""
            lines.append(f"> [!WARNING] {mid}: {m['name']}{tag_str}")
            lines.append(f"> **Structure**: {m['structure']}")
            lines.append(f"> **Example**: {m['example']}")
            lines.append(">")

        with open(self.markdown_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))

# ========== PROJECT MANAGEMENT ==========

def list_projects() -> List[str]:
    """List all projects."""
    if not PROJECTS_DIR.exists():
        return []
    return [d.name for d in PROJECTS_DIR.iterdir() if d.is_dir()]

def create_project(name: str, title: str = None):
    """Create a new project folder and initialize it."""
    project_path = PROJECTS_DIR / name
    project_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize empty tasks.json
    tasks_file = project_path / 'tasks.json'
    if not tasks_file.exists():
        initial_data = {
            "global_context": {
                "project_name": title or name,
                "project_rules": [],
                "current_focus": "Project Start",
                "current_task_index": None,
                "mistakes_registry": [],
                "fuckup_prevention_checklist": [
                    "Did I read the requirements fully?",
                    "Did I check the mistake registry?",
                    "Did I validate the output format?",
                    "Did I log my reasoning?"
                ]
            },
            "tasks": []
        }
        with open(tasks_file, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, indent=4)
    
    # Set as current project
    set_current_project(name)
    print(f"[OK] Created project: {name}")
    print(f"     Path: {project_path}")
    print(f"[OK] Set as current project")

def switch_project(name: str):
    """Switch to an existing project."""
    project_path = PROJECTS_DIR / name
    if not project_path.exists():
        print(f"[ERROR] Project '{name}' not found. Use 'project create {name}' first.")
        return False
    set_current_project(name)
    print(f"[OK] Switched to project: {name}")
    return True

def show_projects():
    """Show all projects and current project."""
    current = get_current_project()
    projects = list_projects()
    
    print("\n[PROJECTS]")
    if not projects:
        print("   (No projects yet. Use 'project create <name>' to start)")
    else:
        for p in projects:
            marker = " <- CURRENT" if p == current else ""
            proj_path = PROJECTS_DIR / p / 'tasks.json'
            if proj_path.exists():
                try:
                    with open(proj_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    task_count = len(data.get("tasks", []))
                    done_count = len([t for t in data.get("tasks", []) if t.get("status") == "done"])
                    print(f"   [{p}] {done_count}/{task_count} tasks done{marker}")
                except:
                    print(f"   [{p}] (error reading){marker}")
            else:
                print(f"   [{p}] (no tasks.json){marker}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="No More Fuckups Task Engine v5",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  project create <name>   Create new project folder
  project switch <name>   Switch to existing project
  project list            List all projects
  project current         Show current project
  
  init                    Initialize empty registry
  preflight               MANDATORY: Show lessons, warnings, checklist
  add <desc>              Add task (--tags t1,t2 --depends 1,2)
  start <idx>             Contextual start with pitfall scan
  done <idx>              Complete task (--lessons "...")
  fail <idx> <reason>     Mark failed
  
  reorder                 Auto-prioritize by dependencies
  global_sync             Sync local mistakes to global registry
  import_global           Import global mistakes to local
  lessons                 Show all lessons (local + global)
  goals                   Show goal analysis
  
  subgoals                Show sub-goals with status
  subgoal <n> done/fail   Update sub-goal status
  link <task> <subgoal>   Link task to sub-goal
  
  tag <idx> t1,t2         Add tags to task
  scan                    Re-scan and auto-link mistakes
  
  reason <idx> "msg"      Add reasoning trace entry
  trace <idx>             View reasoning trace
  postmortem <idx>        View postmortem analysis
  postmortem <idx> "hyp"  Add analysis hypothesis
  rootcause <idx> "cause" Set root cause
  
  mistake "n" "s" "e"     Register mistake (--tags t1,t2)
  mistakes                List all mistakes
  warnings <idx>          Show linked mistakes for task
  
  next / current / status / dump / future / past / rules
        """
    )
    subparsers = parser.add_subparsers(dest="command")

    # Project commands
    project_p = subparsers.add_parser("project")
    project_sub = project_p.add_subparsers(dest="project_cmd")
    
    proj_create = project_sub.add_parser("create")
    proj_create.add_argument("name", type=str)
    proj_create.add_argument("--title", type=str)
    
    proj_switch = project_sub.add_parser("switch")
    proj_switch.add_argument("name", type=str)
    
    project_sub.add_parser("list")
    project_sub.add_parser("current")

    subparsers.add_parser("init")

    add_p = subparsers.add_parser("add")
    add_p.add_argument("description", type=str)
    add_p.add_argument("--data", type=str)
    add_p.add_argument("--priority", type=int, default=0)
    add_p.add_argument("--tags", type=str, help="Comma-separated tags")
    add_p.add_argument("--depends", type=str, help="Comma-separated task indices")

    start_p = subparsers.add_parser("start")
    start_p.add_argument("index", type=int)

    done_p = subparsers.add_parser("done")
    done_p.add_argument("index", type=int)
    done_p.add_argument("--lessons", type=str)

    fail_p = subparsers.add_parser("fail")
    fail_p.add_argument("index", type=int)
    fail_p.add_argument("reason", type=str)

    block_p = subparsers.add_parser("block")
    block_p.add_argument("index", type=int)
    block_p.add_argument("reason", type=str)

    tag_p = subparsers.add_parser("tag")
    tag_p.add_argument("index", type=int)
    tag_p.add_argument("tags", type=str, help="Comma-separated tags")

    subparsers.add_parser("scan")

    reason_p = subparsers.add_parser("reason")
    reason_p.add_argument("index", type=int)
    reason_p.add_argument("message", type=str)

    trace_p = subparsers.add_parser("trace")
    trace_p.add_argument("index", type=int)

    pm_p = subparsers.add_parser("postmortem")
    pm_p.add_argument("index", type=int)
    pm_p.add_argument("hypothesis", type=str, nargs="?")

    rc_p = subparsers.add_parser("rootcause")
    rc_p.add_argument("index", type=int)
    rc_p.add_argument("cause", type=str)

    mistake_p = subparsers.add_parser("mistake")
    mistake_p.add_argument("name", type=str)
    mistake_p.add_argument("structure", type=str)
    mistake_p.add_argument("example", type=str)
    mistake_p.add_argument("--tags", type=str, help="Comma-separated tags")

    subparsers.add_parser("mistakes")

    warn_p = subparsers.add_parser("warnings")
    warn_p.add_argument("index", type=int)

    get_p = subparsers.add_parser("get")
    get_p.add_argument("index", type=int)

    subparsers.add_parser("next")
    subparsers.add_parser("current")
    subparsers.add_parser("future")
    subparsers.add_parser("past")
    subparsers.add_parser("status")
    subparsers.add_parser("dump")
    subparsers.add_parser("rules")
    
    # New v4 commands
    subparsers.add_parser("preflight")
    subparsers.add_parser("global_sync")
    subparsers.add_parser("import_global")
    subparsers.add_parser("lessons")
    subparsers.add_parser("goals")
    subparsers.add_parser("reorder")
    
    # Sub-goal commands
    subparsers.add_parser("subgoals")
    
    subgoal_p = subparsers.add_parser("subgoal")
    subgoal_p.add_argument("index", type=int, help="Sub-goal index (1-based)")
    subgoal_p.add_argument("status", type=str, choices=["pending", "in_progress", "done", "failed"])
    
    link_p = subparsers.add_parser("link")
    link_p.add_argument("task_index", type=int, help="Task index")
    link_p.add_argument("subgoal_index", type=int, help="Sub-goal index (1-based)")

    diagnose_p = subparsers.add_parser("diagnose")
    diagnose_p.add_argument("log_path", type=str, help="Path to chat log file")

    catchup_p = subparsers.add_parser("catchup")
    catchup_p.add_argument("log_path", type=str, help="Path to chat log file")
    catchup_p.add_argument("--id", type=str, help="Conversation ID", default=None)
    catchup_p.add_argument("--brain-dir", type=str, help="Path to brain artifacts", default=None)

    rule_p = subparsers.add_parser("rule")
    rule_p.add_argument("text", type=str)

    focus_p = subparsers.add_parser("focus")
    focus_p.add_argument("text", type=str)

    args = parser.parse_args()
    
    # Handle project commands first (before engine loads)
    if args.command == "project":
        if args.project_cmd == "create":
            create_project(args.name, args.title)
            return
        elif args.project_cmd == "switch":
            switch_project(args.name)
            return
        elif args.project_cmd == "list":
            show_projects()
            return
        elif args.project_cmd == "current":
            current = get_current_project()
            if current:
                print(f"[CURRENT PROJECT] {current}")
                print(f"[PATH] {get_project_path(current)}")
            else:
                print("[INFO] No project selected. Use 'project create <name>' or 'project switch <name>'")
            return
        else:
            parser.print_help()
            return
    
    engine = TaskEngine()
    engine.load()

    if args.command == "init":
        # Create project folder if needed
        if engine.project_name:
            engine.project_path.mkdir(parents=True, exist_ok=True)
        engine.save()
        print(f"[OK] Initialized task registry.")
        if engine.project_name:
            print(f"[PROJECT] {engine.project_name}")
            print(f"[PATH] {engine.project_path}")

    elif args.command == "add":
        tags = args.tags.split(",") if args.tags else None
        depends = [int(x) for x in args.depends.split(",")] if args.depends else None
        engine.add_task(args.description, args.data, args.priority, tags, depends)

    elif args.command == "start":
        engine.start_task(args.index)

    elif args.command == "done":
        engine.complete_task(args.index, args.lessons)

    elif args.command == "fail":
        engine.fail_task(args.index, args.reason)

    elif args.command == "block":
        engine.block_task(args.index, args.reason)

    elif args.command == "tag":
        tags = args.tags.split(",")
        engine.tag_task(args.index, tags)

    elif args.command == "scan":
        engine.scan_links()

    elif args.command == "reason":
        engine.add_reasoning(args.index, args.message)

    elif args.command == "trace":
        engine.view_reasoning(args.index)

    elif args.command == "postmortem":
        engine.postmortem(args.index, args.hypothesis)

    elif args.command == "rootcause":
        engine.set_root_cause(args.index, args.cause)

    elif args.command == "mistake":
        tags = args.tags.split(",") if args.tags else None
        engine.add_mistake(args.name, args.structure, args.example, tags)

    elif args.command == "mistakes":
        for m in engine.get_mistakes():
            tag_str = f" [{', '.join(m.get('tags', []))}]" if m.get('tags') else ""
            print(f"{m['id']}: {m['name']}{tag_str}")
            print(f"   Structure: {m['structure']}")
            print(f"   Example: {m['example']}")

    elif args.command == "warnings":
        task = engine.get_task(args.index)
        if task:
            warnings = engine.get_mistakes_for_task(task)
            if warnings:
                print(f"[WARNINGS for Task {args.index}]")
                for m in warnings:
                    print(f"   {m['id']}: {m['name']}")
            else:
                print("[INFO] No linked mistakes for this task.")

    elif args.command == "get":
        task = engine.get_task(args.index)
        if task:
            print(json.dumps(task.to_dict(), indent=2))

    elif args.command == "next":
        task = engine.get_next()
        if task:
            warnings = engine.get_mistakes_for_task(task)
            if warnings:
                print("[PITFALL SCAN]")
                for m in warnings:
                    print(f"   [X] {m['name']}: {m['structure']}")
                print()
            print(f"NEXT: [{task.index}] {task.description}")
            if task.tags:
                print(f"Tags: {', '.join(task.tags)}")
        else:
            print("[INFO] No pending tasks!")

    elif args.command == "current":
        task = engine.get_current()
        if task:
            print(json.dumps(task.to_dict(), indent=2))
        else:
            print("[INFO] No task in progress.")

    elif args.command == "future":
        for t in engine.get_future_tasks():
            print(f"[{t.index}] {t.description}")

    elif args.command == "past":
        for t in engine.get_past_tasks():
            print(f"[{t.index}] {t.description}")

    elif args.command == "status":
        engine.print_status()

    elif args.command == "dump":
        print(json.dumps(engine.dump_state(), indent=2))

    elif args.command == "rule":
        engine.add_rule(args.text)

    elif args.command == "rules":
        for i, r in enumerate(engine.get_rules(), 1):
            print(f"  {i}. {r}")

    elif args.command == "focus":
        engine.set_focus(args.text)

    # v4 commands
    elif args.command == "preflight":
        engine.preflight()

    elif args.command == "global_sync":
        engine.global_sync()

    elif args.command == "import_global":
        engine.import_from_global()

    elif args.command == "lessons":
        engine.show_lessons()

    elif args.command == "goals":
        engine.show_goals()

    elif args.command == "reorder":
        engine.reorder_by_dependencies()

    # Sub-goal commands
    elif args.command == "subgoals":
        engine.show_subgoals()

    elif args.command == "subgoal":
        engine.update_subgoal(args.index, args.status)

    elif args.command == "link":
        engine.link_task_to_subgoal(args.task_index, args.subgoal_index)

    elif args.command == "diagnose":
        engine.diagnose_friction(args.log_path)

    elif args.command == "catchup":
        engine.catchup(args.log_path, args.id, args.brain_dir)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
