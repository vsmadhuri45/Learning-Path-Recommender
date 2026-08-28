from app.bkt import update,uncertainty_label,initial_prior,MASTERY_THRESHOLD,MIN_EVIDENCE
from app.graph import graph


class FakeSkill:
    def __init__(self,skill,proficiency):
        self.skill=skill
        self.proficiency=proficiency


def test_correct_answer_increases_mastery():
    p=0.5
    assert update(p,True)>p


def test_incorrect_answer_decreases_mastery():
    p=0.5
    assert update(p,False)<p


def test_mastery_stays_in_bounds():
    p=0.5
    for _ in range(50):
        p=update(p,True)
    assert p<=1.0
    p=0.5
    for _ in range(50):
        p=update(p,False)
    assert p>=0.0


def test_uncertainty_label_thresholds():
    assert uncertainty_label(0)=="high"
    assert uncertainty_label(1)=="medium"
    assert uncertainty_label(2)=="medium"
    assert uncertainty_label(3)=="low"
    assert uncertainty_label(10)=="low"


def test_initial_prior_no_match_returns_baseline():
    concept=graph.get("neural_networks")
    prior=initial_prior(concept,[FakeSkill("cooking",5)])
    assert prior==0.5


def test_initial_prior_picks_best_match_not_first():
    sql_joins=graph.get("sql_joins")
    skills=[FakeSkill("sql",2),FakeSkill("sql joins",5)]
    prior=initial_prior(sql_joins,skills)
    assert prior==min(0.3+0.14*5,0.95)


def test_initial_prior_order_independent():
    sql_joins=graph.get("sql_joins")
    a=initial_prior(sql_joins,[FakeSkill("sql",2),FakeSkill("sql joins",5)])
    b=initial_prior(sql_joins,[FakeSkill("sql joins",5),FakeSkill("sql",2)])
    assert a==b
