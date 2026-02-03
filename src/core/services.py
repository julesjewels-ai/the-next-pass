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
    SPORT_SKILL_MAPPINGS,
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
    # Start with universal skills
    translations = {
        corpo_skill: SKILL_DB[db_key]
        for corpo_skill, db_key in UNIVERSAL_SKILLS.items()
    }

    # Apply sport and role specific mappings
    mappings = [
        (profile.sport, SPORT_SKILL_MAPPINGS),
        (profile.role, ROLE_SKILL_MAPPINGS),
    ]

    for source_text, mapping in mappings:
        for keyword, (skill_name, db_key) in mapping.items():
            if keyword in source_text:
                translations[skill_name] = SKILL_DB[db_key]

    return translations


def match_careers(grit_score: int, teamwork_score: int) -> List[Job]:
    """
    Suggests careers based on soft-skill scoring.

    Args:
        grit_score: Int 1-10
        teamwork_score: Int 1-10

    Returns:
        List of Job DTOs.
    """
    job_titles = list(BASE_JOBS)

    if grit_score > HIGH_SCORE_THRESHOLD:
        job_titles.extend(GRIT_JOBS)

    if teamwork_score > HIGH_SCORE_THRESHOLD:
        job_titles.extend(TEAMWORK_JOBS)

    return [Job(title=title) for title in job_titles]
