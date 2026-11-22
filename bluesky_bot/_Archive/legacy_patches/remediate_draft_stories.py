# -*- coding: utf-8 -*-
"""
Remediates draft stories missing Spiritual Mode and Multi-Aspect Audits.
Applies authentic canonical Spirithekanon quotes, sub-audit posts, and aspects fields.
"""
import os
import sys
import json

stories_dir = os.path.join(os.path.dirname(__file__), "stories")

remediations = {
    "factcheck_australian-citrus-promotions-korea.json": {
        "spiritual_post": (
            "Spirithekanon:\n"
            "\"The more he does for others, the more he has; the more he gives to others, the greater his abundance.\" Tao Te Ching 81 PASS\n"
            "Genuine enterprise flourishes when grounded in mutual provision and authentic stewardship of the soil."
        )
    },
    "factcheck_cities-preparing-2026-el-nino.json": {
        "spiritual_post": (
            "Spirithekanon:\n"
            "\"For you have been a refuge to the poor, a refuge to the needy in distress, a shelter from the storm.\" Isaiah 25:4 FAIL\n"
            "True civic resilience is judged by how the vulnerable are sheltered, not by concrete walls that protect only wealth."
        )
    },
    "factcheck_andrew-bragg-super-housing.json": {
        "subaudits_post": (
            "- Coalition Pitch: FAIL (-0.86, -0.73) — Raids future security to pump asset prices.\n"
            "- Treasury & Super Funds: COND (0.30, 0.40) — Defending retirement pools but ignoring entry costs."
        ),
        "aspects": [
            {
                "aspect": "Coalition Pitch",
                "claim_u": 1.0,
                "claim_psi": 1.0,
                "real_u": -0.86,
                "real_psi": -0.73,
                "verdict": "FAIL",
                "reason": "Raids future security to pump asset prices."
            },
            {
                "aspect": "Treasury & Super Funds",
                "claim_u": 0.8,
                "claim_psi": 0.5,
                "real_u": 0.30,
                "real_psi": 0.40,
                "verdict": "COND",
                "reason": "Defending retirement pools but ignoring entry costs."
            }
        ],
        "spiritual_post": (
            "Spirithekanon:\n"
            "\"Precious treasure and oil remain in a wise man's dwelling, but a foolish man devours it.\" Proverbs 21:20 FAIL\n"
            "Raiding future retirement storehouses to subsidize inflated present assets is economic self-cannibalization."
        ),
        "combine_nuance": True
    },
    "factcheck_david_kochie_rba_letter.json": {
        "subaudits_post": (
            "- Media Rhetoric: COND (-0.47, 0.40) — Sharp public pressure, but oversimplifies monetary policy.\n"
            "- Central Bank Policy: COND (0.20, -0.40) — Holds rates steady but balances opposing political currents."
        ),
        "aspects": [
            {
                "aspect": "Media Rhetoric",
                "claim_u": 0.8,
                "claim_psi": 0.8,
                "real_u": -0.47,
                "real_psi": 0.40,
                "verdict": "COND",
                "reason": "Sharp public pressure, but oversimplifies monetary policy."
            },
            {
                "aspect": "Central Bank Policy",
                "claim_u": 0.5,
                "claim_psi": 0.5,
                "real_u": 0.20,
                "real_psi": -0.40,
                "verdict": "COND",
                "reason": "Holds rates steady but balances opposing political currents."
            }
        ],
        "spiritual_post": (
            "Spirithekanon:\n"
            "\"The one who states his case first seems right, until the other comes and examines him.\" Proverbs 18:17 COND\n"
            "Loud media finger-pointing provides theatrical catharsis, but ignores the interlocking forces driving economic strain."
        )
    },
    "factcheck_denver_office_tower_auction.json": {
        "subaudits_post": (
            "- Urban Developers: FAIL (-0.53, -0.68) — Abandoned conversion when subsidies and margins shrank.\n"
            "- Civic Redevelopment: COND (0.30, -0.20) — Sought housing revitalization but caught in debt overhang."
        ),
        "aspects": [
            {
                "aspect": "Urban Developers",
                "claim_u": 0.8,
                "claim_psi": 0.5,
                "real_u": -0.53,
                "real_psi": -0.68,
                "verdict": "FAIL",
                "reason": "Abandoned conversion when subsidies and margins shrank."
            },
            {
                "aspect": "Civic Redevelopment",
                "claim_u": 0.7,
                "claim_psi": 0.6,
                "real_u": 0.30,
                "real_psi": -0.20,
                "verdict": "COND",
                "reason": "Sought housing revitalization but caught in debt overhang."
            }
        ],
        "spiritual_post": (
            "Spirithekanon:\n"
            "\"For which of you, desiring to build a tower, does not first sit down and count the cost?\" Luke 14:28 FAIL\n"
            "Grand architectural promises collapse when speculative real estate paper cannot reconcile with physical economics."
        )
    },
    "factcheck_gus_lamont_grandmother_abduction_2026.json": {
        "subaudits_post": (
            "- Family Public Claims: FAIL (-0.80, -0.60) — Media speculation diverts focus from forensic truth.\n"
            "- Police Investigation: COND (0.20, 0.40) — Methodical forensic search hampered by conflicting narratives."
        ),
        "aspects": [
            {
                "aspect": "Family Public Claims",
                "claim_u": 0.0,
                "claim_psi": 0.5,
                "real_u": -0.80,
                "real_psi": -0.60,
                "verdict": "FAIL",
                "reason": "Media speculation diverts focus from forensic truth."
            },
            {
                "aspect": "Police Investigation",
                "claim_u": 0.5,
                "claim_psi": 0.5,
                "real_u": 0.20,
                "real_psi": 0.40,
                "verdict": "COND",
                "reason": "Methodical forensic search hampered by conflicting narratives."
            }
        ],
        "spiritual_post": (
            "Spirithekanon:\n"
            "\"The Lord is near to the brokenhearted and saves the crushed in spirit.\" Psalm 34:18 COND\n"
            "In the agony of unresolved loss, raw trauma demands profound compassionate silence over sensationalized media theater."
        )
    },
    "factcheck_jesse_gabriel_big_food.json": {
        "subaudits_post": (
            "- State Legislative Action: PASS (0.75, 0.80) — Leverages jurisdictional scale for national consumer safety.\n"
            "- Industrial Food Lobby: FAIL (-0.60, -0.40) — Fought transparency on chemical additives to shield margins."
        ),
        "aspects": [
            {
                "aspect": "State Legislative Action",
                "claim_u": 0.9,
                "claim_psi": 0.8,
                "real_u": 0.75,
                "real_psi": 0.80,
                "verdict": "PASS",
                "reason": "Leverages jurisdictional scale for national consumer safety."
            },
            {
                "aspect": "Industrial Food Lobby",
                "claim_u": 0.0,
                "claim_psi": 0.2,
                "real_u": -0.60,
                "real_psi": -0.40,
                "verdict": "FAIL",
                "reason": "Fought transparency on chemical additives to shield margins."
            }
        ],
        "spiritual_post": (
            "Spirithekanon:\n"
            "\"Why do you spend your money for that which is not bread, and your labor for that which does not satisfy?\" Isaiah 55:2 PASS\n"
            "Purging harmful chemical additives from the daily table honors the sacred responsibility to protect life over corporate profit."
        )
    },
    "factcheck_kasama_tiktok_queue_2026.json": {
        "subaudits_post": (
            "- Culinary Craft: PASS (0.80, 0.85) — Authentic Michelin hospitality grounded in genuine skill.\n"
            "- Viral Spectacle: COND (0.20, 0.50) — Transforms human waiting into algorithmically amplified voyeurism."
        ),
        "aspects": [
            {
                "aspect": "Culinary Craft",
                "claim_u": 0.9,
                "claim_psi": 0.9,
                "real_u": 0.80,
                "real_psi": 0.85,
                "verdict": "PASS",
                "reason": "Authentic Michelin hospitality grounded in genuine skill."
            },
            {
                "aspect": "Viral Spectacle",
                "claim_u": 0.5,
                "claim_psi": 0.8,
                "real_u": 0.20,
                "real_psi": 0.50,
                "verdict": "COND",
                "reason": "Transforms human waiting into algorithmically amplified voyeurism."
            }
        ],
        "spiritual_post": (
            "Spirithekanon:\n"
            "\"The eye is not satisfied with seeing, nor the ear filled with hearing.\" Ecclesiastes 1:8 PASS\n"
            "Digital spectatorship hungers endlessly for external spectacles while overlooking quiet craftsmanship right before it."
        )
    },
    "factcheck_latika-bourke-albanese-un.json": {
        "subaudits_post": (
            "- Press Gallery Framing: FAIL (-0.93, -0.87) — Sacrifices substantive geopolitical context for theatrical clicks.\n"
            "- State Leadership Response: COND (0.10, -0.40) — Rattled defense evades the underlying domestic discontent."
        ),
        "aspects": [
            {
                "aspect": "Press Gallery Framing",
                "claim_u": 0.5,
                "claim_psi": 0.8,
                "real_u": -0.93,
                "real_psi": -0.87,
                "verdict": "FAIL",
                "reason": "Sacrifices substantive geopolitical context for theatrical clicks."
            },
            {
                "aspect": "State Leadership Response",
                "claim_u": 0.6,
                "claim_psi": 0.4,
                "real_u": 0.10,
                "real_psi": -0.40,
                "verdict": "COND",
                "reason": "Rattled defense evades the underlying domestic discontent."
            }
        ],
        "spiritual_post": (
            "Spirithekanon:\n"
            "\"The tongue is a small member, yet it boasts of great things. How great a forest is set ablaze by a small fire!\" James 3:5 FAIL\n"
            "Sensational media baiting trades constructive statecraft for theatrical sparks that burn civic trust."
        )
    },
    "factcheck_nebraska-maryland-game-2026.json": {
        "subaudits_post": (
            "- Conference Scheduling: PASS (1.00, 1.00) — Clear, timely broadcast details for fans and student athletes.\n"
            "- Media Broadcasters: PASS (0.80, 0.90) — Coordinated multi-platform transmission without artificial friction."
        ),
        "aspects": [
            {
                "aspect": "Conference Scheduling",
                "claim_u": 1.0,
                "claim_psi": 1.0,
                "real_u": 1.00,
                "real_psi": 1.00,
                "verdict": "PASS",
                "reason": "Clear, timely broadcast details for fans and student athletes."
            },
            {
                "aspect": "Media Broadcasters",
                "claim_u": 0.9,
                "claim_psi": 0.9,
                "real_u": 0.80,
                "real_psi": 0.90,
                "verdict": "PASS",
                "reason": "Coordinated multi-platform transmission without artificial friction."
            }
        ],
        "spiritual_post": (
            "Spirithekanon:\n"
            "\"One who is faithful in a very little is also faithful in much.\" Luke 16:10 PASS\n"
            "Fulfilling routine civic and logistical commitments with transparent simplicity provides the steady foundation for community joy."
        )
    },
    "factcheck_northeast_airport_outage.json": {
        "subaudits_post": (
            "- Telecom Infrastructure: FAIL (-0.85, -0.83) — 50-year-old circuits lacked basic geographic redundancy.\n"
            "- Regulatory Oversight: COND (-0.20, -0.40) — Repeated warnings ignored until systemic physical failure occurred."
        ),
        "aspects": [
            {
                "aspect": "Telecom Infrastructure",
                "claim_u": 0.5,
                "claim_psi": 0.2,
                "real_u": -0.85,
                "real_psi": -0.83,
                "verdict": "FAIL",
                "reason": "50-year-old circuits lacked basic geographic redundancy."
            },
            {
                "aspect": "Regulatory Oversight",
                "claim_u": 0.6,
                "claim_psi": 0.5,
                "real_u": -0.20,
                "real_psi": -0.40,
                "verdict": "COND",
                "reason": "Repeated warnings ignored until systemic physical failure occurred."
            }
        ],
        "spiritual_post": (
            "Spirithekanon:\n"
            "\"I passed by the field of a sluggard, and behold, it was overgrown and its wall was broken down.\" Proverbs 24:30-31 FAIL\n"
            "Deferred maintenance and unhedged brittleness masquerade as fiscal prudence until fragile critical systems fail all at once."
        )
    },
    "factcheck_rba_mortgage_rate_hike_2026.json": {
        "subaudits_post": (
            "- Central Bank Strategy: FAIL (-0.84, 1.00) — Crushes indebted families to tame supply-side shocks.\n"
            "- Commercial Banks: COND (0.20, 0.50) — Pass rate hikes instantly to borrowers while lagging depositors."
        ),
        "aspects": [
            {
                "aspect": "Central Bank Strategy",
                "claim_u": 0.8,
                "claim_psi": 1.0,
                "real_u": -0.84,
                "real_psi": 1.00,
                "verdict": "FAIL",
                "reason": "Crushes indebted families to tame supply-side shocks."
            },
            {
                "aspect": "Commercial Banks",
                "claim_u": 0.5,
                "claim_psi": 0.6,
                "real_u": 0.20,
                "real_psi": 0.50,
                "verdict": "COND",
                "reason": "Pass rate hikes instantly to borrowers while lagging depositors."
            }
        ],
        "spiritual_post": (
            "Spirithekanon:\n"
            "\"You are exacting interest, each from his brother. I held a great assembly against them.\" Nehemiah 5:7 FAIL\n"
            "Disciplining national balance sheets by crushing everyday households under escalating interest breaches fundamental solidarity."
        )
    },
    "factcheck_rohan-dennis-judge-recusal-argument.json": {
        "subaudits_post": (
            "- Defense Strategy: COND (0.42, -0.75) — Tactical procedural motion to seek more favorable bench.\n"
            "- Judicial Process: PASS (0.80, 0.70) — Upholds standard continuity where trial judge oversees breaches."
        ),
        "aspects": [
            {
                "aspect": "Defense Strategy",
                "claim_u": 0.5,
                "claim_psi": -0.5,
                "real_u": 0.42,
                "real_psi": -0.75,
                "verdict": "COND",
                "reason": "Tactical procedural motion to seek more favorable bench."
            },
            {
                "aspect": "Judicial Process",
                "claim_u": 0.9,
                "claim_psi": 0.8,
                "real_u": 0.80,
                "real_psi": 0.70,
                "verdict": "PASS",
                "reason": "Upholds standard continuity where trial judge oversees breaches."
            }
        ],
        "spiritual_post": (
            "Spirithekanon:\n"
            "\"You shall not pervert justice. You shall not show partiality, nor take a bribe.\" Deuteronomy 16:19 PASS\n"
            "The integrity of the law rests on unwavering impartiality, indifferent to legal maneuvers or celebrity stature."
        )
    },
    "factcheck_tasmania-community-organisations-under-pressure.json": {
        "subaudits_post": (
            "- Community Non-Profits: PASS (0.80, -0.40) — Exhausting reserves to keep vulnerable citizens afloat.\n"
            "- State Grant Funding: FAIL (-0.67, -1.00) — Sub-inflation indexation starves frontline frontline care."
        ),
        "aspects": [
            {
                "aspect": "Community Non-Profits",
                "claim_u": 0.9,
                "claim_psi": 0.5,
                "real_u": 0.80,
                "real_psi": -0.40,
                "verdict": "PASS",
                "reason": "Exhausting reserves to keep vulnerable citizens afloat."
            },
            {
                "aspect": "State Grant Funding",
                "claim_u": 0.6,
                "claim_psi": 0.0,
                "real_u": -0.67,
                "real_psi": -1.00,
                "verdict": "FAIL",
                "reason": "Sub-inflation indexation starves frontline frontline care."
            }
        ],
        "spiritual_post": (
            "Spirithekanon:\n"
            "\"Do not withhold good from those to whom it is due, when it is in your power to act.\" Proverbs 3:27 FAIL\n"
            "A society that withholds essential operating funds from community lifelines abandons its most fragile neighbors."
        )
    },
    "factcheck_texas-abortion-ban-tierra-walker.json": {
        "subaudits_post": (
            "- State Statute Exceptions: FAIL (-1.00, -1.00) — Legislative traps criminalize urgent lifesaving clinical care.\n"
            "- Hospital Legal Risk Management: FAIL (-0.80, -0.70) — Corporate liability fears prioritized over patient survival."
        ),
        "aspects": [
            {
                "aspect": "State Statute Exceptions",
                "claim_u": 1.0,
                "claim_psi": 1.0,
                "real_u": -1.00,
                "real_psi": -1.00,
                "verdict": "FAIL",
                "reason": "Legislative traps criminalize urgent lifesaving clinical care."
            },
            {
                "aspect": "Hospital Legal Risk Management",
                "claim_u": 0.0,
                "claim_psi": 0.0,
                "real_u": -0.80,
                "real_psi": -0.70,
                "verdict": "FAIL",
                "reason": "Corporate liability fears prioritized over patient survival."
            }
        ],
        "spiritual_post": (
            "Spirithekanon:\n"
            "\"If you had known what this means, 'I desire mercy, and not sacrifice,' you would not have condemned the guiltless.\" Matthew 12:7 FAIL\n"
            "Rigid ideological legalism that abandons dying mothers makes a mockery of protecting life."
        )
    },
    "factcheck_trump_white_house_speech_ban_2026.json": {
        "subaudits_post": (
            "- Executive Retaliation: FAIL (-0.98, -0.96) — Uses official state apparatus to punish critical coverage.\n"
            "- Media Solidarity Blackout: COND (0.20, 0.40) — Defends press freedoms but deprives public of direct record."
        ),
        "aspects": [
            {
                "aspect": "Executive Retaliation",
                "claim_u": 0.0,
                "claim_psi": 0.5,
                "real_u": -0.98,
                "real_psi": -0.96,
                "verdict": "FAIL",
                "reason": "Uses official state apparatus to punish critical coverage."
            },
            {
                "aspect": "Media Solidarity Blackout",
                "claim_u": 0.5,
                "claim_psi": 0.5,
                "real_u": 0.20,
                "real_psi": 0.40,
                "verdict": "COND",
                "reason": "Defends press freedoms but deprives public of direct record."
            }
        ],
        "spiritual_post": (
            "Spirithekanon:\n"
            "\"Everyone who does evil hates the light, and will not come into the light for fear that their deeds will be exposed.\" John 3:20 FAIL\n"
            "Silencing dissenting questions reveals an acute fear of transparency that erodes legitimate authority."
        )
    },
    "factcheck_wa_prisons_closing_the_gap.json": {
        "subaudits_post": (
            "- WA Justice Infrastructure: FAIL (-0.93, -0.85) — Pours capital into cells while starving community diversion.\n"
            "- Closing the Gap Targets: COND (0.10, -0.60) — Paper commitments broken by carceral budget allocations."
        ),
        "aspects": [
            {
                "aspect": "WA Justice Infrastructure",
                "claim_u": 0.5,
                "claim_psi": 0.8,
                "real_u": -0.93,
                "real_psi": -0.85,
                "verdict": "FAIL",
                "reason": "Pours capital into cells while starving community diversion."
            },
            {
                "aspect": "Closing the Gap Targets",
                "claim_u": 0.9,
                "claim_psi": 0.5,
                "real_u": 0.10,
                "real_psi": -0.60,
                "verdict": "COND",
                "reason": "Paper commitments broken by carceral budget allocations."
            }
        ],
        "spiritual_post": (
            "Spirithekanon:\n"
            "\"Is not this the fast that I choose: to loose the bonds of wickedness, to undo the straps of the yoke?\" Isaiah 58:6 FAIL\n"
            "Building new cages while sacred treaties of equality go backwards deepens ancestral injustice instead of healing it."
        )
    }
}

def remediate_all():
    remediated_count = 0
    for filename, rem in remediations.items():
        filepath = os.path.join(stories_dir, filename)
        if not os.path.exists(filepath):
            print(f"[SKIP] File not found: {filename}")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        is_list = isinstance(data, list)
        story = data[0] if is_list else data
        posts = story.get("posts", [])

        # 1. Handle subaudits insertion if missing
        if "subaudits_post" in rem:
            subaudits_text = rem["subaudits_post"]
            if rem.get("combine_nuance"):
                # andrew-bragg had bright side and poison split across post 5 and 6
                # posts: [0:hook, 1:claim, 2:reality, 3:verdict, 4:context, 5:bright, 6:poison, ...]
                context_post = posts[4]
                bright_post = posts[5]
                poison_post = posts[6]
                combined_nuance = f"{bright_post.strip()}\n\n{poison_post.strip()}"
                remaining_posts = posts[7:]
                posts = posts[:4] + [subaudits_text, context_post, combined_nuance] + remaining_posts
            else:
                # Normal 13 post structure: insert subaudits at index 4
                posts.insert(4, subaudits_text)

        # 2. Add aspects field
        if "aspects" in rem:
            story["aspects"] = rem["aspects"]
            story["multiAspect"] = True

        # 3. Add Spirithekanon post
        spiritual_text = rem.get("spiritual_post")
        if spiritual_text:
            # Check if spiritual post is already present
            if not any("spirithekanon" in p.lower() for p in posts):
                posts.append(spiritual_text)

        # Validate post counts and lengths
        story["posts"] = posts
        
        # Verify length of every post
        for p_idx, p in enumerate(posts):
            if len(p) > 295:
                print(f"  [WARN] {filename} post[{p_idx}] length is {len(p)} (> 295 chars)")

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([story] if is_list else story, f, indent=2, ensure_ascii=False)

        print(f"[REMEDIATED] {filename} -> {len(posts)} posts | Aspects: {bool(story.get('aspects'))} | Spiritual: {any('spirithekanon' in p.lower() for p in posts)}")
        remediated_count += 1

    print(f"\nRemediation complete! Processed {remediated_count} files.")

if __name__ == "__main__":
    remediate_all()
