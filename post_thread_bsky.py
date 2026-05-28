import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from atproto import Client, models

print("Fetching RSS feed...")
url = 'http://feeds.bbci.co.uk/news/world/rss.xml'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        content = response.read()
    root = ET.fromstring(content)
    item = root.find('.//item')
    title = item.find('title').text
    raw_link = item.find('link').text

    # Clean the URL
    if '?' in raw_link:
        clean_link = raw_link.split('?')[0]
    else:
        clean_link = raw_link

    print(f"Title: {title}")
    print(f"Link: {clean_link}")
except Exception as e:
    print(f"Error fetching RSS: {e}")
    sys.exit(1)

# Ensure the root post is < 300 chars even with the actual link
root_text = f"""CONVERGENCE TEST: Gaza Leadership Strikes
SOURCE: {clean_link}
ASSERTION: Targeted strikes against Hamas leadership dismantle the organization and produce security.
VERDICT: Fails n1 — Plane Error.
COORDS: (υ: -1.5, ψ: -1.5)"""

print(f"Root Post Length: {len(root_text)}")

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

post_texts = [
    root_text,
    """WHO
Claim: The state protecting its citizens.
Evidence: The state attempting to physically eliminate an ideology via military force.

WHERE
Claim: Targeted leadership compounds.
Evidence: Civilian hospitals, displacing the population.""",
    """WHAT
Claim: Elimination of leadership = Destruction of Hamas.
Evidence: The substance delivered is trauma. It guarantees the next generation of recruitment.

WHY
Claim: To end the war.
Evidence: To demonstrate political resolve and satisfy domestic demands.""",
    """HOW
Claim: Precision military targeting.
Evidence: The mechanism relies on overwhelming force in dense urban environments, maximizing collateral damage.

CAUSE
Claim: Retaliation for October 7th.
Evidence: Cyclical refusal to address root geopolitical conditions.""",
    """EFFECT
Claim: A dismantled enemy and a secure border.
Evidence: Decades of identical strikes consistently fail to produce security. The actual effect is perpetual radicalization.

CONVERGENCE: 0/7
DIVERGENCE: 7/7""",
    """THE UNAVOIDABLE TRUTH: Striking leadership successfully projects power and kills specific individuals. This is the only output that matches its intent.

THE UNAVOIDABLE LIE: That this mechanism can solve an ideological and territorial conflict.""",
    """PLANE ERROR: The state claims to operate on the Logical plane (Q5—mechanism for security). It actually operates on the Meta-Physical plane (Q1—Will/Direction)—specifically the will to assert total dominance and retribution, disguising it as a security solution."""
]

image_path = 'dry_run.png'

# Post 1 (Root)
print("Posting Post 1 (Root)...")
try:
    with open(image_path, 'rb') as f:
        img_data = f.read()

    # We will build the embed manually to properly handle facets
    upload = client.com.atproto.repo.upload_blob(img_data)
    images = [
        models.AppBskyEmbedImages.Image(
            alt='Psochic Hegemony Graph showing judgment coordinates',
            image=upload.blob
        )
    ]
    embed = models.AppBskyEmbedImages.Main(images=images)

    # Extract Facet for the clean_link
    facets = []
    byte_text = root_text.encode('UTF-8')
    byte_url = clean_link.encode('UTF-8')
    start_idx = byte_text.find(byte_url)
    if start_idx != -1:
        end_idx = start_idx + len(byte_url)
        facets.append(
            models.AppBskyRichtextFacet.Main(
                features=[models.AppBskyRichtextFacet.Link(uri=clean_link)],
                index=models.AppBskyRichtextFacet.ByteSlice(byte_start=start_idx, byte_end=end_idx)
            )
        )

    root_post = client.com.atproto.repo.create_record(
        models.ComAtprotoRepoCreateRecord.Data(
            repo=client.me.did,
            collection='app.bsky.feed.post',
            record=models.AppBskyFeedPost.Record(
                created_at=get_time(),
                text=root_text,
                facets=facets,
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
for i in range(1, len(post_texts)):
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
                    text=post_texts[i],
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

print("Successfully posted threaded Convergence Test!")
