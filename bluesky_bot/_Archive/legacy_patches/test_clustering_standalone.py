import sys, os, json

# Import functions cleanly
from harvest_candidates import cluster_candidate_stories

mock_raw_candidates = [
    {
        "title": "ICE Arrests 1,300 in Massive DC Suburb Operation",
        "subject": "ICE Arrests 1,300 in Massive DC Suburb Operation",
        "publisher": "Breitbart",
        "url": "https://www.breitbart.com/news/ice-dc-operation",
        "text": "ICE announced over 1,300 undocumented immigrants were apprehended across DC suburbs."
    },
    {
        "title": "ICE Operation Safe Community Detains 1,300 Across DC Region",
        "subject": "ICE Operation Safe Community Detains 1,300 Across DC Region",
        "publisher": "Washington Post",
        "url": "https://www.washingtonpost.com/local/ice-safe-community-dc",
        "text": "Advocacy groups raised concerns after ICE reported 1,300 arrests, noting only 32 had violent felony convictions."
    },
    {
        "title": "Texas Governor Abbott Calls for Review of Data Center Subsidies",
        "subject": "Texas Governor Abbott Calls for Review of Data Center Subsidies",
        "publisher": "Bloomberg",
        "url": "https://www.bloomberg.com/news/abbott-texas-grid",
        "text": "Greg Abbott questioned power grid reliability under rapid AI data center expansion."
    }
]

clustered = cluster_candidate_stories(mock_raw_candidates)

print(f"Total raw input: {len(mock_raw_candidates)} -> Total clustered: {len(clustered)}")
assert len(clustered) == 2, f"Expected 2 topics, got {len(clustered)}"

ice_cluster = [c for c in clustered if "ICE" in c.get("subject", "")][0]
print("\n--- ICE CLUSTER VERIFICATION ---")
print("is_multi_source:", ice_cluster.get("is_multi_source"))
print("Cluster sources count:", len(ice_cluster.get("cluster_sources", [])))
print("Publishers:", [s["publisher"] for s in ice_cluster.get("cluster_sources", [])])
assert ice_cluster.get("is_multi_source") is True
assert len(ice_cluster.get("cluster_sources", [])) == 2

abbott_story = [c for c in clustered if "Abbott" in c.get("subject", "")][0]
print("\n--- ABBOTT STORY VERIFICATION ---")
print("is_multi_source:", abbott_story.get("is_multi_source"))
assert abbott_story.get("is_multi_source") is False

print("\nALL CLUSTERING TESTS PASSED SUCCESSFULLY!")
