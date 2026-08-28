import random

import pytest

from app.assessment import AssessmentEngine


def run_session(role,skills=None,seed=0,bias=0.7):
    random.seed(seed)
    engine=AssessmentEngine("demo",role,skills or [])
    order=[]
    while not engine.is_complete():
        q=engine.next_question()
        if q is None:
            break
        order.append(engine.current_concept_id)
        correct=random.random()<bias
        engine.submit_answer(q["id"],q["answer"] if correct else "WRONG")
    return engine,order


def test_invalid_role_raises():
    with pytest.raises(ValueError):
        AssessmentEngine("demo","Astronaut",[])


def test_session_terminates():
    engine,order=run_session("ML Engineer")
    assert len(order)>0
    assert engine.is_complete()


def test_regression_not_asked_before_its_prerequisites():
    engine,order=run_session("ML Engineer",seed=1)
    if "regression" in order:
        first_regression=order.index("regression")
        assert "statistics" in order[:first_regression]
        assert "linear_algebra" in order[:first_regression]


def test_neural_networks_not_asked_before_its_prerequisites():
    engine,order=run_session("ML Engineer",seed=1)
    if "neural_networks" in order:
        first_nn=order.index("neural_networks")
        assert "optimization" in order[:first_nn]
        assert "classification" in order[:first_nn]


def test_knowledge_profile_shape():
    engine,order=run_session("Data Analyst",seed=2)
    profile=engine.knowledge_profile()
    assert profile["student_id"]=="demo"
    assert profile["target_role"]=="Data Analyst"
    assert len(profile["concepts"])==10
    for c in profile["concepts"]:
        assert set(c.keys())=={"concept_id","skill_id","mastery","uncertainty","evidence_count","role_importance"}
        assert 0<=c["mastery"]<=1
        assert c["uncertainty"] in ("high","medium","low")


def test_submit_answer_mismatch_returns_none():
    engine=AssessmentEngine("demo","ML Engineer",[])
    engine.next_question()
    result=engine.submit_answer("not-a-real-question-id","anything")
    assert result is None


def test_submit_answer_mismatch_does_not_consume_a_question():
    engine=AssessmentEngine("demo","ML Engineer",[])
    engine.next_question()
    before=engine.total_asked
    engine.submit_answer("not-a-real-question-id","anything")
    assert engine.total_asked==before


def test_overall_mastery_within_bounds():
    engine,order=run_session("ML Engineer",seed=3)
    m=engine.overall_mastery()
    assert 0<=m<=1
