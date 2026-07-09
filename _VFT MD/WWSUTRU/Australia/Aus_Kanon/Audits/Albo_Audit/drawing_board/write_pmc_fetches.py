import os
from datetime import date

# Extracted content from Parallel-Search-MCP web_fetch for robodebtgov26
robodebt_text = """1. Home
2. Resources
3. Government response to the Royal Commission into the Robodebt Scheme

# Government response to the Royal Commission into the Robodebt Scheme

The Australian Government released its response to the report of the Royal Commission into the Robodebt Scheme.
The Australian Government has carefully considered the Royal Commission’s report and recommendations.
The Government has accepted or accepted in principle all 56 recommendations made by the Royal Commission.
The Government Response commits to action to implement the recommendations, and reinforces the Government’s commitments to improve trust in government, deliver strong institutions, invest in a capable public sector and ensure people are at the centre of policy development and government service delivery."""

# Extracted content from Parallel-Search-MCP web_fetch for ministerialcode22
code_text = """1. Home
2. Resources
3. Code of Conduct for Ministers

# Code of Conduct for Ministers

The Albanese Government is committed to integrity, fairness, honesty and accountability and Ministers in my Government (including Assistant Ministers) will observe standards of probity, governance and behaviour worthy of the Australian people.
Ministers hold high public office and are entrusted with considerable privilege and power. The people of Australia are entitled to expect that, in the discharge of our duties, we will act in a manner that is consistent with the highest ethical standards.
The convention collective responsibility which applies to the Federal Cabinet ensures that the Government is collectively accountable and responsible to the Parliament and to the people of Australia. This means that Ministers are responsible, both personally and as a group, for the way in which we carry out our official duties.
The Code of Conduct for Ministers sets out, in clear terms, the expectations the Albanese Government has of all its ministers. Ministers also have a special responsibility for ensuring their offices, and the Parliament as a whole, are safe and respectful workplaces."""

def write_cache(tag, url, citation, extracted_text):
    out_path = os.path.join("raw_fetches", f"{tag}.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"SOURCE: [^{tag}]\n")
        f.write(f"CITATION: {citation}\n")
        f.write(f"URL: {url}\n")
        f.write(f"FETCHED: {date.today().isoformat()} (auto, via Parallel-Search-MCP web_fetch)\n")
        f.write(f"STATUS: fetched, NOT yet independently read/verified against any node claim -- update Sources_Verification_Checklist.md after review\n")
        f.write("\n---EXTRACTED TEXT---\n\n")
        f.write(extracted_text)
    print(f"Wrote cached file to {out_path}")

write_cache(
    "robodebtgov26",
    "https://www.pmc.gov.au/resources/government-response-royal-commission-robodebt-scheme",
    "Government response to the Royal Commission into the Robodebt Scheme, Department of the Prime Minister and Cabinet, 10 March 2026: https://www.pmc.gov.au/resources/government-response-royal-commission-robodebt-scheme",
    robodebt_text
)

write_cache(
    "ministerialcode22",
    "https://www.pmc.gov.au/resources/code-conduct-ministers",
    "\"Code of Conduct for Ministers\", Department of the Prime Minister and Cabinet, June 2022: https://www.pmc.gov.au/resources/code-conduct-ministers",
    code_text
)
