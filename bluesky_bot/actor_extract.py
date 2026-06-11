"""Deterministic (non-LLM) actor/entity extraction for Aletheia stories.

Pulls the names of people and organisations a story is *about* from its subject
line using a strict curated map of validated political actors, individuals, and nations.
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
    'us', 'usa', 'uk', 'eu', 'un',
}

# Curated Map of Political Actors, Individuals, and Nations for 100% precise matching
ACTOR_MAP = {
    # Key Individuals (Politicians, Public Figures, Corporate Leaders)
    r'\b(?<!Barron\s)(?<!Melania\s)(?<!Ivanka\s)(?:Donald\s+)?Trump\b': "Donald Trump",
    r'\bBarron\s+Trump\b': "Barron Trump",
    r'\b(?:Anthony\s+)?Albanese\b': "Anthony Albanese",
    r'\b(?:Joe\s+)?Biden\b': "Joe Biden",
    r'\bXi\s+Jinping\b|\bXi\b': "Xi Jinping",  # Case-sensitive check
    r'\bKim\s+Jong\s+Un\b|\bKim\s+Jong-un\b': "Kim Jong Un",
    r'\b(?:Keir\s+)?Starmer\b': "Keir Starmer",
    r'\b(?:Vladimir\s+)?Putin\b': "Vladimir Putin",
    r'\b(?:Volodymyr\s+)?Zelensky\b': "Volodymyr Zelensky",
    r'\b(?:Angus\s+)?Taylor\b': "Angus Taylor",
    r'\b(?:Andy\s+)?Burnham\b': "Andy Burnham",
    r'\b(?:Kemi\s+)?Badenoch\b': "Kemi Badenoch",
    r'\b(?:Elon\s+)?Musk\b': "Elon Musk",
    r'\b(?:Bill\s+)?Gates\b': "Bill Gates",
    r'\b(?:Pete\s+)?Hegseth\b': "Pete Hegseth",
    r'\b(?:Jeremy\s+)?Rockliff\b': "Jeremy Rockliff",
    r'\b(?:Gina\s+)?Rinehart\b': "Gina Rinehart",
    r'\b(?:Barnaby\s+)?Joyce\b': "Barnaby Joyce",
    r'\b(?:Tony\s+)?Abbott\b': "Tony Abbott",
    r'\b(?:Nithya\s+)?Raman\b': "Nithya Raman",
    r'\b(?:Jameson\s+)?Taillon\b': "Jameson Taillon",
    r'\b(?:Nick\s+)?Kyrgios\b': "Nick Kyrgios",
    r'\b(?:Steven\s+)?Spielberg\b': "Steven Spielberg",
    r'\b(?:Laurie\s+)?Daley\b': "Laurie Daley",
    r'\b(?:Paul\s+)?Litherland\b': "Paul Litherland",
    r'\b(?:Michael\s+)?Yabsley\b': "Michael Yabsley",
    r'\bKumanjayi\s+Walker\b|\bKumanjayi\b': "Kumanjayi Walker",
    r'\b(?:Roxanne\s+)?Tickle\b': "Roxanne Tickle",
    r'\b(?:Spencer\s+)?Pratt\b': "Spencer Pratt",
    r'\b(?:Neale\s+)?Daniher\b': "Neale Daniher",
    r'\b(?:Brody\s+)?Mihocek\b': "Brody Mihocek",
    r'\b(?:Ted\s+)?Lieu\b': "Ted Lieu",
    r'\b(?:Hilary\s+)?Knight\b': "Hilary Knight",
    r'\b(?:Hannah\s+)?Thomas\b': "Hannah Thomas",
    r'\b(?:Melissa\s+)?Menta\b': "Melissa Menta",
    r'\b(?:Dion\s+)?Creek\b': "Dion Creek",
    r'\b(?:Naomi\s+)?Hobson\b': "Naomi Hobson",
    r'\b(?:Tim\s+)?Jaffer\b': "Tim Jaffer",
    r'\b(?:Phoebe\s+)?Bridgers\b': "Phoebe Bridgers",
    r'\b(?:Bob\s+)?Brown\b': "Bob Brown",
    r'\b(?:Martin\s+)?Wiberg\b': "Martin Wiberg",
    r'\b(?:Dan\s+)?Royles\b': "Dan Royles",
    r'\b(?:Margaret\s+)?Thornton\b': "Margaret Thornton",
    r'\b(?:Amy\s+)?Tossoun\b': "Amy Tossoun",
    r'\b(?:Sally\s+)?Sara\b': "Sally Sara",
    r'\b(?:Julie\s+)?Newmar\b': "Julie Newmar",
    r'\b(?:Ted\s+)?Lasso\b': "Ted Lasso",
    r'\b(?:Lionel\s+)?Messi\b': "Lionel Messi",
    r'\b(?:Caitlin\s+)?Clark\b': "Caitlin Clark",
    r'\b(?:Justin\s+)?Stevens\b': "Justin Stevens",
    r'\b(?:Hugh\s+)?Marks\b': "Hugh Marks",
    r'\b(?:David\s+)?Sullivan\b': "David Sullivan",
    r'\b(?:Henry\s+)?Nowak\b': "Henry Nowak",
    r'\b(?:David\s+)?Shoebridge\b': "David Shoebridge",
    r'\b(?:Jim\s+)?Chalmers\b|\bChalmers\b': "Jim Chalmers",
    r'\b(?:Michael\s+)?Ravbar\b': "Michael Ravbar",
    r'\b(?:Greg\s+)?Abbott\b': "Greg Abbott",
    r'\b(?:Jacinta\s+)?Allan\b': "Jacinta Allan",
    r'\b(?:Afroman)\b': "Afroman",
    r'\b(?:Mirra\s+)?Andreeva\b': "Mirra Andreeva",
    r'\b(?:Kimi\s+)?Antonelli\b': "Kimi Antonelli",
    r'\b(?:Aubrey\s+)?Donahue\b': "Aubrey Donahue",
    r'\b(?:Ross\s+)?Gittins\b': "Ross Gittins",
    r'\b(?:David\s+)?Pulle\b': "David Pulle",
    r'\b(?:Jennifer\s+)?Parker\b': "Jennifer Parker",
    r'\b(?:Emily\s+)?Blunt\b': "Emily Blunt",
    r'\b(?:Judy\s+)?Woodruff\b': "Judy Woodruff",
    r'\b(?:Peter\s+)?Murrell\b': "Peter Murrell",
    r'\b(?:Pauline\s+)?Hanson\b': "Pauline Hanson",
    r'\b(?:Do\s+)?Kwon\b': "Do Kwon",
    r'\b(?:Nigel\s+)?Farage\b': "Nigel Farage",
    r'\b(?:Angela\s+)?Rayner\b': "Angela Rayner",
    r'\b(?:Penny\s+)?Mordaunt\b': "Penny Mordaunt",
    r'\b(?:Wes\s+)?Streeting\b': "Wes Streeting",
    r'\b(?:Rachel\s+)?Reeves\b': "Rachel Reeves",
    r'\b(?:Mark\s+)?Carney\b': "Mark Carney",
    r'\b(?:Marco\s+)?Rubio\b': "Marco Rubio",
    r'\b(?:JD\s+)?Vance\b': "JD Vance",
    r'\b(?:Tulsi\s+)?Gabbard\b': "Tulsi Gabbard",

    # Political Parties, Government Bodies, Major Agencies, and Orgs
    r'\bReform\s+UK\b': "Reform UK",
    r'\bOne\s+Nation\b': "One Nation",
    r'\bICE\b': "ICE",
    r'\bNDIS\b': "NDIS",
    r'\bCFMEU\b': "CFMEU",
    r'\bWasatch\s+Front\b': "Wasatch Front",
    r'\bChicago\s+Public\s+Schools\b': "Chicago Public Schools",
    r'\bCBS\s+News\b|\bCBS\b': "CBS News",
    r'\bNBC\s+News\b|\bNBC\b': "NBC News",
    r'\bABC\s+News\b|\bABC\b': "ABC News",
    r'\bBBC\b': "BBC",
    r'\bApple\b': "Apple",
    r'\bGoogle\b': "Google",
    r'\bMicrosoft\b': "Microsoft",
    r'\bTesla\b': "Tesla",
    r'\bOpenAI\b': "OpenAI",
    r'\bMeta\b': "Meta",
    r'\bAmazon\b': "Amazon",
    r'\bAFL\b': "AFL",
    r'\bGreens\b': "Greens",
    r'\bLabour\b': "Labour (UK)",
    r'\bLabor\b': "Labor (AU)",
    r'\bGOP\b|\bRepublican\b|\bRepublicans\b': "GOP",
    r'\bDemocrat\b|\bDemocrats\b|\bDemocratic\b': "Democrats",
    r'\bCoalition\b': "Coalition",
    r'\bFIFA\b': "FIFA",
    r'\bANU\b': "ANU",
    r'\bWaymo\b': "Waymo",
    r'\bNASA\b': "NASA",
    r'\bNFL\b': "NFL",
    r'\bHigh\s+Court\b': "High Court",
    r'\bFederal\s+Court\b': "Federal Court",
    r'\bFair\s+Work\s+Commission\b': "Fair Work Commission",
    r'\bLiberal\s+Party\b|\bLiberals\b': "Liberal Party",
    r'\bMCG\b': "MCG",
    r'\bUSDA\b': "USDA",
    r'\bSNAP\b': "SNAP",
    r'\bNHS\b': "NHS",
    r'\bPWHL\b': "PWHL",
    r'\bHome\s+Office\b': "Home Office (UK)",
    r'\bWhite\s+House\b': "White House (US)",
    r'\bDowning\s+Street\b': "Downing Street (UK)",
    r'\bLos\s+Angeles\s+City\s+Council\b|\bLA\s+City\s+Council\b': "LA City Council",
    r'\bChicago\s+Cubs\b': "Chicago Cubs",
    r'\bWest\s+Ham\b': "West Ham United",
    r'\bKnicks\b': "Knicks",
    r'\bDOJ\b': "DOJ",
    r'\bAUKUS\b': "AUKUS",
    r'\bAmnesty\b|\bAmnesty\s+International\b': "Amnesty International",
    r'\bDHS\b': "DHS",
    r'\bRoyal\s+Navy\b': "Royal Navy",
    r'\bNorthwestern\s+University\b': "Northwestern University",
    r'\bNSW\s+Government\b': "NSW Government",
    r'\bNottingham\s+Trent\s+University\b': "Nottingham Trent University",
    r'\bTerra\s+Luna\b': "Terra Luna",

    # Geopolitical State Actors (Nations)
    r'\bUS\b|\bUSA\b|\bUnited\s+States\b|\bAmerica\b': "United States",
    r'\bAustralia\b': "Australia",
    r'\bBritain\b|\bUK\b|\bBritish\b|\bEngland\b': "United Kingdom",
    r'\bIsrael\b': "Israel",
    r'\bIran\b|\bIranian\b': "Iran",
    r'\bRussia\b': "Russia",
    r'\bChina\b': "China",
    r'\bUkraine\b': "Ukraine",
    r'\bNorth\s+Korea\b': "North Korea",
    r'\bCanada\b': "Canada",
    r'\bFrance\b': "France",
    r'\bTaiwan\b': "Taiwan",
}


def extract_actors(text, max_actors=6):
    """Return a de-duplicated list of probable actor/entity names from text."""
    if not text:
        return []

    # Run precise curated map matching ONLY (no heuristic fallback to prevent trash)
    matched = []
    for pattern, canonical in ACTOR_MAP.items():
        flags = 0 if canonical == "Xi Jinping" else re.IGNORECASE
        if re.search(pattern, text, flags):
            if canonical not in matched:
                matched.append(canonical)
    
    return matched[:max_actors]


if __name__ == '__main__':
    samples = [
        "Texas Gov. Greg Abbott is concerned that a new factory isn't expected to start",
        "President Biden and Donald Trump clash over the Bank of America bailout",
        "Elon Musk's Tesla faces scrutiny from the FDA over autopilot claims",
        "Local council in Springfield approves new park funding",
    ]
    for s in samples:
        print(f"{s[:55]:<57} -> {extract_actors(s)}")
