"""
Core business logic for The 98% Platform.

Handles the translation of athletic experiences into professional terminology
and matches athletes with suitable career paths.
"""

from dataclasses import dataclass
from typing import Dict, List

# Domain Constants
SKILL_LEADERSHIP = "Leadership"
SKILL_TIME_MANAGEMENT = "Time Management"
SKILL_STRATEGIC_ANALYSIS = "Strategic Analysis"

# Skill Keys
KEY_CAPTAIN = "Captain"
KEY_FILM_STUDY = "Film Study"
KEY_WORKOUTS = "5am Workouts"

SKILL_DB = {
    KEY_CAPTAIN: (
        "Demonstrated leadership by coordinating team activities and fostering a "
        "collaborative environment under high-pressure conditions."
    ),
    KEY_FILM_STUDY: (
        "Applied analytical skills to evaluate performance metrics and develop "
        "strategic operational plans."
    ),
    KEY_WORKOUTS: (
        "Exhibited exceptional self-discipline and time management skills, "
        "balancing 30+ hour training weeks with academic responsibilities."
    )
}

UNIVERSAL_SKILLS = {
    SKILL_TIME_MANAGEMENT: KEY_WORKOUTS,
    SKILL_STRATEGIC_ANALYSIS: KEY_FILM_STUDY
}

# Mapping: Role Keyword -> (Output Skill Name, Database Key)
ROLE_SKILL_MAPPINGS = {
    KEY_CAPTAIN: (SKILL_LEADERSHIP, KEY_CAPTAIN),
}

BASE_JOBS = ["Sales Development Representative", "Project Coordinator"]
GRIT_JOBS = ["Operations Manager (High Intensity)", "Logistics Specialist"]
TEAMWORK_JOBS = ["Customer Success Manager", "Human Resources Specialist"]

HIGH_SCORE_THRESHOLD = 8


@dataclass
class AthleteProfile:
    """Represents a student-athlete's basic background."""
    sport: str
    role: str


def translate_skills(profile: AthleteProfile) -> Dict[str, str]:
    """
    Translates raw athletic experiences into resume-ready bullet points.

    Args:
        profile: The athlete's profile.

    Returns:
        Dictionary mapping the athletic concept to the corporate translation.
    """
    translations = {
        corpo: SKILL_DB[athletic]
        for corpo, athletic in UNIVERSAL_SKILLS.items()
    }

    # Role Specific
    for role_keyword, (skill_name, db_key) in ROLE_SKILL_MAPPINGS.items():
        if role_keyword in profile.role:
            translations[skill_name] = SKILL_DB[db_key]

    return translations


def match_careers(grit_score: int, teamwork_score: int) -> List[str]:
    """
    Suggests careers based on soft-skill scoring.

    Args:
        grit_score: Int 1-10
        teamwork_score: Int 1-10

    Returns:
        List of job titles.
    """
    matches = list(BASE_JOBS)

    if grit_score > HIGH_SCORE_THRESHOLD:
        matches.extend(GRIT_JOBS)

    if teamwork_score > HIGH_SCORE_THRESHOLD:
        matches.extend(TEAMWORK_JOBS)

    return matches
