---
description: Verify every quote in a Kanon audit plane file against the local Hansard corpus
---

Run the verification gate over the audit files given in $ARGUMENTS (default: every
`Plane_*.md` in the current audit directory).

```bash
python "E:/Vector Field Theory/VFT Docs/_VFT MD/WWSUTRU/Australia/Aus_Kanon/hansard/verify_quotes.py" $ARGUMENTS --speaker "<actor surname>" --quiet
```

Report the summary table and every item needing attention. Do not edit anything
yet: present the findings and let the user choose what to fix.

Verdict meanings:
- **VERIFIED** / **VERIFIED (punctuation differs)** — real, cite as-is
- **NEAR MISS** — real quote, drifted wording. The gate prints the true text
- **NOT FOUND** — not in Hansard. Do not repair; find a different quote, or
  check the non-chamber sources (`sources.py`) if it was never a chamber quote
- **DATE MISMATCH** — right quote, wrong sitting day. Fix header, footnote AND
  the URL, which usually embeds the date
- **ORPHAN MARKER** / **NO CITATION** / **NOT A QUOTE** — citation integrity

Never invent a citation to clear a finding. If a quote cannot be sourced, say so.
