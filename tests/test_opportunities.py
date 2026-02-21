"""
Unit tests for unified matching service (opportunities).
"""
import pytest
from pytest_mock import MockerFixture
from src.core.models import AthleteProfile, Job
from src.core.services import match_opportunities

# Define test data
@pytest.fixture
def mock_profile() -> AthleteProfile:
    return AthleteProfile(sport="TestSport", role="TestRole")

@pytest.fixture
def mock_jobs() -> list[Job]:
    return [
        Job(
            title="Junior Dev",
            employer="TechCorp",
            min_grit=5,
            min_teamwork=5,
            required_skills=["Python", "Git"]
        ),
        Job(
            title="Senior Dev",
            employer="TechCorp",
            min_grit=8,
            min_teamwork=8,
            required_skills=["Python", "System Design"]
        ),
        Job(
            title="Manager",
            employer="BizCorp",
            min_grit=6,
            min_teamwork=9,
            required_skills=["Leadership"]
        )
    ]

def test_match_opportunities_happy_path(mocker: MockerFixture, mock_profile, mock_jobs):
    """Should return jobs where scores and skills match."""
    # Mock JOBS_DB
    mocker.patch("src.core.services.JOBS_DB", mock_jobs)

    # Mock translate_skills to return required skills
    mocker.patch("src.core.services.translate_skills", return_value={
        "Python": "Coding",
        "Git": "Version Control"
    })

    # Call with sufficient scores (7, 7) - should match Junior Dev (5, 5)
    # Senior Dev requires 8, Manager requires 9 teamwork or Leadership skill (not present)
    matches = match_opportunities(mock_profile, grit_score=7, teamwork_score=7)

    assert len(matches) == 1
    assert matches[0].title == "Junior Dev"

def test_match_opportunities_score_filtering(mocker: MockerFixture, mock_profile, mock_jobs):
    """Should filter out jobs with high score requirements."""
    mocker.patch("src.core.services.JOBS_DB", mock_jobs)
    mocker.patch("src.core.services.translate_skills", return_value={
        "Python": "Coding",
        "Git": "Version Control",
        "System Design": "Architecture"
    })

    # Low scores (4, 4) -> No matches even if skills align
    matches = match_opportunities(mock_profile, grit_score=4, teamwork_score=4)
    assert len(matches) == 0

    # High scores (9, 9) -> Matches Junior Dev and Senior Dev
    # Manager requires Leadership which is missing
    matches_high = match_opportunities(mock_profile, grit_score=9, teamwork_score=9)
    assert len(matches_high) == 2
    titles = [j.title for j in matches_high]
    assert "Junior Dev" in titles
    assert "Senior Dev" in titles

def test_match_opportunities_skill_filtering(mocker: MockerFixture, mock_profile, mock_jobs):
    """Should filter out jobs where required skills are missing."""
    mocker.patch("src.core.services.JOBS_DB", mock_jobs)

    # Only Python skill, missing Git
    mocker.patch("src.core.services.translate_skills", return_value={
        "Python": "Coding"
    })

    # Scores are high enough for Junior Dev, but skills missing
    matches = match_opportunities(mock_profile, grit_score=10, teamwork_score=10)
    assert len(matches) == 0

def test_match_opportunities_empty_db(mocker: MockerFixture, mock_profile):
    """Should handle empty database gracefully."""
    mocker.patch("src.core.services.JOBS_DB", [])
    mocker.patch("src.core.services.translate_skills", return_value={})

    matches = match_opportunities(mock_profile, grit_score=10, teamwork_score=10)
    assert matches == []
