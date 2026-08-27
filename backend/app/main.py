"""
Personalized Learning Path Recommender — backend API.

Owned by Mads (conversational interface + profiling engine).
The /profile endpoints are the contract surface every teammate consumes.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from . import extraction, storage
from .models import Goals, LearnerProfile, Preferences

load_dotenv()  # read backend/.env so XAI_API_KEY is available

app = FastAPI(title="Learning Path Recommender API", version="0.2.0")

# Let the Next.js frontend (localhost:3000) call this API during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures"


@app.on_event("startup")
def load_fixtures() -> None:
    """Load sample profiles on boot so teammates have data to build against."""
    for path in FIXTURES_DIR.glob("*.json"):
        data = json.loads(path.read_text())
        storage.save_profile(LearnerProfile(**data))


@app.get("/")
def health() -> dict:
    return {"status": "ok", "service": "learning-path-recommender"}


# ---------------------------------------------------------------------------
# Profile endpoints  (Mads)  — the contract surface everyone else reads
# ---------------------------------------------------------------------------

@app.post("/api/profile", response_model=LearnerProfile)
def upsert_profile(profile: LearnerProfile) -> LearnerProfile:
    """Create or update a learner profile."""
    now = datetime.now(timezone.utc)
    if profile.created_at is None:
        profile.created_at = now
    profile.updated_at = now
    return storage.save_profile(profile)


@app.get("/api/profile/{user_id}", response_model=LearnerProfile)
def read_profile(user_id: str) -> LearnerProfile:
    """Fetch a learner profile. This is the endpoint teammates consume."""
    profile = storage.get_profile(user_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


# ---------------------------------------------------------------------------
# Chat endpoint  (Mads)  — turns natural language into a LearnerProfile
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    user_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str
    profile: LearnerProfile


def _build_reply(profile: LearnerProfile) -> str:
    """A short, human summary of what we captured. No extra LLM call needed."""
    bits: list[str] = []
    if profile.goals.target_role:
        bits.append(f"aiming to become a {profile.goals.target_role}")
    bits.append(f"at a {profile.experience_level.value} level")
    if profile.current_skills:
        skills = ", ".join(s.skill for s in profile.current_skills)
        bits.append(f"with some {skills}")
    summary = "; ".join(bits)
    return f"Got it — I've noted you're {summary}. Tell me more, or ask for your learning path."


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    """Extract/update the learner's profile from a natural-language message."""
    existing = storage.get_profile(req.user_id)
    existing_dict = existing.model_dump(mode="json") if existing else None

    try:
        result = extraction.extract(req.message, existing_dict)
    except RuntimeError as e:  # e.g. missing API key
        raise HTTPException(status_code=503, detail=str(e))

    now = datetime.now(timezone.utc)
    profile = LearnerProfile(
        user_id=req.user_id,
        created_at=existing.created_at if existing else now,
        updated_at=now,
        interests=result.interests,
        experience_level=result.experience_level or "beginner",
        goals=Goals(
            raw_text=req.message,
            parsed=result.parsed_goals,
            target_role=result.target_role,
        ),
        completed_courses=result.completed_courses,
        current_skills=result.current_skills,
        preferences=Preferences(
            time_commitment=result.time_commitment,
            preferred_formats=result.preferred_formats,
        ),
    )
    storage.save_profile(profile)
    return ChatResponse(reply=_build_reply(profile), profile=profile)
