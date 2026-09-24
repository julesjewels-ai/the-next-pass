"""
Unit tests for the personalized career plan features (Skill Gap Analysis).
"""
import pytest
from pytest_mock import MockerFixture

from src.core.data import (
    SKILL_LEADERSHIP,
    SKILL_STRATEGIC_ANALYSIS,
    SKILL_TEAM_COLLABORATION,
)
from src.core.models import AthleteProfile, Employer, Job
from src.core.services import get_skill_gaps


@pytest.fixture
def mock_jobs_db(mocker: MockerFixture) -> list[Job]:
    """Mock JOBS_DB with controlled data."""
    jobs = [
        Job(
            title="Sales Rep",
            employer="TechCorp",
            required_skills=[SKILL_STRATEGIC_ANALYSIS]
        ),
        Job(
            title="Project Manager",
            employer="ConsultingGroup",
            required_skills=[SKILL_TEAM_COLLABORATION]
        )
    ]
    mocker.patch('src.core.services.JOBS_DB', jobs)
    return jobs


@pytest.fixture
def mock_employers_index(mocker: MockerFixture) -> dict[str, Employer]:
    """Mock EMPLOYERS_INDEX with controlled data."""
    index = {
        "TechCorp": Employer(
            name="TechCorp",
            industry="Tech",
            required_skills=[SKILL_LEADERSHIP]
        ),
        "ConsultingGroup": Employer(
            name="ConsultingGroup",
            industry="Consulting",
            required_skills=[SKILL_STRATEGIC_ANALYSIS]
        )
    }
    mocker.patch('src.core.services.EMPLOYERS_INDEX', index)
    return index


def test_get_skill_gaps_with_missing_skills(
    mocker: MockerFixture,
    mock_jobs_db: list[Job],
    mock_employers_index: dict[str, Employer]
) -> None:
    """Test that missing skills are correctly identified when athlete lacks some."""
    profile = AthleteProfile(sport="Basketball", role="Player")

    # Mock translate_skills to return an empty dict (no skills)
    mocker.patch('src.core.services.translate_skills', return_value={})

    missing = get_skill_gaps(profile, "Sales Rep")

    # Job requires Strategic Analysis, Employer requires Leadership
    assert sorted(missing) == sorted([SKILL_STRATEGIC_ANALYSIS, SKILL_LEADERSHIP])


def test_get_skill_gaps_with_no_missing_skills(
    mocker: MockerFixture,
    mock_jobs_db: list[Job],
    mock_employers_index: dict[str, Employer]
) -> None:
    """Test when the athlete has all required skills."""
    profile = AthleteProfile(sport="Basketball", role="Captain")

    # Mock translate_skills to return all required skills
    mocker.patch('src.core.services.translate_skills', return_value={
        SKILL_STRATEGIC_ANALYSIS: "Bullet 1",
        SKILL_LEADERSHIP: "Bullet 2"
    })

    missing = get_skill_gaps(profile, "Sales Rep")
    assert missing == []


def test_get_skill_gaps_job_not_found(
    mock_jobs_db: list[Job],
    mock_employers_index: dict[str, Employer]
) -> None:
    """Test that a ValueError is raised when the job title doesn't exist."""
    profile = AthleteProfile(sport="Basketball", role="Captain")

    with pytest.raises(ValueError, match="Job with title 'Nonexistent Job' not found."):
        get_skill_gaps(profile, "Nonexistent Job")


def test_get_skill_gaps_case_insensitive_job_title(
    mocker: MockerFixture,
    mock_jobs_db: list[Job],
    mock_employers_index: dict[str, Employer]
) -> None:
    """Test that the target job title search is case-insensitive."""
    profile = AthleteProfile(sport="Basketball", role="Player")
    mocker.patch('src.core.services.translate_skills', return_value={})

    # "sales rep" instead of "Sales Rep"
    missing = get_skill_gaps(profile, "sales rep")
    assert sorted(missing) == sorted([SKILL_STRATEGIC_ANALYSIS, SKILL_LEADERSHIP])
