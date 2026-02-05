"""
Data layer for The 98% Platform.
Stores static mappings and database constants.
"""

# Domain Constants
SKILL_LEADERSHIP = "Leadership"
SKILL_TIME_MANAGEMENT = "Time Management"
SKILL_STRATEGIC_ANALYSIS = "Strategic Analysis"
SKILL_TEAM_COLLABORATION = "Team Collaboration"
SKILL_STRATEGIC_EXECUTION = "Strategic Execution"
SKILL_RESILIENCE = "Resilience"
SKILL_ACADEMIC_EXCELLENCE = "Academic Excellence"

# Skill Keys
KEY_CAPTAIN = "Captain"
KEY_ACADEMIC = "Scholar Athlete"
KEY_FILM_STUDY = "Film Study"
KEY_WORKOUTS = "5am Workouts"
KEY_BASKETBALL = "Basketball"
KEY_FOOTBALL = "Football"
KEY_WALKON = "Walk-on"

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
    KEY_BASKETBALL: (
        "Facilitated seamless team operations through constant communication "
        "and rapid decision-making in fast-paced environments."
    ),
    KEY_FOOTBALL: (
        "Executed complex strategic plans under strict time constraints, "
        "requiring precise coordination with team members."
    ),
    KEY_WALKON: (
        "Demonstrated exceptional grit and adaptability by earning a "
        "position through merit-based competition against recruited peers."
    ),
    KEY_ACADEMIC: (
        "Maintained high academic standing while managing rigorous training "
        "schedules, demonstrating strong intellectual capability and focus."
    )
}

UNIVERSAL_SKILLS = {
    SKILL_TIME_MANAGEMENT: KEY_WORKOUTS,
    SKILL_STRATEGIC_ANALYSIS: KEY_FILM_STUDY
}

# Mapping: Sport Name -> (Output Skill Name, Database Key)
SPORT_SKILL_MAPPINGS = {
    KEY_BASKETBALL: (SKILL_TEAM_COLLABORATION, KEY_BASKETBALL),
    KEY_FOOTBALL: (SKILL_STRATEGIC_EXECUTION, KEY_FOOTBALL),
}

# Mapping: Role Keyword -> (Output Skill Name, Database Key)
ROLE_SKILL_MAPPINGS = {
    KEY_CAPTAIN: (SKILL_LEADERSHIP, KEY_CAPTAIN),
    KEY_WALKON: (SKILL_RESILIENCE, KEY_WALKON),
}

BASE_JOBS = ["Sales Development Representative", "Project Coordinator"]
GRIT_JOBS = ["Operations Manager (High Intensity)", "Logistics Specialist"]
TEAMWORK_JOBS = ["Customer Success Manager", "Human Resources Specialist"]

HIGH_SCORE_THRESHOLD = 8
