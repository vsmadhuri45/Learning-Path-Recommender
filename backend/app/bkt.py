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
