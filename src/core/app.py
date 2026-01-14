"""
Core business logic for The 98% Platform.

Handles the translation of athletic experiences into professional terminology
and matches athletes with suitable career paths.
"""

from dataclasses import dataclass
from typing import Dict, List

SKILL_DB = {
    "Captain": (
        "Demonstrated leadership by coordinating team activities and fostering a "
        "collaborative environment under high-pressure conditions."
    ),
    "Film Study": (
        "Applied analytical skills to evaluate performance metrics and develop "
        "strategic operational plans."
    ),
    "5am Workouts": (
        "Exhibited exceptional self-discipline and time management skills, "
        "balancing 30+ hour training weeks with academic responsibilities."
    ),
    "Bench/Reserve": (
        "Maintained high readiness and team support while actively contributing "
        "to group preparation and morale."
    ),
    "Injury Rehab": (
        "Showcased resilience and adaptability by overcoming significant "
        "setbacks through structured recovery planning."
    )
}

UNIVERSAL_SKILLS = {
    "Time Management": "5am Workouts",
    "Strategic Analysis": "Film Study"
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

class CareerPlatform:
    """Main controller for platform features."""

    def translate_skills(self, profile: AthleteProfile) -> Dict[str, str]:
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
        if "Captain" in profile.role:
            translations["Leadership"] = SKILL_DB["Captain"]

        return translations

    def match_careers(self, grit_score: int, teamwork_score: int) -> List[str]:
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
