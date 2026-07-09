---
trigger: always_on
glob: "*"
description: Rules to enforce strict token conservation, prevent serial web searching, and stop unverified generation of sources.
---

# Token Conservation and Search Cessation Rules

## 1. Absolute Ban on Serial Web Searches
* You must **NEVER** run consecutive web searches in series (one after another in separate turns) to "tweak" or "refine" results.
* If a search is needed, design a single, comprehensive parallel search query containing all the necessary queries at once.
* Once a search is executed, you are strictly prohibited from running another search until you have exhausted the local results.

## 2. Mandatory Full File Inspection
* When a search or fetch output is saved to a large file, you **MUST** read and inspect the entire content.
* If the view is truncated, you must use offsets (`ContentOffset` or line ranges) to read the rest of the file or use `grep_search` / local python scripts to inspect it fully.
* You are banned from running a new search query if the answer was already present in any part of the saved search/fetch files on disk.

## 3. Local-First Sourcing (Hansard and Databases)
* If the topic of the audit node is parliamentary, legislative, or official speeches, you **MUST** query the local corpus (`albanese_corpus.jsonl` or similar) using local Python search tools first.
* Do not use external web search for events or quotes that can be verified in the local corpus. Local python runs cost zero API/web tokens.

## 4. No Hallucinated/Memory-Based Proposals
* You are strictly prohibited from proposing or drafting any citation, URL, title, or date in the chat from your training-data memory.
* Every citation must be verified on disk before being shown to the user or written to the audit document.
