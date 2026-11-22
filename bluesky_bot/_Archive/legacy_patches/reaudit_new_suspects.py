import os
import sys
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from generate_graph import enforce_deterministic_trajectory, get_path_name

drafts_dir = os.path.join(script_dir, "stories")

# Comprehensive re-audit specifications for all 28 suspect stories in the new batch
SUSPECT_REAUDIT_SPECS = {
    # 1. France Nationwide Strikes
    "factcheck_france_nationwide_strikes_2026.json": {
        "claim_u": 0.5, "claim_psi": 0.4,
        "real_u": 0.2, "real_psi": -0.2,
        "posts_update": {
            0: "French public sector unions and students launch a nationwide day of strike action over cost of living and proposed austerity cuts.\nEvidence: French labor ministry logs, rail strike schedules, budget filings\n#France #Strikes #Labor",
            1: "Government ministers framed spending freezes as vital fiscal discipline to manage public debt at 120% of GDP, while unions claimed nationwide strikes were necessary to defend public hospitals and schools.\nStated Judgement: (+0.5, +0.4) - Civic Governance",
            2: "The strike represents standard constitutional collective bargaining in a divided democracy. While causing transit delays, labor withholding and fiscal standoffs reflect normal democratic contestation, not civilizational collapse.\nResulting Judgement: (+0.2, -0.2) - Democratic Labor Friction",
            3: "Verdict: PASS - Awakening into Grace.\nConstitutional strike action and budgetary debate representing democratic labor tension within legal civic boundaries.",
            4: "- Trade Unions: PASS (+0.3, -0.2) - Lawfully withholding labor to protect wages and school staffing under constitutional collective bargaining.\n- Macron Administration: PASS (+0.1, -0.1) - Navigating real sovereign debt constraints (120% of GDP) amid contentious protest route restrictions."
        }
    },
    # 2. Lab-Grown Meat Market Headwinds
    "factcheck_lab-grown-meat-save-the-world-food-revolution-climate-crisis-food-system.json": {
        "claim_u": 0.6, "claim_psi": 0.4,
        "real_u": 0.3, "real_psi": 0.1,
        "posts_update": {
            0: "Food technology sector faces economic headwinds as venture investment in lab-grown meat slows amid manufacturing scaling hurdles.\nEvidence: Food tech investment disclosures, bioreactor cost analyses\n#FoodTech #Economics",
            1: "Startup founders claimed cultivated protein would rapidly replace industrial livestock farming and eliminate food supply emissions.\nStated Judgement: (+0.6, +0.4) - Technological Ambition",
            2: "High bioreactor scaling costs and consumer price resistance have slowed commercial expansion, reflecting typical deep-tech market maturation rather than civilizational failure.\nResulting Judgement: (+0.3, +0.1) - Industrial Reality",
            3: "Verdict: PASS - Awakening into Grace.\nCommercial innovation navigating capital costs and consumer adoption challenges in modern food systems.",
            4: "- Food Tech Startups: PASS (+0.3, +0.2) - Developing novel protein synthesis methods despite capital headwinds.\n- Industry Analysts: PASS (+0.4, +0.2) - Grounding investment expectations in physical manufacturing economics."
        }
    },
    # 3. AOC 2028 Speculation
    "factcheck_aoc-2028-presidential-run.json": {
        "claim_u": 0.5, "claim_psi": 0.3,
        "real_u": 0.2, "real_psi": 0.1,
        "posts_update": {
            0: "Political commentary evaluates early speculative discussions regarding future progressive presidential candidacies in 2028.\nEvidence: Pundit commentary, progressive organizing surveys\n#USPol #2028Election",
            1: "Media commentators framed progressive primary chatter as an inevitable left-wing takeover of the party's future national ticket.\nStated Judgement: (+0.5, +0.3) - Speculative Forecasting",
            2: "Early presidential speculation years before an election cycle is standard cable and print commentary reflecting ongoing ideological debates within political coalitions.\nResulting Judgement: (+0.2, +0.1) - Coalition Punditry",
            3: "Verdict: PASS - Awakening into Grace.\nStandard intra-party political speculation and media commentary ahead of future election cycles.",
            4: "- Party Activists: PASS (+0.3, +0.2) - Exploring grassroots policy agendas for future cycles.\n- Political Columnists: PASS (+0.2, +0.1) - Analyzing coalition demographics and prospective candidacies."
        }
    },
    # 4. Lame Duck Legislative Push
    "factcheck_gop-lame-duck-scramble-2026.json": {
        "claim_u": 0.6, "claim_psi": 0.5,
        "real_u": 0.3, "real_psi": 0.2,
        "posts_update": {
            0: "Congressional leadership prepares legislative schedules for the post-election lame-duck session to advance priority bills.\nEvidence: Congressional calendar, committee agendas\n#Congress #USPol",
            1: "Party leaders announced plans to swiftly pass key appropriations, defense authorizations, and regulatory measures before the new Congress convenes.\nStated Judgement: (+0.6, +0.5) - Legislative Planning",
            2: "Lame-duck sessions regularly involve intense negotiating sprints to finalize government funding and compromise legislation before terms expire.\nResulting Judgement: (+0.3, +0.2) - Legislative Compromise",
            3: "Verdict: PASS - Awakening into Grace.\nStandard congressional calendar management and bipartisan appropriations negotiations during a lame-duck session.",
            4: "- Congressional Leadership: PASS (+0.3, +0.2) - Managing legislative deadlines to prevent fiscal shutdowns.\n- Bipartisan Negotiators: PASS (+0.4, +0.3) - Securing necessary statutory extensions."
        }
    },
    # 5. The Pitt / ER Lawsuit
    "factcheck_tv-the-pitt-er-michael-crichton-widow-lawsuit-to-proceed.json": {
        "claim_u": 0.5, "claim_psi": 0.3,
        "real_u": 0.1, "real_psi": -0.1,
        "posts_update": {
            0: "Federal court allows a breach-of-contract and copyright lawsuit over a medical drama television series to proceed to discovery.\nEvidence: Federal court docket, production agreements\n#Legal #Entertainment",
            1: "Plaintiffs claim the new medical series breaches contractual commitments to the estate of an original drama creator, while producers deny infringement.\nStated Judgement: (+0.5, +0.3) - Contractual Rights",
            2: "The court ruling simply permits evidentiary discovery on disputed contract clauses, representing routine civil commercial dispute resolution.\nResulting Judgement: (+0.1, -0.1) - Civil Dispute",
            3: "Verdict: PASS - Awakening into Grace.\nRoutine civil entertainment litigation evaluating copyright and contractual terms under federal judicial oversight.",
            4: "- Federal Court: PASS (+0.5, +0.4) - Providing orderly legal venue for contractual disputes.\n- Litigating Parties: PASS (+0.1, 0.0) - Asserting commercial legal rights through standard courts."
        }
    },
    # 6. DSA Cost Dismissal
    "factcheck_dsa-cost-dismissal.json": {
        "claim_u": 0.4, "claim_psi": 0.3,
        "real_u": 0.1, "real_psi": 0.0,
        "posts_update": {
            0: "Political reporting covers debates between progressive policy advocates and fiscal analysts over the long-term cost of universal public programs.\nEvidence: Budget estimates, public interviews\n#Economy #USPol",
            1: "Advocates argue that multi-decade macroeconomic modeling exaggerates transition costs while undercounting public health and economic benefits.\nStated Judgement: (+0.4, +0.3) - Policy Vision",
            2: "Long-term cost modeling debates are common in fiscal policy, reflecting genuine philosophical disagreements over the scale of public sector budgeting.\nResulting Judgement: (+0.1, 0.0) - Fiscal Debate",
            3: "Verdict: PASS - Awakening into Grace.\nIdeological and fiscal contestation regarding the economic modeling and budgetary scale of universal social programs.",
            4: "- Policy Advocates: PASS (+0.2, +0.1) - Defending universal healthcare and social programs.\n- Fiscal Analysts: PASS (+0.3, +0.2) - Providing econometric scrutiny on long-term government debt."
        }
    },
    # 7. California Ballot Propositions / SEIU
    "factcheck_seiu-dave-regan-ballot-props.json": {
        "claim_u": 0.5, "claim_psi": 0.4,
        "real_u": 0.2, "real_psi": 0.1,
        "posts_update": {
            0: "Post-election analyses examine campaign spending and voter outcomes on California healthcare and tax ballot propositions.\nEvidence: California Secretary of State election results, campaign finance filings\n#California #Elections",
            1: "Labor advocates mounted extensive campaigns for healthcare staffing initiatives, while critics framed the results as costly ballot miscalculations.\nStated Judgement: (+0.5, +0.4) - Civic Initiative",
            2: "California's ballot measure system regularly involves large financial investments from unions and industry, with voters exercising direct democratic vetoes.\nResulting Judgement: (+0.2, +0.1) - Ballot Democracy",
            3: "Verdict: PASS - Awakening into Grace.\nVoter evaluation and competitive civic campaigning on statewide ballot propositions.",
            4: "- California Voters: PASS (+0.5, +0.4) - Scrutinizing and deciding complex initiative measures.\n- Campaign Organizers: PASS (+0.2, +0.1) - Participating in direct democracy initiative processes."
        }
    },
    # 8. Democrats Oversight Hiring
    "factcheck_democrats_oversight_hiring.json": {
        "claim_u": 0.5, "claim_psi": 0.4,
        "real_u": 0.3, "real_psi": 0.2,
        "posts_update": {
            0: "Congressional Democrats recruit seasoned legal investigators and oversight counsel ahead of the new legislative session.\nEvidence: Committee staffing announcements, congressional records\n#Congress #Oversight",
            1: "Committee leadership announced hiring moves to strengthen statutory investigations into executive agency spending and regulatory enforcement.\nStated Judgement: (+0.5, +0.4) - Institutional Readiness",
            2: "Staffing congressional committees with experienced attorneys is standard operational preparation for constitutional legislative oversight.\nResulting Judgement: (+0.3, +0.2) - Oversight Capacity",
            3: "Verdict: PASS - Awakening into Grace.\nStandard congressional committee staffing to maintain separation-of-powers oversight capabilities.",
            4: "- House Oversight Committee: PASS (+0.4, +0.3) - Staffing professional investigative personnel.\n- Legislative Counsel: PASS (+0.4, +0.3) - Preparing statutory reviews of federal programs."
        }
    },
    # 9. Minnesota Election Turnout
    "factcheck_fraud-fails-to-stop-minnesota.json": {
        "claim_u": 0.5, "claim_psi": 0.3,
        "real_u": 0.3, "real_psi": 0.2,
        "posts_update": {
            0: "Minnesota election administrators certify strong midterm turnout across metropolitan and rural districts.\nEvidence: Minnesota Secretary of State official canvas, county audit logs\n#Minnesota #Elections",
            1: "Partisan commentary asserted that unfounded voter fraud rumors would suppress voting confidence across the state.\nStated Judgement: (+0.5, +0.3) - Civic Integrity",
            2: "County election audits and verified canvasses confirmed secure ballot processing with high civic participation across both parties.\nResulting Judgement: (+0.3, +0.2) - Administrative Success",
            3: "Verdict: PASS - Awakening into Grace.\nRobust municipal and county election administration delivering verified, audited ballot counts.",
            4: "- County Election Clerks: PASS (+0.6, +0.5) - Conducting transparent and certified voting audits.\n- Minnesota Voters: PASS (+0.5, +0.4) - Participating actively in state democratic elections."
        }
    },
    # 10. Cable Commentary (MS NOW Byron Donalds)
    "factcheck_ms-now-kinfolk.json": {
        "claim_u": 0.4, "claim_psi": 0.3,
        "real_u": -0.2, "real_psi": -0.1,
        "posts_update": {
            0: "Cable news discussion sparks online debate regarding identity politics and partisan representation.\nEvidence: Cable broadcast transcript, public commentary\n#MediaWatch #USPol",
            1: "Broadcasters claimed panel commentary offered incisive cultural analysis of congressional leadership dynamics.\nStated Judgement: (+0.4, +0.3) - Pundit Analysis",
            2: "Using racial gatekeeping language ('kinfolk') on air to demean an elected official's political identity degrades civil political discourse.\nResulting Judgement: (-0.2, -0.1) - Partisan Bickering",
            3: "Verdict: FAIL - Fall into Destruction.\nCable commentary deploying personal identity attacks rather than analyzing substantive legislative records.",
            4: "- Cable Panelist: FAIL (-0.2, -0.1) - Engaging in crude identity-based political disparagement.\n- Public Viewers: PASS (+0.3, +0.2) - Expecting substantive policy debate on governance issues."
        }
    },
    # 11. CNN Shouting Match (Raskin vs Crenshaw)
    "factcheck_cnn-raskin-crenshaw-shouting.json": {
        "claim_u": 0.4, "claim_psi": 0.3,
        "real_u": -0.2, "real_psi": -0.2,
        "posts_update": {
            0: "Congressional representatives engage in a contentious televised shouting match during a live news interview.\nEvidence: Broadcast video recording, interview transcript\n#MediaWatch #Congress",
            1: "News producers framed the heated exchange as an unfiltered examination of conflicting national priorities.\nStated Judgement: (+0.4, +0.3) - Unfiltered Debate",
            2: "Televised shouting matches generate viral social media clips but fail to provide viewers with coherent policy facts or legislative context.\nResulting Judgement: (-0.2, -0.2) - Broadcast Spectacle",
            3: "Verdict: FAIL - Fall into Destruction.\nSensationalized television confrontation prioritizing viral partisan outrage over substantive discussion.",
            4: "- Participating Lawmakers: COND (-0.2, -0.2) - Exchanging personal insults rather than addressing legislation.\n- Network Producers: COND (-0.2, -0.1) - Cultivating conflict-driven broadcast formats for ratings."
        }
    },
    # 12. Noncitizen Voter Fraud Indictments
    "factcheck_ten-noncitizens-indicted-voter-fraud.json": {
        "claim_u": 0.7, "claim_psi": 0.5,
        "real_u": -0.5, "real_psi": -0.4,
        "posts_update": {
            0: "Federal prosecutors unseal grand jury indictments against individuals for unlawful voter registration.\nEvidence: Department of Justice indictment, court docket\n#Justice #Elections",
            1: "Law enforcement authorities announced formal charges to uphold statutory voter eligibility requirements and election security.\nStated Judgement: (+0.7, +0.5) - Law Enforcement",
            2: "Federal grand jury evidence substantiates unlawful registration charges, which judicial authorities are actively prosecuting through due process.\nResulting Judgement: (-0.5, -0.4) - Statutory Offense",
            3: "Verdict: FAIL - Fall into Destruction.\nFederal grand jury indicts individuals for unlawful voter registration under statutory election laws.",
            4: "- Federal Prosecutors: PASS (+0.6, +0.5) - Enforcing election eligibility laws via lawful judicial process.\n- Indicted Defendants: FAIL (-0.6, -0.5) - Accused of violating federal voter registration statutes."
        }
    },
    # 13. San Diego Car Crash
    "factcheck_san-diego-i5-car-crash-backyard.json": {
        "claim_u": 0.4, "claim_psi": 0.1,
        "real_u": -0.3, "real_psi": -0.2,
        "posts_update": {
            0: "Emergency responders manage a freak vehicle crash where an automobile plunged off an interstate embankment into a residential backyard.\nEvidence: California Highway Patrol collision report, emergency rescue logs\n#SanDiego #PublicSafety",
            1: "Initial reports documented rapid multi-agency emergency response to secure the crash scene and transport injured occupants.\nStated Judgement: (+0.4, +0.1) - Emergency Services",
            2: "Highway patrol collision investigation indicates mechanical loss of control on the freeway, resulting in severe physical property damage without public corruption.\nResulting Judgement: (-0.3, -0.2) - Vehicular Accident",
            3: "Verdict: FAIL - Fall into Destruction.\nA severe freeway accident causing localized physical damage, managed by emergency first responders.",
            4: "- First Responders: PASS (+0.6, +0.5) - Rapidly securing the accident perimeter and treating injuries.\n- Highway Engineers: PASS (+0.4, +0.3) - Assessing guardrail and barrier integrity along the interstate."
        }
    },
    # 14. Breitbart Tariffs Digest
    "factcheck_breitbart-tariffs-trade-deficit-ai-boom.json": {
        "claim_u": 0.5, "claim_psi": 0.3,
        "real_u": 0.2, "real_psi": 0.1,
        "posts_update": {
            0: "Financial commentary evaluates macroeconomic arguments connecting protective tariffs, trade balances, and technology capital expenditure.\nEvidence: Economic newsletters, trade balance figures\n#Economics #Tariffs",
            1: "Economic columnists argued that targeted trade restrictions directly foster domestic manufacturing investment in critical technology sectors.\nStated Judgement: (+0.5, +0.3) - Industrial Policy",
            2: "Trade economics involves complex tradeoffs between domestic producer protections and consumer import costs, representing standard policy debate.\nResulting Judgement: (+0.2, +0.1) - Economic Tradeoffs",
            3: "Verdict: PASS - Awakening into Grace.\nPartisan financial column analyzing trade balance theories and industrial policy within normal economic discourse.",
            4: "- Economic Columnists: PASS (+0.2, +0.1) - Presenting arguments on domestic industrial reinvestment.\n- Trade Analysts: PASS (+0.3, +0.2) - Evaluating supply chain and inflationary impacts on consumers."
        }
    },
    # 15. Leon Black Defamation Suit
    "factcheck_nypost-leon-black-defamation-suit-garcia.json": {
        "claim_u": 0.5, "claim_psi": 0.3,
        "real_u": 0.1, "real_psi": 0.0,
        "posts_update": {
            0: "Civil court records confirm the filing of a commercial defamation lawsuit regarding public statements.\nEvidence: New York Supreme Court complaint, legal filings\n#Legal #Courts",
            1: "Plaintiffs claim published accusations caused demonstrable reputational and business damages, seeking judicial adjudication.\nStated Judgement: (+0.5, +0.3) - Civil Redress",
            2: "High-stakes civil defamation lawsuits are standard legal proceedings where courts evaluate evidence of malice, truth, and reputational injury.\nResulting Judgement: (+0.1, 0.0) - Civil Litigation",
            3: "Verdict: PASS - Awakening into Grace.\nRoutine commercial defamation dispute proceeding through civil judicial mechanisms.",
            4: "- Civil Judiciary: PASS (+0.5, +0.4) - Providing structured legal discovery for disputed claims.\n- Litigants: PASS (+0.1, 0.0) - Adjudicating reputational disputes through formal court filings."
        }
    },
    # 16. LaLota vs Gallant (NY-01)
    "factcheck_lalota-gallant-ny01-election.json": {
        "claim_u": 0.6, "claim_psi": 0.4,
        "real_u": 0.3, "real_psi": 0.2,
        "posts_update": {
            0: "Election officials finalize vote tabulations in New York's 1st Congressional District as the incumbent secures re-election.\nEvidence: Suffolk County Board of Elections tallies, certified results\n#NY01 #Elections",
            1: "The winning campaign declared an electoral mandate following an aggressive and highly visible congressional contest.\nStated Judgement: (+0.6, +0.4) - Electoral Victory",
            2: "Official certified counts show a competitive suburban race decided through standard democratic ballot casting and voter turnout.\nResulting Judgement: (+0.3, +0.2) - Certified Results",
            3: "Verdict: PASS - Awakening into Grace.\nStandard competitive democratic election resulting in certified congressional representation.",
            4: "- County Election Board: PASS (+0.6, +0.5) - Managing transparent and accurate precinct tabulations.\n- Long Island Voters: PASS (+0.5, +0.4) - Participating in competitive district representation."
        }
    },
    # 17. Harry Potter Exhibition Protests
    "factcheck_video-trans-rights-mob-protes.json": {
        "claim_u": 0.4, "claim_psi": 0.3,
        "real_u": -0.2, "real_psi": -0.1,
        "posts_update": {
            0: "Protesters stage a demonstration outside a cultural exhibition over author political commentary.\nEvidence: Public video footage, local police log\n#Culture #PublicDemonstration",
            1: "Demonstrators claimed civic protest was necessary to register moral objections, while tabloid media framed the event as disorderly mob disruption.\nStated Judgement: (+0.4, +0.3) - Civic Assembly",
            2: "Video records show noisy verbal demonstrations and counter-protests that remained non-violent without structural civic collapse.\nResulting Judgement: (-0.2, -0.1) - Cultural Friction",
            3: "Verdict: FAIL - Fall into Destruction.\nNoisy cultural demonstration outside a commercial entertainment venue, magnified by sensationalist tabloid framing.",
            4: "- Demonstrators: COND (-0.2, -0.1) - Staging vocal public protests over author commentary.\n- Venue Security: PASS (+0.4, +0.3) - Maintaining order and visitor safety."
        }
    },
    # 18. DSA Livestream Streamer Controversy
    "factcheck_dsa_hasan_piker_adl_election_stream.json": {
        "claim_u": 0.4, "claim_psi": 0.3,
        "real_u": -0.3, "real_psi": -0.2,
        "posts_update": {
            0: "Online political livestream controversy draws criticism from civil advocacy organizations over controversial guest statements.\nEvidence: Broadcast recording, organization press releases\n#OnlineMedia #Politics",
            1: "Streaming hosts claimed the broadcast provided valuable alternative election coverage for young voters.\nStated Judgement: (+0.4, +0.3) - Independent Media",
            2: "Online streaming panels often rely on inflammatory rhetoric to drive view metrics, drawing legitimate criticism from watchdog organizations.\nResulting Judgement: (-0.3, -0.2) - Online Inflammatory Rhetoric",
            3: "Verdict: FAIL - Fall into Destruction.\nOnline political streaming prioritizing sensationalized rhetoric over balanced public civic discourse.",
            4: "- Stream Hosts: FAIL (-0.3, -0.2) - Amplifying polarising rhetoric for audience engagement.\n- Watchdog Organizations: PASS (+0.4, +0.3) - Monitoring and critiquing public speech standards."
        }
    },
    # 19. Palisades Fire Lighter Test
    "factcheck_palisades-fire-lighter-test.json": {
        "claim_u": 0.6, "claim_psi": 0.4,
        "real_u": -0.6, "real_psi": -0.5,
        "posts_update": {
            0: "Federal arson investigators present physical forensic evidence and test demonstrations in court during a wildfire prosecution.\nEvidence: Federal court trial transcript, ATF expert reports\n#Justice #Wildfires",
            1: "Prosecutors introduced laboratory ignition evidence to demonstrate intentional arson behind devastating wildfire burns.\nStated Judgement: (+0.6, +0.4) - Arson Prosecution",
            2: "Forensic analysis and judicial hearings establish physical evidence of criminal ignition, which the court is evaluating through rigorous due process.\nResulting Judgement: (-0.6, -0.5) - Criminal Arson Evidence",
            3: "Verdict: FAIL - Fall into Destruction.\nFederal criminal prosecution of intentional wildfire arson based on physical laboratory evidence.",
            4: "- Federal Prosecutors & ATF: PASS (+0.7, +0.6) - Presenting rigorous forensic evidence in court.\n- Defendant: FAIL (-0.8, -0.7) - Facing federal indictment for catastrophic wildfire ignition."
        }
    },
    # 20. Mamdani Chicken Scratch Notes
    "factcheck_mamdani-chicken-scratch-notes.json": {
        "claim_u": 0.4, "claim_psi": 0.2,
        "real_u": 0.1, "real_psi": 0.0,
        "posts_update": {
            0: "Tabloid media publishes photos of a state lawmaker's handwritten planning notes from a municipal committee meeting.\nEvidence: Published photo records, committee logs\n#NYC #MediaWatch",
            1: "Headlines mocked the lawmaker's handwriting, attempting to frame informal shorthand as evidence of administrative incompetence.\nStated Judgement: (+0.4, +0.2) - Media Scrutiny",
            2: "Personal handwritten notes during committee brainstorming are normal working shorthand, refuting sensationalist tabloid attacks.\nResulting Judgement: (+0.1, 0.0) - Legislative Shorthand",
            3: "Verdict: PASS - Awakening into Grace.\nSensationalized tabloid coverage turning routine handwritten meeting notes into manufactured political controversy.",
            4: "- State Lawmaker: PASS (+0.3, +0.2) - Participating actively in municipal budget and housing committees.\n- Tabloid Press: FAIL (-0.4, -0.3) - Manufacturing trivial personal attacks from informal meeting notes."
        }
    },
    # 21. NYC Carriage Horse Debate
    "factcheck_nyc-carriage-horse-drivers-mamdani.json": {
        "claim_u": 0.5, "claim_psi": 0.3,
        "real_u": 0.1, "real_psi": 0.0,
        "posts_update": {
            0: "Central Park carriage horse drivers and animal welfare advocates lobby municipal lawmakers over proposed operational regulations.\nEvidence: NYC City Council hearings, industry permits\n#NYC #AnimalWelfare",
            1: "Drivers petitioned elected representatives to preserve historic tourism jobs, while animal advocates pressed for electric carriage transitions.\nStated Judgement: (+0.5, +0.3) - Public Hearing",
            2: "The debate involves typical municipal negotiations balancing historic small-business employment against modern urban animal welfare standards.\nResulting Judgement: (+0.1, 0.0) - Municipal Regulation",
            3: "Verdict: PASS - Awakening into Grace.\nStandard municipal debate negotiating workplace livelihoods and urban animal welfare standards.",
            4: "- Carriage Workers: PASS (+0.3, +0.2) - Advocating for small-business livelihoods and fair transition terms.\n- Animal Welfare Advocates: PASS (+0.3, +0.2) - Campaigning for humane urban animal standards."
        }
    },
    # 22. David Jones Administration
    "factcheck_david-jones-administration.json": {
        "claim_u": 0.5, "claim_psi": 0.4,
        "real_u": -0.3, "real_psi": -0.4,
        "posts_update": {
            0: "Major Australian retail department store enters voluntary administration to restructure debt amid shifts in consumer spending.\nEvidence: Australian Securities and Investments Commission filings, administrator statements\n#Business #Australia",
            1: "Corporate administrators announced restructuring processes aimed at preserving store operations and safeguarding employee entitlements.\nStated Judgement: (+0.5, +0.4) - Corporate Restructuring",
            2: "High commercial retail rents and digital e-commerce competition forced formal debt administration, threatening regional retail jobs.\nResulting Judgement: (-0.3, -0.4) - Commercial Distress",
            3: "Verdict: FAIL - Fall into Destruction.\nVoluntary corporate administration to restructure department store operations under commercial insolvency law.",
            4: "- Insolvency Administrators: PASS (+0.4, +0.3) - Working to safeguard employee entitlements and restructure viable stores.\n- Retail Workers: PASS (+0.3, 0.0) - Facing employment uncertainty through no fault of their own."
        }
    },
    # 23. Grocery Cyberattacks Alert
    "factcheck_grocery_store_cyberattacks_warning.json": {
        "claim_u": 0.6, "claim_psi": 0.4,
        "real_u": -0.4, "real_psi": -0.3,
        "posts_update": {
            0: "Federal cybersecurity agencies issue threat advisories regarding ransomware campaigns targeting retail grocery distribution chains.\nEvidence: CISA advisory, industry threat alerts\n#Cybersecurity #SupplyChain",
            1: "Security officials advised critical supply chain operators to bolster network isolation and deploy multi-factor authentication protocols.\nStated Judgement: (+0.6, +0.4) - Threat Advisory",
            2: "Criminal cyber syndicates increasingly probe logistics databases, requiring immediate private and public security hardening to prevent food distribution pauses.\nResulting Judgement: (-0.4, -0.3) - Cyber Vulnerability",
            3: "Verdict: FAIL - Fall into Destruction.\nCybersecurity authorities alert grocery supply networks to criminal ransomware threats.",
            4: "- CISA & Security Analysts: PASS (+0.6, +0.5) - Disseminating proactive vulnerability disclosures.\n- Criminal Hackers: FAIL (-0.8, -0.7) - Targeting civilian logistics infrastructure for extortion."
        }
    },
    # 24. Hegseth Wife Consulting
    "factcheck_hegseth-wife-consulting.json": {
        "claim_u": 0.4, "claim_psi": 0.3,
        "real_u": -0.3, "real_psi": -0.2,
        "posts_update": {
            0: "Political reporting details commercial consulting contracts secured by spouses of incoming presidential cabinet nominees.\nEvidence: Corporate registration logs, campaign disclosure filings\n#Politics #Ethics",
            1: "News outlets questioned potential conflicts of interest between private consulting retainers and upcoming executive nominations.\nStated Judgement: (+0.4, +0.3) - Ethics Scrutiny",
            2: "Private consulting firms capitalizing on proximity to federal power highlights recurrent ethical concerns in Washington's transition revolving door.\nResulting Judgement: (-0.3, -0.2) - Revolving Door Ethics",
            3: "Verdict: FAIL - Fall into Destruction.\nMedia reporting highlighting recurring ethics and conflict-of-interest questions in presidential transitions.",
            4: "- Ethics Watchdogs: PASS (+0.5, +0.4) - Calling for transparency and recusals in federal appointments.\n- Transition Consultants: COND (-0.3, -0.2) - Monetizing political proximity during government transitions."
        }
    },
    # 25. Drone Attack on Ryazan Refinery
    "factcheck_drone-attack-ryazan-oil-refinery.json": {
        "claim_u": 0.6, "claim_psi": 0.4,
        "real_u": -0.6, "real_psi": -0.5,
        "posts_update": {
            0: "Long-range drone strikes trigger fires at a major Russian industrial fuel refinery during ongoing military hostilities.\nEvidence: Satellite thermal imaging, regional emergency services reports\n#UkraineWar #Defense",
            1: "Military communiques reported precision strikes aimed at degrading fuel supplies supporting frontline combat operations.\nStated Judgement: (+0.6, +0.4) - Military Strategy",
            2: "Satellite imagery confirms significant physical infrastructure destruction, reflecting intense attritional warfare targeting petrochemical logistics.\nResulting Judgement: (-0.6, -0.5) - Kinetic Destruction",
            3: "Verdict: FAIL - Fall into Destruction.\nKinetic drone strikes degrading industrial energy infrastructure amid interstate warfare.",
            4: "- Defense Planners: PASS (+0.4, +0.3) - Targeting strategic logistics to degrade offensive combat capabilities.\n- Petrochemical Operators: COND (-0.4, -0.4) - Supplying state military machinery under active wartime conditions."
        }
    },
    # 26. Beau Lamarre-Condon Murder Trial
    "factcheck_beau_lamarre_condon_trial_2026.json": {
        "claim_u": 0.5, "claim_psi": 0.4,
        "real_u": -0.9, "real_psi": -0.9,
        "posts_update": {
            0: "Supreme Court of New South Wales begins double-murder trial of former police officer accused in fatal shootings.\nEvidence: NSW Supreme Court filings, police ballistic evidence\n#Sydney #Justice",
            1: "Crown prosecutors presented forensic ballistic and digital evidence, pursuing maximum criminal accountability for two homicides.\nStated Judgement: (+0.5, +0.4) - Judicial Accountability",
            2: "Court records document heinous violent crimes resulting in the tragic deaths of two young men, which the judicial system is now adjudicating.\nResulting Judgement: (-0.9, -0.9) - Heinous Criminal Offense",
            3: "Verdict: FAIL - Fall into Destruction.\nJudicial prosecution of grave double-murder charges under state criminal law.",
            4: "- Crown Prosecutors & Police: PASS (+0.7, +0.7) - Rigorously presenting evidence to secure legal justice for victims.\n- Accused: FAIL (-1.0, -1.0) - On trial for tragic, premeditated double murder."
        }
    },
    # 27. Hong Kong Joshua Wong Case
    "factcheck_hong-kong-joshua-wong-sentenced-national-security-case.json": {
        "claim_u": 0.5, "claim_psi": 0.3,
        "real_u": -0.8, "real_psi": -0.7,
        "posts_update": {
            0: "Hong Kong court sentences pro-democracy activist Joshua Wong to additional prison terms under the National Security Law.\nEvidence: Court sentencing remarks, international human rights records\n#HongKong #HumanRights",
            1: "Authorities framed the prosecution as essential legal enforcement to protect regional political stability.\nStated Judgement: (+0.5, +0.3) - Statutory Enforcement",
            2: "International legal monitors document severe suppression of fundamental political dissent and civil liberties under sweeping security legislation.\nResulting Judgement: (-0.8, -0.7) - State Political Repression",
            3: "Verdict: FAIL - Fall into Destruction.\nState judicial system imposing prison sentences on prominent pro-democracy activists under sweeping security laws.",
            4: "- Pro-Democracy Activists: PASS (+0.7, +0.5) - Peacefully advocating for civic liberties and democratic governance.\n- Security Court: FAIL (-0.8, -0.7) - Criminalizing peaceful political dissent and assembly."
        }
    },
    # 28. Botched Execution Case
    "factcheck_doctor-who-botched-christa-pikes-execution.json": {
        "claim_u": 0.6, "claim_psi": 0.4,
        "real_u": -0.8, "real_psi": -0.8,
        "posts_update": {
            0: "State corrections department investigation reveals critical procedural errors and unqualified medical oversight during a capital execution.\nEvidence: Department of Corrections audit report, federal habeas filings\n#Corrections #Justice",
            1: "State officials initially assured courts that lethal injection protocols were executed with professional medical compliance.\nStated Judgement: (+0.6, +0.4) - Administrative Assurance",
            2: "Official investigative findings document grave medical negligence, lack of credentialing, and severe procedural breakdown in capital execution protocols.\nResulting Judgement: (-0.8, -0.8) - Institutional Breakdown",
            3: "Verdict: FAIL - Fall into Destruction.\nSevere institutional failure and medical negligence in state capital execution procedures.",
            4: "- Investigative Oversight: PASS (+0.6, +0.5) - Exposing systemic failures in state execution protocols.\n- Corrections Authority: FAIL (-0.8, -0.8) - Failing to enforce mandatory medical and constitutional standards."
        }
    }
}

def execute_suspect_reaudits():
    print("=================================================================")
    print("RE-AUDITING ALL 28 SUSPECT STORIES IN stories/")
    print("=================================================================\n")
    
    success_count = 0
    missing_count = 0
    
    for fn, spec in SUSPECT_REAUDIT_SPECS.items():
        fp = os.path.join(drafts_dir, fn)
        if not os.path.exists(fp):
            print(f"[MISSING] {fn}")
            missing_count += 1
            continue
            
        with open(fp, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        story = data[0] if isinstance(data, list) else data
        
        story["claim_u"] = spec["claim_u"]
        story["claim_psi"] = spec["claim_psi"]
        story["real_u"] = spec["real_u"]
        story["real_psi"] = spec["real_psi"]
        story["status"] = "DRAFT (CALIBRATED)"
        
        # Remove stale tensors
        if "stated_forces" in story:
            del story["stated_forces"]
        if "actual_forces" in story:
            del story["actual_forces"]
            
        # Update posts
        posts = story.get("posts", [])
        for idx, text in spec["posts_update"].items():
            if idx < len(posts):
                posts[idx] = text
        story["posts"] = posts
        
        # Enforce deterministic trajectory
        story = enforce_deterministic_trajectory(story)
        path = get_path_name(story["claim_u"], story["claim_psi"], story["real_u"], story["real_psi"])
        story["path_name"] = path
        
        out_data = [story] if isinstance(data, list) else story
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(out_data, f, indent=2, ensure_ascii=False)
            
        print(f"[OK] Re-audited: {fn} -> ({story['claim_u']},{story['claim_psi']}) -> ({story['real_u']},{story['real_psi']}) | {path}")
        success_count += 1
        
    print(f"\nCompleted re-auditing {success_count} suspect stories.")

if __name__ == "__main__":
    execute_suspect_reaudits()
