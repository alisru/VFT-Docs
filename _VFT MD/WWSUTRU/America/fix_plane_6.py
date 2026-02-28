import re

file_path = r'e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America\Trump_American_Kanon_Plane_6_Cause.md'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

def replace_line(prefix, new_line):
    global text
    pattern = re.compile(re.escape(prefix) + r'.*', re.MULTILINE)
    text = pattern.sub(new_line, text)

# P6.1
replace_line('| Cause.Who.Who |', '| Cause.Who.Who | **The Puritan** | -1 | -1.0 | +0.0 | **Quote:** *"I don\'t think I have."* — Responding to whether he has ever asked God for forgiveness, Family Leadership Summit, July 2015.<br><br>The Puritan ideal demands submission to a higher moral order and strict communal discipline. Trump is publicly and proudly hedonistic, materialistic, and transactional. By explicitly denying the need for divine or communal forgiveness, he fundamentally violates the core premise of the archetype. |')
replace_line('| Cause.Who.What |', '| Cause.Who.What | **The Slave** | -1 | -0.9 | +0.5 | **Quote:** *"I am the most persecuted person in the history of our country."* — Rally in Texas, explicitly claiming the narrative of ultimate subjugation and victimhood, October 2022.<br><br>Trump operates entirely from a position of absolute privilege and assumed mastery. By utilizing the language of extreme subjugation to describe his own political friction, he corrupts the historical reality of the archetype, appropriating the profound grievance of the enslaved to fuel the political grievances of the privileged. |')
replace_line('| Cause.Who.Cause |', '| Cause.Who.Cause | **The Indigenous** | -1 | -0.8 | +0.0 | **Quote:** *"They don\'t look like Indians to me, and they don\'t look like Indians to Indians."* — Testimony before Congress regarding Native American casino competitors, 1993, demonstrating a purely transactional engagement with Indigenous identity.<br><br>Trump possesses zero connection to the Indigenous archetype—the deep, ancient alignment with the physical reality of the specific land, long predating the legal concept of the \'Nation.\' He views land purely as a commodity to be developed, bordered, and monetized (real estate, border walls), rather than a Sacred entity commanding respect and stewardship. His aesthetic and policies completely exclude and commodify the Indigenous perspective, violating the foundational connection to the land. |')

# P6.2
replace_line('| Cause.Where.Who |', '| Cause.Where.Who | **Plymouth Rock** | -1 | -1.0 | -0.5 | **Quote:** *"I could stand in the middle of Fifth Avenue and shoot somebody, and I wouldn\'t lose any voters."* — Rally in Iowa, January 2016, demonstrating a bond based on a destructive cult of personality rather than a shared moral covenant.<br><br>Plymouth Rock symbolizes the ideal of the covenant—the foundational agreement to form a civil body politic bound by shared moral and religious purpose. Trump operates entirely against the logic of the covenant. The quote illustrates a transactional bond based on absolute amoral loyalty (immunity to murder) which profoundly violates the concept of a shared ethical foundation required by the ideal. |')
replace_line('| Cause.Where.Why |', '| Cause.Where.Why | **The Frontier (Historical)** | -1 | -0.9 | +0.5 | **Quote:** *"We are going to build a great border wall."* — Constant campaign promise, redefining the American frontier not as an open expanse to be explored, but as a hostile perimeter to be fortified.<br><br>The Historical Frontier ideal champions the open expanse, rugged individualism, and the optimistic pushing of boundaries. Trump completely subverts this ideal, replacing the infinite openness of the frontier with a terrified obsession over physical fortification and absolute closure. He replaces the pioneer\'s gaze toward the horizon with the siege mentality of the fortress. |')
replace_line('| Cause.Where.Cause |', '| Cause.Where.Cause | **Jamestown** | -1 | -0.8 | -0.8 | **Quote:** *"I’ve always won, and I’m going to continue to win."* — Interview with Time Magazine, April 2016.<br><br>Jamestown represents the brutal, profit-driven reality of the American origin, but crucially, one defined by near-total catastrophic failure, starvation, and desperate perseverance. Trump shares the profit motive but violently denies the vulnerability that defined the Jamestown reality. He presents a narrative of flawless, effortless success, rendering the actual harsh sacrifice of the origin fundamentally invisible. |')

# P6.3
replace_line('| Cause.What.Where |', '| Cause.What.Where | **Federalism** | -1 | -0.8 | +0.6 | **Quote:** *"When somebody is the president of the United States, the authority is total. And that\'s the way it\'s got to be."* — Combative press briefing asserting Federal supremacy over state governors regarding COVID lockdowns, April 2020.<br><br>Federalism idealizes the constitutional division and balance of power between the states and the central government to prevent tyranny. Trump fundamentally rejects this balance whenever it impedes his Will, explicitly asserting "total" authority that annihilates the concept of state sovereignty. Federalism is not a principle to him; it is merely an obstacle he claims the power to bypass. |')
replace_line('| Cause.What.How |', '| Cause.What.How | **Judicial Review** | -1 | -0.9 | +0.5 | **Quote:** *"This so-called judge... essentially takes law enforcement away from our country, is ridiculous and will be overturned!"* — Twitter Post attacking U.S. District Judge James Robart, February 2017.<br><br>Judicial Review relies on the acceptance of independent courts interpreting the law neutrally. Trump fundamentally attacks the legitimacy of Judicial Review itself, framing judgments against him not as legal disagreements, but as illegitimate, partisan attacks by "so-called" judges. He appoints judges to gain power, but actively attacks the concept of independent judicial constraint. |')

# P6.4
replace_line('| Cause.Why.Who |', '| Cause.Why.Who | **Religious Freedom** | -1 | -1.0 | +0.6 | **Quote:** *"Donald J. Trump is calling for a total and complete shutdown of Muslims entering the United States."* — Campaign Statement, December 2015.<br><br>The ideal of Religious Freedom demands absolute state neutrality regarding faith. While Trump delivered policy victories to his specific religious base (Evangelicals), his call to explicitly ban individuals from the nation based entirely on their religion represents a catastrophic violation of the American Kanon\'s foundational definition of religious liberty. |')
replace_line('| Cause.Why.Why |', '| Cause.Why.Why | **Liberty** | -1 | -1.0 | +0.6 | **Quote:** *"We\'re going to open up our libel laws, so when they write purposely negative and horrible and false articles, we can sue them and win lots of money."* — Campaign Rally, February 2016.<br><br>The Kanonic ideal of Liberty includes structurally guaranteed freedoms (like the press) that protect the citizenry from power. Trump champions a corrupted, negative liberty: absolute freedom for himself to act without constraint, combined with a desire to legally restrict the liberty of those who criticize him. He seeks to weaponize the state to restrict the civil liberties of his opponents. |')
replace_line('| Cause.Why.Cause |', '| Cause.Why.Cause | **Fear of Tyranny** | -1 | -1.0 | +0.8 | **Quote:** *"They\'re not after me. They\'re after you. I\'m just in the way."* — Campaign Rally slogan.<br><br>The American Foundation is built on an intense, structural fear of the executive tyrant. Trump brilliantly weaponizes this fear conceptually, but he himself is the exact manifestation of the executive overreach the Founders feared. He utilizes the rhetoric of anti-tyranny to justify his own tyrannical actions, violating the core Kanonic imperative to limit sovereign power. |')

# P6.5
replace_line('| Cause.How.Cause |', '| Cause.How.Cause | **War** | -1 | -0.8 | +0.8 | **Quote:** *"Will someone from his depleted and food starved regime please inform him that I too have a Nuclear Button... and my Button works!"* — Twitter Post regarding North Korea, January 2018.<br><br>The ideal of War in the Kanon requires solemn deliberation, structural mobilization, and the gravest responsibility. Trump treats the threat of total nuclear conflict as a flippant, egotistical boast on social media, using annihilation as a chaotic negotiation tactic. This entirely degrades the gravity required by the Foundation when confronting the ultimate destructive power of the State. |')

# P6.6
replace_line('| Cause.Cause.Who |', '| Cause.Cause.Who | **The Ancients** | -1 | -0.9 | +0.0 | **Quote:** *"I could be the most presidential person ever, except for maybe Abe Lincoln with his big top hat."* — Rally in Pennsylvania, 2018.<br><br>The Founders built the Republic on the solemn, deeply studied lessons of the collapse of the Roman and Greek republics (The Ancients), desperate to prevent Caesarism. Trump possesses absolute ignorance of this history, lacking any connection to the intellectual tradition that structured the nation. He blindly repeats the exact behavioral profile of the late-Roman demagogue that the Founders studied the Ancients specifically to avoid. |')
replace_line('| Cause.Cause.What |', '| Cause.Cause.What | **The Bible** | -1 | -0.8 | +0.5 | **Quote:** *"It’s a Bible. A very special book. It’s my favorite book."* — Outside St. John\'s Church after clearing Lafayette Square with tear gas, June 2020.<br><br>The ideal of The Bible in the Kanon represents a moral compass of charity, humility, and justice. Trump’s relationship with it is entirely aesthetic and instrumental. He utilizes it purely as a prop to signal tribal allegiance, successfully convincing millions that he is the fiercely unapologetic defender of the physical book, even as he systematically violates the spiritual principles contained within it. |')

# P6.7
replace_line('| Cause.Effect.Who |', '| Cause.Effect.Who | **The Founder** | -1 | -1.0 | +0.8 | **Quote:** *"I am the chosen one."* — Speaking to reporters on the White House lawn, August 2019.<br><br>The ideal of \'The Founder\' (e.g., Washington) is defined by the ultimate, agonizing surrender of absolute power to the structural law of the new Republic. Trump positions himself as the \'Founder\' entirely in a megalomaniacal sense, claiming chosen status while violently attacking the very constitutional structure the original Founders sacrificed to build. He claims the title while actively betraying the action. |')
replace_line('| Cause.Effect.Where |', '| Cause.Effect.Where | **The Monument** | -1 | -0.8 | +0.5 | **Quote:** *"Sad to see the history and culture of our great country being ripped apart with the removal of our beautiful statues and monuments."* — Twitter Post, August 2017 (referencing Confederate memorials).<br><br>The Kanonic Monument exists to unify the nation around its highest shared ideals. Trump weaponizes the aesthetic of The Monument specifically to defend the memorials of the Confederacy (the ultimate traitors to the Kanon). He utilizes monuments not to elevate the unified Republic, but as a deliberate, divisive tool to exacerbate racial cultural friction, completely subverting the unifying purpose of the physical memorial. |')
replace_line('| Cause.Effect.Why |', '| Cause.Effect.Why | **Civil Religion** | -1 | -0.8 | +0.8 | **Quote:** *"God is on our side."* — Frequent campaign sign-off.<br><br>American Civil Religion is designed to be a broad, inclusive spiritual umbrella prioritizing the survival of the Republic. Trump profoundly violates this by transforming it into a narrow, hyper-partisan Christian Nationalism. He claims divine mandate exclusively for his political faction, corrupting the unifying Civic Religion by aggressively weaponizing it to excommunicate half the country from the national soul. |')
replace_line('| Cause.Effect.How |', '| Cause.Effect.How | **Originalism** | 0 | +0.0 | +0.5 | **Quote:** *"We are appointing judges who will interpret the Constitution as written."* — State of the Union Address, February 2020.<br><br>While Trump appointed \'Originalist\' judges, successfully hijacking the intellectual framework of the conservative legal movement, he demonstrates zero personal adherence or intellectual commitment to the ideal of Originalism. He leverages the philosophy entirely instrumentally to secure political victories (like overturning Roe) and secure tribal loyalty, fundamentally viewing judicial philosophy merely as a mechanism for raw power enforcement. |')
replace_line('| Cause.Effect.Cause |', '| Cause.Effect.Cause | **The Burden** | -1 | -1.0 | +0.0 | **Quote:** *"I don\'t take responsibility at all."* — Rose Garden press conference, March 2020.<br><br>The Burden is the horrifying, sobering awareness of the responsibility required to keep the Republic from shattering. Trump explicitly and repeatedly refuses to carry any burden of leadership, assigning all blame outward and claiming absolute immunity from consequence. He violates the most basic psychological requirement of the Executive: the willingness to accept the crushing weight of structural responsibility. |')

replace_line('**Score: 0 / 7**', '**Score: -3 / 7**')

# Need to accurately replace the scores by finding their index or just using split
parts = text.split('**Score: ')
if len(parts) > 7:
    # 6.1
    parts[1] = parts[1].replace('0 / 7**', '-3 / 7**')
    # 6.2
    parts[2] = parts[2].replace('-3 / 7**', '-5 / 7**')
    # 6.3
    parts[3] = parts[3].replace('-3 / 7**', '-5 / 7**')
    # 6.4
    parts[4] = parts[4].replace('+7 / 7**', '+1 / 7**')
    # 6.5
    parts[5] = parts[5].replace('-4 / 7**', '-5 / 7**')
    # 6.6
    parts[6] = parts[6].replace('0 / 7**', '-3 / 7**')
    # 6.7
    parts[7] = parts[7].replace('+2 / 7**', '-6 / 7**')
    
text = '**Score: '.join(parts)

# Fix Totality
text = text.replace('**Plane 6 Score: -1 / 49**', '**Plane 6 Score: -26 / 49**')
text = text.replace('**Plane 6 Percentage: 48.9% Alignment**', '**Plane 6 Percentage: 23.5% Alignment**')

# Replace exact analysis text
old_analysis = """**Analysis:**
Plane 6 is the "Armor of the Idea," focusing heavily on the structural constraints built by the Founders to prevent tyranny (Separation of Powers, The Constitution, Magna Carta, Debate, Compromise, The Press). Predictably, Donald Trump scores extremely poorly on these structural vectors. He views the machinery of the Republic as an impediment to his Will, actively attacking the precise mechanisms engineered to keep the State safe. He is anti-Enlightenment, anti-Compromise, and anti-Precedent.

However, he scores a remarkable, perfect +1 sweep on **Plane 6.4 (The Why of the Foundation)**. He perfectly channels the *emotional engine* of the American Revolution: **Grievance, Fear of Tyranny, Self-Determination, Liberty (as rebellion), and Taxation (as refusal)**. 

Trump aligns deeply with the rebellious energy of the American founding (The Revolutionary, The Reformation), but completely rejects the intellectual architecture designed to contain that energy after the revolution was won (The Framer, The Constitution). He wants the adrenaline of 1776 without the boring, restrictive paperwork of 1787."""

new_analysis = """**Analysis:**
Plane 6 is the "Armor of the Idea," focusing heavily on the structural constraints built by the Founders to prevent tyranny (Separation of Powers, The Constitution, Magna Carta, Debate, Compromise, The Press). When measured strictly against the *Ideal* of each vector, Donald Trump scores catastrophically poor across nearly the entire Foundation plane. He views the machinery of the Republic as an impediment to his Will, actively attacking the precise mechanisms engineered to keep the State safe. He is anti-Enlightenment, anti-Compromise, and anti-Precedent.

His handful of positive alignments (+1) occur essentially where the 'Ideal' demands a disruptive force or embodies raw American instinct disconnected from structural management. He perfectly channels the Revolutionary drive, the Battlefield’s adrenaline, Historical Land Hunger, resistance to Taxation, the instinct to utilize The Militia, decentralized tools of The Reformation, and Geographic isolationism. 

Trump aligns deeply with the raw, rebellious, and acquisitive energy of the American origin, but completely rejects and violently attacks the intellectual architecture designed to contain that energy after the revolution was won (The Framer, The Constitution, Natural Rights). He wants the adrenaline of 1776 without the boring, restrictive paperwork of 1787, proving that raw American Will without Kanonic constraint inevitably seeks to dismantle the Republic."""

text = text.replace(old_analysis, new_analysis)
text = text.replace('**Average Trump υ (Morality):** -0.06', '**Average Trump υ (Morality):** -0.85')
text = text.replace('**Average Trump ψ (Will):** -0.07', '**Average Trump ψ (Will):** +0.10')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated successfully')
