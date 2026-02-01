"""
Data layer for The 98% Platform.
Stores static mappings and database constants.
"""

# Domain Constants
SKILL_LEADERSHIP = "Leadership"
SKILL_TIME_MANAGEMENT = "Time Management"
SKILL_STRATEGIC_ANALYSIS = "Strategic Analysis"
SKILL_DECISION_MAKING = "Rapid Decision Making"
SKILL_GOAL_SETTING = "Goal Setting"
SKILL_RESILIENCE = "Resilience"

# Skill Keys
KEY_CAPTAIN = "Captain"
KEY_FILM_STUDY = "Film Study"
KEY_WORKOUTS = "5am Workouts"
KEY_DECISION_MAKING = "Game Time Decisions"
KEY_GOAL_SETTING = "Lap Times"
KEY_RESILIENCE = "Walk-on"

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
    ),
    KEY_DECISION_MAKING: (
        "Demonstrated ability to make high-stakes decisions rapidly "
        "in dynamic, fast-paced environments."
    ),
    KEY_GOAL_SETTING: (
        "Utilized data-driven goal setting to track progress and "
        "achieve continuous performance improvement."
    ),
    KEY_RESILIENCE: (
        "Proved resilience and determination by earning a position "
        "through merit and persistence without guaranteed status."
    )
}

UNIVERSAL_SKILLS = {
    SKILL_TIME_MANAGEMENT: KEY_WORKOUTS,
    SKILL_STRATEGIC_ANALYSIS: KEY_FILM_STUDY
}

# Mapping: Role Keyword -> (Output Skill Name, Database Key)
ROLE_SKILL_MAPPINGS = {
    KEY_CAPTAIN: (SKILL_LEADERSHIP, KEY_CAPTAIN),
    KEY_RESILIENCE: (SKILL_RESILIENCE, KEY_RESILIENCE),
}

# Mapping: Sport Name -> (Output Skill Name, Database Key)
SPORT_SKILL_MAPPINGS = {
    "Basketball": (SKILL_DECISION_MAKING, KEY_DECISION_MAKING),
    "Swimming": (SKILL_GOAL_SETTING, KEY_GOAL_SETTING),
}

BASE_JOBS = ["Sales Development Representative", "Project Coordinator"]
GRIT_JOBS = ["Operations Manager (High Intensity)", "Logistics Specialist"]
TEAMWORK_JOBS = ["Customer Success Manager", "Human Resources Specialist"]

HIGH_SCORE_THRESHOLD = 8
