import os
import sys
from datetime import datetime, timezone
import urllib.request
import xml.etree.ElementTree as ET
from atproto import Client, models
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

# Grab password from environment variable for security
password = os.environ.get('BSKY_PASSWORD')
# For this script, we ALWAYS do a dry run unless explicitly overridden in code.
dry_run = True

print("Fetching RSS feed...")
url = 'http://feeds.bbci.co.uk/news/world/rss.xml'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        content = response.read()
    root = ET.fromstring(content)

    # We'll take the second item to get a new story
    items = root.findall('.//item')
    item = items[1] if len(items) > 1 else items[0]
    title = item.find('title').text
    raw_link = item.find('link').text

    if '?' in raw_link:
        clean_link = raw_link.split('?')[0]
    else:
        clean_link = raw_link

    print(f"Title: {title}")
    print(f"Link: {clean_link}")
except Exception as e:
    print(f"Error fetching RSS: {e}")
    sys.exit(1)

# Let's perform a live Convergence Test on a generic new tech/corporate consolidation story format
# Using mock coordinates for a typical Deception trajectory:
# Stated: +1.0, +1.0 (Greater Good)
# Actual: -1.0, -0.5 (My Group / Partial Suppression)
claim_u = 1.0
claim_psi = 1.0
real_u = -1.0
real_psi = -0.5

# Generate the graph
draw_graph(claim_u, claim_psi, real_u, real_psi, "Convergence Test", "dry_run.png")

# Using the new Plain English template with Plane Error
post_texts = [
    f"""A classic case of an organization saying one thing, while their structural mechanics build the exact opposite.

Subject: {title}
Source: {clean_link}
Verdict: FAIL — The Path of Deception""",

    """What's happening:
NASA is facing severe delays and budget overruns with their Artemis Moon program, largely due to explosive test failures and systemic unreliability from their contracted private launch providers.""",

    """We are watching the privatization of space exploration hit a structural reality check. The system is currently trapped between the need for reliable public infrastructure and the mechanics of private, profit-driven corporate consolidation.""",

    """The Claim:
The actors involved state that privatizing these launch vehicles increases efficiency, reduces costs for the taxpayer, and accelerates humanity's return to the Moon for the benefit of everyone.""",

    """The Reality:
The evidence shows that turning over core public infrastructure to private monopolies has actually created massive bottlenecks. The structure isn't delivering efficiency; it's delivering delays while extracting public funding to subsidize private risk.""",

    """The Breakdown & Plane Error:
The actors claim their actions are simply about finding the most logical engineering method (HOW) to get to space.

But their actual structural effect operates on entirely different plane: establishing dominance over the marketplace (WHO).""",

    """It's a classic bait-and-switch: they hook the public with the promise of universal progress, but the system is actually built to extract capital strictly for the benefit of an exclusive in-group. It's a closed loop of self-interest.""",

    """The Trajectory: The Path of Deception
They claim to operate for the Greater Good (+1.0, +1.0), but their actual mechanics operate purely for Self-Interest and Suppression (-1.0, -0.5).

When you map the gap between their stated intent and actual actions...""",

    """...it plots a direct trajectory toward total structural extraction (The Greater Evil). They are wearing the mask of universal progress to disguise a mechanism of pure corporate consolidation.""",

    """The Unavoidable Truth: Turning over vital public exploration infrastructure to profit-driven monopolies reliably produces extortion and delay, not innovation.

The Unavoidable Lie: That billionaire consolidation is the same thing as human progress."""
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

if dry_run:
    print("Dry run complete. Exiting without posting to Bluesky.")
    sys.exit(0)
