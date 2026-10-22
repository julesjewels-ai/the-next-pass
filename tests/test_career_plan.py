import pytest

from src.core.data import (
    SKILL_STRATEGIC_EXECUTION,
    SKILL_TEAM_COLLABORATION,
)
from src.core.models import AthleteProfile, CareerPlan
from src.core.services import generate_career_plan


@pytest.mark.parametrize(
    "sport, role, target_job_title, expected_missing, expected_ready",
    [
        # Basketball Player aiming for HR Specialist (Job needs Team Collaboration, Employer needs Strategic Execution, Team Collaboration)
        # Basketball translates to Team Collaboration. Missing Strategic Execution.
        ("Basketball", "Player", "Human Resources Specialist", [SKILL_STRATEGIC_EXECUTION], False),

        # Football Player aiming for HR Specialist
        # Football translates to Strategic Execution. Missing Team Collaboration.
        ("Football", "Player", "Human Resources Specialist", [SKILL_TEAM_COLLABORATION], False),

        # Football Captain aiming for SDR (Job needs Strategic Analysis, Employer TechCorp needs Leadership, Strategic Analysis)
        # Football Captain translates to Strategic Execution, Leadership, Operational Command.
        # UNIVERSAL_SKILLS provide Strategic Analysis and Time Management for all.
        # So they have everything needed.
        ("Football", "Captain", "Sales Development Representative", [], True),

        # Walk-on aiming for Project Coordinator (Needs Team Collaboration + ConsultingGroup skills: Strategic Execution, Team Collaboration)
        # Walk-on translates to Resilience. Missing Strategic Execution, Team Collaboration.
        ("Swimming", "Walk-on", "Project Coordinator", [SKILL_STRATEGIC_EXECUTION, SKILL_TEAM_COLLABORATION], False),

        # Case Insensitive match check
        ("Basketball", "Player", "human resources specialist", [SKILL_STRATEGIC_EXECUTION], False)
    ]
)
def test_generate_career_plan_logic(sport, role, target_job_title, expected_missing, expected_ready):
    profile = AthleteProfile(sport=sport, role=role)
    plan = generate_career_plan(profile, target_job_title)

    assert isinstance(plan, CareerPlan)
    assert plan.target_job_title.lower() == target_job_title.lower()

    # Use set comparison for lists that might be unordered
    assert set(plan.missing_skills) == set(expected_missing)
    assert plan.is_ready == expected_ready


def test_generate_career_plan_invalid_job():
    profile = AthleteProfile(sport="Football", role="Player")
    with pytest.raises(ValueError, match="Target job 'Astronaut' not found in database."):
        generate_career_plan(profile, "Astronaut")
