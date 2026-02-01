"""
Data layer for The 98% Platform.
Stores static mappings and database constants.
"""

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
        "Demonstrated leadership by coordinating team activities and "
        "fostering a collaborative environment under high-pressure conditions."
    ),
    KEY_FILM_STUDY: (
        "Applied analytical skills to evaluate performance metrics and "
        "develop strategic operational plans."
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
