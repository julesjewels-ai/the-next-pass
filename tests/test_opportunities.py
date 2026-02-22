"""
Tests for unified job opportunity matching.
"""
import pytest
from src.core.models import AthleteProfile, Job
# match_opportunities will be implemented in src/core/services.py
# For now, we import it to test, assuming it will be there.
from src.core.services import match_opportunities

# Mock data
MOCK_SKILLS = {"Leadership": "Some desc", "Strategic Analysis": "Desc"}

@pytest.fixture
def mock_translate(mocker):
    """Mock translate_skills to return a fixed set of skills."""
    return mocker.patch("src.core.services.translate_skills", return_value=MOCK_SKILLS)

@pytest.fixture
def mock_jobs_db(mocker):
    """Mock JOBS_DB with controlled test cases."""
    jobs = [
        Job(title="Perfect Match", min_grit=5, min_teamwork=5, required_skills=["Leadership"]),
        Job(title="Skill Mismatch", min_grit=5, min_teamwork=5, required_skills=["Coding"]),
        Job(title="Grit Mismatch", min_grit=10, min_teamwork=5, required_skills=["Leadership"]),
        Job(title="Teamwork Mismatch", min_grit=5, min_teamwork=10, required_skills=["Leadership"]),
        Job(title="Subset Match", min_grit=5, min_teamwork=5, required_skills=["Leadership", "Strategic Analysis"]),
        Job(title="Superset Mismatch", min_grit=5, min_teamwork=5, required_skills=["Leadership", "Strategic Analysis", "Coding"]),
    ]
    mocker.patch("src.core.services.JOBS_DB", jobs)
    return jobs

def test_match_opportunities_exact_match(mock_translate, mock_jobs_db):
    """Test that jobs with matching skills and scores are returned."""
    profile = AthleteProfile(sport="Football", role="Captain")
    matches = match_opportunities(profile, grit_score=8, teamwork_score=8)

    titles = [job.title for job in matches]
    assert "Perfect Match" in titles
    assert "Subset Match" in titles # Both required skills are in MOCK_SKILLS
    assert "Skill Mismatch" not in titles
    assert "Grit Mismatch" not in titles
    assert "Teamwork Mismatch" not in titles
    assert "Superset Mismatch" not in titles

def test_match_opportunities_grit_filter(mock_translate, mock_jobs_db):
    """Test that jobs requiring higher grit are filtered out."""
    profile = AthleteProfile(sport="Football", role="Captain")
    # Low grit score
    matches = match_opportunities(profile, grit_score=2, teamwork_score=8)

    titles = [job.title for job in matches]
    assert "Perfect Match" not in titles # min_grit=5 > 2

def test_match_opportunities_teamwork_filter(mock_translate, mock_jobs_db):
    """Test that jobs requiring higher teamwork are filtered out."""
    profile = AthleteProfile(sport="Football", role="Captain")
    # Low teamwork score
    matches = match_opportunities(profile, grit_score=8, teamwork_score=2)

    titles = [job.title for job in matches]
    assert "Perfect Match" not in titles # min_teamwork=5 > 2

def test_match_opportunities_no_skills(mocker, mock_jobs_db):
    """Test matching when athlete has no translated skills."""
    mocker.patch("src.core.services.translate_skills", return_value={})
    profile = AthleteProfile(sport="General", role="Player")
    matches = match_opportunities(profile, grit_score=10, teamwork_score=10)

    # Should only match jobs with NO required skills.
    # In mock_jobs_db, all have required skills. So empty.
    assert len(matches) == 0

def test_match_opportunities_partial_skills(mock_translate, mock_jobs_db):
    """Test that jobs requiring MORE skills than athlete has are filtered out."""
    profile = AthleteProfile(sport="Football", role="Captain")
    matches = match_opportunities(profile, grit_score=10, teamwork_score=10)

    titles = [job.title for job in matches]
    # "Superset Mismatch" requires Coding, which athlete doesn't have.
    assert "Superset Mismatch" not in titles
