"""
Data layer for The 98% Platform.
Stores static mappings and database constants.
"""
from src.core.models import Employer, Job

# Domain Constants
SKILL_LEADERSHIP = "Leadership"
SKILL_TIME_MANAGEMENT = "Time Management"
SKILL_STRATEGIC_ANALYSIS = "Strategic Analysis"
SKILL_TEAM_COLLABORATION = "Team Collaboration"
SKILL_STRATEGIC_EXECUTION = "Strategic Execution"
SKILL_RESILIENCE = "Resilience"
SKILL_OPERATIONAL_COMMAND = "Operational Command"

# Skill Keys
KEY_CAPTAIN = "Captain"
KEY_FILM_STUDY = "Film Study"
KEY_WORKOUTS = "5am Workouts"
KEY_BASKETBALL = "Basketball"
KEY_FOOTBALL = "Football"
KEY_WALKON = "Walk-on"
KEY_FOOTBALL_CAPTAIN = "Football Captain"

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
    KEY_FOOTBALL_CAPTAIN: (
        "Directed large-scale team maneuvers and maintained operational "
        "cohesion under strict play clocks."
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

# Mapping: (Sport Keyword, Role Keyword) -> (Output Skill Name, Database Key)
COMPOSITE_SKILL_MAPPINGS = {
    (KEY_FOOTBALL, KEY_CAPTAIN): (SKILL_OPERATIONAL_COMMAND, KEY_FOOTBALL_CAPTAIN),
}

HIGH_SCORE_THRESHOLD = 8

SAMPLE_EMPLOYERS = [
    Employer(
        name="TechCorp",
        industry="Technology",
        required_skills=[SKILL_LEADERSHIP, SKILL_STRATEGIC_ANALYSIS]
    ),
    Employer(
        name="LogisticsInc",
        industry="Supply Chain",
        required_skills=[SKILL_OPERATIONAL_COMMAND, SKILL_RESILIENCE]
    ),
    Employer(
        name="ConsultingGroup",
        industry="Consulting",
        required_skills=[SKILL_STRATEGIC_EXECUTION, SKILL_TEAM_COLLABORATION]
    )
]

EMPLOYERS_INDEX = {emp.name: emp for emp in SAMPLE_EMPLOYERS}

JOBS_DB = [
    Job(
        title="Sales Development Representative",
        employer="TechCorp",
        required_skills=[SKILL_STRATEGIC_ANALYSIS],
        base_salary=70000,
        signing_bonus=5000
    ),
    Job(
        title="Project Coordinator",
        employer="ConsultingGroup",
        required_skills=[SKILL_TEAM_COLLABORATION],
        base_salary=80000,
        signing_bonus=0
    ),
    Job(
        title="Operations Manager (High Intensity)",
        min_grit=HIGH_SCORE_THRESHOLD + 1,
        employer="LogisticsInc",
        required_skills=[SKILL_OPERATIONAL_COMMAND],
        base_salary=90000,
        signing_bonus=10000
    ),
    Job(
        title="Logistics Specialist",
        min_grit=HIGH_SCORE_THRESHOLD + 1,
        employer="LogisticsInc",
        required_skills=[SKILL_STRATEGIC_EXECUTION],
        base_salary=75000,
        signing_bonus=0
    ),
    Job(
        title="Customer Success Manager",
        min_teamwork=HIGH_SCORE_THRESHOLD + 1,
        employer="TechCorp",
        required_skills=[SKILL_TEAM_COLLABORATION, SKILL_LEADERSHIP],
        base_salary=85000,
        signing_bonus=5000
    ),
    Job(
        title="Human Resources Specialist",
        min_teamwork=HIGH_SCORE_THRESHOLD + 1,
        employer="ConsultingGroup",
        required_skills=[SKILL_TEAM_COLLABORATION],
        base_salary=65000,
        signing_bonus=0
    )
]
