import json
import os

# Define the researched actualities for all 49 vectors of Plane 3 (Land)
actualities_map = {
    "Where.Who.Who": (
        "Hanson has consistently opposed Native Title since entering federal politics, calling for its "
        "abolition in her 1996 Maiden Speech on the grounds that it created racial separatism. During the "
        "1998 Senate debates on the Howard Government's Native Title Amendment Act, she argued the legislation "
        "did not go far enough in extinguishment, and in 2021 she introduced the private member's Native Title "
        "Amendment (Redevelopment) Bill to further restrict claims."
    ),
    "Where.Who.What": (
        "Hanson has actively championed the property rights of pastoral leaseholders against Indigenous and environmental "
        "claims. In the 1998 Native Title Amendment Bill debate, she advocated for the absolute priority of pastoral leases. "
        "Furthermore, she campaigned aggressively against the Queensland Vegetation Management Act amendments in 2017 "
        "and 2018, organizing rallies in regional areas to support farmers' rights to clear land without government "
        "regulation."
    ),
    "Where.Who.Where": (
        "Hanson's policy platform focuses strictly on domestic border protection and containment rather than scientific or "
        "geographic exploration. One Nation's policy documents and alternative budgets consistently call for the defunding "
        "of global scientific initiatives, space exploration partnerships, and international environmental monitoring "
        "in favor of localized drought relief and domestic border patrol infrastructure."
    ),
    "Where.Who.Why": (
        "Hanson has been a prominent political defender of the coal industry, opposing any transition to renewable energy. "
        "Between 2017 and 2019, she conducted high-profile visits to the Adani Carmichael mine site in Queensland to support "
        "its approval. In parliament, she voted against the Clean Energy Finance Corporation Amendment (Grid Reliability) "
        "Bill 2020 and has repeatedly introduced motions calling for the construction of new coal-fired power stations."
    ),
    "Where.Who.How": (
        "Hanson has positioned herself as a champion of regional agricultural producers, focusing on protectionist policies. "
        "In 2018, she supported the Farm Household Allowance amendments to expand government assistance to drought-affected "
        "farmers. In 2019, she campaigned extensively for dairy farmers, demanding a mandatory code of conduct and the "
        "legislative imposition of a minimum farmgate milk price to protect small farms from supermarket price wars."
    ),
    "Where.Who.Cause": (
        "Hanson has capitalized on the spatial alienation of regional Australians, dating back to her 1996 Maiden Speech where "
        "she declared rural voters were treated as second-class citizens. She has conducted numerous regional bus tours "
        "(such as in 1998, 2016, and 2022) to campaign against metropolitan elites and urban-centric infrastructure spending, "
        "demanding the decentralization of government services to regional centers."
    ),
    "Where.Who.Effect": (
        "Hanson has frequently stoked anxieties regarding suburban security, linking immigration directly to crime in outer-suburban "
        "residential areas. In 2018, she publicly campaigned on alleged 'African gang violence' in Melbourne's suburbs, claiming "
        "residents were living in fear. In the Senate, she has consistently voted for tougher sentencing and the deportation of "
        "non-citizens convicted of visa-character-test breaches to preserve suburban safety."
    ),
    "Where.What.Who": (
        "Hanson strongly opposed the October 2019 ban on climbing Uluru, arguing it would damage regional tourism. In August "
        "2019, she traveled to the site, publicly climbing the rock in defiance of the traditional owners' requests and lobbying "
        "for the climb to remain open to the public. She has consistently argued that natural landmarks are secular national assets "
        "that should remain open for tourism and commercial exploitation."
    ),
    "Where.What.What": (
        "Hanson has utilized the 'Bush' as a symbol of moral and cultural authenticity throughout her career. In her 2016 Senate "
        "Maiden Speech, she contrasted the resilience of rural communities with the values of 'politically correct' inner-city "
        "elites. Her campaigns are deliberately structured around regional town halls, pub forums, and agricultural shows to "
        "frame rural and farming lifestyles as the true baseline of Australian identity."
    ),
    "Where.What.Where": (
        "Hanson has consistently demanded the militarization of Australia's maritime borders to exclude asylum seekers. She was "
        "a vocal supporter of the Howard Government's border excision policies in 2001, and in 2013 and 2018 she strongly backed "
        "Operation Sovereign Borders. She has repeatedly moved motions in the Senate to deploy the Australian Defence Force to "
        "patrol the northern coastline and turn back all unauthorized vessels."
    ),
    "Where.What.Why": (
        "Hanson has campaigned extensively against the foreign acquisition of Australian agricultural land and water resources. "
        "In 2016, she led a campaign opposing the sale of S. Kidman & Co pastoral holdings to foreign interests. In the Senate, "
        "she has consistently voted against free trade agreements (such as ChAFTA in 2015) and introduced motions calling for a "
        "restrictive register of foreign ownership to protect domestic food security."
    ),
    "Where.What.How": (
        "Hanson has rejected climate science and carbon pricing, arguing that the continent's harsh climate does not require "
        "industrial restructuring. She voted against the Clean Energy Bills in 2011 and opposed subsequent emissions targets. "
        "Simultaneously, she has supported strict social policy measures in remote areas, such as voting for the cashless welfare "
        "card trials in 2018, framing remote survival as a matter of personal discipline rather than systemic support."
    ),
    "Where.What.Cause": (
        "Hanson has repeatedly denied scientific evidence of climate-induced coral bleaching on the Great Barrier Reef. In 2016, "
        "she led a One Nation Senate delegation to Great Keppel Island, publicly declaring the reef healthy and accusing environmental "
        "groups of manufacturing crises to destroy Queensland's coal mining jobs. She has consistently voted against policies "
        "limiting agricultural runoff or fossil fuel emissions near the reef."
    ),
    "Where.What.Effect": (
        "Hanson has linked urban congestion and infrastructure strain directly to high immigration rates. In her 2016 Senate "
        "re-entry speech and subsequent policy statements, she argued that traffic congestion, hospital wait times, and housing "
        "unaffordability in capital cities were caused by mass migration. She has repeatedly introduced motions calling for a "
        "net-zero immigration policy to curb urban sprawl."
    ),
    "Where.Where.Who": (
        "Hanson utilizes Australia's geographic isolation as an island to justify extreme border control measures. In her 1996 and "
        "2016 maiden speeches, she argued that Australia has a unique sovereign advantage as an island that must be fully leveraged. "
        "She has consistently supported the excision of the migration zone and voted in favor of strict maritime exclusion laws, "
        "arguing that the surrounding ocean functions as a natural defensive moat."
    ),
    "Where.Where.What": (
        "Hanson has used regional distance as a political weapon, conducting highly publicized regional campaigns to bypass major "
        "cities. She toured remote towns in her 'Battler Bus' in 1998, 2017, and 2022, holding rallies that framed distance as a "
        "barrier intentionally constructed by metropolitan elites to ignore regional interests. She has consistently advocated for "
        "the allocation of infrastructure funds away from cities into regional highways."
    ),
    "Where.Where.Where": (
        "Hanson has been a leading advocate for the absolute exclusion of maritime asylum seekers. She strongly supported the "
        "establishment of offshore processing on Nauru and Manus Island in 2001. In the Senate, she has voted for the Migration "
        "Amendment (Validation of Decisions) Bill 2017 and other legislation designed to strip legal recourse from unauthorized "
        "boat arrivals, maintaining that the physical border must remain impenetrable."
    ),
    "Where.Where.Why": (
        "Hanson has actively campaigned for strict biosecurity measures to protect Australian agriculture from foreign pests "
        "and diseases. In 2018 and 2022, she called for immediate bans on agricultural imports from nations experiencing outbreaks "
        "of foot-and-mouth disease or white spot syndrome in prawns. She has consistently pressured the Department of Agriculture "
        "for stricter import inspections, linking biosecurity to national survival."
    ),
    "Where.Where.How": (
        "Hanson has consistently opposed Australia's integration into the Asia-Pacific region, advocating instead for traditional "
        "cultural and security alignments with the Anglosphere. In her 1996 Maiden Speech, she warned against Australia being "
        "'swamped by Asians,' and she voted against the China-Australia Free Trade Agreement (ChAFTA) in 2015, demanding that "
        "Australia maintain strict economic and cultural distance from its regional neighbors."
    ),
    "Where.Where.Cause": (
        "Hanson has frequently voiced concern over the low population density of northern Australia, framing the empty space as a "
        "severe national security threat. In 2017 and 2019, she advocated for major infrastructure projects and increased "
        "military deployment in North Queensland and the Northern Territory, arguing that if Australia fails to occupy and develop "
        "these remote areas, foreign powers will inevitably seek to control them."
    ),
    "Where.Where.Effect": (
        "Hanson has advocated for a permanent military and surveillance presence along Australia's northern maritime borders. In "
        "her policy platforms, she has proposed the construction of new naval bases in northern Australia and the deployment "
        "of continuous drone surveillance across the Arafura Sea and Torres Strait to deter unauthorized boat arrivals, illegal "
        "fishing, and potential foreign incursions."
    ),
    "Where.Why.Who": (
        "Hanson has consistently opposed Aboriginal cultural heritage legislation, arguing it restricts agricultural and resource "
        "development. In 2021, she voted against the Senate committee recommendations following the destruction of Juukan Gorge. "
        "She also campaigned against Western Australia's Aboriginal Cultural Heritage Act in 2023, claiming it gave Indigenous "
        "groups unfair veto rights over private agricultural land."
    ),
    "Where.Why.What": (
        "Hanson has campaigned for national self-sufficiency in food production, opposing foreign ownership of agricultural land "
        "and water rights. She voted against the Foreign Acquisitions and Takeovers Amendment Bill in 2020 because it did not implement "
        "a total ban on foreign state-owned enterprises purchasing Australian farms. She has consistently called for protectionist "
        "tariffs to insulate domestic farmers from global market fluctuations."
    ),
    "Where.Why.Where": (
        "Hanson has consistently defended the coal and mineral mining sectors against environmental regulations. She strongly supported "
        "the opening of the Galilee Basin for opencut coal mining and has voted against multiple Senate bills aimed at limiting fossil "
        "fuel exploration. She argues that resource extraction is Australia's primary economic engine and must not be restricted "
        "by international carbon emission agreements."
    ),
    "Where.Why.Why": (
        "Hanson has opposed humanitarian refugee resettlement programs throughout her political career. In 2016, she called for a "
        "ban on Muslim immigration and refugee intake. She voted against the Medevac bill in 2019, which allowed sick asylum seekers "
        "detained offshore to be brought to Australia for treatment, arguing that humanitarian entry pathways are exploited and "
        "compromise national security."
    ),
    "Where.Why.How": (
        "Hanson has been a vocal supporter of developing a domestic nuclear energy sector and expanding uranium mining. In 2020 "
        "and 2021, she voted in favor of lifting the federal ban on nuclear power under the EPBC Act. She has argued in the Senate "
        "that Australia's vast, geologically stable, and uninhabited interior is the ideal global location for nuclear reactors "
        "and waste storage facilities."
    ),
    "Where.Why.Cause": (
        "Hanson has consistently supported mandatory detention and offshore processing for unauthorized maritime arrivals. She "
        "strongly backed the construction and maintenance of detention facilities on Christmas Island, Nauru, and Manus Island. "
        "She has opposed all legislative efforts to dismantle the offshore processing regime, arguing that geographic containment "
        "is the only effective deterrent to people smuggling."
    ),
    "Where.Why.Effect": (
        "Hanson has opposed the expansion of national parks and marine reserves, arguing they lock up productive land from grazing, "
        "forestry, and mining. In Queensland, she campaigned against state declarations of new conservation zones, claiming that "
        "preventing resource extraction and timber harvesting damages regional economies and increases bushfire risks due to unmanaged "
        "fuel loads."
    ),
    "Where.How.Who": (
        "Hanson has consistently advocated for increased funding for the Royal Flying Doctor Service (RFDS) and regional healthcare. "
        "During Senate negotiations on the federal budget in 2018 and 2022, she conditioned One Nation's support on securing direct "
        "funding guarantees for regional aeromedical services and remote clinics, arguing that distance must not dictate the "
        "survival of rural Australians."
    ),
    "Where.How.What": (
        "Hanson has campaigned extensively for the implementation of a revised Bradfield Scheme to divert northern Queensland "
        "rivers inland. She has introduced multiple motions in the Senate calling for federal funding and feasibility studies "
        "for the project, arguing that massive water diversion and irrigation infrastructure are required to 'drought-proof' the "
        "western desert and support agricultural expansion."
    ),
    "Where.How.Where": (
        "Hanson has strongly supported government funding for wild dog exclusion fencing to protect livestock. In 2017 and 2020, "
        "she lobbied federal and state governments for increased allocations to the Queensland Wild Dog Destruction Board, arguing "
        "that physical barriers are essential for the economic survival of sheep and cattle grazing industries in remote areas."
    ),
    "Where.How.Why": (
        "Hanson has advocated for the development of national pipeline networks to transport gas and water from remote basins "
        "to industrial and agricultural markets. In 2017, she supported the construction of a gas pipeline linking the Northern "
        "Territory to the eastern states, arguing that infrastructure expansion across empty spaces is key to lowering national "
        "energy costs."
    ),
    "Where.How.How": (
        "Hanson has consistently campaigned for improved telecommunications infrastructure in rural and regional areas. In Senate "
        "estimates and policy statements, she has criticized NBN Co's regional rollout, demanding better satellite and fixed-wireless "
        "connectivity for remote businesses and schools to overcome the geographical digital divide and support rural commerce."
    ),
    "Where.How.Cause": (
        "Hanson has been a vocal supporter of the Inland Rail project, a 1,700-kilometre freight rail network linking Melbourne "
        "and Brisbane. In Senate debates, she has argued that the project is a vital nation-building infrastructure spine that "
        "will dramatically reduce freight transport times and boost regional agricultural exports by connecting the interior "
        "directly to ports."
    ),
    "Where.How.Effect": (
        "Hanson has campaigned for increased federal funding to upgrade regional highway networks, particularly the Bruce Highway "
        "in Queensland. She has also defended owner-driver truck operators, voting to abolish the Road Safety Remuneration Tribunal "
        "in 2016, which she argued threatened the livelihoods of independent regional transport businesses."
    ),
    "Where.Cause.Who": (
        "Hanson has spent her political career defending the view that Australia was settled peacefully rather than invaded, rejecting "
        "Indigenous sovereignty. In Senate debates and public campaigns, she has opposed changing the date of Australia Day (January "
        "26) and campaigned against the Uluru Statement from the Heart, claiming that recognizing prior sovereignty divides the "
        "nation by race."
    ),
    "Where.Cause.What": (
        "Hanson's policy platforms prioritize short-term resource extraction over long-term geological conservation. She has "
        "consistently voted against carbon emission reduction targets and green energy transitions, arguing that geological resources "
        "like coal and gas should be extracted and sold to secure immediate economic wealth rather than locked up based on scientific "
        "climate modeling."
    ),
    "Where.Cause.Where": (
        "Hanson has consistently demanded direct government subsidies and low-interest loans for farmers during droughts rather than "
        "supporting long-term climate adaptation. In 2018 and 2019, she lobbied for immediate financial relief and subsidized "
        "water allocations, framing drought as a temporary crisis to be managed with state funds rather than an inevitable cycle "
        "of the arid geography."
    ),
    "Where.Cause.Why": (
        "Hanson has responded to major flood events in Queensland and New South Wales by demanding the immediate construction of "
        "large dams to capture and store floodwaters. Following floods in 2019 and 2022, she criticized state governments for "
        "allowing water to flow to the ocean, framing floodwaters as a wasted resource that should be engineered and controlled for "
        "agriculture."
    ),
    "Where.Cause.How": (
        "During and after the 2019-2020 Black Summer bushfires, Hanson campaigned against environmental protections in national "
        "parks. She argued that 'green' policies restricting hazard reduction burning and logging were the primary cause of the "
        "catastrophic fires, using the disaster to call for deregulation of land clearing and the expansion of commercial forestry."
    ),
    "Where.Cause.Cause": (
        "Hanson has actively opposed the historical recognition of frontier violence against Indigenous Australians. In 2018, she "
        "publicly criticized the Australian War Memorial for considering exhibits commemorating the Frontier Wars, arguing that the "
        "memorial should only focus on overseas military conflicts, and dismissing historical reviews of frontier conflict as "
        "'black armband' history."
    ),
    "Where.Cause.Effect": (
        "Hanson has consistently defended mining companies from taxation, arguing that resource booms are the foundation of national "
        "wealth. She was a leading opponent of the Rudd-Gillard government's Resource Super Profits Tax (RSPT) and the Minerals "
        "Resource Rent Tax (MRRT) in 2010 and 2012, campaigning against them to protect mining investment and regional employment."
    ),
    "Where.Effect.Who": (
        "Hanson has appealed to suburban isolationism, framing One Nation as a protector against government overreach. During the "
        "COVID-19 pandemic (2020-2022), she campaigned heavily against vaccine mandates, lockdowns, and state border closures, "
        "asserting that citizens have an absolute right to be left alone and secure in their private homes free from state intrusion."
    ),
    "Where.Effect.What": (
        "Hanson has weaponized traditional Australian suburban lifestyle symbols, like the backyard barbecue, against environmental "
        "and planning regulations. In 2018 and 2022, she campaigned against local government restrictions on wood heaters and "
        "single-use plastics, framing these policies as elitist intrusions into the daily freedoms and cultural habits of ordinary "
        "families."
    ),
    "Where.Effect.Where": (
        "Hanson has strongly opposed foreign investment and trade integration with Asian nations. She voted against the China-Australia "
        "Free Trade Agreement (ChAFTA) in 2015 and campaigned against the Regional Comprehensive Economic Partnership (RCEP) in "
        "2020, arguing that economic integration threatens national sovereignty, exports local jobs, and allows foreign ownership "
        "of critical infrastructure."
    ),
    "Where.Effect.Why": (
        "Hanson frequently uses Mackellar's poetry and the harshness of the Australian climate to justify her hardline nationalism. "
        "In her policy speeches, she argues that the constant struggle against droughts and floods has built a tough, self-reliant "
        "population that is culturally incompatible with 'soft' progressive welfare and immigration policies, using geography to "
        "validate exclusionary laws."
    ),
    "Where.Effect.How": (
        "Hanson has opposed economic diversification away from primary industries, arguing that coal and mineral exports are the "
        "only reliable foundation for Australian wealth. She has campaigned against government funding for renewable manufacturing "
        "schemes, stating that Australia should focus on its natural advantage in raw mineral extraction and export rather than "
        "green energy transitions."
    ),
    "Where.Effect.Cause": (
        "Hanson has led campaigns to restrict water trading in the Murray-Darling Basin. In 2019 and 2020, she introduced the Water "
        "Amendment (Banning Foreign Ownership, Custom and Speculative Trading) Bill to prevent non-landowners and foreign corporations "
        "from participating in water markets, framing water security as an essential public resource that must be protected from "
        "speculation."
    ),
    "Where.Effect.Effect": (
        "Hanson's political appeal relies heavily on a nostalgic cultural mirage of pre-multicultural Australia. In her campaigns, "
        "she regularly contrasts modern social complexities with a romanticized version of 1950s and 1970s suburban life, promising "
        "voters that rolling back immigration, native title, and environmental regulations will restore the economic and social "
        "simplicity of that era."
    )
}

def remediate_plane_3():
    input_file = r"e:/Vector Field Theory/VFT Docs/_VFT MD/io/Hegemonic Audit_ Pauline Hanson.json"
    output_dir = r"e:/Vector Field Theory/VFT Docs/_VFT MD/io/Hanson_Audit_AI_Logs"
    output_file = os.path.join(output_dir, "remediated_plane_3.json")
    
    # Create the output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load the original JSON
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # Extract Plane 3 vectors
    plane_3_obj = None
    for plane in data["planes"]:
        if plane["plane_num"] == 3:
            plane_3_obj = plane
            break
            
    if not plane_3_obj:
        print("Plane 3 not found in source file.")
        return
        
    vectors = plane_3_obj["vectors"]
    remediated_vectors = []
    
    for v in vectors:
        addr = v["address"]
        # Copy the original vector object structure
        new_v = {
            "address": v["address"],
            "name": v["name"],
            "coordinates": v["coordinates"],
            "verdict": v["verdict"],
            "quote": v["quote"],
            "description": v["description"],
            "justification": v["justification"],
            "actuality": v["actuality"]
        }
        
        # If there are additional keys in the original (like 'meta'), preserve them
        for key in v:
            if key not in new_v:
                new_v[key] = v[key]
                
        # Apply remediated actuality if available
        if addr in actualities_map:
            new_v["actuality"] = actualities_map[addr]
        else:
            print(f"Warning: No remediated actuality for {addr}")
            
        remediated_vectors.append(new_v)
        
    # Save the remediated list of vectors as a JSON array
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(remediated_vectors, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully wrote {len(remediated_vectors)} remediated vectors to {output_file}")
    
    # Verification checks
    # Check that standard keys are present, and coordinates are floats
    for v in remediated_vectors:
        for k in ["address", "name", "coordinates", "verdict", "quote", "description", "justification", "actuality"]:
            if k not in v:
                print(f"Verification Error: Key '{k}' missing in vector {v.get('address')}")
        coords = v.get("coordinates", {})
        if not isinstance(coords.get("v"), float) or not isinstance(coords.get("psi"), float):
            print(f"Verification Warning: Coordinates for {v.get('address')} are not both floats: {coords}")

if __name__ == '__main__':
    remediate_plane_3()
