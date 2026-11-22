# Semantic Gluon Project Manager MCP Implementation Plan

## Objective
Upgrade the existing prototypes in `semantic-gluon-bundle` into a unified, battle-tested, production-grade Model Context Protocol (MCP) server for project management that:
1. Implements the 8-vertex modal topology (`will_be`, `can_be`, `may_be`, `is_like`, `is_not`, `cant_be`, `wont_be`, `was_like`, and ground truth `is`).
2. Implements Comparative Goal Anchoring (`anchor-comparative` & `verify-comparative` for grounding vague goals like "better" against empirical baselines and taboo boundaries).
3. Connects robust SQLite relational persistence with real-time JSON sync and export.
4. Auto-detects opposition vector collisions (`will_be` vs `cant_be`, `can_be` vs `is_not`, etc.) with automatic status cancellation and boundary defense.
5. Exposes a comprehensive toolset compliant with MCP specifications (JSON-RPC 2.0 stdio).
6. Registers the MCP server into Antigravity configuration and generates matching tool schemas.

## Architecture & File Structure
- `semantic_project_db.py`: Core database and domain logic engine (SQLite + JSON sync).
- `mcp-server/semantic_gluon_mcp.py`: Production-grade JSON-RPC 2.0 MCP server wrapping the database engine.
- `skills/gemini-project-manager/SKILL.md`: Synchronized skill instructions for the agent.
- `C:\Users\hungh\.gemini\config\mcp_config.json`: Global MCP server registration.
- `C:\Users\hungh\.gemini\antigravity\mcp\semantic-gluon\`: Schema files for lazy loading tools.
