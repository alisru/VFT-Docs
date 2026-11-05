# Active Task List: Australian & International RSS Feeds Expansion and Latency Resolution

- [ ] Upgrade User-Agent header in `harvest_candidates.py` to modern Chrome browser string to resolve Google News connection delay.
- [ ] Upgrade User-Agent header in `google_ai_studio_one_shot.py` to modern Chrome browser string.
- [ ] Add the newly identified Australian and international RSS feeds from Feedspot to the `rss_feeds` list in `harvest_candidates.py`.
- [ ] Add the newly identified Australian and international RSS feeds to `_CATEGORY_FEEDS` in `google_ai_studio_one_shot.py`.
- [ ] Run verification tests of candidate harvesting using `python bluesky_bot/harvest_candidates.py --rss-target 5 --bsky-target 0` to check yield and latency.
- [ ] Verify category harvesting via `python bluesky_bot/google_ai_studio_one_shot.py --rss 5 --bsky 0 --dry-run` to make sure it loads category feeds correctly.
