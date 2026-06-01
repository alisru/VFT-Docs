import os
import sys
import json

# Ensure parent directory is in path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(os.path.join(parent_dir, "bluesky_bot"))

from generate_graph import draw_graph
from aletheia_bot import save_and_sync_story

# Define data for all 16 missing candidates
eval_data = [
  {
    "slug": "andrew_johnson_usc",
    "subject": "USC Baseball Victory",
    "link": "https://www.latimes.com/sports/usc/story/2026-05-31/usc-baseball-dominates-texas-a-m-to-force-showdown-with-aggies",
    "target_url": "https://bsky.app/profile/latimes.com/post/3mn7bquup7l2a",
    "mode": "reply",
    "claim_u": 1.0,
    "claim_psi": 1.0,
    "real_u": 1.0,
    "real_psi": 1.0,
    "verdict": "PASS — The Path of Grace",
    "posts": [
      "1/ We're auditing the USC Baseball Victory over Texas A&M.\nTarget Post: https://www.latimes.com/sports/usc/story/2026-05-31/usc-baseball-dominates-texas-a-m-to-force-showdown-with-aggies\n\nPsochic Hegemony Graph",
      "2/ Claim: USC athletic department aims to demonstrate pure athletic excellence and sporting merit in a regional showdown.\nStated Judgement: (+1.0, +1.0) — Greater Good",
      "3/ Reality: The performance on the field was an organic realization of that ideal, with Andrew Johnson and the team delivering active sporting value.\nResulting Judgement: (+1.0, +1.0) — Greater Good",
      "4/ The Verdict? PASS. We're looking at The Path of Grace. The stated athletic standard matches the physical execution on the field.",
      "5/ What's happening: USC baseball dominated Texas A&M to force a regional final showdown, showcasing high sportsmanship and high-level college athletics.",
      "6/ The Bright Side: Athletic competitions represent an honest create/action space where physical output directly corresponds to merit and dedication.",
      "7/ The Breakdown: Unlike corporate governance, on-field competition possesses structural transparency (WHAT) and direct physical accountability (HOW).",
      "8/ The Trajectory: The Path of Grace\nWhen you map the alignment between sporting effort and on-field results...",
      "9/ ...it plots a direct trajectory toward a high-integrity, competitive sporting resolution vector.",
      "10/ The Unavoidable Truth: Dedication on the training field translates directly to physical performance under pressure.\nThe Unavoidable Lie: That victory can be bought without athletic labor.",
      "11/ Alethekanon: An authentic display of meritocratic competition. No corporate extraction or PR capture detected; the scores reflect actual sportsmanship.",
      "12/ Awwthekanon: Seeing these young athletes push themselves to the absolute limit and support each other is a beautiful reminder of teamwork.",
      "13/ Brothekanon: Bro, USC just went out there, ignored the bracket math, and forced a regional showdown by sheer force of will. That’s pure grit.",
      "14/ Blended Path: Support merit-based local sports programs that foster authentic human excellence.\nFinal Recalculated Coordinates: (+1.0, +1.0)"
    ]
  },
  {
    "slug": "don_pasquale_review",
    "subject": "Don Pasquale review",
    "link": "https://www.thetimes.com/culture/classical-opera/article/don-pasquale-review-bring-on-the-sword-and-sandals-dxmxcr83p?utm_term=Autofeed&utm_medium=Social&utm_source=Bluesky#Echobox=1780286718",
    "target_url": "https://bsky.app/profile/thetimes.com/post/3mn7bntmnc32e",
    "mode": "reply",
    "claim_u": 1.0,
    "claim_psi": 1.0,
    "real_u": 1.0,
    "real_psi": 1.0,
    "verdict": "PASS — The Path of Grace",
    "posts": [
      "1/ We're auditing the Don Pasquale theatrical opera review.\nTarget Post: https://www.thetimes.com/culture/classical-opera/article/don-pasquale-review-bring-on-the-sword-and-sandals-dxmxcr83p\n\nPsochic Hegemony Graph",
      "2/ Claim: The production aims to revitalize classical opera, delivering rich cultural value and aesthetic fulfillment to the audience.\nStated Judgement: (+1.0, +1.0) — Greater Good",
      "3/ Reality: The production succeeds in creating active cultural value, blending traditional opera with fresh theatrical vision.\nResulting Judgement: (+1.0, +1.0) — Greater Good",
      "4/ The Verdict? PASS. We're looking at The Path of Grace. The artistic endeavor successfully creates public joy and high aesthetic value.",
      "5/ What's happening: A review of the new Don Pasquale opera highlights its creative, highly engaging 'swords and sandals' aesthetic direction.",
      "6/ The Bright Side: High-quality artistic expression provides a shared cultural space that enriches human subjective experience.",
      "7/ The Breakdown: The performance uses classic narrative forms to reflect deep human behaviors, maintaining semantic harmony across the board.",
      "8/ The Trajectory: The Path of Grace\nWhen you map the alignment between artistic intent and audience resonance...",
      "9/ ...it plots a direct trajectory toward long-term cultural enrichment and shared human appreciation.",
      "10/ The Unavoidable Truth: Art is necessary for emotional and cognitive health.\nThe Unavoidable Lie: That culture can be completely reduced to financial spreadsheets.",
      "11/ Alethekanon: Artistic production serves as a functional generator of systemic cultural capital, aligning intent with public benefit.",
      "12/ Awwthekanon: Bringing sword-and-sandals elements into classical opera makes it feel so much more vibrant and accessible to everyone.",
      "13/ Brothekanon: Bro, turning a classic 19th-century opera into a Gladiator-style showdown is the ultimate theatrical glow-up. Highly approve.",
      "14/ Blended Path: Encourage public support for accessible classical arts and creative community theatre.\nFinal Recalculated Coordinates: (+1.0, +1.0)"
    ]
  },
  {
    "slug": "china_outbound_capital",
    "subject": "China Outbound Capital Controls",
    "link": "https://on.wsj.com/4dU12Zc",
    "target_url": "https://bsky.app/profile/wsj.com/post/3mn7bmfcpio2u",
    "mode": "reply",
    "claim_u": 1.0,
    "claim_psi": 1.0,
    "real_u": -0.5,
    "real_psi": -0.5,
    "verdict": "FAIL — The Path of The Fall",
    "posts": [
      "1/ We're auditing China's tightening of outbound capital controls.\nTarget Post: https://on.wsj.com/4dU12Zc\n\nPsochic Hegemony Graph",
      "2/ Claim: Authorities claim capital restrictions protect the sovereign economy and ensure long-term stability for everyone.\nStated Judgement: (+1.0, +1.0) — Greater Good",
      "3/ Reality: It's group-level protectionism (-0.5, -0.5) that restricts citizen economic freedom and extracts transactional value.\nResulting Judgement: (-0.5, -0.5) — Lesser Evil",
      "4/ The Verdict? FAIL. We're looking at The Path of The Fall. National protectionism sacrifices global economic integration for state control.",
      "5/ What's happening: Chinese regulators are tightening outbound investment and capital flows following the unwinding of the Meta-Manus deal.",
      "6/ The Bright Side: Sovereign security guards against volatile capital flight and keeps manufacturing domestic in the short term.",
      "7/ The Breakdown: The state claims this is a purely defensive measure (HOW), but structurally it enforces severe transactional capture (WHO).",
      "8/ The Trajectory: The Path of The Fall\nWhen you map the divergence between national security branding and restrictive reality...",
      "9/ ...it plots a direct trajectory toward a highly isolated and state-directed domestic economic model.",
      "10/ The Unavoidable Truth: Restricting capital flow reduces long-term investment trust.\nThe Unavoidable Lie: That domestic growth can occur in a fully closed loop.",
      "11/ Alethekanon: Tightening outbound flows is a classic sovereignty capture loop. It stabilizes state metrics at the cost of public economic agency.",
      "12/ Awwthekanon: It must be stressful for individuals trying to manage their personal savings under such tight, unpredictable regulations.",
      "13/ Brothekanon: Bro, shutting down outbound deals because you're scared of capital leaving is the ultimate corporate panic-button move.",
      "14/ Blended Path: Develop international investment standards that protect local industries without absolute transaction suppression.\nFinal Recalculated Coordinates: (-0.5, -0.5)"
    ]
  },
  {
    "slug": "illinois_midwest_sharing",
    "subject": "Illinois Tourism Sharing",
    "link": "https://www.chicagotribune.com/2026/05/30/illinois-250-art-culture-food-music/",
    "target_url": "https://bsky.app/profile/chicagotribune.com/post/3mn7bkazogz2g",
    "mode": "reply",
    "claim_u": 1.0,
    "claim_psi": 1.0,
    "real_u": 0.5,
    "real_psi": 0.0,
    "verdict": "FAIL — The Path of The Fall",
    "posts": [
      "1/ We're auditing the Illinois Art and Tourism sharing campaign.\nTarget Post: https://www.chicagotribune.com/2026/05/30/illinois-250-art-culture-food-music/\n\nPsochic Hegemony Graph",
      "2/ Claim: The campaign represents authentic Midwestern hospitality and the altruistic sharing of cultural heritage for all.\nStated Judgement: (+1.0, +1.0) — Greater Good",
      "3/ Reality: It functions as a standard marketing program (+0.5, 0.0) designed to attract tourism capital and boost local revenue.\nResulting Judgement: (+0.5, 0.0) — Good Preference",
      "4/ The Verdict? FAIL. We're looking at The Path of The Fall. The high-prestige branding of altruism hides standard commerce.",
      "5/ What's happening: Illinois launched a major art, culture, food, and music promotion highlighting Midwestern hospitality and destinations.",
      "6/ The Bright Side: Sharing local art and cultural history does foster genuine human interest and support local creative economies.",
      "7/ The Breakdown: The campaign uses the language of selfless sharing (WHY), but operates strictly as a transactional commercial model (WHO).",
      "8/ The Trajectory: The Path of The Fall\nWhen you map the gap between communal altruism and commercial branding...",
      "9/ ...it plots a direct trajectory toward a conventional, highly marketized tourism extraction vector.",
      "10/ The Unavoidable Truth: Tourism campaigns require economic returns to justify their public funding.\nThe Unavoidable Lie: That tourism marketing is driven by pure charity.",
      "11/ Alethekanon: Altruistic branding mask. The program is a standard economic multiplier. While harmless, calling it selfless is a semantic error.",
      "12/ Awwthekanon: I love celebrating local artists and food makers! Even if it is marketing, it's nice to see community creators get support.",
      "13/ Brothekanon: Bro, calling a tourism billboard 'altruistic Midwestern sharing' is hilarious. Just tell me where the good deep-dish pizza is.",
      "14/ Blended Path: Champion authentic, community-led cultural exchanges that do not rely on corporate marketing branding.\nFinal Recalculated Coordinates: (+0.5, 0.0)"
    ]
  },
  {
    "slug": "solar_eclipse_darkness",
    "subject": "Solar Eclipse Viewing",
    "link": "https://www.nytimes.com/2026/05/26/travel/solar-eclipse-spain-iceland-greenland.html",
    "target_url": "https://bsky.app/profile/upshot.nytimes.com/post/3mn7bdni2ik2z",
    "mode": "reply",
    "claim_u": 1.0,
    "claim_psi": 0.0,
    "real_u": 1.0,
    "real_psi": 1.0,
    "verdict": "PASS — The Path of Grace",
    "posts": [
      "1/ We're auditing the upcoming solar eclipse viewing routes.\nTarget Post: https://www.nytimes.com/2026/05/26/travel/solar-eclipse-spain-iceland-greenland.html\n\nPsochic Hegemony Graph",
      "2/ Claim: Exploring the celestial event is a passive, individual appreciation of a spectacular natural phenomenon.\nStated Judgement: (+1.0, 0.0) — Good Preference",
      "3/ Reality: It serves as a Greater Good (+1.0, +1.0) by actively uniting diverse communities globally in shared wonder.\nResulting Judgement: (+1.0, +1.0) — Greater Good",
      "4/ The Verdict? PASS. We're looking at The Path of Grace. The passive natural wonder translates into active community value.",
      "5/ What's happening: Global travel routes are being mapped for the August 12 solar eclipse across Greenland, Iceland, Spain, and Portugal.",
      "6/ The Bright Side: Nature provides grand unifying experiences that transcend political, national, and economic divides.",
      "7/ The Breakdown: The event requires zero corporate production (HOW) and generates massive, decentralized communal inspiration (WHY).",
      "8/ The Trajectory: The Path of Grace\nWhen you map the transformation from quiet travel to active international sharing...",
      "9/ ...it plots a direct trajectory toward a high-connectivity, harmonious global appreciation of our shared universe.",
      "10/ The Unavoidable Truth: The cosmos operates on physical laws entirely indifferent to human capital.\nThe Unavoidable Lie: That one can own a shadow.",
      "11/ Alethekanon: A zero-rent systemic benefit. Natural phenomena are the ultimate public goods, maximizing signal with zero exploitation.",
      "12/ Awwthekanon: It is deeply moving to think of thousands of people looking up at the sky together in shared, quiet awe.",
      "13/ Brothekanon: Bro, traveling all the way to Greenland just to watch the sun disappear for two minutes is the ultimate cosmic road trip.",
      "14/ Blended Path: Foster public astronomy programs and coordinate accessible travel for scientific education.\nFinal Recalculated Coordinates: (+1.0, +1.0)"
    ]
  },
  {
    "slug": "torres_settlement_invalidation",
    "subject": "Torres Settlement Invalidation",
    "link": "https://www.nminewsservice.com/oag-motion-invalidate-torres-settlement-2026/",
    "target_url": "https://bsky.app/profile/pasquines.us/post/3mn7bclqrnp2r",
    "mode": "reply",
    "claim_u": 1.5,
    "claim_psi": 1.0,
    "real_u": 1.0,
    "real_psi": 1.0,
    "verdict": "PASS — The Path of Grace",
    "posts": [
      "1/ We're auditing the OAG motion to invalidate the Torres Settlement.\nTarget Post: https://www.nminewsservice.com/oag-motion-invalidate-torres-settlement-2026/\n\nPsochic Hegemony Graph",
      "2/ Claim: The Office of the Attorney General aims to invalidate a corrupt settlement, restoring systemic legal accountability for all.\nStated Judgement: (+1.5, +1.0) — Greater Good",
      "3/ Reality: The motion actively upholds rule of law (+1.0, +1.0), correcting structural capture and protecting institutional integrity.\nResulting Judgement: (+1.0, +1.0) — Greater Good",
      "4/ The Verdict? PASS. We're looking at The Path of Grace. An official state entity actively works to restore accountability.",
      "5/ What's happening: The NMI Attorney General filed a motion to invalidate a settlement that dismissed criminal charges against former Governor Torres.",
      "6/ The Bright Side: When legal oversight bodies actively self-correct, they restore public trust in democratic systems.",
      "7/ The Breakdown: The previous settlement was a classic capture loop (WHO). Invalidating it returns the process to transparent legal review.",
      "8/ The Trajectory: The Path of Grace\nWhen you map the correction from administrative corruption to active legal accountability...",
      "9/ ...it plots a direct trajectory toward a restored, high-integrity legal framework for the territory.",
      "10/ The Unavoidable Truth: Public trust demands that high-level officials face the same legal standards as citizens.\nThe Unavoidable Lie: That institutional peace can be achieved by burying crimes.",
      "11/ Alethekanon: A rare institutional immune response. The OAG's action actively checks elite impunity, restoring systemic legal integrity.",
      "12/ Awwthekanon: It is encouraging to see people in authority stand up for what's right, even when it means auditing past mistakes.",
      "13/ Brothekanon: Bro, trying to sneakily dismiss your own criminal charges and then getting called out by the AG is a massive self-own.",
      "14/ Blended Path: Build independent prosecutorial bodies that can audit and invalidate corrupt backroom deals automatically.\nFinal Recalculated Coordinates: (+1.0, +1.0)"
    ]
  },
  {
    "slug": "nvidia_pc_arm_chip",
    "subject": "Nvidia Arm PC Chip",
    "link": "https://cnb.cx/4dPPqGM",
    "target_url": "https://bsky.app/profile/cnbc.com/post/3mn7ba2jota2h",
    "mode": "reply",
    "claim_u": 1.0,
    "claim_psi": 1.0,
    "real_u": 1.0,
    "real_psi": 1.5,
    "verdict": "PASS — The Path of Grace",
    "posts": [
      "1/ We're auditing Nvidia's jump into Arm-based laptop chips.\nTarget Post: https://cnb.cx/4dPPqGM\n\nPsochic Hegemony Graph",
      "2/ Claim: Nvidia aims to disrupt the laptop market, expanding technological choices and boosting computing efficiency.\nStated Judgement: (+1.0, +1.0) — Greater Good",
      "3/ Reality: The engineering delivers massive physical utility (+1.0, +1.5), breaking an x86 silicon monopoly and creating systemic value.\nResulting Judgement: (+1.0, +1.5) — Greater Good",
      "4/ The Verdict? PASS. We're looking at The Path of Grace. Real technological innovation actively drives marketplace productivity.",
      "5/ What's happening: Nvidia has launched a new Arm-based processor for consumer laptops, partnering with Microsoft, Dell, and HP.",
      "6/ The Bright Side: Breaking silicon monocultures drives hardware competition, lowering power consumption and increasing consumer options.",
      "7/ The Breakdown: The development represents a massive increase in thermodynamic compute capacity (WHAT) and physical efficiency (HOW).",
      "8/ The Trajectory: The Path of Grace\nWhen you map the progression from conceptual design to high-efficiency hardware deployment...",
      "9/ ...it plots a direct trajectory toward a highly productive, low-power consumer computing future.",
      "10/ The Unavoidable Truth: Software demands will always rise to consume the physical limits of hardware engineering.\nThe Unavoidable Lie: That architectural dominance can last forever.",
      "11/ Alethekanon: True productive value. Nvidia's engineering output delivers genuine efficiency increases, expanding systemic compute limits.",
      "12/ Awwthekanon: Low-power chips mean longer laptop battery life, letting people work and connect without hunting for outlets constantly.",
      "13/ Brothekanon: Bro, Nvidia saw Apple Silicon winning all the battery life tests and decided it was time to drop a heavy bomb on Intel.",
      "14/ Blended Path: Foster open-standard computing platforms that encourage diverse silicon competition.\nFinal Recalculated Coordinates: (+1.0, +1.5)"
    ]
  },
  {
    "slug": "donald_trump_jr_bettina",
    "subject": "Trump Jr Bettina Union",
    "link": "https://www.irishstar.com/news/us-news/donald-trump-jr-bettina-president-37229823",
    "target_url": "https://bsky.app/profile/irishstar.com/post/3mn7b2xb34b2s",
    "mode": "reply",
    "claim_u": 1.0,
    "claim_psi": 1.0,
    "real_u": -1.0,
    "real_psi": 0.5,
    "verdict": "FAIL — The Path of Deception",
    "posts": [
      "1/ We're auditing the Donald Trump Jr. and Bettina Anderson social union.\nTarget Post: https://www.irishstar.com/news/us-news/donald-trump-jr-bettina-president-37229823\n\nPsochic Hegemony Graph",
      "2/ Claim: The union is framed as an organic, personal marriage celebrating mutual devotion and public happiness.\nStated Judgement: (+1.0, +1.0) — Greater Good",
      "3/ Reality: It operates as the Greatest Lie (-1.0, +0.5). It is a strategic political branding union designed to consolidate social capital.\nResulting Judgement: (-1.0, +0.5) — Greatest Lie / Mask",
      "4/ The Verdict? FAIL. We're looking at The Path of Deception. A highly public, strategic branding event masquerades as pure romance.",
      "5/ What's happening: Media reports highlight Bettina Anderson's high-society entry following her marriage to Donald Trump Jr.",
      "6/ The Poison: Elite social circles use romance as an extraction loop to capture public attention and secure political power.",
      "7/ The Breakdown: The event claims to be a private human bond (WHY), but operates as a highly transactional power consolidation (WHO).",
      "8/ The Trajectory: The Path of Deception\nWhen you map the gap between organic romantic ideals and strategic status capture...",
      "9/ ...it plots a direct trajectory toward a highly calculated, elite-facing transactional brand loop.",
      "10/ The Unavoidable Truth: High-society marriages are bound by strategic alignment as much as emotional choice.\nThe Unavoidable Lie: That modern celebrity relationships exist in a PR-free vacuum.",
      "11/ Alethekanon: Power consolidation mask. The union serves to reinforce domestic elite networks, converting social trust into branding capital.",
      "12/ Awwthekanon: Behind the cameras and strategic PR, I hope there is genuine human connection. Living in a constant media fishbowl is tough.",
      "13/ Brothekanon: Bro, the ink on the contract is barely dry and they're already running lifestyle puff pieces. That’s premium brand management.",
      "14/ Blended Path: Encourage a cultural shift away from dynastic celebrity worship toward localized, peer-level community bonds.\nFinal Recalculated Coordinates: (-1.0, +0.5)"
    ]
  },
  {
    "slug": "ftse_entrant_ai_boom",
    "subject": "FTSE AI Entrant",
    "link": "https://ft.trib.al/m4hsgbR",
    "target_url": "https://bsky.app/profile/financialtimes.com/post/3mn7ayaz5cx2e",
    "mode": "reply",
    "claim_u": 1.0,
    "claim_psi": 1.0,
    "real_u": 0.0,
    "real_psi": 0.8,
    "verdict": "FAIL — The Path of The Fall",
    "posts": [
      "1/ We're auditing the FTSE 100's new British AI entrant.\nTarget Post: https://ft.trib.al/m4hsgbR\n\nPsochic Hegemony Graph",
      "2/ Claim: The entrant aims to lead a technological revolution, creating sovereign AI wealth and structural benefits for all.\nStated Judgement: (+1.0, +1.0) — Greater Good",
      "3/ Reality: It operates as a standard corporate capital extraction loop (0.0, +0.8), maximizing stock valuations and shareholder return.\nResulting Judgement: (0.0, +0.8) — Center",
      "4/ The Verdict? FAIL. We're looking at The Path of The Fall. The high-prestige promise of sovereign innovation masks basic corporate growth.",
      "5/ What's happening: Financial media highlights a likely new FTSE 100 entrant putting a British spin on the global AI market.",
      "6/ The Poison: Tech valuation cycles leverage public excitement over AI to extract venture capital, without delivering localized labor value.",
      "7/ The Breakdown: The firm claims its primary value is national technological advancement (WHY), but its engine is shareholder extraction (WHO).",
      "8/ The Trajectory: The Path of The Fall\nWhen you map the divergence between strategic tech ideals and standard stock growth...",
      "9/ ...it plots a direct trajectory toward a conventional, highly marketized capital concentration vector.",
      "10/ The Unavoidable Truth: Venture valuations must eventually reconcile with physical balance sheets and actual utility.\nThe Unavoidable Lie: That national glory pays corporate interest bills.",
      "11/ Alethekanon: Classic market marketing. The 'British AI boom' tag is an empty maximizer used to command a premium multiple at listing.",
      "12/ Awwthekanon: I hope the growth of these tech firms actually translates into secure, well-paying jobs for local working people.",
      "13/ Brothekanon: Bro, slapping 'British AI Boom' on a listing is the easiest way to get investors to look past the lack of cash flow.",
      "14/ Blended Path: Restructure stock markets to reward long-term research and development over short-term listing pops.\nFinal Recalculated Coordinates: (0.0, +0.8)"
    ]
  },
  {
    "slug": "la_la_land_pianist",
    "subject": "Sydney La La Land Pianist",
    "link": "https://www.theguardian.com/australia-news/2026/jun/01/audience-member-replaces-ill-keyboardist-sydney-la-land-justin-hurwitz",
    "target_url": "https://bsky.app/profile/theguardian.com/post/3mn7ay4uyex24",
    "mode": "reply",
    "claim_u": 1.0,
    "claim_psi": 1.0,
    "real_u": 1.5,
    "real_psi": 1.5,
    "verdict": "PASS — The Path of Grace",
    "posts": [
      "1/ We're auditing the Sydney La La Land pianist replacement.\nTarget Post: https://www.theguardian.com/australia-news/2026/jun/01/audience-member-replaces-ill-keyboardist-sydney-la-land-justin-hurwitz\n\nPsochic Hegemony Graph",
      "2/ Claim: A concert performance aims to deliver standard artistic entertainment under structured commercial terms.\nStated Judgement: (+1.0, +1.0) — Greater Good",
      "3/ Reality: An audience member stepping in to save the show is an act of pure, beautiful cooperation (+1.5, +1.5), maximizing community value.\nResulting Judgement: (+1.5, +1.5) — Greater Good",
      "4/ The Verdict? PASS. We're looking at The Path of Grace. Spontaneous human collaboration saves a shared community experience.",
      "5/ What's happening: When the keyboardist fell ill during a La La Land live concert in Sydney, an audience member stepped up and played.",
      "6/ The Bright Side: Human beings possess incredible, uncommodified talents and a natural willingness to cooperate and save the day.",
      "7/ The Breakdown: The event bypassed standard commercial union rules (HOW) to prioritize immediate collective joy and performance success (WHY).",
      "8/ The Trajectory: The Path of Grace\nWhen you map the transformation from passive customer to active community savior...",
      "9/ ...it plots a direct trajectory toward a high-trust, collaborative realization of human talent and mutual aid.",
      "10/ The Unavoidable Truth: True community resilience is built on spontaneous cooperation, not rigid contracts.\nThe Unavoidable Lie: That professional stages are completely closed systems.",
      "11/ Alethekanon: Exceptional positive anomaly. Spontaneous labor substitution maximized systemic value with zero transactional friction.",
      "12/ Awwthekanon: This story is so incredibly heartwarming! It shows how a community can come together to support each other in a pinch.",
      "13/ Brothekanon: Bro, imagine sitting in the crowd, having a beer, and suddenly you're playing keyboard for a packed stadium. Absolute legend.",
      "14/ Blended Path: Celebrate and foster platforms that lower the barrier between passive consumers and active creative participants.\nFinal Recalculated Coordinates: (+1.5, +1.5)"
    ]
  },
  {
    "slug": "sweden_world_cup",
    "subject": "Sweden World Cup Guide",
    "link": "https://www.thenationalnews.com/sport/football/2026/06/01/world-cup-2026-group-f-guide-hannibal-is-main-man-for-tunisia-netherlands-need-gakpo-goals/",
    "target_url": "https://bsky.app/profile/thenationalnews.com/post/3mn7axass3g2l",
    "mode": "reply",
    "claim_u": 1.0,
    "claim_psi": 1.0,
    "real_u": 1.0,
    "real_psi": 1.0,
    "verdict": "PASS — The Path of Grace",
    "posts": [
      "1/ We're auditing Sweden's FIFA World Cup 2026 Group F guide.\nTarget Post: https://www.thenationalnews.com/sport/football/2026/06/01/world-cup-2026-group-f-guide-hannibal-is-main-man-for-tunisia-netherlands-need-gakpo-goals/\n\nPsochic Hegemony Graph",
      "2/ Claim: Elite international sport provides a harmonious competitive arena, driving athletic excellence and global connection.\nStated Judgement: (+1.0, +1.0) — Greater Good",
      "3/ Reality: The tournament creates real, active athletic value and global community focus (+1.0, +1.0), aligning perfectly with the sporting ideal.\nResulting Judgement: (+1.0, +1.0) — Greater Good",
      "4/ The Verdict? PASS. We're looking at The Path of Grace. Clean athletic competition creates organic, worldwide collaborative focus.",
      "5/ What's happening: Sports media outlines the highly competitive Group F lineup, highlighting Sweden's envied forward line and Japan.",
      "6/ The Bright Side: International sports festivals are highly functional spaces for positive, peaceful cross-border rivalry.",
      "7/ The Breakdown: The event operates with absolute competitive transparency (HOW), delivering deep global entertainment (WHY).",
      "8/ The Trajectory: The Path of Grace\nWhen you map the alignment between athletic training and competitive realization...",
      "9/ ...it plots a direct trajectory toward a high-prestige, globally resonant sporting spectacle.",
      "10/ The Unavoidable Truth: True athletic triumph cannot be falsified; it must be physically executed on the grass.\nThe Unavoidable Lie: That sports analysis can predict chaotic matches.",
      "11/ Alethekanon: Functional competitive alignment. The athletic metrics are empirical, offering a transparent, high-integrity action vector.",
      "12/ Awwthekanon: Sports brings families and whole nations together in shared hope. The excitement of the World Cup is so special.",
      "13/ Brothekanon: Bro, Group F is an absolute bloodbath. Sweden and Japan are going to run circles around everyone. I can't wait.",
      "14/ Blended Path: Protect grassroots youth football programs from excessive commercialization.\nFinal Recalculated Coordinates: (+1.0, +1.0)"
    ]
  },
  {
    "slug": "chile_fifa_stickers",
    "subject": "Chile Sticker Swap",
    "link": "https://bsky.app/profile/reuters.com/post/3mn7audydig2s",
    "target_url": "https://bsky.app/profile/reuters.com/post/3mn7audydig2s",
    "mode": "reply",
    "claim_u": 1.0,
    "claim_psi": 1.0,
    "real_u": 1.5,
    "real_psi": 1.0,
    "verdict": "PASS — The Path of Grace",
    "posts": [
      "1/ We're auditing the Chile World Cup sticker-swap event.\nTarget Post: https://bsky.app/profile/reuters.com/post/3mn7audydig2s\n\nPsochic Hegemony Graph",
      "2/ Claim: The event represents a passive hobby gathering for fans trading Panini World Cup stickers.\nStated Judgement: (+1.0, +1.0) — Greater Good",
      "3/ Reality: It serves as a beautiful community generation loop (+1.5, +1.0), fostering dense social trust and shared intergenerational joy.\nResulting Judgement: (+1.5, +1.0) — Greater Good",
      "4/ The Verdict? PASS. We're looking at The Path of Grace. A simple hobby event builds a massive, high-trust community space.",
      "5/ What's happening: Thousands of soccer fans packed Santiago's Bicentenario Stadium for a massive FIFA World Cup sticker-swap event.",
      "6/ The Bright Side: Simple, uncommodified community swap meets are the ultimate antidote to digital algorithmic isolation.",
      "7/ The Breakdown: The event relies on organic peer-to-peer exchange (HOW) rather than commercial retail transactions (WHAT).",
      "8/ The Trajectory: The Path of Grace\nWhen you map the transformation from retail collection to massive local community gathering...",
      "9/ ...it plots a direct trajectory toward a high-trust, extremely harmonious local neighborhood network.",
      "10/ The Unavoidable Truth: Human connection naturally crystallizes around simple shared games and physical collections.\nThe Unavoidable Lie: That digital networks can fully replace physical community spaces.",
      "11/ Alethekanon: High Net Reality Ratio. Pure peer-to-peer network routing. Trading cards bypass corporate paywalls to build direct social trust.",
      "12/ Awwthekanon: Seeing kids and grandparents sitting on the stadium turf together trading stickers is just so lovely and pure.",
      "13/ Brothekanon: Bro, thousands of adults gathering in a stadium to swap cardboard stickers is the most wholesome energy imaginable.",
      "14/ Blended Path: Fund and protect public community spaces for local swaps, hobby meets, and shared physical play.\nFinal Recalculated Coordinates: (+1.5, +1.0)"
    ]
  },
  {
    "slug": "us_military_iran",
    "subject": "US Military Iran Radar Targets",
    "link": "https://bit.ly/4x1xTEo",
    "target_url": "https://bsky.app/profile/apnews.com/post/3mn7anrm6ku2b",
    "mode": "reply",
    "claim_u": 1.0,
    "claim_psi": 1.0,
    "real_u": -1.0,
    "real_psi": -1.0,
    "verdict": "FAIL — The Path of Deception",
    "posts": [
      "1/ We're auditing the US military strikes on Iranian radar sites.\nTarget Post: https://bit.ly/4x1xTEo\n\nPsochic Hegemony Graph",
      "2/ Claim: The military actions are defensive operations meant to stabilize regional security and protect everyone's freedom.\nStated Judgement: (+1.0, +1.0) — Greater Good",
      "3/ Reality: The action represents geostrategic escalation (-1.0, -1.0), actively generating chaos, destruction, and long-term instability.\nResulting Judgement: (-1.0, -1.0) — Greater Evil",
      "4/ The Verdict? FAIL. We're looking at The Path of Deception. The rhetoric of stability masks a destructive geopolitical cycle.",
      "5/ What's happening: US military targeted Iranian radar and drone control sites after Tehran shot down an American MQ-1 Predator drone.",
      "6/ The Poison: Military-industrial operations frame escalation as containment, leading to permanent, highly profitable warfare loops.",
      "7/ The Breakdown: The state claims deterrence (WHY), but the physical output is active material destruction and perpetual risk (HOW).",
      "8/ The Trajectory: The Path of Deception\nWhen you map the divergence between peace rhetoric and active kinetic strikes...",
      "9/ ...it plots a direct trajectory toward a highly destructive, destabilizing regional escalation vector.",
      "10/ The Unavoidable Truth: Kinetic escalation never creates structural safety; it only breeds future threat loops.\nThe Unavoidable Lie: That one can bomb a region into harmonious democratic peace.",
      "11/ Alethekanon: Classic geopolitical feedback capture. The escalation loop generates perpetual security demand, fueling defense extraction.",
      "12/ Awwthekanon: My heart goes out to the innocent civilians who will suffer the consequences of these military escalations and missile fire.",
      "13/ Brothekanon: Bro, shooting down a drone and immediately blowing up a radar station is the ultimate geopolitical game of chicken.",
      "14/ Blended Path: Support strict international mediation and demilitarized buffer zones over immediate kinetic response.\nFinal Recalculated Coordinates: (-1.0, -1.0)"
    ]
  },
  {
    "slug": "arkansas_abortion_ban",
    "subject": "Arkansas Miscarriage Healthcare Ban",
    "link": "https://www.propublica.org/article/arkansas-abortion-ban-miscarriage-care",
    "target_url": "https://bsky.app/profile/propublica.org/post/3mn6uvkksvg2j",
    "mode": "reply",
    "claim_u": 2.0,
    "claim_psi": 1.0,
    "real_u": -1.5,
    "real_psi": -1.5,
    "verdict": "FAIL — The Path of Deception",
    "posts": [
      "1/ We're auditing the Arkansas Miscarriage Healthcare Ban case.\nTarget Post: https://www.propublica.org/article/arkansas-abortion-ban-miscarriage-care\n\nPsochic Hegemony Graph",
      "2/ Claim: Proponents claim the ban protects sacred human life and enforces maximum moral order (+2.0, +1.0) for the community.\nStated Judgement: (+2.0, +1.0) — Greater Good",
      "3/ Reality: It acts as an extraction of basic care (-1.5, -1.5), actively destroying healthcare access and causing life-threatening suffering.\nResulting Judgement: (-1.5, -1.5) — Greater Evil",
      "4/ The Verdict? FAIL. We're looking at The Path of Deception. The rhetoric of protecting life leads directly to systemic harm.",
      "5/ What's happening: A woman was denied standard, life-saving miscarriage care in Arkansas due to strict legal abortion bans.",
      "6/ The Poison: Ideological legal mandates extract professional medical judgment, replacing baseline human care with carceral threats.",
      "7/ The Breakdown: The state claims supreme moral protection (WHY), but the physical consequence is active systemic cruelty (HOW).",
      "8/ The Trajectory: The Path of Deception\nWhen you map the gap between pro-life claims and actual medical endangerment...",
      "9/ ...it plots a direct trajectory toward a highly punitive, anti-empirical carceral medical capture zone.",
      "10/ The Unavoidable Truth: Banning reproductive healthcare directly increases maternal mortality rates.\nThe Unavoidable Lie: That a system can care about children while torturing mothers.",
      "11/ Alethekanon: Total systemic failure. The legal framework contains a massive plane error, prioritizing ideological rules over biological reality.",
      "12/ Awwthekanon: This is absolutely heartbreaking. A woman undergoing a miscarriage should be surrounded by care, not legal fear.",
      "13/ Brothekanon: Bro, denying medical treatment for a miscarriage to the point where vets treat dogs better is a horrifying failure.",
      "14/ Blended Path: Enact federal healthcare protections that guarantee medical immunity for emergency pregnancy care.\nFinal Recalculated Coordinates: (-1.5, -1.5)"
    ]
  },
  {
    "slug": "powell_fed_warning",
    "subject": "Powell Federal Reserve Warning",
    "link": "https://www.axios.com/2026/06/01/powell-fed-warsh-trump",
    "target_url": "https://bsky.app/profile/axios.com/post/3mn6vrjzux22j",
    "mode": "reply",
    "claim_u": 1.0,
    "claim_psi": 1.0,
    "real_u": 0.5,
    "real_psi": 0.5,
    "verdict": "FAIL — The Path of The Fall",
    "posts": [
      "1/ We're auditing Jerome Powell's Federal Reserve warning.\nTarget Post: https://www.axios.com/2026/06/01/powell-fed-warsh-trump\n\nPsochic Hegemony Graph",
      "2/ Claim: The Fed claims to act as a neutral, independent economic stabilizer promoting the Greater Good (+1.0, +1.0).\nStated Judgement: (+1.0, +1.0) — Greater Good",
      "3/ Reality: It operates as a technocratic stabilizer (+0.5, +0.5), navigating tense corporate/political capture and inflation pressures.\nResulting Judgement: (+0.5, +0.5) — Good Preference",
      "4/ The Verdict? FAIL. We're looking at The Path of The Fall. The high ideal of complete monetary independence falls back to political navigation.",
      "5/ What's happening: Fed Chair Jerome Powell issued a warning defending central bank independence against potential Trump administration policy pressure.",
      "6/ The Poison: Technocratic central banking relies on the fiction of absolute independence, hiding deep systemic ties to private banking capital.",
      "7/ The Breakdown: The Fed claims standard scientific neutrality (WHY), but operates as a political buffer in elite monetary conflicts (WHO).",
      "8/ The Trajectory: The Path of The Fall\nWhen you map the gap between absolute technocratic ideals and intense political reality...",
      "9/ ...it plots a direct trajectory toward a highly defensive, politically captured monetary policy loop.",
      "10/ The Unavoidable Truth: Central banks cannot isolate themselves from the political systems that define their legal power.\nThe Unavoidable Lie: That money is completely independent of politics.",
      "11/ Alethekanon: Defensive institutional posturing. Powell is signaling a boundary to protect technocratic control against political capture.",
      "12/ Awwthekanon: Central bank decisions impact interest rates on homes and credit cards, making daily life harder for working families.",
      "13/ Brothekanon: Bro, Powell is basically telling the new administration 'don't touch my dials,' but everyone knows they're touching them anyway.",
      "14/ Blended Path: Reform central banking to increase direct democratic input while keeping core structural safeguards.\nFinal Recalculated Coordinates: (+0.5, +0.5)"
    ]
  },
  {
    "slug": "cuba_collapses",
    "subject": "Cuba Collapse Consequences",
    "link": "https://news.sky.com/story/bluesky-13549534",
    "target_url": "https://bsky.app/profile/news.sky.com/post/3mn74erri3l26",
    "mode": "reply",
    "claim_u": 1.0,
    "claim_psi": 0.0,
    "real_u": -1.2,
    "real_psi": -1.0,
    "verdict": "FAIL — The Path of Deception",
    "posts": [
      "1/ We're auditing the geostrategic consequences of a Cuban economic collapse.\nTarget Post: https://news.sky.com/story/bluesky-13549534\n\nPsochic Hegemony Graph",
      "2/ Claim: US policy proponents claim the embargo passive-neutrally promotes democracy and human rights (+1.0, 0.0).\nStated Judgement: (+1.0, 0.0) — Good Preference",
      "3/ Reality: It acts as destructive economic warfare (-1.2, -1.0), triggering systemic societal collapse and massive human flight.\nResulting Judgement: (-1.2, -1.0) — Greater Evil",
      "4/ The Verdict? FAIL. We're looking at The Path of Deception. Embargoes branded as 'democratic incentives' execute active structural devastation.",
      "5/ What's happening: Media reports warning that the US will face massive migration and security consequences if Cuba's economy collapses under sanctions.",
      "6/ The Poison: High-altitude geopolitical sanctions punish everyday working families, forcing collapse to extract political capitulation.",
      "7/ The Breakdown: The state claims it is championing liberty (WHY), but the physical result is active systemic starvation and chaos (HOW).",
      "8/ The Trajectory: The Path of Deception\nWhen you map the gap between democratic rhetoric and the realities of starvation embargoes...",
      "9/ ...it plots a direct trajectory toward a highly chaotic, destabilizing humanitarian emergency vector.",
      "10/ The Unavoidable Truth: Strangling an island's economy eventually forces its people to flee to your own borders.\nThe Unavoidable Lie: That you can isolate a neighbor without suffering the splash damage of their pain.",
      "11/ Alethekanon: Severe plane error. The sanctions regime fails its own objective, creating a border crisis to fulfill an outdated Cold War ideology.",
      "12/ Awwthekanon: The human suffering in Cuba is immense. Sanctions are depriving everyday people of medicine, electricity, and basic food.",
      "13/ Brothekanon: Bro, keeping an embargo active for 60 years and then acting shocked when the island's collapse causes a refugee crisis is wild.",
      "14/ Blended Path: Lift the embargo immediately to foster mutually beneficial trade and raise the quality of life for all.\nFinal Recalculated Coordinates: (-1.2, -1.0)"
    ]
  }
]

print(f"Loaded {len(eval_data)} stories to generate.")

for idx, data in enumerate(eval_data, 1):
    slug = data["slug"]
    print(f"\n[{idx}/16] Processing '{slug}'...")
    
    # 1. Generate Trajectory Graph
    # Determine output paths
    # We save to:
    # - scratch/[slug]_graph.png
    # - bluesky_bot/[slug]_graph.png
    # - _Generated_Content/[slug]_graph.png
    graph_filename = f"{slug}_graph.png"
    
    scratch_graph_path = os.path.join(script_dir, graph_filename)
    bot_graph_path = os.path.join(parent_dir, "bluesky_bot", graph_filename)
    gen_graph_path = os.path.join(parent_dir, "_Generated_Content", graph_filename)
    
    print(f"  Drawing graph for coordinates ({data['claim_u']}, {data['claim_psi']}) -> ({data['real_u']}, {data['real_psi']})")
    
    # Draw scratch graph first
    draw_graph(
        claim_u=data["claim_u"],
        claim_psi=data["claim_psi"],
        real_u=data["real_u"],
        real_psi=data["real_psi"],
        title=data["subject"],
        filename=scratch_graph_path
    )
    
    # Copy graph to other locations
    import shutil
    for path in [bot_graph_path, gen_graph_path]:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        shutil.copy(scratch_graph_path, path)
        print(f"  Copied graph to {path}")
        
    # 2. Formulate thread config dictionary
    thread_config = {
        "subject_slug": slug,
        "subject": data["subject"],
        "link": data["link"],
        "target_url": data["target_url"],
        "mode": data["mode"],
        "claim_u": data["claim_u"],
        "claim_psi": data["claim_psi"],
        "real_u": data["real_u"],
        "real_psi": data["real_psi"],
        "posts": data["posts"],
        "status": "COMPLETED DRY RUN",
        "verdict": data["verdict"],
        "graph_img": graph_filename
    }
    
    # 3. Call save_and_sync_story to write individual JSON files and update the registry sequentially
    print(f"  Syncing story to registries...")
    save_and_sync_story(thread_config)

print("\nAll 16 missing candidate stories successfully evaluated, graphs generated, and registries synchronized!")
