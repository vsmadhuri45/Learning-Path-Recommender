"""
Storage layer.

Starts as an in-memory dict so the team is unblocked with zero setup.
Swap the body of these functions for Supabase later — the rest of the app
never has to change, because it only calls these three functions.
"""

from .models import LearnerProfile

_profiles: dict[str, LearnerProfile] = {}


def save_profile(profile: LearnerProfile) -> LearnerProfile:
    _profiles[profile.user_id] = profile
    return profile


def get_profile(user_id: str) -> LearnerProfile | None:
    return _profiles.get(user_id)


def all_profiles() -> list[LearnerProfile]:
    return list(_profiles.values())
