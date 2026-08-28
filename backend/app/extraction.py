import json
import os
import re

from openai import OpenAI
from pydantic import BaseModel

from .graph import graph
from .models import CompletedCourse,ExperienceLevel,Skill

GROQ_MODEL="llama-3.3-70b-versatile"
GROQ_BASE_URL="https://api.groq.com/openai/v1"

_client:OpenAI|None=None


def _get_client()->OpenAI:
    global _client
    if _client is None:
        api_key=os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to backend/.env (see .env.example)."
            )
        _client=OpenAI(api_key=api_key,base_url=GROQ_BASE_URL)
    return _client


class ExtractionResult(BaseModel):
    interests:list[str]=[]
    experience_level:ExperienceLevel|None=None
    parsed_goals:list[str]=[]
    target_role:str|None=None
    completed_courses:list[CompletedCourse]=[]
    current_skills:list[Skill]=[]
    time_commitment:str|None=None
    preferred_formats:list[str]=[]


def _system_prompt()->str:
    roles="\", \"".join(graph.roles)
    return f"""You extract a learner's profile from what they tell you.

Return ONLY a JSON object with these keys (omit nothing; use empty lists / null
when unknown):
- interests: string[]            (topics they care about)
- experience_level: one of "beginner", "intermediate", "advanced", or null
- parsed_goals: string[]         (concrete goals, e.g. "learn SQL")
- target_role: one of "{roles}", or null if the learner's goal does not
    clearly match either of these two supported roles. Do not invent other
    role names — only these two are supported right now.
- completed_courses: array of {{course_id, title, provider, completed_at}}
    (only if the learner names real courses; leave [] otherwise)
- current_skills: array of {{skill, proficiency}} where proficiency is an
    integer 1-5 (1=aware, 3=competent, 5=expert). Estimate conservatively.
- time_commitment: string or null (e.g. "5 hours/week")
- preferred_formats: string[]    (e.g. "video", "reading", "project")

Rules:
- Only include facts the learner actually stated or that are in the existing
  profile. NEVER invent skills, courses, or goals.
- If an existing profile is provided, MERGE: keep known facts and add new ones.
- Output must be valid JSON and nothing else. No markdown, no commentary."""


def _normalize_role(raw:str|None)->str|None:
    if raw is None:
        return None
    if raw in graph.roles:
        return raw
    text=raw.lower()
    if "data analyst" in text or re.search(r"\b(da|analyst)\b",text):
        return "Data Analyst"
    if "machine learning" in text or "ml engineer" in text or re.search(r"\b(mle|ml)\b",text):
        return "ML Engineer"
    return None


def extract(message:str,existing:dict|None=None)->ExtractionResult:
    user_content=f"Learner message:\n{message}"
    if existing:
        user_content+=f"\n\nExisting profile (merge into this):\n{json.dumps(existing)}"

    resp=_get_client().chat.completions.create(
    model=GROQ_MODEL,
    messages=[
    {"role":"system","content":_system_prompt()},
    {"role":"user","content":user_content}
    ],
    response_format={"type":"json_object"},
    temperature=0
    )
    raw=resp.choices[0].message.content or "{}"
    result=ExtractionResult.model_validate_json(raw)
    result.target_role=_normalize_role(result.target_role)
    return result