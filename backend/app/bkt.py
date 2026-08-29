PGUESS=0.25
PSLIP=0.10
PTRANSIT=0.05
MASTERY_THRESHOLD=0.90
MIN_EVIDENCE=3
MAX_EVIDENCE_CAP=4


def update(p,correct,pguess=PGUESS,pslip=PSLIP,ptransit=PTRANSIT):
    if correct:
        pobs=(p*(1-pslip))/((p*(1-pslip))+((1-p)*pguess))
    else:
        pobs=(p*pslip)/((p*pslip)+((1-p)*(1-pguess)))
    return pobs+(1-pobs)*ptransit


def uncertainty_label(evidence_count):
    if evidence_count>=MIN_EVIDENCE:
        return "low"
    if evidence_count>=1:
        return "medium"
    return "high"


def initial_prior(concept,current_skills):
    best=0.5
    matched=False
    for skill in current_skills:
        name=skill.skill.lower()
        if name in concept.name.lower() or name in concept.skill_id.lower():
            prior=min(0.3+0.14*skill.proficiency,0.95)
            if not matched or prior>best:
                best=prior
                matched=True
    return best
class BKTModel:
    def __init__(self):
        # Updated standard BKT parameters
        self.p_init = 0.15     # P(L0): Probability of prior knowledge
        self.p_transit = 0.10  # P(T): Probability of learning a new concept per attempt
        self.p_guess = 0.20    # P(G): Probability of guessing correctly without knowing
        self.p_slip = 0.10     # P(S): Probability of making a mistake despite knowing
        
        # Strict threshold
        self.mastery_threshold = 0.95 
        
        # In-memory dictionary mimicking database storage 
        # Format: { user_id: { concept_id: mastery_probability } }
        self.user_mastery = {}

    def get_mastery(self, user_id, concept_id):
        """Fetch current mastery probability, default to p_init if unseen."""
        return self.user_mastery.get(user_id, {}).get(concept_id, self.p_init)

    def train_mastery(self, user_id, concept_id, is_correct: bool):
        """
        Uses Bayes' Theorem to update the student's mastery probability 
        based on whether they got a question right or wrong.
        """
        p_prev = self.get_mastery(user_id, concept_id)
        
        if is_correct:
            # Probability of having mastered it given a correct observation
            numerator = p_prev * (1 - self.p_slip)
            denominator = numerator + (1 - p_prev) * self.p_guess
        else:
            # Probability of having mastered it given an incorrect observation
            numerator = p_prev * self.p_slip
            denominator = numerator + (1 - p_prev) * (1 - self.p_guess)
            
        p_obs = numerator / denominator
        
        # Incorporate the probability of learning during the transition (P_transit)
        p_next = p_obs + (1 - p_obs) * self.p_transit
        
        # Save updated state
        if user_id not in self.user_mastery:
            self.user_mastery[user_id] = {}
            
        self.user_mastery[user_id][concept_id] = p_next
        return p_next