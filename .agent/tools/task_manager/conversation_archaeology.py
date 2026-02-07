#!/usr/bin/env python3
"""
Conversation Archaeology Module v3
===================================
Enhanced Features:
1. Goal extraction from user prompts (via conversation summary/title)
2. Error collection from walkthroughs, corrections, and failed tasks
3. Mistake registry migration from existing tasks.json
4. Theme and pattern analysis

Scans conversation artifacts to auto-generate task registry.
"""

import json
import os
import re
import argparse
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

class ChatLogAnalyzer:
    """
    Analyzes raw chat logs to identify friction points and correlate them with tasks.
    """
    def __init__(self):
        self.friction_patterns = {
            "correction": [r"\bno\b", r"\bwrong", r"\bstop\b", r"\bnot what i", r"\badjust", r"\bfix", r"\bincorrect"],
            "confusion": [r"\bwhat\?", r"\bconfus", r"\bexplain", r"\bdon't understand", r"\bunclear"],
            "frustration": [r"\bagain\b", r"\bstill\b", r"\bfail", r"\bhard\b", r"\bdifficult", r"\bproblems?", r"\bissues?"],
            "positive": [r"\bgreat", r"\bgood", r"\bthanks", r"\bperfect", r"\bcorrect\b"]
        }

    def parse_log(self, log_path: Path) -> List[Dict]:
        """
        Parse chat log into turns. Supports format:
        User: ...
        Model: ...
        or timestamped.
        """
        turns = []
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return turns

        # Split by typical headers (User:/Model: or similar)
        # Regex to find "User:" or "Model:" or "Human:" or "Assistant:" at start of lines
        turn_pattern = r'^(User|Model|Human|Assistant|AI|System):'
        parts = re.split(turn_pattern, content, flags=re.MULTILINE)
        
        if len(parts) < 2:
            return turns # Format not recognized

        current_role = "Unknown"
        for i in range(1, len(parts), 2):
            role_str = parts[i].strip()
            text = parts[i+1].strip() if i+1 < len(parts) else ""
            
            role = "user" if role_str.lower() in ["user", "human"] else "model"
            turns.append({
                "index": len(turns) + 1,
                "role": role,
                "text": text,
                "length": len(text)
            })
            
        return turns

    def detect_friction(self, turns: List[Dict]) -> List[Dict]:
        """Identify friction points in user turns."""
        friction_events = []
        
        for i, turn in enumerate(turns):
            if turn["role"] != "user":
                continue
                
            text_lower = turn["text"].lower()
            
            # Check patterns
            detected_types = []
            score = 0
            
            for ftype, patterns in self.friction_patterns.items():
                if ftype == "positive": continue
                for pat in patterns:
                    if re.search(pat, text_lower):
                        detected_types.append(ftype)
                        score += 1
                        break
            
            # Context checks
            if i > 0 and turns[i-1]["role"] == "model":
                # If user message is short (< 20 chars) and contains negative keyword -> High friction
                if len(text_lower) < 20 and detected_types:
                    score += 2
            
            if detected_types:
                friction_events.append({
                    "turn_index": turn["index"],
                    "text": turn["text"][:100],
                    "types": detected_types,
                    "score": score,
                    "model_response_index": i + 1 if i + 1 < len(turns) else None
                })
                
        return friction_events

    def correlate_tasks(self, friction_events: List[Dict], tasks: List[Dict]) -> List[Dict]:
        """Map friction events to tasks based on keyword overlap."""
        correlated = []
        
        for event in friction_events:
            event_text = event["text"].lower()
            best_task = None
            max_score = 0
            
            for task in tasks:
                score = 0
                task_desc = task["description"].lower()
                
                # Check for exact phrase matches (high confidence)
                if task_desc in event_text:
                    score += 5
                
                # Tokenize and check for partial matches
                task_tokens = set(re.findall(r'\w{4,}', task_desc))
                if not task_tokens: continue
                
                for token in task_tokens:
                    # Simple stemming: remove 'ing', 's', 'ed'
                    stem = token
                    if stem.endswith('ing'): stem = stem[:-3]
                    elif stem.endswith('s'): stem = stem[:-1]
                    elif stem.endswith('ed'): stem = stem[:-2]
                    
                    if len(stem) < 4: continue # Too short after stemming
                    
                    if stem in event_text:
                        score += 1
                
                if score > max_score:
                    max_score = score
                    best_task = task
            
            if best_task and max_score >= 1:
                correlated.append({
                    "event": event,
                    "task_index": best_task["index"],
                    "task_desc": best_task["description"]
                })
                
        return correlated
class ConversationArchaeologist:
    """
    Scans for artifacts in the brain directory.
    """
    def __init__(self, brain_dir: str):
        self.brain_dir = Path(brain_dir)
        
    def find_artifacts(self, conversation_id: str) -> Dict[str, List[Path]]:
        """Find all artifact files in a conversation directory."""
        conv_dir = self.brain_dir / conversation_id
        
        artifacts = {
            "implementation_plans": [],
            "tasks": [],
            "walkthroughs": [],
            "other_md": [],
            "metadata": [],
            "json_data": []
        }
        
        if not conv_dir.exists():
            print(f"[WARN] Conversation directory not found: {conv_dir}")
            return artifacts
        
        for file in conv_dir.iterdir():
            if file.suffix == ".json":
                if "metadata" in file.name:
                    artifacts["metadata"].append(file)
                else:
                    artifacts["json_data"].append(file)
            elif file.suffix == ".md":
                name_lower = file.name.lower()
                if "implementation" in name_lower or "plan" in name_lower:
                    artifacts["implementation_plans"].append(file)
                elif "task" in name_lower:
                    artifacts["tasks"].append(file)
                elif "walkthrough" in name_lower:
                    artifacts["walkthroughs"].append(file)
                else:
                    artifacts["other_md"].append(file)
        
        return artifacts
    
    def parse_metadata(self, meta_path: Path) -> Dict:
        """Parse artifact metadata JSON."""
        try:
            with open(meta_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def parse_json_file(self, json_path: Path) -> Dict:
        """Parse a general JSON file."""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    # ==================== GOAL EXTRACTION ====================
    
    def extract_user_goals(self, artifacts: Dict, conversation_title: str = None) -> List[Dict]:
        """
        Extract user goals from multiple sources:
        1. Conversation title/summary (highest priority)
        2. Implementation plan titles and objectives
        3. Walkthrough goals
        """
        goals = []
        
        # Priority 1: Conversation title (represents user's original intent)
        if conversation_title:
            goals.append({
                "text": conversation_title,
                "source": "user_prompt:title",
                "priority": 15,  # Highest priority
                "type": "user_intent"
            })
        
        # Priority 2: Walkthrough goals (represent verified objectives)
        for wt_path in artifacts.get("walkthroughs", []):
            wt_goals = self._extract_walkthrough_goals(wt_path)
            goals.extend(wt_goals)
        
        # Priority 3: Implementation plan goals
        for plan_path in artifacts.get("implementation_plans", []):
            plan_goals = self._extract_plan_goals(plan_path)
            goals.extend(plan_goals)
        
        return goals
    
    def _extract_walkthrough_goals(self, wt_path: Path) -> List[Dict]:
        """Extract goals from walkthrough '## Goal' sections."""
        goals = []
        try:
            with open(wt_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return goals
        
        # Extract ## Goal section
        goal_match = re.search(r'^##\s*Goal\s*\n(.+?)(?=\n##|\Z)', content, re.MULTILINE | re.DOTALL)
        if goal_match:
            goal_text = goal_match.group(1).strip()
            # Take first paragraph only
            first_para = goal_text.split('\n\n')[0].replace('\n', ' ').strip()
            if len(first_para) > 20:
                goals.append({
                    "text": first_para[:200],
                    "source": f"walkthrough:{wt_path.name}",
                    "priority": 12,
                    "type": "verified_goal"
                })
        
        return goals
    
    def _extract_plan_goals(self, plan_path: Path) -> List[Dict]:
        """Extract goals from implementation plan."""
        goals = []
        try:
            with open(plan_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return goals
        
        # Main title
        title_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
        if title_match:
            goals.append({
                "text": title_match.group(1).strip(),
                "source": f"plan:{plan_path.name}",
                "priority": 10,
                "type": "plan_title"
            })
        
        # Phase headers
        phases = re.findall(r'^###?\s*(Phase\s*\d+[:\s]+.+?)$', content, re.MULTILINE | re.IGNORECASE)
        for phase in phases[:10]:
            goals.append({
                "text": phase.strip(),
                "source": f"plan:{plan_path.name}",
                "priority": 8,
                "type": "phase"
            })
        
        # [MODIFY], [NEW] items
        modify_items = re.findall(r'\[MODIFY\]\s*(.+?)(?:\n|$)', content)[:15]
        for item in modify_items:
            goals.append({
                "text": f"Modify: {item.strip()[:100]}",
                "source": f"plan:{plan_path.name}",
                "priority": 5,
                "type": "work_item"
            })
        
        return goals

    # ==================== AI GOAL ANALYSIS ====================
    
    def analyze_goals_deeply(self, goals: List[Dict], themes: List[str]) -> Dict:
        """
        AI Goal Analyzer: Decompose goals, generate success criteria, predict pitfalls.
        This provides granular understanding of what the user actually wants.
        """
        analysis = {
            "primary_goal": None,
            "sub_goals": [],
            "success_criteria": [],
            "predicted_pitfalls": [],
            "scope_guards": [],
            "output_expectations": [],
            "goal_type": None,
            "complexity_score": 0
        }
        
        if not goals:
            return analysis
        
        # === STEP 1: IDENTIFY PRIMARY GOAL ===
        # Highest priority goal
        primary = max(goals, key=lambda g: g.get("priority", 0))
        analysis["primary_goal"] = primary["text"]
        
        # === STEP 2: CLASSIFY GOAL TYPE ===
        goal_type_patterns = {
            "generation": ["generate", "create", "build", "make", "produce", "write"],
            "modification": ["modify", "update", "edit", "change", "fix", "correct", "remediate"],
            "analysis": ["analyze", "review", "audit", "check", "validate", "verify"],
            "integration": ["integrate", "merge", "combine", "sync", "connect"],
            "documentation": ["document", "describe", "explain", "outline"],
            "migration": ["migrate", "move", "transfer", "convert", "port"]
        }
        
        goal_lower = analysis["primary_goal"].lower()
        for gtype, keywords in goal_type_patterns.items():
            if any(kw in goal_lower for kw in keywords):
                analysis["goal_type"] = gtype
                break
        
        if not analysis["goal_type"]:
            analysis["goal_type"] = "general"
        
        # === STEP 3: DECOMPOSE INTO SUB-GOALS ===
        sub_goals = []
        
        # Domain-specific decomposition (VFT)
        vft_patterns = {
            "kanon": ["research sources", "verify attributions", "validate formatting", "check plane structure", "apply gold standard"],
            "plane": ["identify vectors", "gather quotes", "verify authors/years", "structure content", "add sense statements"],
            "generation": ["define scope", "gather inputs", "generate content", "validate output", "review quality"],
            "modification": ["identify current state", "define target state", "plan changes", "implement changes", "verify results"],
            "integration": ["understand both parts", "identify conflicts", "plan merge strategy", "execute merge", "validate integration"]
        }
        
        # Match based on goal type and keywords
        for pattern_key, sub_goal_list in vft_patterns.items():
            if pattern_key in goal_lower or pattern_key == analysis["goal_type"]:
                for sg in sub_goal_list:
                    sub_goals.append({
                        "description": sg,
                        "derived_from": pattern_key,
                        "status": "pending"
                    })
                break
        
        # If no specific match, use generic decomposition
        if not sub_goals:
            sub_goals = [
                {"description": "Define requirements", "derived_from": "generic", "status": "pending"},
                {"description": "Execute primary work", "derived_from": "generic", "status": "pending"},
                {"description": "Validate results", "derived_from": "generic", "status": "pending"}
            ]
        
        analysis["sub_goals"] = sub_goals
        
        # === STEP 4: GENERATE SUCCESS CRITERIA ===
        criteria_by_type = {
            "generation": [
                "All output files created successfully",
                "Output matches expected structure/format",
                "No placeholder content remains",
                "Content meets quality standards"
            ],
            "modification": [
                "All targeted changes applied",
                "Existing functionality preserved",
                "Changes match specification",
                "No regressions introduced"
            ],
            "analysis": [
                "All items reviewed",
                "Findings documented",
                "Severity assessed",
                "Recommendations provided"
            ],
            "documentation": [
                "All topics covered",
                "Clear and understandable",
                "Accurate and verified",
                "Properly formatted"
            ]
        }
        
        analysis["success_criteria"] = criteria_by_type.get(
            analysis["goal_type"], 
            ["Goal completed", "Quality verified", "User satisfied"]
        )
        
        # Add domain-specific criteria for VFT
        if any(kw in goal_lower for kw in ["kanon", "plane", "vector", "vft"]):
            analysis["success_criteria"].extend([
                "Sources verified: Author, Work, Year",
                "Formatting matches Gold Standard",
                "7-Sentence Rule applied where needed",
                "No generic attributions"
            ])
        
        # === STEP 5: PREDICT PITFALLS ===
        pitfalls_by_type = {
            "generation": [
                {"name": "Placeholder Pollution", "description": "Leaving TODO or placeholder text in output"},
                {"name": "Format Drift", "description": "Output structure deviates from template"},
                {"name": "Scope Creep", "description": "Adding features not in original requirement"}
            ],
            "modification": [
                {"name": "Incomplete Changes", "description": "Missing some instances that should be changed"},
                {"name": "Breaking Existing", "description": "Changes that break unrelated functionality"},
                {"name": "Order Dependency", "description": "Making changes in wrong order"}
            ],
            "analysis": [
                {"name": "False Negatives", "description": "Missing issues that should be caught"},
                {"name": "Context Blindness", "description": "Judging without understanding intent"},
                {"name": "Severity Misclassification", "description": "Wrong priority on findings"}
            ]
        }
        
        analysis["predicted_pitfalls"] = pitfalls_by_type.get(
            analysis["goal_type"],
            [{"name": "Generic Error", "description": "Unspecified failure mode"}]
        )
        
        # Add VFT-specific pitfalls
        if any(kw in goal_lower for kw in ["kanon", "plane", "australia"]):
            analysis["predicted_pitfalls"].extend([
                {"name": "Generic Sourcing", "description": "Using 'Australian saying' instead of real sources"},
                {"name": "Plane Misplacement", "description": "Content in wrong plane file"},
                {"name": "First Nations Oversight", "description": "Missing indigenous perspective in Partner Row"},
                {"name": "Attribution Laziness", "description": "Not researching full Author, Work, Year"}
            ])
        
        # === STEP 6: GENERATE SCOPE GUARDS ===
        analysis["scope_guards"] = [
            f"Does this action serve the primary goal: '{analysis['primary_goal'][:50]}...'?",
            "Am I adding features not explicitly requested?",
            "Is this the right file/location for this change?",
            "Have I verified this matches the stated requirements?"
        ]
        
        # === STEP 7: OUTPUT EXPECTATIONS ===
        output_patterns = {
            "kanon": ["Australian_Kanon_Plane_*.md files", "Structured quote format", "7 vectors per sub-section"],
            "generation": ["New files created", "Content populated", "No placeholders"],
            "modification": ["Files updated in place", "Changes logged", "Validation passed"],
            "documentation": ["Markdown files", "Clear structure", "Examples included"]
        }
        
        for pattern_key, expectations in output_patterns.items():
            if pattern_key in goal_lower or pattern_key == analysis["goal_type"]:
                analysis["output_expectations"] = expectations
                break
        
        if not analysis["output_expectations"]:
            analysis["output_expectations"] = ["User-specified output format"]
        
        # === STEP 8: COMPLEXITY SCORE ===
        # 1-10 based on goal characteristics
        score = 1
        if len(goals) > 5:
            score += 2
        if analysis["goal_type"] in ["integration", "migration"]:
            score += 2
        if any(kw in goal_lower for kw in ["all", "every", "complete", "comprehensive"]):
            score += 2
        if any(kw in goal_lower for kw in ["kanon", "plane", "vector"]):
            score += 2  # Domain complexity
        if len(sub_goals) > 4:
            score += 1
        
        analysis["complexity_score"] = min(score, 10)
        
        return analysis
    
    def generate_goal_report(self, goal_analysis: Dict) -> str:
        """Generate human-readable goal analysis report."""
        lines = []
        lines.append("# Goal Analysis (AI Generated)")
        lines.append("")
        lines.append(f"**Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"**Complexity Score**: {goal_analysis['complexity_score']}/10")
        lines.append(f"**Goal Type**: {goal_analysis['goal_type']}")
        lines.append("")
        
        # Primary Goal
        lines.append("## Primary Goal")
        lines.append(f"> {goal_analysis['primary_goal']}")
        lines.append("")
        
        # Sub-goals
        if goal_analysis.get("sub_goals"):
            lines.append("## Sub-Goals (Decomposition)")
            for i, sg in enumerate(goal_analysis["sub_goals"], 1):
                lines.append(f"{i}. [ ] {sg['description']}")
            lines.append("")
        
        # Success Criteria
        if goal_analysis.get("success_criteria"):
            lines.append("## Success Criteria")
            for criterion in goal_analysis["success_criteria"]:
                lines.append(f"- [ ] {criterion}")
            lines.append("")
        
        # Predicted Pitfalls
        if goal_analysis.get("predicted_pitfalls"):
            lines.append("## Predicted Pitfalls")
            for pitfall in goal_analysis["predicted_pitfalls"]:
                lines.append(f"> [!WARNING] **{pitfall['name']}**")
                lines.append(f"> {pitfall['description']}")
                lines.append(">")
            lines.append("")
        
        # Scope Guards
        if goal_analysis.get("scope_guards"):
            lines.append("## Scope Guards (Check Before Acting)")
            for guard in goal_analysis["scope_guards"]:
                lines.append(f"- {guard}")
            lines.append("")
        
        # Output Expectations
        if goal_analysis.get("output_expectations"):
            lines.append("## Expected Outputs")
            for out in goal_analysis["output_expectations"]:
                lines.append(f"- {out}")
        
        return "\n".join(lines)
    
    def extract_errors(self, artifacts: Dict) -> List[Dict]:
        """
        Collect errors from multiple sources:
        1. Walkthrough corrections/fixes
        2. Failed tasks in tasks.json
        3. Existing mistakes_registry
        """
        errors = []
        
        # Source 1: Walkthrough corrections
        for wt_path in artifacts.get("walkthroughs", []):
            wt_errors = self._extract_walkthrough_errors(wt_path)
            errors.extend(wt_errors)
        
        # Source 2: Existing tasks.json mistakes and failed tasks
        for json_path in artifacts.get("json_data", []):
            if "tasks" in json_path.name:
                json_errors = self._extract_json_errors(json_path)
                errors.extend(json_errors)
        
        # Source 3: Any markdown with "error", "fix", "bug" mentions
        all_md = (artifacts.get("implementation_plans", []) + 
                  artifacts.get("other_md", []))
        for md_path in all_md[:10]:
            md_errors = self._extract_md_errors(md_path)
            errors.extend(md_errors)
        
        return errors
    
    def _extract_walkthrough_errors(self, wt_path: Path) -> List[Dict]:
        """Extract corrections and fixes from walkthrough."""
        errors = []
        try:
            with open(wt_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return errors
        
        # Look for "Correction", "Fix", "Error" sections
        patterns = [
            (r'\*\*([^*]+(?:Fix|Correction|Error)[^*]*)\*\*[:\s]+(.+?)(?=\n-|\n\*|\n#|\Z)', 'correction'),
            (r'^-\s*\*\*([^:]+)\*\*:\s*(.+?)(?=\n)', 'bullet_fix'),
            (r'(?:Fixed|Corrected|Resolved)[:\s]+(.+?)(?:\.|$)', 'inline_fix'),
        ]
        
        for pattern, error_type in patterns:
            matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
            for match in matches[:10]:
                if isinstance(match, tuple):
                    name, desc = match[0][:50], match[1][:100] if len(match) > 1 else match[0][:100]
                else:
                    name, desc = error_type, match[:100]
                
                errors.append({
                    "id": f"ARC_{len(errors)+1:03d}",
                    "name": name.strip(),
                    "description": desc.strip(),
                    "source": f"walkthrough:{wt_path.name}",
                    "type": error_type,
                    "tags": ["archaeology", "historical"]
                })
        
        return errors
    
    def _extract_json_errors(self, json_path: Path) -> List[Dict]:
        """Extract mistakes and failed tasks from tasks.json."""
        errors = []
        data = self.parse_json_file(json_path)
        
        # Existing mistakes registry
        if "global_context" in data:
            for mistake in data["global_context"].get("mistakes_registry", []):
                errors.append({
                    "id": mistake.get("id", f"LEGACY_{len(errors)+1:03d}"),
                    "name": mistake.get("name", "Unknown"),
                    "description": mistake.get("structure", "") + ": " + mistake.get("example", ""),
                    "source": "tasks.json:registry",
                    "type": "registered_mistake",
                    "tags": mistake.get("tags", []) + ["migrated"]
                })
        
        # Failed tasks
        for task in data.get("tasks", []):
            if task.get("status") == "failed":
                # Get root cause if available
                root_cause = task.get("postmortem", {}).get("root_cause", "No root cause recorded")
                errors.append({
                    "id": f"FAIL_{task.get('index', 0):03d}",
                    "name": f"Failed: {task.get('description', 'Unknown')[:50]}",
                    "description": root_cause,
                    "source": "tasks.json:failed",
                    "type": "task_failure",
                    "tags": task.get("tags", []) + ["failure"]
                })
        
        return errors
    
    def _extract_md_errors(self, md_path: Path) -> List[Dict]:
        """Extract error mentions from general markdown files."""
        errors = []
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return errors
        
        # Look for [!WARNING] and [!CAUTION] blocks
        warning_pattern = r'>\s*\[!(?:WARNING|CAUTION)\][^\n]*\n>\s*(.+?)(?=\n[^>]|\Z)'
        matches = re.findall(warning_pattern, content, re.MULTILINE | re.DOTALL)
        
        for match in matches[:5]:
            clean = match.replace('>', '').replace('\n', ' ').strip()[:100]
            errors.append({
                "id": f"WARN_{len(errors)+1:03d}",
                "name": "Warning/Caution",
                "description": clean,
                "source": f"markdown:{md_path.name}",
                "type": "warning",
                "tags": ["archaeology", "warning"]
            })
        
        return errors

    # ==================== ANALYSIS ====================
    
    def extract_existing_tasks(self, task_path: Path) -> List[Dict]:
        """Extract existing task items from task.md."""
        tasks = []
        try:
            with open(task_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return tasks
        
        task_pattern = r'^\s*[-*]\s*\[([ x/\-!~])\]\s*(.+?)(?:<!--.*-->)?$'
        matches = re.findall(task_pattern, content, re.MULTILINE)
        
        for status_char, description in matches:
            status = "todo"
            if status_char == "x":
                status = "done"
            elif status_char == "/":
                status = "in_progress"
            elif status_char == "-":
                status = "failed"
            
            tasks.append({
                "text": description.strip(),
                "status": status,
                "source": "task.md"
            })
        
        return tasks
    
    def extract_themes(self, md_paths: List[Path]) -> List[str]:
        """Extract common themes from all markdown files."""
        word_counts: Dict[str, int] = {}
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
                     'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                     'would', 'could', 'should', 'may', 'might', 'must', 'shall',
                     'can', 'need', 'to', 'of', 'in', 'for', 'on', 'with', 'at',
                     'by', 'from', 'up', 'about', 'into', 'through', 'during',
                     'before', 'after', 'above', 'below', 'between', 'under',
                     'again', 'further', 'then', 'once', 'here', 'there', 'when',
                     'where', 'why', 'how', 'all', 'each', 'few', 'more', 'most',
                     'other', 'some', 'such', 'only', 'own', 'same', 'than',
                     'too', 'very', 'just', 'and', 'but', 'if', 'or', 'because',
                     'this', 'that', 'these', 'those', 'it', 'its', 'you', 'your',
                     'we', 'our', 'they', 'their', 'he', 'she', 'who', 'which',
                     'what', 'also', 'like', 'make', 'get', 'use', 'new', 'file',
                     'current', 'using', 'update', 'add', 'not', 'will', 'must'}
        
        for path in md_paths[:20]:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    text = f.read()
                words = re.findall(r'\b[a-z]{4,}\b', text.lower())
                for word in words:
                    if word not in stopwords:
                        word_counts[word] = word_counts.get(word, 0) + 1
            except:
                continue
        
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        return [w for w, c in sorted_words[:15] if c >= 3]

    # ==================== AI ERROR ANALYSIS ====================
    
    def analyze_errors_deeply(self, errors: List[Dict], themes: List[str]) -> Dict:
        """
        AI Analysis Layer: Categorize errors, identify patterns, generate lessons.
        This produces human-readable insights, not just raw data.
        """
        analysis = {
            "categories": {},
            "patterns": [],
            "root_causes": [],
            "lessons_learned": [],
            "recommendations": [],
            "severity_distribution": {"critical": 0, "major": 0, "minor": 0}
        }
        
        if not errors:
            return analysis
        
        # === STEP 1: CATEGORIZE ERRORS ===
        category_keywords = {
            "formatting": ["format", "style", "layout", "structure", "header", "line", "spacing"],
            "sourcing": ["source", "author", "quote", "attribution", "citation", "year", "reference"],
            "data_integrity": ["missing", "incorrect", "wrong", "typo", "error", "invalid"],
            "structural": ["location", "plane", "moved", "position", "placement"],
            "encoding": ["encoding", "character", "utf", "unicode", "artifact"],
            "logic": ["logic", "flow", "dependency", "order", "sequence"],
            "process": ["forgot", "skipped", "missed", "incomplete", "partial"]
        }
        
        for err in errors:
            text = f"{err.get('name', '')} {err.get('description', '')}".lower()
            categorized = False
            
            for category, keywords in category_keywords.items():
                if any(kw in text for kw in keywords):
                    if category not in analysis["categories"]:
                        analysis["categories"][category] = []
                    analysis["categories"][category].append(err)
                    categorized = True
                    break
            
            if not categorized:
                if "other" not in analysis["categories"]:
                    analysis["categories"]["other"] = []
                analysis["categories"]["other"].append(err)
        
        # === STEP 2: IDENTIFY PATTERNS ===
        # Count category frequencies
        category_counts = {cat: len(errs) for cat, errs in analysis["categories"].items()}
        total = sum(category_counts.values())
        
        for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
            if count >= 2:  # Pattern = 2+ occurrences
                pct = (count / total) * 100
                analysis["patterns"].append({
                    "category": cat,
                    "count": count,
                    "percentage": round(pct, 1),
                    "observation": f"{count} errors ({pct:.0f}%) relate to {cat}"
                })
        
        # === STEP 3: IDENTIFY ROOT CAUSES ===
        root_cause_map = {
            "formatting": "Inconsistent application of formatting standards",
            "sourcing": "Incomplete research or attribution verification",
            "data_integrity": "Lack of validation before committing changes",
            "structural": "Unclear mental model of document organization",
            "encoding": "Platform/tool incompatibility not anticipated",
            "logic": "Rushed implementation without dependency analysis",
            "process": "Missing checklist or verification step"
        }
        
        for cat in analysis["categories"]:
            if cat in root_cause_map:
                analysis["root_causes"].append({
                    "category": cat,
                    "root_cause": root_cause_map[cat],
                    "affected_count": len(analysis["categories"][cat])
                })
        
        # === STEP 4: GENERATE LESSONS LEARNED ===
        lessons_map = {
            "formatting": "Always validate formatting against the Gold Standard before committing. Create a formatting checklist.",
            "sourcing": "Research the source fully: Author, Work, Year. Generic attributions are technical debt.",
            "data_integrity": "Run validation scripts before AND after major changes. Trust but verify.",
            "structural": "Map the document structure before editing. Know WHERE things belong, not just WHAT.",
            "encoding": "Test content in the target environment. Character encoding issues compound over time.",
            "logic": "Draw the dependency graph. Edit in dependency order, not file order.",
            "process": "If you forgot once, you'll forget again. Add it to the checklist."
        }
        
        for cat in analysis["categories"]:
            if cat in lessons_map:
                analysis["lessons_learned"].append({
                    "from_category": cat,
                    "lesson": lessons_map[cat]
                })
        
        # === STEP 5: GENERATE RECOMMENDATIONS ===
        # Priority recommendations based on error frequency
        for pattern in analysis["patterns"][:3]:  # Top 3 problem areas
            cat = pattern["category"]
            recommendations = {
                "formatting": "Add a formatting validation step to the pre-commit checklist",
                "sourcing": "Create a sourcing template: 'Quote - Author, Work, Year'",
                "data_integrity": "Run automated validators after each editing session",
                "structural": "Maintain a structural map document for complex projects",
                "encoding": "Standardize on UTF-8 and validate after any cross-platform work",
                "logic": "Create a dependency diagram before multi-file changes",
                "process": "Review the mistake registry at the START of each session"
            }
            if cat in recommendations:
                analysis["recommendations"].append({
                    "priority": len(analysis["recommendations"]) + 1,
                    "category": cat,
                    "recommendation": recommendations[cat]
                })
        
        # === STEP 6: SEVERITY DISTRIBUTION ===
        for err in errors:
            text = f"{err.get('name', '')} {err.get('description', '')}".lower()
            if any(w in text for w in ["critical", "break", "fail", "corrupt", "lost"]):
                analysis["severity_distribution"]["critical"] += 1
            elif any(w in text for w in ["incorrect", "wrong", "missing", "error"]):
                analysis["severity_distribution"]["major"] += 1
            else:
                analysis["severity_distribution"]["minor"] += 1
        
        return analysis
    
    def generate_lessons_report(self, error_analysis: Dict) -> str:
        """Generate a human-readable lessons learned report."""
        lines = []
        lines.append("# Lessons Learned (Archaeological Analysis)")
        lines.append("")
        lines.append(f"**Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("")
        
        # Patterns
        if error_analysis.get("patterns"):
            lines.append("## Error Patterns Identified")
            for p in error_analysis["patterns"]:
                lines.append(f"- **{p['category'].title()}**: {p['observation']}")
            lines.append("")
        
        # Root Causes
        if error_analysis.get("root_causes"):
            lines.append("## Root Causes")
            for rc in error_analysis["root_causes"]:
                lines.append(f"- **{rc['category'].title()}** ({rc['affected_count']} errors): {rc['root_cause']}")
            lines.append("")
        
        # Lessons
        if error_analysis.get("lessons_learned"):
            lines.append("## Key Lessons")
            for i, lesson in enumerate(error_analysis["lessons_learned"], 1):
                lines.append(f"{i}. **{lesson['from_category'].title()}**: {lesson['lesson']}")
            lines.append("")
        
        # Recommendations
        if error_analysis.get("recommendations"):
            lines.append("## Recommendations (Priority Order)")
            for rec in error_analysis["recommendations"]:
                lines.append(f"{rec['priority']}. [{rec['category'].upper()}] {rec['recommendation']}")
            lines.append("")
        
        # Severity
        sev = error_analysis.get("severity_distribution", {})
        if any(sev.values()):
            lines.append("## Severity Distribution")
            lines.append(f"- Critical: {sev.get('critical', 0)}")
            lines.append(f"- Major: {sev.get('major', 0)}")
            lines.append(f"- Minor: {sev.get('minor', 0)}")
        
        return "\n".join(lines)

    # ==================== MAIN ANALYSIS ====================
    
    def analyze_conversation(self, conversation_id: str, conversation_title: str = None, chat_log_path: str = None) -> Dict:
        """Full analysis of a conversation directory."""
        print(f"[ARCHAEOLOGY v3] Analyzing: {conversation_id}")
        
        artifacts = self.find_artifacts(conversation_id)
        
        analysis = {
            "conversation_id": conversation_id,
            "conversation_title": conversation_title,
            "user_goals": [],
            "work_items": [],
            "existing_tasks": [],
            "errors": [],
            "themes": [],
            "artifact_summaries": [],
            "artifact_count": sum(len(v) for v in artifacts.values()),
            "friction_events": [],
            "correlated_friction": []
        }
        
        # Analyze Chat Log (if provided)
        if chat_log_path and Path(chat_log_path).exists():
            print(f"   [CHAT] Parsing log: {Path(chat_log_path).name}")
            analyzer = ChatLogAnalyzer()
            turns = analyzer.parse_log(Path(chat_log_path))
            print(f"   [CHAT] Turns: {len(turns)}")
            
            friction = analyzer.detect_friction(turns)
            analysis["friction_events"] = friction
            print(f"   [CHAT] Friction Events: {len(friction)}")
            
            # Note: Correlation happens later when tasks are extracted
        elif chat_log_path:
            print(f"[WARN] Chat log not found: {chat_log_path}")
        
        # Parse metadata for summaries
        for meta_path in artifacts["metadata"]:
            meta = self.parse_metadata(meta_path)
            if meta.get("summary"):
                analysis["artifact_summaries"].append({
                    "file": meta_path.stem.replace(".metadata", ""),
                    "type": meta.get("artifactType", "unknown"),
                    "summary": meta["summary"]
                })
        
        # Extract user goals
        goals = self.extract_user_goals(artifacts, conversation_title)
        # Separate high-priority user goals from work items
        for g in goals:
            if g["priority"] >= 10:
                analysis["user_goals"].append(g)
            else:
                analysis["work_items"].append(g)
        print(f"   User Goals: {len(analysis['user_goals'])}")
        print(f"   Work Items: {len(analysis['work_items'])}")
        
        # Extract errors
        analysis["errors"] = self.extract_errors(artifacts)
        print(f"   Errors Collected: {len(analysis['errors'])}")
        
        # Extract existing tasks
        for task_path in artifacts["tasks"]:
            tasks = self.extract_existing_tasks(task_path)
            analysis["existing_tasks"].extend(tasks)
        print(f"   Existing Tasks: {len(analysis['existing_tasks'])}")
        
        # Extract themes
        all_md = (artifacts["implementation_plans"] + artifacts["tasks"] + 
                  artifacts["walkthroughs"] + artifacts["other_md"])
        analysis["themes"] = self.extract_themes(all_md)
        print(f"   Themes: {', '.join(analysis['themes'][:5])}")
        
        return analysis
    
    def generate_registry(self, analysis: Dict) -> Dict:
        """Generate full task registry from analysis."""
        tasks = []
        seen = set()
        
        # User goals first (highest priority)
        for goal in sorted(analysis.get("user_goals", []), key=lambda x: -x.get("priority", 0)):
            key = goal["text"][:50].lower()
            if key not in seen:
                seen.add(key)
                tasks.append({
                    "description": goal["text"],
                    "tags": ["user_goal"] + analysis.get("themes", [])[:2],
                    "source": goal["source"],
                    "priority": goal.get("priority", 0),
                    "status": "todo"
                })
        
        # Work items
        for item in sorted(analysis.get("work_items", []), key=lambda x: -x.get("priority", 0)):
            key = item["text"][:50].lower()
            if key not in seen:
                seen.add(key)
                tasks.append({
                    "description": item["text"],
                    "tags": analysis.get("themes", [])[:3],
                    "source": item["source"],
                    "priority": item.get("priority", 0),
                    "status": "todo"
                })
        
        # Get project name
        project_name = "Bootstrapped Project"
        if analysis.get("user_goals"):
            project_name = analysis["user_goals"][0]["text"][:60]
        elif analysis.get("artifact_summaries"):
            project_name = analysis["artifact_summaries"][0]["summary"][:60]
        
        # Convert errors to mistakes registry
        mistakes = []
        for err in analysis.get("errors", [])[:20]:
            mistakes.append({
                "id": err["id"],
                "name": err["name"],
                "structure": err["description"],
                "example": f"Source: {err['source']}",
                "tags": err.get("tags", []),
                "linked_tasks": [],
                "timestamp": datetime.now().isoformat()
            })
        
        registry = {
            "global_context": {
                "project_name": project_name,
                "project_rules": [],
                "current_focus": "Review archaeology results",
                "current_task_index": None,
                "mistakes_registry": mistakes,
                "fuckup_prevention_checklist": [
                    "Did I read the requirements fully?",
                    "Did I check the mistake registry?",
                    "Did I validate the output format?",
                    "Did I log my reasoning?"
                ],
                "archaeology_source": {
                    "conversation_id": analysis["conversation_id"],
                    "conversation_title": analysis.get("conversation_title"),
                    "analysis_timestamp": datetime.now().isoformat(),
                    "themes": analysis["themes"],
                    "user_goals_count": len(analysis["user_goals"]),
                    "errors_collected": len(analysis["errors"]),
                    "artifact_summaries": analysis["artifact_summaries"][:5]
                }
            },
            "tasks": []
        }
        
        for i, task in enumerate(tasks[:40]):
            registry["tasks"].append({
                "index": i,
                "id": f"task_{i}",
                "description": task["description"],
                "status": task["status"],
                "data": {"source": task["source"]},
                "validation": {"criteria": [], "examples": []},
                "rules": [],
                "logs": [f"[{datetime.now().isoformat()}] Created via archaeology v3"],
                "lessons_learned": [],
                "depends_on": [],
                "priority": task["priority"],
                "tags": task["tags"],
                "reasoning_trace": [],
                "auto_linked_mistakes": [],
                "postmortem": {"passes": [], "root_cause": None}
            })
        
        return registry
    
    def bootstrap_from_conversation(self, conversation_id: str, 
                                    conversation_title: str = None,
                                    chat_log_path: str = None,
                                    output_path: str = "tasks.json"):
        """Main entry: Analyze conversation and generate task registry."""
        analysis = self.analyze_conversation(conversation_id, conversation_title, chat_log_path)
        
        # === AI ANALYSIS LAYER ===
        print(f"\n[AI ANALYSIS] Analyzing errors...")
        error_analysis = self.analyze_errors_deeply(analysis["errors"], analysis["themes"])
        
        if error_analysis["patterns"]:
            print(f"   Patterns Found: {len(error_analysis['patterns'])}")
            for p in error_analysis["patterns"][:3]:
                print(f"     - {p['observation']}")
        
        if error_analysis["lessons_learned"]:
            print(f"   Lessons Generated: {len(error_analysis['lessons_learned'])}")
        
        # Store analysis in the analysis dict for registry generation
        analysis["error_analysis"] = error_analysis
        
        registry = self.generate_registry(analysis)
        
        # === FRICTION ANALYSIS CORRELATION ===
        if analysis.get("friction_events"):
            print(f"\n[AI FRICTION] Correlating friction events to tasks...")
            analyzer = ChatLogAnalyzer()
            # Map registry tasks format to simple dict
            simple_tasks = [{"index": t["index"], "description": t["description"]} for t in registry["tasks"]]
            
            correlations = analyzer.correlate_tasks(analysis["friction_events"], simple_tasks)
            print(f"   Correlated Events: {len(correlations)}")
            
            # Update tasks with friction logs
            for corr in correlations:
                idx = corr["task_index"]
                event = corr["event"]
                task = registry["tasks"][idx]
                
                log_entry = f"[FRICTION] Turn {event['turn_index']} (Score: {event['score']}): {event['text']}..."
                task["logs"].append(log_entry)
                
                # If high score, mark as struggled
                if event["score"] >= 2:
                    if "struggled" not in task["tags"]:
                        task["tags"].append("struggled")
            
            # Add friction summary to global context
            registry["global_context"]["friction_log"] = correlations

        # Add error analysis to global context
        registry["global_context"]["error_analysis"] = error_analysis
        
        # Analyze goals deeply
        print(f"\n[AI GOAL] Deeply analyzing goals...")
        goal_analysis = self.analyze_goals_deeply(analysis["user_goals"], analysis["themes"])
        registry["global_context"]["goal_analysis"] = goal_analysis
        
        print(f"   Primary: {goal_analysis['primary_goal']}")
        print(f"   Predicted Pitfalls: {len(goal_analysis['predicted_pitfalls'])}")
        
        # === MISTAKES REGISTRY ===
        # registry["global_context"]["mistakes_registry"] is already populated by generate_registry

        
        print(f"\n[BOOTSTRAP] Writing to {output_path}...")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=4)
            
        print("[BOOTSTRAP] Generating task.md...")
        md_file = Path(output_path).with_name('task.md')
        self._render_markdown(registry, str(md_file))
        
        if analysis["error_analysis"]:
            print("[BOOTSTRAP] Generating lessons_learned.md...")
            lessons_report = self.generate_lessons_report(analysis["error_analysis"])
            with open("lessons_learned.md", 'w', encoding='utf-8') as f:
                f.write(lessons_report)
                
        if goal_analysis:
            print("[BOOTSTRAP] Generating goal_analysis.md...")
            goal_report = self.generate_goal_report(goal_analysis)
            with open("goal_analysis.md", 'w', encoding='utf-8') as f:
                f.write(goal_report)
            print(f"[OK] Generated goal_analysis.md")
        
        return registry
    
    def _render_markdown(self, registry: Dict, output_path: str):
        """Generate task.md from registry."""
        lines = []
        gc = registry["global_context"]
        lines.append(f"# {gc.get('project_name', 'Task List')}")
        lines.append("")
        lines.append(f"**Focus**: {gc.get('current_focus', 'None')}")
        lines.append("")
        
        done = sum(1 for t in registry["tasks"] if t["status"] == "done")
        total = len(registry["tasks"])
        lines.append(f"**Progress**: {done}/{total}")
        lines.append("")
        lines.append("## Tasks")
        
        for task in registry["tasks"]:
            cb = {"todo": "[ ]", "done": "[x]", "in_progress": "[/]", "failed": "[-]"}.get(task["status"], "[ ]")
            tag_str = f" `{' '.join(task['tags'][:2])}`" if task.get('tags') else ""
            friction = " ⚠️" if "struggled" in task.get("tags", []) else ""
            lines.append(f"- {cb} {task['description']}{tag_str}{friction} <!-- id: {task['index']} -->")
        
        # Add mistakes section
        mistakes = gc.get("mistakes_registry", [])
        if mistakes:
            lines.append("")
            lines.append("## Error Registry (Archaeological)")
            for m in mistakes[:10]:
                lines.append(f"> [!WARNING] {m['id']}: {m['name']}")
                lines.append(f"> {m['structure'][:80]}")
                lines.append(">")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(description="Conversation Archaeology v3")
    parser.add_argument("conversation_id", type=str)
    parser.add_argument("--title", type=str, default=None,
                        help="Conversation title (user's original goal)")
    parser.add_argument("--brain-dir", type=str, 
                        default=r"C:\Users\hungh\.gemini\antigravity\brain")
    parser.add_argument("--output", type=str, default="tasks.json")
    parser.add_argument("--chat-log", type=str, default=None, 
                        help="Path to raw chat log file for friction analysis")
    
    args = parser.parse_args()
    
    archaeologist = ConversationArchaeologist(args.brain_dir)
    archaeologist.bootstrap_from_conversation(
        args.conversation_id, 
        args.title,
        args.output
    )


if __name__ == "__main__":
    main()
