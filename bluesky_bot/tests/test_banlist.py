import os
import sys
import re

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from harvest_candidates import is_banned, load_banned_topics

def run_tests():
    # 1. Load banned topics and assert it's a dict
    banned_map = load_banned_topics()
    print(f"Loaded banned topics map with keys: {list(banned_map.keys())}")
    assert isinstance(banned_map, dict), "Banned topics should be a dictionary!"
    assert "sport" in banned_map, "sport category missing!"
    assert "tour de france" in banned_map["sport"], "tour de france keyword missing from sport category!"

    # 2. Test keyword resolver logic manually
    # Case A: CLI passes "sport, travel"
    cli_input = "sport, travel, mycustomkeyword"
    user_banned = [k.strip().lower() for k in cli_input.split(",") if k.strip()]
    resolved_keywords = []
    for item in user_banned:
        if item in banned_map:
            resolved_keywords.extend(banned_map[item])
        else:
            resolved_keywords.append(item)
    resolved_keywords = list(dict.fromkeys(resolved_keywords))

    print(f"Resolved keywords from '{cli_input}': {len(resolved_keywords)} keywords.")
    assert "tour de france" in resolved_keywords, "tour de france keyword should be resolved from sport category!"
    assert "mycustomkeyword" in resolved_keywords, "custom keyword mycustomkeyword should be resolved!"
    assert "obituary" not in resolved_keywords, "obituary should NOT be resolved since it wasn't requested!"

    # Case B: CLI is empty (defaults to all categories)
    all_resolved = []
    for cat, kws in banned_map.items():
        all_resolved.extend(kws)
    all_resolved = list(dict.fromkeys(all_resolved))
    print(f"Resolved all keywords: {len(all_resolved)} keywords.")
    assert "obituary" in all_resolved, "obituary should be resolved when loading all categories!"
    assert "tour de france" in all_resolved, "tour de france should be resolved when loading all categories!"

    # 3. Test false-positive word matching
    # 'transportation' contains 'sport' as a substring, but it shouldn't match with \b
    text_trans = "The city is investing in public transportation."
    banned_trans = is_banned(text_trans, "", all_resolved)
    print(f"Text: '{text_trans}' -> Banned? {banned_trans}")
    assert not banned_trans, "FAIL: 'transportation' was incorrectly blocked by 'sport'!"

    # 4. Test true-positive word matching for categories
    text_sports = "New sports center opens downtown."
    banned_sports = is_banned(text_sports, "", all_resolved)
    print(f"Text: '{text_sports}' -> Banned? {banned_sports}")
    assert banned_sports, "FAIL: 'sports' was not blocked!"

    text_obituary = "Obituary of local hero."
    banned_obituary = is_banned(text_obituary, "", all_resolved)
    print(f"Text: '{text_obituary}' -> Banned? {banned_obituary}")
    assert banned_obituary, "FAIL: 'Obituary' was not blocked!"

    # 5. Test Tour de France matching
    text_tdf = "Tadej Pogacar wins the Tour de France stage."
    banned_tdf = is_banned(text_tdf, "", resolved_keywords)
    print(f"Text: '{text_tdf}' with 'sport' enabled -> Banned? {banned_tdf}")
    assert banned_tdf, "FAIL: 'Tour de France' should be blocked when sport is enabled!"

    # Test Tour de France NOT matched when sport category is omitted
    cli_no_sport = "travel, obituaries"
    user_no_sport = [k.strip().lower() for k in cli_no_sport.split(",") if k.strip()]
    no_sport_resolved = []
    for item in user_no_sport:
        if item in banned_map:
            no_sport_resolved.extend(banned_map[item])
        else:
            no_sport_resolved.append(item)
    
    banned_tdf_no_sport = is_banned(text_tdf, "", no_sport_resolved)
    print(f"Text: '{text_tdf}' with 'sport' omitted -> Banned? {banned_tdf_no_sport}")
    assert not banned_tdf_no_sport, "FAIL: 'Tour de France' was incorrectly blocked when sport was disabled!"

    # 6. Test space-separated phrase variations
    text_dies_at = "Prominent director dies at 85."
    banned_dies = is_banned(text_dies_at, "", all_resolved)
    print(f"Text: '{text_dies_at}' -> Banned? {banned_dies}")
    assert banned_dies, "FAIL: 'dies at' phrase was not blocked!"

    # Test variant hyphenation
    text_tv_show = "A review of the latest tv-show."
    banned_tv = is_banned(text_tv_show, "", all_resolved)
    print(f"Text: '{text_tv_show}' -> Banned? {banned_tv}")
    assert banned_tv, "FAIL: 'tv-show' variant was not blocked!"

    print("ALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
