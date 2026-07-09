"""
Test: get Albanese's person_id, then search for a known quote via OpenAustralia API.
"""
import json, urllib.request, urllib.parse, time

API_KEY = "F9TbUzGNMr3rDTBxkvG47QHG"
BASE = "https://www.openaustralia.org.au/api"

def api_get(fn, **params):
    params["key"] = API_KEY
    params["output"] = "js"
    url = f"{BASE}/{fn}?{urllib.parse.urlencode(params)}"
    print(f"  Calling: {url}")
    with urllib.request.urlopen(url, timeout=15) as r:
        return json.loads(r.read().decode())

# Step 1: get person_id
reps = api_get("getRepresentatives", search="Albanese")
print("Representatives found:")
for r in reps:
    print(f"  {r.get('full_name')} | person_id={r.get('person_id')} | party={r.get('party')}")

person_id = reps[0]["person_id"]
print(f"\nUsing person_id={person_id}")

# Step 2: get first page of their debates (newest first)
debates = api_get("getDebates", type="representatives", person=person_id, page=1)
rows = debates.get("rows", [])
print(f"\nFirst debate result:")
row = rows[0]
print(json.dumps({k: v for k, v in row.items() if k != "body"}, indent=2))

# Build URL from listurl
listurl = row.get("listurl", "")
clean = "https://www.openaustralia.org.au" + listurl.split("&amp;")[0].split("&")[0]
print(f"\nDirect URL: {clean}")
print(f"GID: {row.get('gid')}")
