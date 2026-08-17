"""aletheia_mcp_server.py — Dedicated FastMCP Server for Aletheia Bot News Audits, Hypocrisy Analytics & Chat Memory.

## Usage
To connect to Claude Desktop or AGY, add to claude_desktop_config.json:
{
  "mcpServers": {
    "aletheia": {
      "command": "python",
      "args": ["e:/Vector Field Theory/VFT Docs/bluesky_bot/aletheia_mcp_server.py"]
    }
  }
}
"""
import os
import sys
import glob
import json
import datetime
import urllib.parse
from dotenv import load_dotenv

script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(script_dir, ".env"))

# Import local SQLite memory engine
sys.path.insert(0, script_dir)
try:
    import memory_store
except ImportError:
    memory_store = None

STORIES_DIR = os.path.join(script_dir, "stories")
LIVE_DIR = os.path.join(STORIES_DIR, "live")
DARKROOM_DIR = os.path.join(STORIES_DIR, "darkroom")
POLICY_LEDGER_PATH = os.path.join(script_dir, "policy_ledger.json")
SESSIONS_DIR = os.path.join(script_dir, "chat_sessions")

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    try:
        from mcp.server import MCPServer as FastMCP
    except ImportError:
        FastMCP = None

if FastMCP is None:
    print("Warning: 'mcp' python package is not installed. Install via: pip install mcp", file=sys.stderr)

mcp = FastMCP("Aletheia Bot") if FastMCP else None


def _load_all_stories():
    """Load all factcheck JSON files across live, darkroom, and stories root dynamically."""
    stories = {}
    search_dirs = [LIVE_DIR, DARKROOM_DIR, STORIES_DIR]
    for sdir in search_dirs:
        if not os.path.exists(sdir):
            continue
        for p in glob.glob(os.path.join(sdir, "factcheck_*.json")):
            slug = os.path.basename(p)[len("factcheck_"):-len(".json")]
            if slug in stories:
                continue
            try:
                mtime = os.path.getmtime(p)
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                cfg = data[0] if isinstance(data, list) and len(data) > 0 else (data if isinstance(data, dict) else {})
                cfg["_mtime"] = mtime
                cfg["_filepath"] = p
                if "id" not in cfg:
                    cfg["id"] = slug
                stories[slug] = cfg
            except Exception:
                pass
    return stories


def _get_verdict(real_u, real_psi):
    if real_u is None or real_psi is None:
        return "UNKNOWN"
    return "PASS" if (real_u >= 0 and real_psi >= 0) else "FAIL"


def _get_path_name(claim_u, claim_psi, real_u, real_psi):
    if any(v is None for v in [claim_u, claim_psi, real_u, real_psi]):
        return "Unmapped"
    c_pos = (claim_u >= 0 and claim_psi >= 0)
    r_pos = (real_u >= 0 and real_psi >= 0)
    if c_pos and r_pos:
        return "Path of Grace"
    elif c_pos and not r_pos:
        return "Path of Deception"
    elif not c_pos and r_pos:
        return "Path of Redemption"
    elif not c_pos and not r_pos:
        return "Path of Fall"
    return "Path of Compromise"


if mcp:
    # --- STORY & AUDIT TOOLS ---
    @mcp.tool()
    def list_stories(verdict: str = "", limit: int = 20) -> str:
        """List evaluated stories. Optional verdict filter: 'PASS' or 'FAIL'."""
        stories = _load_all_stories()
        items = list(stories.values())
        items.sort(key=lambda x: x.get("_mtime", 0), reverse=True)

        results = []
        for s in items:
            u = s.get("real_u")
            psi = s.get("real_psi")
            v = _get_verdict(u, psi)
            if verdict and v.upper() != verdict.upper():
                continue
            mtime_str = datetime.datetime.fromtimestamp(s.get("_mtime", 0)).strftime("%Y-%m-%d %H:%M")
            results.append({
                "id": s.get("id"),
                "subject": s.get("subject", ""),
                "real_u": u,
                "real_psi": psi,
                "verdict": v,
                "date": mtime_str,
                "status": s.get("status", "draft")
            })
            if len(results) >= limit:
                break
        return json.dumps(results, indent=2)

    @mcp.tool()
    def get_story(slug: str) -> str:
        """Get the full JSON config for a story by its slug or id."""
        stories = _load_all_stories()
        clean_slug = slug.strip()
        if clean_slug.startswith("factcheck_"):
            clean_slug = clean_slug[len("factcheck_"):]
        if clean_slug.endswith(".json"):
            clean_slug = clean_slug[:-len(".json")]

        story = stories.get(clean_slug)
        if not story:
            return json.dumps({"error": f"Story '{slug}' not found."})
        return json.dumps(story, indent=2)

    @mcp.tool()
    def get_corpus_overview() -> str:
        """Get high-level summary of the entire audit corpus: total records, moral averages, pass rate, trajectory splits."""
        stories = _load_all_stories()
        u_vals, psi_vals, deltas = [], [], []
        pass_c, fail_c = 0, 0
        paths = {}

        for s in stories.values():
            u = s.get("real_u")
            psi = s.get("real_psi")
            cu = s.get("claim_u")
            cpsi = s.get("claim_psi")
            if u is not None and psi is not None:
                u_vals.append(u)
                psi_vals.append(psi)
                if cu is not None:
                    deltas.append(cu - u)
                if u >= 0 and psi >= 0:
                    pass_c += 1
                else:
                    fail_c += 1
                pname = _get_path_name(cu, cpsi, u, psi)
                paths[pname] = paths.get(pname, 0) + 1

        total = len(u_vals)
        res = {
            "total_records": len(stories),
            "scored_records": total,
            "overall_avg_reality_u": round(sum(u_vals) / total, 4) if total else 0,
            "overall_avg_reality_psi": round(sum(psi_vals) / total, 4) if total else 0,
            "overall_avg_claim_gap_delta_u": round(sum(deltas) / len(deltas), 4) if deltas else 0,
            "pass_count": pass_c,
            "fail_count": fail_c,
            "pass_rate_pct": round(pass_c / total * 100, 2) if total else 0,
            "trajectories": paths
        }
        return json.dumps(res, indent=2)

    @mcp.tool()
    def get_gap_distribution() -> str:
        """Get Claim -> Reality Gap (Delta u = claim_u - real_u) histogram distribution across the corpus."""
        stories = _load_all_stories()
        buckets = {"Negative (< 0)": 0, "0.0 - 0.2 (Honest)": 0, "0.2 - 0.5 (Moderate Spin)": 0, "0.5 - 1.0 (High Distortion)": 0, "1.0+ (Extreme Hypocrisy)": 0}
        
        for s in stories.values():
            cu, ru = s.get("claim_u"), s.get("real_u")
            if cu is not None and ru is not None:
                delta = cu - ru
                if delta < 0:
                    buckets["Negative (< 0)"] += 1
                elif delta <= 0.2:
                    buckets["0.0 - 0.2 (Honest)"] += 1
                elif delta <= 0.5:
                    buckets["0.2 - 0.5 (Moderate Spin)"] += 1
                elif delta <= 1.0:
                    buckets["0.5 - 1.0 (High Distortion)"] += 1
                else:
                    buckets["1.0+ (Extreme Hypocrisy)"] += 1
        return json.dumps(buckets, indent=2)

    @mcp.tool()
    def get_actor_hypocrisy_leaderboard(limit: int = 15) -> str:
        """Get leaderboard of political/corporate actors ranked by hypocrisy (average Delta u divergence)."""
        stories = _load_all_stories()
        actors = {}
        for s in stories.values():
            cu, ru = s.get("claim_u"), s.get("real_u")
            if cu is not None and ru is not None:
                delta = cu - ru
                for a in s.get("actors", []):
                    if not a or len(a) < 2:
                        continue
                    if a not in actors:
                        actors[a] = {"name": a, "stories": 0, "deltas": [], "real_u": []}
                    actors[a]["stories"] += 1
                    actors[a]["deltas"].append(delta)
                    actors[a]["real_u"].append(ru)

        qualified = [a for a in actors.values() if a["stories"] >= 2]
        for a in qualified:
            a["avg_delta_u"] = round(sum(a["deltas"]) / len(a["deltas"]), 3)
            a["avg_real_u"] = round(sum(a["real_u"]) / len(a["real_u"]), 3)
            del a["deltas"]
            del a["real_u"]

        qualified.sort(key=lambda x: (x["avg_delta_u"], x["stories"]), reverse=True)
        return json.dumps(qualified[:limit], indent=2)

    @mcp.tool()
    def get_outlet_hypocrisy_leaderboard(limit: int = 15) -> str:
        """Get leaderboard of news outlets/sources ranked by average narrative divergence (Delta u)."""
        stories = _load_all_stories()
        outlets = {}
        for s in stories.values():
            cu, ru = s.get("claim_u"), s.get("real_u")
            link = s.get("link", "")
            if cu is not None and ru is not None and link:
                try:
                    domain = urllib.parse.urlparse(link).netloc.lower().replace("www.", "")
                except Exception:
                    domain = "unknown"
                if domain:
                    if domain not in outlets:
                        outlets[domain] = {"domain": domain, "stories": 0, "deltas": [], "real_u": []}
                    outlets[domain]["stories"] += 1
                    outlets[domain]["deltas"].append(cu - ru)
                    outlets[domain]["real_u"].append(ru)

        qualified = [o for o in outlets.values() if o["stories"] >= 3]
        for o in qualified:
            o["avg_delta_u"] = round(sum(o["deltas"]) / len(o["deltas"]), 3)
            o["avg_real_u"] = round(sum(o["real_u"]) / len(o["real_u"]), 3)
            del o["deltas"]
            del o["real_u"]

        qualified.sort(key=lambda x: (x["avg_delta_u"], x["stories"]), reverse=True)
        return json.dumps(qualified[:limit], indent=2)

    @mcp.tool()
    def get_worst_divergence_stories(limit: int = 10) -> str:
        """Get top stories with the worst divergence between claimed intent and actual outcome."""
        stories = _load_all_stories()
        scored = []
        for s in stories.values():
            cu, ru = s.get("claim_u"), s.get("real_u")
            if cu is not None and ru is not None:
                delta = cu - ru
                scored.append({
                    "id": s.get("id"),
                    "subject": s.get("subject"),
                    "claim_u": cu,
                    "real_u": ru,
                    "delta_u": round(delta, 2),
                    "verdict": s.get("verdict")
                })
        scored.sort(key=lambda x: x["delta_u"], reverse=True)
        return json.dumps(scored[:limit], indent=2)

    @mcp.tool()
    def get_pass_stories(limit: int = 10) -> str:
        """Get top PASS stories where actual reality created positive systemic value (real_u > 0 and real_psi > 0)."""
        stories = _load_all_stories()
        passed = []
        for s in stories.values():
            ru, rpsi = s.get("real_u"), s.get("real_psi")
            if ru is not None and rpsi is not None and ru > 0 and rpsi > 0:
                passed.append({
                    "id": s.get("id"),
                    "subject": s.get("subject"),
                    "real_u": ru,
                    "real_psi": rpsi,
                    "combined_score": round(ru + rpsi, 2),
                    "verdict": s.get("verdict")
                })
        passed.sort(key=lambda x: x["combined_score"], reverse=True)
        return json.dumps(passed[:limit], indent=2)

    @mcp.tool()
    def get_policy_status(policy_slug: str = "") -> str:
        """Get tracking data from policy_ledger.json."""
        if not os.path.exists(POLICY_LEDGER_PATH):
            return json.dumps({"error": "policy_ledger.json not found."})
        try:
            with open(POLICY_LEDGER_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            policies = data.get("policies", {})
            if policy_slug:
                clean_slug = policy_slug.strip().lower()
                if clean_slug in policies:
                    return json.dumps(policies[clean_slug], indent=2)
                return json.dumps({"error": f"Policy '{policy_slug}' not found in ledger."})
            return json.dumps(data, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    @mcp.tool()
    def get_policy_report() -> str:
        """Generate a formatted plain-text policy morality & trajectory report."""
        if not os.path.exists(POLICY_LEDGER_PATH):
            return "No policy ledger data available."
        try:
            with open(POLICY_LEDGER_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            policies = data.get("policies", {})
            if not policies:
                return "Policy ledger is currently empty."

            lines = ["# ALETHEIA POLICY LEDGER REPORT", f"Updated: {data.get('last_updated', 'Unknown')}", "=" * 50]
            for slug, p in sorted(policies.items(), key=lambda x: x[1].get("story_count", 0), reverse=True):
                u = p.get("avg_real_u")
                psi = p.get("avg_real_psi")
                count = p.get("story_count", 0)
                pass_c = p.get("pass_count", 0)
                fail_c = p.get("fail_count", 0)
                lines.append(f"## {p.get('name', slug)} ({slug})")
                lines.append(f"  - Stories Audited: {count}")
                lines.append(f"  - Avg Moral Coords (υ, ψ): ({u}, {psi})")
                lines.append(f"  - Pass/Fail: {pass_c} PASS / {fail_c} FAIL")
                lines.append(f"  - First Seen: {p.get('first_seen')} | Last: {p.get('last_updated')}")
                lines.append("")
            return "\n".join(lines)
        except Exception as e:
            return f"Error generating report: {e}"

    # --- CHAT & CONVERSATION MEMORY TOOLS ---
    @mcp.tool()
    def search_chat_memory(query: str, limit: int = 5) -> str:
        """Search across stored operator memories and topic thread observations in SQLite memory store."""
        if not memory_store:
            return json.dumps({"error": "memory_store module unavailable."})
        res = memory_store.search_memories(query, limit=limit)
        return json.dumps(res, indent=2)

    @mcp.tool()
    def create_memory_observation(topic: str, observation: str, tags: str = "") -> str:
        """Save a new structured observation or takeaway to the SQLite memory store."""
        if not memory_store:
            return json.dumps({"error": "memory_store module unavailable."})
        tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
        res = memory_store.create_memory(observation, category="observation", tags=tag_list)
        return json.dumps(res, indent=2)

    @mcp.tool()
    def get_chat_session(session_id: str) -> str:
        """Get the full thread hierarchy and narrative spine for a specific chat session."""
        target_path = os.path.join(SESSIONS_DIR, f"{session_id}.json" if not session_id.endswith(".json") else session_id)
        if not os.path.exists(target_path):
            return json.dumps({"error": f"Session '{session_id}' not found."})
        try:
            with open(target_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return json.dumps({"error": str(e)})

    @mcp.tool()
    def get_narrative_spine(session_id: str) -> str:
        """Get the executive chronological summary (Narrative Spine) for a session."""
        target_path = os.path.join(SESSIONS_DIR, f"{session_id}.json" if not session_id.endswith(".json") else session_id)
        if not os.path.exists(target_path):
            return json.dumps({"error": f"Session '{session_id}' not found."})
        try:
            with open(target_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            spine = data.get("narrative_spine", [])
            return json.dumps({"session_id": session_id, "narrative_spine": spine}, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    # --- RESOURCES ---
    @mcp.resource("aletheia://registry")
    def get_registry_resource() -> str:
        """Full stories registry as JSON."""
        return json.dumps(_load_all_stories(), indent=2)

    @mcp.resource("aletheia://policy-ledger")
    def get_policy_ledger_resource() -> str:
        """Full policy tracking ledger as JSON."""
        if os.path.exists(POLICY_LEDGER_PATH):
            with open(POLICY_LEDGER_PATH, "r", encoding="utf-8") as f:
                return f.read()
        return "{}"

    @mcp.resource("aletheia://moral-report")
    def get_moral_report_resource() -> str:
        """Auto-generated morality summary report in plain text."""
        return get_policy_report()

    @mcp.resource("aletheia://memory-profile")
    def get_memory_profile_resource() -> str:
        """Global operator memory profile."""
        profile_path = os.path.join(SESSIONS_DIR, "memory_profile.json")
        if os.path.exists(profile_path):
            with open(profile_path, "r", encoding="utf-8") as f:
                return f.read()
        return "{}"


if __name__ == "__main__":
    if mcp:
        mcp.run()
    else:
        print("MCP SDK not available. Run: pip install mcp")
