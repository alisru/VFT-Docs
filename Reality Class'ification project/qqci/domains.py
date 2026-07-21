"""
Domain lexicons. Each maps surface nouns to FUNCTIONAL TYPES.

The functional type is what survives rebinding. A boat and a product are the
same thing at the level the framework operates on: a constructed vessel the
agent commits to and can lose. Actualism step 6: functional identity, not
literal role.
"""

from sael import Domain

# Functional types used across all domains. Keep this list closed: it is the
# type vocabulary the isomorphism is defined over.
#   AGENT      the protagonist, the one who wills
#   PATRON     the established power that can aid or withhold
#   FORCE      an impersonal destructive agent
#   VESSEL     the constructed thing the agent commits to
#   MATERIAL   what the vessel is made from
#   GROUND     the place ventured to
#   HAVEN      the place of safety
#   TOKEN      a transferable object of value
#   KNOWLEDGE  a topic that can be taught

SEA = Domain(
    name="sea",
    context="maritime",
    entities={
        "fisherman": "AGENT",
        "harbourmaster": "PATRON",
        "storm": "FORCE",
        "boat": "VESSEL",
        "oak": "MATERIAL",
        "reef": "GROUND",
        "harbour": "HAVEN",
        "charts": "TOKEN",
        "tides": "KNOWLEDGE",
    },
    verb_style={
        "@CREATE": "built",
        "@RELOCATE": "sailed",
        "@TERMINATE": "wrecked",
        "@AID": "rescued",
        "@TRANSFER": "gave",
        "@ACQUIRE": "took",
        "@MUTATE": "repaired",
        "@INSTRUCT": "taught",
    },
)

STARTUP = Domain(
    name="startup",
    context="commerce",
    entities={
        "founder": "AGENT",
        "investor": "PATRON",
        "recession": "FORCE",
        "product": "VESSEL",
        "opensource": "MATERIAL",
        "market": "GROUND",
        "incubator": "HAVEN",
        "equity": "TOKEN",
        "retention": "KNOWLEDGE",
    },
    display={"opensource": "open source"},
    verb_style={
        "@CREATE": "built",
        "@RELOCATE": "launched",
        "@TERMINATE": "destroyed",
        "@AID": "backed",
        "@TRANSFER": "gave",
        "@ACQUIRE": "took",
        "@MUTATE": "fixed",
        "@INSTRUCT": "taught",
    },
)

ORBIT = Domain(
    name="orbit",
    context="physics",
    entities={
        "engineer": "AGENT",
        "director": "PATRON",
        "solarflare": "FORCE",
        "probe": "VESSEL",
        "alloy": "MATERIAL",
        "asteroid": "GROUND",
        "station": "HAVEN",
        "telemetry": "TOKEN",
        "drift": "KNOWLEDGE",
    },
    display={"solarflare": "solar flare"},
    verb_style={
        "@CREATE": "assembled",
        "@RELOCATE": "flew",
        "@TERMINATE": "destroyed",
        "@AID": "saved",
        "@TRANSFER": "sent",
        "@ACQUIRE": "secured",
        "@MUTATE": "repaired",
        "@INSTRUCT": "warned",
    },
)

ALL_DOMAINS = {d.name: d for d in (SEA, STARTUP, ORBIT)}


# The source story. Deliberately mixed voice: sentence 4 is passive, so the
# parser must place the agent correctly rather than by word order. That is the
# vicious case a bag-of-words collapse gets wrong.
SEA_STORY = [
    "The fisherman built a boat from oak.",
    "The fisherman sailed the boat to the reef.",
    "The storm wrecked the boat.",
    "The fisherman was rescued by the harbourmaster.",
    "The fisherman gave the charts to the harbourmaster.",
    "The harbourmaster taught the fisherman about tides.",
]
