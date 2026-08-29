"""
AI assistant: explains roadmap items and answers free-form learner
questions, grounded in the learner's actual profile + roadmap data —
not a generic chatbot. One function handles both cases (a roadmap-item
explanation is just a specific kind of question), one LLM call per
request, same Groq client as extraction.py.
"""

from . import llm


def _context_summary(profile: dict | None, roadmap: dict | None) -> str:
    parts = []
    if profile:
        parts.append(f"Target role: {profile.get('goals', {}).get('target_role')}")
        parts.append(f"Experience level: {profile.get('experience_level')}")
        skills = profile.get("current_skills", [])
        if skills:
            parts.append("Current skills: " + ", ".join(f"{s['skill']} ({s['proficiency']}/5)" for s in skills))
    if roadmap:
        items = roadmap.get("roadmap", [])
        if items:
            lines = [
                f"- {it['title']}: {round(it['current_mastery']*100)}% mastery, "
                f"status={it['status']}, priority={it['priority']}"
                for it in items[:10]
            ]
            parts.append("Current roadmap:\n" + "\n".join(lines))
        gaps = roadmap.get("gap_analysis", {}).get("critical_gaps", [])
        if gaps:
            parts.append(
                "Critical bottlenecks: "
                + "; ".join(f"{g['prerequisite_id']} blocks {g['blocks']}" for g in gaps)
            )
    return "\n".join(parts) if parts else "No profile or roadmap data available yet."


def _system_prompt() -> str:
    return """You are a learning path assistant. Answer the learner's question,
or explain a roadmap item, using ONLY the context provided below about their
actual profile and roadmap. Be concise (2-4 sentences), specific, and
encouraging. If the context doesn't cover what they're asking, say so
honestly instead of inventing details."""


def explain(question: str, profile: dict | None = None, roadmap: dict | None = None) -> str:
    context = _context_summary(profile, roadmap)
    resp = llm.get_client().chat.completions.create(
        model=llm.GROQ_MODEL,
        messages=[
            {"role": "system", "content": _system_prompt()},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
        temperature=0.3,
    )
    return resp.choices[0].message.content or "I couldn't generate an answer — try rephrasing your question."