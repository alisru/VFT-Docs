import os
import sys
from dotenv import load_dotenv
from atproto import Client, models, IdResolver

load_dotenv()

TARGET_POST_URL = "https://bsky.app/profile/motherjones.com/post/3mn3fzc3oau2d"

def parse_bsky_url(url):
    parts = url.strip("/").split("/")
    handle_idx = parts.index("profile") + 1
    post_idx = parts.index("post") + 1
    return parts[handle_idx], parts[post_idx]

def main():
    handle = os.environ.get('BSKY_HANDLE', 'judgement-bot.bsky.social')
    password = os.environ.get('BSKY_PASSWORD')
    
    client = Client()
    client.login(handle, password)
    
    target_handle, rkey = parse_bsky_url(TARGET_POST_URL)
    resolver = IdResolver()
    target_did = resolver.handle.resolve(target_handle)
    
    response = client.com.atproto.repo.get_record(
        models.ComAtprotoRepoGetRecord.Params(
            repo=target_did,
            collection='app.bsky.feed.post',
            rkey=rkey
        )
    )
    
    record = response.value
    
    print(f"--- POST TEXT ---\n{record.text}\n-----------------\n")
    
    print("--- EMBED ---")
    if hasattr(record, 'embed') and record.embed:
        print(type(record.embed))
        if hasattr(record.embed, 'external'):
            print(f"External URI: {record.embed.external.uri}")
        else:
            print(record.embed)
    else:
        print("No embed")
        
    print("\n--- FACETS ---")
    if hasattr(record, 'facets') and record.facets:
        for f in record.facets:
            for feat in f.features:
                if hasattr(feat, 'uri'):
                    print(f"Facet URI: {feat.uri}")
    else:
        print("No facets")

if __name__ == "__main__":
    main()
