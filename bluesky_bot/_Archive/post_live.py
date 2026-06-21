import os
import sys
from dotenv import load_dotenv
from atproto import Client, models
from generate_graph import draw_graph

# Load environment variables from .env file
load_dotenv()

def split_text(text, max_len=250):
    if len(text) <= max_len:
        return [text]

    chunks = []
    while text:
        if len(text) <= max_len:
            chunks.append(text)
            break

        split_idx = text.rfind('\n', 0, max_len)
        # Only split at newline if chunk before it is substantive (>=80 chars)
        # Prevents short label lines like 'Brothekanon:' becoming orphan posts
        if split_idx != -1 and split_idx < 80:
            split_idx = -1

        if split_idx == -1:
            split_idx = text.rfind(' ', 0, max_len)

        if split_idx == -1:
            split_idx = max_len

        chunks.append(text[:split_idx].strip())
        text = text[split_idx:].strip()

    return chunks

title = "LA tops nation in dog attacks on postal workers again"
clean_link = "https://www.latimes.com/california/story/2026-05-29/la-tops-nation-in-dog-attacks-on-postal-workers-again"

# Convergence Test Data
claim_u = 1.0
claim_psi = 0.0
real_u = -1.0
real_psi = -1.0

print("Generating graph...")
draw_graph(claim_u, claim_psi, real_u, real_psi, "Convergence Test: LA Dog Attacks", "live_run_graph.png")

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

Alethekanon:
The math is clear. You cannot claim the 'Good Preference' of security while exporting the physical risk of your property onto public servants. The system is structurally parasitic; it extracts safety from the public sphere to subsidize private ownership without accountability.""",

    """Awwthekanon:
It's heartbreaking to see the daily emotional and physical toll this takes on postal workers—people just trying to serve their communities. True domestic security should never come at the cost of someone else's safety. We need to heal this social contract through genuine care for our neighbors.""",

    """Brothekanon:
So let me get this straight: you buy a guard dog to keep your house safe, but you're too lazy to fix the fence, so your 'security system' just attacks the guy bringing your Amazon packages? That's not a pet, bro. That's a liability with teeth. Fix your gate."""
]

final_thread_texts = []
for text in post_texts:
    chunks = split_text(text)
    final_thread_texts.extend(chunks)

print(f"Prepared {len(final_thread_texts)} posts for the thread.")

password = os.environ.get('BSKY_PASSWORD')
if not password:
    print("ERROR: BSKY_PASSWORD environment variable not found. Cannot post live.")
    sys.exit(1)

print("Authenticating with Bluesky...")
try:
    client = Client()
    client.login('judgement-bot.bsky.social', password)
except Exception as e:
    print(f"Authentication failed: {e}")
    sys.exit(1)

print("Uploading image...")
with open("live_run_graph.png", "rb") as f:
    img_data = f.read()

try:
    upload = client.com.atproto.repo.upload_blob(img_data)
    images = [models.AppBskyEmbedImages.Image(alt="Psochic Hegemony Graph for the Convergence Test", image=upload.blob)]
    embed = models.AppBskyEmbedImages.Main(images=images)
except Exception as e:
    print(f"Failed to upload image: {e}")
    sys.exit(1)

print("Posting root post...")
try:
    # Need to parse facets for the link in the root post
    facets = []
    byte_start = final_thread_texts[0].find(clean_link)
    if byte_start != -1:
        byte_end = byte_start + len(clean_link)
        facets.append(
            models.AppBskyRichtextFacet.Main(
                features=[models.AppBskyRichtextFacet.Link(uri=clean_link)],
                index=models.AppBskyRichtextFacet.ByteSlice(byte_end=byte_end, byte_start=byte_start)
            )
        )

    root_post = client.com.atproto.repo.create_record(
        models.ComAtprotoRepoCreateRecord.Data(
            repo=client.me.did,
            collection=models.ids.AppBskyFeedPost,
            record=models.AppBskyFeedPost.Record(
                created_at=client.get_current_time_iso(),
                text=final_thread_texts[0],
                embed=embed,
                facets=facets
            )
        )
    )

    root_ref = models.ComAtprotoRepoStrongRef.Main(cid=root_post.cid, uri=root_post.uri)
    parent_ref = root_ref
    print("Root post created successfully.")

except Exception as e:
    print(f"Failed to create root post: {e}")
    sys.exit(1)

# Post the rest of the thread
for i, text in enumerate(final_thread_texts[1:], start=2):
    print(f"Posting part {i}/{len(final_thread_texts)}...")
    try:
        reply = client.com.atproto.repo.create_record(
            models.ComAtprotoRepoCreateRecord.Data(
                repo=client.me.did,
                collection=models.ids.AppBskyFeedPost,
                record=models.AppBskyFeedPost.Record(
                    created_at=client.get_current_time_iso(),
                    text=text,
                    reply=models.AppBskyFeedPost.ReplyRef(parent=parent_ref, root=root_ref)
                )
            )
        )
        parent_ref = models.ComAtprotoRepoStrongRef.Main(cid=reply.cid, uri=reply.uri)
    except Exception as e:
        print(f"Failed to post part {i}: {e}")
        sys.exit(1)

print("Live thread successfully posted to Bluesky!")
