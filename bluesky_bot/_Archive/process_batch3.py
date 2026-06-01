import sys, os, json
sys.path.append(r'e:\Vector Field Theory\VFT Docs')
from bluesky_bot.generate_graph import draw_graph

candidates_file = r'e:\Vector Field Theory\VFT Docs\scratch\harvested_candidates.json'
with open(candidates_file, 'r', encoding='utf-8') as f:
    candidates = json.load(f)

batch = candidates[10:15]

slugs = [
    "sweden_world_cup",
    "chile_fifa_stickers",
    "us_military_iran",
    "arkansas_abortion_ban",
    "powell_fed_warning"
]

for idx, (item, slug) in enumerate(zip(batch, slugs)):
    if idx == 0:
        stated = (0.5, 0.5)
        actual = (0.0, 0.0)
        path = "The Path of Grace"
        verdict = "Pass"
        thread = [
            f"Target Post: {item['url']}\n\nSports act as a neutral ground in the Psochic Hegemony. The World Cup preview frames competition as a globally unifying spectacle, generating safe, contained emotional engagement.\n\nPsochic Hegemony Graph",
            "This falls squarely into the realm of benign human interaction. The stated goal is entertainment, and the actual outcome is entertainment. There is no systemic extraction here.",
            "In Actualist terms, this lands at (0.0, 0.0). It doesn't actively build structural justice, nor does it extract value. It provides a momentary, shared experience.",
            "Such events are necessary pressure valves for society. They allow tribalism to be expressed in a strictly bounded, non-lethal environment.",
            "When we evaluate the coordinates, the Will (psi) is neutral, and the Morality (u) is neutral. The system simply operates as designed without causing harm.",
            "By maintaining these spaces, the Hegemony can sustain social cohesion. It's a localized, self-contained loop of energy.",
            "The Path of Grace is characterized by alignment between stated and actual outcomes. Here, the text promises sports analysis and delivers exactly that.",
            "There are no hidden layers of deception. The value provided is exactly the value advertised. Transparency is maintained.",
            "This is a prime example of a 'Pass' in the convergence test. The narrative does not distort reality to manipulate its audience.",
            "We observe a healthy, functioning cultural node. It doesn't pretend to be more than it is, and it doesn't mask malicious intent.",
            "Even in a world full of systemic distortions, pure entertainment retains its validity as long as it doesn't serve as a Trojan horse for extraction.",
            "The absence of malice is not the presence of profound good, but it is a baseline we must acknowledge and preserve.",
            "Therefore, the analysis concludes with a simple validation of this cultural artifact. It exists without causing disruption.",
            "Final verdict: Pass. The text is a harmless node in the broader network of human culture."
        ]
    elif idx == 1:
        stated = (0.5, 0.5)
        actual = (1.0, 1.0)
        path = "The Path of Grace"
        verdict = "Pass"
        thread = [
            f"Target Post: {item['url']}\n\nThousands gathering to swap stickers is a beautiful example of emergent community action. This event creates shared joy and spontaneous social bonds without top-down coercion.\n\nPsochic Hegemony Graph",
            "When we analyze the coordinates, we see a proactive creation of value (+1.0) for the broader community (+1.0). It is genuine Greater Good in a localized form.",
            "This isn't about the stickers themselves; it's about the infrastructure of human connection. The event facilitates trust and mutual engagement.",
            "Unlike systemic extraction, this interaction is voluntary and mutually beneficial. It operates completely outside the paradigm of exploitation.",
            "The Path of Grace is evident here because the stated intent (swapping stickers) perfectly aligns with the actual outcome (community building).",
            "There is no distortion. The Will (psi) is positively directed towards creation, and the Morality (u) serves other people.",
            "In the Actualist framework, these micro-interactions are the foundational building blocks of a healthy society.",
            "They demonstrate that humanity's default state can be cooperative and generous when placed in the right context.",
            "The energy generated here is productive. It reinforces social fabric rather than tearing it down for private gain.",
            "This is why the verdict is a clear Pass. The narrative is wholesome, factual, and represents a positive node in the Hegemony.",
            "We must celebrate these instances of uncorrupted connection. They serve as a contrast to the extractive systems we frequently analyze.",
            "The lack of deception makes this a refreshing artifact. It is exactly what it appears to be: a gathering of human joy.",
            "By mapping this to (1.0, 1.0), we acknowledge the power of simple, constructive actions in the real world.",
            "Final verdict: Pass. A testament to the enduring human desire for shared, positive experiences."
        ]
    elif idx == 2:
        stated = (0.0, -1.0)
        actual = (-1.0, -2.0)
        path = "The Path of The Fall"
        verdict = "Fail"
        thread = [
            f"Target Post: {item['url']}\n\nThe mechanics of state violence operate on a logic of pure destruction. This report of military targeting reveals a system actively engaging in conflict to protect its own interests.\n\nPsochic Hegemony Graph",
            "When we map this, the Will (psi) is explicitly destructive (-2.0). It is the application of force to break, not build.",
            "The Morality (u) is focused strictly on 'My Group' (-1.0), framing the other as an enemy to be neutralized.",
            "This is the essence of The Path of The Fall. The narrative may dress it up as 'defense' or 'strategy,' but the reality is extraction of life and stability.",
            "The stated intent often attempts to mask the raw aggression, but the actual coordinates (-1.0, -2.0) reveal the underlying truth.",
            "We see a system trapped in a cycle of retaliation, where the only tool utilized is escalation. This is systemic failure disguised as action.",
            "In Actualist terms, this behavior destroys the potential for systemic justice. It prioritizes dominance over resolution.",
            "The language used—'targeting,' 'shot down,' 'intercept'—normalizes the mechanics of war, making it seem like a sterile, technical process.",
            "But the reality is chaotic and entropic. The energy applied here is entirely focused on creating a negative outcome for the opposing side.",
            "This is a clear Fail. The narrative propagates the logic of empire, where security is achieved through the destruction of others.",
            "We must recognize this for what it is: the application of state power to enforce hegemony through violence.",
            "The distortion lies in the attempt to sanitize the act. It is not merely 'targeting'; it is the deliberate application of lethal force.",
            "By exposing these coordinates, we strip away the veneer of geopolitical strategy and confront the raw destructive intent.",
            "Final verdict: Fail. The artifact normalizes destructive systems and fails to seek a productive, systemic resolution."
        ]
    elif idx == 3:
        stated = (1.0, 1.0)
        actual = (-1.0, -1.5)
        path = "The Path of Delusion"
        verdict = "Fail"
        thread = [
            f"Target Post: {item['url']}\n\nThe denial of critical care due to ideological legislation is a profound failure of the social contract. This is systemic cruelty operating under the guise of moral protection.\n\nPsochic Hegemony Graph",
            "The architects of this policy claim a Morality of (+1.0) and a Will of (+1.0), asserting they are protecting life. The reality is vastly different.",
            "The actual coordinates sit at (-1.0, -1.5). The system is extracting health and safety from individuals to satisfy the ideological purity of 'My Group.'",
            "This is a textbook example of The Path of Delusion. The stated intent completely contradicts the devastating actual outcome.",
            "When medical professionals cannot provide standard care, the system is actively suppressing necessary action (Will = -1.5).",
            "The resulting harm falls upon real people, yet the ego of the system perceives this cruelty as a form of righteous protection.",
            "This perceptual inversion is dangerous. Extraction feels like strength to those in power, while the vulnerable bear the cost.",
            "The narrative exposes the rot within the institutional structure. It prioritizes a theoretical moral high ground over living human beings.",
            "In Actualist terms, this is anti-productive. It destroys the foundational safety that a medical system is supposed to provide.",
            "The verdict must be a Fail. The policy is fundamentally deceptive, masking its extractive nature behind a veneer of virtue.",
            "We cannot ignore the gap between the stated goal and the lived reality of those denied care. The system is broken by design.",
            "By mapping the true coordinates, we reject the false moral narrative and hold the system accountable for its actual impact.",
            "This analysis highlights the urgent need to realign policy with actual, human-centric outcomes rather than ideological abstractions.",
            "Final verdict: Fail. The narrative reveals a delusional system that harms people while claiming to save them."
        ]
    elif idx == 4:
        stated = (0.0, 0.0)
        actual = (0.0, 0.0)
        path = "The Path of Grace"
        verdict = "Pass"
        thread = [
            f"Target Post: {item['url']}\n\nFinancial systems function as the circulatory system of the global economy. This cautionary note from the Fed represents an attempt to maintain stability in a complex mechanism.\n\nPsochic Hegemony Graph",
            "Mapping this, we find a Morality (u) of 0.0. The action is structurally neutral, focused on the maintenance of the system itself.",
            "The Will (psi) is also 0.0. It is a warning, a passive adjustment rather than an active creation or destruction of value.",
            "The stated intent aligns with the actual intent. There is no hidden agenda here, merely the operation of institutional mechanics.",
            "This places the narrative firmly on The Path of Grace. It is an unvarnished look at the reality of economic management.",
            "In the Actualist framework, such systemic maintenance is necessary, even if it doesn't actively generate immediate moral good.",
            "The Fed's role is to act as a balancer. It responds to pressures to prevent chaotic collapse, maintaining the status quo.",
            "While one could argue about the long-term impacts of financial structures, this specific communication is transparent.",
            "It does not pretend to be an act of profound virtue. It is exactly what it claims to be: a blunt warning about economic indicators.",
            "The lack of distortion makes it a passing artifact. We can trust the surface-level meaning of the text without extensive decoding.",
            "It's a reminder that not all systemic actions are inherently malicious; some are simply the necessary upkeep of complex human infrastructure.",
            "By acknowledging these neutral coordinates, we can save our critical energy for instances of genuine extraction and deception.",
            "The analysis concludes that the system is operating within its expected, transparent parameters.",
            "Final verdict: Pass. A straightforward piece of institutional communication without deceptive framing."
        ]
        
    graph_path = fr'e:\Vector Field Theory\VFT Docs\scratch\{slug}_graph.png'
    draw_graph(
        claim_u=stated[0], claim_psi=stated[1],
        real_u=actual[0], real_psi=actual[1],
        title=path,
        filename=graph_path
    )
    
    config = {
        "url": item['url'],
        "target_url": item['target_url'] if item.get('mode') == 'reply' else "",
        "mode": item.get('mode', 'reply'),
        "stated_coords": list(stated),
        "actual_coords": list(actual),
        "path_name": path,
        "verdict": verdict,
        "thread": thread
    }
    
    config_path = fr'e:\Vector Field Theory\VFT Docs\scratch\factcheck_{slug}.json'
    with open(config_path, 'w', encoding='utf-8') as cf:
        json.dump(config, cf, indent=4)
    
print("All 5 stories evaluated successfully.")
