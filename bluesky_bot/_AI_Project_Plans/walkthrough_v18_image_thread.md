# Mobile-Optimized Split Verdict (1-3) & Analysis (4-13) Infographic Walkthrough

We have updated the visual card engine to output the story in a highly-readable two-part split format optimized for mobile timelines. This includes:
1.  **Card 1: Core Verdict Card (1-3)**: Focuses strictly on Hook, Claim, Reality, and Verdict, showing the coordinate details in the subtitle.
2.  **Card 2: System Analysis & Perspectives Card (4-13)**: Groups Context, Nuance, Breakdown, Social Physics, Trajectory, and Unavoidables alongside the Trinary Perspectives reactions at the bottom, matching the classic unified structure but with a 3px font size bump.

---

## Alt Text & Metadata Integration
*   The **Resulting Judgement Coordinates** `(v, psi) — Zone Anchor | Verdict Status` are dynamically extracted from the story data and embedded directly into the visual headers.
*   The bot automatically uploads both images alongside the Trajectory Graph, creating a neat 3-image swipeable layout in the Bluesky feed.

Below is the swipeable carousel showing the new split cards:

````carousel
![Part 1: Core Verdict Card](C:/Users/hungh/.gemini/antigravity/brain/b3441d49-6c57-4a6f-80a8-7437cd18cea1/orchids_bloom_wa_wildflowers_info_card_verdict.png)
<!-- slide -->
![Part 2: Analysis & Perspectives Card](C:/Users/hungh/.gemini/antigravity/brain/b3441d49-6c57-4a6f-80a8-7437cd18cea1/orchids_bloom_wa_wildflowers_info_card_analysis.png)
````

---

## Legacy Unified Card Layout (Option A)
The classic 2-column grid visual is still generated to maintain backwards compatibility with dashboards and external index displays:

![Unified Card Layout](C:/Users/hungh/.gemini/antigravity/brain/b3441d49-6c57-4a6f-80a8-7437cd18cea1/orchids_bloom_wa_wildflowers_info_card.png)
