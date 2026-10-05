# Implementation Plan - Manual Remediation of 17 Draft Stories

## Overview
17 draft stories in `bluesky_bot/stories/` were generated with "Enable Spiritual Mode" and "Enable Multi-Aspect Audit" unchecked.
This plan outlines the manual remediation process to:
1. Formulate structured Multi-Aspect sub-audits (`aspects` array and Post 4 `Sub-Audits Breakdown:`) for the 15 stories missing multi-aspect audits.
2. Formulate authentic canonical Spiritual Audits (`Spirithekanon:` post) with verified scripture / wisdom citations strictly under 280 characters for all 17 stories.
3. Update each draft JSON file in place, ensuring full schema compliance, valid coordinates, and correct post sequence (15 posts total).

## Stories to Remediate (17 Total)
1. `factcheck_andrew-bragg-super-housing.json`
2. `factcheck_australian-citrus-promotions-korea.json` (add Spirithekanon)
3. `factcheck_cities-preparing-2026-el-nino.json` (add Spirithekanon)
4. `factcheck_david_kochie_rba_letter.json`
5. `factcheck_denver_office_tower_auction.json`
6. `factcheck_gus_lamont_grandmother_abduction_2026.json`
7. `factcheck_jesse_gabriel_big_food.json`
8. `factcheck_kasama_tiktok_queue_2026.json`
9. `factcheck_latika-bourke-albanese-un.json`
10. `factcheck_nebraska-maryland-game-2026.json`
11. `factcheck_northeast_airport_outage.json`
12. `factcheck_rba_mortgage_rate_hike_2026.json`
13. `factcheck_rohan-dennis-judge-recusal-argument.json`
14. `factcheck_tasmania-community-organisations-under-pressure.json`
15. `factcheck_texas-abortion-ban-tierra-walker.json`
16. `factcheck_trump_white_house_speech_ban_2026.json`
17. `factcheck_wa_prisons_closing_the_gap.json`

## Verification
- Verify each file has exactly 15 posts (or 14/15 structured), all under character limits.
- Verify `generate_compact_info_card()` renders without errors for each file.
- Verify running Launcher process is untouched.
