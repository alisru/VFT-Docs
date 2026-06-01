import json
import os

data = [
    {
        "subject_slug": "cuba_collapses",
        "subject": "Cuba collapses",
        "link": "https://news.sky.com/story/bluesky-13549534",
        "target_url": "https://bsky.app/profile/news.sky.com/post/3mn74erri3l26",
        "mode": "reply",
        "claim_u": 1.0, "claim_psi": -1.0,
        "real_u": -1.0, "real_psi": -1.0,
        "posts": [
            "1/ We're running a Psochic Hegemony audit on US policy regarding Cuba.\nTarget Post: https://news.sky.com/story/bluesky-13549534\n\nPsochic Hegemony Graph",
            "2/ Claim: The embargo is framed as a Lesser Good (+1.0, -1.0). It claims to contain a dangerous regime and promote long-term peace by isolating the nation.",
            "3/ Reality: The embargo acts as a Greater Evil (-1.0, -1.0). It actively extracts value and punishes a vulnerable civilian population for geopolitical leverage.",
            "4/ The verdict? FAIL. This maps directly to The Path of Deception. What is sold as a protective containment measure is actually a mechanism for destruction.",
            "5/ Who does this benefit? Not the Cuban people. It benefits a tribal subset of US political interests, prioritizing ideological signaling over human welfare.",
            "6/ What is the trajectory? Active destruction. By blocking essential goods, the policy ensures systemic necrosis rather than promoting democratic reform.",
            "7/ The hypocrisy gap here is massive. The US claims to be protecting human rights while actively restricting access to food, medicine, and basic infrastructure.",
            "8/ This is a classic Fake Maximizer. It uses the moral cover of 'fighting communism' to justify policies that cause undeniable material harm to civilians.",
            "9/ We have to ask: is this a Helxis Capture Loop? Yes. The policy is self-sustaining. It creates poverty, points to the poverty as failure, and tightens the screws.",
            "10/ The Net Reality Ratio is extremely low. After decades, the embargo has failed to achieve its stated goal, revealing it as an ungrounded ideological obsession.",
            "11/ The dominant failure mode is Systemic Necrosis. We are watching an entire society's infrastructure slowly suffocate under the weight of external pressure.",
            "12/ True progress requires alignment. If the goal is a healthy, free Cuba, policies must reflect Grace—building value for all—rather than extracting it.",
            "13/ It's time to recognize that punishing people for their government's actions only entrenches the very systems we claim to oppose.",
            "14/ Real solutions mean acknowledging the humanity of all beings. We must end policies of engineered collapse and start building paths toward systemic justice."
        ]
    },
    {
        "subject_slug": "alabama_voting",
        "subject": "Elimination of Black Voting Districts",
        "link": "https://www.democracydocket.com/opinion/alabama-keeps-telling-us-what-it-thinks-democracy-should-look-like/",
        "target_url": "https://bsky.app/profile/democracydocket.com/post/3mn6t7sxrxm2j",
        "mode": "reply",
        "claim_u": 1.0, "claim_psi": 1.0,
        "real_u": -1.0, "real_psi": -1.0,
        "posts": [
            "1/ We're auditing the elimination of majority-Black voting districts.\nTarget Post: https://www.democracydocket.com/opinion/alabama-keeps-telling-us-what-it-thinks-democracy-should-look-like/\n\nPsochic Hegemony Graph",
            "2/ Claim: Map-drawers claim these changes are 'race-neutral' and promote the Greater Good (+1.0, +1.0) by ensuring fairness under the law.",
            "3/ Reality: It’s the Greater Evil (-1.0, -1.0). This is active suppression, destroying the political power of a targeted group to consolidate tribal control.",
            "4/ The Verdict? FAIL. We're looking at The Path of Deception. The language of equality is being weaponized to achieve systemic exclusion.",
            "5/ Who really benefits? A highly specific in-group seeking to artificially maintain power against demographic shifts, at the direct expense of out-groups.",
            "6/ The trajectory here is regression. This isn't just about lines on a map; it's about systematically dismantling the mechanisms of democratic accountability.",
            "7/ The Tribal Gap is severe. The system is designed to lock out opposing voices, creating a feedback loop where the powerful only answer to themselves.",
            "8/ This operates as a Fake Maximizer. It uses the noble cover of 'fairness' to mask a highly destructive capture loop that extracts political agency.",
            "9/ By erasing representation, the system moves further from empirical reality. A healthy democracy requires a high Net Reality Ratio, reflecting its actual people.",
            "10/ The dominant failure point here is Egoic Capture. The system has become obsessed with its own preservation rather than fulfilling its functional purpose.",
            "11/ When we look at the Cause and Effect: the cause is fear of lost power. The effect is the structural disenfranchisement of marginalized communities.",
            "12/ We must recognize these actions for what they are: not administrative tweaks, but deliberate acts of systemic extraction and destruction.",
            "13/ True democratic integrity requires moving toward the Greater Good—building systems that empower every voice, rather than silencing them.",
            "14/ We can't afford to stay asleep. Defending the integrity of our voting maps is the baseline requirement for maintaining a functional, just society."
        ]
    },
    {
        "subject_slug": "xavier_becerra",
        "subject": "Xavier Becerra's Political Rise",
        "link": "https://www.washingtonpost.com/politics/2026/05/31/xavier-becerra-surprise-pick-bidens-cabinet-hopes-defy-odds-again-california-governor/?utm_campaign=wp_main&utm_source=bluesky&utm_medium=social",
        "target_url": "https://bsky.app/profile/washingtonpost.com/post/3mn6yavpkwo2a",
        "mode": "reply",
        "claim_u": 1.0, "claim_psi": 1.0,
        "real_u": -1.0, "real_psi": 1.0,
        "posts": [
            "1/ We are auditing the career ascension of political figures like Xavier Becerra.\nTarget Post: https://www.washingtonpost.com/politics/2026/05/31/xavier-becerra-surprise-pick-bidens-cabinet-hopes-defy-odds-again-california-governor/\n\nPsochic Hegemony Graph",
            "2/ Claim: Political careers are often framed as the Greater Good (+1.0, +1.0). The narrative is always about active public service and systemic value creation.",
            "3/ Reality: Often, it's the Greatest Lie (-1.0, +1.0). The energy is highly proactive, but the true beneficiary is the individual or their immediate political tribe.",
            "4/ The Verdict? FAIL. This follows The Path of The Fall. The structural reality reveals tribal ambition masquerading as universal public service.",
            "5/ Who is the primary agent? The politician. While some public good occurs, the primary thermodynamic drive is the consolidation of personal and tribal power.",
            "6/ We must examine the Hypocrisy Gap. What is the distance between the idealized projection of 'serving the people' and the pragmatic reality of campaigning?",
            "7/ This is the danger of the Fake Maximizer. The 'public servant' narrative acts as bait, providing moral cover for the extraction of political capital.",
            "8/ The Helxis Capture Loop here is subtle. The system demands that leaders prioritize optics and tribal loyalty over empirical, systemic problem-solving.",
            "9/ When the Net Reality Ratio drops, we see Semantic Drift. 'Public service' becomes redefined as merely 'winning the next election.'",
            "10/ The dominant failure point is often Egoic Capture. The individual becomes convinced that their personal success is synonymous with the public good.",
            "11/ We need to separate the function from the ego. A true public servant operates from a place of Grace, building value without the need for extraction.",
            "12/ But our current political incentive structures heavily reward the Greatest Lie. They reward proactive tribalism over quiet, systemic maintenance.",
            "13/ This isn't just about one person; it's about the archetype of the modern politician and the thermodynamic pressures that shape their actions.",
            "14/ Until we realign these incentives, the path of political ascension will continue to be paved with tribal allegiances rather than universal truths."
        ]
    },
    {
        "subject_slug": "sandy_shooting",
        "subject": "Public Violence in Sandy",
        "link": "https://www.opb.org/article/2026/05/31/reported-shooting-in-sandy-draws-large-police-response-sunday-evening/",
        "target_url": "https://bsky.app/profile/opb.org/post/3mn722zowmu2e",
        "mode": "reply",
        "claim_u": -1.0, "claim_psi": 1.0,
        "real_u": -1.0, "real_psi": -1.0,
        "posts": [
            "1/ We're conducting a systemic audit on acts of public violence, focusing on Sandy, OR.\nTarget Post: https://www.opb.org/article/2026/05/31/reported-shooting-in-sandy-draws-large-police-response-sunday-evening/\n\nPsochic Hegemony Graph",
            "2/ Claim: The perpetrator often acts from the Greatest Lie (-1.0, +1.0)—a proactive assertion of ego, grievance, or perceived tribal justice.",
            "3/ Reality: It is the Greater Evil (-1.0, -1.0). The act is pure chaos, extracting life, peace, and value from the community for no functional purpose.",
            "4/ The Verdict? FAIL. This maps to The Path of Delusion. The actor believes their proactive violence serves a purpose, but it only creates entropy.",
            "5/ Who is affected? Everyone. The blast radius of such actions extends far beyond the immediate victims, creating systemic necrosis in the community.",
            "6/ The trajectory is a rapid collapse. Violence is the ultimate failure of functional systems, forcing the community into a defensive, reactive posture.",
            "7/ There is no Hypocrisy Gap here to measure, only a complete detachment from reality. The Net Reality Ratio of the actor is functionally zero.",
            "8/ The dominant failure is total Egoic Capture combined with structural delusion. The actor's internal world has completely severed from empirical truth.",
            "9/ The 'Cause' is often untreated psychological pressure or ideological infection. The 'Effect' is immediate thermodynamic destruction of the social fabric.",
            "10/ This is why we must actively build resilient communities. When the baseline of care fails, the resulting chaos extracts a massive toll.",
            "11/ The police response, conversely, attempts to restore the Greater Good (+1.0, +1.0) by actively suppressing the chaos and re-establishing order.",
            "12/ But order is only the first step. True systemic justice requires understanding and dismantling the pathways that lead to such delusional violence.",
            "13/ We must move beyond simply reacting to the collapse. We need proactive systems that identify and heal semantic and psychological drift before it breaks.",
            "14/ Every act of violence is a tragedy and a systemic failure. Our goal must be to build structures that render The Path of Delusion obsolete."
        ]
    },
    {
        "subject_slug": "ice_facility",
        "subject": "For-Profit ICE Facility",
        "link": "https://www.sltrib.com/opinion/letters/2026/05/31/letter-what-could-we-expect-an-ice/?utm_campaign=snd-autopilot",
        "target_url": "https://bsky.app/profile/sltrib.com/post/3mn6v4qvlg325",
        "mode": "reply",
        "claim_u": 1.0, "claim_psi": 1.0,
        "real_u": -1.0, "real_psi": -1.0,
        "posts": [
            "1/ We're auditing the systemic impact of for-profit ICE detention facilities.\nTarget Post: https://www.sltrib.com/opinion/letters/2026/05/31/letter-what-could-we-expect-an-ice/\n\nPsochic Hegemony Graph",
            "2/ Claim: The system claims to operate for the Greater Good (+1.0, +1.0), proactively ensuring national security and upholding the rule of law.",
            "3/ Reality: It operates as a Greater Evil (-1.0, -1.0). It is an extractive model that generates profit by actively detaining and isolating vulnerable people.",
            "4/ The Verdict? FAIL. This maps to The Path of Deception. A narrative of public safety is used to mask a highly destructive, tribal profit engine.",
            "5/ Who benefits? A small group of corporate shareholders and contractors. Who pays the price? The detainees and the moral integrity of the wider society.",
            "6/ This is a prime example of a Fake Maximizer. The 'security' narrative is the bait, providing cover for the true intent: extracting capital from human bodies.",
            "7/ The Helxis Capture Loop is blatant. The corporation requires a constant supply of detainees to maintain its profit margins, incentivizing stricter enforcement.",
            "8/ The Hypocrisy Gap is massive. The system claims to enforce the law, but relies on a business model that fundamentally degrades human dignity.",
            "9/ The Net Reality Ratio is low because the stated purpose (security) is decoupled from the actual function (profit). It is systemic necrosis by design.",
            "10/ When a system’s survival depends on maximizing incarceration, it will inevitably distort the legal framework to ensure its own feeding.",
            "11/ The tribal boundary here is absolute. The system categorizes individuals as 'out-groups' to justify their commodification and extraction.",
            "12/ True security cannot be built on a foundation of extraction. A healthy system seeks to integrate and uplift, not isolate and exploit.",
            "13/ We must recognize that outsourcing justice to profit-driven entities always results in The Path of Deception. The incentives are mathematically flawed.",
            "14/ Realigning this requires moving toward Grace. We must dismantle systems that profit from suffering and build frameworks that serve the well-being of all."
        ]
    },
    {
        "subject_slug": "graze_social",
        "subject": "Graze Social Infrastructure",
        "link": "https://bsky.app/profile/aendra.com/post/3miiiuexl7k22",
        "target_url": "https://bsky.app/profile/aendra.com/post/3miiiuexl7k22",
        "mode": "reply",
        "claim_u": 1.0, "claim_psi": -1.0,
        "real_u": 1.0, "real_psi": 1.0,
        "posts": [
            "1/ We're conducting a positive audit on open social infrastructure, looking at Graze.social.\nTarget Post: https://bsky.app/profile/aendra.com/post/3miiiuexl7k22\n\nPsochic Hegemony Graph",
            "2/ Claim: The service is presented modestly as a Lesser Good (+1.0, -1.0)—a passive tool provided free of charge for the community to use.",
            "3/ Reality: It functions as a Greater Good (+1.0, +1.0). It is actively creating systemic value, empowering users, and building resilient infrastructure.",
            "4/ The Verdict? PASS. This maps to The Path of Grace. It moves from passive provision to active, community-sustained creation.",
            "5/ Who benefits? Everyone. By democratizing the feed ecosystem, it breaks down tribal boundaries and allows for a pluralistic exchange of information.",
            "6/ The thermodynamic pressure here is positive. The creator is absorbing the cost to provide value, and now seeks a minor, equitable contribution to scale it.",
            "7/ There is no Hypocrisy Gap. The stated intent aligns perfectly with the pragmatic action. The Net Reality Ratio is incredibly high (1.00).",
            "8/ This is the opposite of a Fake Maximizer. There is no bait, no cover, and no hidden extraction. The intent is transparent and mutually beneficial.",
            "9/ The requested $1/mo contribution is an honest 'For You, Me, and Everyone' loop. It asks for a tiny input to sustain a massive systemic output.",
            "10/ This model prevents Egoic Capture by decentralizing control. Users are empowered to remix and customize their experience, retaining their agency.",
            "11/ The dominant strength here is Systemic Integrity. It relies on the collective goodwill and functional cooperation of its user base.",
            "12/ When we support infrastructure like this, we actively vote against extractive algorithms and corporate silos. We choose the Greater Good.",
            "13/ This is what real progress looks like. It isn't flashy; it's the quiet, consistent work of building tools that serve the actual needs of the people.",
            "14/ By chipping in and supporting open ecosystems, we can ensure that the future of the social web remains on The Path of Grace."
        ]
    }
]

for d in data:
    filepath = os.path.join("e:\\Vector Field Theory\\VFT Docs\\scratch", f"factcheck_{d['subject_slug']}.json")
    with open(filepath, 'w') as f:
        json.dump(d, f, indent=2)
    print(f"Wrote {filepath}")

