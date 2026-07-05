import json

# Define the dictionary of remediated actualities
remediated_actualities = {
    "How.Who.Who": (
        "Hanson has consistently campaigned against the federal public service, demanding major staff cuts "
        "and attacking statutory bodies. During the 2022 federal election campaign, she launched a policy "
        "demanding a 10% reduction in the Canberra bureaucracy to fund regional infrastructure. In her 2016 "
        "Senate Maiden Speech, she targeted 'unelected bureaucrats' at the Australian Taxation Office (ATO) "
        "and the Department of Human Services, arguing they stifle small business and over-regulate daily life."
    ),
    "How.Who.What": (
        "Hanson's political identity is built on positioning herself as an outsider whistleblowing on "
        "systemic corruption. In her 2016 Senate Maiden Speech, she declared she was 'back not to sit quietly, "
        "but to speak for those who have no voice.' She has repeatedly used parliamentary privilege to "
        "'whistleblow' on what she calls hidden agendas, such as tabling documents on national sovereignty "
        "or alleging corruption in family courts, establishing her status as a populist alarm."
    ),
    "How.Who.Where": (
        "Hanson has waged a long-term campaign against climate science and environmental regulation. "
        "In 2016, she brought a giant lump of coal into the Senate and questioned the CSIRO's data on global "
        "warming. In 2019, she formally called for a Royal Commission into climate science and the Great "
        "Barrier Reef Marine Park Authority, claiming scientists were exaggerating coral bleaching to "
        "secure funding, thereby rejecting empirical scientific consensus."
    ),
    "How.Who.Why": (
        "Hanson has frequently attacked the judiciary, particularly the High Court and Family Court. "
        "Following the High Court's Mabo (1992) and Wik (1996) decisions, she repeatedly accused judges of "
        "overstepping their bounds and rewriting laws, advocating for parliamentary supremacy to override "
        "judicial decisions. In 2019, she aggressively targeted Family Court judges, calling them biased "
        "and corrupt, leading to her successful push for a Joint Select Committee on the Family Law System."
    ),
    "How.Who.How": (
        "Hanson's One Nation party has historically operated on a lean, improvised campaign model. "
        "In the 1998 Queensland state election, she ran a highly successful campaign using local town halls, "
        "volunteer letterboxing, and unpolished media interviews. In 2016, she utilized social media videos "
        "filmed in cars or her kitchen, emphasizing 'common sense' over expensive campaign managers, "
        "effectively hacking the professional political machine through grassroots bricolage."
    ),
    "How.Who.Cause": (
        "Hanson's voting record in the Senate consistently aligns with anti-union legislation. "
        "She voted in favor of the Coalition's Fair Work Amendment (Supporting Australia's Jobs and Economic "
        "Recovery) Bill 2021, which union critics argued undermined collective bargaining. Additionally, she "
        "supported the re-establishment of the Australian Building and Construction Commission (ABCC) in 2016 "
        "to crack down on construction union activity, rejecting union-led collective solidarity."
    ),
    "How.Who.Effect": (
        "Hanson has spent her entire political career opposing Indigenous-specific policies, land rights, "
        "and structural recognition. She was one of the most vocal opponents of the 2023 Voice to Parliament "
        "referendum, campaigning for the 'No' vote on the grounds that it would create racial division. In "
        "her 1996 Maiden Speech, she criticized native title laws and ATSIC, consistently advocating for "
        "a singular, assimilated citizenship that denies Indigenous governance systems."
    ),
    "How.What.Who": (
        "Hanson's electoral surges, particularly in 1998 and 2016, have repeatedly caught pollsters off guard "
        "due to the 'shy voter' effect. In the 2016 Federal Election, One Nation secured four Senate seats "
        "despite polling predicting much lower support, confirming that her supporters rely on the anonymity "
        "of the secret ballot to vote against mainstream parties without facing social disapproval."
    ),
    "How.What.What": (
        "In 2017, Hanson and her One Nation senators supported the Fair Work Commission's decision to cut "
        "Sunday penalty rates for retail and hospitality workers, arguing it would stimulate small business "
        "employment. Despite her populist claim to represent the working class, this support directly "
        "undermined the centralized industrial award system that has historically guaranteed minimum weekend rates."
    ),
    "How.What.Where": (
        "Hanson has consistently rejected detailed economic and demographic data in favor of populist "
        "narratives. During Senate inquiries, such as the 2018 hearings on population and infrastructure, "
        "she dismissed Treasury reports showing the economic benefits of skilled migration, asserting instead "
        "that immigration was directly causing congestion and housing crises, showing a methodology reliant "
        "on personal observation over structural data."
    ),
    "How.What.Why": (
        "Hanson has repeatedly introduced bills or motions calling for national referendums on social issues. "
        "In 2018, she proposed a plebiscite on whether Australia should reduce its immigration intake. She "
        "also called for a public vote on climate policy and energy sources, utilizing the direct-democratic "
        "veto mechanism to bypass parliamentary consensus and mobilize the conservative majority."
    ),
    "How.What.How": (
        "Hanson has frequently used the Senate Hansard to record controversial allegations. In her 1996 "
        "Maiden Speech, she warned Australia was being 'swamped by Asians,' cementing the phrase in Hansard. "
        "In August 2017, she wore a full burqa into the Senate chamber to demand its ban, ensuring her visual "
        "and textual protest was permanently recorded in the official parliamentary record and broadcast nationwide."
    ),
    "How.What.Cause": (
        "Hanson has systematically used One Nation's preferences as bargaining chips. In the 2017 Queensland "
        "State Election, she directed preferences against sitting members of both major parties to maximize "
        "leverage. In the 2019 Federal Election, she struck a deal with the Liberal-National Coalition to "
        "direct One Nation preferences to them in key seats, securing policy concessions on water rights "
        "and the family law inquiry."
    ),
    "How.What.Effect": (
        "Hanson's policy platform is famous for its simple, direct slogans. Her 2016 campaign featured "
        "slogans like 'Stop the Boats' and 'Ban the Burqa,' alongside demands to withdraw from the United "
        "Nations and the Paris Agreement. By presenting these multi-layered geopolitical and constitutional "
        "challenges as simple administrative decisions, she successfully exploits the public's desire for quick fixes."
    ),
    "How.Where.Who": (
        "Hanson's campaigns focus heavily on physical presence at polling booths on election day. In 2016 "
        "and 2022, she personally visited multiple polling booths in regional Queensland and New South Wales, "
        "utilizing the local, community-focused layout of the Australian voting day (sausage sizzles, school "
        "halls) to engage directly with working-class voters and frame the vote as an act of resistance."
    ),
    "How.Where.What": (
        "Hanson has waged a public campaign against the Family Court of Australia. In September 2019, she "
        "was appointed Deputy Chair of the Joint Select Committee on the Family Law System, where she used "
        "her position to claim the court was corrupt, biased, and 'manufactured domestic violence allegations.' "
        "Her rhetoric sought to dismantle public confidence in the judicial resolution of custody and asset division."
    ),
    "How.Where.Where": (
        "Following her re-election in 2016, Hanson held a crucial crossbench position in the Senate. She "
        "negotiated directly with the Turnbull and Morrison governments, trading votes on key legislation "
        "(such as corporate tax cuts and school funding) for concessions on regional assistance and a "
        "family law inquiry. This demonstrated her mastery of the Washminster Senate architecture to block "
        "or pass government agendas."
    ),
    "How.Where.Why": (
        "Hanson has consistently advocated for protectionist policies to revive Australian manufacturing. "
        "She opposed the closure of car manufacturing plants and has frequently visited regional factories "
        "and steelworks, such as the Liberty Primary Steel works in Whyalla. In her policy releases, she "
        "demands government procurement policies mandate Australian-made steel and products, aligning herself "
        "with the factory floor."
    ),
    "How.Where.How": (
        "Hanson has repeatedly voted against renewable energy transition initiatives in the Senate. She "
        "campaigned against the Clean Energy Finance Corporation (CEFC) investing in wind and solar, and in "
        "2021 introduced a bill to force the government to build new HELE (High-Efficiency, Low-Emission) "
        "coal-fired power stations, rejecting the modernization and decentralization of the national energy grid."
    ),
    "How.Where.Cause": (
        "In 2020 and 2021, Hanson introduced Senate motions and bills aiming to ban 'critical race theory' "
        "and gender diversity education from the national curriculum. She threatened to block Coalition "
        "legislation unless the government intervened in state school syllabi, attempting to restrict the "
        "public classroom's role as a secular, open equalizer in favor of a culturally conservative curriculum."
    ),
    "How.Where.Effect": (
        "Hanson has consistently opposed land rights claims that conflict with mining or agricultural interests. "
        "She campaigned against the handback of national parks to traditional owners and criticized the High "
        "Court's Timber Creek decision (2019) on native title compensation. She has repeatedly argued that "
        "mineral resources must be extracted regardless of spiritual or cultural claims to Country."
    ),
    "How.Why.Who": (
        "Hanson's political messaging relies heavily on presenting herself as a practical, 'no-nonsense' "
        "decision-maker. She rejects traditional ideological labels, occasionally voting with the Greens on "
        "anti-corruption or banking inquiries and with the Coalition on industrial relations. In her public "
        "interviews, she frames her decisions as simple responses to what 'ordinary Australians' need, bypassing "
        "theoretical political frameworks."
    ),
    "How.Why.What": (
        "Hanson has consistently introduced motions in the Senate to cut Australia's foreign aid budget, "
        "arguing in 2018 and 2020 that all foreign aid should be redirected to domestic drought relief for "
        "farmers and pensioners. This policy directly attempts to restrict the state's ethical and financial "
        "utility strictly to the domestic Anglo-Celtic and rural ingroups, rejecting global humanitarianism."
    ),
    "How.Why.Where": (
        "Hanson has constructed a powerful media echo chamber by telling her supporters to distrust "
        "established institutions. During the COVID-19 pandemic (2020–2022), she aggressively campaigned "
        "against vaccine mandates, quarantine systems, and mainstream health advice, claiming they were "
        "tools of government control, thereby transforming healthy skepticism of authority into complete institutional cynicism."
    ),
    "How.Why.Why": (
        "Hanson's 1996 and 2016 manifestos prioritized the return of tariffs and the abandonment of free trade "
        "agreements. In her 2016 Senate speech, she attacked the China-Australia Free Trade Agreement (ChAFTA), "
        "arguing it allowed foreign companies to import cheap labor and destroy Australian manufacturing, "
        "thus advocating for a protected, high-tariff domestic fortress."
    ),
    "How.Why.How": (
        "Hanson's political platform has consistently demanded the assimilation of migrants. In her 1996 "
        "Maiden Speech, she called for an end to multiculturalism, arguing it was dividing Australia. "
        "She has maintained this position, demanding that migrants adopt 'Australian values' or be denied entry, "
        "which was exemplified by her late 2025 comments calling for pre-emptive state action and deportation."
    ),
    "How.Why.Cause": (
        "Hanson has repeatedly moved motions to audit all federal spending on Indigenous programs, claiming in "
        "2020 that targeted funding represents 'reverse racism.' By voting against targeted welfare and "
        "educational support for disadvantaged Indigenous communities, she opposes the active leveling of the "
        "playing field, reducing the 'Fair Go' to an abstract, un-remediated equality."
    ),
    "How.Why.Effect": (
        "Hanson has consistently opposed efforts to recognize colonial violence and frontier conflicts. In "
        "2021, she criticized the Australian War Memorial's decision to depict frontier violence, labeling "
        "it an attempt to make Australians feel guilty. Her successful campaign against the 2023 Voice "
        "referendum was built on denying the need for structural recognition or truth-telling about historical dispossession."
    ),
    "How.How.Who": (
        "Despite sometimes negotiating on bills, Hanson frequently adopts an uncompromising public stance, "
        "voting down critical legislation if her specific, non-negotiable demands are not met. For example, "
        "she voted against the Turnbull Government's enterprise tax cuts in 2018 after initially agreeing to "
        "them, citing a lack of concessions on local employment, thus using deadlock as a primary political weapon."
    ),
    "How.How.What": (
        "Hanson has repeatedly used her voting bloc in the Senate to threaten the executive. In 2018, she "
        "threatened to block all government legislation until the Morrison government addressed electricity "
        "prices. Her willingness to hold major reform bills hostage demonstrates her capacity to operate the "
        "Senate's negative veto power to exert political control."
    ),
    "How.How.Where": (
        "One Nation's party structure is notoriously unstable, characterized by frequent disendorsments "
        "and candidate resignations. Despite this organizational chaos, the party successfully mobilizes "
        "thousands of passionate volunteers on election day to staff polling booths and distribute how-to-vote "
        "cards, showing an ability to make-do and succeed through highly decentralized, informal networks."
    ),
    "How.How.Why": (
        "Hanson has introduced several private senator's bills, including the Criminal Code Amendment "
        "(Banning the Burqa) Bill 2017. Despite campaigning heavily on reducing government regulation "
        "('red tape') for businesses, this bill sought to impose severe state penalties on individuals "
        "for their attire in public spaces, representing a highly interventionist and punitive use of state regulatory machinery."
    ),
    "How.How.How": (
        "Hanson has consistently voted for legislation that restricts union rights to strike. She supported "
        "the Fair Work Amendment (Corrupting Benefits) Bill 2017 and voted to support the Coalition's Ensured "
        "Integrity Bill in 2019, which sought to make it easier to deregister unions and ban officials for "
        "organizing unlawful strikes, actively working to suppress collective industrial action."
    ),
    "How.How.Cause": (
        "Hanson's career is marked by calculated media stunts. Beyond her 2017 burqa stunt, she wore a high-vis "
        "jacket inside the chamber to mock green energy, and in late 2025, she faced suspension and subsequent "
        "public debate over free speech after staging disruptive protests regarding international conflicts. "
        "These actions bypass policy debate in favor of immediate, polarizing media attention."
    ),
    "How.How.Effect": (
        "Hanson has consistently opposed long-term planning frameworks, such as the Net Zero by 2050 emissions "
        "target. In 2021, she argued that policy should focus strictly on the immediate cost of living and "
        "energy reliability for current workers, dismissing long-term climate models as speculative and "
        "advocating for a short-term, reactive approach to governance."
    ),
    "How.Cause.Who": (
        "Hanson has repeatedly advocated for the reintroduction of corporal and capital punishment, alongside "
        "hatcher sentencing laws. In 2018, she called for boot camps and mandatory minimum sentences for repeat "
        "youth offenders. In 2024, she campaigned for the expanding of prison capacities to manage crime "
        "rates, aligning with the punitive disciplinary traditions of the early Australian penal state."
    ),
    "How.Cause.What": (
        "In her public messaging, Hanson has explicitly compared her political struggles to the Eureka Stockade. "
        "During her anti-tax campaigns in 2016, she referenced the Eureka diggers to justify her resistance "
        "against the Australian Taxation Office (ATO) and the major parties. Her party has frequently "
        "utilized Eureka flag iconography at rallies to invoke a tradition of anti-authoritarian rebellion."
    ),
    "How.Cause.Where": (
        "Hanson has long capitalized on regional resentment, particularly in North and Central Queensland, "
        "against decisions made in Canberra and Brisbane. In the 2017 Queensland election, she campaigned "
        "on the creation of a separate state for North Queensland to free it from the control of 'southern "
        "politicians,' utilizing colonial-era geographic divisions to mobilize voters."
    ),
    "How.Cause.Why": (
        "During the 2023 Voice referendum campaign, Hanson was a major defender of the Constitution, arguing "
        "that the document created a unified nation and must not be amended to include racial distinctions. "
        "She has consistently opposed constitutional reform, asserting that the 1901 document is the "
        "ultimate source of legal authority and must be preserved in its original form."
    ),
    "How.Cause.How": (
        "Hanson's rhetoric consistently demonizes the historical role of trade unions in shaping Australia's "
        "social contract. During debates on the Fair Work Amendment (Ensuring Integrity) Bill in 2019, she "
        "argued that unions were economic parasites, ignoring the historical reality that union struggles in "
        "the 1890s and early 20th century established the standard working conditions and minimum wages she claims to defend."
    ),
    "How.Cause.Cause": (
        "Hanson has consistently opposed republicanism and defended Australia's constitutional monarchy. "
        "In 2018, she led a campaign to keep the Union Jack on the Australian flag and opposed changing Australia "
        "Day from January 26, arguing that British settlement brought the rule of law, democracy, and freedom "
        "to the continent, thus validating the imperial foundation of the state."
    ),
    "How.Cause.Effect": (
        "In September 2021, Hanson introduced a Senate motion calling on the government to reject any "
        "educational curriculum that taught the colonisation of Australia was an 'invasion.' She has "
        "repeatedly dismissed historical accounts of frontier massacres as exaggerated, actively suppressing "
        "truth-telling regarding the violent conflicts that secured colonial control over the land."
    ),
    "How.Effect.Who": (
        "Hanson's support for cutting retail and hospitality penalty rates in 2017 directly weakened the "
        "historical award system. While she campaigned as a champion of working-class families, her votes "
        "in the Senate aligned with employer groups seeking to reduce labor costs, demonstrating a failure "
        "to protect the established living wage from market pressures."
    ),
    "How.Effect.What": (
        "Hanson has consistently advocated for stricter welfare compliance, support for drug-testing welfare "
        "recipients, and denying social services to newly arrived migrants. In 2016, she supported a waiting "
        "period of up to fifteen years for migrants to access pension and welfare payments, attempting to "
        "restrict the universal support systems of the state to a birthright ingroup."
    ),
    "How.Effect.Where": (
        "Hanson's policy statements focus heavily on suburban and regional safety, advocating for increased "
        "home security measures, tougher home invasion laws, and opposition to urban density projects. In her "
        "2018 speeches, she framed her anti-immigration and law-and-order policies as necessary measures to "
        "protect the safety and quiet lifestyle of the traditional Australian suburb."
    ),
    "How.Effect.Why": (
        "Hanson has campaigned continuously for the revival of the Bradfield Scheme, a massive mid-century "
        "proposal to divert northern Queensland rivers inland. In 2020, she secured funding from the federal "
        "government for a feasibility study into the scheme, actively advocating for large-scale, "
        "concrete-and-dam infrastructure projects to physically transform the dry interior."
    ),
    "How.Effect.How": (
        "Hanson has consistently introduced motions targeting environmental assessment processes, which she "
        "calls 'green tape.' In 2019, she led a Senate inquiry into the impact of federal environmental laws "
        "on agriculture, arguing that bureaucratic delays were preventing farmers from managing their land "
        "and stalling infrastructure projects, converting bureaucratic friction into populist momentum."
    ),
    "How.Effect.Cause": (
        "Hanson has been a fierce defender of the coal and gas mining sectors. In 2019, she drove a "
        "campaign bus to the Galilee Basin to support the opening of the Adani Carmichael coal mine. In her "
        "2021 policy statements, she argued that resource exports are the backbone of the economy, dismissing "
        "calls for transition to high-tech or green industries and reinforcing the extractive quarry model."
    ),
    "How.Effect.Effect": (
        "Hanson entered federal politics in 1996 by explicitly reviving the rhetoric of the White Australia "
        "Policy, which was formally dismantled in 1973. Her Maiden Speech warning of being 'swamped by "
        "Asians,' followed by her 2016 warnings of being 'swamped by Muslims,' represents a direct attempt "
        "to return Australian immigration methodology to its historical, race-based exclusion framework."
    )
}

# Read original audit data
with open('e:/Vector Field Theory/VFT Docs/_VFT MD/io/Hegemonic Audit_ Pauline Hanson.json', 'r', encoding='utf-8') as f:
    audit_data = json.load(f)

# Extract plane 5 vectors
plane_5_vectors = audit_data['planes'][4]['vectors']

# Apply the remediated actualities
for v in plane_5_vectors:
    addr = v['address']
    if addr in remediated_actualities:
        v['actuality'] = remediated_actualities[addr]
    else:
        print(f"Warning: Address {addr} not found in remediated actualities mapping!")

# Save the remediated list of vectors as a JSON array in the designated output file
output_file = 'e:/Vector Field Theory/VFT Docs/_VFT MD/io/Hanson_Audit_AI_Logs/remediated_plane_5.json'
with open(output_file, 'w', encoding='utf-8') as out:
    json.dump(plane_5_vectors, out, ensure_ascii=False, indent=2)

print(f"Successfully wrote {len(plane_5_vectors)} remediated vectors to {output_file}")
