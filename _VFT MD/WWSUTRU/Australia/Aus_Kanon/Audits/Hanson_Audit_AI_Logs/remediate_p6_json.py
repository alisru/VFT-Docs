import json

# Define the researched actualities for Plane 6
actualities = {
    "Cause.Who.Who": (
        "Pauline Hanson's populist rhetoric has consistently weaponized working-class resentment against the Canberra "
        "\"elites\" since her 1996 maiden speech. Her 2016 Senate maiden speech reinforced this, claiming \"ordinary Australians\" "
        "are ignored. Throughout her career, she has capitalized on this anti-establishment sentiment, notably in campaigns "
        "against carbon tax policies (2011–2014) and during COVID-19 restriction protests (2020–2022)."
    ),
    "Cause.Who.What": (
        "Hanson has consistently championed British colonial legacy as the source of Australia's democratic foundations. "
        "In a 2018 Senate debate and her 2022 speeches opposing the First Nations Voice, she declared that Australia owes "
        "its legal system and freedoms to its British heritage and the Magna Carta. She has repeatedly opposed attempts "
        "to change the date of Australia Day (January 26) or replace the flag, arguing they represent this foundational British settlement."
    ),
    "Cause.Who.Where": (
        "Hanson has long championed the rights of regional farmers and pastoralists, positioning them as the backbone of "
        "the nation. In 2017, she strongly defended agricultural water allocations in the Murray-Darling Basin and campaigned "
        "against foreign ownership of agricultural land (e.g., the sale of S. Kidman & Co). Her Senate votes consistently favor "
        "deregulation for regional farming and protection of rural property rights against state-imposed environmental restrictions."
    ),
    "Cause.Who.Why": (
        "Hanson has vehemently denied First Nations prior sovereignty throughout her career. During the 2023 Voice to "
        "Parliament referendum campaign, she campaigned for the \"No\" vote, repeatedly stating that there is no prior "
        "sovereignty and that all Australians are equal under one law. This aligns with her walking out of the Senate Welcome "
        "to Country in July 2022, where she declared, \"I have as much right to be here as anyone else.\""
    ),
    "Cause.Who.How": (
        "Hanson has actively campaigned to defend the Australian flag and the ANZAC tradition from progressive reform. "
        "In 2018, she introduced motions to protect the flag and frequently weaponizes the ANZAC legacy in speeches, "
        "arguing that the sacrifices at Gallipoli and the Western Front mandate strict border protection. She has also "
        "strongly opposed replacing the flag, calling it an insult to the diggers who fought under it."
    ),
    "Cause.Who.Cause": (
        "Hanson's voting record in the Senate shows consistent opposition to union power, voting in favor of the Coalition's "
        "Ensuring Integrity Bill in 2019 to make it easier to deregister unions. While she claims to represent the working class, "
        "she frequently attacks union leadership (such as the CFMEU) in public debates, arguing that union strikes and "
        "collective agreements inflate construction costs and harm small businesses."
    ),
    "Cause.Who.Effect": (
        "In her 2016 Senate maiden speech and subsequent media appearances, Hanson praised post-war European immigrants for "
        "their \"assimilation and hard work.\" She used this historical standard to criticize modern non-white and Muslim "
        "immigration, claiming they form enclaves and refuse to integrate. This narrative forms the basis of her calls "
        "for zero net immigration and the reintroduction of assimilationist policies."
    ),
    "Cause.What.Who": (
        "Hanson has repeatedly defined 1788 as the starting point of Australian civilization, downplaying or ignoring "
        "pre-colonial history. In speeches surrounding Australia Day debates (2020–2024), she argued that British settlement "
        "brought modern infrastructure and law to the continent, and that Australians have \"nothing to be ashamed of.\" "
        "She opposes efforts to treat January 26 as \"Invasion Day,\" framing it instead as a day of national birth."
    ),
    "Cause.What.What": (
        "In 2021 and 2022 Senate debates on history curriculum, Hanson rejected the inclusion of the Frontier Wars, labeling "
        "Aboriginal societies as \"stone-age\" before British arrival. She has consistently opposed efforts to recognize "
        "colonial violence in national war memorials, arguing that settlement was largely peaceful and that modern curriculum "
        "is being rewritten by \"left-wing activists\" to foster national guilt."
    ),
    "Cause.What.Where": (
        "Hanson has frequently used the Eureka Stockade and the Southern Cross flag to symbolize her anti-taxation and "
        "anti-government stances. In her 2016 campaign, she equated rural frustration over banking and dairy deregulation "
        "to the 1854 miners' revolt. However, she has also opposed the use of the Eureka flag by trade unions, asserting "
        "that the symbol belongs to ordinary tax-paying citizens fighting government overreach."
    ),
    "Cause.What.Why": (
        "Hanson has positioned herself as a strict constitutional monarchist, opposing any alteration to the 1901 constitutional "
        "framework. She strongly campaigned against the Republic referendum in 1999 and the Voice to Parliament referendum in 2023. "
        "She argues that the Constitution's existing division of powers and legal structure must remain unchanged to preserve "
        "national unity and the sovereignty of the Crown."
    ),
    "Cause.What.How": (
        "Hanson has consistently utilized ANZAC Day (April 25) to promote a nationalist agenda, introducing motions to "
        "protect military commemorations. In 2018, she condemned activists who critiqued the ANZAC myth or linked it to "
        "imperialism. She regularly attends Dawn Services and campaigns for increased funding for the Australian War Memorial, "
        "arguing that the ANZAC spirit is the sole binding narrative of the Australian people."
    ),
    "Cause.What.Cause": (
        "Hanson has defended the constitutional structure that allows the Governor-General to dismiss a government, most "
        "notably in discussions surrounding the legacy of the 1975 Dismissal. She argues that the reserve powers of the Crown "
        "are a necessary constitutional fail-safe to protect the nation from political instability or executive overreach by "
        "the Prime Minister, reinforcing her constitutional monarchist stance."
    ),
    "Cause.What.Effect": (
        "Hanson was not in parliament during the 2008 Apology to the Stolen Generations but publicly opposed it, calling "
        "it part of a \"guilt industry.\" In July 2022, she walked out of the Senate during the Welcome to Country ceremony, "
        "asserting that she would not apologize for historical actions she did not commit. Her voting record includes "
        "consistent opposition to any legislation that embeds symbolic reconciliation or historical apology."
    ),
    "Cause.Where.Who": (
        "Throughout her political career, Hanson has advocated for tough-on-crime policies, including mandatory sentencing "
        "and stricter prison conditions. In her 2018 law-and-order policy announcements, she called for the reintroduction "
        "of national service for repeat offenders and harsher penalties for property crimes. Her rhetoric emphasizes "
        "retributive justice and incarceration as the primary mechanism for social stability."
    ),
    "Cause.Where.What": (
        "Hanson has been a vociferous supporter of the Australian resource sector, especially coal and gas mining in Queensland. "
        "In 2019, she campaigned heavily for the approval of the Adani Carmichael coal mine and has repeatedly voted against "
        "carbon pricing, mining taxes, and emissions reduction targets, arguing that the nation's economic survival is dependent "
        "on fossil fuel extraction."
    ),
    "Cause.Where.Where": (
        "Hanson's political platform is built on appealing to regional and rural voters, frequently contrasting \"hard-working "
        "bush communities\" with \"latte-sipping urban elites.\" During her regional tours (e.g., Queensland regional tours "
        "in 2017 and 2020), she framed cities as centers of progressive decay and out-of-touch policies, while arguing that "
        "authentic Australian values are preserved in the agricultural and mining regions."
    ),
    "Cause.Where.Why": (
        "Hanson's campaign rhetoric frequently uses militaristic language, framing cultural debates as a \"battle for Australia's "
        "survival.\" In her 2016 Senate election campaign and subsequent anti-immigration rallies, she characterized progressive "
        "immigration policies as an invasion that is \"swamping\" the country, calling on supporters to \"hold the line\" and "
        "defend their heritage like soldiers on a battlefield."
    ),
    "Cause.Where.How": (
        "Hanson has repeatedly attacked the legitimacy of the Aboriginal Tent Embassy in Canberra, calling it an eyesore "
        "and demanding its removal. In 2018, she moved a motion in the Senate to remove the Aboriginal flag from the chamber, "
        "arguing that it is a divisive symbol and that only the Australian National Flag should be displayed in official public institutions."
    ),
    "Cause.Where.Cause": (
        "In her regional development policies, Hanson has advocated for major nation-building infrastructure projects, "
        "such as the Hybrid Snowy 2.0 scheme and the Bradfield Scheme to divert northern rivers inland. In 2020, she urged the "
        "federal government to bypass environmental regulations to fast-track these dams and water projects, framing them as "
        "essential for regional survival and drought-proofing."
    ),
    "Cause.Where.Effect": (
        "In her election campaigns (notably in 2016 and 2019), Hanson has nostalgically evoked the \"1950s suburb\" where "
        "doors could be left unlocked and children played safely. She uses this nostalgic imagery to campaign against "
        "high-density housing, urban consolidation, and the rapid population growth driven by immigration, claiming that urban "
        "development is destroying the Australian way of life."
    ),
    "Cause.Why.Who": (
        "Hanson has been a pioneer of hardline border security, advocating for offshore processing and mandatory detention "
        "since 1996. She strongly supported the Howard government's Pacific Solution in 2001 and subsequent sovereign borders "
        "policies under Abbott and Morrison. Her Senate voting record shows consistent support for offshore detention facilities "
        "on Manus Island and Nauru, framing it as a vital deterrent."
    ),
    "Cause.Why.What": (
        "Hanson’s public speeches frequently celebrate the \"pioneer spirit\" that cleared and farmed the Australian bush. "
        "In debates on Australia Day and history curriculum (2018–2021), she rejected critical histories of British colonization, "
        "arguing that settlers did not commit genocide but instead worked under extreme hardship to build a civilized, "
        "productive nation out of a wilderness."
    ),
    "Cause.Why.Where": (
        "Hanson's 1996 maiden speech famously warned that Australia was \"in danger of being swamped by Asians.\" She leveraged "
        "geographical isolation to argue for a closed-door immigration policy, suggesting that high immigration would lead "
        "to the destruction of Australian culture. Her rhetoric continues to play on this geographic and cultural vulnerability, "
        "targeting Asian and Muslim migration patterns."
    ),
    "Cause.Why.Why": (
        "Hanson has consistently attacked targeted government assistance for Indigenous Australians and multicultural "
        "organizations, arguing it violates the principle of a \"fair go for all.\" In her 1996 maiden speech and 2016 "
        "Senate return, she campaigned to abolish ATSIC and targeted Indigenous welfare programs, claiming they create "
        "a system of racial separatism where mainstream Australians are treated as second-class."
    ),
    "Cause.Why.How": (
        "While Hanson frequently invokes the term \"mateship\" to describe her base, her actual policy platform is highly "
        "exclusionary. In her 2016 Senate speech and subsequent anti-halal and anti-mosque campaigns, she defined mateship "
        "as a bond exclusive to \"mainstream\" Australians who share a common Judeo-Christian heritage, explicitly "
        "excluding non-assimilating multicultural groups from this national contract."
    ),
    "Cause.Why.Cause": (
        "Hanson has repeatedly warned that Australia's low population and vast landmass make it vulnerable to foreign takeover, "
        "particularly by China. Throughout the 2010s and 2020s, she campaigned against foreign ownership of Australian "
        "infrastructure, ports (such as the Port of Darwin lease), and agricultural land, arguing that selling national "
        "assets compromises national sovereignty and security."
    ),
    "Cause.Why.Effect": (
        "Hanson's energy policies are built on preserving Australia's reliance on raw coal and gas extraction. She has "
        "consistently opposed the transition to renewable energy, claiming in Senate debates (2020–2025) that climate change "
        "is a hoax and that phasing out fossil fuels is economic suicide. Her policies advocate for cheap, unearned resource "
        "extraction to maintain high standards of living."
    ),
    "Cause.How.Who": (
        "Hanson has long positioned herself as a champion of \"common sense\" over \"expert\" consensus, frequently questioning "
        "scientific findings on climate change, Great Barrier Reef health, and public health policies. During the COVID-19 "
        "pandemic (2020–2022), she opposed vaccine mandates and lockdowns, arguing that everyday Australians should rely "
        "on their own judgment and personal choice."
    ),
    "Cause.How.What": (
        "Hanson’s One Nation party has consistently voted to limit the powers of trade unions and collective bargaining. "
        "She voted in favor of the Coalition's Australian Building and Construction Commission (ABCC) restoration in 2016, "
        "aligning herself with employer associations against organized labor. Her populist narrative focuses on the small-business "
        "owner rather than the collective action of unionized workers."
    ),
    "Cause.How.Where": (
        "Hanson frequently visits regional farming areas to praise the self-reliance and resourcefulness of rural Australians. "
        "During the 2019-2020 bushfires and subsequent floods, she highlighted community-led recovery efforts while attacking "
        "government disaster management bureaucracies, arguing that local, practical knowledge is far superior to centralized "
        "government interventions."
    ),
    "Cause.How.Why": (
        "Hanson has expressed deep suspicion of modern electoral reforms, including electronic voting and changes to Senate "
        "voting systems. In 2016, she opposed Coalition changes to Senate voting preferences, claiming they were designed "
        "to wipe out minor parties. She has consistently campaigned to keep paper balloting and manual counting to prevent "
        "electoral fraud and ensure democratic transparency."
    ),
    "Cause.How.How": (
        "Hanson's small-business policy platform has consistently advocated for deregulating the labor market, including "
        "reducing penalty rates for retail and hospitality workers. In 2017, she supported the Fair Work Commission's "
        "decision to cut Sunday penalty rates, arguing that centralized award systems place an unfair burden on small family "
        "businesses and restrict employment growth."
    ),
    "Cause.How.Cause": (
        "As a staunch supporter of constitutional monarchism, Hanson campaigned actively against a republic during the 1999 "
        "referendum and continues to defend the role of the Governor-General. She argues that the Crown's representative "
        "provides an essential, non-partisan check on parliamentary power, preventing political parties from consolidating "
        "absolute power or destabilizing the nation."
    ),
    "Cause.How.Effect": (
        "Hanson has been a key political voice in Australians for Constitutional Monarchy campaigns, repeatedly opposing a "
        "referendum to replace the British Monarch with an Australian President. In 2022, following the death of Queen Elizabeth "
        "II, she condemned calls for a republic, asserting that the British Crown remains the ultimate symbol of Australia's "
        "democratic stability and legal continuity."
    ),
    "Cause.Cause.Who": (
        "Hanson entered federal politics in 1996 on a platform that strongly opposed the High Court's Native Title decisions "
        "(Mabo and Wik). She argued that native title creates \"two classes of citizens\" and campaigned to overturn the Native "
        "Title Act 1993, claiming that the legislation threatens agricultural investments, mining projects, and private property rights."
    ),
    "Cause.Cause.What": (
        "Hanson's legislative output has consistently ignored environmental conservation in favor of resource extraction. "
        "She has repeatedly voted against expanding national parks or marine reserves, arguing that restricting access to "
        "public lands locks up valuable mineral and timber resources. Her rhetoric treats the Australian continent as an economic asset."
    ),
    "Cause.Cause.Where": (
        "In 2019, Hanson led a high-profile Senate delegation to the Great Barrier Reef, where she went snorkeling and claimed "
        "the reef was in \"pristine condition\" and not threatened by climate change. She accused marine scientists of fabricating "
        "coral bleaching data to secure government research funding, calling it a conspiracy to destroy regional industries."
    ),
    "Cause.Cause.Why": (
        "Hanson has consistently dismissed warnings about human-caused ecological collapse, voting against the Climate Change "
        "Act 2022 and targets for net-zero emissions. In parliamentary debates, she argues that climate cycles are entirely natural "
        "and that restrictions on land clearing or carbon emissions are unnecessary interventions that damage rural economies."
    ),
    "Cause.Cause.How": (
        "During and after the 2019-2020 Black Summer bushfires, Hanson dismissed calls to integrate traditional Indigenous fire-stick "
        "farming techniques into national land management. She instead blamed the severity of the fires on the failure of state "
        "governments to conduct fuel reduction burns and allow logging in national parks, rejecting pre-colonial practices."
    ),
    "Cause.Cause.Cause": (
        "Hanson’s economic policies rest on the assumption of infinite mineral extraction. In debates regarding coal, iron ore, "
        "and gas exports, she has consistently opposed environmental regulations that limit mining expansion. She rejects the concept "
        "of ecological carrying capacity, arguing that Australia should maximize resource exploitation to fund development."
    ),
    "Cause.Cause.Effect": (
        "Hanson has supported proposals to establish a national nuclear waste repository in remote parts of South Australia and "
        "the Northern Territory. She has also advocated for uranium mining and nuclear power in Australia, arguing that the "
        "continent's geologically stable, arid interior is the ideal location for storing hazardous industrial waste."
    ),
    "Cause.Effect.Who": (
        "Hanson’s public speeches and social media campaigns consistently elevate ANZAC Day as the core of Australian national identity. "
        "She has repeatedly introduced motions in the Senate to protect military legacy and veterans' services, arguing that the "
        "military virtues of courage, sacrifice, and loyalty are the true source of national unity."
    ),
    "Cause.Effect.What": (
        "Hanson has consistently voted against motions seeking to recognize First Nations resistance fighters or the Frontier Wars "
        "in the Australian War Memorial. In 2021, she argued that the War Memorial should focus exclusively on official military "
        "deployments overseas, rejecting the historical reality of armed conflict between settlers and Indigenous Australians."
    ),
    "Cause.Effect.Where": (
        "Hanson has campaigned strongly against foreign investment in residential real estate, claiming in Senate debates (2018–2022) "
        "that foreign buyers (particularly from China) are pricing young Australians out of the housing market. She advocates for "
        "restricting home ownership to citizens and permanent residents to protect the suburban dream."
    ),
    "Cause.Effect.Why": (
        "Hanson has consistently voted for stricter welfare compliance measures, including the Cashless Debit Card scheme for "
        "regional communities, which she strongly defended in 2020. She has campaigned to restrict access to welfare for newly "
        "arrived immigrants, proposing a five-year waiting period before migrants can access Centrelink payments."
    ),
    "Cause.Effect.How": (
        "Throughout her political career, Hanson has rejected bipartisan consensus, building her brand on polarization and controversy. "
        "From her 1996 maiden speech to her 2022 walkouts, she has positioned herself as a disruptor of political consensus, arguing "
        "that compromise between major parties is a betrayal of the voter."
    ),
    "Cause.Effect.Cause": (
        "Hanson has campaigned vigorously against any proposal for a Treaty with Indigenous Australians or the establishment of a "
        "Truth-Telling Commission. During the 2023 referendum on the Voice, she argued that a treaty would split the nation into two "
        "states and create a permanent racial division, actively working to keep the foundational issues of sovereignty unresolved."
    ),
    "Cause.Effect.Effect": (
        "Hanson has led Senate campaigns against the national curriculum, introducing motions in 2020 and 2021 to audit school "
        "history textbooks for \"left-wing bias.\" She opposes the teaching of systemic racism or colonial massacres, arguing that "
        "the curriculum should focus on the achievements of British settlement and development to build national pride."
    )
}

# Load the original vectors
with open('plane_6_temp_dump.json', 'r', encoding='utf-8') as f:
    vectors = json.load(f)

# Update each vector's actuality and keep only specified keys
remediated_vectors = []
for v in vectors:
    addr = v['address']
    if addr in actualities:
        new_act = actualities[addr]
    else:
        new_act = v['actuality'] # fallback (should not be reached)
    
    # Ensure coordinates are floats
    coords = v['coordinates']
    formatted_coords = {
        "v": float(coords['v']),
        "psi": float(coords['psi'])
    }
    
    # Construct clean vector dictionary with only requested keys
    cleaned_v = {
        "address": v['address'],
        "name": v['name'],
        "coordinates": formatted_coords,
        "verdict": v['verdict'],
        "quote": v['quote'],
        "description": v['description'],
        "justification": v['justification'],
        "actuality": new_act
    }
    remediated_vectors.append(cleaned_v)

# Write to output file
out_path = 'e:/Vector Field Theory/VFT Docs/_VFT MD/io/Hanson_Audit_AI_Logs/remediated_plane_6.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(remediated_vectors, f, indent=2, ensure_ascii=False)

print("Remediation complete. Output written to:", out_path)
