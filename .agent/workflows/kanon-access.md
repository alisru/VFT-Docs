---
description: How to initialize, validate, and export National Kanon files using the official schema.
---

# Kanon Access Workflow

This workflow outlines the standard procedure for creating and managing a National Kanon using the JSON-first methodology.

## Prerequisites

- Python 3.x
- `jsonschema` library (`pip install jsonschema`)

## 1. Initialize a New Kanon

To start a new analysis for a nation, initialize a JSON file from the template.

```powershell
cd "e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU"
python kanon_manager.py init [NationName]
```

*Example:* `python kanon_manager.py init Canada` -> Creates `Canada_Kanon.json`.
*   **Automatic Interrogative Injection:** The system automatically parses `interrogative_7x7x7_semantic.md` and prepopulates every item with its unique 7x7x7 Interrogative Question (e.g., "(Who.Who.Who)" -> "Which specific identity is being identified?"). This ensures semantic precision from the start.

## 2. Edit the JSON File

Open the generated JSON file in your editor. Fill in the data following the schema structure.
- **Planes**: Ensure all 7 Planes (Who-Effect) are present.
- **Senses**: Ensure all 7 Senses (q1-q7) are present within each Plane.
- **Items**: Ensure all 7 Vectors are present within each Sense.
- **Narratives**: Provide comprehensive narratives for each Sense and the Plane Totality.

## 3. Validate the Data

Run the validation command frequently to check for schema errors and semantic compliance (e.g., sentence counts).

```powershell
python kanon_manager.py validate [NationName]_Kanon.json
```

*   **Schema Errors:** Invalid structure or missing required fields.
*   **Semantic Warnings:** Narratives too short, missing "This establishes..." formula, etc.

## 4. Export to Markdown

Once validation passes (or is acceptable), export the data to the standard Markdown format (`[Nation]_Kanon_Plane_X_....md`).

```powershell
python kanon_manager.py export [NationName]_Kanon.json --output [OutputDirectory]
```

*   If no output directory is specified, files are generated in the current directory.
*   These Markdown files are the "Gold Standard" source for the site generator.
*   **Interrogative Context:** The exporter automatically injects the corresponding question as a blockquote (`> **Q:** *Question?*`) above the Context Analysis in the Markdown, providing direct guidance for the quote selection and analysis.

## 5. Generate the Site (Optional)

After exporting to Markdown, you can run the site generator (if configured for your nation) to build the HTML visualization.

```powershell
python generate_kanon_site.py
```
