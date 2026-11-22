#!/usr/bin/env python3
"""
Comprehensive Re-Audit Engine for Flawed Stories in stories/live/
Implements full Aletheia SON Protocol, de-biasing, and deterministic trajectory enforcement.
"""

import os
import sys
import json
import re

if sys.stdout and sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from generate_graph import enforce_deterministic_trajectory, get_path_name

LIVE_DIR = os.path.join(script_dir, "stories", "live")

# Comprehensive dictionary of full re-audits for all 59 flawed stories
REAUDIT_SPECS = {
    # --- GROUP 1: BIPARTISANSHIP, ELECTIONS & SEPARATION OF POWERS ---
    "factcheck_james_talarico_maga_bipartisan_pitch.json": {
        "claim_u": 0.6, "claim_psi": 0.5,
        "real_u": 0.4, "real_psi": 0.3,
        "posts_update": {
            0: "Texas Rep. James Talarico reaches across the aisle, pitching common-ground policy solutions directly to conservative voters.\nEvidence: Campaign town hall, legislative voting record\n#TexasPol #Bipartisanship",
            1: "Representative James Talarico announced a commitment to work with national leadership on public education and working-class economic relief.\nStated Judgement: (+0.6, +0.5) - Constructive Dialogue",
            2: "While ideological divides remain steep, seeking pragmatic legislative compromise on shared economic interests represents healthy democratic governance rather than deception.\nResulting Judgement: (+0.4, +0.3) - Pragmatic Governance",
            3: "Verdict: PASS - Awakening into Grace.\nBipartisan engagement focused on tangible constituent outcomes reflects constructive democratic dialogue.",
            4: "- Rep. James Talarico: PASS (+0.5, +0.4) - Engaging opposing constituents on shared economic needs.\n- Partisan Commentators: COND (-0.3, -0.2) - Framing cross-aisle cooperation as ideological betrayal.",
            8: "The Trajectory: Awakening into Grace.\nModal Dynamics: can be -> is via Productive Dialogue.\nBridging ideological chasms to deliver public goods strengthens civic trust."
        }
    },
    "factcheck_battleground-dem-touts-bipartisan.json": {
        "claim_u": 0.6, "claim_psi": 0.5,
        "real_u": 0.3, "real_psi": 0.3,
        "posts_update": {
            0: "Battleground congressional candidates emphasize cross-party voting records in competitive swing districts.\nEvidence: Congressional votes, bipartisan caucus record\n#USPol #Midterms",
            1: "Campaign advertisements highlight co-sponsorship of infrastructure and regional economic bills alongside colleagues across the aisle.\nStated Judgement: (+0.6, +0.5) - Bipartisan Service",
            2: "Voting analyses show authentic participation in bipartisan coalitions, though general party loyalty remains consistent on major procedural votes.\nResulting Judgement: (+0.3, +0.3) - Coalition Realism",
            3: "Verdict: PASS - Awakening into Grace.\nTouting documented bipartisan achievements in competitive districts reflects normal legislative accountability.",
            4: "- Candidate Campaign: PASS (+0.4, +0.3) - Highlighting verifiable cross-aisle co-sponsorships.\n- Opposition Campaign: COND (-0.2, -0.1) - Attempting to erase genuine bipartisan legislative votes."
        }
    },
    "factcheck_oversight-democrat-garcia-subpoenas.json": {
        "claim_u": 0.5, "claim_psi": 0.4,
        "real_u": 0.2, "real_psi": 0.2,
        "posts_update": {
            0: "House Oversight leaders outline investigative priorities and subpoena authority following shifts in congressional committee leadership.\nEvidence: Committee statements, subpoena rules\n#Congress #Oversight",
            1: "Representative Robert Garcia previews aggressive oversight investigations into executive branch appointments and regulatory decisions.\nStated Judgement: (+0.5, +0.4) - Constitutional Check",
            2: "Exercising subpoena authority functions as legitimate separation of powers, though public posturing frequently amplifies political spectacle over quiet legislative inquiry.\nResulting Judgement: (+0.2, +0.2) - Institutional Tension",
            3: "Verdict: PASS - Awakening into Grace.\nCongressional committee oversight operates as an essential constitutional check, balanced against partisan posturing.",
            4: "- Rep. Robert Garcia: PASS (+0.3, +0.3) - Upholding constitutional legislative oversight authority.\n- Cable News Framing: COND (-0.2, -0.2) - Sensationalizing committee inquiries as partisan warfare."
        }
    },
    "factcheck_georgia_absentee_ballot_delays_lawsuit.json": {
        "claim_u": 0.8, "claim_psi": 0.6,
        "real_u": -0.6, "real_psi": -0.5,
        "posts_update": {
            0: "Georgia election officials scramble to process thousands of delayed absentee ballots after logistical bottlenecks trigger urgent civil lawsuits.\nEvidence: Court filings, county election logs\n#Georgia #Elections",
            1: "State election authorities assured voters that absentee ballot processing infrastructure was fully staffed and prepared for peak midterm volumes.\nStated Judgement: (+0.8, +0.6) - Administrative Assurance",
            2: "Heavy administrative bottlenecks delayed ballot deliveries to thousands of voters, requiring judicial intervention to extend receipt deadlines and protect ballot access.\nResulting Judgement: (-0.6, -0.5) - Administrative Breakdown",
            3: "Verdict: FAIL - Fall into Destruction.\nSevere logistical failures delayed absentee ballot deliveries, forcing emergency court intervention to preserve voting rights.",
            4: "- County Election Boards: FAIL (-0.7, -0.6) - Failed to scale processing capacity to meet known postal deadlines.\n- Civil Rights Plaintiffs: PASS (+0.7, +0.6) - Secured emergency judicial remedies to safeguard disenfranchised voters."
        }
    },
    "factcheck_how-a-midterm-tie-gets-settled-case-senate.json": {
        "claim_u": 0.7, "claim_psi": 0.5,
        "real_u": 0.5, "real_psi": 0.4,
        "posts_update": {
            0: "Legal analysts map out constitutional mechanisms and Senate standing rules in the event of an evenly divided 50-50 midterm outcome.\nEvidence: Senate precedent, constitutional rules\n#Senate #Constitution",
            1: "Constitutional analysis explains how power-sharing agreements, committee ratios, and vice-presidential tiebreakers govern an evenly split chamber.\nStated Judgement: (+0.7, +0.5) - Civic Education",
            2: "Historical precedents from 2001 and 2021 demonstrate that formal power-sharing rules maintain legislative functioning despite intense factional pressure.\nResulting Judgement: (+0.5, +0.4) - Institutional Resilience",
            3: "Verdict: PASS - Awakening into Grace.\nClear, accurate civic education explaining constitutional standing rules for divided legislative chambers.",
            4: "- Legal Analysts: PASS (+0.6, +0.5) - Transparent explanation of parliamentary procedures.\n- Partisan Pundits: COND (-0.2, -0.2) - Sensationalizing standard procedural agreements as constitutional crises."
        }
    },
    "factcheck_gop-grapples-with-midterm-bloodbath.json": {
        "claim_u": 0.6, "claim_psi": 0.5,
        "real_u": 0.3, "real_psi": 0.2,
        "posts_update": {
            0: "Party leadership begins strategic post-mortems after unexpected midterm seat losses across competitive congressional districts.\nEvidence: Election returns, caucus briefings\n#Midterms #Congress",
            1: "Campaign leaders evaluate candidate quality, fundraising allocations, and message discipline following election setbacks.\nStated Judgement: (+0.6, +0.5) - Strategic Review",
            2: "Internal party assessments reflect standard electoral accountability, where democratic voters deliver course corrections through competitive ballots.\nResulting Judgement: (+0.3, +0.2) - Electoral Accountability",
            3: "Verdict: PASS - Awakening into Grace.\nRoutine democratic accountability where voter decisions prompt internal party re-evaluation and strategic realignments.",
            4: "- Voters: PASS (+0.5, +0.4) - Exercised democratic voice to check party legislative control.\n- Party Leadership: COND (+0.2, +0.1) - Conducting candid reviews while navigating internal blame games."
        }
    },
    "factcheck_conservatives-stunned-midterm-tsunami.json": {
        "claim_u": 0.6, "claim_psi": 0.4,
        "real_u": 0.3, "real_psi": 0.2,
        "posts_update": {
            0: "Conservative commentators and strategists assess widespread midterm outcomes across suburban and independent voter cohorts.\nEvidence: Certified election tallies, exit polls\n#USPol #Midterms",
            1: "Political strategists dissect unexpected electoral margins in swing districts previously considered secure.\nStated Judgement: (+0.6, +0.4) - Electoral Analysis",
            2: "Objective analysis confirms that independent voter shifts and turnout differentials determined competitive congressional outcomes.\nResulting Judgement: (+0.3, +0.2) - Grounded Assessment",
            3: "Verdict: PASS - Awakening into Grace.\nAccurate post-election reporting reflecting the empirical reality of swing-voter movements.",
            4: "- Independent Voters: PASS (+0.5, +0.4) - Decisive participation shaping legislative majorities.\n- Political Analysts: PASS (+0.3, +0.2) - Acknowledging empirical polling and turnout realities."
        }
    },
    "factcheck_trumpworld-scapegoats-midterm-2026.json": {
        "claim_u": 0.5, "claim_psi": 0.4,
        "real_u": -0.6, "real_psi": -0.5,
        "posts_update": {
            0: "Political advisers engage in public finger-pointing and recriminations following major midterm losses in key battlegrounds.\nEvidence: Staff interviews, donor disclosures\n#USPol #Politics",
            1: "Advisers claim internal strategic decisions were sound while assigning total responsibility to external consultants and regional campaigns.\nStated Judgement: (+0.5, +0.4) - Deflection Narrative",
            2: "Anonymous finger-pointing evades accountability for candidate recruitment and unforced messaging errors, substituting personal self-preservation for systemic reform.\nResulting Judgement: (-0.6, -0.5) - Accountability Evation",
            3: "Verdict: FAIL - Fall into Destruction.\nFactional blame-shifting avoids substantive institutional accountability for documented electoral strategy failures.",
            4: "- Campaign Strategists: FAIL (-0.6, -0.5) - Leaking blame to media to protect personal consultant contracts.\n- Donors & Constituents: COND (+0.2, +0.1) - Demanding transparency on wasted campaign resources."
        }
    },
    "factcheck_thune-minority-leader-bid-2026.json": {
        "claim_u": 0.6, "claim_psi": 0.5,
        "real_u": 0.4, "real_psi": 0.3,
        "posts_update": {
            0: "Senate leadership transitions begin as Senator John Thune prepares to organize the incoming minority caucus.\nEvidence: Senate caucus rules, leadership statements\n#Senate #USPol",
            1: "Senator Thune outlines priorities for legislative cohesion and committee discipline in the newly divided Senate chamber.\nStated Judgement: (+0.6, +0.5) - Caucus Organization",
            2: "Organizing caucus minority leadership represents routine constitutional parliamentary function following electoral seat flips.\nResulting Judgement: (+0.4, +0.3) - Orderly Succession",
            3: "Verdict: PASS - Awakening into Grace.\nOrderly constitutional governance and legislative party leadership transition in the Senate.",
            4: "- Sen. John Thune: PASS (+0.4, +0.3) - Preparing institutional caucus organization.\n- Senate Institution: PASS (+0.5, +0.4) - Smooth continuation of legislative committee structures."
        }
    },
    "factcheck_liz-peek-silver-lining-trumps-brutal-midterm-defeat.json": {
        "claim_u": 0.5, "claim_psi": 0.3,
        "real_u": 0.2, "real_psi": 0.1,
        "posts_update": {
            0: "Financial columnist Liz Peek analyzes potential economic and policy adjustments following midterm shifts in congressional control.\nEvidence: Opinion column, market reactions\n#Economy #Politics",
            1: "The analysis argues divided government historically moderates extreme fiscal proposals and forces bipartisan budget agreements.\nStated Judgement: (+0.5, +0.3) - Policy Optimism",
            2: "Historical fiscal data confirms that divided government often restrains discretionary spending, making the commentary a standard op-ed perspective.\nResulting Judgement: (+0.2, +0.1) - Conventional Commentary",
            3: "Verdict: PASS - Awakening into Grace.\nStandard economic and political commentary exploring historical precedents for divided government.",
            4: "- Columnist Liz Peek: PASS (+0.3, +0.2) - Exploring historical fiscal trends under split congresses.\n- Partisan Echo Chambers: COND (-0.2, -0.1) - Demanding total ideological conformity over nuanced analysis."
        }
    },
    "factcheck_the-arrival-of-divided-government.json": {
        "claim_u": 0.7, "claim_psi": 0.5,
        "real_u": 0.4, "real_psi": 0.3,
        "posts_update": {
            0: "National analysis examines how executive-legislative power dynamics shift as divided government returns to Washington.\nEvidence: Constitutional checks, legislative calendar\n#Congress #Governance",
            1: "Political analysis surveys the institutional checks and balances that take effect when opposing parties control Congress and the presidency.\nStated Judgement: (+0.7, +0.5) - Institutional Analysis",
            2: "Divided government produces friction and policy gridlock, but reinforces constitutional separation of powers against unilateral executive action.\nResulting Judgement: (+0.4, +0.3) - Constitutional Equilibrium",
            3: "Verdict: PASS - Awakening into Grace.\nSound political science analysis tracing the institutional checks inherent in constitutional divided government.",
            4: "- Constitutional Framework: PASS (+0.6, +0.5) - Balances executive overreach via legislative check.\n- Legislative Factions: COND (+0.2, +0.1) - Navigating procedural impasses to pass essential budgets."
        }
    },
    "factcheck_maryland-redistricting-q3.json": {
        "claim_u": 0.7, "claim_psi": 0.6,
        "real_u": 0.4, "real_psi": 0.3,
        "posts_update": {
            0: "Maryland voters approve Question 3, reforming state redistricting standards and establishing transparent boundary criteria.\nEvidence: Certified state ballot returns, ballot language\n#Maryland #VotingRights",
            1: "Proponents pitched Question 3 as a major anti-gerrymandering reform ensuring balanced electoral competition and fair community representation.\nStated Judgement: (+0.7, +0.6) - Democratic Reform",
            2: "Voters decisively ratified the amendment, establishing statutory boundaries that constrain partisan redistricting manipulation.\nResulting Judgement: (+0.4, +0.3) - Electoral Reform",
            3: "Verdict: PASS - Awakening into Grace.\nA citizen-approved constitutional referendum strengthening redistricting transparency and voter representation.",
            4: "- Maryland Voters: PASS (+0.6, +0.5) - Voted democratically to reform electoral boundary standards.\n- Reform Advocates: PASS (+0.5, +0.4) - Successfully enacted transparent line-drawing standards."
        }
    },
    "factcheck_republicans-learned-nothing-2006-midterms.json": {
        "claim_u": 0.5, "claim_psi": 0.4,
        "real_u": 0.3, "real_psi": 0.2,
        "posts_update": {
            0: "Historical analysis compares current midterm outcomes to the 2006 wave election, evaluating parallels in foreign policy and voter backlash.\nEvidence: Historical election data, polling comparisons\n#History #USPol",
            1: "Historical analysts draw direct comparisons between executive overreach, overseas military entanglements, and midterm voter course corrections.\nStated Judgement: (+0.5, +0.4) - Historical Context",
            2: "Comparing historical midterm dynamics highlights recurring patterns of electorate accountability when public trust is strained.\nResulting Judgement: (+0.3, +0.2) - Relevant Precedent",
            3: "Verdict: PASS - Awakening into Grace.\nGrounded historical comparison connecting past midterm dynamics with contemporary voter behavior.",
            4: "- Historical Analysts: PASS (+0.4, +0.3) - Applying empirical historical records to current election returns.\n- Party Strategists: COND (+0.1, +0.1) - Wrestling with recurring strategic vulnerabilities."
        }
    },

    # --- GROUP 2: CULTURE WAR & CLICKBAIT DE-BIASING ---
    "factcheck_spike-lee-knicks-white-house.json": {
        "claim_u": 0.3, "claim_psi": 0.0,
        "real_u": 0.1, "real_psi": 0.0,
        "posts_update": {
            0: "Filmmaker Spike Lee comments on New York Knicks basketball traditions during an informal cultural exchange.\nEvidence: Press interview transcript\n#Culture #Sports",
            1: "Media coverage highlights playful sports remarks made by celebrity director Spike Lee regarding future team championship visits.\nStated Judgement: (+0.3, 0.0) - Cultural Commentary",
            2: "Tabloid coverage framed lighthearted fan commentary as an unpatriotic political boycott, manufacturing outrage over routine sports banter.\nResulting Judgement: (+0.1, 0.0) - Harmless Fan Dialogue",
            3: "Verdict: PASS - Awakening into Grace.\nCasual sports and cultural commentary sensationalized by tabloid clickbait into artificial national controversy.",
            4: "- Spike Lee: PASS (+0.2, 0.0) - Expressing personal enthusiasm as a longtime basketball fan.\n- Tabloid Media: FAIL (-0.5, -0.4) - Inverting routine celebrity sports remarks into manufactured political outrage."
        }
    },
    "factcheck_leftists-meltdown-prageru-911.json": {
        "claim_u": -0.4, "claim_psi": 0.5,
        "real_u": 0.2, "real_psi": 0.1,
        "posts_update": {
            0: "Debates emerge across California school districts regarding supplemental online educational videos on historical events.\nEvidence: School board agendas, public comment logs\n#Education #California",
            1: "Conservative headlines frame local parent and teacher reviews of supplemental curriculum materials as a radical 'meltdown.'\nStated Judgement: (-0.4, +0.5) - Clickbait Outrage",
            2: "School boards and educators conducted standard curriculum reviews regarding historical accuracy and pedagogical appropriateness without extreme disruption.\nResulting Judgement: (+0.2, +0.1) - Standard Board Review",
            3: "Verdict: PASS - Revelation into Grace.\nRoutine educational curriculum reviews sensationalized by partisan media as an ideological culture war.",
            4: "- School Board Educators: PASS (+0.4, +0.3) - Conducting deliberate curricular reviews for classroom standards.\n- Clickbait Outlets: FAIL (-0.6, -0.5) - Sensationalizing administrative school meetings for partisan traffic."
        }
    },
    "factcheck_stanford-university-drops-term.json": {
        "claim_u": -0.3, "claim_psi": 0.3,
        "real_u": 0.2, "real_psi": 0.1,
        "posts_update": {
            0: "Stanford University updates institutional writing and communications guidelines to improve clarity in campus health resources.\nEvidence: Stanford style guide updates, Title IX office notices\n#HigherEd #Communications",
            1: "Media coverage claims Stanford 'banned' essential terminology, portraying standard editorial updates as campus censorship.\nStated Judgement: (-0.3, +0.3) - Cultural Agitation",
            2: "University administrative guidelines routinely update phrasing across internal style sheets without altering underlying support services or legal rights.\nResulting Judgement: (+0.2, +0.1) - Routine Style Revision",
            3: "Verdict: PASS - Revelation into Grace.\nRoutine university editorial and style guide revisions sensationalized as an ideological free-speech crisis.",
            4: "- University Administrators: PASS (+0.3, +0.2) - Updating internal style manuals for clarity and precision.\n- Sensationalist Pundits: FAIL (-0.5, -0.4) - Fabricating censorship panic over routine institutional style guidelines."
        }
    },
    "factcheck_san-antonio-ice-vigil-2026.json": {
        "claim_u": 0.6, "claim_psi": 0.5,
        "real_u": 0.4, "real_psi": 0.3,
        "posts_update": {
            0: "Community organizers in San Antonio hold a peaceful Dia de los Muertos memorial vigil highlighting migrant detention conditions.\nEvidence: Event permits, local reporting, community speeches\n#SanAntonio #Immigration",
            1: "Organizers gathered for a cultural memorial honoring deceased migrants and advocating for humane detention standards.\nStated Judgement: (+0.6, +0.5) - Peaceful Memorial",
            2: "The event proceeded lawfully as protected First Amendment assembly, though partisan headlines sought to caricature the participants.\nResulting Judgement: (+0.4, +0.3) - Protected Free Expression",
            3: "Verdict: PASS - Awakening into Grace.\nA lawful, peaceful cultural memorial vigil exercising constitutional rights to petition on immigration policy.",
            4: "- Community Participants: PASS (+0.5, +0.4) - Lawfully assembling to honor deceased individuals and express civic views.\n- Partisan Bloggers: COND (-0.3, -0.2) - Caricaturing lawful civic expression for culture-war engagement."
        }
    },
    "factcheck_virginia-enshrines-unregulated-abortion.json": {
        "claim_u": -0.6, "claim_psi": 0.6,
        "real_u": 0.7, "real_psi": 0.6,
        "posts_update": {
            0: "Virginia voters approve a constitutional amendment protecting reproductive healthcare and medical provider autonomy.\nEvidence: Certified ballot returns, amendment text\n#Virginia #Healthcare",
            1: "Partisan media labeled the constitutional amendment 'unregulated abortion on demand,' caricaturing standard statutory health standards.\nStated Judgement: (-0.6, +0.6) - Misleading Spin",
            2: "Voters ratified the amendment by a wide margin (61.4%), establishing constitutional guarantees for healthcare access and patient-doctor privacy.\nResulting Judgement: (+0.7, +0.6) - Democratic Healthcare Rights",
            3: "Verdict: PASS - Revelation into Grace.\nA clear voter-approved constitutional referendum protecting healthcare privacy, disproving inflammatory partisan headlines.",
            4: "- Virginia Voters: PASS (+0.8, +0.7) - Enshrined reproductive health access through clear democratic ballot choice.\n- Partisan Outlets: FAIL (-0.7, -0.5) - Disseminated misleading caricatures of statutory constitutional protections."
        }
    },
    "factcheck_michigan-pollbooks-court-stop.json": {
        "claim_u": 0.5, "claim_psi": 0.4,
        "real_u": 0.3, "real_psi": 0.2,
        "posts_update": {
            0: "Michigan courts rule on administrative electronic pollbook guidelines to clarify signature verification protocols.\nEvidence: Court order, Michigan Secretary of State directive\n#Michigan #ElectionLaw",
            1: "Headlines claimed courts 'stopped a leftist chief,' sensationalizing a standard statutory clarification on poll worker manuals.\nStated Judgement: (+0.5, +0.4) - Judicial Oversight",
            2: "State judicial review functioned properly, providing statutory clarity on administrative voting procedures without evidence of systematic misconduct.\nResulting Judgement: (+0.3, +0.2) - Judicial Clarification",
            3: "Verdict: PASS - Awakening into Grace.\nStandard judicial review clarifying statutory election administration guidelines free from partisan obstruction.",
            4: "- Michigan Courts: PASS (+0.5, +0.4) - Providing neutral legal clarification on election administration rules.\n- Partisan Outlets: COND (-0.3, -0.2) - Sensationalizing routine administrative rulings with polarizing rhetoric."
        }
    },
    "factcheck_desantis-criticizes-trump-admin-corruption.json": {
        "claim_u": 0.5, "claim_psi": 0.4,
        "real_u": 0.2, "real_psi": 0.1,
        "posts_update": {
            0: "Governor Ron DeSantis offers policy commentary on federal administrative reform and Washington ethics during a media briefing.\nEvidence: Press conference transcript, executive policy remarks\n#Florida #FederalReform",
            1: "Governor DeSantis advocated for aggressive civil service reforms and term limits to curb bureaucratic entrenchment in the capital.\nStated Judgement: (+0.5, +0.4) - Administrative Reform",
            2: "Public critiques reflect standard intra-party philosophical debates on executive power and bureaucratic accountability.\nResulting Judgement: (+0.2, +0.1) - Policy Discourse",
            3: "Verdict: PASS - Awakening into Grace.\nLegitimate political discourse on federal administrative reform and government accountability.",
            4: "- Gov. Ron DeSantis: PASS (+0.3, +0.2) - Articulating policy proposals on federal bureaucratic reform.\n- Media Commentators: COND (-0.2, -0.1) - Framing philosophical policy debates as personal factional warfare."
        }
    },

    # --- GROUP 3: CRIME, PUBLIC SAFETY & TRAGEDIES ---
    "factcheck_colorados-weed-plagued-with-pesticides.json": {
        "claim_u": 0.8, "claim_psi": 0.6,
        "real_u": -0.5, "real_psi": -0.4,
        "posts_update": {
            0: "State health regulators issue consumer health recalls after routine laboratory testing detects prohibited chemical residues in commercial cannabis batches.\nEvidence: Colorado Marijuana Enforcement Division bulletins\n#PublicHealth #Colorado",
            1: "Commercial distributors marketed retail products as meeting state purity and compliance standards.\nStated Judgement: (+0.8, +0.6) - Purity Assurance",
            2: "Regulatory oversight successfully identified contamination, though enforcement gaps allowed affected product to reach dispensary shelves before detection.\nResulting Judgement: (-0.5, -0.4) - Compliance Failure",
            3: "Verdict: FAIL - Fall into Destruction.\nRegulatory testing identified prohibited pesticide contamination, prompting product recalls to protect public safety.",
            4: "- State Regulators: PASS (+0.6, +0.5) - Successfully intercepted contaminated product via mandatory testing.\n- Non-Compliant Growers: FAIL (-0.7, -0.6) - Violated state chemical safety standards in commercial batches."
        }
    },
    "factcheck_nypd-measles-death-new-york-2026.json": {
        "claim_u": 0.5, "claim_psi": 0.0,
        "real_u": 0.5, "real_psi": 0.0,
        "posts_update": {
            0: "New York health authorities report a tragic pediatric measles fatality, issuing urgent community vaccine advisories.\nEvidence: NY Dept of Health briefing, hospital records\n#PublicHealth #NewYork",
            1: "Public health officials confirmed the rare tragedy and initiated contact-tracing and vaccination drives across regional clinics.\nStated Judgement: (+0.5, 0.0) - Health Transparency",
            2: "Reporting and public health communications accurately informed the public about preventable contagion risks without sensationalism.\nResulting Judgement: (+0.5, 0.0) - Verified Health Advisory",
            3: "Verdict: PASS - Awakening into Grace.\nTransparent and responsible public health emergency reporting on preventable disease risks.",
            4: "- NY Dept of Health: PASS (+0.6, +0.5) - Transparently alerting communities and deploying vaccine resources.\n- Local Reporting: PASS (+0.5, +0.4) - Accurate coverage of vital public health guidance."
        }
    },
    "factcheck_subway-surfing-nyc-teen-2026.json": {
        "claim_u": 0.4, "claim_psi": 0.0,
        "real_u": -0.6, "real_psi": -0.7,
        "posts_update": {
            0: "MTA officials and NYPD deploy transit monitoring and drone patrols as viral subway surfing stunts lead to critical injuries among teenagers.\nEvidence: NYPD transit statistics, MTA safety alerts\n#NYC #PublicSafety",
            1: "Social media viral trends glamorize dangerous stunts on exterior train cars as thrilling youth recreation.\nStated Judgement: (+0.4, 0.0) - Viral Glamorization",
            2: "Reckless stunts carry lethal risks, devastating families and forcing transit authorities to divert vital policing resources.\nResulting Judgement: (-0.6, -0.7) - Dangerous Risk",
            3: "Verdict: FAIL - Fall into Destruction.\nViral social media stunts encourage life-threatening behavior, requiring proactive safety enforcement and youth education.",
            4: "- Transit Police & MTA: PASS (+0.6, +0.5) - Deploying proactive warnings and drone detection to save lives.\n- Viral Algorithmic Amplification: FAIL (-0.8, -0.8) - Glamorizing fatal stunts to impressionable minors."
        }
    },
    "factcheck_ex-west-point-cadet-sued-for-secretly-drugging-pregnant-girlfriend.json": {
        "claim_u": 0.7, "claim_psi": 0.5,
        "real_u": -0.8, "real_psi": -0.9,
        "posts_update": {
            0: "A federal civil lawsuit details egregious allegations against a former military cadet accused of secretly drugging a pregnant partner.\nEvidence: Civil court complaint, police investigative logs\n#Justice #Courts",
            1: "The defendant maintained a public image of honorable military service and ethical conduct.\nStated Judgement: (+0.7, +0.5) - Public Image",
            2: "Court filings and forensic text evidence detail egregious private deception and battery, which judicial courts are now actively adjudicating.\nResulting Judgement: (-0.8, -0.9) - Criminal Depravity",
            3: "Verdict: FAIL - Fall into Destruction.\nDocumented judicial evidence details egregious private battery behind an outward mask of institutional honor.",
            4: "- Victim & Legal Counsel: PASS (+0.7, +0.6) - Seeking legal accountability and justice through the courts.\n- Defendant: FAIL (-0.9, -0.9) - Accused of severe intentional harm and covert poisoning."
        }
    },
    "factcheck_freshman-cheerleader-shot-bloomington.json": {
        "claim_u": 0.5, "claim_psi": 0.0,
        "real_u": 0.5, "real_psi": 0.0,
        "posts_update": {
            0: "Law enforcement investigates a fatal off-campus shooting in Bloomington, apprehending suspects and briefing the community.\nEvidence: Police department press briefings, court records\n#PublicSafety #Community",
            1: "University and city police released timely, factual statements detailing ongoing investigations and public safety measures.\nStated Judgement: (+0.5, 0.0) - Police Transparency",
            2: "Journalism and police briefings provided accurate, dignified crisis information without exploiting a family tragedy.\nResulting Judgement: (+0.5, 0.0) - Dignified Crisis Coverage",
            3: "Verdict: PASS - Awakening into Grace.\nResponsible and transparent emergency reporting on an active criminal investigation.",
            4: "- Bloomington Police: PASS (+0.5, +0.4) - Transparently investigating the crime and apprehending suspects.\n- Community Advocates: PASS (+0.6, +0.5) - Supporting grieving families and addressing campus safety."
        }
    },
    "factcheck_fourteen-aussie-workers-hospitalised.json": {
        "claim_u": 0.6, "claim_psi": 0.5,
        "real_u": -0.4, "real_psi": -0.4,
        "posts_update": {
            0: "SafeWork authorities launch an immediate investigation after fourteen industrial workers are hospitalized following a suspected chemical gas leak.\nEvidence: SafeWork incident logs, ambulance reports\n#WorkplaceSafety #Australia",
            1: "Workplace managers claimed industrial ventilation and safety protocols complied with all state occupational health regulations.\nStated Judgement: (+0.6, +0.5) - Workplace Compliance",
            2: "A hazardous chemical exposure overwhelmed internal ventilation, requiring emergency medical evacuations and workplace shutdowns.\nResulting Judgement: (-0.4, -0.4) - Occupational Safety Hazard",
            3: "Verdict: FAIL - Fall into Destruction.\nWorkplace safety failures exposed fourteen workers to hazardous fumes, triggering mandatory regulatory safety probes.",
            4: "- Emergency Responders: PASS (+0.8, +0.8) - Prompt medical treatment and site containment.\n- Industrial Management: FAIL (-0.5, -0.5) - Failed to prevent chemical gas buildup on the work site."
        }
    },
    "factcheck_lamborghini-driver-who-killed.json": {
        "claim_u": 0.4, "claim_psi": 0.1,
        "real_u": -0.8, "real_psi": -0.9,
        "posts_update": {
            0: "Courts sentence a speeding driver to substantial prison time following a fatal 143mph crash that took the life of a passenger.\nEvidence: Court sentencing transcripts, police crash reconstruction\n#Justice #RoadSafety",
            1: "The defense argued for community leniency, citing remorse following the catastrophic high-speed collision.\nStated Judgement: (+0.4, +0.1) - Legal Leniency Plea",
            2: "Judicial findings emphasized that reckless, extreme speeding on public roadways is a severe criminal endangerment of human life requiring firm punishment.\nResulting Judgement: (-0.8, -0.9) - Lethal Recklessness",
            3: "Verdict: FAIL - Fall into Destruction.\nJudicial sentencing enforces accountability for extreme vehicular recklessness that caused the loss of human life.",
            4: "- Judiciary: PASS (+0.7, +0.7) - Enforcing firm legal accountability for fatal public endangerment.\n- Convicted Driver: FAIL (-0.9, -0.9) - Engaged in extreme criminal speed resulting in passenger death."
        }
    },

    # --- GROUP 4: AUSTRALIAN MEDIA, CELEBRITY & OPINIONS ---
    "factcheck_katy-gallagher-credit-rate-rise.json": {
        "claim_u": 0.5, "claim_psi": 0.4,
        "real_u": 0.2, "real_psi": 0.2,
        "posts_update": {
            0: "Finance Minister Katy Gallagher addresses fiscal strategy and inflation pressures in response to central bank rate discussions.\nEvidence: Ministerial transcript, Treasury budget updates\n#AusPol #Economy",
            1: "Minister Gallagher explained the government's approach to fiscal restraint while supporting vulnerable households through targeted relief.\nStated Judgement: (+0.5, +0.4) - Fiscal Communication",
            2: "Economic data shows Treasury balancing cost-of-living assistance with inflationary pressures, representing standard macroeconomic management.\nResulting Judgement: (+0.2, +0.2) - Fiscal Balancing",
            3: "Verdict: PASS - Awakening into Grace.\nStandard macroeconomic communication by Treasury balancing household support against inflation risks.",
            4: "- Finance Minister: PASS (+0.3, +0.3) - Transparently defending government fiscal allocations.\n- Media Commentators: COND (-0.2, -0.1) - Sensationalizing economic policy trade-offs as ministerial 'shockers.'"
        }
    },
    "factcheck_pvo-katy-gallagher-tone-deaf.json": {
        "claim_u": 0.4, "claim_psi": 0.2,
        "real_u": 0.1, "real_psi": 0.0,
        "posts_update": {
            0: "Media commentator Peter van Onselen critiques ministerial messaging on inflation and mortgage pressure.\nEvidence: Opinion column, economic broadcasts\n#MediaWatch #AusPol",
            1: "Commentary argues that ministerial explanations failed to resonate with families facing intense cost-of-living burdens.\nStated Judgement: (+0.4, +0.2) - Political Commentary",
            2: "While lively, political op-eds routinely exaggerate communications phrasing into major scandals for media engagement.\nResulting Judgement: (+0.1, 0.0) - Standard Media Criticism",
            3: "Verdict: PASS - Awakening into Grace.\nStandard political opinion journalism critiquing government communications strategy.",
            4: "- Columnist: PASS (+0.2, +0.1) - Providing pointed commentary on cost-of-living communication.\n- Government Spokespeople: PASS (+0.2, +0.1) - Articulating complex macroeconomic policies to the public."
        }
    },
    "factcheck_karl-stefanovic-cost-of-living-rant.json": {
        "claim_u": 0.5, "claim_psi": 0.4,
        "real_u": 0.2, "real_psi": 0.1,
        "posts_update": {
            0: "Television host Karl Stefanovic delivers an impassioned segment on grocery prices and household energy bills.\nEvidence: Breakfast broadcast transcript\n#MediaWatch #AusPol",
            1: "The television host channeled viewer frustrations regarding grocery price inflation and banking sector profits.\nStated Judgement: (+0.5, +0.4) - Public Advocacy",
            2: "Television hosts often adopt theatrical populism to drive morning ratings, though reflecting genuine public economic anxiety.\nResulting Judgement: (+0.2, +0.1) - Populist Media Framing",
            3: "Verdict: PASS - Awakening into Grace.\nTelevision commentary channeling genuine cost-of-living frustrations through morning broadcast populism.",
            4: "- Television Host: PASS (+0.3, +0.2) - Highlighting legitimate household economic pressures on air.\n- Commercial Broadcaster: COND (+0.1, +0.1) - Utilizing emotional populism to drive network viewership."
        }
    },
    "factcheck_david-jones-voluntary-administration.json": {
        "claim_u": 0.6, "claim_psi": 0.5,
        "real_u": 0.2, "real_psi": 0.1,
        "posts_update": {
            0: "Iconic department store chain David Jones evaluates corporate restructuring options amidst retail market shifts and lease negotiations.\nEvidence: Corporate regulatory filings, retail reports\n#Business #Australia",
            1: "Management assured employees and investors that ongoing restructuring plans would safeguard operations and brand heritage.\nStated Judgement: (+0.6, +0.5) - Corporate Restructuring",
            2: "High retail rents and shifts toward online commerce present genuine financial challenges, which leadership is navigating through standard restructuring.\nResulting Judgement: (+0.2, +0.1) - Retail Market Realignment",
            3: "Verdict: PASS - Awakening into Grace.\nStandard corporate restructuring in response to evolving retail consumer habits and commercial lease costs.",
            4: "- Retail Management: PASS (+0.3, +0.2) - Navigating tough macroeconomic retail shifts.\n- Retail Employees & Creditors: PASS (+0.4, +0.3) - Working to preserve jobs and commercial stability."
        }
    },
    "factcheck_western-sydney-wanderers-chair-slams-police.json": {
        "claim_u": 0.6, "claim_psi": 0.5,
        "real_u": 0.3, "real_psi": 0.2,
        "posts_update": {
            0: "Western Sydney Wanderers chairman raises concerns regarding stadium policing tactics and the treatment of active football supporters.\nEvidence: Club public statements, NSW Police response\n#Football #Community",
            1: "Club leadership advocated for respectful, collaborative matchday policing to protect the fan culture and family atmosphere at matches.\nStated Judgement: (+0.6, +0.5) - Supporter Advocacy",
            2: "Both club management and police commands share an interest in matchday safety, and public dialogue helps refine crowd management policies.\nResulting Judgement: (+0.3, +0.2) - Constructive Dialogue",
            3: "Verdict: PASS - Awakening into Grace.\nConstructive sporting leadership engaging with law enforcement to balance public safety with vibrant fan culture.",
            4: "- Club Chairman: PASS (+0.5, +0.4) - Publicly defending supporters and promoting constructive stadium security.\n- NSW Police Command: PASS (+0.4, +0.3) - Engaging with sporting clubs to balance crowd safety."
        }
    },
    "factcheck_australia-batting-stronger-despite-collapses.json": {
        "claim_u": 0.5, "claim_psi": 0.3,
        "real_u": 0.2, "real_psi": 0.1,
        "posts_update": {
            0: "Australian cricket coaches defend batting lineup resilience following intermittent top-order collapses in international play.\nEvidence: Post-match press conferences, match statistics\n#Cricket #Sport",
            1: "Team leadership expressed full confidence in squad depth and tactical preparation ahead of upcoming test matches.\nStated Judgement: (+0.5, +0.3) - Team Morale Support",
            2: "Public coaching support for players is standard team leadership practice during fluctuations in competitive sporting form.\nResulting Judgement: (+0.2, +0.1) - Standard Sports Management",
            3: "Verdict: PASS - Awakening into Grace.\nStandard athletic leadership offering public backing to national team players amidst performance cycles.",
            4: "- Team Coaches: PASS (+0.3, +0.2) - Supporting athlete confidence during challenging fixtures.\n- Sports Journalists: PASS (+0.3, +0.2) - Providing factual statistical analysis of match performance."
        }
    },
    "factcheck_ballina-powerball-rumor.json": {
        "claim_u": 0.4, "claim_psi": 0.1,
        "real_u": 0.1, "real_psi": 0.0,
        "posts_update": {
            0: "Residents in coastal Ballina share excitement and local rumors following a record $100M lottery jackpot announcement.\nEvidence: Lottery agency release, local news reporting\n#Community #LocalNews",
            1: "Community chatter circulated rumors that a local syndicate had secured the historic national jackpot.\nStated Judgement: (+0.4, +0.1) - Local Excitement",
            2: "Lottery officials confirmed standard verification protocols, showing harmless community buzz rather than deceptive fraud.\nResulting Judgement: (+0.1, 0.0) - Harmless Community Buzz",
            3: "Verdict: PASS - Awakening into Grace.\nHarmless local community excitement and rumor-swapping following a record national lottery draw.",
            4: "- Local Community: PASS (+0.3, +0.1) - Sharing lighthearted neighborhood speculation.\n- Lottery Corporation: PASS (+0.4, +0.3) - Maintaining strict verification and winner privacy protocols."
        }
    },
    "factcheck_craig-silvey-apology.json": {
        "claim_u": 0.5, "claim_psi": 0.3,
        "real_u": -0.7, "real_psi": -0.8,
        "posts_update": {
            0: "Author Craig Silvey issues a formal public statement following revelations of serious personal misconduct.\nEvidence: Published author statement, festival cancellations\n#Arts #Accountability",
            1: "The author issued an apology expressing regret and acknowledging accountability for past actions.\nStated Judgement: (+0.5, +0.3) - Public Apology",
            2: "Documented misconduct caused genuine harm and led literary institutions to immediately withdraw honors and sever affiliations.\nResulting Judgement: (-0.7, -0.8) - Reputational Reckoning",
            3: "Verdict: FAIL - Fall into Destruction.\nInstitutional accountability and festival cancellations follow documented personal misconduct.",
            4: "- Literary Organizations: PASS (+0.7, +0.6) - Taking prompt action to protect community safety and ethics.\n- Accused Author: FAIL (-0.8, -0.8) - Acknowledged serious misconduct that damaged institutional standing."
        }
    },
    "factcheck_alexander-brothers-prison-privileges.json": {
        "claim_u": 0.5, "claim_psi": 0.3,
        "real_u": 0.2, "real_psi": 0.1,
        "posts_update": {
            0: "Corrections officials review visitation rules following tabloid reporting on inmate contact visits in a high-security facility.\nEvidence: Department of Corrections policy, official audit\n#Justice #Corrections",
            1: "Sensationalized headlines claimed inmates received 'special kissing privileges' in violation of prison rules.\nStated Judgement: (+0.5, +0.3) - Tabloid Sensationalism",
            2: "Corrections audits confirmed standard contact visitation guidelines applied equally under routine correctional protocols without special favoritism.\nResulting Judgement: (+0.2, +0.1) - Standard Corrections Policy",
            3: "Verdict: PASS - Awakening into Grace.\nStandard correctional visitation policies confirmed by internal audit, debunking tabloid sensationalism.",
            4: "- Corrections Department: PASS (+0.4, +0.3) - Enforcing consistent visitation rules across inmate populations.\n- Tabloid Press: FAIL (-0.5, -0.4) - Misrepresenting standard family visitation protocols as illicit privileges."
        }
    },
    "factcheck_netanyahu-faces-coalition-showdown.json": {
        "claim_u": 0.6, "claim_psi": 0.5,
        "real_u": 0.2, "real_psi": 0.2,
        "posts_update": {
            0: "Israeli parliamentary factions navigate intense coalition disputes over military conscription legislation and judicial policy.\nEvidence: Knesset voting records, party statements\n#MiddleEast #Politics",
            1: "Coalition partners assert firm policy demands while seeking to maintain parliamentary majority stability.\nStated Judgement: (+0.6, +0.5) - Parliamentary Negotiations",
            2: "Heated parliamentary bargaining and ultimatum deadlines represent standard coalition mechanics in multi-party parliamentary systems.\nResulting Judgement: (+0.2, +0.2) - Coalition Mechanics",
            3: "Verdict: PASS - Awakening into Grace.\nStandard parliamentary coalition bargaining and legislative compromises in a multi-party system.",
            4: "- Parliamentary Factions: PASS (+0.3, +0.2) - Negotiating competing policy mandates under democratic rules.\n- Coalition Government: PASS (+0.3, +0.2) - Managing complex factional pressures within constitutional boundaries."
        }
    },
    "factcheck_firefighters_eu_budget_cuts_brussels.json": {
        "claim_u": 0.7, "claim_psi": 0.6,
        "real_u": 0.4, "real_psi": 0.3,
        "posts_update": {
            0: "Firefighters from nineteen European nations gather in Brussels to protest proposed civil protection budget reductions.\nEvidence: Union statements, European Commission budget draft\n#Europe #Labor",
            1: "Emergency service unions advocate for robust European civil protection funding to combat climate disasters and wildfires.\nStated Judgement: (+0.7, +0.6) - Emergency Service Advocacy",
            2: "Firefighter unions peacefully mobilized to highlight critical equipment needs, successfully prompting parliamentary budget reviews.\nResulting Judgement: (+0.4, +0.3) - Civic Labor Engagement",
            3: "Verdict: PASS - Awakening into Grace.\nLawful democratic labor advocacy by first responders successfully focusing attention on emergency preparedness.",
            4: "- European Firefighter Unions: PASS (+0.6, +0.5) - Lawfully advocating for life-saving emergency resources.\n- European Parliament: PASS (+0.4, +0.3) - Engaging with civil protection personnel on budget priorities."
        }
    },
    "factcheck_king-charles-commonwealth-slavery.json": {
        "claim_u": 0.6, "claim_psi": 0.5,
        "real_u": 0.4, "real_psi": 0.4,
        "posts_update": {
            0: "King Charles addresses the Commonwealth Heads of Government Meeting, acknowledging the painful legacy of transatlantic slavery.\nEvidence: Official speech transcript, CHOGM communiques\n#Commonwealth #History",
            1: "The monarch expressed deep personal sorrow regarding historical atrocities and urged leaders to build shared future partnerships.\nStated Judgement: (+0.6, +0.5) - Historical Reconciliation",
            2: "Public recognition of historical injustices represents an important diplomatic step in fostering honest Commonwealth dialogue.\nResulting Judgement: (+0.4, +0.4) - Diplomatic Reconciliation",
            3: "Verdict: PASS - Awakening into Grace.\nConstructive diplomatic acknowledgement of historical atrocities aimed at strengthening international reconciliation.",
            4: "- Monarch: PASS (+0.5, +0.4) - Transparently acknowledging historical atrocities at an international forum.\n- Commonwealth Delegates: PASS (+0.5, +0.4) - Engaging in constructive diplomatic dialogue on legacy justice."
        }
    },
    "factcheck_andrew-mountbatten-windsor-summons.json": {
        "claim_u": 0.4, "claim_psi": 0.2,
        "real_u": 0.2, "real_psi": 0.1,
        "posts_update": {
            0: "Legal process servers execute formal judicial summons delivery regarding ongoing civil litigation proceedings.\nEvidence: High Court filings, legal service affidavits\n#Law #Courts",
            1: "Civil litigants utilized standard legal channels to ensure formal service of process on named defendants.\nStated Judgement: (+0.4, +0.2) - Due Process",
            2: "Court filings demonstrate that legal due process operates consistently regardless of royal titles or public status.\nResulting Judgement: (+0.2, +0.1) - Legal Equality",
            3: "Verdict: PASS - Awakening into Grace.\nStandard judicial due process operating impartially without regard to social status or title.",
            4: "- Legal Process Servers: PASS (+0.4, +0.3) - Executing lawful service of process under court rules.\n- Judicial Courts: PASS (+0.5, +0.4) - Upholding equal application of procedural law."
        }
    },
    "factcheck_nithya-raman-votes-against-westside-homeless-encampment-ban.json": {
        "claim_u": 0.6, "claim_psi": 0.5,
        "real_u": 0.3, "real_psi": 0.2,
        "posts_update": {
            0: "Los Angeles City Council debates municipal ordinances on public encampments and permanent supportive housing expansion.\nEvidence: City Council voting records, municipal transcripts\n#LosAngeles #Housing",
            1: "Councilmember Nithya Raman voted against expanding enforcement zones, advocating instead for direct housing services and outreach.\nStated Judgement: (+0.6, +0.5) - Policy Principle",
            2: "Elected council members engaged in standard democratic policy debates over whether criminalization or services best resolve homelessness.\nResulting Judgement: (+0.3, +0.2) - Municipal Policy Debate",
            3: "Verdict: PASS - Awakening into Grace.\nA legitimate policy disagreement within municipal governance regarding housing-first vs enforcement strategies.",
            4: "- Councilmember Raman: PASS (+0.4, +0.3) - Voting consistently on stated policy principles for supportive housing.\n- City Council Colleagues: PASS (+0.3, +0.2) - Debating public space management under municipal authority."
        }
    },
    "factcheck_openai-compute-campuses-midterms.json": {
        "claim_u": 0.6, "claim_psi": 0.5,
        "real_u": 0.3, "real_psi": 0.2,
        "posts_update": {
            0: "Technology infrastructure developers explore regional partnerships for energy-efficient computing centers and power grid agreements.\nEvidence: Regulatory filings, utility applications\n#Tech #Energy",
            1: "Developers emphasize long-term economic investment, job creation, and dedicated renewable energy infrastructure.\nStated Judgement: (+0.6, +0.5) - Infrastructure Investment",
            2: "Tech firms navigate complex public utility reviews and local zoning oversight to ensure grid reliability and water conservation.\nResulting Judgement: (+0.3, +0.2) - Regulatory Review",
            3: "Verdict: PASS - Awakening into Grace.\nLarge-scale technological infrastructure planning proceeding through standard public utility and zoning oversight.",
            4: "- Infrastructure Developers: PASS (+0.4, +0.3) - Submitting engineering plans to public utility commissions.\n- Local Utility Regulators: PASS (+0.5, +0.4) - Protecting regional power grid stability and water resources."
        }
    },
    "factcheck_ai-chatbots-political-advisers-midterms.json": {
        "claim_u": 0.6, "claim_psi": 0.5,
        "real_u": 0.2, "real_psi": 0.1,
        "posts_update": {
            0: "Campaigns and voter outreach organizations test generative AI tools for drafting correspondence and analyzing public policy polling.\nEvidence: Campaign disclosures, tech platform terms\n#AI #Elections",
            1: "Technology advocates promote conversational tools as efficient aids for drafting routine donor communications and volunteer schedules.\nStated Judgement: (+0.6, +0.5) - Campaign Efficiency",
            2: "Campaign strategists utilize tools for routine drafting while maintaining human oversight over core strategy and policy commitments.\nResulting Judgement: (+0.2, +0.1) - Tool Augmentation",
            3: "Verdict: PASS - Awakening into Grace.\nAdoption of productivity software for routine campaign logistics under responsible human editorial oversight.",
            4: "- Campaign Staff: PASS (+0.3, +0.2) - Utilizing productivity tools while retaining human strategy oversight.\n- AI Developers: PASS (+0.3, +0.2) - Implementing safeguards against automated election disinformation."
        }
    },
    "factcheck_debris-from-doomed-learjet-scarred-florida.json": {
        "claim_u": 0.5, "claim_psi": 0.0,
        "real_u": 0.5, "real_psi": 0.0,
        "posts_update": {
            0: "NTSB investigators deploy forensic teams to recover flight recorders and map wreckage following an aviation accident in Florida.\nEvidence: NTSB briefings, FAA preliminary accident reports\n#Aviation #Safety",
            1: "Federal aviation safety investigators published timely, transparent updates detailing search and recovery operations.\nStated Judgement: (+0.5, 0.0) - Investigative Transparency",
            2: "Safety agencies conducted rigorous technical investigations to identify mechanical or environmental factors and prevent future accidents.\nResulting Judgement: (+0.5, 0.0) - Verified Safety Probe",
            3: "Verdict: PASS - Awakening into Grace.\nThorough and transparent aviation accident investigation by federal transportation safety officials.",
            4: "- NTSB Investigators: PASS (+0.7, +0.6) - Conducting thorough forensic technical analysis to protect air safety.\n- First Responders: PASS (+0.7, +0.6) - Swift recovery and site containment operations."
        }
    },
    "factcheck_two-teenage-boys-victims-california-shooting-beach.json": {
        "claim_u": 0.5, "claim_psi": 0.0,
        "real_u": 0.5, "real_psi": 0.0,
        "posts_update": {
            0: "Community members hold beachside vigils as police investigate a tragic shooting involving two local teenagers in Southern California.\nEvidence: Police department press notices, community memorials\n#Community #PublicSafety",
            1: "City leaders and law enforcement provided verified updates while families and neighbors mobilized grief-counseling support.\nStated Judgement: (+0.5, 0.0) - Community Support",
            2: "Local reporting and municipal authorities handled emergency communications with factual accuracy and appropriate sensitivity.\nResulting Judgement: (+0.5, 0.0) - Dignified Public Reporting",
            3: "Verdict: PASS - Awakening into Grace.\nRespectful and transparent community reporting during a tragic local criminal investigation.",
            4: "- Community Support Groups: PASS (+0.7, +0.6) - Mobilizing compassionate grief and family counseling resources.\n- Local Law Enforcement: PASS (+0.5, +0.4) - Diligently pursuing suspects to secure justice."
        }
    },
    "factcheck_beauty-queen-kiara-bowling-returns-to-crash-site.json": {
        "claim_u": 0.6, "claim_psi": 0.5,
        "real_u": 0.5, "real_psi": 0.4,
        "posts_update": {
            0: "Survivor Kiara Bowling returns to the site of a severe automobile accident to advocate for road safety improvements and highway lighting.\nEvidence: Community safety forum, public remarks\n#RoadSafety #Community",
            1: "After enduring major injuries, the survivor dedicated her platform to campaigning for regional road infrastructure upgrades.\nStated Judgement: (+0.6, +0.5) - Personal Advocacy",
            2: "Channeling traumatic recovery into constructive civic advocacy for safer highways represents inspiring personal resilience.\nResulting Judgement: (+0.5, +0.4) - Constructive Resilience",
            3: "Verdict: PASS - Awakening into Grace.\nTransforming personal trauma into constructive civic advocacy for public highway safety improvements.",
            4: "- Kiara Bowling: PASS (+0.7, +0.6) - Using personal recovery to advocate for regional road safety.\n- Transportation Advocates: PASS (+0.5, +0.4) - Supporting infrastructure lighting and barrier upgrades."
        }
    },
    "factcheck_exclusive-woman-allegedly-raped-illegal-alien.json": {
        "claim_u": 0.5, "claim_psi": 0.4,
        "real_u": -0.8, "real_psi": -0.8,
        "posts_update": {
            0: "Law enforcement apprehends a violent offender following a serious criminal sexual assault investigation.\nEvidence: Police arrest logs, grand jury indictment\n#Justice #PublicSafety",
            1: "Prosecutors filed formal criminal indictments, seeking maximum statutory sentencing for violent felony assault.\nStated Judgement: (+0.5, +0.4) - Judicial Accountability",
            2: "Forensic evidence and police reports document a severe violent crime, which the criminal justice system is now prosecuting.\nResulting Judgement: (-0.8, -0.8) - Heinous Criminal Offense",
            3: "Verdict: FAIL - Fall into Destruction.\nLaw enforcement enforces strict legal accountability for severe violent felony assault.",
            4: "- Prosecutors & Police: PASS (+0.7, +0.7) - Diligently investigating and prosecuting violent felonious crime.\n- Perpetrator: FAIL (-0.9, -0.9) - Committed grave violent assault against an innocent victim."
        }
    },
    "factcheck_filipino-police-thomas-markle-cseam.json": {
        "claim_u": 0.5, "claim_psi": 0.4,
        "real_u": -0.9, "real_psi": -0.9,
        "posts_update": {
            0: "International law enforcement authorities execute search warrants in a high-profile child exploitation investigation.\nEvidence: Police evidentiary logs, international arrest warrants\n#Justice #ChildSafety",
            1: "Law enforcement agencies confirmed coordinated cross-border operations targeting illicit digital material.\nStated Judgement: (+0.5, +0.4) - International Enforcement",
            2: "Seized evidence details heinous exploitation material, leading international authorities to initiate formal extradition proceedings.\nResulting Judgement: (-0.9, -0.9) - Criminal Depravity",
            3: "Verdict: FAIL - Fall into Destruction.\nInternational police cooperation acts decisively to dismantle criminal child exploitation networks.",
            4: "- International Police: PASS (+0.8, +0.8) - Coordinated global law enforcement to protect vulnerable victims.\n- Suspect: FAIL (-1.0, -1.0) - Subject of international warrants for illicit exploitation material."
        }
    },
    "factcheck_darline-graham-loses-late-brot.json": {
        "claim_u": 0.6, "claim_psi": 0.4,
        "real_u": 0.4, "real_psi": 0.3,
        "posts_update": {
            0: "Voters decide a competitive legislative primary contest, choosing nominee experience over dynastic family name recognition.\nEvidence: Certified election returns, county board filings\n#Elections #Democracy",
            1: "Candidate campaigned on carrying forward a family legislative legacy and regional community values.\nStated Judgement: (+0.6, +0.4) - Campaign Legacy",
            2: "Primary voters exercised democratic choice based on individual candidate debate performance and policy platform rather than familial lineage.\nResulting Judgement: (+0.4, +0.3) - Democratic Selection",
            3: "Verdict: PASS - Awakening into Grace.\nA standard primary election where voters chose candidate merits over dynastic family name recognition.",
            4: "- Primary Voters: PASS (+0.5, +0.4) - Evaluated candidates on individual merits and platforms.\n- Candidates: PASS (+0.3, +0.2) - Conceded gracefully and respected the democratic outcome."
        }
    },
    "factcheck_gop-set-to-lose-the-house-in-m.json": {
        "claim_u": 0.6, "claim_psi": 0.5,
        "real_u": 0.4, "real_psi": 0.3,
        "posts_update": {
            0: "Non-partisan election forecasters update midterm congressional race ratings across suburban battlegrounds.\nEvidence: Cook Political Report, state polling aggregations\n#Forecasting #Midterms",
            1: "Forecasters released updated seat-projection models based on generic ballot polling and economic indicators.\nStated Judgement: (+0.6, +0.5) - Empirical Forecasting",
            2: "Statistical election forecasting tracks shifts in electorate sentiment, providing transparent modeling ahead of voting day.\nResulting Judgement: (+0.4, +0.3) - Methodological Transparency",
            3: "Verdict: PASS - Awakening into Grace.\nGrounded statistical election forecasting mapping competitive congressional battlegrounds without partisan bias.",
            4: "- Non-Partisan Forecasters: PASS (+0.5, +0.4) - Publishing transparent probabilistic modeling.\n- Campaign Strategists: PASS (+0.3, +0.2) - Utilizing polling data to adjust candidate resource allocations."
        }
    },
    "factcheck_trump-fox-news-tirade-midterms.json": {
        "claim_u": 0.4, "claim_psi": 0.2,
        "real_u": -0.5, "real_psi": -0.6,
        "posts_update": {
            0: "Former President Trump criticizes cable news coverage following midterm election projections.\nEvidence: Broadcast transcripts, social media posts\n#Media #USPol",
            1: "Public statements took aim at news network analysts for reporting unfavorable exit polling and race calls.\nStated Judgement: (+0.4, +0.2) - Political Pushback",
            2: "Public attacks on journalists reporting verified election data undermine civic trust in election journalism.\nResulting Judgement: (-0.5, -0.6) - Press Intimidation",
            3: "Verdict: FAIL - Fall into Destruction.\nPublic attacks on verified news reporting seek to undermine confidence in journalistic election transparency.",
            4: "- Journalistic Reporters: PASS (+0.6, +0.5) - Accurately reporting verified ballot returns.\n- Political Figures: FAIL (-0.6, -0.6) - Attacking journalists for broadcasting empirical election results."
        }
    },
    "factcheck_kansas-postal-worker-mail-theft.json": {
        "claim_u": 0.7, "claim_psi": 0.5,
        "real_u": -0.6, "real_psi": -0.7,
        "posts_update": {
            0: "Federal postal inspectors indict an individual postal employee for intercepting mail ballots and packages.\nEvidence: Federal indictment, USPS Inspector General report\n#USPS #Justice",
            1: "Postal inspectors reaffirmed their commitment to investigating mail theft and safeguarding the security of the mail.\nStated Judgement: (+0.7, +0.5) - Law Enforcement Action",
            2: "Inspectors successfully caught and prosecuted the rogue employee, proving federal safeguards work while holding the individual accountable.\nResulting Judgement: (-0.6, -0.7) - Individual Breach",
            3: "Verdict: FAIL - Fall into Destruction.\nFederal postal inspectors successfully intercepted an individual mail theft scheme, protecting public mail integrity.",
            4: "- USPS Postal Inspectors: PASS (+0.8, +0.7) - Swiftly caught and indicted the individual employee.\n- Indicted Worker: FAIL (-0.8, -0.8) - Violated public trust by stealing mail items."
        }
    },
    "factcheck_foreign-ai-firm-with-alleged-china-ties.json": {
        "claim_u": 0.5, "claim_psi": 0.4,
        "real_u": 0.2, "real_psi": 0.2,
        "posts_update": {
            0: "Federal trade regulators review cross-border technology venture partnerships under national security review guidelines.\nEvidence: CFIUS filings, regulatory disclosures\n#TechPolicy #NationalSecurity",
            1: "Partisan media framed a routine corporate software partnership as an immediate foreign espionage threat.\nStated Judgement: (+0.5, +0.4) - Regulatory Scrutiny",
            2: "Federal agencies routinely review cross-border tech investments through established CFIUS protocols without evidence of compromise.\nResulting Judgement: (+0.2, +0.2) - Regulatory Due Diligence",
            3: "Verdict: PASS - Awakening into Grace.\nStandard national security and trade regulatory reviews operating through established federal oversight mechanisms.",
            4: "- Regulatory Reviewers: PASS (+0.5, +0.4) - Conducting formal national security due diligence.\n- Tabloid Commentators: COND (-0.3, -0.2) - Sensationalizing standard regulatory reviews for clicks."
        }
    },
    "factcheck_exit-poll-reveals-gops-biggest-vulnerability.json": {
        "claim_u": 0.6, "claim_psi": 0.5,
        "real_u": 0.4, "real_psi": 0.3,
        "posts_update": {
            0: "Electoral analysts review certified exit poll demographics to identify shifts among key regional voting blocs.\nEvidence: National Election Pool exit poll, AP VoteCast\n#Data #Midterms",
            1: "Polling analysts published demographic cross-tabs detailing voter motivations on healthcare, the economy, and governance.\nStated Judgement: (+0.6, +0.5) - Demographic Analysis",
            2: "Empirical polling data accurately maps voter priorities, providing transparent data for civic understanding.\nResulting Judgement: (+0.4, +0.3) - Objective Research",
            3: "Verdict: PASS - Awakening into Grace.\nObjective, verified exit poll analysis providing transparent insights into voter motivations.",
            4: "- Exit Poll Researchers: PASS (+0.6, +0.5) - Conducting empirical, transparent voter surveys.\n- Electorate: PASS (+0.5, +0.4) - Participating in democratic decision-making."
        }
    },
    "factcheck_exit-poll-iran-war-crucial-factor.json": {
        "claim_u": 0.6, "claim_psi": 0.5,
        "real_u": 0.4, "real_psi": 0.3,
        "posts_update": {
            0: "Exit polling surveys reveal that voter sentiment on foreign policy and military conflict influenced contested races.\nEvidence: Exit poll cross-tabs, candidate foreign policy platforms\n#ForeignPolicy #Midterms",
            1: "Survey data highlights that voters prioritized diplomatic de-escalation and regional stability when casting ballots.\nStated Judgement: (+0.6, +0.5) - Voter Survey",
            2: "Voters used the ballot box to voice preferences on international engagement and conflict prevention, reflecting democratic input.\nResulting Judgement: (+0.4, +0.3) - Civic Voice",
            3: "Verdict: PASS - Awakening into Grace.\nVoters democratically expressing clear preferences for international stability and diplomatic accountability.",
            4: "- Voters: PASS (+0.6, +0.5) - Guiding national foreign policy through democratic ballots.\n- Polling Organizations: PASS (+0.5, +0.4) - Accurately documenting voter priorities on foreign affairs."
        }
    },
    "factcheck_iran-war-hawks-midterm-reality-check.json": {
        "claim_u": 0.5, "claim_psi": 0.4,
        "real_u": 0.3, "real_psi": 0.2,
        "posts_update": {
            0: "Foreign policy commentators analyze election returns as voters reject interventionist platforms in key congressional districts.\nEvidence: Election tallies, foreign policy think-tank reports\n#ForeignPolicy #Elections",
            1: "Political analysis argues that voters punished candidates promoting aggressive military entanglements in the Middle East.\nStated Judgement: (+0.5, +0.4) - Policy Analysis",
            2: "Election outcomes demonstrate that public skepticism of open-ended overseas conflicts acts as a constitutional check on foreign policy.\nResulting Judgement: (+0.3, +0.2) - Democratic Constraint",
            3: "Verdict: PASS - Awakening into Grace.\nVoters exercising democratic oversight to constrain aggressive overseas military commitments.",
            4: "- Electorate: PASS (+0.6, +0.5) - Demanding accountability and restraint in foreign policy.\n- Policy Analysts: PASS (+0.4, +0.3) - Transparently analyzing voter opposition to foreign entanglements."
        }
    },
    "factcheck_pod-save-america-hosts-call-democratic-party-midterm-wins-end-trump-era.json": {
        "claim_u": 0.5, "claim_psi": 0.3,
        "real_u": 0.2, "real_psi": 0.1,
        "posts_update": {
            0: "Political podcast commentators debate long-term party alignment following congressional midterm gains.\nEvidence: Audio broadcast transcript\n#Media #Politics",
            1: "Commentators declared midterm seat flips signify a permanent political realignment in national governance.\nStated Judgement: (+0.5, +0.3) - Partisan Commentary",
            2: "While reflecting progressive enthusiasm, declaring the permanent end of a political era is conventional partisan podcast punditry.\nResulting Judgement: (+0.2, +0.1) - Pundit Enthusiasm",
            3: "Verdict: PASS - Awakening into Grace.\nStandard partisan political podcasting analyzing electoral outcomes with predictable partisan optimism.",
            4: "- Podcast Commentators: PASS (+0.3, +0.2) - Expressing partisan analysis and enthusiasm for their party's gains.\n- Swing Voters: PASS (+0.4, +0.3) - Deciding competitive races through nuanced ticket-splitting."
        }
    },
    "factcheck_trump-iran-conflict-soft-war-midterms-2026.json": {
        "claim_u": 0.5, "claim_psi": 0.4,
        "real_u": 0.2, "real_psi": 0.1,
        "posts_update": {
            0: "Former President Trump delivers foreign policy remarks characterizing ongoing regional confrontations as economic and diplomatic 'soft war.'\nEvidence: Speech transcript, foreign policy briefing\n#Diplomacy #USPol",
            1: "Political speeches framed Middle Eastern deterrence as focused primarily on sanctions, economic pressure, and trade leverage.\nStated Judgement: (+0.5, +0.4) - Diplomatic Framing",
            2: "While framed as non-kinetic, economic sanctions and drone skirmishes carry real geopolitical friction requiring nuanced strategic analysis.\nResulting Judgement: (+0.2, +0.1) - Geopolitical Realities",
            3: "Verdict: PASS - Awakening into Grace.\nPolitical discourse exploring economic deterrence and sanctions strategy in international relations.",
            4: "- Diplomatic Analysts: PASS (+0.4, +0.3) - Evaluating the real-world trade-offs of economic sanctions.\n- Campaign Speakers: PASS (+0.2, +0.1) - Outlining foreign policy strategies to voters."
        }
    },
    "factcheck_mamdani-a-no-show-at-funeral.json": {
        "claim_u": 0.4, "claim_psi": 0.2,
        "real_u": 0.1, "real_psi": 0.0,
        "posts_update": {
            0: "Local New York media covers municipal attendance at memorial services for unhoused community members.\nEvidence: Public memorial logs, municipal schedules\n#NYC #Community",
            1: "Tabloid headlines targeted state lawmaker Zohran Mamdani for non-attendance at a specific community memorial service.\nStated Judgement: (+0.4, +0.2) - Attendance Criticism",
            2: "Legislative records show active policy sponsorship on municipal housing and homeless shelter funding, refuting tabloid claims of indifference.\nResulting Judgement: (+0.1, 0.0) - Legislative Record",
            3: "Verdict: PASS - Awakening into Grace.\nA legislative track record of supporting unhoused funding, contrasting with sensationalized tabloid attendance attacks.",
            4: "- Lawmaker Office: PASS (+0.3, +0.2) - Actively authoring and funding municipal housing legislation.\n- Tabloid Press: FAIL (-0.5, -0.4) - Sensationalizing memorial attendance to manufacture personal political attacks."
        }
    },
    "factcheck_republicans_meltdown_blue_wave_2026.json": {
        "claim_u": 0.5, "claim_psi": 0.3,
        "real_u": 0.2, "real_psi": 0.1,
        "posts_update": {
            0: "Commentary analyzes congressional midterm shifts as Democrats gain key House seats in swing districts.\nEvidence: Certified election returns, district demographic data\n#USPol #Midterms",
            1: "Partisan media framed midterm seat pickups as a total political collapse of the opposition party.\nStated Judgement: (+0.5, +0.3) - Partisan Narrative",
            2: "Certified election tallies demonstrate competitive suburban swings and tight margins, reflecting normal midterm electoral ebb and flow.\nResulting Judgement: (+0.2, +0.1) - Midterm Reality",
            3: "Verdict: PASS - Awakening into Grace.\nStandard partisan post-election commentary celebrating swing district gains within regular democratic cycles.",
            4: "- Winning Candidates: PASS (+0.4, +0.3) - Building competitive coalitions across suburban districts.\n- Partisan Pundits: PASS (+0.2, +0.1) - Celebrating election night victories with predictable political spin."
        }
    },
    "factcheck_saudi-arabia-asian-cup-postponed.json": {
        "claim_u": 0.6, "claim_psi": 0.4,
        "real_u": 0.4, "real_psi": 0.2,
        "posts_update": {
            0: "Asian Football Confederation confirms the rescheduling of the 2027 Asian Cup in Saudi Arabia to ensure regional safety.\nEvidence: AFC official announcement, security risk briefings\n#Soccer #AsianCup #Sports",
            1: "The AFC announced that the continental tournament would proceed smoothly as a premier international sporting event.\nStated Judgement: (+0.6, +0.4) - Sporting Ambition",
            2: "Regional security assessments and flight disruptions prompted sports governing bodies to postpone the tournament, prioritizing athlete and spectator safety.\nResulting Judgement: (+0.4, +0.2) - Prudent Safety Oversight",
            3: "Verdict: PASS - Awakening into Grace.\nPrudent risk management by international football administrators postponing a tournament to guarantee team and visitor security.",
            4: "- AFC Administration: PASS (+0.5, +0.3) - Prioritizing player and spectator safety amid regional security challenges.\n- Participating Federations: PASS (+0.4, +0.2) - Cooperating on calendar adjustments to preserve competition integrity."
        }
    },
    "factcheck_van-jones-jonestown-midterms.json": {
        "claim_u": 0.4, "claim_psi": 0.3,
        "real_u": -0.3, "real_psi": -0.2,
        "posts_update": {
            0: "Cable news broadcast analyzes post-midterm political strategies and campaign postmortems.\nEvidence: CNN broadcast transcript, election commentary logs\n#MediaWatch #USPol",
            1: "Network commentators claimed their panel discussion provided hard-hitting, necessary political analysis of midterm election losses.\nStated Judgement: (+0.4, +0.3) - Political Commentary",
            2: "Comparing political party campaign miscalculations to a historic mass suicide (Jonestown) is sensationalist hyperbole that debases civil political discourse.\nResulting Judgement: (-0.3, -0.2) - Sensationalist Hyperbole",
            3: "Verdict: FAIL - Fall into Destruction.\nCable commentary deploying extreme historical shock comparisons to dramatize standard election losses.",
            4: "- Cable Commentator: FAIL (-0.3, -0.2) - Resorting to crude historical hyperbole for broadcast attention.\n- Election Analysts: PASS (+0.3, +0.2) - Grounding midterm voting shifts in precinct data and voter economics."
        }
    }
}

def execute_reaudit():
    print("================================================================")
    print("STARTING FULL RE-AUDIT OF FLAWED STORIES IN stories/live/")
    print(f"Targeting: {len(REAUDIT_SPECS)} identified broken stories")
    print("================================================================\n")

    re_audited_count = 0
    missing_count = 0

    for fn, spec in REAUDIT_SPECS.items():
        fp = os.path.join(LIVE_DIR, fn)
        if not os.path.exists(fp):
            print(f"[MISSING] File not found in live: {fn}")
            missing_count += 1
            continue

        with open(fp, "r", encoding="utf-8") as f:
            data = json.load(f)

        story = data[0] if isinstance(data, list) else data

        # Apply coordinates
        story["claim_u"] = spec["claim_u"]
        story["claim_psi"] = spec["claim_psi"]
        story["real_u"] = spec["real_u"]
        story["real_psi"] = spec["real_psi"]

        # Remove stale force tensors to prevent old calculations
        if "stated_forces" in story:
            del story["stated_forces"]
        if "actual_forces" in story:
            del story["actual_forces"]

        # Apply post updates
        posts = story.get("posts", [])
        if "posts_update" in spec and isinstance(spec["posts_update"], dict):
            for p_idx, p_text in spec["posts_update"].items():
                if p_idx < len(posts):
                    posts[p_idx] = p_text

        story["posts"] = posts

        # Enforce deterministic trajectory invariant
        story = enforce_deterministic_trajectory(story)
        path_name = get_path_name(story["claim_u"], story["claim_psi"], story["real_u"], story["real_psi"])
        story["path_name"] = path_name

        # Save back to file
        out_data = [story] if isinstance(data, list) else story
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(out_data, f, indent=2, ensure_ascii=False)

        print(f"[OK] Re-audited: {fn} -> Path: {path_name}")
        re_audited_count += 1

    print(f"\nCompleted re-auditing {re_audited_count} stories in stories/live/.")
    if missing_count > 0:
        print(f"Warning: {missing_count} files were not found.")

if __name__ == "__main__":
    execute_reaudit()
