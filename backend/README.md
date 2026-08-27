# Backend — Learning Path Recommender

FastAPI backend. Owns the conversational interface + learner profiling engine.
The `/api/profile` endpoints are the contract surface every teammate consumes
(see `docs/CONTRACT.md`).

## Run it (in VS Code terminal)

```bash
cd backend
python -m venv venv

# activate the virtual environment:
#   macOS / Linux:
source venv/bin/activate
#   Windows (PowerShell):
venv\Scripts\Activate.ps1

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open **http://localhost:8000/docs** — FastAPI's auto-generated interactive
docs. You can call every endpoint from that page without writing any client code.

## What's here

| Path | What it is |
|---|---|
| `app/models.py` | `LearnerProfile` and friends — the data contract in code. |
| `app/storage.py` | In-memory store. Swap for Supabase later; nothing else changes. |
| `app/main.py` | The API: profile endpoints + a stubbed `/api/chat`. |
| `fixtures/` | Sample profiles, auto-loaded on startup so teammates have data. |

## Endpoints

- `GET  /` — health check
- `POST /api/profile` — create/update a profile
- `GET  /api/profile/{user_id}` — fetch a profile *(this is what teammates call)*
- `POST /api/chat` — **stub**; wire an LLM here next to build profiles from chat

Two profiles load on startup:
`550e8400-e29b-41d4-a716-446655440000` (beginner) and
`7c9e6679-7425-40de-944b-e07fc1f90ae7` (advanced).

## Next steps for Mads

1. Replace the `/api/chat` stub with an LLM call that extracts a `LearnerProfile`
   from the learner's message (structured output / function calling).
2. Later: replace `storage.py` internals with Supabase so profiles persist and
   teammates share one database.
