"""
Service layer for The 98% Platform.
Handles business logic for skill translation and career matching.
"""
from typing import List, Dict

from src.core.models import AthleteProfile, Job
from src.core.data import (
    SKILL_DB,
    UNIVERSAL_SKILLS,
    ROLE_SKILL_MAPPINGS,
    BASE_JOBS,
    GRIT_JOBS,
    TEAMWORK_JOBS,
    HIGH_SCORE_THRESHOLD
)


def translate_skills(profile: AthleteProfile) -> Dict[str, str]:
    """
    Translates raw athletic experiences into resume-ready bullet points.

    Args:
        profile: The athlete's profile (DTO).

    Returns:
        Dictionary mapping the corporate skill name to the resume translation.
    """
    universal_skills = {
        corpo: SKILL_DB[db_key]
        for corpo, db_key in UNIVERSAL_SKILLS.items()
    }

    role_skills = {
        skill: SKILL_DB[db_key]
        for keyword, (skill, db_key) in ROLE_SKILL_MAPPINGS.items()
        if keyword in profile.role
    }

    return {**universal_skills, **role_skills}


def match_careers(grit_score: int, teamwork_score: int) -> List[Job]:
    """
    Suggests careers based on soft-skill scoring.

    Args:
        grit_score: Int 1-10
        teamwork_score: Int 1-10

    Returns:
        List of Job DTOs.
    """
    job_titles = [
        *BASE_JOBS,
        *(GRIT_JOBS if grit_score > HIGH_SCORE_THRESHOLD else []),
        *(TEAMWORK_JOBS if teamwork_score > HIGH_SCORE_THRESHOLD else [])
    ]

    return [Job(title=title) for title in job_titles]
