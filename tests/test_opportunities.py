"""
Unit tests for opportunity matching logic.
"""
from typing import List, Dict
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture
from src.core.models import AthleteProfile, Job
from src.core.services import match_opportunities

# Mock data
MOCK_JOBS = [
    Job(
        title="Software Engineer",
        employer="TechCorp",
        min_grit=5,
        min_teamwork=5,
        required_skills=["Coding", "Problem Solving"]
    ),
    Job(
        title="Sales Rep",
        employer="BizCorp",
        min_grit=8,
        min_teamwork=8,
        required_skills=["Communication", "Resilience"]
    ),
    Job(
        title="Team Lead",
        employer="TechCorp",
        min_grit=6,
        min_teamwork=9,
        required_skills=["Leadership", "Communication"]
    )
]

@pytest.fixture
def mock_jobs_db(mocker: MockerFixture) -> None:
    """Mock the JOBS_DB to have predictable data."""
    mocker.patch("src.core.services.JOBS_DB", MOCK_JOBS)

@pytest.fixture
def mock_translate_skills(mocker: MockerFixture) -> Mock:
    """Mock translate_skills to return controlled skills."""
    return mocker.patch("src.core.services.translate_skills")

@pytest.mark.parametrize("grit, teamwork, skills, expected_titles", [
    # Scenario 1: High scores, all skills -> Match all relevant
    (10, 10, {"Coding": "desc", "Problem Solving": "desc", "Communication": "desc", "Resilience": "desc", "Leadership": "desc"},
     ["Software Engineer", "Sales Rep", "Team Lead"]),

    # Scenario 2: Low grit -> Filter out high grit jobs
    (4, 10, {"Coding": "desc", "Problem Solving": "desc"}, []),

    # Scenario 3: High scores, missing skills for some jobs
    (10, 10, {"Coding": "desc", "Problem Solving": "desc"}, ["Software Engineer"]),

    # Scenario 4: Exact match for Sales Rep
    (8, 8, {"Communication": "desc", "Resilience": "desc"}, ["Sales Rep"]),

    # Scenario 5: High scores, no skills -> No matches
    (10, 10, {}, []),
])
def test_match_opportunities_filtering(
    mock_jobs_db: None,
    mock_translate_skills: Mock,
    grit: int,
    teamwork: int,
    skills: Dict[str, str],
    expected_titles: List[str]
) -> None:
    """Test filtering logic based on grit, teamwork, and skills."""
    # Arrange
    mock_translate_skills.return_value = skills
    profile = AthleteProfile(sport="Any", role="Any")

    # Act
    matches = match_opportunities(profile, grit, teamwork)
    match_titles = [job.title for job in matches]

    # Assert
    assert sorted(match_titles) == sorted(expected_titles)

def test_match_opportunities_calls_translate(mock_jobs_db: None, mock_translate_skills: Mock) -> None:
    """Verify that translate_skills is called with the correct profile."""
    # Arrange
    mock_translate_skills.return_value = {}
    profile = AthleteProfile(sport="Football", role="Captain")

    # Act
    match_opportunities(profile, 8, 8)

    # Assert
    mock_translate_skills.assert_called_once_with(profile)
