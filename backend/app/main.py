"""
Personalized Learning Path Recommender — backend API.

Owned by Mads (conversational interface + profiling engine).
The /profile endpoints are the contract surface every teammate consumes.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .models import LearnerProfile
from . import storage

app = FastAPI(title="Learning Path Recommender API", version="0.1.0")

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
# Chat endpoint  (Mads)  — STUB. Wire an LLM here next to extract the profile
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    user_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    """
    TODO: send `req.message` to an LLM with a prompt that extracts
    interests / experience_level / goals into a LearnerProfile, then
    save it via storage.save_profile(...). For now it just echoes.
    """
    return ChatResponse(
        reply=f"(stub) Got your message: {req.message!r}. LLM extraction goes here."
    )
