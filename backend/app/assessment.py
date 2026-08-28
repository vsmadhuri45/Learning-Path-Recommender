from . import bkt
from .graph import graph
from .questions import questions_for


class ConceptState:
    def __init__(self,concept,mastery):
        self.concept=concept
        self.mastery=mastery
        self.evidence_count=0
        self.asked_question_ids=set()


class AssessmentEngine:
    def __init__(self,student_id,role,current_skills,max_questions=20):
        if role not in graph.roles:
            raise ValueError(f"unknown role '{role}', expected one of {graph.roles}")
        self.student_id=student_id
        self.role=role
        self.max_questions=max_questions
        self.total_asked=0
        concepts=graph.concepts_for_role(role)
        self.states={c.concept_id:ConceptState(c,bkt.initial_prior(c,current_skills)) for c in concepts}
        self.current_question=None
        self.current_concept_id=None

    def _prereqs_started(self,concept):
        if not concept.prerequisites:
            return True
        return all(self.states[p].evidence_count>=1 for p in concept.prerequisites)

    def _has_unused_question(self,state):
        pool=questions_for(state.concept.concept_id)
        return any(q["id"] not in state.asked_question_ids for q in pool)

    def _eligible_states(self):
        result=[]
        for state in self.states.values():
            if state.evidence_count>=bkt.MAX_EVIDENCE_CAP:
                continue
            if not self._prereqs_started(state.concept):
                continue
            if not self._has_unused_question(state):
                continue
            result.append(state)
        return result

    def _priority(self,state):
        uncertainty_weight=1-(state.evidence_count/bkt.MAX_EVIDENCE_CAP)
        return state.concept.role_importance*uncertainty_weight

    def _pick_next_state(self):
        candidates=self._eligible_states()
        if not candidates:
            return None
        candidates.sort(key=lambda s:(-self._priority(s),s.concept.difficulty,s.concept.concept_id))
        return candidates[0]

    def is_complete(self):
        if self.total_asked>=self.max_questions:
            return True
        for state in self.states.values():
            mastered=state.mastery>=bkt.MASTERY_THRESHOLD and state.evidence_count>=bkt.MIN_EVIDENCE
            exhausted=state.evidence_count>=bkt.MAX_EVIDENCE_CAP or not self._has_unused_question(state)
            if not (mastered or exhausted):
                return False
        return True

    def next_question(self):
        if self.is_complete():
            self.current_question=None
            self.current_concept_id=None
            return None
        state=self._pick_next_state()
        if state is None:
            self.current_question=None
            self.current_concept_id=None
            return None
        pool=questions_for(state.concept.concept_id)
        question=next(q for q in pool if q["id"] not in state.asked_question_ids)
        state.asked_question_ids.add(question["id"])
        self.current_question=question
        self.current_concept_id=state.concept.concept_id
        return question

    def submit_answer(self,question_id,answer):
        if self.current_question is None or self.current_question["id"]!=question_id:
            return None
        state=self.states[self.current_concept_id]
        correct=answer==self.current_question["answer"]
        state.mastery=bkt.update(state.mastery,correct)
        state.evidence_count+=1
        self.total_asked+=1
        self.current_question=None
        self.current_concept_id=None
        return correct

    def overall_mastery(self):
        weighted=sum(s.mastery*s.concept.role_importance for s in self.states.values())
        total_weight=sum(s.concept.role_importance for s in self.states.values())
        return weighted/total_weight if total_weight else 0

    def knowledge_profile(self):
        concepts=[]
        for state in self.states.values():
            concepts.append({
                "concept_id":state.concept.concept_id,
                "skill_id":state.concept.skill_id,
                "mastery":round(state.mastery,3),
                "uncertainty":bkt.uncertainty_label(state.evidence_count),
                "evidence_count":state.evidence_count,
                "role_importance":state.concept.role_importance
            })
        return {
            "student_id":self.student_id,
            "target_role":self.role,
            "concepts":concepts
        }
