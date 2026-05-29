import sys
from datetime import datetime, timezone
from atproto import Client, models

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

# The 13-post threaded draft provided in the previous turn
post_texts = [
    """CONVERGENCE TEST: US "Maximum Pressure" Oil Embargo (Iran)
SOURCE: https://www.bbc.com/news/world-middle-east-48028751
ASSERTION: Crushing Iran's oil exports will defund terror proxies, stop nuclear proliferation, and force diplomatic submission.
VERDICT: Fails n1 — Plane Error.
COORDS: (υ: -1.5, ψ: -1.2)""",
    """Q1 — WHO (Metaphysical)
Claim: The US acting to enforce international norms.
Evidence: An isolated executive acting unilaterally, withdrawing from a multilateral agreement against the explicit advice of European allies.""",
    """Q2 — WHAT (Possible)
Claim: Maximum economic pressure = Diplomatic submission.
Evidence: The substance delivered is systemic trauma, eliminating moderate political factions and consolidating hardliner control.""",
    """Q3 — WHERE (Physical)
Claim: Targeted Iranian military and nuclear infrastructure.
Evidence: The Iranian civilian economy. The locus of impact was domestic markets, triggering hyperinflation.""",
    """Q4 — WHY (Lyrical)
Claim: To secure a "better deal" and ensure regional safety.
Evidence: To unilaterally dismantle the previous administration's legacy. The motive is dominance, not diplomatic resolution.""",
    """Q5 — HOW (Logical)
Claim: Secondary sanctions on global oil buyers.
Evidence: Weaponizing the US dollar reserve status to act as a unilateral global financial hegemon.""",
    """Q6 — CAUSE (Historical)
Claim: The JCPOA was a "flawed deal" exploited by Iran.
Evidence: IAEA inspectors repeatedly confirmed Iranian compliance. The cause was the executive's political imperative.""",
    """Q7 — EFFECT (Emotive)
Claim: A defunded, compliant Iran returning to negotiations.
Evidence: Accelerated uranium enrichment and increased proxy attacks. The effect was the exact opposite of the stated intent.

CONVERGENCE: 0/7
DIVERGENCE: 7/7""",
    """THE UNAVOIDABLE TRUTH: Unilateral sanctions successfully weaponize the US dollar to collapse foreign civilian economies.

THE UNAVOIDABLE LIE: That maximum pressure produces diplomatic capitulation. It reliably produces accelerated escalation.""",
    """PLANE ERROR: The embargo claims to operate on the Logical plane (Q5—mechanism for forcing a new treaty). It actually operates on the Metaphysical plane (Q1)—specifically the will to inflict total economic punishment and assert dominance.""",
    """MP ASSESSMENT (ISOMORPHISM):
When subjected to a socioeconomic siege via energy starvation, states historically follow a mathematically inevitable path toward the "fight or die" threshold.""",
    """ISOMORPHIC REFERENCE: The US oil embargo on Imperial Japan (1941), which reliably produced kinetic military retaliation within 120 days. The Metaphysical structure of starving a state's thermodynamics guarantees kinetic escalation, not capitulation.""",
    """VECTOR JUSTIFICATION:
Morality (υ): -1.5. The executive prioritizes unilateral dominance (Self) over international civilian stability (Everyone).
Will (ψ): -1.2. The mechanism relies entirely on systemic thermodynamic destruction (Destroy)."""
]

# Apply dynamic splitting just in case any edits pushed it over 300
final_thread_texts = []
for text in post_texts:
    chunks = split_text(text)
    final_thread_texts.extend(chunks)

print(f"Original post count: {len(post_texts)}")
print(f"Final thread post count after dynamic splitting: {len(final_thread_texts)}")

# Setup ATProto Client
handle = 'judgement-bot.bsky.social'
password = 'e6qy-uioe-efrl-hhis'
client = Client()

try:
    print(f"Logging in as {handle}...")
    client.login(handle, password)
except Exception as e:
    print(f"Login failed: {e}")
    sys.exit(1)

def get_time():
    return datetime.now(timezone.utc).isoformat()

image_path = 'embargo_graph.png'

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
            alt='Psochic Hegemony Graph showing judgment coordinates',
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

print("Successfully posted the Oil Embargo Convergence Test thread!")
