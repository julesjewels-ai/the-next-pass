"""
Core business logic for The 98% Platform.

Handles the translation of athletic experiences into professional terminology
and matches athletes with suitable career paths.
"""

from dataclasses import dataclass
from typing import Dict, List

@dataclass
class AthleteProfile:
    """Represents a student-athlete's basic background."""
    sport: str
    role: str

class CareerPlatform:
    """Main controller for platform features."""

    def __init__(self) -> None:
        self._skill_db = {
            "Captain": "Demonstrated leadership by coordinating team activities and fostering a collaborative environment under high-pressure conditions.",
            "Film Study": "Applied analytical skills to evaluate performance metrics and develop strategic operational plans.",
            "5am Workouts": "Exhibited exceptional self-discipline and time management skills, balancing 30+ hour training weeks with academic responsibilities.",
            "Bench/Reserve": "Maintained high readiness and team support while actively contributing to group preparation and morale.",
            "Injury Rehab": "Showcased resilience and adaptability by overcoming significant setbacks through structured recovery planning."
        }

    def translate_skills(self, profile: AthleteProfile) -> Dict[str, str]:
        """
        Translates raw athletic experiences into resume-ready bullet points.
        
        Args:
            profile: The athlete's profile.
            
        Returns:
            Dictionary mapping the athletic concept to the corporate translation.
        """
        translations = {}
        
        # Universal Athlete Skills
        translations["Time Management"] = self._skill_db["5am Workouts"]
        translations["Strategic Analysis"] = self._skill_db["Film Study"]

        # Role Specific
        if "Captain" in profile.role:
            translations["Leadership"] = self._skill_db["Captain"]
        
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
        matches = ["Sales Development Representative", "Project Coordinator"]
        
        if grit_score > 8:
            matches.append("Operations Manager (High Intensity)")
            matches.append("Logistics Specialist")
            
        if teamwork_score > 8:
            matches.append("Customer Success Manager")
            matches.append("Human Resources Specialist")
            
        return matches