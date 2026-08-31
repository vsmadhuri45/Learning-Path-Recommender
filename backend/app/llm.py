"""
Shared Groq client setup. Used by assistant.py for explanations/Q&A.
"""

import os
from openai import OpenAI

GROQ_MODEL = "openai/gpt-oss-120b"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

_client: OpenAI | None = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        # Check environment variable, with a direct fallback to your key for the demo
        api_key = os.environ.get("GROQ_API_KEY")
        
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Add it to backend/.env (see .env.example)."
            )
        _client = OpenAI(api_key=api_key, base_url=GROQ_BASE_URL)
    return _client