# Infographic Card Mobile Optimization Walkthrough

We have added support for generating both a **Single Unified 13-Element Card** and **Three Slipped Cards** optimized for mobile viewports without needing pinch-to-zoom.

---

## 1. Split Image Mobile Layout (Option B)
Each section is drawn in a single-column container spanning the full width of the canvas (1200px width). This allows the text to wrap at 1060px, doubling the legibility on mobile devices.

The three generated split cards are:
1.  **Part 1: Core Verdict**: Includes Hook, Claim, Reality, Verdict, and Context.
2.  **Part 2: System Analysis**: Includes Nuance, Breakdown, Social Physics, Trajectory, and The Unavoidables.
3.  **Part 3: Perspective Reactions**: Includes Alethekanon, Awwthekanon, and Brothekanon reaction blocks side-by-side.

Below is the swipeable carousel showing how these split cards render:

````carousel
![Part 1: Core Verdict](C:/Users/hungh/.gemini/antigravity/brain/b3441d49-6c57-4a6f-80a8-7437cd18cea1/orchids_bloom_wa_wildflowers_info_card_core.png)
<!-- slide -->
![Part 2: System Analysis](C:/Users/hungh/.gemini/antigravity/brain/b3441d49-6c57-4a6f-80a8-7437cd18cea1/orchids_bloom_wa_wildflowers_info_card_analysis.png)
<!-- slide -->
![Part 3: Perspective Reactions](C:/Users/hungh/.gemini/antigravity/brain/b3441d49-6c57-4a6f-80a8-7437cd18cea1/orchids_bloom_wa_wildflowers_info_card_perspectives.png)
````

---

## 2. Legacy Unified Card Layout (Option A)
The classic 2-column grid visual is still generated to maintain backwards compatibility with dashboards and external index displays:

![Unified Card Layout](C:/Users/hungh/.gemini/antigravity/brain/b3441d49-6c57-4a6f-80a8-7437cd18cea1/orchids_bloom_wa_wildflowers_info_card.png)
