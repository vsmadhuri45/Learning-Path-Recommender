"""
Role -> Skill -> Concept dependency graph.

Loads the static concept graph (backend/app/data/concept_graph.json) once at
import time and exposes small, dependency-free lookup helpers. Every other
piece of the assessment engine (BKT mastery model, question selection,
stopping criteria, gap analysis, roadmap builder) should go through this
module rather than reading the JSON file directly.

Kept intentionally simple for the prototype: two hardcoded roles, ~10
concepts each, no persistence layer. Swap `_load()` for a DB-backed version
later without changing any call sites.
"""

import json
from pathlib import Path

from pydantic import BaseModel

DATA_PATH = Path(__file__).resolve().parent / "data" / "concept_graph.json"


class Concept(BaseModel):
    concept_id: str
    name: str
    skill_id: str
    role_id: str
    prerequisites: list[str] = []
    role_importance: float
    difficulty: int
    estimated_learning_cost: float


class ConceptGraph:
    """In-memory view of the concept graph with lookup + traversal helpers."""

    def __init__(self, roles: list[str], concepts: list[Concept]):
        self.roles = roles
        self._by_id: dict[str, Concept] = {c.concept_id: c for c in concepts}
        self._validate()

    def _validate(self) -> None:
        """Fail fast on bad data: dangling prerequisite refs or cycles."""
        for concept in self._by_id.values():
            for prereq_id in concept.prerequisites:
                if prereq_id not in self._by_id:
                    raise ValueError(
                        f"{concept.concept_id} references unknown prerequisite '{prereq_id}'"
                    )
        for concept in self._by_id.values():
            self._check_no_cycle(concept.concept_id, set())

    def _check_no_cycle(self, concept_id: str, seen: set[str]) -> None:
        if concept_id in seen:
            raise ValueError(f"Cycle detected in concept graph at '{concept_id}'")
        seen = seen | {concept_id}
        for prereq_id in self._by_id[concept_id].prerequisites:
            self._check_no_cycle(prereq_id, seen)

    def get(self, concept_id: str) -> Concept | None:
        return self._by_id.get(concept_id)

    def concepts_for_role(self, role: str) -> list[Concept]:
        return [c for c in self._by_id.values() if c.role_id == role]

    def prerequisites_of(self, concept_id: str) -> list[Concept]:
        concept = self._by_id[concept_id]
        return [self._by_id[p] for p in concept.prerequisites]

    def all_prerequisite_ids(self, concept_id: str) -> set[str]:
        """Transitive closure of prerequisites (direct + indirect)."""
        concept = self._by_id.get(concept_id)
        if concept is None:
            return set()
        direct = set(concept.prerequisites)
        transitive: set[str] = set()
        for p in direct:
            transitive |= self.all_prerequisite_ids(p)
        return direct | transitive

    def topological_order(self, role: str) -> list[Concept]:
        """Concepts for a role, ordered so prerequisites always precede dependents."""
        role_concepts = {c.concept_id: c for c in self.concepts_for_role(role)}
        visited: set[str] = set()
        ordered: list[Concept] = []

        def visit(concept_id: str) -> None:
            if concept_id in visited or concept_id not in role_concepts:
                return
            visited.add(concept_id)
            for prereq_id in role_concepts[concept_id].prerequisites:
                visit(prereq_id)
            ordered.append(role_concepts[concept_id])

        for cid in role_concepts:
            visit(cid)
        return ordered


def _load() -> ConceptGraph:
    raw = json.loads(DATA_PATH.read_text())
    concepts = [Concept(**c) for c in raw["concepts"]]
    return ConceptGraph(roles=raw["roles"], concepts=concepts)


graph = _load()