"""
Isomorphic retelling: abstract, rebind, render.

This is Actualism step 7 made executable:
    Remove names and literal events.
    Preserve plane-state patterns.
    Allow a new narrative to emerge from the dynamics.
    If the patterns remain consistent, the meaning is preserved.

The abstraction is the QUOTIENT (what the story IS, stripped of its setting).
The rebinding is a type-preserving bijection into a new setting.
The rendering re-clothes the skeleton in the target domain's surface forms.

If the framework is doing what it claims, round-tripping the rendered story
back through the parser must recover the same skeleton. That is the falsifier,
and it is Actualism step 8's "survive translation into a different setting".
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from qqci_engine import BeliefState, FunctionalIdentity, Plane, Systemic
from sael import Domain, Transition, parse_story


# ---------------------------------------------------------------------------
# THE SKELETON: what survives translation.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SkeletonStep:
    action: str
    role_types: Tuple[Tuple[str, str], ...]   # (role, functional type), sorted
    role_slots: Tuple[Tuple[str, str], ...]   # (role, slot id), sorted
    effect_shape: Tuple[str, ...]             # effects with entities typed out
    belief: BeliefState
    identity: FunctionalIdentity
    systemic: Systemic
    planes: Tuple[Tuple[Plane, float], ...]

    def matches(self, other: "SkeletonStep") -> Dict[str, bool]:
        return {
            "action": self.action == other.action,
            "role_types": self.role_types == other.role_types,
            "role_slots": self.role_slots == other.role_slots,
            "effects": self.effect_shape == other.effect_shape,
            "belief": self.belief == other.belief,
            "identity": self.identity == other.identity,
            "systemic": self.systemic == other.systemic,
            "planes": self.planes == other.planes,
        }


@dataclass
class Skeleton:
    steps: List[SkeletonStep] = field(default_factory=list)
    slot_types: Dict[str, str] = field(default_factory=dict)   # slot id -> type
    bindings: Dict[str, str] = field(default_factory=dict)     # entity -> slot id

    def score_against(self, other: "Skeleton") -> Tuple[float, List[dict]]:
        n = max(len(self.steps), len(other.steps))
        if n == 0:
            return 0.0, []
        rows, total, checks = [], 0, 0
        for i in range(n):
            if i >= len(self.steps) or i >= len(other.steps):
                rows.append({"step": i + 1, "missing": True})
                checks += 8
                continue
            m = self.steps[i].matches(other.steps[i])
            rows.append({"step": i + 1, **m})
            total += sum(1 for v in m.values() if v)
            checks += len(m)
        return (total / checks if checks else 0.0), rows


def abstract(transitions: List[Transition], domain: Domain) -> Skeleton:
    """
    Remove names and literal events. Entities become typed slots, allocated in
    order of first appearance so identity is preserved across the whole story:
    the same fisherman in step 1 and step 6 is the same slot.
    """
    skel = Skeleton()
    counters: Dict[str, int] = {}

    def slot_for(entity: str) -> str:
        if entity in skel.bindings:
            return skel.bindings[entity]
        ftype = domain.type_of(entity) or "UNKNOWN"
        counters[ftype] = counters.get(ftype, 0) + 1
        sid = f"{ftype}#{counters[ftype]}"
        skel.bindings[entity] = sid
        skel.slot_types[sid] = ftype
        return sid

    for t in transitions:
        role_types, role_slots = [], []
        for role, entity in sorted(t.roles.items()):
            sid = slot_for(entity)
            role_types.append((role, domain.type_of(entity) or "UNKNOWN"))
            role_slots.append((role, sid))

        # Effects with every entity replaced by its slot: the delta PATTERN.
        shape = []
        for e in t.effects:
            s = e
            for entity, sid in skel.bindings.items():
                s = s.replace(entity, sid)
            shape.append(s)

        skel.steps.append(SkeletonStep(
            action=t.action,
            role_types=tuple(role_types),
            role_slots=tuple(role_slots),
            effect_shape=tuple(sorted(shape)),
            belief=t.belief,
            identity=t.identity,
            systemic=t.systemic,
            planes=tuple(sorted(t.planes.items())),
        ))
    return skel


def rebind(skel: Skeleton, target: Domain) -> Dict[str, str]:
    """
    Type-preserving bijection: each slot takes a target-domain entity of the
    same functional type. One slot, one entity, consistently across the story.
    """
    mapping: Dict[str, str] = {}
    used: set = set()
    for sid, ftype in skel.slot_types.items():
        entity = target.entity_for_type(ftype, used)
        if entity is None:
            raise ValueError(
                f"Target domain '{target.name}' has no entity of type {ftype}. "
                f"Isomorphic rebinding requires type coverage."
            )
        mapping[sid] = entity
        used.add(entity)
    return mapping


# ---------------------------------------------------------------------------
# RENDERING: re-clothe the skeleton in the target domain's surface forms.
# ---------------------------------------------------------------------------

# Types that take no article (mass nouns / abstractions).
BARE_TYPES = {"MATERIAL", "KNOWLEDGE"}

TEMPLATES_ACTIVE = {
    "@CREATE":    "{Agent} {verb} {a_patient} from {bare_source}.",
    "@RELOCATE":  "{Agent} {verb} {the_patient} to {the_destination}.",
    "@TERMINATE": "{Agent} {verb} {the_patient}.",
    "@AID":       "{Agent} {verb} {the_patient}.",
    "@TRANSFER":  "{Agent} {verb} {the_patient} to {the_recipient}.",
    "@ACQUIRE":   "{Agent} {verb} {the_patient}.",
    "@MUTATE":    "{Agent} {verb} {the_patient}.",
    "@INSTRUCT":  "{Agent} {verb} {the_recipient} about {bare_topic}.",
}

TEMPLATES_PASSIVE = {
    "@TERMINATE": "{Patient} was {verb} by {the_agent}.",
    "@AID":       "{Patient} was {verb} by {the_agent}.",
    "@CREATE":    "{Patient} was {verb} from {bare_source} by {the_agent}.",
    "@MUTATE":    "{Patient} was {verb} by {the_agent}.",
}


def _np(entity: str, domain: Domain, capital: bool = False) -> str:
    ftype = domain.type_of(entity) or ""
    pretty = domain.pretty(entity)
    if ftype in BARE_TYPES:
        return pretty
    art = "The" if capital else "the"
    return f"{art} {pretty}"


def render(skel: Skeleton, mapping: Dict[str, str], target: Domain,
           sigmas: Optional[List[Dict[str, str]]] = None) -> List[str]:
    """
    Render each skeleton step as a target-domain sentence. The style residue
    (sigma) is applied here, not stored in the referent: that is the factoring.
    Passing sigmas preserves the original voice; omitting them renders all
    active, which is the pure-quotient behaviour for comparison.
    """
    out: List[str] = []
    for i, step in enumerate(skel.steps):
        roles = {role: mapping[sid] for role, sid in step.role_slots}
        sigma = sigmas[i] if sigmas and i < len(sigmas) else {"voice": "active"}
        passive = sigma.get("voice") == "passive" and step.action in TEMPLATES_PASSIVE
        tmpl = (TEMPLATES_PASSIVE if passive else TEMPLATES_ACTIVE).get(step.action)
        if tmpl is None:
            continue

        fields: Dict[str, str] = {"verb": target.verb_style.get(step.action, "acted")}
        for role, entity in roles.items():
            pretty = target.pretty(entity)
            ftype = target.type_of(entity) or ""
            fields[role.capitalize()] = _np(entity, target, capital=True)
            fields[f"the_{role}"] = _np(entity, target)
            fields[f"bare_{role}"] = pretty
            fields[f"a_{role}"] = (pretty if ftype in BARE_TYPES
                                   else f"a {pretty}")
        try:
            out.append(tmpl.format(**fields))
        except KeyError:
            continue  # a template slot has no binding: skip rather than invent
    return out


def retell(sentences: List[str], source: Domain, target: Domain,
           preserve_voice: bool = True) -> Tuple[List[str], Skeleton, Dict[str, str],
                                                 List[Transition]]:
    """Full pipeline: parse, abstract, rebind, render."""
    transitions = parse_story(sentences, source)
    skel = abstract(transitions, source)
    mapping = rebind(skel, target)
    sigmas = [t.sigma for t in transitions] if preserve_voice else None
    rendered = render(skel, mapping, target, sigmas)
    return rendered, skel, mapping, transitions
