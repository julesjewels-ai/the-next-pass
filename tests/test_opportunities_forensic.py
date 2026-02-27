"""
Forensic tests for `match_opportunities` edge cases and disjoint sets.
"""
import pytest
from src.core.models import AthleteProfile, Job, Employer
from src.core.services import match_opportunities


@pytest.fixture
def empty_db(mocker):
    """Mocks an empty JOBS_DB."""
    mocker.patch("src.core.services.JOBS_DB", [])
    mocker.patch("src.core.services.EMPLOYERS_INDEX", {})
    return []


@pytest.fixture
def mock_dbs(mocker):
    """Mocks JOBS_DB and EMPLOYERS_INDEX for forensic testing."""
    employers = {
        "StrictCorp": Employer(
            name="StrictCorp",
            industry="Tech",
            required_skills=["A", "B"]
        ),
        "LenientCorp": Employer(
            name="LenientCorp",
            industry="Sales",
            required_skills=["A"]
        )
    }
    jobs = [
        Job(
            title="Strict Job",
            employer="StrictCorp",
            required_skills=["C"],
            min_grit=5,
            min_teamwork=5
        ),
        Job(
            title="Lenient Job",
            employer="LenientCorp",
            required_skills=["D"],
            min_grit=5,
            min_teamwork=5
        ),
        Job(
            title="No Employer Job",
            employer="UnknownCorp",
            required_skills=["A"],
            min_grit=5,
            min_teamwork=5
        )
    ]
    mocker.patch("src.core.services.EMPLOYERS_INDEX", employers)
    mocker.patch("src.core.services.JOBS_DB", jobs)
    return jobs


def test_match_opportunities_empty_db(empty_db):
    """Test behavior when the database is completely empty."""
    profile = AthleteProfile(sport="Basketball", role="Player")
    matches = match_opportunities(profile, grit_score=10, teamwork_score=10)
    assert len(matches) == 0


def test_match_opportunities_disjoint_skills(mock_dbs, mocker):
    """Test when athlete has job skills but lacks employer skills."""
    # Athlete has 'C' (matches Strict Job) but lacks 'A' and 'B' (StrictCorp).
    mocker.patch("src.core.services.translate_skills", return_value={"C": "Skill C"})
    profile = AthleteProfile(sport="TestSport", role="TestRole")

    matches = match_opportunities(profile, grit_score=10, teamwork_score=10)
    titles = [job.title for job in matches]

    assert "Strict Job" not in titles
    assert len(matches) == 0


def test_match_opportunities_exact_match(mock_dbs, mocker):
    """Test when athlete has exactly the required skills for job and employer."""
    # Athlete has 'A', 'B', 'C' matching Strict Job + StrictCorp exactly
    mocker.patch(
        "src.core.services.translate_skills",
        return_value={"A": "Skill A", "B": "Skill B", "C": "Skill C"}
    )
    profile = AthleteProfile(sport="TestSport", role="TestRole")

    matches = match_opportunities(profile, grit_score=10, teamwork_score=10)
    titles = [job.title for job in matches]

    assert "Strict Job" in titles
    assert "Lenient Job" not in titles # Lacks 'D'


def test_match_opportunities_unknown_employer(mock_dbs, mocker):
    """Test when a job's employer does not exist in EMPLOYERS_INDEX."""
    # Athlete has 'A', matching "No Employer Job"
    mocker.patch("src.core.services.translate_skills", return_value={"A": "Skill A"})
    profile = AthleteProfile(sport="TestSport", role="TestRole")

    matches = match_opportunities(profile, grit_score=10, teamwork_score=10)
    titles = [job.title for job in matches]

    # Should match because employer is unknown, meaning employer_skills_met defaults to True
    assert "No Employer Job" in titles
    assert "Lenient Job" not in titles # Lacks 'D'


def test_match_opportunities_score_boundaries(mock_dbs, mocker):
    """Test boundary conditions for grit and teamwork scores."""
    mocker.patch(
        "src.core.services.translate_skills",
        return_value={"A": "Skill A", "B": "Skill B", "C": "Skill C"}
    )
    profile = AthleteProfile(sport="TestSport", role="TestRole")

    # Exact boundary (should pass)
    matches = match_opportunities(profile, grit_score=5, teamwork_score=5)
    assert len(matches) > 0

    # Off by one grit (should fail)
    matches = match_opportunities(profile, grit_score=4, teamwork_score=5)
    assert len(matches) == 0

    # Off by one teamwork (should fail)
    matches = match_opportunities(profile, grit_score=5, teamwork_score=4)
    assert len(matches) == 0
