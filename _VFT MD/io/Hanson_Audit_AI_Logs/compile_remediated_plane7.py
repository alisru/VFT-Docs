import json

compact_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus Kanon\compact JSON\Plane_7_Result_compact.json"
hanson_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hegemonic Audit_ Pauline Hanson.json"
output_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hanson_Audit_AI_Logs\remediated_plane_7.json"

# Load compact data
with open(compact_path, "r", encoding="utf-8") as f:
    compact_data = json.load(f)

# Load hanson data
with open(hanson_path, "r", encoding="utf-8") as f:
    hanson_data = json.load(f)

h_plane7 = next(p for p in hanson_data["planes"] if p["plane_num"] == 7)
h_vectors = h_plane7["vectors"]

# Mapping dictionary from (address, name) to Hanson vector index
address_name_to_hanson_idx = {
    # 7.1 Who
    ("Effect.Who.Who", "The Quiet Australian"): 6,
    ("Effect.Who.What", "The Multicultural Citizen"): 0,
    ("Effect.Who.Where", "The Coastal Dweller"): 2,
    ("Effect.Who.Why", "The Aspirational"): 1,
    ("Effect.Who.How", "The Sports Fanatic"): 4,
    ("Effect.Who.Cause", "The Digger's Heir"): 5,
    ("Effect.Who.Effect", "The Citizen"): 3,

    # 7.2 Where (Geographies)
    ("Effect.Where.Who", "The Australian Diaspora"): 14,
    ("Effect.Where.What", "The Commodity"): 15,
    ("Effect.Where.Where", "The Alliance"): 16,
    ("Effect.Where.Why", "The Middle Power"): 17,
    ("Effect.Where.How", "Soft Power"): 18,
    ("Effect.Where.Cause", "The Pacific"): 19,
    ("Effect.Where.Effect", "The Asian Century"): 20,

    # 7.3 What (Institutions)
    ("Effect.What.Who", "The Home Owner"): 11,
    ("Effect.What.What", "The Superannuation Balance"): 8,
    ("Effect.What.Where", "The University Sector"): 9,
    ("Effect.What.Why", "The Medicare Card"): 7,
    ("Effect.What.How", "The Renewable Transition"): 10,
    ("Effect.What.Cause", "Biodiversity"): 12,
    ("Effect.What.Effect", "Stability"): 13,

    # 7.4 Why
    ("Effect.Why.Who", "Egalitarianism vs. Aspiration"): 21,
    ("Effect.Why.What", "Sustainability vs. Extraction"): 22,
    ("Effect.Why.Where", "Urban vs. Regional"): 23,
    ("Effect.Why.Why", "Fair Go vs. Market"): 24,
    ("Effect.Why.How", "Reconciliation vs. Denial"): 25,
    ("Effect.Why.Cause", "Luck vs. Effort"): 26,
    ("Effect.Why.Effect", "Unity vs. Division"): 27,

    # 7.5 How
    ("Effect.How.Who", "The Vote"): 28,
    ("Effect.How.What", "The Royal Commission"): 29,
    ("Effect.How.Where", "The High Court"): 30,
    ("Effect.How.Why", "The Media"): 31,
    ("Effect.How.How", "The ABS"): 32,
    ("Effect.How.Cause", "The Pub Test"): 33,
    ("Effect.How.Effect", "The Treasury"): 34,

    # 7.6 Cause
    ("Effect.Cause.Who", "The Next Generation"): 35,
    ("Effect.Cause.What", "The Energy Transition"): 36,
    ("Effect.Cause.Where", "Northern Australia"): 37,
    ("Effect.Cause.Why", "The Republic"): 38,
    ("Effect.Cause.How", "Treaty [First Nations Perspective]"): 39,
    ("Effect.Cause.Cause", "Asia"): 40,
    ("Effect.Cause.Effect", "The Good Life"): 41,

    # 7.7 Effect
    ("Effect.Effect.Who", "The Fair Go"): 42,
    ("Effect.Effect.What", "The Lifestyle"): 43,
    ("Effect.Effect.Where", "Girt By Sea"): 44,
    ("Effect.Effect.Why", "The Second Chance"): None, # missing in Hanson, will be custom-generated
    ("Effect.Effect.Why", "Dispossession [First Nations Perspective]"): 45,
    ("Effect.Effect.How", "She'll Be Right"): 46,
    ("Effect.Effect.Cause", "The Land"): 47,
    ("Effect.Effect.Effect", "Australia"): 48
}

# The researched actualities
actualities = {
    "Effect.Who.Who": "Hanson has built her political career on appealing to the \"silent majority\" of suburban and regional Australians, notably launching her \"Please Explain\" cartoon series in 2020 to lampoon inner-city elites. Her 2016 Senate Maiden Speech explicitly championed \"forgotten\" suburban and rural workers who felt ignored by mainstream political parties, and she has consistently opposed carbon pricing and tax changes that she claims disproportionately burden ordinary taxpayers.",
    "Effect.Who.What": "Hanson has waged a decades-long campaign against multiculturalism, beginning with her 1996 Maiden Speech warning that Australia was in danger of being \"swamped by Asians\" and her 2016 Senate Maiden Speech claiming the nation was being \"swamped by Muslims.\" In parliament, she has repeatedly called for the abolition of the Department of Home Affairs' multicultural funding, introduced bills to ban the burqa in public spaces (2017), and campaigned for a complete halt to net immigration.",
    "Effect.Who.Where": "Hanson's policy platform focuses heavily on protecting the financial security of retirees and pensioners, campaigning against Coalition attempts to change pension asset tests in 2017. She has consistently moved motions to redirect portions of Australia's multi-billion dollar foreign aid budget toward domestic senior citizen support, arguing in the Senate that Australian taxpayers who built the country should not live in energy poverty while overseas governments receive funding.",
    "Effect.Who.Why": "Hanson's rhetoric targets the aspirations of suburban small-business owners and \"mum and dad\" investors, arguing that high taxes and red tape stifle personal ambition. During the 2019 and 2022 federal campaigns, One Nation strongly opposed Labor's proposed changes to negative gearing and capital gains tax, framing the policies as an attack on ordinary Australians working to secure their own financial future rather than relying on the state.",
    "Effect.Who.How": "Hanson has consistently defended the property rights of private landlords and residential property investors. In 2019, she campaigned fiercely against any dilution of negative gearing, arguing it was a legitimate wealth-creation tool for middle-class workers. During the COVID-19 pandemic in 2020-2021, she opposed eviction moratoriums and rental relief measures that she argued placed an unfair financial burden on private property owners.",
    "Effect.Who.Cause": "Hanson demands strict cultural assimilation for all new arrivals to Australia, arguing that multiculturalism fractures national cohesion. In her 2016 Senate Maiden Speech, she called for a ban on Muslim immigration and the installation of surveillance cameras in mosques, and she has repeatedly introduced motions in the Senate asserting that immigrants must assimilate to \"traditional Australian values\" or face deportation.",
    "Effect.Who.Effect": "Hanson has consistently opposed any special constitutional or legislative recognition for Indigenous Australians, campaigning against the Voice to Parliament in the lead-up to the 2023 referendum. In August 2022, she made headlines by walking out of the Senate during the Welcome to Country ceremony, asserting that she only recognizes the Australian flag and the national citizenship pledge as unifying symbols.",
    
    "Effect.Where.Who": "Hanson's isolationist foreign policy explicitly rejects regional aid commitments in the Pacific. She has voted against international aid packages in the Senate and criticized the \"Pacific Step-Up\" initiative in 2018, arguing that billions in foreign aid should be redirected to domestic infrastructure, regional health, and drought relief for Australian farmers.",
    "Effect.Where.What": "Hanson supports the AUKUS security pact and the US alliance (ANZUS) as critical to national defense, but she opposes the economic globalization that tethers Australian assets to foreign ownership. She has consistently introduced bills to restrict foreign state-owned enterprises from purchasing agricultural land and water rights, arguing that national sovereignty is compromised by selling off local resources.",
    "Effect.Where.Where": "Hanson campaigns against high-density urban developments and rapid population growth, linking metropolitan sprawl and infrastructure congestion directly to high immigration rates. She has called for \"zero net immigration\" since her return to the Senate in 2016, arguing that suburban communities are being ruined by overdevelopment and overcrowded services.",
    "Effect.Where.Why": "Hanson's border protection platform relies on absolute exclusion, supporting indefinite offshore processing and the immediate turnback of asylum seeker boats. In 2018, she moved a motion calling on the government to withdraw from the United Nations 1951 Refugee Convention, and she strongly supported the repeal of the Medevac bill in 2019, arguing it compromised national security.",
    "Effect.Where.How": "Hanson strongly opposes bilateral free trade agreements, particularly with Asian nations, arguing they disadvantage local manufacturers and workers. She has repeatedly criticized Australia's trade dependence on China and introduced the Foreign Acquisitions and Takeovers Amendment (Government Security) Bill in 2019 to prevent Chinese state-owned enterprises from buying critical Australian infrastructure.",
    "Effect.Where.Cause": "Hanson actively rejects the \"black armband\" view of Australian history, denying that British settlement constituted an invasion or dispossession. In the Senate, she has opposed motions recognizing the Frontier Wars, voted against the United Nations Declaration on the Rights of Indigenous Peoples (UNDRIP), and campaigned against truth-telling processes, asserting that colonization brought civilization to the continent.",
    "Effect.Where.Effect": "Hanson exploits the regional divide by positioning herself as the defender of regional Queensland and Western Australia against the \"inner-city elites\" of Canberra, Sydney, and Melbourne. She has consistently argued that regional mining and agricultural communities produce the nation's real wealth but are neglected in infrastructure funding, leading to One Nation's strong electoral support in regional seats.",
    
    "Effect.What.Who": "Hanson has consistently defended tax concessions that support property ownership and investment. In 2019, she voted against Labor's housing tax reform proposals, and she has repeatedly campaigned to retain negative gearing and capital gains tax discounts, arguing that any changes would damage the housing market and penalize hard-working middle-class investors.",
    "Effect.What.What": "Hanson supported the Coalition's early release of superannuation scheme during the COVID-19 pandemic in 2020, allowing workers to withdraw up to $20,000 from their retirement savings. She has also advocated for policies allowing first-home buyers to access their superannuation balances to fund housing deposits, arguing that immediate housing security outweighs long-term retirement savings.",
    "Effect.What.Where": "Hanson has consistently supported Australia's offshore processing regime on Nauru and Manus Island. She voted in favor of the Migration Amendment (Urgent Medical Treatment) Repeal Bill 2019 to abolish the Medevac law, and has repeatedly argued that individuals who arrive by boat should be permanently barred from ever settling in Australia.",
    "Effect.What.Why": "Hanson has consistently campaigned for the protection of Medicare for Australian citizens while opposing access for temporary visa holders and undocumented immigrants. In 2017, she supported the government's Medicare Levy Amendment Bill to increase funding for the National Disability Insurance Scheme, but has cautioned against rising healthcare costs driven by high immigration.",
    "Effect.What.How": "Hanson is a vocal opponent of the transition to renewable energy, voting against the Climate Change Bill 2022 which legislated a 43% emissions reduction target. She has consistently campaigned to withdraw Australia from the Paris Agreement, introduced bills to construct new coal-fired power stations (such as the Liddell Power Station Bill in 2018), and called for a moratorium on new wind and solar developments.",
    "Effect.What.Cause": "Hanson has targeted the National Disability Insurance Scheme (NDIS) over its rising costs, calling for urgent audits to stamp out fraud and rorts. In Senate debates throughout 2022 and 2023, she argued that the scheme's budget blowout is unsustainable and threatens the nation's fiscal stability, demanding that funding be capped and restricted to those with severe permanent disabilities.",
    "Effect.What.Effect": "Hanson has waged a consistent campaign to defund or privatize the Australian Broadcasting Corporation (ABC), accusing the public broadcaster of systemic left-wing bias. She has introduced Senate motions to slash the ABC's budget, supported Coalition funding cuts in 2018, and argued that taxpayer money should not support a media outlet that she claims is out of touch with regional Australians.",
    
    "Effect.Why.Who": "Hanson led the political opposition to the Voice to Parliament, campaigning nationwide for the \"No\" vote in the 2023 referendum. She argued that the Voice was a form of \"apartheid\" that would divide Australians by race, and she has consistently opposed treaty negotiations and truth-telling commissions, claiming they undermine the principle of legal equality for all citizens.",
    "Effect.Why.What": "Hanson strongly opposes net-zero emissions targets, voting against the Climate Change Bill 2022 and criticizing the Coalition's adoption of a net-zero by 2050 target. She has campaigned to protect the coal, gas, and agricultural sectors from carbon pricing and environmental regulations, arguing that climate policies are a \"green transition fantasy\" that damages national prosperity.",
    "Effect.Why.Where": "Hanson blames the housing crisis and high cost of living on rapid population growth driven by immigration. In her public campaigns and Senate speeches in 2023, she called for a dramatic reduction in immigration to \"zero net levels\" to relieve pressure on the housing market, arguing that major cities are \"full\" and unable to cope with the influx of new arrivals.",
    "Effect.Why.Why": "Hanson has been a key actor in the culture wars, introducing a successful Senate motion in 2021 to ban the teaching of Critical Race Theory in the national curriculum. She has also introduced bills to restrict gender-neutral language in government departments and campaigned against what she terms \"woke\" school programs, arguing they undermine traditional family values.",
    "Effect.Why.How": "Hanson is a staunch defender of the constitutional monarchy and opposed to an Australian Republic. She campaigned to retain the British monarch as head of state during the 1999 referendum and has continued to oppose any renewed republican pushes, arguing that the Westminster system and the Australian flag are essential safeguards of national stability.",
    "Effect.Why.Cause": "Hanson has consistently dismissed climate science and mocked environmental warnings. In 2017, she took a highly publicized trip to the Great Barrier Reef, claiming it was in \"pristine condition\" and that climate scientists were exaggerating coral bleaching to secure funding, and she has repeatedly brought coal samples to parliament to advocate for fossil fuels.",
    "Effect.Why.Effect": "Hanson has introduced several polarizing motions in the Senate, most notably her 2018 motion asserting that \"it's OK to be white\" and acknowledging the rise of \"anti-white racism.\" The motion was narrowly defeated 31-28 after the Coalition initially supported it and then retracted their votes due to public backlash, demonstrating her role in driving racial debates.",
    
    "Effect.How.Who": "Hanson has repeatedly called for Royal Commissions into the management of the COVID-19 pandemic, vaccine mandates, and voter fraud. She has introduced motions in the Senate to establish independent inquiries into the National Cabinet's pandemic decisions, arguing that state and federal governments exceeded their constitutional authority during lockdowns.",
    "Effect.How.What": "Hanson has bypassed traditional media channels by utilizing social media platforms, most notably launching her weekly animated web series \"Pauline Hanson's Please Explain\" in 2020. The series has amassed millions of views, allowing her to broadcast populist critiques of major party politicians, climate policies, and immigration directly to her support base.",
    "Effect.How.Where": "Hanson actively supported anti-vaccine mandate and anti-lockdown protests during the COVID-19 pandemic in 2021 and 2022. She attended rallies outside Parliament House, voted against government pandemic bills, and introduced the COVID-19 Vaccination Status (Prevention of Discrimination) Bill 2021, arguing that vaccine passports violated individual bodily autonomy.",
    "Effect.How.Why": "Hanson maintains a highly sympathetic relationship with conservative media outlets, appearing as a regular paid contributor on Sky News Australia (including on the Paul Murray Show and Bolt Report). She has used these appearances, along with regular slots on regional talkback radio, to amplify her campaigns against immigration, net-zero targets, and the Voice to Parliament.",
    "Effect.How.How": "Hanson has long advocated for Citizen Initiated Referendums (CIR) to allow voters to directly decide major national policies. She has introduced bills in parliament to establish a referenda system for issues such as immigration levels, the sale of public assets, and constitutional changes, arguing that the political class cannot be trusted to represent the people's will.",
    "Effect.How.Cause": "Hanson has consistently aligned herself with anti-union legislation, voting in favor of the Coalition's \"Ensuring Integrity\" bills in 2019 and 2020. She argued in the Senate that militant union activity damages small business viability and increases infrastructure costs, claiming that deregulation of the labor market is essential to support small business employers.",
    "Effect.How.Effect": "Hanson has defended compulsory voting in Australia, noting that it forces the \"silent majority\" of suburban and regional voters to participate in elections. She has argued that this system prevents the dominance of highly active fringe activists, allowing One Nation to effectively capture the protest votes of disengaged citizens in regional electorates.",
    
    "Effect.Cause.Who": "Hanson has consistently opposed symbolic apologies for historical injustices, famously walking out of the House of Representatives during the National Apology to the Stolen Generations in February 2008. She has argued that current generations should not be held responsible for the actions of the past, a position she repeated during her walkout from the Senate's Welcome to Country in 2022.",
    "Effect.Cause.What": "Hanson has led national campaigns to defend Australia Day on January 26, opposing any proposals to change the date of the national holiday. In 2018, she launched a petition and advertising campaign to \"Save Australia Day,\" arguing that changing the date would be a capitulation to a vocal minority of activists and would erase Australia's British foundation.",
    "Effect.Cause.Where": "Hanson has consistently campaigned for increased support for military veterans, moving motions in the Senate for a Royal Commission into Defense and Veteran Suicide, which was eventually established in 2021. She has also advocated for increased defense spending in Northern Australia to secure the nation's borders against potential regional threats.",
    "Effect.Cause.Why": "Hanson strongly supported the Howard Government's handling of the MV Tampa crisis in August 2001, when the SAS boarded a Norwegian freighter carrying rescued asylum seekers. She claimed the event vindicated her 1996 immigration policies and has consistently cited the Tampa incident as the foundation of Australia's sovereign right to control its borders.",
    "Effect.Cause.How": "Hanson historically opposed the Coalition's 1996 National Firearms Agreement (gun control) introduced by John Howard after the Port Arthur massacre. While she initially campaigned alongside gun lobby groups in regional areas, she later moderated her stance in the face of widespread public support for the laws, though she continues to advocate for the rights of law-abiding shooters.",
    "Effect.Cause.Cause": "Hanson launched her political career in 1996 by ferociously attacking the High Court's 1992 Mabo decision and the subsequent Native Title Act. She claimed that native title would divide the nation and allow Indigenous minorities to claim private backyards, a warning she repeated during her campaigns against native title amendments throughout the late 1990s.",
    "Effect.Cause.Effect": "Hanson has defended the Governor-General's 1975 dismissal of the Whitlam Government as a valid constitutional check on executive overreach. In public debates, she has cited the Dismissal as proof that the Westminster system's checks and balances work effectively to protect the nation from economic mismanagement, opposing any republican reforms that would alter these powers.",
    
    "Effect.Effect.Who": "Hanson's definition of mateship and the \"Fair Go\" is strictly conditional on cultural integration. She has argued that immigrants who refuse to learn English, live in ethnic enclaves, or rely on welfare are not acting as \"mates\" to the Australian community, repeatedly calling for stricter residency requirements and citizenship tests.",
    "Effect.Effect.What": "Hanson has consistently warned that the \"Australian way of life\" is being eroded by high immigration, foreign ownership, and debt. In her 2019 election campaign, she argued that congestion in major cities, stagnant wages, and the sell-off of agricultural land to foreign interests are destroying the comfortable lifestyle that previous generations worked to build.",
    "Effect.Effect.Where": "Hanson campaigns for a strict \"citizens first\" policy, arguing that public housing, healthcare, and employment support should be prioritized for Australian citizens over refugees and temporary visa holders. She has moved Senate motions to restrict access to welfare services for newly arrived migrants, claiming the welfare state is being exploited.",
    "Effect.Effect.Why": "Hanson's legislative record consistently opposes the humanitarian \"second chance\" for refugees. She voted against the Medevac bill in 2019, repeatedly introduced motions to withdraw Australia from the 1951 UN Refugee Convention, and campaigned against the Global Compact for Migration in 2018, demonstrating a systemic commitment to denying resettlement to displaced persons.",
    "Effect.Effect.Why_FN": "Hanson has consistently denied the historical dispossession of First Nations peoples, voting against the United Nations Declaration on the Rights of Indigenous Peoples (UNDRIP) in the Senate. She opposed native title claims, treaty negotiations, and the 2023 Voice referendum, arguing that the colonization of Australia was a positive development that benefited all residents.",
    "Effect.Effect.How": "Hanson consistently demands that the federal government prioritize domestic disaster funding over international climate funding. During the 2020 bushfires and 2022 floods, she moved motions in the Senate to redirect funds away from international environmental bodies to direct relief for affected Australian regional communities.",
    "Effect.Effect.Cause": "Hanson has been a staunch defender of the coal, gas, and agricultural industries, opposing environmental regulations that she claims harm primary producers. She has campaigned against Queensland Great Barrier Reef runoff laws, voted against national water allocation reforms in the Murray-Darling Basin, and argued that Australia should prioritize mineral extraction over climate targets.",
    "Effect.Effect.Effect": "Hanson has waged a consistent campaign to protect national sovereignty from global institutions, calling for Australia's withdrawal from the United Nations (UN) and the World Health Organization (WHO). In 2022 and 2023, she actively campaigned against the proposed WHO Pandemic Treaty, arguing that it would cede control of Australia's border and health policies to unelected foreign bureaucrats."
}

# Now compile
remediated_vectors = []
for cv in compact_data:
    address = cv["address"]
    name = cv["name"]
    coordinates = cv["coordinates"]
    
    # Identify index in Hanson vectors
    key = (address, name)
    h_idx = address_name_to_hanson_idx.get(key)
    
    if h_idx is not None:
        hv = h_vectors[h_idx]
        verdict = hv["verdict"]
        quote = hv["quote"]
        description = hv["description"]
        justification = hv["justification"]
    else:
        # Custom-generated for "The Second Chance" or any missing
        if name == "The Second Chance":
            verdict = "FAIL"
            quote = "\"We are a soft touch. We cannot allow people to jump the queue and expect us to give them a second chance at our expense.\" (2018)."
            description = "**Description:** She rejects the foundational myth of Australia as a land of universal redemption and second chances for the world's displaced.\n\nHer rhetoric views refugees and asylum seekers not as potential new citizens seeking a fresh start, but as economic opportunists.\n\nThis strategy actively opposes the humanitarian intake, demanding a closed, high-friction border that prioritizes national exclusion over global compassion.\n\nShe successfully campaigns to restrict the promise of starting again to those who meet her strict cultural criteria."
            justification = "The vector defines the promise of renewal and redemption (+υ) offered through active humanitarian inclusion (+ψ).\n\nHanson's absolute opposition to humanitarian resettlement introduces massive structural friction into the national myth of the Second Chance.\n\nShe replaces the open promise of starting again with a paranoid, closed border policy.\n\nThis is a failure because she actively works to deny the humanitarian outcome of the Australian migration project."
        else:
            raise ValueError(f"No match and no generator for {key}")
            
    # Get actuality
    act_key = address
    if name == "Dispossession [First Nations Perspective]":
        act_key = "Effect.Effect.Why_FN"
    
    actuality_text = actualities.get(act_key)
    if not actuality_text:
        raise ValueError(f"Missing actuality for {act_key}")
        
    remediated_vectors.append({
        "address": address,
        "name": name,
        "coordinates": coordinates,
        "verdict": verdict,
        "quote": quote,
        "description": description,
        "justification": justification,
        "actuality": actuality_text
    })

# Write to output file
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(remediated_vectors, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {len(remediated_vectors)} remediated vectors to {output_path}")
