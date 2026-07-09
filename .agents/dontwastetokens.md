# Token Conservation and Search Cessation Rule

* **Immediate Stop on Success**: If you are searching for a quote, fact, or source to validate a statement or node, and a search result excerpt contains a valid, direct, and verifiable quote or the necessary info, you MUST STOP searching immediately.
* **No Redundant Fetches**: Do not run additional web searches or `web_fetch`/browser visits to retrieve the full page just to verify the quote if the excerpt already contains a verbatim, attributed block of text that satisfies the criteria.
* **Execute Immediately**: Proceed directly to editing the files or completing the task with the data already in your context. Do not write multiple search queries in series if the first ones have already yielded candidate matches.
