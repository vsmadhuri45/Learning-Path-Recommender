"""
Chat -> profile extraction using the xAI (Grok) API.

Grok is OpenAI-compatible, so we use the `openai` SDK pointed at xAI's base URL.
The learner's message (plus whatever we already know) goes in; a structured
ExtractionResult comes out, which the chat endpoint turns into a LearnerProfile.
"""

import json
import os

from openai import OpenAI
from pydantic import BaseModel

from .models import CompletedCourse, ExperienceLevel, Skill

# --- config -----------------------------------------------------------------
# Model names change often at xAI. Change this one line to switch models
# (e.g. to an OpenAI model — the rest of the code stays the same).
GROK_MODEL = "grok-4.5"
XAI_BASE_URL = "https://api.x.ai/v1"

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    """Create the client lazily so the app still boots without an API key set."""
    global _client
    if _client is None:
        api_key = os.environ.get("XAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "XAI_API_KEY is not set. Add it to backend/.env (see .env.example)."
            )
        _client = OpenAI(api_key=api_key, base_url=XAI_BASE_URL)
    return _client


# --- what the LLM returns ---------------------------------------------------
# A flat shape is easiest for the model to fill reliably. The chat endpoint
# reshapes this into a full LearnerProfile.
class ExtractionResult(BaseModel):
    interests: list[str] = []
    experience_level: ExperienceLevel | None = None
    parsed_goals: list[str] = []
    target_role: str | None = None
    completed_courses: list[CompletedCourse] = []
    current_skills: list[Skill] = []
    time_commitment: str | None = None
    preferred_formats: list[str] = []


SYSTEM_PROMPT = """You extract a learner's profile from what they tell you.

Return ONLY a JSON object with these keys (omit nothing; use empty lists / null
when unknown):
- interests: string[]            (topics they care about)
- experience_level: one of "beginner", "intermediate", "advanced", or null
- parsed_goals: string[]         (concrete goals, e.g. "learn SQL")
- target_role: string or null    (e.g. "Data Analyst")
- completed_courses: array of {course_id, title, provider, completed_at}
    (only if the learner names real courses; leave [] otherwise)
- current_skills: array of {skill, proficiency} where proficiency is an
    integer 1-5 (1=aware, 3=competent, 5=expert). Estimate conservatively.
- time_commitment: string or null (e.g. "5 hours/week")
- preferred_formats: string[]    (e.g. "video", "reading", "project")

Rules:
- Only include facts the learner actually stated or that are in the existing
  profile. NEVER invent skills, courses, or goals.
- If an existing profile is provided, MERGE: keep known facts and add new ones.
- Output must be valid JSON and nothing else. No markdown, no commentary."""


def extract(message: str, existing: dict | None = None) -> ExtractionResult:
    """Send the learner's message to Grok and return a structured extraction."""
    user_content = f"Learner message:\n{message}"
    if existing:
        user_content += f"\n\nExisting profile (merge into this):\n{json.dumps(existing)}"

    resp = _get_client().chat.completions.create(
        model=GROK_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    raw = resp.choices[0].message.content or "{}"
    return ExtractionResult.model_validate_json(raw)
