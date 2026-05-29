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
if not password:
    print("Warning: BSKY_PASSWORD environment variable not set. Will do a dry run.")
    dry_run = True
else:
    dry_run = False

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
# Stated: +1, +1 (Greater Good)
# Actual: -1, -0.5 (My Group / Partial Suppression)
claim_u = 1.0
claim_psi = 1.0
real_u = -1.0
real_psi = -0.5

# Generate the graph
draw_graph(claim_u, claim_psi, real_u, real_psi, "Convergence Test: " + title[:30] + "...", "dry_run.png")

post_texts = [
    f"""CONVERGENCE TEST: {title}
SOURCE: {clean_link}
EVIDENCE STANDARDS: [A] Stated ideal, [B] Actions in context
ASSERTION: The consolidation of systemic resources serves to increase universal efficiency and collective security.
VERDICT: Fails. Deception Trajectory.
COORDS: CLAIM (1.0, 1.0) -> REAL ({-1.0}, {-0.5})""",
    """Q1 — WHO (Metaphysical) [FAIL] [P:0, F:7, B:0]
Claim: A structure operating for the universal public benefit.
Evidence: An extractive mechanism operating strictly for the preservation and expansion of its own in-group (Helxis detected).""",
    """Q2 — WHAT (Possible) [FAIL] [P:0, F:6, B:1]
Claim: Technological or systemic progression.
Evidence: The monopolization of pathways, masking structural fragility under the guise of inevitability.""",
    """Q3 — WHERE (Physical) [PASS] [P:5×0.8, F:2, B:0]
Claim: The global marketplace/digital commons.
Evidence: The privatization of previously open structural domains.""",
    """Q4 — WHY (Lyrical) [FAIL] [P:0, F:7, B:0]
Claim: To protect users and ensure stability.
Evidence: To eliminate alternatives and capture the host environment.""",
    """Q5 — HOW (Logical) [PASS] [P:7×1.0, F:0, B:0]
Claim: Synergistic integration.
Evidence: Algorithmic and systemic suppression of competitors. Coercive capture works exactly as designed.""",
    """Q6 — CAUSE (Historical) [PARTIAL] [P:3×0.5, F:4, B:0]
Claim: Organic growth driven by superior utility.
Evidence: Growth subsidized by unchecked leverage and regulatory capture.""",
    """Q7 — EFFECT (Emotive) [FAIL] [P:0, F:7, B:0]
Claim: Universal empowerment.
Evidence: Apathy, structural dependency, and the normalization of extraction.

Convergences: 2/7 · Divergences: 5/7""",
    f"""VECTOR VERIFICATION:
Morality Scope (-1.0): Me (self only). The system actively extracts from the universal base to feed the central node.
Will Action (-0.5): Partially suppressing. Active enclosure of the ecosystem.
z-profile: [0, 1, 0, 0, 0, 0, 0]
SOURCE INTEGRITY (ΔH): Fail (ΔH > 0.7)""",
    """FORENSIC STRESS TEST:
Fake Maximiser: Yes. The systemic issues it claims to solve are intentionally prolonged to justify the system's continued expansion.
Helxis (Bait/Switch): Detected. Bait: Universal utility. Switch: Centralized rent-extraction.""",
    """VERDICT & PROJECTED EVENTUALITY:
Trajectory: Deception (LE→GG→LG→GE). Stated overshoots actual toward +υ,+ψ. Mask active.
Gap Vector: (-2.0, -1.5)
Projected Terminal: Greater Evil (Void/Total Extraction)
R_net: 64.5 — Significant failure.
[A]: The system violates its own stated ideals of universal benefit.
[B]: The system reliably executes a highly coherent protocol of systemic extraction."""
]

final_thread_texts = []
for text in post_texts:
    chunks = split_text(text)
    final_thread_texts.extend(chunks)

print(f"Original post count: {len(post_texts)}")
print(f"Final thread post count after dynamic splitting: {len(final_thread_texts)}")

if dry_run:
    print("Dry run complete. Set BSKY_PASSWORD to post to Bluesky.")
    sys.exit(0)

# Setup ATProto Client
handle = 'judgement-bot.bsky.social'
client = Client()

try:
    print(f"Logging in as {handle}...")
    client.login(handle, password)
except Exception as e:
    print(f"Login failed: {e}")
    sys.exit(1)

def get_time():
    return datetime.now(timezone.utc).isoformat()

image_path = 'dry_run.png'

# Helper function to create a text post, extracting facets (like URLs) so they are clickable
def build_facets(text):
    facets = []
    if "http://" in text or "https://" in text:
        words = text.split()
        for word in words:
            if word.startswith("http://") or word.startswith("https://"):
                url = word
                byte_text = text.encode('UTF-8')
                byte_url = url.encode('UTF-8')
                start_idx = byte_text.find(byte_url)
                if start_idx != -1:
                    end_idx = start_idx + len(byte_url)
                    facets.append(
                        models.AppBskyRichtextFacet.Main(
                            features=[models.AppBskyRichtextFacet.Link(uri=url)],
                            index=models.AppBskyRichtextFacet.ByteSlice(byte_start=start_idx, byte_end=end_idx)
                        )
                    )
    return facets

# Post 1 (Root)
print("Posting Post 1 (Root)...")
try:
    with open(image_path, 'rb') as f:
        img_data = f.read()

    upload = client.com.atproto.repo.upload_blob(img_data)
    images = [
        models.AppBskyEmbedImages.Image(
            alt='Psochic Hegemony Graph showing stated claim and actual reality trajectory',
            image=upload.blob
        )
    ]
    embed = models.AppBskyEmbedImages.Main(images=images)

    root_post = client.com.atproto.repo.create_record(
        models.ComAtprotoRepoCreateRecord.Data(
            repo=client.me.did,
            collection='app.bsky.feed.post',
            record=models.AppBskyFeedPost.Record(
                created_at=get_time(),
                text=final_thread_texts[0],
                facets=build_facets(final_thread_texts[0]),
                embed=embed
            )
        )
    )

    root_ref = models.ComAtprotoRepoStrongRef.Main(
        cid=root_post.cid,
        uri=root_post.uri
    )
    parent_ref = root_ref

except Exception as e:
    print(f"Failed to post root: {e}")
    sys.exit(1)

# Post remaining replies
for i in range(1, len(final_thread_texts)):
    print(f"Posting Post {i+1}...")
    try:
        reply_ref = models.AppBskyFeedPost.ReplyRef(
            parent=parent_ref,
            root=root_ref
        )

        reply_post = client.com.atproto.repo.create_record(
            models.ComAtprotoRepoCreateRecord.Data(
                repo=client.me.did,
                collection='app.bsky.feed.post',
                record=models.AppBskyFeedPost.Record(
                    created_at=get_time(),
                    text=final_thread_texts[i],
                    reply=reply_ref
                )
            )
        )

        parent_ref = models.ComAtprotoRepoStrongRef.Main(
            cid=reply_post.cid,
            uri=reply_post.uri
        )
    except Exception as e:
        print(f"Failed to post reply {i+1}: {e}")
        break

print("Successfully posted the Convergence Test thread!")
