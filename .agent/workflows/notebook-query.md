---
description: How to map files to NotebookLM notebooks and execute queries against them
---

This workflow directs the user and AI agents on how to map workspace files to their corresponding NotebookLM notebooks and execute targeted queries.

### 1. Locate File Mappings
To find which notebook contains a specific file, check the master registry:
- **Registry Path**: [google_notebooks_file_list.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/Semantic_Clusters/google_notebooks_file_list.md)

This file catalogs the imported sources for all primary notebooks.

### 2. Primary Notebook Registry
Here is the index of primary notebooks, their Google NotebookLM IDs, and their key thematic scopes:

| Notebook Title | Notebook ID | Key Scope / Themes |
| :--- | :--- | :--- |
| **Geometry of Definition** | `9ec890d1-e940-4811-b528-ceecf5f28287` | Foundational Actualism, Convergence Test, 7x7x7 pulse protocol, ethical geometry. |
| **Geometry of Definitions wChat** | `afa5b090-682e-47b2-9eb2-7358185c989d` | Lorentz transformations of consciousness, 42-structure hermeneutics, action-effect math. |
| **Vector Field Theory: A Unified Model of Reality** | `79d71291-8c03-4ad4-91fd-35e2832ab76f` | Unified physics, time models, lattice theory, Alethekanon master protocols, price equations. |
| **[What Was Swept Under The Rug Uncovered, The Web Of Lies Revealed]** | `b1d9ab6a-4994-4070-b49f-ad9668bb17fd` | WWSUTRU, political capture analysis (Australia/US), geopolitical & economic warfare. |
| **Metaphysics: Linguistic Relationalism & Psychology** | `14fd53eb-0497-4bf2-8ada-e44e2862673d` | Relationalism, cognitive frameworks, psychological dynamics. |
| **Information Physics & Thermodynamics** | `664250dd-ceed-4703-bc87-b46059bcb25e` | Information theory, thermal systems, entropy, mathematical physics. |
| **Metaphysics: Ontological Metaphysics & Theology** | `002010d7-d35c-48ec-b177-8a2f49aa7e76` | Being, existence, solar theology, volitional biology. |
| **Ontological Auditing & Geopolitics** | `33f7aece-10be-4dae-af2a-17c7d370ae02` | Auditing frameworks, power structures, geopolitical analysis. |
| **System Protocols & Operational Guides** | `270deb0d-d2d1-43b8-a90c-b6a1a41c58ad` | Operating manuals, AI system rules, instructions. |
| **Unstructured Notes & Chat Logs** | `df59c227-b02a-4e8b-ac52-723cc489b214` | Raw chat transcripts, brainstorm notes, logs. |

### 3. Query Strategy
When querying a notebook:
1. **Identify the Notebook**: Match your query topic to the closest theme in the table above.
2. **Double-Check Sources**: Refer to the registry to ensure the relevant files are listed in that notebook.
3. **Execute the Query**: Call the MCP tool `notebook_query` with the corresponding `notebook_id` and your natural language question.

### 4. Direct CLI Query Execution
If you are running queries via the CLI client, run:
```powershell
python "e:\Vector Field Theory\VFT Docs\_AI files and chat logs\query_notebook.py" --notebook-id "YOUR_NOTEBOOK_ID" --query "YOUR_QUESTION"
```
