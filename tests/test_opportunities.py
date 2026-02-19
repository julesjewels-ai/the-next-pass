import pytest
from src.core.models import AthleteProfile, Job
from src.core.services import match_opportunities

@pytest.fixture
def mock_jobs(mocker):
    jobs = [
        Job(title="Easy Job", employer="E1", min_grit=1, min_teamwork=1, required_skills=["Skill A"]),
        Job(title="Hard Job", employer="E2", min_grit=10, min_teamwork=10, required_skills=["Skill A", "Skill B"]),
        Job(title="Skill Job", employer="E3", min_grit=5, min_teamwork=5, required_skills=["Skill C"]),
    ]
    mocker.patch("src.core.services.JOBS_DB", jobs)
    return jobs

@pytest.fixture
def mock_translate(mocker):
    return mocker.patch("src.core.services.translate_skills")

def test_match_opportunities_perfect_match(mock_jobs, mock_translate):
    """Test that a job is matched when all criteria are met."""
    mock_translate.return_value = {"Skill A": "desc", "Skill B": "desc"}
    profile = AthleteProfile(sport="Any", role="Any")

    matches = match_opportunities(profile, grit_score=10, teamwork_score=10)

    titles = [j.title for j in matches]
    assert "Easy Job" in titles
    assert "Hard Job" in titles
    assert "Skill Job" not in titles # Missing Skill C

def test_match_opportunities_score_mismatch(mock_jobs, mock_translate):
    """Test that jobs are filtered out if scores are too low."""
    mock_translate.return_value = {"Skill A": "desc", "Skill B": "desc"}
    profile = AthleteProfile(sport="Any", role="Any")

    matches = match_opportunities(profile, grit_score=5, teamwork_score=5)

    titles = [j.title for j in matches]
    assert "Easy Job" in titles
    assert "Hard Job" not in titles # Grit/Teamwork too high

def test_match_opportunities_skill_mismatch(mock_jobs, mock_translate):
    """Test that jobs are filtered out if required skills are missing."""
    mock_translate.return_value = {"Skill A": "desc"}
    profile = AthleteProfile(sport="Any", role="Any")

    matches = match_opportunities(profile, grit_score=10, teamwork_score=10)

    titles = [j.title for j in matches]
    assert "Easy Job" in titles
    assert "Hard Job" not in titles # Missing Skill B

def test_match_opportunities_no_matches(mock_jobs, mock_translate):
    """Test that no jobs are returned if nothing matches."""
    mock_translate.return_value = {"Skill Z": "desc"}
    profile = AthleteProfile(sport="Any", role="Any")

    matches = match_opportunities(profile, grit_score=1, teamwork_score=1)

    assert len(matches) == 0
