"""
Unit tests for the Career Plans/Skill Gap Analysis feature.
"""
import pytest

from src.core.data import (
    SKILL_LEADERSHIP,
    SKILL_STRATEGIC_ANALYSIS,
    SKILL_TEAM_COLLABORATION,
)
from src.core.models import AthleteProfile, CareerPlan, Employer, Job
from src.core.services import generate_career_plan


@pytest.fixture
def base_profile():
    return AthleteProfile(sport="Basketball", role="Player")

@pytest.fixture(autouse=True)
def mock_data(mocker):
    """Mock the JOBS_DB and EMPLOYERS_INDEX to have predictable test cases."""
    mock_employers_index = {
        "MockCorp": Employer(name="MockCorp", industry="Tech", required_skills=[]),
        "StrictCorp": Employer(name="StrictCorp", industry="Finance", required_skills=[SKILL_LEADERSHIP])
    }
    mock_jobs_db = [
        Job(title="Easy Job", employer="MockCorp", required_skills=[SKILL_TEAM_COLLABORATION]),
        Job(title="Hard Job", employer="StrictCorp", required_skills=[SKILL_STRATEGIC_ANALYSIS])
    ]
    mocker.patch("src.core.services.JOBS_DB", mock_jobs_db)
    mocker.patch("src.core.services.EMPLOYERS_INDEX", mock_employers_index)

@pytest.mark.parametrize("target_job_title, expected_is_ready, expected_missing", [
    ("Easy Job", True, []), # Requires only Team Collaboration, which Basketball Player has
    ("Hard Job", False, [SKILL_LEADERSHIP]), # Requires Leadership from Employer, which they don't have
])
def test_generate_career_plan_found(base_profile, target_job_title, expected_is_ready, expected_missing):
    """Test generating a career plan for a job that exists."""
    plan = generate_career_plan(base_profile, target_job_title)

    assert plan is not None
    assert isinstance(plan, CareerPlan)
    assert plan.target_job_title == target_job_title
    assert plan.is_ready == expected_is_ready
    for skill in expected_missing:
        assert skill in plan.missing_skills

    # Basketball Player has Team Collaboration, so it should be in current_skills
    assert SKILL_TEAM_COLLABORATION in plan.current_skills

def test_generate_career_plan_not_found(base_profile):
    """Test generating a career plan for a job that does not exist."""
    plan = generate_career_plan(base_profile, "Astronaut")
    assert plan is None

def test_generate_career_plan_case_insensitive(base_profile):
    """Test that finding the target job is case-insensitive."""
    plan = generate_career_plan(base_profile, "eAsY jOb")
    assert plan is not None
    assert plan.target_job_title == "Easy Job"
