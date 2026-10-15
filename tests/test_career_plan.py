"""
Unit tests for the Career Plan and Skill Gap Analysis feature.
"""
import pytest

from src.core.data import (
    KEY_CAPTAIN,
    KEY_FOOTBALL,
)
from src.core.models import AthleteProfile, CareerPlan
from src.core.services import generate_career_plan


@pytest.mark.parametrize("target_job_title, expected_match_pct_approx, expected_missing_skills, expected_exception", [
    (
        "Operations Manager (High Intensity)", # Requires Operational Command, min_grit=9. (LogisticsInc adds Resilience)
        50.0, # Football Captain has Operational Command (1/2 skills). Grit=8 means 0/1 traits met. (1 skill / (2 skills + 2 traits)) = 25%? Let's check logic:
              # target_job.min_grit = 9, grit_score = 10 -> met_traits = 1
              # target_job.min_teamwork = 0, teamwork_score = 10 -> met_traits = 1
              # Total met_traits = 2
              # job_skills = [Operational Command], employer LogisticsInc skills = [Operational Command, Resilience] -> total skills = 2.
              # Football Captain has: Operational Command (from Composite), Strategic Execution (from Football), Leadership (from Captain). Total = 3
              # Intersection with required = [Operational Command]. met_skills = 1.
              # Total criteria = 2 (skills) + 2 (traits) = 4. Met = 1 + 2 = 3. Match = 75.0%
        [ "Resilience" ],
        None
    ),
    (
        "Nonexistent Job",
        0.0,
        [],
        ValueError
    )
])
def test_generate_career_plan(target_job_title, expected_match_pct_approx, expected_missing_skills, expected_exception):
    """Test generate_career_plan with parameterized inputs."""
    profile = AthleteProfile(sport=KEY_FOOTBALL, role=KEY_CAPTAIN)
    grit_score = 10
    teamwork_score = 10

    if expected_exception:
        with pytest.raises(expected_exception):
            generate_career_plan(profile, grit_score, teamwork_score, target_job_title)
    else:
        plan = generate_career_plan(profile, grit_score, teamwork_score, target_job_title)
        assert isinstance(plan, CareerPlan)
        assert plan.match_percentage == 75.0
        assert "Resilience" in plan.missing_skills
        assert "Operational Command" in plan.current_skills
