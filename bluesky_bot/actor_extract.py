"""Deterministic (non-LLM) actor/entity extraction for Aletheia stories.

Pulls the names of people and organisations a story is *about* from its subject
line (and optionally body text) using capitalisation heuristics. Intentionally
simple and dependency-free so it can run in the harvest pipeline and as a
one-time backfill without any API calls.
"""
import re

# Honorifics / titles that precede a name — stripped so "Gov. Greg Abbott" -> "Greg Abbott".
TITLES = {
    'gov', 'sen', 'rep', 'pres', 'president', 'vp', 'mr', 'mrs', 'ms', 'dr',
    'prof', 'sir', 'lord', 'lady', 'gen', 'col', 'capt', 'lt', 'sgt', 'judge',
    'justice', 'mayor', 'governor', 'senator', 'congressman', 'congresswoman',
    'minister', 'chancellor', 'premier', 'pope', 'king', 'queen', 'prince',
    'princess', 'sheikh', 'ayatollah', 'rabbi', 'imam', 'secretary', 'attorney',
    'general', 'admiral', 'pm', 'ceo', 'cfo', 'chairman', 'director', 'officer',
}

# Common capitalised words that are NOT entities (sentence starters, connectives,
# months, generic nouns that often appear capitalised in headlines).
STOPWORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'for', 'nor', 'so', 'yet', 'as',
    'at', 'by', 'in', 'of', 'on', 'to', 'up', 'it', 'is', 'are', 'was', 'were',
    'be', 'been', 'this', 'that', 'these', 'those', 'his', 'her', 'their', 'its',
    'new', 'old', 'how', 'why', 'what', 'when', 'where', 'who', 'which',
    'after', 'before', 'during', 'over', 'under', 'into', 'onto', 'amid',
    'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
    'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
    'september', 'october', 'november', 'december',
    'us', 'usa', 'uk', 'eu', 'un',  # handled separately as known orgs if desired
}

# Generic nouns that frequently appear capitalised in headlines but are never actors.
# A captured phrase consisting mainly of these is dropped.
GENERIC_NOUNS = {
    'cost', 'costs', 'law', 'laws', 'victory', 'remarks', 'strikes', 'strike',
    'measures', 'standards', 'trial', 'center', 'centre', 'speech', 'book',
    'pillows', 'fight', 'war', 'wars', 'ceasefire', 'delegation', 'theme',
    'transit', 'report', 'study', 'plan', 'plans', 'deal', 'crisis', 'summit',
    'election', 'vote', 'bill', 'act', 'ban', 'rules', 'policy', 'tax', 'taxes',
    'cup', 'league', 'series', 'show', 'season', 'game', 'match', 'film', 'movie',
    'samaritan', 'good', 'new', 'day', 'immigration', 'democracy', 'emergency',
    'domestic', 'intelligence', 'staff', 'standards', 'certification', 'trust',
    'marketplaces', 'online', 'sleep', 'baby', 'dangerous', 'interfaith',
}

# Known single-token figures/orgs worth capturing even without a second name token.
KNOWN_SINGLE = {
    'trump', 'biden', 'obama', 'putin', 'zelensky', 'netanyahu', 'xi', 'modi',
    'macron', 'musk', 'bezos', 'zuckerberg', 'harris', 'pelosi', 'desantis',
    'erdogan', 'kim', 'maduro', 'orban', 'meloni', 'starmer', 'albanese',
    'google', 'apple', 'amazon', 'meta', 'microsoft', 'tesla', 'openai',
    'nato', 'opec', 'fbi', 'cia', 'irs', 'fda', 'epa', 'ice', 'doge',
}

# Title-cased multi-word proper-noun runs (allows internal lowercase particles
# like "of"/"the" in org names, e.g. "Bank of America", "University of Texas").
_NAME_RE = re.compile(
    r'\b([A-Z][a-zA-Z.\'\-]+(?:\s+(?:of|the|and|for|de|van|von|al)\s+)?'
    r'(?:\s*[A-Z][a-zA-Z.\'\-]+){1,3})\b'
)


def _clean_token(tok):
    return tok.strip().strip('.').lower()


def extract_actors(text, max_actors=6):
    """Return a de-duplicated list of probable actor/entity names from text."""
    if not text:
        return []

    found = []
    seen = set()

    for match in _NAME_RE.finditer(text):
        phrase = match.group(1).strip()
        phrase = phrase.strip('.,;:!?\'"-')

        # Cut at a possessive so "Musk's Tesla" -> "Musk" (the actor, not the asset).
        phrase = re.split(r"'s\b", phrase)[0].strip()

        words = phrase.split()
        # Remove title tokens anywhere ("Texas Gov. Greg Abbott" -> "Texas Greg Abbott"
        # is wrong, so titles also act as a split point): split into segments on titles.
        segment = []
        for w in words:
            if _clean_token(w) in TITLES:
                # Title encountered: keep only the part AFTER it (name follows title).
                segment = []
                continue
            segment.append(w)
        words = segment
        if not words:
            continue

        # Trim trailing generic nouns ("Hegseth Immigration Remarks" -> "Hegseth ...").
        while words and _clean_token(words[-1]) in GENERIC_NOUNS:
            words.pop()
        # Trim leading generic/stop nouns.
        while words and _clean_token(words[0]) in GENERIC_NOUNS:
            words.pop(0)
        if not words:
            continue

        # Drop phrases that are mostly generic nouns (headline fragments, not entities).
        generic_count = sum(1 for w in words if _clean_token(w) in GENERIC_NOUNS)
        has_known = any(_clean_token(w) in KNOWN_SINGLE for w in words)
        if not has_known and generic_count > len(words) / 2:
            continue

        # Require at least two name tokens, OR a single known figure/org.
        meaningful = [w for w in words if _clean_token(w) not in STOPWORDS and _clean_token(w) not in GENERIC_NOUNS]
        if len(meaningful) < 2:
            single = _clean_token(words[-1])
            if single not in KNOWN_SINGLE:
                continue

        name = ' '.join(words)
        key = name.lower()
        if key in seen:
            continue
        seen.add(key)
        found.append(name)

    # Catch standalone known single-token figures the regex run missed.
    for tok in re.findall(r"\b([A-Za-z][A-Za-z.'\-]+)\b", text):
        low = _clean_token(tok)
        if low in KNOWN_SINGLE:
            canonical = tok.strip('.').split("'")[0]
            if canonical.lower() not in seen:
                seen.add(canonical.lower())
                found.append(canonical)

    # Drop entries that are a subset of a longer captured name
    # (e.g. drop "Trump" when "Donald Trump" is present).
    deduped = []
    for name in found:
        nlow = name.lower()
        if any(nlow != other.lower() and nlow in other.lower().split() for other in found):
            continue
        # also drop single-word entry contained as a token in a longer multiword name
        if ' ' not in name and any(name.lower() in o.lower().split() and o != name for o in found):
            continue
        deduped.append(name)

    return deduped[:max_actors]


if __name__ == '__main__':
    samples = [
        "Texas Gov. Greg Abbott is concerned that a new factory isn't expected to start",
        "President Biden and Donald Trump clash over the Bank of America bailout",
        "Elon Musk's Tesla faces scrutiny from the FDA over autopilot claims",
        "Local council in Springfield approves new park funding",
    ]
    for s in samples:
        print(f"{s[:55]:<57} -> {extract_actors(s)}")
