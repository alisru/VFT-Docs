# Workspace Rules

## Brain Step Output Rule

When any tool call returns the message:
> "The output was large and was saved to: file:///C:/Users/hungh/.gemini/antigravity/brain/..."

**Immediately** run a `Copy-Item` to copy that file to the active project folder with a descriptive name, **before** reading or acting on the content:

```powershell
Copy-Item "C:\Users\hungh\.gemini\antigravity\brain\<conv-id>\.system_generated\steps\N\output.txt" `
  "e:\Vector Field Theory\VFT Docs\<active-project-path>\fetch_<description>_<YYYYMMDD>.json"
```

Rules:
- Filename must be descriptive (e.g. `fetch_shangri_la_2023.json`, `search_matildas_speech.json`)
- Destination is the **active project folder** — not drawing_board, not a temp folder, not the brain
- Copy happens **before** reading — so the file exists even if the session is interrupted or quota-crashed
- After copying, also extract key quotes/URLs into the project's `sources_raw.md` as a human-readable record


## Absolute Ban on Implicit Deletion
You must NEVER run destructive commands (e.g., `Remove-Item`, `rm -rf`, deleting folders) based on implicit instructions, frustration, or requests to "clean up."
If the user says "I hate this folder," "unfuck this," or "clean this up," you must ASSUME they want to fix the contents or move files, NOT delete them.
To delete a file or folder, you must explicitly present the exact `Remove-Item` command you plan to run and wait for the user to reply with an unambiguous "Yes, delete it" before executing.

## Skill Path Synchronization Priority
If a user is actively discussing or complaining about a specific `SKILL.md` file, or if they provide a specific file path to a skill, you MUST immediately compare that path against the system-loaded customization root (e.g., `.agents/skills/`).
If the paths differ (e.g., the user is editing a local copy in their active project directory), the user's local copy is the GROUND TRUTH. You must instantly diff them, acknowledge the discrepancy, and ask if the system `.agents` version should be overwritten with their local version before proceeding with the task.
Never argue with the user about a skill's contents without first verifying you are both looking at the exact same file path.


## Strict Adherence to Designated Skill Tools
If a `SKILL.md` file explicitly lists specific local scripts or tools to use (e.g., "Local Sourcing Tools" like `query_hansard_corpus.py`), you MUST use them.
Do NOT attempt to write your own custom Python web scrapers, `curl` commands, or ad-hoc API scripts to bypass or replicate the designated tools. Relying on the project's established infrastructure is mandatory.

## Absolute Ban on Generic Citations
When a task or skill requires a citation (especially Kanon Audits), you must NEVER use a generic root domain (e.g., `https://www.pm.gov.au`) as a placeholder. You must cite the *most specific URL* containing the claim.
If your standard tools (like `search_web`) obscure the direct URL behind redirects, you must pivot to raw tools (like `Parallel-Search-MCP web_search`), local scraping scripts, or **browser use tools** to obtain the exact URL. If you cannot find the specific page, explicitly report the failure in the chat; do not manufacture a generic link to force a passing state.

## Subagent Delegation Ban for Rigid Workflows
Do NOT delegate strict, format-heavy tasks like `/kanon-audit` to subagents.
Subagents suffer from context amnesia and routinely fail to uphold rigid formatting invariants (like footnote markers, specific node headers, and coordinate syntax). These workflows must be executed manually and methodically in the main chat, where the primary model can maintain total control over the output quality and structure.

## Token Conservation and Search Cessation Rule
- **Immediate Stop on Success**: If you are searching for a quote, fact, or source to validate a statement or node, and any search result excerpt contains a valid, direct, and verifiable quote or the necessary info, you MUST STOP searching immediately. Do NOT run additional searches, browser visits, or fetches to "double-check" or get full context if the excerpt has a verbatim, attributed block of text.
- **Write Node Immediately**: You MUST write the completed node(s) to the target markdown file on disk *before* initiating any new search query or tool call for subsequent nodes. Never chain multiple search queries for different nodes in a single turn.
- **No Redundant Fetches**: Do not run additional web searches or `web_fetch`/browser visits to retrieve the full page just to verify the quote if the excerpt already contains a verbatim, attributed block of text that satisfies the criteria.
- **Execute Immediately**: Proceed directly to editing the files or completing the task with the data already in your context. Do not write multiple search queries in series if the first ones have already yielded candidate matches.
- **Absolute Ban on Serial Searches**: You are strictly prohibited from executing consecutive web searches in series across turns to refine results. Design one parallel query and run it once.
- **Mandatory Full File Inspection**: When any search/fetch is saved to a large file on disk, you are banned from searching again until you have inspected the entire file (using offsets if truncated) or run local grep searches on it to confirm the information is not there.
- **Local-First Sourcing**: For parliamentary or legislative nodes, you must search the local `albanese_corpus.jsonl` first. Local python runs cost zero API/web tokens.
- **No Memory-Based Proposing**: Never propose or draft any citation, URL, or date in the chat based on training-data memory without first validating it using a tool.

## Kanon Audit Execution Rules
- **Anti-Overproofing**: Keep the Actuality section focused strictly on the primary, most direct, and verifiable action(s) needed to prove the vector verdict (e.g., the Robodebt Royal Commission for the Royal Commission vector). Do not pull in unrelated secondary examples, recent debates, or additional cases just to "overprove" the point.
- **Verify Full Timelines**: If you must include a historical detail, you must verify the full timeline of the action. Do not report an initial refusal or statement as a final position if subsequent events or policy reversals occurred.
- **Hypothesis Generation Prompting**: Before generating a hypothesis or searching for any node, you must explicitly write down and evaluate the following question in your internal thoughts:
  `"How does [actor] hit or miss [whole node JSON text] in a quote?"`
  Include the complete, unredacted JSON object of the node in this question.
- **Corpus-First Auditing**: Build/reference the actor's source corpus up front, and search only for genuine gaps. Archive fetched text locally so re-reading a source later costs zero tool calls. Sourcing must target specific primary documents (Hansard, official speeches, policy platform pages) matched to the claim type.

## Sourcing and Verification Efficiency Guidelines
- **Absolute Ban on Ad-hoc Throwaway Scripts**: You are strictly prohibited from writing temporary, throwaway Python or PowerShell scripts in the workspace to perform simple checks (e.g. redirect resolution, keyword grepping, or parsing local JSON search results). Use direct, native tools (like `Parallel-Search-MCP` or standard shell commands) instead. Only write scripts for complex data migrations or when explicitly requested by the user.
- **Mandatory Parallel Search Consolidation**: If multiple search queries or URLs need to be fetched/searched, you must consolidate them into a single call to `Parallel-Search-MCP` (using the `search_queries` or `urls` array) rather than executing multiple sequential calls to `search_web` or `web_fetch`.
- **Maximum 5-Step Execution Cap**: Limit your turns to a maximum of 5 tool steps when investigating a single node. If you find yourself chaining multiple commands, scripts, and checks, stop and simplify your workflow.

## Quote Sourcing & Search Formulation Rules
- **No Poetic/Literal Search Strings**: Never query search engines or corpora using the poetic or historical name of a Kanon vector (e.g. "Weird Melancholy", "The Sunburnt Country", "The Never-Never"). You must translate the vector's underlying structural mechanism into its modern political/policy equivalents (e.g. postcode inequality, natural disasters, transition delays) before searching.
- **Local Database Sourcing Priority**: For any quote validation, you must search the local database (`albanese_corpus.jsonl` or `.parquet`) first using standard local commands before running any web searches.
- **Batch Verification URL Consolidation**: When fetching external source URLs for validation, always combine all URLs into a single parallel call to `Parallel-Search-MCP` (`web_fetch`) rather than running multiple sequential fetches across turns.
