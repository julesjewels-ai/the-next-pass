"""
Forensic unit tests for opportunity matching (skills + soft skills).
Isolates logic by mocking databases.
"""
from typing import List, Dict, Any, Callable
import pytest
from pytest_mock import MockerFixture

from src.core.models import AthleteProfile, Job, Employer
from src.core.services import match_opportunities

@pytest.fixture
def mock_jobs_db(mocker: MockerFixture) -> List[Job]:
    """Mock JOBS_DB with controlled data."""
    jobs = [
        Job(
            title="Forensic Analyst",
            employer="MockCorp",
            min_grit=5,
            min_teamwork=5,
            required_skills=["Analysis"]
        ),
        Job(
            title="Senior Forensic Analyst",
            employer="MockCorp",
            min_grit=9,
            min_teamwork=9,
            required_skills=["Analysis", "Leadership"]
        ),
        Job(
            title="Unrelated Role",
            employer="OtherCorp",
            min_grit=5,
            min_teamwork=5,
            required_skills=["Sales"]
        ),
    ]
    mocker.patch("src.core.services.JOBS_DB", jobs)
    return jobs

@pytest.fixture
def mock_employers_index(mocker: MockerFixture) -> Dict[str, Employer]:
    """Mock EMPLOYERS_INDEX with controlled data."""
    index = {
        "MockCorp": Employer(
            name="MockCorp",
            industry="Testing",
            required_skills=["Integrity"]
        ),
        "OtherCorp": Employer(
            name="OtherCorp",
            industry="Other",
            required_skills=["Communication"]
        )
    }
    mocker.patch("src.core.services.EMPLOYERS_INDEX", index)
    return index

@pytest.mark.parametrize(
    "translated_skills, empty_db, empty_index, expected_titles, assert_msg",
    [
        (
            {"Analysis": "Skill1", "Integrity": "Skill2"}, False, False, ["Forensic Analyst"],
            "Should match exact skills"
        ),
        (
            {"Analysis": "Skill1"}, False, False, [],
            "Should fail because Employer skill 'Integrity' is missing"
        ),
        (
            {"Integrity": "Skill2"}, False, False, [],
            "Should fail because Job skill 'Analysis' is missing"
        ),
        (
            {"Analysis": "Skill1", "Integrity": "Skill2"}, True, False, [],
            "Should return empty list for empty db"
        ),
        (
            {"Analysis": "Skill1"}, False, True, ["Forensic Analyst"],
            "Should still match if employer not found but job skills match"
        ),
    ],
)
def test_match_opportunities_forensic_edge_cases(
    mocker: MockerFixture,
    mock_jobs_db: List[Job],
    mock_employers_index: Dict[str, Employer],
    translated_skills: Dict[str, str],
    empty_db: bool,
    empty_index: bool,
    expected_titles: List[str],
    assert_msg: str
) -> None:
    """Test opportunity matching logic focusing on complex boundary conditions."""
    mocker.patch("src.core.services.translate_skills", return_value=translated_skills)

    if empty_db:
        mocker.patch("src.core.services.JOBS_DB", [])
    if empty_index:
        mocker.patch("src.core.services.EMPLOYERS_INDEX", {})

    profile = AthleteProfile(sport="Test", role="Test")
    matches = match_opportunities(profile, grit_score=5, teamwork_score=5)
    titles = [job.title for job in matches]

    assert titles == expected_titles, assert_msg
