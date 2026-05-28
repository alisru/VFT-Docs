import sys
import urllib.request
import xml.etree.ElementTree as ET
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

print("Fetching RSS feed...")
url = 'http://feeds.bbci.co.uk/news/world/rss.xml'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        content = response.read()
    root = ET.fromstring(content)

    # We'll take the first item
    item = root.find('.//item')
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

# Draft the post using the Minimisation Plan context
root_text = f"""CONVERGENCE TEST: The Minimisation Plan (Phase 1/2)
SOURCE: {clean_link}
ASSERTION: Coordinated amplification of US domestic chaos and scandal serves to restructure global power by destroying American moral authority.
VERDICT: Fails n1 — Plane Error.
COORDS: (υ: -1.8, ψ: -1.5)"""

print(f"Root Post Length: {len(root_text)}")

long_post = """WHAT
Claim: A search for truth and accountability.
Evidence: The weaponization of partial truths. The substance delivered is total institutional cynicism, not justice.

WHY
Claim: To drain the swamp / expose corruption.
Evidence: To execute a "reputation flip," transitioning the US from world leader to "objective evil," allowing authoritarianism to appear as the "subjective good" by comparison."""

post_texts = [
    root_text,
    """WHO
Claim: Domestic political actors fighting for national reform.
Evidence: Foreign state actors (Russia/China) amplifying internal divisions as a coordinated "political dirty bomb."

WHERE
Claim: The American domestic political arena.
Evidence: The global information space, restructuring international perception.""",
    long_post,
    """HOW
Claim: Organic populist movements and social media outrage.
Evidence: Algorithmic amplification of division, where the chaotic executive acts as a massive distraction for long-term strategic realignment.

CAUSE
Claim: Genuine systemic failure in democratic systems.
Evidence: A manufactured, atmospheric attack designed to erode reality itself.""",
    """EFFECT
Claim: Accountability and political renewal.
Evidence: The normalization of authoritarianism. A paralyzed public incapable of distinguishing reality from the absurd.

CONVERGENCE: 0/7
DIVERGENCE: 7/7""",
    """THE UNAVOIDABLE TRUTH: The chaotic executive and the amplification of scandals successfully consume all public attention and erode institutional trust.

THE UNAVOIDABLE LIE: That this chaos is an organic product of democracy, rather than a subsidized weapon against it.""",
    """PLANE ERROR: The actors claim to operate on the Ethical/Logical planes (Q5—exposing corruption to fix the system). They actually operate on the Meta-Physical plane (Q1—Will/Direction)—specifically the will to dismantle liberal democracy to justify totalitarian utopias.""",
    """VECTOR JUSTIFICATION:
Morality (υ): -1.8. The strategy actively weaponizes societal collapse for authoritarian Self-benefit over Universal stability.
Will (ψ): -1.5. The mechanism relies entirely on the destruction of trust and the suppression of democratic reality (Destroy)."""
]

# Apply the dynamic splitting
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

print("Successfully posted threaded Convergence Test using Minimisation Plan context!")
