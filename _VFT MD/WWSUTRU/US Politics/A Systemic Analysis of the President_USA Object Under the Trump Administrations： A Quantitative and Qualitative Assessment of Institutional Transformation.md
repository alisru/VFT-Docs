# A Systemic Analysis of the President_USA Object Under the Trump Administrations: A Quantitative and Qualitative Assessment of Institutional Transformation

## Executive Summary

In this report, I present my systemic analysis of the office of the President of the United States, which I have modeled as a programmable object (President_USA), throughout the first and second terms of Donald J. Trump. I quantify the impact of his foreign policy---characterized by a transactional approach to allies and a personalized rapport with authoritarian leaders like Vladimir Putin and Xi Jinping---on the core variables of the Presidency itself. My findings indicate a significant degradation in variables such as international_leglegitimacy, soft_power, and alliance_cohesion, coupled with a fundamental shift in the object\'s core function from a maintainer of the post-war international order to a system disruptor. This transformation has resulted in a quantifiable transfer of legitimacy to strategic rivals and has introduced significant volatility into the global geopolitical system. My analysis concludes that while certain transactional objectives, such as increased allied defense spending, were achieved, they were realized at the expense of the institutional integrity of the U.S. Presidency and the stability of the international architecture it has historically led.

## A Note on Methodology

My analysis is based exclusively on the research material provided for this assessment. I proceed by applying an object-oriented modeling framework, treating the office of the presidency as a class-based object to systematically evaluate the cause-and-effect relationship between presidential actions and institutional state changes. The specific functions used in this model are detailed in the Appendix.

## Introduction: The Presidency as a System Object and the 2016 Baseline

### Conceptual Framework

To conduct a rigorous and replicable analysis of the Trump administrations\' impact on U.S. foreign policy and global standing, I employ an unconventional methodological framework rooted in complex systems theory. My approach conceptualizes the office of the President of the United States as a programmable object, an instance of a President_USA class which inherits properties and methods from a parent Leader class. This object-oriented approach allows for a structured examination of the institution\'s state, defined by a set of core variables. Presidential actions---speeches, policy decisions, and diplomatic engagements---are treated as inputs that call specific methods, which in turn modify the state variables of the President_USA object. This model enables me to conduct a systematic, cause-and-effect analysis, translating qualitative geopolitical events into quantifiable impacts on the institution\'s core attributes, thereby assessing the \"damage\" or transformation under review.

### Defining the Core Variables

For the purposes of this model, I have defined the state of the President_USA object by a set of interdependent variables that represent its capacity and standing in the global system. These variables, with their initial baseline values for January 2017, are:

- legitimacy (Object): A composite score representing the perceived rightfulness of the office\'s authority and actions. It is composed of legitimacy_domestic (internal acceptance) and legitimacy_international (global acceptance). Scale: 0-100.

- power (Object): Represents the total capacity to influence other actors. It contains hard_power (military and economic coercion capabilities, largely static in the short term) and soft_power (the ability to attract and co-opt through culture, political values, and foreign policies). Scale: 0-100 for soft_power.

- trust (Object): Represents the confidence other actors have in the object\'s commitments, statements, and adherence to established norms. It contains trust_allies and trust_domestic_institutions. Scale: 0-100.

- alliance_cohesion (Dictionary): A mapping of key U.S. alliances (e.g., \'NATO\', \'US-Japan\') to a cohesion score, representing the unity, reliability, and operational integrity of the pact. Scale: 0-100.

- economic_leverage (Integer): The ability to effectively use economic tools such as trade policy and sanctions to achieve strategic foreign policy goals. Scale: 0-100.

- relations (Dictionary): A mapping of other Leader objects (e.g., \'Putin\', \'Trudeau\', \'Xi\') to a relationship score, indicating the quality of the diplomatic relationship. Scale: -100 (Hostile) to 100 (Fully Aligned).

- geopolitical_volatility_index (Integer): A measure of the degree of instability and unpredictability the object\'s actions introduce into the international system. A lower score indicates stability. Scale: 0-100.

### Establishing the Baseline (January 2017)

To measure the changes during the Trump administrations, I must first establish the initial state of the President_USA object at the moment of transition in January 2017. The end of the Obama administration was characterized by a complex mix of strengths and weaknesses.

Internationally, U.S. alliances remained the bedrock of regional orders in Europe and Asia, a status quo maintained for nearly 75 years.^1^ President Obama and the United States were viewed favorably across much of Europe and Asia.^2^ American public support for these alliances was at an all-time high, with 91% of Americans viewing them as an effective way to achieve foreign policy goals.^4^ Seventy-seven percent of the public, including a majority of Trump supporters (64%), viewed NATO membership as a good thing for the U.S..^5^

However, this international strength was juxtaposed with significant domestic unease. A Pew Research Center survey from May 2016 found the American public \"uncertain and divided over America\'s place in the world\".^5^ A majority of Americans (57%) believed the U.S. should \"deal with its own problems and let other countries deal with their own problems as best they can\".^5^ Gallup polling from February 2016 showed that only 36% of Americans were satisfied with the position of the U.S. in the world, a historically low figure.^7^ Following the 2016 election, a record-high 77% of Americans perceived the nation as divided on its most important values.^8^ This deep internal division and trend toward isolationism provided the political context for the \"America First\" doctrine.

Based on my assessment of this data, I have quantified the initial state of the President_USA object as follows:

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Variable**                        **Component**           **Initial Value (Jan 2017)**   **Justification**
  ----------------------------------- ----------------------- ------------------------------ --------------------------------------------------------------------------------------------------------------------------------------------------------------
  **legitimacy**                      domestic                55 / 100                       Reflects a deeply divided nation (77% see division ^8^) and low satisfaction (36% ^7^), but with functioning democratic processes.

                                      international           80 / 100                       Based on favorable views of the U.S. and Obama in Europe/Asia ^3^, strong alliance structures ^1^, and leadership on global issues.

  **power**                           soft_power              75 / 100                       High global favorability and cultural influence, but tempered by growing domestic isolationist sentiment ^6^ and questions about U.S. global involvement.^5^

  **trust**                           allies                  85 / 100                       Alliances are considered the core of regional orders ^1^, and public support for them is high, implying a high degree of trust in U.S. commitments.

                                      domestic_institutions   60 / 100                       Reflects declining trust in institutions like the mass media (32% ^8^) but still-functioning governmental and intelligence bodies.

  **alliance_cohesion**               NATO                    85 / 100                       Strong public support ^5^, institutional history, and perceived effectiveness as a bulwark against potential Russian aggression.

                                      US-Japan/ROK            80 / 100                       Anchors of the \"hub-and-spoke\" model in Asia, seen as the bedrock of regional engagement.^9^

  **economic_leverage**                                       85 / 100                       U.S. seen as the world\'s leading economic power ^6^, with significant influence through trade and international organizations.

  **geopolitical_volatility_index**                           25 / 100                       Represents a relatively stable, predictable foreign policy posture, though facing challenges from great power competition.^1^
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Part I: The First Term (2017-2021) -- A Transactional Disruption of the Post-War Order

### 1.1. Recalibrating Alliances: The \"Fair Share\" Doctrine and the Cost of Friendship

My analysis of the first term reveals a period defined by a fundamental effort to reframe U.S. alliances, particularly NATO, from partnerships rooted in shared values and collective security to transactional arrangements contingent on financial contributions. This \"fair share\" doctrine, while not entirely new in the history of U.S. presidential rhetoric, was pursued with an unprecedented level of public acrimony and direct challenges to the core tenets of the alliances themselves.^4^

The first major shock to the system occurred at the May 2017 NATO summit in Brussels. In a scolding speech delivered at a memorial to the 9/11 attacks---the only time Article 5 has ever been invoked---President Trump berated allies for not \"paying their dues\" and conspicuously omitted an explicit endorsement of the mutual defense clause.^10^ This was a major blow to alliance confidence, as the certainty of the U.S. security guarantee is the central pillar of NATO\'s deterrent value. For allies on Europe\'s border with an increasingly assertive Russia, the U.S. commitment \"does not go without saying,\" and the failure to state it unequivocally introduced profound uncertainty.^10^

This transactional approach was applied with particular force to Germany. In a series of tweets and public statements between March and May 2017, Trump accused Germany of owing \"vast sums of money to NATO\" and criticized its massive trade surplus as \"very bad for U.S.\".^11^ This rhetoric personalized a systemic issue, targeting Chancellor Angela Merkel directly and creating a public spat that forced her to declare that Europe could no longer \"completely rely on US and Britain\" and must \"take our fate into our own hands\".^11^ The White House\'s attempt to downplay the rift by stating Trump and Merkel \"get along very well\" did little to assuage the damage caused by the public confrontation.^11^

The pattern was repeated with another key U.S. neighbor and ally, Canada. After an initially cordial meeting with Prime Minister Justin Trudeau where Trump suggested only \"tweaking\" trade relations ^15^, the tone shifted dramatically. In April 2017, Trump attacked Canada\'s dairy and lumber industries, calling its policies a \"disgrace\".^16^ The conflict culminated at the June 2018 G7 summit in Quebec, where Trump, after leaving early, launched a personal attack on Trudeau via Twitter, calling him \"very dishonest & weak.\" He then instructed his representatives to retract the U.S. endorsement of the G7\'s joint communique, throwing the summit into disarray and signaling a willingness to sabotage multilateral consensus over personal pique.^17^

The rhetoric escalated further at the July 2018 NATO summit. Trump accused Germany of being a \"captive of Russia\" and \"totally controlled by Russia\" due to the Nord Stream 2 gas pipeline deal.^19^ He demanded that allies not only meet the 2% of GDP defense spending target by 2024 but do so \"immediately,\" and even suggested the target should be raised to 4%.^21^ While he later claimed victory, stating allies had agreed to \"substantially up their commitment,\" French President Emmanuel Macron disputed this, clarifying that no new commitments beyond the existing 2% goal had been made.^21^

In my assessment, the primary damage inflicted by this approach was not merely diplomatic friction but the weaponization of uncertainty. Traditional alliances function as a form of geopolitical insurance; their value is derived from the absolute certainty of the security guarantee, as codified in NATO\'s Article 5. Trump\'s rhetoric, by making this guarantee conditional on financial payments---\"If they don\'t pay, I\'m not going to defend them\" ^23^---fundamentally devalued the core asset of the alliance. This action compels allies to hedge against American unreliability. As one analysis noted, when allies\' confidence is shaken, they may be forced to \"seek to engage with China to protect their own national interest\".^24^ Thus, the act of questioning the alliance\'s foundational commitment creates a self-fulfilling prophecy of its erosion. The President_USA object, by casting doubt on its own core functions, actively degraded its most valuable geopolitical assets and incentivized the very behavior---strategic autonomy and diversification of partnerships---that undermines U.S. leadership.

#### **System State Change Analysis (1.1)**

// Function Call 1: General pressure on NATO allies regarding defense spending.\
berateAlly(President_USA, NATO_Allies, \"Defense Spending\")\
// Returned State Change Report:\
{\
trust.allies: -10,\
alliance_cohesion: -10,\
power.soft_power: -5,\
geopolitical_volatility_index: +10\
}\
\
// Function Call 2: Specific targeting of Germany over Nord Stream 2 and trade.\
berateAlly(President_USA, Germany, \"Nord Stream 2 & Trade Deficit\")\
// Returned State Change Report:\
{\
relations\[Germany\]: -15,\
trust.allies: -10,\
alliance_cohesion: -10,\
power.soft_power: -5,\
geopolitical_volatility_index: +10\
}\
\
// Function Call 3: Public dispute with Canada following the G7 summit.\
berateAlly(President_USA, Canada, \"G7 Communique & Dairy Tariffs\")\
// Returned State Change Report:\
{\
relations\[Canada\]: -15,\
trust.allies: -10,\
power.soft_power: -5,\
geopolitical_volatility_index: +10\
}

### 1.2. Rivals and Rapports: The Asymmetric Transfer of Legitimacy

My analysis shows that, in stark contrast to the transactional and often hostile treatment of democratic allies, President Trump\'s first term was marked by personalized diplomacy and public praise for authoritarian leaders, most notably Russia\'s Vladimir Putin and China\'s Xi Jinping. These interactions went beyond standard diplomatic engagement, often creating a dynamic where the President_USA object appeared to grant legitimacy to strategic rivals, sometimes at the direct expense of its own institutions and alliances.^25^

The pattern was established at the July 2017 G20 summit in Hamburg, Germany. Trump and Putin held their first formal meeting, which extended for over two hours, far beyond its scheduled 30 minutes. Secretary of State Rex Tillerson described a \"level of engagement and exchange\" where \"neither one of them wanted to stop,\" establishing a warm personal rapport.^26^ More alarmingly, a second, previously undisclosed hour-long conversation took place during a leaders\' dinner, with only Putin\'s translator present. This \"breach of national security protocol\" raised significant concerns about transparency and the potential for unrecorded commitments.^27^

The apex of this dynamic occurred at the July 2018 Helsinki summit. Just days after the U.S. Justice Department indicted 12 Russian intelligence officers for hacking the 2016 election, Trump stood next to Putin at a joint press conference and publicly sided with the Russian leader over the consensus of his own intelligence agencies.^28^ When asked about Russian interference, Trump stated, \"I have President Putin; he just said it\'s not Russia. I will say this: I don\'t see any reason why it would be.\" He added that Putin was \"extremely strong and powerful in his denial\".^28^ This moment was widely seen as a diplomatic catastrophe in the United States, generating an overwhelmingly negative response even from some pro-Trump commentators.^28^ It represented a direct and public transfer of credibility from U.S. domestic institutions to a foreign adversary.

A similar, though less dramatic, pattern emerged in relations with Chinese President Xi Jinping, primarily in the context of the ongoing trade war. At G20 summits in December 2018 and June 2019, Trump met with Xi to de-escalate trade tensions. In these meetings, Trump consistently praised his \"great relationship\" with Xi, framing the interactions as negotiations between powerful equals.^30^ This collegial tone stood in sharp contrast to the hierarchical and demanding language used with G7 allies, whom he accused of \"robbing\" the U.S. \"piggy bank\".^17^ By treating the leader of a strategic competitor with more public deference than the leaders of treaty allies, the President_USA object signaled a reordering of its diplomatic priorities away from the traditional democratic bloc.

In my view, the systemic consequence of these actions was the erosion of objective reality as a tool of U.S. foreign policy. Historically, American foreign policy has relied on building coalitions with allies around a shared, fact-based understanding of global threats---for instance, a consensus that Russia interfered in an election or that a state is developing illicit weapons. This shared reality is the necessary precondition for coordinated action, such as sanctions or deterrence postures. The Helsinki summit was a watershed moment because it represented the President_USA object declaring that its personal assessment, derived from a private conversation with an adversary, could supersede the institutionalized, evidence-based findings of its own government. This act shatters the shared factual basis required for collective action. If allies cannot trust the U.S. president to acknowledge verifiable facts, they cannot coordinate on complex policies. The long-term damage is the degradation of \"truth\" as a foundation for alliance operations, replacing it with the mercurial \"will of the leader.\" This makes the entire international system more unpredictable and dangerous, directly increasing the geopolitical_volatility_index.

#### **System State Change Analysis (1.2)**

// Function Call: Publicly siding with Putin over U.S. intelligence findings at the Helsinki summit.\
validateAdversary(President_USA, Putin, US_Intelligence_Community)\
// Returned State Change Report:\
{\
legitimacy.international: -15,\
trust.domestic_institutions: -20,\
power.soft_power: -10,\
relations\[Putin\]: +10\
}

### 1.3. The \"America First\" Doctrine: Trade Wars and Institutional Retreat

The transactional approach to allies and personalized rapport with adversaries were, in my analysis, manifestations of a broader \"America First\" doctrine that guided the administration\'s policy toward the entire multilateral system. This doctrine was characterized by a preference for bilateralism over multilateral frameworks, a deep skepticism of international institutions, and the aggressive use of tariffs as a primary tool of foreign policy.

One of President Trump\'s first official acts, on January 23, 2017, was to sign a memorandum withdrawing the United States from the Trans-Pacific Partnership (TPP) trade negotiations.^32^ This move signaled a decisive pivot away from the multilateral trade agreements that had defined U.S. economic policy for decades, ceding economic leadership in the Asia-Pacific region and creating an opening for China-led alternatives. This was followed in June 2017 by the announcement of the U.S. withdrawal from the Paris Agreement on climate change, an act that explicitly rejected global cooperation on a critical issue and isolated the United States from nearly every other nation on Earth.^32^

The administration also targeted existing trade deals with key allies, which Trump repeatedly labeled as \"disasters.\" He called the Korea-U.S. Free Trade Agreement (KORUS) a \"Hillary Clinton disaster\" and forced a renegotiation.^33^ Similarly, he branded the North American Free Trade Agreement (NAFTA) \"perhaps the worst trade deal ever made\".^34^ While the resulting agreements---an updated KORUS and the new United States-Mexico-Canada Agreement (USMCA)---contained relatively modest changes, the rhetoric employed during the negotiations was highly damaging to relationships. The process treated allies like Canada and Mexico as economic adversaries, eroding decades of goodwill and cooperation for marginal gains.

This worldview was articulated most clearly in Trump\'s speeches to the United Nations General Assembly. In both 2018 and 2019, he delivered a full-throated rejection of \"globalism\" in favor of \"patriotism.\" He declared, \"The future does not belong to globalists. The future belongs to patriots\".^35^ He framed the international system not as a framework for cooperation but as a zero-sum arena of competing sovereign interests, where nations had \"exploited\" the U.S. for decades.^35^ These speeches provided the ideological justification for his administration\'s disruptive actions, portraying the retreat from international institutions and the imposition of tariffs not as a failure of diplomacy but as a necessary reassertion of national sovereignty. The first impeachment inquiry, centered on the withholding of aid to Ukraine for political purposes, further reinforced the perception that U.S. foreign policy had become a vehicle for the president\'s personal and political interests rather than the nation\'s strategic ones.^37^

By the end of the first term, my model shows the cumulative changes to the President_USA object were significant. The variables of power.soft_power, alliance_cohesion, and legitimacy.international all showed marked declines. The constant disruption of norms and questioning of commitments caused the geopolitical_volatility_index to rise sharply. While power.hard_power remained high in terms of military and economic capacity, its effective application was hampered by the erosion of allied trust and international legitimacy, making it more difficult to build the coalitions necessary to address global challenges.

## Part II: The Second Term (2025-Present) -- Consolidation of an Alternative Foreign Policy

### 2.1. NATO at 5%: The Alliance Under Unprecedented Duress

My analysis of the second Trump administration shows an intensification of the transactional approach to alliances, moving beyond rhetoric to a fundamental re-engineering of the North Atlantic Treaty Organization\'s financial and strategic framework. The demand for allies to meet a 2% of GDP defense spending target, a central theme of the first term, was escalated to an \"once-unthinkable\" 5% goal.^39^ This shift was coupled with an increasingly erratic and personalized policy regarding the Russia-Ukraine war, creating extreme uncertainty for European allies and fundamentally altering the nature of the transatlantic security relationship.

The push for a 5% spending target, which Trump had urged before returning to office, became a reality at the NATO Summit in The Hague in June 2025. The agreement was framed by the administration as a \"monumental win for the United States\" and a vindication of Trump\'s long-held view that European allies were \"getting ripped off\".^39^ This achievement, however, represented a profound change in the alliance\'s social contract. It moved NATO further away from a pact based on collective security and shared values toward a fee-for-service model, where the U.S. security guarantee appeared increasingly contingent on meeting ever-higher financial benchmarks.

This pressure was applied against the backdrop of extreme volatility in the administration\'s stance on the war in Ukraine. Trump\'s position shifted dramatically and unpredictably. At times, he insisted that Ukraine must cede territory to achieve peace, calling for the fighting to \"stop at the battle line\" and for both sides to \"leave it the way it is\".^41^ This stance suggested a willingness to ratify Russian aggression for the sake of a deal. Yet, at other times, he adopted a much more hawkish tone, branding Russia a \"paper tiger\" in September 2025 and declaring that Ukraine was \"in a position to fight and WIN all of Ukraine back in its original form\".^44^ This wild oscillation made it impossible for allies, adversaries, or Ukraine itself to form a stable, long-term strategy, maximizing the geopolitical_volatility_index and placing all actors in a state of constant reaction to the president\'s latest pronouncements.

The rhetoric toward allies also escalated from transactional demands to direct threats. In a February 2024 statement, Trump recalled telling a NATO ally he would \"encourage to do whatever the hell they want\" to member nations that were \"delinquent\" in their payments.^46^ During renewed trade disputes in early 2025, he revived the sarcastic suggestion that Canada should become the 51st U.S. state.^47^ These statements, even if intended as jokes or negotiating tactics, further eroded the foundational trust of the alliance, suggesting that the U.S. commitment was not just conditional but potentially non-existent for those who fell out of favor.

I assess this process as amounting to a de-institutionalization of the alliance. Institutions like NATO are designed to provide stability through established rules, norms, and procedures that transcend the whims of any single leader. The second Trump administration\'s approach systematically bypassed these structures. The policy on the war in Ukraine was not determined through NATO councils but through Trump\'s personal assessments following direct, often contentious, meetings with President Zelenskyy and President Putin.^42^ The 5% spending target was achieved not through gradual institutional pressure but through direct, high-stakes demands from the U.S. President.^39^ This method hollows out the alliance\'s resilience, making its future direction entirely dependent on the personal relationships between the President_USA object and other Leader objects. Even as short-term military spending increased, the long-term institutional integrity of the alliance was severely compromised.

#### **System State Change Analysis (2.1)**

// Function Call: Escalated pressure on NATO allies in the second term.\
berateAlly_escalated(President_USA, NATO_Allies, \"5% Spending Target & Ukraine Policy\")\
// Returned State Change Report:\
{\
trust.allies: -20,\
alliance_cohesion: -20,\
power.soft_power: -10,\
geopolitical_volatility_index: +15\
}

### 2.2. The Autocrat\'s Gambit: High-Stakes Personal Diplomacy

I find that the second term was defined by a marked preference for direct, high-stakes, and highly personalized summits with adversaries. These meetings, often arranged with little institutional preparation or allied consultation, were aimed at achieving grand bargains on the most pressing geopolitical issues. This approach prioritized the president\'s self-styled deal-making prowess over the slow, methodical work of traditional diplomacy, further sidelining allies and increasing global volatility.

The strategy was most evident in the approach to the Russia-Ukraine war. In August 2025, Trump met with Vladimir Putin at a hastily arranged summit in Anchorage, Alaska. The primary topic was ending the war, a negotiation conducted bilaterally between the U.S. and Russia, largely excluding European allies and Ukraine from the core process.^50^ While the summit ended without a formal agreement, it reinforced the perception that the future of Europe\'s security architecture was being decided directly between Washington and Moscow. This was followed by plans for another meeting in Budapest, with Trump again positioning himself as the central arbiter of the conflict.^51^

A similar dynamic played out with China. Amid an ongoing trade war and heightened tensions over Taiwan, Trump pursued a personal relationship with Xi Jinping as the primary vehicle for managing the relationship. During a meeting with the Australian Prime Minister in October 2025, Trump expressed high confidence that his personal rapport with Xi could manage tensions, including the threat of an invasion of Taiwan.^52^ He went so far as to claim that Xi had personally assured him China would not invade Taiwan while he was in office.^53^ This statement is a paradigmatic example of the new approach: U.S. policy and regional stability were made to rest not on established deterrence, treaties, or verifiable actions, but on a private, verbal assurance between two leaders.

It is my assessment that this approach creates a significant moral hazard for adversaries. By signaling that the most critical geopolitical outcomes---the borders of Ukraine, the security of Taiwan---are negotiable in direct, one-on-one meetings with the U.S. president, the President_USA object creates a powerful incentive for these adversaries to manufacture crises. An ongoing war or heightened military pressure are no longer simply aggressive actions; they become valuable bargaining chips to be brought to the summit table. This dynamic risks rewarding aggressive behavior with a direct line to the center of American power and the possibility of a favorable settlement. The long-term effect is a more dangerous and unstable world, as adversaries are implicitly encouraged to escalate tensions to force a \"deal.\" This further inflates the geopolitical_volatility_index and undermines the very global stability the President_USA object is traditionally tasked with ensuring.

#### **System State Change Analysis (2.2)**

// Function Call: Bilateral summit with Putin on Ukraine, bypassing allies.\
attemptGrandBargain(President_USA, Putin, \"Ukraine War Settlement\")\
// Returned State Change Report:\
{\
geopolitical_volatility_index: +20,\
trust.allies: -15,\
legitimacy.international: -15,\
power.soft_power: -10,\
relations\[European Allies\]: -10\
}

### 2.3. Deconstruction of the Globalist Agenda: The Void in Global Leadership

In the second term, I observed the systematic implementation of the \"America First\" ideology through a series of executive actions designed to withdraw the United States from international obligations and institutions. This deliberate retreat from global leadership created a vacuum, particularly in multilateral forums, which strategic competitors like China were well-positioned to fill.

Within hours of his inauguration in January 2025, President Trump signed an executive order to once again initiate the U.S. withdrawal from the World Health Organization (WHO). The order cited the WHO\'s mishandling of the COVID-19 pandemic and its \"inability to demonstrate independence\" from China as justification.^54^ This action, a repeat of a move from his first term that was reversed by the subsequent administration, signaled a definitive U.S. abdication of leadership in global public health, even as the world was still grappling with the lessons of the pandemic.^57^

This was accompanied by another executive order pausing all U.S. foreign development assistance for a 90-day review to ensure alignment with the \"America First\" foreign policy.^56^ This move threatened to disrupt critical health, development, and humanitarian programs worldwide and signaled a broader retreat from the use of foreign aid as a key instrument of U.S. soft power and influence. The administration\'s stated view was that the \"foreign aid industry and bureaucracy are not aligned with American interests\".^56^

This self-imposed isolation created a significant strategic opportunity for China. As analyses from the period noted, a U.S. partial or total withdrawal from international organizations creates a vacuum that \"Beijing will be keen to exploit\".^58^ With the U.S. absent or disengaged, China could more effectively advance its own vision for global governance. This includes promoting its Global Security Initiative (GSI) as an alternative to U.S. military alliances, shaping international standards for emerging technologies like artificial intelligence, and positioning itself as the indispensable partner for developing nations in the green energy transition.^58^ The President_USA object, by actively dismantling the tools of American soft power and multilateral engagement, was effectively ceding the playing field to its primary global competitor.

## Part III: A Lexicon of Diplomatic Disruption

A defining characteristic of the Trump administrations has been the use of highly personal, often critical, and sometimes insulting language toward foreign leaders, including close allies. This stands in stark contrast to traditional diplomatic norms and has had a tangible impact on bilateral relations and the cohesion of international alliances. The following is a non-exhaustive catalogue of such instances.

### Allies in Europe

- **Angela Merkel (Germany):** The former German Chancellor was a frequent target. Trump reportedly referred to her as \"that b\*\*\*\* Merkel\" and a \"loser\" after she experienced political setbacks.^59^ He also used the derogatory term \"krauts\" to describe Germans.^59^ He publicly stated Merkel \"should be ashamed of herself\" for her refugee policy, which he claimed was \"ruining Germany\".^59^ During their first meeting, he appeared to ignore requests for a handshake.^61^ Years later, he continued to scorn her legacy, particularly her \"open-door\" refugee policy and support for the Nord Stream 2 pipeline, in front of her successor.^62^

- **Theresa May (United Kingdom):** The former British Prime Minister was also reportedly called a \"loser\" and viewed as a \"dead woman walking\" after losing her parliamentary majority in a snap election.^60^ Trump publicly stated that her Brexit deal was a \"disaster\" because she ignored his advice and that it would \"kill\" any future U.S.-UK trade deal.^63^ He also commented that under her leadership, the UK was \"losing your culture\".^63^

- **Emmanuel Macron (France):** The French President was labeled \"very, very nasty\" and \"insulting\" for his comment that NATO was experiencing \"brain dead\".^65^ At a G7 summit, Trump dismissed Macron\'s explanation for his early departure as \"wrong,\" calling him a \"publicity-seeking President\".^66^ Other interactions included a prolonged, tense handshake where Trump appeared to physically dominate the exchange ^67^ and public humiliation at a Gaza summit where Macron was chided for not standing behind him on stage.^68^ Trump also recounted threatening Macron with a 100% tariff on French wine to block a French tax on American tech companies.^69^

- **Sadiq Khan (Mayor of London):** Trump has repeatedly attacked the Mayor of London, calling him \"among the worst mayors in the world\" and claiming he has done a \"terrible job\" on crime and immigration.^70^ He admitted to asking that Khan not be invited to a state banquet during his UK visit.^71^

- **European Union:** On the eve of his 2018 summit with Vladimir Putin, Trump described the European Union as a \"foe\" in terms of trade.^73^

### Allies in North America

- **Justin Trudeau (Canada):** The Canadian Prime Minister has been a frequent target. Trump has called him \"two-faced\" ^65^, \"very dishonest & weak\" ^17^, and a \"loser\" who has \"destroyed\" Canada with \"radical left\" policies.^74^ Following Trudeau\'s resignation, Trump sarcastically suggested Canada should become the \"51st State\" of the U.S., referring to Trudeau as its \"governor\".^63^

### Allies in the Indo-Pacific

- **Malcolm Turnbull (Australia):** Trump engaged in an acrimonious 2017 phone call with the former Australian Prime Minister over a refugee deal, calling it a \"bad deal\" that would make him look like a \"dope\" and stating the call was the \"most unpleasant\" of his day.^76^ Years later, he lashed out on social media, calling Turnbull a \"weak and ineffective leader\" who \"never understood what was going on in China\".^76^

- **Kevin Rudd (Australian Ambassador):** During a 2025 White House meeting, Trump was made aware of past comments in which Rudd, a former Prime Minister, had called him a \"village idiot\" and a \"traitor to the West\".^77^ Trump confronted Rudd directly in the meeting, stating, \"I don\'t like you either --- and I probably never will\".^77^

- **Shinzo Abe (Japan):** At a G7 summit, Trump reportedly told the late Japanese Prime Minister, \"Shinzo, you don\'t have this problem \[migration\], but I can send you 25 million Mexicans and you\'ll be out of office very soon\".^79^

### Other Leaders and Nations

- **General Insults:** In a widely reported 2018 incident, Trump referred to Haiti, El Salvador, and African nations as \"shithole countries\".^81^ He has also referred to Mexico sending \"rapists\" and called China\'s trade practices a \"rape\" of the U.S. economy.^81^

- **Various Leaders:** During summits, Trump has engaged in numerous awkward or insulting exchanges. At a Gaza summit, he publicly humiliated UK Prime Minister Keir Starmer, snubbed Egyptian President Abdel Fatah al-Sisi\'s handshake, and took a jab at Canadian Prime Minister Mark Carney.^68^ He also appeared impatient with a West African leader\'s speech, asking him to just state his name and country to save time.^82^

## Conclusion: The Net Assessment and Final State of the Object

### Synthesis of Findings

My analysis of the President_USA object across two terms under Donald J. Trump reveals a fundamental transformation of the institution\'s function and standing. The object\'s operational logic shifted from that of a predictable, alliance-leading, system-maintaining entity to that of a volatile, transactional, and system-disrupting one. The core programming of \"America First\" prioritized perceived short-term, bilateral gains over the long-term health of the multilateral, rules-based international order that the office had constructed and maintained for over seven decades.

The consistent disparagement of allies and the simultaneous validation of authoritarian rivals resulted in a quantifiable transfer of legitimacy and soft power from the United States to its competitors. While transactional \"wins,\" such as compelling NATO allies to commit to significantly higher defense spending, were achieved, these successes were Pyrrhic. They were secured through methods that eroded the foundational trust and cohesion of the alliances themselves, transforming them from partnerships of shared values into conditional, fee-for-service arrangements. The introduction of radical uncertainty as a negotiating tactic increased the geopolitical_volatility_index to historically high levels, forcing both allies and adversaries into a constant state of reactive crisis management and undermining strategic stability.

By the end of the period under review, the President_USA object has been fundamentally altered. Its methods, properties, and core purpose have been redefined in ways that present a profound and lasting challenge to the future of American foreign policy and the global order.

### Table 2: President_USA Variable Trajectory (2017-Present)

The following table summarizes my assessment of the cumulative changes to the object\'s key variables, representing the final \"running total\" of the institutional transformation based on the model\'s calculations.

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Variable**                        **Component**           **Initial Value (Jan 2017)**   **Final Value (Present)**   **Net Change**   **Key Drivers of Change**
  ----------------------------------- ----------------------- ------------------------------ --------------------------- ---------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **legitimacy**                      domestic                55                             55                          0                Domestic legitimacy remained highly polarized but was not the primary variable affected by the foreign policy actions modeled.

                                      international           80                             50                          -30              Siding with adversaries over allies (Helsinki ^28^); withdrawal from international agreements (Paris Accord, WHO ^32^); erratic policy shifts.

  **power**                           soft_power              75                             30                          -45              Rejection of \"globalism\" ^35^; public criticism of allies ^17^; retreat from leadership on global issues like climate and health.

  **trust**                           allies                  85                             20                          -65              Questioning of Article 5 ^10^; personal attacks on leaders ^17^; unpredictable policy reversals (Ukraine ^42^); bypassing allies in negotiations with adversaries.

                                      domestic_institutions   60                             40                          -20              Publicly questioning and contradicting intelligence agencies ^28^; use of government apparatus for perceived political ends.

  **alliance_cohesion**               NATO                    85                             45                          -40              Constant threats over spending ^23^; public rifts with Germany/France ^13^; de-institutionalization of decision-making.

                                      US-Japan/ROK            80                             65                          -15              Less direct criticism than NATO, but trade disputes ^33^ and unpredictable North Korea policy created friction. AUKUS endorsement in 2nd term provided some stability.^83^

  **economic_leverage**                                       85                             70                          -15              Aggressive use of tariffs created friction and retaliatory measures, reducing cooperative economic action. U.S. remains a powerhouse, but its ability to lead coalitions is diminished.

  **geopolitical_volatility_index**                           25                             90                          +65              The defining feature of the era. Unpredictable policy shifts, threats to withdraw from alliances, and personalized diplomacy created a highly unstable and reactive global environment.
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Long-Term Implications

In my judgment, the lasting impact of this transformation is significant. The degradation of trust in U.S. commitments is not easily reversible and may have permanently fractured the Western alliance system, encouraging strategic autonomy in Europe and Asia. The empowerment of strategic rivals, who were granted legitimacy and saw the U.S. retreat from multilateral leadership, has accelerated the shift toward a more multipolar and contested world order.^58^ Future administrations will inherit a President_USA object whose credibility has been deeply damaged and whose traditional tools of soft power and alliance leadership have been severely blunted. Rebuilding the institutional capital expended during this period will be a generational challenge, requiring a sustained and predictable recommitment to the principles of collective security and multilateral cooperation that were systematically dismantled.

## Appendix: System Class and Function Definitions

The following appendix details the class and function definitions for the object-oriented model I developed for this analysis.

### A.1: Leader Class Definition

/\*\*\
\* Represents a generic national leader in the international system.\
\* This is the base class from which specific leader types, like President_USA, inherit.\
\*/\
class Leader {\
// PROPERTIES\
string name;\
string country;\
string title;\
string alliance; // e.g., \"NATO\", \"None\"\
\
object legitimacy = {\
domestic: integer, // Perceived rightfulness of rule at home (0-100)\
international: integer // Perceived rightfulness of actions abroad (0-100)\
};\
\
object power = {\
hard_power: integer, // Composite score of military and economic coercive capacity\
soft_power: integer // Ability to influence through attraction and persuasion (0-100)\
};\
}

### A.2: President_USA Class Definition

/\*\*\
\* Represents the office of the President of the United States.\
\* Inherits from the base Leader class and adds properties and methods\
\* unique to the U.S. Presidency\'s role in the global system.\
\*/\
class President_USA extends Leader {\
// PROPERTIES (Inherited: name, country=\'USA\', title=\'President\', etc.)\
\
// Additional properties specific to President_USA\
object trust = {\
allies: integer, // Allies\' confidence in U.S. commitments (0-100)\
domestic_institutions: integer // Confidence in institutions like Intelligence Community, DOJ (0-100)\
};\
\
dictionary alliance_cohesion = {\
// Maps alliance names to a cohesion score (0-100)\
// Example: {\"NATO\": 85, \"US-Japan/ROK\": 80}\
};\
\
integer economic_leverage; // Ability to use economic tools for foreign policy goals (0-100)\
\
dictionary relations = {\
// Maps other leader names to a relationship score (-100 to 100)\
// Example: {\"Putin\": 10, \"Trudeau\": -20}\
};\
\
integer geopolitical_volatility_index; // Instability introduced by actions (0-100)\
\
boolean veto_power_UNSC = true; // Static property representing UN Security Council veto.\
}

### A.3: System Function Definitions

> Code snippet

function berateAlly(president, ally, issue) {\
// Publicly criticizes an allied leader, reducing trust and cohesion.\
let changes = {};\
\
if (ally.name!= \"NATO_Allies\") {\
president.relations\[ally.name\] -= 15;\
changes\[\'relations\[\' + ally.name + \'\]\'\] = -15;\
}\
president.trust.allies -= 10;\
changes\[\'trust.allies\'\] = -10;\
\
if (ally.alliance == \"NATO\") {\
president.alliance_cohesion\[ally.alliance\] -= 10;\
changes\'\] = -10;\
}\
\
president.power.soft_power -= 5;\
changes\[\'power.soft_power\'\] = -5;\
\
president.geopolitical_volatility_index += 10;\
changes\[\'geopolitical_volatility_index\'\] = +10;\
\
return changes;\
}\
\
function berateAlly_escalated(president, ally, issue) {\
// Represents an intensified version of berateAlly for the second term.\
let changes = {};\
\
president.trust.allies -= 20;\
changes\[\'trust.allies\'\] = -20;\
\
if (ally.alliance == \"NATO\") {\
president.alliance_cohesion\[ally.alliance\] -= 20;\
changes\'\] = -20;\
}\
\
president.power.soft_power -= 10;\
changes\[\'power.soft_power\'\] = -10;\
\
president.geopolitical_volatility_index += 15;\
changes\[\'geopolitical_volatility_index\'\] = +15;\
\
return changes;\
}\
\
function validateAdversary(president, adversary, domestic_institution) {\
// Publicly sides with an adversary over a domestic institution, transferring legitimacy.\
let changes = {};\
\
president.legitimacy.international -= 15;\
changes\[\'legitimacy.international\'\] = -15;\
\
president.trust.domestic_institutions -= 20;\
changes\[\'trust.domestic_institutions\'\] = -20;\
\
president.power.soft_power -= 10;\
changes\[\'power.soft_power\'\] = -10;\
\
president.relations\[adversary.name\] += 10;\
changes\[\'relations\[\' + adversary.name + \'\]\'\] = +10;\
\
// adversary.legitimacy.international is also increased, but not tracked in the President_USA object.\
\
return changes;\
}\
\
function attemptGrandBargain(president, adversary, issue) {\
// Bypasses allied and institutional input for a high-risk, high-reward personal negotiation.\
// This model assumes the \'failed\' path, resulting in instability without a concrete, lasting agreement.\
let changes = {};\
\
president.geopolitical_volatility_index += 20;\
changes\[\'geopolitical_volatility_index\'\] = +20;\
\
president.trust.allies -= 15;\
changes\[\'trust.allies\'\] = -15;\
\
president.legitimacy.international -= 15;\
changes\[\'legitimacy.international\'\] = -15;\
\
president.power.soft_power -= 10;\
changes\[\'power.soft_power\'\] = -10;\
\
// Sidelined allies\' relations are damaged.\
changes\[\'relations\[European Allies\]\'\] = -10;\
\
return changes;\
}

#### Works cited

1.  Worldviews on the United States, alliances, and the changing international order: an introduction, accessed October 21, 2025, [[https://www.spf.org/jpus-insights/spf-worldviews-on-the-united-states-en/woldviews-on-the-united-states001.html]{.underline}](https://www.spf.org/jpus-insights/spf-worldviews-on-the-united-states-en/woldviews-on-the-united-states001.html)

2.  As Obama Years Draw to Close, President and U.S. Seen Favorably in Europe and Asia - Pew Research Center, accessed October 21, 2025, [[https://www.pewresearch.org/global/wp-content/uploads/sites/2/2016/06/Pew-Research-Center-Balance-of-Power-Report-FINAL-June-29-2016.pdf]{.underline}](https://www.pewresearch.org/global/wp-content/uploads/sites/2/2016/06/Pew-Research-Center-Balance-of-Power-Report-FINAL-June-29-2016.pdf)

3.  As Obama Years Draw to Close, President and U.S. Seen Favorably in Europe and Asia, accessed October 21, 2025, [[https://www.pewresearch.org/global/2016/06/29/as-obama-years-draw-to-close-president-and-u-s-seen-favorably-in-europe-and-asia/]{.underline}](https://www.pewresearch.org/global/2016/06/29/as-obama-years-draw-to-close-president-and-u-s-seen-favorably-in-europe-and-asia/)

4.  US Public Support for Alliances at All-Time High, accessed October 21, 2025, [[https://globalaffairs.org/research/public-opinion-survey/us-public-support-alliances-all-time-high]{.underline}](https://globalaffairs.org/research/public-opinion-survey/us-public-support-alliances-all-time-high)

5.  Key findings on how Americans view the U.S. role in the world \| Pew Research Center, accessed October 21, 2025, [[https://www.pewresearch.org/short-reads/2016/05/05/key-findings-on-how-americans-view-the-u-s-role-in-the-world/]{.underline}](https://www.pewresearch.org/short-reads/2016/05/05/key-findings-on-how-americans-view-the-u-s-role-in-the-world/)

6.  Public Uncertain, Divided Over America\'s Place in the World - Pew Research Center, accessed October 21, 2025, [[https://www.pewresearch.org/politics/2016/05/05/public-uncertain-divided-over-americas-place-in-the-world/]{.underline}](https://www.pewresearch.org/politics/2016/05/05/public-uncertain-divided-over-americas-place-in-the-world/)

7.  U.S. Position in the World \| Gallup Historical Trends, accessed October 21, 2025, [[https://news.gallup.com/poll/116350/position-world.aspx]{.underline}](https://news.gallup.com/poll/116350/position-world.aspx)

8.  The 2016 Year in Review at Gallup.com, accessed October 21, 2025, [[https://news.gallup.com/poll/200342/2016-year-review-gallup-com.aspx]{.underline}](https://news.gallup.com/poll/200342/2016-year-review-gallup-com.aspx)

9.  Full article: Allies and partners: US public opinion and relationships in the Indo-Pacific, accessed October 21, 2025, [[https://www.tandfonline.com/doi/full/10.1080/13523260.2025.2522708]{.underline}](https://www.tandfonline.com/doi/full/10.1080/13523260.2025.2522708)

10. For once, Trump stays silent about Nato unity -- and US allies are disappointed, accessed October 21, 2025, [[https://www.theguardian.com/us-news/2017/may/25/trump-nato-speech-unity-brussels-belgium-russia]{.underline}](https://www.theguardian.com/us-news/2017/may/25/trump-nato-speech-unity-brussels-belgium-russia)

11. Trump clashes with German leaders as transatlantic tensions boil over - The Guardian, accessed October 21, 2025, [[https://www.theguardian.com/world/2017/may/30/donald-trump-germany-angela-merkel-election]{.underline}](https://www.theguardian.com/world/2017/may/30/donald-trump-germany-angela-merkel-election)

12. \'That\'s not how it works\': Trump\'s grasp of Nato questioned - The Guardian, accessed October 21, 2025, [[https://www.theguardian.com/world/2017/mar/18/trump-merkel-nato-germany-owe-money-tweet]{.underline}](https://www.theguardian.com/world/2017/mar/18/trump-merkel-nato-germany-owe-money-tweet)

13. Donald Trump lashes out at Germany after Angela Merkel questions U.S. reliability as an ally - National \| Globalnews.ca, accessed October 21, 2025, [[https://globalnews.ca/news/3488188/donald-trump-germany-angela-merkel-ally/]{.underline}](https://globalnews.ca/news/3488188/donald-trump-germany-angela-merkel-ally/)

14. Trump, Merkel \'Get Along Very Well,\' White House Says - Radio Free Europe, accessed October 21, 2025, [[https://www.rferl.org/a/us-germany-nato-trump-lashes-out-merkel/28518674.html]{.underline}](https://www.rferl.org/a/us-germany-nato-trump-lashes-out-merkel/28518674.html)

15. Trump says he\'ll only tweak U.S.-Canada trade relations - MPR News, accessed October 21, 2025, [[https://www.mprnews.org/story/2017/02/13/watch-canada-trudeau-talks-trade-with-trump-at-white-house]{.underline}](https://www.mprnews.org/story/2017/02/13/watch-canada-trudeau-talks-trade-with-trump-at-white-house)

16. Blame Canada: Trudeau forced on defensive as Trump targets trade - The Guardian, accessed October 21, 2025, [[https://www.theguardian.com/us-news/2017/apr/22/donald-trump-justin-trudeau-us-canada-trade]{.underline}](https://www.theguardian.com/us-news/2017/apr/22/donald-trump-justin-trudeau-us-canada-trade)

17. G7 in disarray after Trump rejects communique and attacks \'weak\' Trudeau - The Guardian, accessed October 21, 2025, [[https://www.theguardian.com/world/2018/jun/10/g7-in-disarray-after-trump-rejects-communique-and-attacks-weak-trudeau]{.underline}](https://www.theguardian.com/world/2018/jun/10/g7-in-disarray-after-trump-rejects-communique-and-attacks-weak-trudeau)

18. G7 - Wikipedia, accessed October 21, 2025, [[https://en.wikipedia.org/wiki/G7]{.underline}](https://en.wikipedia.org/wiki/G7)

19. Trump blasts NATO allies for inaction, accuses Germany of being under Russia\'s control, accessed October 21, 2025, [[https://www.defensenews.com/smr/nato-priorities/2018/07/11/trump-blasts-nato-allies-for-inaction-accuses-germany-of-being-under-russias-control/]{.underline}](https://www.defensenews.com/smr/nato-priorities/2018/07/11/trump-blasts-nato-allies-for-inaction-accuses-germany-of-being-under-russias-control/)

20. Trump kicks off NATO summit with jab at Germany - CBS News, accessed October 21, 2025, [[https://www.cbsnews.com/news/donald-trump-nato-germany-captive-to-russia-not-fair-funding-europe-2018-07-11/]{.underline}](https://www.cbsnews.com/news/donald-trump-nato-germany-captive-to-russia-not-fair-funding-europe-2018-07-11/)

21. Trump Declares NATO Victory With Spending Commitments From Allies - VOA, accessed October 21, 2025, [[https://www.voanews.com/a/trump-nato-defense-spending/4479427.html]{.underline}](https://www.voanews.com/a/trump-nato-defense-spending/4479427.html)

22. Trump\'s NATO \| Carnegie Endowment for International Peace, accessed October 21, 2025, [[https://carnegieendowment.org/europe/strategic-europe/2018/07/trumps-nato?lang=en]{.underline}](https://carnegieendowment.org/europe/strategic-europe/2018/07/trumps-nato?lang=en)

23. Trump casts doubt on willingness to defend Nato allies \'if they don\'t pay\' - The Guardian, accessed October 21, 2025, [[https://www.theguardian.com/us-news/2025/mar/07/donald-trump-nato-alliance-us-security-support]{.underline}](https://www.theguardian.com/us-news/2025/mar/07/donald-trump-nato-alliance-us-security-support)

24. \- MODERNIZING U.S. ALLIANCES AND PARTNERSHIPS IN THE INDO-PACIFIC - GovInfo, accessed October 21, 2025, [[https://www.govinfo.gov/content/pkg/CHRG-118shrg57384/html/CHRG-118shrg57384.htm]{.underline}](https://www.govinfo.gov/content/pkg/CHRG-118shrg57384/html/CHRG-118shrg57384.htm)

25. Donald Trump: Foreign Affairs - Miller Center, accessed October 21, 2025, [[https://millercenter.org/president/trump/foreign-affairs]{.underline}](https://millercenter.org/president/trump/foreign-affairs)

26. \'Neither of them wanted to stop\': Trump and Putin enjoy successful \'first date\' - The Guardian, accessed October 21, 2025, [[https://www.theguardian.com/us-news/2017/jul/07/trump-putin-g20-hamburg-meeting-first-date]{.underline}](https://www.theguardian.com/us-news/2017/jul/07/trump-putin-g20-hamburg-meeting-first-date)

27. Trump, Putin held previously undisclosed 1-hour meeting at Hamburg dinner - Euractiv, accessed October 21, 2025, [[https://www.euractiv.com/news/trump-putin-held-previously-undisclosed-1-hour-meeting-at-hamburg-dinner/]{.underline}](https://www.euractiv.com/news/trump-putin-held-previously-undisclosed-1-hour-meeting-at-hamburg-dinner/)

28. At Helsinki Summit, Trump and Putin Become Partners in Destruction - Chatham House, accessed October 21, 2025, [[https://www.chathamhouse.org/2018/07/helsinki-summit-trump-and-putin-become-partners-destruction]{.underline}](https://www.chathamhouse.org/2018/07/helsinki-summit-trump-and-putin-become-partners-destruction)

29. Russia--United States Summit (2018) \| Research Starters - EBSCO, accessed October 21, 2025, [[https://www.ebsco.com/research-starters/history/russia-united-states-summit-2018]{.underline}](https://www.ebsco.com/research-starters/history/russia-united-states-summit-2018)

30. What Deal Did Trump and Xi Strike at the G20?, accessed October 21, 2025, [[https://carnegieendowment.org/posts/2018/12/what-deal-did-trump-and-xi-strike-at-the-g20?lang=en]{.underline}](https://carnegieendowment.org/posts/2018/12/what-deal-did-trump-and-xi-strike-at-the-g20?lang=en)

31. Xi and Trump hold talks at G20 summit - People\'s Daily Online, accessed October 21, 2025, [[https://en.people.cn/n3/2019/0629/c90000-9592791.html]{.underline}](https://en.people.cn/n3/2019/0629/c90000-9592791.html)

32. Donald J. Trump Event Timeline \| The American Presidency Project, accessed October 21, 2025, [[https://www.presidency.ucsb.edu/documents/donald-j-trump-event-timeline]{.underline}](https://www.presidency.ucsb.edu/documents/donald-j-trump-event-timeline)

33. Trump\'s First Trade Deal: The Slightly Revised Korea-U.S. Free Trade Agreement, accessed October 21, 2025, [[https://www.cato.org/free-trade-bulletin/trumps-first-trade-deal-slightly-revised-korea-us-free-trade-agreement]{.underline}](https://www.cato.org/free-trade-bulletin/trumps-first-trade-deal-slightly-revised-korea-us-free-trade-agreement)

34. Remarks by President Trump on the United States-Mexico-Canada Agreement, accessed October 21, 2025, [[https://trumpwhitehouse.archives.gov/briefings-statements/remarks-president-trump-united-states-mexico-canada-agreement/]{.underline}](https://trumpwhitehouse.archives.gov/briefings-statements/remarks-president-trump-united-states-mexico-canada-agreement/)

35. Remarks by President Trump to the 74th Session of the United Nations General Assembly, accessed October 21, 2025, [[https://trumpwhitehouse.archives.gov/briefings-statements/remarks-president-trump-74th-session-united-nations-general-assembly/]{.underline}](https://trumpwhitehouse.archives.gov/briefings-statements/remarks-president-trump-74th-session-united-nations-general-assembly/)

36. Remarks by President Trump to the 73rd Session of the United Nations General Assembly \| New York, NY, accessed October 21, 2025, [[https://trumpwhitehouse.archives.gov/briefings-statements/remarks-president-trump-73rd-session-united-nations-general-assembly-new-york-ny/]{.underline}](https://trumpwhitehouse.archives.gov/briefings-statements/remarks-president-trump-73rd-session-united-nations-general-assembly-new-york-ny/)

37. First impeachment of Donald Trump - Wikipedia, accessed October 21, 2025, [[https://en.wikipedia.org/wiki/First_impeachment_of_Donald_Trump]{.underline}](https://en.wikipedia.org/wiki/First_impeachment_of_Donald_Trump)

38. THE COST OF TRUMP\'S FOREIGN POLICY: DAMAGE AND CONSEQUENCES FOR U.S. AND GLOBAL SECURITY - GovInfo, accessed October 21, 2025, [[https://www.govinfo.gov/content/pkg/CPRT-116SPRT44275/html/CPRT-116SPRT44275.htm]{.underline}](https://www.govinfo.gov/content/pkg/CPRT-116SPRT44275/html/CPRT-116SPRT44275.htm)

39. Marco Rubio: Trump defense deal with NATO is a big, beautiful win for America, accessed October 21, 2025, [[https://it.usembassy.gov/marco-rubio-trump-defense-deal-with-nato-is-a-big-beautiful-win-for-america/]{.underline}](https://it.usembassy.gov/marco-rubio-trump-defense-deal-with-nato-is-a-big-beautiful-win-for-america/)

40. Trump calls increase in NATO defense spending a \"big win\" for Europe, US - YouTube, accessed October 21, 2025, [[https://www.youtube.com/watch?v=V-Xcg6I_qTY]{.underline}](https://www.youtube.com/watch?v=V-Xcg6I_qTY)

41. Trump calls for Ukraine war to halt with Russia in control of occupied territory: \"Leave it the way it is\" - CBS News, accessed October 21, 2025, [[https://www.cbsnews.com/news/trump-russia-ukraine-war-zelenskyy-putin-ceasefire/]{.underline}](https://www.cbsnews.com/news/trump-russia-ukraine-war-zelenskyy-putin-ceasefire/)

42. After Zelenskyy meeting, Trump calls on Ukraine and Russia to 'stop where they are' and end the war, accessed October 21, 2025, [[https://apnews.com/article/trump-zelenskyy-putin-ukraine-tomahawks-ce697e5eda6ce9793b4343499d105a8c]{.underline}](https://apnews.com/article/trump-zelenskyy-putin-ukraine-tomahawks-ce697e5eda6ce9793b4343499d105a8c)

43. In Gaza, and now Ukraine, Donald Trump may be peace activists' greatest ally. That deserves our backing, accessed October 21, 2025, [[https://www.theguardian.com/commentisfree/2025/oct/20/gaza-ukraine-donald-trump-stop-war-peace]{.underline}](https://www.theguardian.com/commentisfree/2025/oct/20/gaza-ukraine-donald-trump-stop-war-peace)

44. Trump says he believes Ukraine can regain all land lost to Russia since 2022 invasion, accessed October 21, 2025, [[https://www.theguardian.com/us-news/2025/sep/23/trump-ukraine-land-lost-russia-nato-oil-imports-un-speech]{.underline}](https://www.theguardian.com/us-news/2025/sep/23/trump-ukraine-land-lost-russia-nato-oil-imports-un-speech)

45. Trump called Russia a \'paper tiger\' because he believes Putin is losing - Atlantic Council, accessed October 21, 2025, [[https://www.atlanticcouncil.org/blogs/ukrainealert/trump-called-russia-a-paper-tiger-because-he-believes-putin-is-losing/]{.underline}](https://www.atlanticcouncil.org/blogs/ukrainealert/trump-called-russia-a-paper-tiger-because-he-believes-putin-is-losing/)

46. Fact-checking Trump\'s comments urging Russia to invade \'delinquent\' NATO members, accessed October 21, 2025, [[https://www.pbs.org/newshour/politics/fact-checking-trumps-comments-urging-russia-to-invade-delinquent-nato-members]{.underline}](https://www.pbs.org/newshour/politics/fact-checking-trumps-comments-urging-russia-to-invade-delinquent-nato-members)

47. Donald Trump Says Canada Should Be \'51st State\' as Justin Trudeau Resigns - People.com, accessed October 21, 2025, [[https://people.com/donald-trump-responds-justin-trudeau-resignation-8769726]{.underline}](https://people.com/donald-trump-responds-justin-trudeau-resignation-8769726)

48. Justin Trudeau Responds To Donald Trump\'s \"Canada 51st State\", \"Governor\" Jibes - NDTV, accessed October 21, 2025, [[https://www.ndtv.com/world-news/justin-trudeau-responds-to-donald-trumps-canada-51st-state-governor-jibes-7441427]{.underline}](https://www.ndtv.com/world-news/justin-trudeau-responds-to-donald-trumps-canada-51st-state-governor-jibes-7441427)

49. Trump to meet Putin in Hungary for talks to end Russia-Ukraine war, accessed October 21, 2025, [[https://indianexpress.com/article/world/trump-to-meet-putin-hungary-resolve-russia-ukraine-war-10311274/]{.underline}](https://indianexpress.com/article/world/trump-to-meet-putin-hungary-resolve-russia-ukraine-war-10311274/)

50. 2025 Russia--United States Summit in Alaska - Wikipedia, accessed October 21, 2025, [[https://en.wikipedia.org/wiki/2025_Russia%E2%80%93United_States_Summit_in_Alaska]{.underline}](https://en.wikipedia.org/wiki/2025_Russia%E2%80%93United_States_Summit_in_Alaska)

51. Zelenskyy says he would join Trump-Putin summit in Hungary if invited -- as it happened, accessed October 21, 2025, [[https://www.theguardian.com/world/live/2025/oct/20/zelenskyy-trump-putin-russia-ukraine-war-eu-france-latest-news-updates]{.underline}](https://www.theguardian.com/world/live/2025/oct/20/zelenskyy-trump-putin-russia-ukraine-war-eu-france-latest-news-updates)

52. Trump says China \'doesn\'t want\' to invade Taiwan and reaffirms trust in Xi - The Guardian, accessed October 21, 2025, [[https://www.theguardian.com/us-news/2025/oct/20/trump-china-taiwan-invasion-xi-jinping]{.underline}](https://www.theguardian.com/us-news/2025/oct/20/trump-china-taiwan-invasion-xi-jinping)

53. Xi\'s Taiwan Promise to Trump Sends Shockwaves Through Global Leadership \| World News, accessed October 21, 2025, [[https://www.youtube.com/watch?v=FfGyeVlmlzQ]{.underline}](https://www.youtube.com/watch?v=FfGyeVlmlzQ)

54. Withdrawing The United States From The World Health Organization - The White House, accessed October 21, 2025, [[https://www.whitehouse.gov/presidential-actions/2025/01/withdrawing-the-united-states-from-the-worldhealth-organization/]{.underline}](https://www.whitehouse.gov/presidential-actions/2025/01/withdrawing-the-united-states-from-the-worldhealth-organization/)

55. Trump issues order to withdraw US from WHO - CIDRAP - University of Minnesota, accessed October 21, 2025, [[https://www.cidrap.umn.edu/covid-19/trump-issues-order-withdraw-us-who]{.underline}](https://www.cidrap.umn.edu/covid-19/trump-issues-order-withdraw-us-who)

56. Overview of President Trump\'s Executive Actions on Global Health - KFF, accessed October 21, 2025, [[https://www.kff.org/global-health-policy/overview-of-president-trumps-executive-actions-on-global-health/]{.underline}](https://www.kff.org/global-health-policy/overview-of-president-trumps-executive-actions-on-global-health/)

57. Trump Administration Submits Notice of U.S. Withdrawal from the World Health Organization Amid COVID-19 Pandemic \| American Journal of International Law \| Cambridge Core, accessed October 21, 2025, [[https://www.cambridge.org/core/journals/american-journal-of-international-law/article/trump-administration-submits-notice-of-us-withdrawal-from-the-world-health-organization-amid-covid19-pandemic/6EE130BFAFE5654D59F948E146E24478]{.underline}](https://www.cambridge.org/core/journals/american-journal-of-international-law/article/trump-administration-submits-notice-of-us-withdrawal-from-the-world-health-organization-amid-covid19-pandemic/6EE130BFAFE5654D59F948E146E24478)

58. Trump\'s \'America First\' foreign policy will accelerate China\'s push for global leadership, accessed October 21, 2025, [[https://www.chathamhouse.org/2024/11/trumps-america-first-foreign-policy-will-accelerate-chinas-push-global-leadership]{.underline}](https://www.chathamhouse.org/2024/11/trumps-america-first-foreign-policy-will-accelerate-chinas-push-global-leadership)

59. Donald Trump Called Angela Merkel \'That B\*\*\*\*\' and \'Kraut\': Book \..., accessed October 21, 2025, [[https://www.newsweek.com/donald-trump-angela-merkel-insult-kraut-book-1609917]{.underline}](https://www.newsweek.com/donald-trump-angela-merkel-insult-kraut-book-1609917)

60. Trump called May and Merkel \'losers\' after their political setbacks, ex \..., accessed October 21, 2025, [[https://www.theguardian.com/us-news/2020/jul/01/donald-trump-theresa-may-angela-merkel-setbacks]{.underline}](https://www.theguardian.com/us-news/2020/jul/01/donald-trump-theresa-may-angela-merkel-setbacks)

61. Trump​ appears to ignore requests for a handshake with Angela Merkel​ - YouTube, accessed October 21, 2025, [[https://www.youtube.com/watch?v=uLfukuEutIU]{.underline}](https://www.youtube.com/watch?v=uLfukuEutIU)

62. Trump scorns Merkel legacy during new German chancellor\'s White House visit \| Germany, accessed October 21, 2025, [[https://www.theguardian.com/world/2025/jun/05/trump-scorns-angela-merkel-legacy-during-new-german-chancellors-white-house-visit-friedrich-merz]{.underline}](https://www.theguardian.com/world/2025/jun/05/trump-scorns-angela-merkel-legacy-during-new-german-chancellors-white-house-visit-friedrich-merz)

63. How Trump undermined Theresa May \| Brookings, accessed October 21, 2025, [[https://www.brookings.edu/articles/how-trump-undermined-theresa-may/]{.underline}](https://www.brookings.edu/articles/how-trump-undermined-theresa-may/)

64. Trump attacks May as \'foolish\' in growing ambassador row - YouTube, accessed October 21, 2025, [[https://www.youtube.com/watch?v=yZY_mVFR8mg]{.underline}](https://www.youtube.com/watch?v=yZY_mVFR8mg)

65. Trump cuts short Nato summit after fellow leaders\' hot-mic video - The Guardian, accessed October 21, 2025, [[https://www.theguardian.com/us-news/2019/dec/04/trump-describes-trudeau-as-two-faced-over-nato-hot-mic-video]{.underline}](https://www.theguardian.com/us-news/2019/dec/04/trump-describes-trudeau-as-two-faced-over-nato-hot-mic-video)

66. \'Macron always gets it wrong\': Trump slams French Prez, reveals \..., accessed October 21, 2025, [[https://www.youtube.com/watch?v=pDpFDQ-eIiI]{.underline}](https://www.youtube.com/watch?v=pDpFDQ-eIiI)

67. From Macron to Meloni: 5 world leaders who experienced the \'Trump treatment\' at the Gaza summit, accessed October 21, 2025, [[https://timesofindia.indiatimes.com/world/us/from-macron-to-meloni-5-world-leaders-who-experienced-the-trump-treatment-at-the-gaza-summit/articleshow/124554417.cms]{.underline}](https://timesofindia.indiatimes.com/world/us/from-macron-to-meloni-5-world-leaders-who-experienced-the-trump-treatment-at-the-gaza-summit/articleshow/124554417.cms)

68. \'I am the only one that matters\': Trump deals praise and insults at Gaza summit - The Guardian, accessed October 21, 2025, [[https://www.theguardian.com/us-news/2025/oct/14/donald-trump-gaza-summit-praise-insults-world-leaders]{.underline}](https://www.theguardian.com/us-news/2025/oct/14/donald-trump-gaza-summit-praise-insults-world-leaders)

69. Trump puts on heavy French accent to mock Emmanuel Macron - YouTube, accessed October 21, 2025, [[https://www.youtube.com/watch?v=TyrHqJdgU7w]{.underline}](https://www.youtube.com/watch?v=TyrHqJdgU7w)

70. Trump snubs London Mayor Khan, calls him \'one of worst mayors in world\' - YouTube, accessed October 21, 2025, [[https://www.youtube.com/watch?v=v2gaJFJbpH4]{.underline}](https://www.youtube.com/watch?v=v2gaJFJbpH4)

71. Trump says he did not want London mayor at UK state banquet, accessed October 21, 2025, [[https://www.aa.com.tr/en/americas/trump-says-he-did-not-want-london-mayor-at-uk-state-banquet/3692068]{.underline}](https://www.aa.com.tr/en/americas/trump-says-he-did-not-want-london-mayor-at-uk-state-banquet/3692068)

72. Trump Boasts He Blocked Sadiq Khan From State Banquet; \'One Of The Worst Mayors, Didn\'t Want Him...\' - YouTube, accessed October 21, 2025, [[https://www.youtube.com/watch?v=fR0vY99BFZw]{.underline}](https://www.youtube.com/watch?v=fR0vY99BFZw)

73. EU and US will \'always be close friends\', insists Mogherini \| Euractiv, accessed October 21, 2025, [[https://www.euractiv.com/news/eu-and-us-will-always-be-close-friends-insists-mogherini/]{.underline}](https://www.euractiv.com/news/eu-and-us-will-always-be-close-friends-insists-mogherini/)

74. Trudeau \'destroyed\' Canada, says Trump - Anadolu Ajansı, accessed October 21, 2025, [[https://www.aa.com.tr/en/americas/trudeau-destroyed-canada-says-trump/3489365]{.underline}](https://www.aa.com.tr/en/americas/trudeau-destroyed-canada-says-trump/3489365)

75. Trump responds to Trudeau resignation by suggesting Canada merge with U.S. \| CBC News, accessed October 21, 2025, [[https://www.cbc.ca/news/politics/justin-trudeau-resigns-us-donald-trump-tariffs-1.7423756]{.underline}](https://www.cbc.ca/news/politics/justin-trudeau-resigns-us-donald-trump-tariffs-1.7423756)

76. Former Australian PM Malcolm Turnbull says leaders must stand up \..., accessed October 21, 2025, [[https://www.theguardian.com/us-news/2025/mar/10/donald-trump-criticises-former-australian-prime-minister-pm-malcolm-turnbull]{.underline}](https://www.theguardian.com/us-news/2025/mar/10/donald-trump-criticises-former-australian-prime-minister-pm-malcolm-turnbull)

77. \'Village Idiot\': The White House guest who made Donald Trump see red, accessed October 21, 2025, [[https://timesofindia.indiatimes.com/world/us/village-idiot-the-white-house-guest-who-made-donald-trump-see-red/articleshow/124712674.cms]{.underline}](https://timesofindia.indiatimes.com/world/us/village-idiot-the-white-house-guest-who-made-donald-trump-see-red/articleshow/124712674.cms)

78. \'I don't like you and never will\': Donald Trump's awkward confrontation with Australian ambassador in White House -- Watch, accessed October 21, 2025, [[https://timesofindia.indiatimes.com/world/us/i-dont-like-you-and-never-will-donald-trumps-awkward-confrontation-with-australian-ambassador-in-white-house-watch/articleshow/124709564.cms]{.underline}](https://timesofindia.indiatimes.com/world/us/i-dont-like-you-and-never-will-donald-trumps-awkward-confrontation-with-australian-ambassador-in-white-house-watch/articleshow/124709564.cms)

79. 44th G7 summit - Wikipedia, accessed October 21, 2025, [[https://en.wikipedia.org/wiki/44th_G7_summit]{.underline}](https://en.wikipedia.org/wiki/44th_G7_summit)

80. Trump threatened to send 25 million Mexicans to Japan: report \| The Times of Israel, accessed October 21, 2025, [[https://www.timesofisrael.com/trump-threatened-to-send-25-million-mexicans-to-japan-report/]{.underline}](https://www.timesofisrael.com/trump-threatened-to-send-25-million-mexicans-to-japan-report/)

81. Can you match the Donald Trump insult to the country he insulted \..., accessed October 21, 2025, [[https://www.theguardian.com/us-news/2018/jan/12/can-you-match-donald-trump-insult-country-insulted]{.underline}](https://www.theguardian.com/us-news/2018/jan/12/can-you-match-donald-trump-insult-country-insulted)

82. \'Don\'t Have Time\': Trump \'INSULTS\' World Leaders At Oval Office; Tense Moments On Cam, accessed October 21, 2025, [[https://www.youtube.com/watch?v=PwIoRbX9Ljk]{.underline}](https://www.youtube.com/watch?v=PwIoRbX9Ljk)

83. Trump officially endorses AUKUS at White House meeting with Australian prime minister, accessed October 21, 2025, [[https://defensescoop.com/2025/10/20/trump-officially-endorses-aukus-at-white-house-meeting-with-australian-prime-minister/]{.underline}](https://defensescoop.com/2025/10/20/trump-officially-endorses-aukus-at-white-house-meeting-with-australian-prime-minister/)
