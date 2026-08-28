import pytest

from app.graph import ConceptGraph,Concept,graph


def test_roles_present():
    assert "ML Engineer" in graph.roles
    assert "Data Analyst" in graph.roles


def test_each_role_has_ten_concepts():
    for role in graph.roles:
        assert len(graph.concepts_for_role(role))==10


def test_topological_order_respects_prerequisites():
    for role in graph.roles:
        order=graph.topological_order(role)
        seen=set()
        for concept in order:
            for prereq_id in concept.prerequisites:
                assert prereq_id in seen
            seen.add(concept.concept_id)


def test_all_prerequisite_ids_transitive():
    result=graph.all_prerequisite_ids("neural_networks")
    assert "optimization" in result
    assert "linear_algebra" in result
    assert "classification" in result
    assert "regression" in result


def test_all_prerequisite_ids_unknown_concept_returns_empty():
    assert graph.all_prerequisite_ids("does_not_exist")==set()


def test_dangling_prerequisite_raises():
    concepts=[Concept(concept_id="a",name="A",skill_id="s",role_id="R",prerequisites=["ghost"],role_importance=0.5,difficulty=1,estimated_learning_cost=1)]
    with pytest.raises(ValueError):
        ConceptGraph(roles=["R"],concepts=concepts)


def test_cycle_raises():
    concepts=[
    Concept(concept_id="a",name="A",skill_id="s",role_id="R",prerequisites=["b"],role_importance=0.5,difficulty=1,estimated_learning_cost=1),
    Concept(concept_id="b",name="B",skill_id="s",role_id="R",prerequisites=["a"],role_importance=0.5,difficulty=1,estimated_learning_cost=1)
    ]
    with pytest.raises(ValueError):
        ConceptGraph(roles=["R"],concepts=concepts)
