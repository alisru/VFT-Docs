import sys
from atproto import Client, client_utils, models

handle = '@judgement-bot.bsky.social'
handle = handle.lstrip('@')
password = 'e6qy-uioe-efrl-hhis'

client = Client()

try:
    print(f"Logging in as {handle}...")
    client.login(handle, password)
except Exception as e:
    print(f"Login failed: {e}")
    sys.exit(1)

post_text = """[Convergence Test]
Subject: US/Iran strikes
Verdict: Cycle of destruction driven by state self-interest over peace. Fails to converge toward Flow.
Coords: (υ: -1.2, ψ: -1.5)"""

image_path = 'dry_run.png'

print(f"Uploading image {image_path}...")
try:
    with open(image_path, 'rb') as f:
        img_data = f.read()

    # Using client.send_image since newer versions of atproto have a helper,
    # but let's try the models import correctly for manual embed
    upload = client.com.atproto.repo.upload_blob(img_data)
    images = [
        models.AppBskyEmbedImages.Image(
            alt='Psochic Hegemony Graph showing judgment coordinates',
            image=upload.blob
        )
    ]
    embed = models.AppBskyEmbedImages.Main(images=images)

    print("Posting to Bluesky...")
    client.com.atproto.repo.create_record(
        models.ComAtprotoRepoCreateRecord.Data(
            repo=client.me.did,
            collection='app.bsky.feed.post',
            record=models.AppBskyFeedPost.Record(
                created_at=client_utils.get_current_time(),
                text=post_text,
                embed=embed
            )
        )
    )
    print("Successfully posted to Bluesky!")
except Exception as e:
    print(f"Failed to post via manual embed: {e}")
    print("Falling back to client.send_image...")
    try:
        client.send_image(
            text=post_text,
            image=img_data,
            image_alt='Psochic Hegemony Graph showing judgment coordinates'
        )
        print("Successfully posted to Bluesky via send_image!")
    except Exception as inner_e:
        print(f"Failed to post via send_image: {inner_e}")
