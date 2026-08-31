import re
from . import bkt
from .graph import graph
from .questions import questions_for


def grade_text_answer(question_text: str, user_answer: str, question_type: str, rubric: str = "") -> dict:
    """
    Pure Python evaluation engine for fast, local quiz grading of two-liners and paragraphs.
    """
    user_clean = user_answer.lower().strip()
    
    if not user_clean or len(user_clean) < 5:
        return {
            "correct": False,
            "score": 0.0,
            "feedback": "Answer was too short or empty."
        }
    
    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", 
        "with", "by", "is", "of", "it", "as", "be", "that", "this", "are", "from"
    }
    
    rubric_words = {w for w in re.findall(r'\b\w+\b', rubric.lower()) if w not in stop_words}
    user_words = {w for w in re.findall(r'\b\w+\b', user_clean) if w not in stop_words}
    
    if not rubric_words:
        word_count = len(user_clean.split())
        score = 0.8 if word_count >= 10 else 0.4
        return {
            "correct": score >= 0.5,
            "score": score,
            "feedback": "Answer submitted and verified via length analysis."
        }
    
    matched_words = rubric_words.intersection(user_words)
    coverage = len(matched_words) / len(rubric_words)
    word_count = len(user_clean.split())
    
    if question_type == "two_liner":
        length_factor = 1.0 if (8 <= word_count <= 50) else 0.7
        score = min(1.0, (coverage * 0.75 + (0.25 if length_factor == 1.0 else 0.1)))
    else:  # paragraph
        length_factor = 1.0 if word_count >= 20 else 0.5
        score = min(1.0, (coverage * 0.65 + (0.35 if length_factor == 1.0 else 0.15)))
    
    correct = score >= 0.5
    
    if correct:
        feedback = f"Good explanation! Covered key concepts successfully ({len(matched_words)}/{len(rubric_words)} expected terms found)."
    else:
        feedback = f"Partial answer. Try mentioning core terms related to: {', '.join(list(rubric_words)[:3])}."

    return {
        "correct": correct,
        "score": round(score, 2),
        "feedback": feedback
    }


class ConceptState:
    def __init__(self, concept, mastery):
        self.concept = concept
        self.mastery = mastery
        self.evidence_count = 0
        self.asked_question_ids = set()


class AssessmentEngine:
    def __init__(self, student_id, role, current_skills, max_questions=14):
        if role not in graph.roles:
            raise ValueError(f"unknown role '{role}', expected one of {graph.roles}")
        self.student_id = student_id
        self.role = role
        self.max_questions = max_questions
        self.total_asked = 0
        concepts = graph.concepts_for_role(role)
        self.states = {c.concept_id: ConceptState(c, bkt.initial_prior(c, current_skills)) for c in concepts}
        self.current_question = None
        self.current_concept_id = None

    def _get_desired_type(self):
        """Determine what type of question we want based on how many have been asked."""
        if self.total_asked < 10:
            return "mcq"
        elif self.total_asked < 13:
            return "two_liner"
        else:
            return "paragraph"

    def _prereqs_started(self, concept):
        if not concept.prerequisites:
            return True
        return all(self.states[p].evidence_count >= 1 for p in concept.prerequisites)

    def _has_unused_question(self, state, desired_type=None):
        pool = questions_for(state.concept.concept_id)
        for q in pool:
            if q["id"] not in state.asked_question_ids:
                if desired_type is None or q.get("type", "mcq") == desired_type:
                    return True
        return False

    def _eligible_states(self, desired_type=None):
        result = []
        for state in self.states.values():
            if state.evidence_count >= bkt.MAX_EVIDENCE_CAP:
                continue
            if not self._prereqs_started(state.concept):
                continue
            if not self._has_unused_question(state, desired_type):
                continue
            result.append(state)
        return result

    def _priority(self, state):
        uncertainty_weight = 1 - (state.evidence_count / bkt.MAX_EVIDENCE_CAP)
        return state.concept.role_importance * uncertainty_weight

    def _pick_next_state(self):
        desired_type = self._get_desired_type()
        candidates = self._eligible_states(desired_type)
        if not candidates:
            candidates = self._eligible_states(None)
        if not candidates:
            return None
        candidates.sort(key=lambda s: (-self._priority(s), s.concept.difficulty, s.concept.concept_id))
        return candidates[0]

    def is_complete(self):
        if self.total_asked >= self.max_questions:
            return True
        for state in self.states.values():
            mastered = state.mastery >= bkt.MASTERY_THRESHOLD and state.evidence_count >= bkt.MIN_EVIDENCE
            exhausted = state.evidence_count >= bkt.MAX_EVIDENCE_CAP or not self._has_unused_question(state)
            if not (mastered or exhausted):
                return False
        return True

    def next_question(self):
        if self.is_complete():
            self.current_question = None
            self.current_concept_id = None
            return None
        state = self._pick_next_state()
        if state is None:
            self.current_question = None
            self.current_concept_id = None
            return None
        
        desired_type = self._get_desired_type()
        pool = questions_for(state.concept.concept_id)
        available = [q for q in pool if q["id"] not in state.asked_question_ids]
        type_matches = [q for q in available if q.get("type", "mcq") == desired_type]
        
        question = type_matches[0] if type_matches else available[0]
        state.asked_question_ids.add(question["id"])
        self.current_question = question
        self.current_concept_id = state.concept.concept_id
        return question

    def submit_answer(self, question_id, answer):
        if self.current_question is None or self.current_question["id"] != question_id:
            return None
        
        state = self.states[self.current_concept_id]
        q_type = self.current_question.get("type", "mcq")

        if q_type == "mcq":
            correct = (answer.strip() == self.current_question.get("answer", ""))
            score = 1.0 if correct else 0.0
            feedback = "Correct!" if correct else "Incorrect answer."
        else:
            # Evaluate short and paragraph text answers locally using pure Python
            eval_res = grade_text_answer(
                question_text=self.current_question["text"],
                user_answer=answer,
                question_type=q_type,
                rubric=self.current_question.get("rubric", "")
            )
            correct = eval_res["correct"]
            score = eval_res["score"]
            feedback = eval_res["feedback"]

        # Update BKT mastery
        state.mastery = bkt.update(state.mastery, correct)
        state.evidence_count += 1
        self.total_asked += 1
        
        self.current_question = None
        self.current_concept_id = None
        
        return {
            "correct": correct,
            "score": score,
            "feedback": feedback,
            "current_mastery": round(self.overall_mastery(), 3)
        }

    def overall_mastery(self):
        weighted = sum(s.mastery * s.concept.role_importance for s in self.states.values())
        total_weight = sum(s.concept.role_importance for s in self.states.values())
        return weighted / total_weight if total_weight else 0

    def knowledge_profile(self):
        concepts = []
        for state in self.states.values():
            concepts.append({
                "concept_id": state.concept.concept_id,
                "skill_id": state.concept.skill_id,
                "mastery": round(state.mastery, 3),
                "uncertainty": bkt.uncertainty_label(state.evidence_count),
                "evidence_count": state.evidence_count,
                "role_importance": state.concept.role_importance
            })
        return {
            "student_id": self.student_id,
            "target_role": self.role,
            "overall_mastery": round(self.overall_mastery(), 3),
            "concepts": concepts
        }