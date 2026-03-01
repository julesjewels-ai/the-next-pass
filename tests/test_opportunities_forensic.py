"""
Forensic unit tests for opportunity matching (skills + soft skills).
Isolates logic by mocking databases.
"""
from typing import List, Dict
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

def test_match_opportunities_forensic_exact_match(
    mocker: MockerFixture,
    mock_jobs_db: List[Job],
    mock_employers_index: Dict[str, Employer]
) -> None:
    """Test exact match boundary where athlete has precisely the required skills."""
    # Mock translate_skills so we have absolute control over the returned skills
    mocker.patch(
        "src.core.services.translate_skills",
        return_value={"Analysis": "Skill1", "Integrity": "Skill2"}
    )
    profile = AthleteProfile(sport="Test", role="Test")

    matches = match_opportunities(profile, grit_score=5, teamwork_score=5)
    titles = [job.title for job in matches]

    assert "Forensic Analyst" in titles, "Should match exact skills"
    assert len(titles) == 1, "Should only match the one job"

def test_match_opportunities_forensic_missing_employer_skill(
    mocker: MockerFixture,
    mock_jobs_db: List[Job],
    mock_employers_index: Dict[str, Employer]
) -> None:
    """Test failure when athlete has job skills but missing employer skills."""
    mocker.patch(
        "src.core.services.translate_skills",
        return_value={"Analysis": "Skill1"} # Missing Integrity
    )
    profile = AthleteProfile(sport="Test", role="Test")

    matches = match_opportunities(profile, grit_score=5, teamwork_score=5)

    assert len(matches) == 0, "Should fail because Employer skill 'Integrity' is missing"

def test_match_opportunities_forensic_missing_job_skill(
    mocker: MockerFixture,
    mock_jobs_db: List[Job],
    mock_employers_index: Dict[str, Employer]
) -> None:
    """Test failure when athlete has employer skills but missing job skills."""
    mocker.patch(
        "src.core.services.translate_skills",
        return_value={"Integrity": "Skill2"} # Missing Analysis
    )
    profile = AthleteProfile(sport="Test", role="Test")

    matches = match_opportunities(profile, grit_score=5, teamwork_score=5)

    assert len(matches) == 0, "Should fail because Job skill 'Analysis' is missing"

def test_match_opportunities_forensic_empty_db(
    mocker: MockerFixture,
    mock_employers_index: Dict[str, Employer]
) -> None:
    """Test edge case with empty jobs database."""
    mocker.patch("src.core.services.JOBS_DB", [])
    mocker.patch(
        "src.core.services.translate_skills",
        return_value={"Analysis": "Skill1", "Integrity": "Skill2"}
    )
    profile = AthleteProfile(sport="Test", role="Test")

    matches = match_opportunities(profile, grit_score=5, teamwork_score=5)

    assert len(matches) == 0, "Should return empty list for empty db"

def test_match_opportunities_forensic_employer_not_found(
    mocker: MockerFixture,
    mock_jobs_db: List[Job]
) -> None:
    """Test resilience when job's employer is not in EMPLOYERS_INDEX."""
    # Ensure index is empty
    mocker.patch("src.core.services.EMPLOYERS_INDEX", {})
    mocker.patch(
        "src.core.services.translate_skills",
        return_value={"Analysis": "Skill1"}
    )
    profile = AthleteProfile(sport="Test", role="Test")

    matches = match_opportunities(profile, grit_score=5, teamwork_score=5)
    titles = [job.title for job in matches]

    assert "Forensic Analyst" in titles, "Should still match if employer not found but job skills match"
