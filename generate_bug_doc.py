import json
import re

with open(r"e:\Vector Field Theory\VFT Docs\formatting_bug_prompts.json", "r", encoding="utf-8") as f:
    items = json.load(f)

# Categories
cat_black_bar = []
cat_tiles_unreadable = []
cat_content_disjointed = []
cat_contrast_classic_blue = []
cat_readable_scaling = []
cat_fit_header_collapse = []

for it in items:
    txt = it["content"]
    low = txt.lower()
    
    if any(k in low for k in ["black bar", "black fucking bar", "black image bar", "black on black", "black cover"]):
        cat_black_bar.append(it)
    if any(k in low for k in ["tiles mode", "tiles has", "tiles thing", "white text white bg", "white on white", "image files tiles"]):
        cat_tiles_unreadable.append(it)
    if any(k in low for k in ["content mode", "disjointed"]):
        cat_content_disjointed.append(it)
    if any(k in low for k in ["classic blue", "black on black", "white on colored", "black on white text"]):
        cat_contrast_classic_blue.append(it)
    if any(k in low for k in ["readable", "scaling", "scale up", "camzoom", "zoom into the folder"]):
        cat_readable_scaling.append(it)
    if any(k in low for k in ["fit shrinks", "'fit' shrinks", "header eats", "spawn on top", "rooms spawn", "overlapping on folders", "bridge buttons overlapping"]):
        cat_fit_header_collapse.append(it)

doc = []
doc.append("# Comprehensive Audit: Formatting, Contrast & View Mode Failures")
doc.append("")
doc.append("> **Authoritative Historical Record of User Demands & Agent Failures**")
doc.append("> Generated from raw conversation transcripts (`transcript.jsonl`) to track every repeated complaint, verbatim user instruction, failure frequency count, and the exact architectural root causes.")
doc.append("")
doc.append("---")
doc.append("")
doc.append("## Executive Summary of Failure Counts")
doc.append("")
doc.append("| Bug Category | User Complaints Count | Core Symptom | Root Cause |")
doc.append("|---|:---:|---|---|")
doc.append(f"| **1. Black Bar on Images in Details/List** | **{len(cat_black_bar)}** | Horizontal solid black/charcoal rectangle across the row for files with thumbnails | Un-scoped `.row.item.has-thumb` / `.room-item.has-thumb .c-name` background leaking into table rows |")
doc.append(f"| **2. White-on-White Ghost Text in Tiles** | **{len(cat_tiles_unreadable)}** | Filename invisible on white/light tile cards | Indiscriminate `.has-thumb .nm` forced to white text on white tile cards |")
doc.append(f"| **3. Disjointed / Misaligned Icons in Content Mode** | **{len(cat_content_disjointed)}** | Image thumbnails squished, tiny, offset, or floating, pushing text out of column alignment | Grid-mode thumbnail CSS (`object-fit`, `width: 100%`) colliding with Content flex container |")
doc.append(f"| **4. Broken Color & Surface Contrast (Classic Blue)** | **{len(cat_contrast_classic_blue)}** | Black text on dark rooms, white text on white rooms, inverse contrast failure | Blindness to surface type (room floor vs card vs image banner); blanket CSS overrides |")
doc.append(f"| **5. Readable Mode & Zoom Text Scaling Blowout** | **{len(cat_readable_scaling)}** | Text blown up to 100px or tiny 4px; rooms stretching to 1400px pillars | Font-size formula desync between camera zoom, container overflow, and room height |")
doc.append(f"| **6. Fit Shrink, Header Overlap & Room Collisions** | **{len(cat_fit_header_collapse)}** | Fit button collapsing rooms; header wrapping over controls; rooms overlapping | Adding `height: auto !important` breaking JS collision engine and layout caches |")
doc.append("")
doc.append("---")
doc.append("")

def render_category(title, cat_items, desc):
    doc.append(f"## {title} (Total Complaints: {len(cat_items)})")
    doc.append("")
    doc.append(f"**Issue Description:** {desc}")
    doc.append("")
    for i, it in enumerate(cat_items, 1):
        doc.append(f"### Complaint #{i} — Step {it['step']} ({it['created']})")
        doc.append("```")
        doc.append(it["content"])
        doc.append("```")
        doc.append("")
    doc.append("---")
    doc.append("")

render_category(
    "1. Black Bar on Images in Details & List View",
    cat_black_bar,
    "Solid black or charcoal rectangle painted across the entire row or name column for any image/video file in Details and List views, rendering text unreadable or visually deformed."
)

render_category(
    "2. White-on-White / Unreadable Text in Tiles Mode",
    cat_tiles_unreadable,
    "Files with thumbnails in Tiles mode displaying invisible or ghosted white text on white card surfaces, with black drop shadow halos instead of crisp black text on white."
)

render_category(
    "3. Disjointed / Misaligned Icons in Content Mode",
    cat_content_disjointed,
    "In Content view, normal text documents have a clean 32px icon, but image files have irregular, squished, offset, or floating thumbnails that break row alignment and dislocate text."
)

render_category(
    "4. Surface Contrast Inversion (Peek Classic Blue & Palettes)",
    cat_contrast_classic_blue,
    "Repeated failure to enforce the invariant: Black text on white/light surfaces, White text on dark/colored surfaces. Hardcoded CSS color overrides repeatedly inverted contrast."
)

render_category(
    "5. Readable Mode Text Scaling & Room Pillar Expansion",
    cat_readable_scaling,
    "Scaling text based on camera zoom caused rooms to stretch into 1,400px towers, breaking room collision math, causing massive frame drops, or leaving text unreadable when zoomed out."
)

render_category(
    "6. Fit Shrink, Header Button Overlap & Collision Breaking",
    cat_fit_header_collapse,
    "Auto-fit button shrinking rooms instead of expanding them; header text expansion wrapping and displacing room action buttons; rooms spawning directly on top of each other."
)

with open(r"e:\Vector Field Theory\VFT Docs\FORMATTING_AND_VIEW_BUGS_RECORD.md", "w", encoding="utf-8") as f:
    f.write("\n".join(doc))

with open(r"E:\Vector Field Theory\peek_explorer\docs\FORMATTING_AND_VIEW_BUGS_RECORD.md", "w", encoding="utf-8") as f:
    f.write("\n".join(doc))

print("Document generated successfully in both locations.")
