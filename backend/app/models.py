"""
LearnerProfile models — the data contract (see docs/CONTRACT.md).

This is the single source of truth the profiling engine produces and every
other feature consumes. Keep this in sync with CONTRACT.md section 2.
"""

from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field


class ExperienceLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class Goals(BaseModel):
    raw_text: str
    parsed: list[str] = []
    target_role: str | None = None


class CompletedCourse(BaseModel):
    course_id: str
    title: str
    provider: str | None = None
    completed_at: date | None = None


class Skill(BaseModel):
    skill: str
    proficiency: int = Field(ge=1, le=5)  # 1 = aware ... 5 = expert


class Preferences(BaseModel):
    time_commitment: str | None = None
    preferred_formats: list[str] = []


class LearnerProfile(BaseModel):
    user_id: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    interests: list[str] = []
    experience_level: ExperienceLevel
    goals: Goals
    completed_courses: list[CompletedCourse] = []
    current_skills: list[Skill] = []
    preferences: Preferences = Preferences()
