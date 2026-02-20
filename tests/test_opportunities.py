"""
Unit tests for unified job matching (opportunities).
"""
import pytest
from src.core.models import AthleteProfile, Job
from src.core.services import match_opportunities


# Mock data
MOCK_JOB_HIGH_GRIT = Job(
    title="High Grit Job",
    employer="HardCorp",
    min_grit=8,
    min_teamwork=0,
    required_skills=["Resilience"]
)

MOCK_JOB_HIGH_TEAMWORK = Job(
    title="High Teamwork Job",
    employer="TeamCorp",
    min_grit=0,
    min_teamwork=8,
    required_skills=["Team Collaboration"]
)

MOCK_JOB_COMPLEX = Job(
    title="Complex Job",
    employer="ComplexCorp",
    min_grit=5,
    min_teamwork=5,
    required_skills=["Resilience", "Strategic Analysis"]
)


@pytest.fixture
def mock_jobs_db(mocker):
    """Mocks the JOBS_DB in services."""
    return mocker.patch(
        "src.core.services.JOBS_DB",
        [MOCK_JOB_HIGH_GRIT, MOCK_JOB_HIGH_TEAMWORK, MOCK_JOB_COMPLEX]
    )


@pytest.fixture
def mock_translate_skills(mocker):
    """Mocks translate_skills to control athlete skills."""
    return mocker.patch("src.core.services.translate_skills")


def test_match_opportunities_perfect_match(mock_jobs_db, mock_translate_skills):
    """Test a perfect match scenario."""
    # Setup
    mock_translate_skills.return_value = {
        "Resilience": "...",
        "Strategic Analysis": "..."
    }
    profile = AthleteProfile(sport="Test", role="Test")

    # Execute (High scores to pass trait filters)
    matches = match_opportunities(profile, grit_score=10, teamwork_score=10)

    # Verify
    titles = [job.title for job in matches]
    assert "Complex Job" in titles
    assert "High Grit Job" in titles  # Has Resilience
    # High Teamwork Job requires Team Collaboration, not in skills
    assert "High Teamwork Job" not in titles


def test_match_opportunities_trait_filtering(mock_jobs_db, mock_translate_skills):
    """Test that jobs are filtered by grit/teamwork even if skills match."""
    mock_translate_skills.return_value = {"Resilience": "..."}
    profile = AthleteProfile(sport="Test", role="Test")

    # Low grit, should filter out High Grit Job
    matches = match_opportunities(profile, grit_score=2, teamwork_score=10)

    titles = [job.title for job in matches]
    assert "High Grit Job" not in titles


def test_match_opportunities_skill_filtering(mock_jobs_db, mock_translate_skills):
    """Test that jobs are filtered if skills are missing."""
    # Missing Strategic Analysis
    mock_translate_skills.return_value = {"Resilience": "..."}
    profile = AthleteProfile(sport="Test", role="Test")

    # High scores
    matches = match_opportunities(profile, grit_score=10, teamwork_score=10)

    titles = [job.title for job in matches]
    assert "Complex Job" not in titles  # Missing Strategic Analysis
    assert "High Grit Job" in titles


def test_match_opportunities_no_matches(mock_jobs_db, mock_translate_skills):
    """Test return empty list when nothing matches."""
    mock_translate_skills.return_value = {}
    profile = AthleteProfile(sport="Test", role="Test")

    matches = match_opportunities(profile, grit_score=0, teamwork_score=0)
    assert matches == []
