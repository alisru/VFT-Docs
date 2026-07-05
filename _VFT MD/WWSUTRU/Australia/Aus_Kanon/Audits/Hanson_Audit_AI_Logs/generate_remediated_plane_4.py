import json
from pathlib import Path

audit_path = Path("e:/Vector Field Theory/VFT Docs/_VFT MD/io/Hegemonic Audit_ Pauline Hanson.json")
output_path = Path("e:/Vector Field Theory/VFT Docs/_VFT MD/io/Hanson_Audit_AI_Logs/remediated_plane_4.json")

with open(audit_path, 'r', encoding='utf-8') as f:
    audit_data = json.load(f)

plane_4 = next(p for p in audit_data['planes'] if p['plane_num'] == 4)
vectors = plane_4['vectors']

actualities_map = {
    ("Why.Who.Who", "The Volunteer"): (
        "During the 2019-20 Black Summer bushfires, Hanson repeatedly rejected community-led fundraising and voluntary relief efforts as a substitute for government action, criticizing Prime Minister Scott Morrison's reliance on unpaid volunteer firefighters. In her media statements, she argued that the state was abdicating its duty by relying on the charity of citizens, thereby shifting focus from civic volunteerism to top-down government resources."
    ),
    ("Why.Who.What", "The Bludger"): (
        "In her September 10, 1996 Maiden Speech, Hanson explicitly attacked the welfare state, introducing the term 'welfare cheats and dole bludgers' into modern Australian political debate. Throughout her career, she has voted for bills enforcing mutual obligations, such as supporting the Cashless Debit Card trials in 2016 and the Social Services Legislation Amendment (Drug Testing Trial) Bill in 2018, actively seeking to restrict benefits to those who work."
    ),
    ("Why.Who.Where", "The Knocker"): (
        "Hanson's political record is characterized by persistent attacks on intellectual elites, academics, and experts. In her public campaigns, she criticized medical experts regarding vaccination policies in 2017, and in 2019, she aggressively targeted the Family Court judiciary, calling for its abolition in favor of a community-led tribunal. This narrative actively positions regional and suburban common sense against metropolitan authority."
    ),
    ("Why.Who.Why", "The Digger"): (
        "Hanson consistently frames her political longevity and personal hardships—including her 2003 conviction and subsequent acquittal, and her multiple electoral losses between 1998 and 2016—as a form of stoic, nationalistic endurance. Upon her return to the Senate in 2016, she repeatedly claimed that she had survived the establishment's attempts to silence her, using her resilience to build moral authority."
    ),
    ("Why.Who.How", "The Gambler"): (
        "Hanson opposes market-driven economic changes and speculative environmental schemes, voting consistently to protect traditional sectors like coal mining and manufacturing. She voted against the Clean Energy Act 2011 and has repeatedly called for the construction of new coal-fired power stations, rejecting carbon pricing and renewable energy targets as dangerous gambles with the nation's economic security."
    ),
    ("Why.Who.Cause", "The Battler"): (
        "Hanson's entire political brand is built on the 'battler' archetype, starting with her 1996 Maiden Speech declaration as a 'fish and chip shop lady.' During the COVID-19 pandemic in 2020 and 2021, she actively campaigned against lockdowns and restrictions, framing them as direct assaults on small business owners and regional workers who represent the moral heart of the country."
    ),
    ("Why.Who.Effect", "The Larrikin"): (
        "Hanson relies on disruptive stunts and anti-establishment humor to subvert parliamentary norms, exemplified by her famous 1996 'Please explain?' catchphrase. Her most controversial stunt occurred in August 2017 when she wore a full burqa into the Senate chamber to protest Islamic dress, drawing widespread media attention and demonstrating her use of larrikin-style provocation to mock political correctness."
    ),
    ("Why.What.Who", "The Fair Go"): (
        "Hanson has consistently worked to restrict the 'Fair Go' to a culturally defined ingroup by opposing the allocation of resources to immigrants and refugees. In 2018, she moved a controversial Senate motion asserting 'It's OK to be white,' and she has consistently voted to cut welfare access for newly arrived migrants and restrict the rights of asylum seekers to protect local workers."
    ),
    ("Why.What.What", "The Weekend"): (
        "In 2017, Hanson and One Nation senators voted in support of the Fair Work Commission's decision to cut Sunday and public holiday penalty rates for retail and hospitality workers. Hanson defended the decision in parliamentary debate, arguing that penalty rates were an unsustainable burden on small businesses, thereby prioritizing employer profitability over the traditional Australian weekend."
    ),
    ("Why.What.Where", "The Home"): (
        "Hanson has actively campaigned against the foreign acquisition of Australian residential property and agricultural land, framing it as an invasion of local sovereignty. In 2019 and 2020, she introduced private senator's bills to restrict foreign buyers from purchasing residential real estate, arguing that local ownership of the suburban home is a sacred right that must be preserved."
    ),
    ("Why.What.Why", "The Holiday"): (
        "Hanson's political messaging is built on a permanent state of national emergency, rejecting recreational leisure in favor of constant vigilance. Her campaign schedules and public communications emphasize that Australia is under immediate threat from immigration, Islamic influence, and globalist treaties, leaving no room for the traditional cultural reset of the holiday."
    ),
    ("Why.What.How", "The Ute"): (
        "During the 2019 and 2022 federal election campaigns, Hanson heavily targeted EV policies, framing electric vehicles as impractical luxury items pushed by urban elites. She actively championed traditional diesel-powered utility vehicles (utes) as the only practical tool for regional workers and farmers, turning a vehicle type into a symbol of working-class defiance."
    ),
    ("Why.What.Cause", "The Pay Packet"): (
        "Hanson has consistently campaigned against the importation of cheap foreign labor, arguing that it undermines the wages of local workers. Upon her return to the Senate in 2016, she demanded strict labor market testing and voted to restrict temporary work visas, such as the former 457 visa, to artificially protect the pay packets of mainstream Australian workers."
    ),
    ("Why.What.Effect", "The Pension"): (
        "Hanson has consistently opposed foreign aid budgets, introducing motions in the Senate in 2017 and 2020 to divert foreign aid funding directly to Australian age pensioners and veterans. Her rhetoric frames the age pension as a sacred, earned contract between the citizen and the state that must be protected from budget cuts, especially when compared to international spending."
    ),
    ("Why.Where.Who", "The Pub"): (
        "Hanson actively conducts regional tours, such as her One Nation 'Battler Bus' campaigns in regional Queensland during the 2016, 2017, and 2020 elections, where she holds public forums in local pubs. She uses the 'front bar' as the primary arena to validate her political platform, claiming that pub conversations represent the authentic voice of the people, bypass media filters, and test policy legitimacy."
    ),
    ("Why.Where.What", "The Beach"): (
        "Hanson has repeatedly used the beach as a cultural symbol to campaign against multiculturalism and integration. In public statements during the 2017 debates on integration, she vocally opposed the introduction of burkinis in public pools and surf lifesaving clubs, arguing that the traditional, open Australian beach culture must remain free from foreign religious modesty codes."
    ),
    ("Why.Where.Where", "Country"): (
        "Hanson has consistently opposed First Nations land rights and native title legislation throughout her career. She vocally opposed the Mabo decision in her 1996 Maiden Speech, campaigned against the handback of Uluru in 1999, and argued in the Senate during debates in 2022 that native title creates division rather than unity, treating the continent purely as a secular, unified resource."
    ),
    ("Why.Where.Why", "The Club"): (
        "Hanson frequently uses regional RSLs and community sports clubs as the primary staging grounds for her town hall meetings and regional campaigns. In 2019, she publicly opposed tax increases and regulations that threatened the financial viability of these clubs, arguing that their combination of cheap meals, war memorials, and gaming revenue is essential for suburban social cohesion."
    ),
    ("Why.Where.How", "The Shed"): (
        "Hanson has consistently supported funding and recognition for the Australian Men's Shed Association and local community sheds, praising them as vital spaces for practical learning and mental health support. Her rhetoric celebrates the backyard shed as the true site of hands-on intelligence and self-reliance, contrasting it with the uselessness of academic and political debate."
    ),
    ("Why.Where.Cause", "The Field"): (
        "Hanson frequently uses sporting metaphors in her political campaigns and aligns herself with Queensland rugby league culture to project national pride. In 2019, she publicly defended rugby player Israel Folau's right to voice conservative religious opinions, mapping the sports field's competitive spirit onto her broader defense of traditional free speech and national identity."
    ),
    ("Why.Where.Effect", "The Mall"): (
        "Hanson has repeatedly targeted large supermarket chains like Coles and Woolworths, calling for a Royal Commission into supermarket pricing and supporting legislation to limit their market share. Her rhetoric opposes the consolidation of retail capital by multinational malls, attempting to protect small, family-owned local businesses in regional communities."
    ),
    ("Why.Why.Who", "Mateship"): (
        "Hanson restricts the application of mateship by asserting that it cannot extend to immigrants who do not fully assimilate. In her 2016 Senate Maiden Speech and subsequent policy statements, she argued that mutual solidarity is a conditional contract reserved only for those who respect traditional Australian laws and cultural norms, excluding advocates of multiculturalism."
    ),
    ("Why.Why.What", "Tall Poppy Syndrome"): (
        "Hanson has consistently attacked high-profile corporate leaders and institutions that engage in progressive social advocacy, notably calling for funding cuts to the Australian Broadcasting Corporation (ABC). Her campaigns against corporate activism, such as her criticism of Qantas CEO Alan Joyce in 2017, demonstrate her active use of tall poppy cutting to neutralize cultural elites."
    ),
    ("Why.Why.Where", "Cultural Cringe"): (
        "Hanson has consistently opposed Australia's integration into global frameworks, campaigning against treaties like the UN Global Compact on Migration in 2018. Her speeches reject international legal standards and foreign court decisions, framing any reliance on global bodies as a form of cultural weakness and an abdication of national independent authority."
    ),
    ("Why.Why.Why", "She'll Be Right"): (
        "Hanson actively campaigns against apathetic optimism, using warnings of impending national ruin to mobilize voters. On issues like foreign ownership of agricultural land and water rights in the Murray-Darling Basin, she has introduced private senator's bills warning of systemic economic collapse, explicitly rejecting the comforting 'she'll be right' attitude."
    ),
    ("Why.Why.How", "Have a Go"): (
        "Despite losing her seat in 1998 and failing in multiple state and federal elections over the next 18 years, Hanson persisted until her return to the Senate in 2016. Her political narrative leverages this history of perseverance to claim the 'Have a Go' ethos, framing her campaign as a courageous, amateur effort against the political establishment."
    ),
    ("Why.Why.Cause", "Fear of Missing Out"): (
        "Hanson strongly rejects the global anxiety of being left behind, voting against international climate treaties and emissions targets. She opposed the signing of the Paris Agreement and has consistently argued in Senate debates that Australia should not sacrifice its traditional industries purely to match international consensus or avoid diplomatic isolation."
    ),
    ("Why.Why.Effect", "The Good Life"): (
        "Hanson's platform rejects comfortable, passive hedonism when the nation is perceived to be in danger. She campaigns on a platform of border security and cultural preservation, arguing that the material comforts of the 'Good Life' are temporary illusions unless the country's borders are strictly defended."
    ),
    ("Why.How.Who", "Shouting"): (
        "Hanson opposes foreign aid and international contributions. She has consistently voted to cut Australia's foreign aid budget, arguing in the Senate that sending taxpayer dollars overseas is equivalent to 'shouting' foreign nations while regional Australians go without basic services."
    ),
    ("Why.How.What", "Sledging"): (
        "Hanson uses aggressive personal attacks and parliamentary insults (sledging) to disrupt opponents. Most recently, on November 24-25, 2025, her verbal attacks in the Senate led to her suspension from the chamber, demonstrating her ongoing use of tactical abuse to undermine political adversaries."
    ),
    ("Why.How.Where", "Queuing"): (
        "Hanson has consistently used the 'queue-jumper' label to describe asylum seekers arriving by boat. She supported the migration amendment bills in 2016 and 2018 that enforced lifetime bans on visas for boat arrivals, arguing that maintaining the integrity of the orderly queue is a matter of basic fairness."
    ),
    ("Why.How.Why", "Striking"): (
        "Hanson and One Nation senators supported the Coalition's Ensuring Integrity Bill in 2019, which sought to make it easier to deregister unions and ban officials, arguing that union strikes damage small businesses and disrupt the national economy."
    ),
    ("Why.How.How", "Improvising"): (
        "Hanson's One Nation party operates as a highly centralized yet structurally makeshift grassroots campaign. She relies on social media videos, direct regional tours in the One Nation 'Battler Bus,' and volunteer-led local campaigns rather than high-cost advertising agencies to secure electoral support."
    ),
    ("Why.How.Cause", "Gambling"): (
        "Hanson has consistently opposed federal intervention to reform the gambling industry or restrict poker machines (pokies), voting against mandatory pre-commitment trials and arguing that gaming revenue is essential for funding community services and sporting clubs."
    ),
    ("Why.How.Effect", "Volunteering"): (
        "During regional floods in 2022, Hanson focused her public commentary on government planning failures and infrastructure neglect, arguing that reliance on voluntary organizations like the SES and local communities was an abdication of government duty rather than a model for civic action."
    ),
    ("Why.Cause.Who", "The Stain"): (
        "Hanson has consistently opposed public gestures of historical guilt, such as changing the date of Australia Day. In 2018, she led a campaign in the Senate to reject national apologies and historical revisionism, arguing that Australians should not feel shame for the actions of early British settlers."
    ),
    ("Why.Cause.Who", "Guilt [First Nations Perspective]"): (
        "Hanson has repeatedly denied key aspects of First Nations historical trauma. In 2017, she stated in the Senate that there was no 'Stolen Generation' and actively campaigned against the Uluru Statement from the Heart and the 2023 Indigenous Voice to Parliament referendum, denying the need for structural reckoning."
    ),
    ("Why.Cause.What", "The Gold"): (
        "Hanson is a fierce defender of the resources sector, opposing the Minerals Resource Rent Tax (MRRT) in 2012 and repeatedly calling for the approval of new coal and gas projects, such as the Adani Carmichael mine in Queensland, to secure national prosperity."
    ),
    ("Why.Cause.Where", "The Bush"): (
        "Hanson routinely contrasts the moral character of regional Australians with metropolitan residents. She has campaigned heavily on agricultural water rights, regional infrastructure, and drought assistance, framing the rural lifestyle as the authentic heart of the national character."
    ),
    ("Why.Cause.Where", "Abundance [First Nations Perspective]"): (
        "Hanson's agricultural policies demand high-impact land clearing and water diversion, such as her support for the Bradfield Scheme to divert northern rivers. She rejects First Nations fire management and ecological conservation strategies, treating the natural landscape as an under-utilized resource."
    ),
    ("Why.Cause.Why", "The War"): (
        "Hanson has consistently used the Anzac legend to defend the Australian flag and traditional national holidays. In 2018, she introduced motions to penalize the desecration of the flag and has campaigned against changing the date of Australia Day, citing military sacrifice."
    ),
    ("Why.Cause.Why", "Resistance [First Nations Perspective]"): (
        "Hanson has actively denied the existence of pre-colonial warfare and frontier resistance. In Senate debates and public interviews (including on Sky News in 2021), she has rejected the term 'invasion' to describe British settlement, arguing that the colonizers encountered no organized national resistance."
    ),
    ("Why.Cause.How", "The Depression"): (
        "Hanson frequently references the economic vulnerability of the working class, citing manufacturing job losses in regions like Geelong and Adelaide. She has supported protectionist tariffs and opposed free trade agreements (like the Peru-Australia Free Trade Agreement in 2018) to prevent a slide into economic depression."
    ),
    ("Why.Cause.Cause", "The Isolation"): (
        "Hanson has consistently advocated for defense self-reliance, supporting increased spending on domestic defense manufacturing. During the COVID-19 pandemic in 2020, she argued that Australia's geographic isolation required the repatriation of critical manufacturing to secure the country against global supply disruptions."
    ),
    ("Why.Cause.Effect", "The Boom"): (
        "Hanson's economic policy revolves around supporting commodity booms. She has opposed carbon taxes and mining taxes, arguing that Australia's economic stability depends entirely on unrestricted exports of coal, gas, and agricultural products to Asian markets."
    ),
    ("Why.Effect.Who", "The Citizen"): (
        "Hanson's electoral strategy relies on capturing the votes of disaffected citizens who are legally compelled to vote. She has consistently defended compulsory voting as a democratic safeguard, using it to mobilize the 'silent majority' who do not normally engage in political activism."
    ),
    ("Why.Effect.What", "The Middle Class"): (
        "Hanson's tax policy focuses on supporting suburban middle-class families. In 2019, she supported the Coalition's personal income tax cuts, arguing that middle-income earners bear the highest tax burden and deserve structural relief to maintain their standard of living."
    ),
    ("Why.Effect.Where", "The Suburb"): (
        "Hanson has campaigned against high-density urban planning and high immigration rates, arguing they lead to congestion in outer-suburban areas. She has consistently supported policies to protect low-density suburban zoning and regional development to maintain private suburban spaces."
    ),
    ("Why.Effect.Why", "Stability"): (
        "Hanson's parliamentary behavior is highly disruptive, regularly using stunts (like wearing a burqa or walking out of the Senate during the Acknowledgement of Country in 2022) to challenge conventions. She opposes major party consensus and acts as a destabilizing force on the crossbench."
    ),
    ("Why.Effect.How", "Cynicism"): (
        "Hanson's political messaging has consistently promoted skepticism of the major parties since 1996. She positions One Nation as a watchdog to 'keep the bastards honest,' tapping into deep voter cynicism toward mainstream political institutions and career politicians."
    ),
    ("Why.Effect.Cause", "Prosperity"): (
        "Hanson has consistently opposed the sale of Australian assets and agricultural land to foreign buyers. In 2019, she called for tighter restrictions on foreign investment, arguing that Australia's resource-driven prosperity should be preserved for native-born citizens."
    ),
    ("Why.Effect.Effect", "Sovereignty"): (
        "Hanson has campaigned aggressively against international agreements that impact Australian domestic laws. In 2018, she successfully pressured the Coalition government to reject the UN Global Compact on Migration, arguing it compromised Australia's national sovereignty over border protection."
    ),
}

updated_vectors = []
for v in vectors:
    key = (v['address'], v['name'])
    if key in actualities_map:
        v['actuality'] = actualities_map[key]
        updated_vectors.append(v)
    else:
        print(f"Warning: {key} not found in actualities map!")

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(updated_vectors, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {len(updated_vectors)} remediated vectors to {output_path}")
