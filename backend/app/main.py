import json
import random
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
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


# ---------------------------------------------------------------------------
# Quiz endpoints (BKT via WebSockets)
# ---------------------------------------------------------------------------

# BKT Constants
P_GUESS = 0.25
P_SLIP = 0.10
P_TRANSIT = 0.05
MASTERY_THRESHOLD = 0.95

# Mock Database: Focus on Data Science & DBMS
QUESTION_BANK = [
    {"id": "q1", "topic": "sql_basics", "text": "Which clause is used to filter the results of a GROUP BY operation?", "options": ["WHERE", "HAVING", "ORDER BY", "FILTER"], "answer": "HAVING"},
    {"id": "q2", "topic": "sql_basics", "text": "What does ACID stand for in database management?", "options": ["Atomicity, Consistency, Isolation, Durability", "Accuracy, Completeness, Integrity, Data", "Automated, Concurrent, Indexed, Distributed", "Array, Character, Integer, Double"], "answer": "Atomicity, Consistency, Isolation, Durability"},
    {"id": "q3", "topic": "sql_basics", "text": "Which JOIN returns all rows from the right table, and the matched rows from the left table?", "options": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN"], "answer": "RIGHT JOIN"},
    {"id": "q4", "topic": "numpy_basics", "text": "Which NumPy function is used to create an array of evenly spaced values?", "options": ["np.arange()", "np.linspace()", "Both A and B", "np.create()"], "answer": "Both A and B"}
]

class QuizSessionManager:
    def __init__(self):
        self.active_sessions = {}

    async def connect(self, websocket: WebSocket, session_id: str, initial_knowledge: float):
        await websocket.accept()
        self.active_sessions[session_id] = {
            "ws": websocket,
            "p_mastery": initial_knowledge,
            "asked_questions": []
        }

    def get_next_question(self, session_id: str):
        asked = self.active_sessions[session_id]["asked_questions"]
        available = [q for q in QUESTION_BANK if q["id"] not in asked]
        if not available:
            return None
        question = random.choice(available)
        self.active_sessions[session_id]["asked_questions"].append(question["id"])
        return question

    def update_bkt(self, session_id: str, is_correct: bool) -> float:
        p_l = self.active_sessions[session_id]["p_mastery"]
        
        # 1. Update probability based on observation
        if is_correct:
            p_obs = (p_l * (1 - P_SLIP)) / ((p_l * (1 - P_SLIP)) + ((1 - p_l) * P_GUESS))
        else:
            p_obs = (p_l * P_SLIP) / ((p_l * P_SLIP) + ((1 - p_l) * (1 - P_GUESS)))
            
        # 2. Apply transit (learning) probability
        p_new = p_obs + (1 - p_obs) * P_TRANSIT
        self.active_sessions[session_id]["p_mastery"] = p_new
        return p_new

manager = QuizSessionManager()

@app.websocket("/api/ws/quiz/{user_id}")
async def quiz_endpoint(websocket: WebSocket, user_id: str):
    # Retrieve profile to set the initial knowledge state dynamically
    profile = storage.get_profile(user_id)
    
    initial_p = 0.20 # Default to beginner
    if profile and hasattr(profile, 'experience_level'):
        level = getattr(profile.experience_level, 'value', str(profile.experience_level)).lower()
        if level == "intermediate":
            initial_p = 0.50
        elif level == "advanced":
            initial_p = 0.80

    await manager.connect(websocket, user_id, initial_p)
    
    try:
        # Serve the first question
        first_q = manager.get_next_question(user_id)
        if first_q:
            await websocket.send_json({"type": "question", "data": {"id": first_q["id"], "text": first_q["text"], "options": first_q["options"]}})
        
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            
            if payload["type"] == "answer":
                q_id = payload["question_id"]
                user_answer = payload["answer"]
                question = next((q for q in QUESTION_BANK if q["id"] == q_id), None)
                
                if question:
                    is_correct = (question["answer"] == user_answer)
                    new_mastery = manager.update_bkt(user_id, is_correct)
                    
                    if new_mastery >= MASTERY_THRESHOLD:
                        await websocket.send_json({"type": "complete", "message": "Mastery Achieved!", "mastery_level": round(new_mastery, 2)})
                        break
                    else:
                        next_q = manager.get_next_question(user_id)
                        if next_q:
                            await websocket.send_json({"type": "question", "data": {"id": next_q["id"], "text": next_q["text"], "options": next_q["options"]}})
                        else:
                            await websocket.send_json({"type": "complete", "message": "Question pool exhausted.", "mastery_level": round(new_mastery, 2)})
                            break
                        
    except WebSocketDisconnect:
        # Clean up the session if the user drops off
        if user_id in manager.active_sessions:
            del manager.active_sessions[user_id]
