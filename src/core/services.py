"""
Service layer for The 98% Platform.
Handles business logic for skill translation and career matching.
"""
from typing import List, Dict

from src.core.models import AthleteProfile, Job, Employer
from src.core.data import (
    SKILL_DB,
    UNIVERSAL_SKILLS,
    ROLE_SKILL_MAPPINGS,
    SPORT_SKILL_MAPPINGS,
    COMPOSITE_SKILL_MAPPINGS,
    JOBS_DB,
    SAMPLE_EMPLOYERS
)


def _resolve_skills(mapping: Dict[str, tuple[str, str]], source: str) -> Dict[str, str]:
    """Helper to extract skills from mappings based on substring containment."""
    return {
        skill_name: SKILL_DB[db_key]
        for keyword, (skill_name, db_key) in mapping.items()
        if keyword in source
    }


def _resolve_composite_skills(
    mapping: Dict[tuple[str, str], tuple[str, str]],
    profile: AthleteProfile
) -> Dict[str, str]:
    """Helper to extract skills from composite mappings (Sport + Role)."""
    return {
        skill_name: SKILL_DB[db_key]
        for (sport_kw, role_kw), (skill_name, db_key) in mapping.items()
        if sport_kw in profile.sport and role_kw in profile.role
    }


def translate_skills(profile: AthleteProfile) -> Dict[str, str]:
    """
    Translates raw athletic experiences into resume-ready bullet points.

    Args:
        profile: The athlete's profile (DTO).

    Returns:
        Dictionary mapping the corporate skill name to the resume translation.
    """
    return {
        **{k: SKILL_DB[v] for k, v in UNIVERSAL_SKILLS.items()},
        **_resolve_skills(SPORT_SKILL_MAPPINGS, profile.sport),
        **_resolve_skills(ROLE_SKILL_MAPPINGS, profile.role),
        **_resolve_composite_skills(COMPOSITE_SKILL_MAPPINGS, profile),
    }


def match_careers(grit_score: int, teamwork_score: int) -> List[Job]:
    """
    Suggests careers based on soft-skill scoring.

    Args:
        grit_score: Int 1-10
        teamwork_score: Int 1-10

    Returns:
        List of Job DTOs.
    """
    return [
        job for job in JOBS_DB
        if grit_score >= job.min_grit and teamwork_score >= job.min_teamwork
    ]


def match_employers(profile: AthleteProfile) -> List[Employer]:
    """
    Finds employers whose required skills match the athlete's translated skills.

    Args:
        profile: The athlete's profile (DTO).

    Returns:
        List of Employer DTOs where all required skills are present in the
        athlete's skill set.
    """
    athlete_skills = translate_skills(profile)
    skill_names = set(athlete_skills.keys())

    return [
        employer for employer in SAMPLE_EMPLOYERS
        if set(employer.required_skills).issubset(skill_names)
    ]


def match_opportunities(
    profile: AthleteProfile,
    grit_score: int,
    teamwork_score: int
) -> List[Job]:
    """
    Finds jobs that match both hard skills (resume bullets) and soft skills (grit/teamwork).

    Args:
        profile: The athlete's profile (DTO).
        grit_score: Int 1-10.
        teamwork_score: Int 1-10.

    Returns:
        List of Job DTOs where:
        1. job.min_grit <= grit_score
        2. job.min_teamwork <= teamwork_score
        3. job.required_skills is a subset of the athlete's translated skills
    """
    athlete_skills = translate_skills(profile)
    skill_names = set(athlete_skills.keys())

    return [
        job for job in JOBS_DB
        if grit_score >= job.min_grit
        and teamwork_score >= job.min_teamwork
        and set(job.required_skills).issubset(skill_names)
    ]
