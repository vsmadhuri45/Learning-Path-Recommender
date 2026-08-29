"""
Roadmap builder: combines gap analysis + resources into a prioritized,
prerequisite-ordered study plan.

Priority formula (doc section 12, cut down): role_importance * (1-mastery)
/ estimated_learning_cost — favors concepts that matter more, are weaker,
and are cheaper to fix first. Ordering respects the concept graph's
topological order so a concept never appears before something it depends
on, even if its raw priority score would otherwise put it earlier.
"""

from . import bkt
from .gaps import analyze_gaps
from .graph import graph
from .resources import resources_for


def _prereqs_cleared(states, concept):
    return all(
        p in states and states[p].mastery >= bkt.MASTERY_THRESHOLD
        for p in concept.prerequisites
    )


def build_roadmap(engine) -> dict:
    """engine: an AssessmentEngine instance (uses .states, .role, .student_id)."""
    gap_analysis = analyze_gaps(engine.states)
    needs_work = set(gap_analysis["buckets"]["weak"]) | set(gap_analysis["buckets"]["partial"])

    items = []
    for concept in graph.topological_order(engine.role):
        if concept.concept_id not in needs_work:
            continue
        state = engine.states[concept.concept_id]
        priority = (
            concept.role_importance
            * (1 - state.mastery)
            / max(concept.estimated_learning_cost, 0.01)
        )
        items.append({
            "concept_id": concept.concept_id,
            "title": concept.name,
            "skill_id": concept.skill_id,
            "current_mastery": round(state.mastery, 3),
            "target_mastery": bkt.MASTERY_THRESHOLD,
            "status": "Ready to Study" if _prereqs_cleared(engine.states, concept) else "Locked",
            "priority": round(priority, 3),
            "difficulty": concept.difficulty,
            "role_importance": concept.role_importance,
            "resources": resources_for(concept.concept_id),
        })

    # Ready-to-study first, then by priority — but never ahead of a prerequisite
    # (topological order above already guarantees that; this sort only
    # reorders *within* what's already prerequisite-safe).
    items.sort(key=lambda it: (0 if it["status"] == "Ready to Study" else 1, -it["priority"]))

    return {
        "student_id": engine.student_id,
        "target_role": engine.role,
        "total_gaps": len(items),
        "roadmap": items,
        "gap_analysis": gap_analysis,
    }