"""
Gap analysis: bucket assessed concepts strong/partial/weak and flag
critical prerequisite gaps.

Doc module 11/12, cut down: three fixed buckets by mastery threshold
instead of a calibrated confidence model, and "critical" means a weak
concept that is also a prerequisite of something else the learner still
needs — i.e. a bottleneck, not just any weak spot (doc section 27's
"prerequisite masking" idea, in its smallest useful form).
"""

from .graph import graph

STRONG_THRESHOLD = 0.75
WEAK_THRESHOLD = 0.40


def _bucket(mastery: float) -> str:
    if mastery >= STRONG_THRESHOLD:
        return "strong"
    if mastery >= WEAK_THRESHOLD:
        return "partial"
    return "weak"


def analyze_gaps(states: dict) -> dict:
    """
    states: dict of concept_id -> ConceptState (from AssessmentEngine).
    Returns strong/partial/weak concept_id buckets plus a list of
    critical gaps: weak concepts that block a dependent concept.
    """
    buckets = {"strong": [], "partial": [], "weak": []}
    for concept_id, state in states.items():
        buckets[_bucket(state.mastery)].append(concept_id)

    weak_ids = set(buckets["weak"])
    critical = []
    for concept_id, state in states.items():
        if concept_id in weak_ids:
            continue
        # does this (non-weak) concept depend on a weak prerequisite?
        blocking = [p for p in state.concept.prerequisites if p in weak_ids]
        if blocking:
            for p in blocking:
                critical.append({
                    "prerequisite_id": p,
                    "blocks": concept_id,
                    "prerequisite_mastery": round(states[p].mastery, 3) if p in states else None,
                })

    return {
        "buckets": buckets,
        "critical_gaps": critical,
    }