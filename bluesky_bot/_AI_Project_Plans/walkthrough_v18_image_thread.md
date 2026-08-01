# Compact Posting Modes (Thread & Single-Post) Walkthrough

We have successfully implemented and verified both **Compact Thread Mode** and **Compact Single-Post Mode** with **On-the-Fly Image Conversion** across the entire Bluesky bot pipeline.

---

## 1. Compact Thread Mode (4-Post Thread)
*   **Structure**: Posts 1 to 4 are published as native text posts (Hook, Claim, Reality, Verdict).
*   **Embeds**:
    *   Post 1 (Hook): Trajectory Graph PNG.
    *   Post 2 (Claim): Link Preview Card (external embed).
    *   Post 4 (Verdict): Compact 6-Card Infographic PNG (Context, Nuance, Breakdown, Social Physics, Trajectory, Unavoidables) + Persona Reactions.
*   **Layout**: 6 sections arranged in a 2-column grid (3 left, 3 right) + 3 side-by-side persona blocks.

---

## 2. Compact Single-Post Mode (1-Post Feed Item)
*   **Structure**: Only a single post (Hook) is published on the timeline.
*   **Embeds**: Both the **Trajectory Graph** and the **9-Card Visual Infographic** are attached to this single post as a joint image embed.
*   **Reference Links**: The external article URL is appended directly to the first post text (e.g. `Reference: <link>`) and parsed as a clickable link facet, fitting within the 299 character limit.
*   **Layout**: The Claim, Reality, and Verdict text are prepended as visual cards at the start of the columns inside the infographic.
    *   **Left Column (5 Cards)**: Claim, Reality, Verdict, Context, Nuance.
    *   **Right Column (4 Cards)**: Breakdown, Social Physics, Trajectory, The Unavoidables.
    *   **Bottom Row (3 Columns)**: Alethekanon, Awwthekanon, and Brothekanon persona reactions aligned horizontally with equal heights.

Below is the newly rendered 9-card visual infographic generated for our most recent story `factcheck_bill_wilson_obituary.json` in Compact Single Mode:

![Infographic Card Single Post Mode Layout](C:/Users/hungh/.gemini/antigravity/brain/b3441d49-6c57-4a6f-80a8-7437cd18cea1/bill_wilson_obituary_single_info_card.png)
