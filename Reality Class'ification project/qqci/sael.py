"""
SAEL: Semantic Action-Effect Language.

Collapses isomorphic surface expressions into one canonical transition while
retaining the manner of saying. The operation is a FACTORING, not a bare
quotient: nothing is deleted, reference and style live in separate coordinates.

    T = <C, alpha, Delta, sigma>

    C      Context   - the domain envelope (commerce, physics, ...)
    alpha  Action    - the collapsed canonical action primitive
    Delta  Effects   - the actual state mutation
    sigma  Residue   - HOW it was said (voice, register). Q4/Q7 content.

Plus, per Actualism, each transition carries its plane-state pattern: which
planes are active and what belief state the agent holds on each.

Scope honesty: this is a hand-seeded parser over constrained declarative
English, not open-domain NLP. It exists to test whether the STRUCTURE holds,
not to demonstrate coverage.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from qqci_engine import (
    BeliefState,
    CoherenceVector,
    FunctionalIdentity,
    Plane,
    QqciAddress,
    Ray,
    Systemic,
    DEFAULT_SYSTEMIC,
)


# ---------------------------------------------------------------------------
# THE COLLAPSE DICTIONARY
# Canonical actions with their equivalence classes of surface verbs.
# Five from the SAEL proposal, three added here for narrative coverage.
# ---------------------------------------------------------------------------

COLLAPSE: Dict[str, List[str]] = {
    "@TRANSFER":  ["give", "gave", "given", "send", "sent", "pay", "paid",
                   "wire", "wired", "hand", "handed", "donate", "donated",
                   "bequeath", "bequeathed", "pass", "passed", "offer", "offered"],
    "@ACQUIRE":   ["buy", "bought", "purchase", "purchased", "obtain", "obtained",
                   "get", "got", "grab", "grabbed", "fetch", "fetched",
                   "secure", "secured", "receive", "received", "take", "took"],
    "@MUTATE":    ["edit", "edited", "change", "changed", "modify", "modified",
                   "transform", "transformed", "adjust", "adjusted", "tweak",
                   "tweaked", "update", "updated", "repair", "repaired",
                   "mend", "mended", "fix", "fixed"],
    "@RELOCATE":  ["go", "went", "travel", "travelled", "traveled", "walk",
                   "walked", "fly", "flew", "move", "moved", "drive", "drove",
                   "run", "ran", "sail", "sailed", "carry", "carried",
                   "displace", "displaced", "steer", "steered",
                   "launch", "launched", "ship", "shipped"],
    "@TERMINATE": ["delete", "deleted", "kill", "killed", "destroy", "destroyed",
                   "end", "ended", "stop", "stopped", "cancel", "cancelled",
                   "erase", "erased", "wreck", "wrecked", "sink", "sank",
                   "shatter", "shattered", "ruin", "ruined"],
    # --- extensions beyond the original five, for narrative coverage ---
    "@CREATE":    ["build", "built", "make", "made", "craft", "crafted",
                   "forge", "forged", "construct", "constructed", "found",
                   "founded", "raise", "raised", "assemble", "assembled"],
    "@AID":       ["rescue", "rescued", "save", "saved", "help", "helped",
                   "aid", "aided", "support", "supported", "shelter",
                   "sheltered", "back", "backed"],
    "@INSTRUCT":  ["teach", "taught", "show", "showed", "shown", "warn",
                   "warned", "tell", "told", "explain", "explained",
                   "instruct", "instructed", "advise", "advised"],
}

VERB_TO_ACTION: Dict[str, str] = {
    v: a for a, verbs in COLLAPSE.items() for v in verbs
}


# Which planes each canonical action natively engages, and with what weight.
# This is the action's plane signature: its fixed geometry, not learned.
ACTION_PLANES: Dict[str, Dict[Plane, float]] = {
    "@CREATE":    {Plane.WHO: 1.0, Plane.WHAT: 1.0, Plane.WHERE: 0.9, Plane.CAUSE: 0.8},
    "@RELOCATE":  {Plane.WHO: 0.9, Plane.WHERE: 1.0, Plane.HOW: 0.8, Plane.CAUSE: 0.7},
    "@TERMINATE": {Plane.WHERE: 1.0, Plane.CAUSE: 1.0, Plane.EFFECT: 1.0, Plane.WHO: 0.7},
    "@AID":       {Plane.WHO: 1.0, Plane.EFFECT: 1.0, Plane.WHY: 0.9, Plane.CAUSE: 0.7},
    "@TRANSFER":  {Plane.WHO: 0.9, Plane.WHAT: 0.9, Plane.CAUSE: 0.8, Plane.EFFECT: 0.8},
    "@ACQUIRE":   {Plane.WHO: 0.9, Plane.WHAT: 1.0, Plane.WHERE: 0.7, Plane.EFFECT: 0.8},
    "@MUTATE":    {Plane.WHAT: 1.0, Plane.HOW: 1.0, Plane.WHERE: 0.8, Plane.CAUSE: 0.8},
    "@INSTRUCT":  {Plane.WHY: 1.0, Plane.HOW: 1.0, Plane.WHO: 0.9, Plane.CAUSE: 0.8},
}

# The belief state each action expresses by default, per Actualism step 2.
ACTION_BELIEF: Dict[str, BeliefState] = {
    "@CREATE":    BeliefState.WILL_TO_KNOW,
    "@RELOCATE":  BeliefState.WILL_TO_KNOW,
    "@TERMINATE": BeliefState.INSULT,
    "@AID":       BeliefState.TRUTH,
    "@TRANSFER":  BeliefState.TRUTH,
    "@ACQUIRE":   BeliefState.WILL_TO_KNOW,
    "@MUTATE":    BeliefState.WILL_TO_KNOW,
    "@INSTRUCT":  BeliefState.TRUTH,
}

# The functional identity an action assigns to its agent (Actualism step 6).
ACTION_IDENTITY: Dict[str, FunctionalIdentity] = {
    "@CREATE":    FunctionalIdentity.INQUIRER,
    "@RELOCATE":  FunctionalIdentity.INQUIRER,
    "@TERMINATE": FunctionalIdentity.CATALYST,
    "@AID":       FunctionalIdentity.STABILISER,
    "@TRANSFER":  FunctionalIdentity.STABILISER,
    "@ACQUIRE":   FunctionalIdentity.INQUIRER,
    "@MUTATE":    FunctionalIdentity.ENFORCER,
    "@INSTRUCT":  FunctionalIdentity.STABILISER,
}

# Effect templates: the state delta each action commits.
# Written against role names so they survive rebinding unchanged.
EFFECT_TEMPLATES: Dict[str, List[Tuple[str, str, str]]] = {
    "@CREATE":    [("patient", "exists", "=> true"),
                   ("patient", "origin_material", "=> {source}"),
                   ("agent", "holdings", "=> +{patient}")],
    "@RELOCATE":  [("patient", "position", "=> to {destination}"),
                   ("agent", "position", "=> to {destination}")],
    "@TERMINATE": [("patient", "exists", "=> false"),
                   ("agent", "holdings", "=> -{patient}")],
    "@AID":       [("patient", "condition", "=> restored"),
                   ("agent", "obligation_held_over", "=> +{patient}")],
    "@TRANSFER":  [("patient", "owner", "=> {recipient}"),
                   ("agent", "holdings", "=> -{patient}"),
                   ("recipient", "holdings", "=> +{patient}")],
    "@ACQUIRE":   [("patient", "owner", "=> {agent}"),
                   ("agent", "holdings", "=> +{patient}")],
    "@MUTATE":    [("patient", "state", "=> altered"),
                   ("patient", "integrity", "=> +1")],
    "@INSTRUCT":  [("recipient", "knowledge", "=> +{topic}"),
                   ("agent", "knowledge", "=> shared")],
}


# ---------------------------------------------------------------------------
# ENTITY TYPING: the functional type is what survives rebinding.
# ---------------------------------------------------------------------------

@dataclass
class Domain:
    name: str
    context: str                     # the SAEL context envelope
    entities: Dict[str, str]         # surface noun -> functional type
    verb_style: Dict[str, str]       # canonical action -> domain-flavoured verb
    display: Dict[str, str] = field(default_factory=dict)  # token -> pretty form
    articles: Dict[str, str] = field(default_factory=dict)

    def pretty(self, noun: str) -> str:
        return self.display.get(noun, noun)

    def type_of(self, noun: str) -> Optional[str]:
        return self.entities.get(noun)

    def entity_for_type(self, ftype: str, used: set) -> Optional[str]:
        for noun, t in self.entities.items():
            if t == ftype and noun not in used:
                return noun
        for noun, t in self.entities.items():
            if t == ftype:
                return noun
        return None

    def article(self, noun: str) -> str:
        return self.articles.get(noun, "the")


# ---------------------------------------------------------------------------
# THE TRANSITION: <C, alpha, Delta, sigma> plus plane-state
# ---------------------------------------------------------------------------

@dataclass
class Transition:
    context: str
    action: str
    roles: Dict[str, str]                     # role -> surface entity
    effects: List[str] = field(default_factory=list)
    sigma: Dict[str, str] = field(default_factory=dict)   # style residue
    planes: Dict[Plane, float] = field(default_factory=dict)
    belief: BeliefState = BeliefState.TRUTH
    identity: FunctionalIdentity = FunctionalIdentity.UNSET
    systemic: Systemic = Systemic.NEUTRAL
    source_text: str = ""

    @property
    def address(self) -> QqciAddress:
        """
        Compositional address: the transition is rooted at its dominant plane,
        drilled by its second-strongest. The interrogative path IS the identity,
        so ordering matters and is not commutative.
        """
        ranked = sorted(self.planes.items(), key=lambda kv: (-kv[1], kv[0]))
        if len(ranked) >= 2:
            return QqciAddress.of(ranked[0][0], ranked[1][0])
        return QqciAddress.of(ranked[0][0] if ranked else Plane.WHAT)

    def coherence(self) -> CoherenceVector:
        cv = CoherenceVector()
        for p, w in self.planes.items():
            cv[p] = w
        return cv

    def rays(self, observer_prefix: str = "") -> List[Ray]:
        """
        Each active plane casts a constraint ray at the transition's canonical
        coordinate. Independent vantages, one voxel. Intersection is meaning.
        """
        target = self.voxel()
        return [
            Ray(observer=f"{observer_prefix}{p.name}", plane=p,
                target=target, strength=w)
            for p, w in self.planes.items()
        ]

    def voxel(self) -> str:
        """The canonical coordinate: what the transition IS, stripped of style."""
        role_sig = ",".join(f"{k}:{v}" for k, v in sorted(self.roles.items()))
        return f"{self.context}::{self.action}{{{role_sig}}}"

    def render_sael(self) -> str:
        params = ", ".join(f"{k}={v}" for k, v in sorted(self.roles.items()))
        head = f"{self.context} :: {self.action} {{ {params} }} ->"
        body = "\n".join(f"    {e};" for e in self.effects)
        return head + "\n" + body.rstrip(";")


# ---------------------------------------------------------------------------
# THE PARSER: Phi(L) -> <C, alpha, Delta, sigma>
# ---------------------------------------------------------------------------

PREP_TO_ROLE = {
    "to": "destination",
    "into": "destination",
    "toward": "destination",
    "from": "source",
    "out": "source",
    "with": "instrument",
    "using": "instrument",
    "about": "topic",
    "of": "topic",
    "for": "beneficiary",
    "by": "agent",
    "at": "destination",
    "on": "destination",
}

# @TRANSFER and @INSTRUCT reassign 'destination' to 'recipient': a person
# received it, not a place. Compositional typing: the same preposition takes
# a different role depending on the action operating over it.
RECIPIENT_ACTIONS = {"@TRANSFER", "@INSTRUCT", "@AID"}

STOPWORDS = {"the", "a", "an", "his", "her", "their", "its", "my", "our", "some"}
BE_FORMS = {"was", "were", "is", "are", "been", "being"}


def _clean(text: str, domain: Optional[Domain] = None) -> List[str]:
    text = text.lower().strip().rstrip(".!?")
    text = re.sub(r"[^a-z0-9\s'-]", " ", text)
    # Rank-2 pre-pass: recompose known multi-word display forms into their
    # single-token identity ("solar flare" -> "solarflare") BEFORE rank-1
    # tokenisation. Without this, a phrase-rank surface form fails to contract
    # to its word-rank node and the entity vanishes from the parse.
    if domain and domain.display:
        for token, pretty in sorted(domain.display.items(),
                                    key=lambda kv: -len(kv[1])):
            text = text.replace(pretty.lower(), token)
    return [t for t in text.split() if t]


def validate_domain(domain: Domain) -> List[str]:
    """
    Build-time check: every domain-flavoured verb must exist in the Collapse
    Dictionary, or sentences using it silently fail to parse and the whole
    story misaligns. A never-parse is a diagnostic, not a mystery.
    """
    problems = []
    for action, verb in domain.verb_style.items():
        if verb not in VERB_TO_ACTION:
            problems.append(
                f"{domain.name}: verb '{verb}' for {action} is not in the "
                f"Collapse Dictionary")
        elif VERB_TO_ACTION[verb] != action:
            problems.append(
                f"{domain.name}: verb '{verb}' collapses to "
                f"{VERB_TO_ACTION[verb]}, not {action}")
    return problems


def parse_sentence(text: str, domain: Domain) -> Optional[Transition]:
    """
    Hand-seeded parse of one declarative sentence into a canonical transition.
    Handles active and passive voice; passive is recorded in sigma, not in the
    referent, which is the whole point of the factoring.
    """
    tokens = _clean(text, domain)
    if not tokens:
        return None

    # --- locate the verb and its canonical action ---
    verb_idx, action, surface_verb = -1, None, None
    for i, t in enumerate(tokens):
        if t in VERB_TO_ACTION:
            verb_idx, action, surface_verb = i, VERB_TO_ACTION[t], t
            break
    if action is None:
        return None

    # --- voice detection: sigma, not referent ---
    passive = verb_idx > 0 and tokens[verb_idx - 1] in BE_FORMS
    sigma = {
        "voice": "passive" if passive else "active",
        "surface_verb": surface_verb,
        "register": "plain",
    }

    def entities_in(span: List[str]) -> List[str]:
        return [t for t in span if t not in STOPWORDS and domain.type_of(t)]

    head_span = tokens[: verb_idx - 1] if passive else tokens[:verb_idx]
    tail_span = tokens[verb_idx + 1:]

    roles: Dict[str, str] = {}

    # --- prepositional roles from the tail ---
    tail_entities: List[str] = []
    i = 0
    while i < len(tail_span):
        tok = tail_span[i]
        if tok in PREP_TO_ROLE:
            role = PREP_TO_ROLE[tok]
            rest = tail_span[i + 1:]
            found = entities_in(rest)
            if found:
                if role == "destination" and action in RECIPIENT_ACTIONS:
                    role = "recipient"
                roles.setdefault(role, found[0])
                # consume up to and including that entity
                j = rest.index(found[0])
                i += 1 + j + 1
                continue
        else:
            if tok not in STOPWORDS and domain.type_of(tok):
                tail_entities.append(tok)
        i += 1

    head_entities = entities_in(head_span)

    # --- assign agent / patient by voice ---
    if passive:
        # "The fisherman was rescued by the harbourmaster"
        patient = head_entities[0] if head_entities else None
        agent = roles.pop("agent", None)
        if patient:
            roles["patient"] = patient
        if agent:
            roles["agent"] = agent
    else:
        if head_entities:
            roles["agent"] = head_entities[0]
        if tail_entities:
            roles["patient"] = tail_entities[0]
        roles.pop("agent", None) if "agent" not in roles else None
        if "agent" not in roles and head_entities:
            roles["agent"] = head_entities[0]

    # @INSTRUCT: "taught the fisherman about tides" -> recipient is the object
    if action == "@INSTRUCT" and "patient" in roles and "recipient" not in roles:
        roles["recipient"] = roles.pop("patient")

    if not roles:
        return None

    # --- Delta: bind the effect template to the roles present ---
    effects: List[str] = []
    for subject, prop, mutation in EFFECT_TEMPLATES.get(action, []):
        if subject not in roles:
            continue
        try:
            filled = mutation.format(**roles)
        except KeyError:
            continue  # template slot has no binding in this sentence
        effects.append(f"{roles[subject]}.{prop} {filled}")

    belief = ACTION_BELIEF.get(action, BeliefState.TRUTH)
    return Transition(
        context=domain.context,
        action=action,
        roles=roles,
        effects=effects,
        sigma=sigma,
        planes=dict(ACTION_PLANES.get(action, {})),
        belief=belief,
        identity=ACTION_IDENTITY.get(action, FunctionalIdentity.UNSET),
        systemic=DEFAULT_SYSTEMIC.get(belief, Systemic.NEUTRAL),
        source_text=text.strip(),
    )


def parse_story(sentences: List[str], domain: Domain) -> List[Transition]:
    out = []
    for s in sentences:
        t = parse_sentence(s, domain)
        if t is not None:
            out.append(t)
    return out
