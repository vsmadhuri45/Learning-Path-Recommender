# Data Contract — Personalized Learning Path Recommender

**Status:** Draft v0.1 · **Owner of this doc:** Mads · **Last updated:** 2026-08-27

This is the single source of truth the whole team builds against. The `LearnerProfile`
object is produced by the conversational interface + profiling engine and **consumed by
every other feature**. If you need a field that isn't here, don't add it silently — propose
the change in the team channel and bump the version so nobody builds against a moving target.

---

## 1. Rules of the road

- `LearnerProfile` is the contract. The profiling engine writes it; everyone else reads it.
- **Derived data is not stored in the profile.** Skill gaps, recommendations, and the
  learning path are *computed* from the profile by their respective owners — they are not
  fields on the profile.
- Any change to the schema requires a quick team sign-off + a version bump (v0.1 → v0.2).
- Keep the three language versions below in sync. The JSON is the source of truth; Pydantic
  and TypeScript must match it.

---

## 2. The `LearnerProfile` object

### 2.1 Canonical shape (JSON)

```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2026-08-27T10:00:00Z",
  "updated_at": "2026-08-27T10:00:00Z",

  "interests": ["data analysis", "machine learning", "python"],

  "experience_level": "beginner",

  "goals": {
    "raw_text": "I want to become a data analyst. I know a little Python and Excel.",
    "parsed": ["become a data analyst", "learn SQL", "learn data visualization"],
    "target_role": "Data Analyst"
  },

  "completed_courses": [
    {
      "course_id": "py-101",
      "title": "Intro to Python",
      "provider": "Coursera",
      "completed_at": "2026-06-01"
    }
  ],

  "current_skills": [
    { "skill": "python", "proficiency": 2 },
    { "skill": "excel", "proficiency": 3 }
  ],

  "preferences": {
    "time_commitment": "5 hours/week",
    "preferred_formats": ["video", "project"]
  }
}
```

### 2.2 Field reference

| Field | Type | Notes |
|---|---|---|
| `user_id` | UUID string | Primary key. Comes from Supabase auth. |
| `created_at` / `updated_at` | ISO 8601 timestamp | Set by the backend. |
| `interests` | string[] | Free-form topics the learner cares about. |
| `experience_level` | enum | One of `"beginner"`, `"intermediate"`, `"advanced"`. |
| `goals.raw_text` | string | Exactly what the learner typed. Never lose this. |
| `goals.parsed` | string[] | LLM-extracted discrete goals. |
| `goals.target_role` | string \| null | Extracted role, if any (e.g. "Data Analyst"). |
| `completed_courses` | object[] | `course_id`, `title` required; `provider`, `completed_at` optional. |
| `current_skills` | object[] | `skill` (string) + `proficiency` (int **1–5**, see legend). |
| `preferences.time_commitment` | string \| null | Free text, e.g. "5 hours/week". |
| `preferences.preferred_formats` | string[] | e.g. `"video"`, `"reading"`, `"project"`. |

**Proficiency legend (1–5):** 1 = none/aware · 2 = novice · 3 = competent · 4 = proficient · 5 = expert.
The recommendation engine diffs these against course requirements to find skill gaps.

### 2.3 Pydantic (backend — FastAPI)

```python
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
    proficiency: int = Field(ge=1, le=5)

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
```

### 2.4 TypeScript (frontend — Next.js)

```typescript
export type ExperienceLevel = "beginner" | "intermediate" | "advanced";

export interface LearnerProfile {
  user_id: string;
  created_at?: string;
  updated_at?: string;
  interests: string[];
  experience_level: ExperienceLevel;
  goals: {
    raw_text: string;
    parsed: string[];
    target_role: string | null;
  };
  completed_courses: {
    course_id: string;
    title: string;
    provider?: string;
    completed_at?: string;
  }[];
  current_skills: { skill: string; proficiency: number }[]; // 1–5
  preferences: {
    time_commitment?: string;
    preferred_formats?: string[];
  };
}
```

---

## 3. API endpoints (sketch)

Base URL: `/api`. All request/response bodies are JSON. These shapes can be refined by each
owner, but the **profile shape flowing between them must stay as defined in section 2**.

| Method | Endpoint | Purpose | Owner |
|---|---|---|---|
| POST | `/chat` | Conversational intake. Takes learner messages, returns assistant reply + updates profile. | Mads |
| POST | `/profile` | Create or update a `LearnerProfile`. | Mads |
| GET | `/profile/{user_id}` | Fetch the profile. **The endpoint everyone consumes.** | Mads |
| POST | `/recommendations` | In: `LearnerProfile`. Out: ranked courses/projects/resources + skill gaps. | Person B |
| POST | `/learning-path` | In: profile + recommendations. Out: ordered roadmap with prerequisites & milestones. | Person B |
| POST | `/explain` | In: a recommendation or a learner question. Out: natural-language explanation/answer. | Person C |
| GET | `/progress/{user_id}` | Dashboard data: progress, skills, milestones, next actions. | Person C |

**Example — `GET /profile/{user_id}`** returns the object in section 2.1 verbatim.

**Example — `POST /recommendations`**
```json
// request
{ "profile": { /* LearnerProfile */ } }

// response
{
  "skill_gaps": ["sql", "data visualization"],
  "recommendations": [
    { "course_id": "sql-201", "title": "SQL for Analysts", "type": "course", "reason_key": "gap:sql" }
  ]
}
```

---

## 4. Feature ownership

Six required features, split across three people. Adjust names/split with the team.

| # | Feature | Owner | Depends on |
|---|---|---|---|
| 1 | Conversational interface (natural-language goals) | **Mads** | LLM extraction → profile |
| 2 | Learner profiling engine | **Mads** | — (produces the profile) |
| 3 | Recommendation engine (courses, projects, resources) | **Person B** | `GET /profile` |
| 4 | Learning path generator (prerequisites + milestones) | **Person B** | recommendations |
| 5 | AI assistant (explains recommendations, answers queries) | **Person C** | profile + path |
| 6 | Progress dashboard | **Person C** | profile + path + progress |

**Critical path:** Features 3–6 all wait on features 1–2. So Mads ships a working
`GET /profile` endpoint (even returning hardcoded sample data) *first* — that unblocks
everyone else immediately.

---

## 5. Sample data for unblocking teammates

Until the real intake flow is live, teammates build against these fixtures. Mads maintains
them so they always match the current schema version.

- `sample_profile_beginner.json` — the object in section 2.1.
- `sample_profile_advanced.json` — an advanced learner with several completed courses.

Drop these in `/backend/fixtures/` so anyone can load a valid profile without the UI.