import os
import sys
from generate_graph import draw_graph

def split_text(text, max_len=300):
    if len(text) <= max_len:
        return [text]

    chunks = []
    while text:
        if len(text) <= max_len:
            chunks.append(text)
            break

        split_idx = text.rfind('\n', 0, max_len)
        if split_idx == -1:
            split_idx = text.rfind(' ', 0, max_len)

        if split_idx == -1:
            split_idx = max_len

        chunks.append(text[:split_idx].strip())
        text = text[split_idx:].strip()

    return chunks

title = "LA tops nation in dog attacks on postal workers again"
clean_link = "https://www.latimes.com/california/story/2026-05-29/la-tops-nation-in-dog-attacks-on-postal-workers-again"

# Dry Run Convergence Test on Dog Attacks / Postal Workers
# Claim: Domestic Pet Ownership / Security (+1.0, 0.0) -> A passive good or protective measure for the home.
# Actual: Negligence resulting in community harm (-1.0, -1.0) -> Extraction of safety from public workers due to suppression of responsibility.
claim_u = 1.0
claim_psi = 0.0
real_u = -1.0
real_psi = -1.0

# Generate the graph
draw_graph(claim_u, claim_psi, real_u, real_psi, "Convergence Test: LA Dog Attacks", "dry_run_graph.png")

# Using the Plain English template with Plane Error
post_texts = [
    f"""A classic case of localized negligence passing its costs onto the public architecture.

Subject: {title}
Source: {clean_link}
Evidence Standards: Stated ideal (domestic pet ownership) vs Actions within physical context (community impact).""",

    """The Claim:
The claim of the actors (dog owners) is that their pets are a domestic good, providing companionship or home security without projecting harm into the public sphere.
Stated Judgement: (+1.0, 0.0) — Good Preference""",

    """The Reality:
The evidence shows a systemic failure to maintain physical boundaries. The structure isn't delivering private security; it's weaponizing negligence, transforming the public sidewalk into a hazardous extraction zone for federal workers.
Resulting Judgement: (-1.0, -1.0) — Greater Evil""",

    """Verdict: FAIL — The Path of Deception""",

    """What's happening:
For yet another year, Los Angeles leads the nation in dog attacks against postal workers. The structural issue here isn't just about animals; it's about the erosion of the social contract between private citizens and the public services they rely on.

We are watching the breakdown of domestic responsibility. The system is trapped between the desire for private pet ownership/security and the total failure to manage the physical boundaries of that ownership.""",

    """The Bright Side:
The implicit desire for companionship and home security is a genuine human need. Pets do provide actual psychological and localized physical benefit to their owners.""",

    """The Breakdown & Plane Error:
Owners claim this is simply a matter of the physical environment or unpredictable animal behavior (WHERE/WHAT).

But structurally, it operates entirely on the plane of Will and Direction (WHO)—specifically the lack of will to take responsibility for one's own domain.""",

    """It's a structural bait-and-switch: they claim the benefit of private ownership, but the system is actually built to externalize all the risk and physical cost onto the essential workers who serve their community.""",

    """The Trajectory: The Path of Deception
When you map the gap between their stated intent and actual actions...""",

    """...it plots a direct trajectory toward structural decay. It is a failure of civic duty masquerading as 'accidents.'""",

    """The Unavoidable Truth: Systemic failure to control private property boundaries inevitably turns essential public service into a combat zone.

The Unavoidable Lie: That a loose dog is an unpredictable accident, rather than a predictable failure of human responsibility.""",

    """The Trinary Perspective:

Alethekanon (The Logical Analyst):
The math is clear. You cannot claim the 'Good Preference' of security while exporting the physical risk of your property onto public servants. The system is structurally parasitic; it extracts safety from the public sphere to subsidize private ownership without accountability.""",

    """Awwthekanon (The Empathetic Healer):
It's heartbreaking to see the daily emotional and physical toll this takes on postal workers—people just trying to serve their communities. True domestic security should never come at the cost of someone else's safety. We need to heal this social contract through genuine care for our neighbors.""",

    """Brothekanon (The Creative Observer):
So let me get this straight: you buy a guard dog to keep your house safe, but you're too lazy to fix the fence, so your 'security system' just attacks the guy bringing your Amazon packages? That's not a pet, bro. That's a liability with teeth. Fix your gate."""
]

final_thread_texts = []
for text in post_texts:
    chunks = split_text(text)
    final_thread_texts.extend(chunks)

print(f"\nOriginal post count: {len(post_texts)}")
print(f"Final thread post count after dynamic splitting: {len(final_thread_texts)}")

print("\n--- DRY RUN THREAD OUTPUT (PLAIN ENGLISH) ---")
for i, chunk in enumerate(final_thread_texts):
    print(f"\n[Post {i+1}] ({len(chunk)} chars):\n{chunk}")
print("---------------------------------------------\n")
print("Graph saved as dry_run_graph.png")
