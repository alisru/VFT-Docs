import os
import sys
import argparse
from dotenv import load_dotenv
from atproto import Client, IdResolver

# Load environment variables
load_dotenv()

# Pre-compiled list of verified news domains/handles to filter results
VERIFIED_NEWS_DOMAINS = {
    'reuters.com', 'apnews.com', 'nytimes.com', 'washingtonpost.com',
    'bbcnews.com', 'motherjones.com', 'goodnewsnetwork.org', 'theguardian.com',
    'bloomberg.com', 'npr.org', 'cnn.com', 'foxnews.com', 'wsj.com',
    'latimes.com', 'abcnews.go.com', 'nbcnews.com', 'cbsnews.com',
    'alisru.bsky.social', 'alethekanon.bsky.social', 'judgement-bot.bsky.social',
    'theintercept.com', 'propublica.org', 'politico.com', 'axios.com'
}

def is_verified_news(handle):
    """Checks if a Bluesky handle matches or contains our verified news domains."""
    handle_lower = handle.lower()
    for domain in VERIFIED_NEWS_DOMAINS:
        if domain in handle_lower:
            return True
    return False

def make_bsky_url(handle, uri):
    """Converts an at-uri and a handle into a standard bsky.app web URL."""
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    try:
        rkey = uri.split('/')[-1]
        return f"https://bsky.app/profile/{handle}/post/{rkey}"
    except Exception:
        return uri

def parse_feed_url(url):
    """Parses a custom feed URL to extract the handle and feed key."""
    parts = url.strip("/").split("/")
    if "profile" not in parts or "feed" not in parts:
        raise ValueError("Invalid custom feed URL format. Must contain '/profile/<handle>/feed/<feed_name>'")
    handle_idx = parts.index("profile") + 1
    feed_idx = parts.index("feed") + 1
    return parts[handle_idx], parts[feed_idx]

def main():
    parser = argparse.ArgumentParser(description="Search Bluesky Posts and Feeds")
    parser.add_argument("query", help="The keyword or search query to filter posts by.")
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--news-only", "-n", action="store_true", help="Filter standard search results to only recognized news handles.")
    group.add_argument("--feed", "-f", nargs="?", const="https://bsky.app/profile/aendra.com/feed/verified-news", 
                       help="Fetch and search inside a custom feed URL (defaults to Aendra's 'verified-news' if no URL given).")
    
    parser.add_argument("--limit", type=int, default=25, help="Maximum number of raw posts to fetch (default: 25, max: 100).")
    args = parser.parse_args()

    # Verify credentials
    handle = os.environ.get('BSKY_HANDLE', 'judgement-bot.bsky.social')
    password = os.environ.get('BSKY_PASSWORD')
    if not password:
        print("ERROR: BSKY_PASSWORD environment variable not found in .env.")
        sys.exit(1)

    print(f"Connecting to Bluesky as {handle}...")
    client = Client()
    try:
        client.login(handle, password)
        print("Connected!")
    except Exception as e:
        print(f"Authentication failed: {e}")
        sys.exit(1)

    # Force standard stdout to use utf-8 encoding on Windows to prevent emoji print crashes
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    if args.feed:
        # Custom Feed Search Mode
        feed_url = args.feed
        print(f"\nResolving custom feed generator URL: {feed_url}...")
        try:
            feed_handle, feed_rkey = parse_feed_url(feed_url)
            resolver = IdResolver()
            feed_did = resolver.handle.resolve(feed_handle)
            feed_uri = f"at://{feed_did}/app.bsky.feed.generator/{feed_rkey}"
            
            print(f"Fetching posts from custom feed: {feed_uri} (limit: {args.limit})...")
            feed_data = client.app.bsky.feed.get_feed(params={'feed': feed_uri, 'limit': args.limit})
            
            if not feed_data.feed:
                print("No posts found in the custom feed.")
                return

            print(f"Filtering feed posts locally for keyword: '{args.query}'...\n")
            matching_posts = []
            query_lower = args.query.lower()
            
            for item in feed_data.feed:
                post = item.post
                post_text = getattr(post.record, 'text', '')
                if query_lower in post_text.lower():
                    matching_posts.append(post)
            
            if not matching_posts:
                print(f"No posts in the custom feed matched the keyword '{args.query}'.")
                return

            print(f"Found {len(matching_posts)} matching posts from the custom feed:\n")
            print("=" * 80)
            
            for idx, post in enumerate(matching_posts, 1):
                author_handle = post.author.handle
                post_text = post.record.text
                web_url = make_bsky_url(author_handle, post.uri)
                
                print(f"[{idx}] FROM: @{author_handle} (Verified News Feed)")
                print(f"    URL:  {web_url}")
                print(f"\n    TEXT:\n    {post_text.replace(chr(10), chr(10) + '    ')}")
                print("-" * 80)

        except Exception as e:
            print(f"Failed to fetch and search custom feed: {e}")
            sys.exit(1)

    else:
        # Standard Search Mode (with optional news filter)
        print(f"\nSearching standard timeline posts matching: '{args.query}' (limit: {args.limit})...")
        if args.news_only:
            print("Filtering results to recognized journalism and news handles only.\n")
        else:
            print("")

        try:
            results = client.app.bsky.feed.search_posts({'q': args.query, 'limit': args.limit})
            
            if not results.posts:
                print("No posts found matching that query.")
                return

            # Apply news only handle filter if requested
            filtered_posts = []
            for post in results.posts:
                if args.news_only:
                    if is_verified_news(post.author.handle):
                        filtered_posts.append(post)
                else:
                    filtered_posts.append(post)

            if not filtered_posts:
                print("No posts found matching that query from recognized news handles.")
                return

            print(f"Found {len(filtered_posts)} matching posts:\n")
            print("=" * 80)
            
            for idx, post in enumerate(filtered_posts, 1):
                author_handle = post.author.handle
                post_text = post.record.text
                web_url = make_bsky_url(author_handle, post.uri)
                likes = getattr(post, 'like_count', 0)
                reposts = getattr(post, 'repost_count', 0)
                
                print(f"[{idx}] FROM: @{author_handle}")
                print(f"    URL:  {web_url}")
                if likes or reposts:
                    print(f"    Stats: {likes} likes, {reposts} reposts")
                print(f"\n    TEXT:\n    {post_text.replace(chr(10), chr(10) + '    ')}")
                print("-" * 80)
                
        except Exception as e:
            print(f"Search failed: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
