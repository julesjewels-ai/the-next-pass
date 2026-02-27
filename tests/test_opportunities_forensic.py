import pytest
from pytest_mock import MockerFixture
from src.core.services import match_opportunities
from src.core.models import AthleteProfile, Job
from typing import List, Dict, Any
from unittest.mock import Mock

@pytest.fixture
def mock_jobs_db(mocker: MockerFixture) -> List[Job]:
    """Fixture to mock the JOBS_DB with a controlled set of jobs."""
    jobs = [
        Job(title="Low Bar", min_grit=1, min_teamwork=1, required_skills=["Skill A"]),
        Job(title="High Bar", min_grit=8, min_teamwork=8, required_skills=["Skill A", "Skill B"]),
        Job(title="Specialist", min_grit=5, min_teamwork=5, required_skills=["Skill C"]),
        Job(title="Generalist", min_grit=3, min_teamwork=3, required_skills=[])
    ]
    mocker.patch("src.core.services.JOBS_DB", jobs)
    return jobs

@pytest.fixture
def mock_translate_skills(mocker: MockerFixture) -> Mock:
    """Fixture to control the output of translate_skills."""
    mock = mocker.patch("src.core.services.translate_skills")
    return mock

@pytest.mark.parametrize("grit, teamwork, athlete_skills, expected_titles", [
    # Case 1: Perfect Match (High Scores, All Skills)
    (10, 10, {"Skill A": "Desc", "Skill B": "Desc", "Skill C": "Desc"}, ["Low Bar", "High Bar", "Specialist", "Generalist"]),

    # Case 2: Grit Filter (Low Grit, High Teamwork, All Skills)
    (4, 10, {"Skill A": "Desc", "Skill B": "Desc", "Skill C": "Desc"}, ["Low Bar", "Generalist"]),

    # Case 3: Teamwork Filter (High Grit, Low Teamwork, All Skills)
    (10, 4, {"Skill A": "Desc", "Skill B": "Desc", "Skill C": "Desc"}, ["Low Bar", "Generalist"]),

    # Case 4: Skill Mismatch (High Scores, Missing "Skill B")
    (10, 10, {"Skill A": "Desc", "Skill C": "Desc"}, ["Low Bar", "Specialist", "Generalist"]),

    # Case 5: Partial Skill Match (High Scores, Only "Skill A")
    (10, 10, {"Skill A": "Desc"}, ["Low Bar", "Generalist"]),

    # Case 6: No Skills (High Scores, No Skills)
    (10, 10, {}, ["Generalist"]),

    # Case 7: Boundary Condition (Exact Thresholds for Specialist)
    (5, 5, {"Skill C": "Desc"}, ["Specialist", "Generalist"]),

    # Case 8: Boundary Condition (One below Threshold for Specialist)
    (4, 5, {"Skill C": "Desc"}, ["Generalist"]),

    # Case 9: Boundary Condition (One below Threshold for Specialist - Teamwork)
    (5, 4, {"Skill C": "Desc"}, ["Generalist"]),
])
def test_match_opportunities_forensic(
    mock_jobs_db: List[Job],
    mock_translate_skills: Mock,
    grit: int,
    teamwork: int,
    athlete_skills: Dict[str, str],
    expected_titles: List[str]
) -> None:
    """
    Forensic test suite for match_opportunities to verify:
    1. Soft skill filtering (grit/teamwork thresholds).
    2. Hard skill matching (subset logic).
    3. Integration of both filters.
    """
    # Arrange
    profile = AthleteProfile(sport="Test", role="Test")
    mock_translate_skills.return_value = athlete_skills

    # Act
    matches = match_opportunities(profile, grit, teamwork)
    match_titles = [job.title for job in matches]

    # Assert
    assert sorted(match_titles) == sorted(expected_titles)

def test_match_opportunities_empty_db(mocker: MockerFixture, mock_translate_skills: Mock) -> None:
    """Verify behavior when JOBS_DB is empty."""
    mocker.patch("src.core.services.JOBS_DB", [])
    mock_translate_skills.return_value = {"Skill A": "Desc"}

    matches = match_opportunities(AthleteProfile(sport="Test", role="Test"), 10, 10)
    assert matches == []
