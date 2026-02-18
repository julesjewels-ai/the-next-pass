"""
Tests for unified job matching logic.
"""
import pytest
from src.core.models import AthleteProfile, Job
from src.core.services import match_opportunities
from src.core.data import (
    SKILL_LEADERSHIP,
    SKILL_STRATEGIC_ANALYSIS,
    SKILL_RESILIENCE
)

@pytest.fixture
def mock_jobs(mocker):
    """Overrides JOBS_DB with controlled data."""
    jobs = [
        Job(
            title="Generalist",
            min_grit=1,
            min_teamwork=1,
            required_skills=[]
        ),
        Job(
            title="Elite Commander",
            min_grit=9,
            min_teamwork=9,
            required_skills=[SKILL_LEADERSHIP, SKILL_STRATEGIC_ANALYSIS]
        ),
        Job(
            title="Gritty Worker",
            min_grit=8,
            min_teamwork=1,
            required_skills=[SKILL_RESILIENCE]
        )
    ]
    mocker.patch("src.core.services.JOBS_DB", jobs)
    return jobs

def test_match_opportunities_perfect_match(mock_jobs):
    """Test that a high-performing athlete matches elite jobs."""
    # Captain provides Leadership.
    # Universal provides Strategic Analysis.
    profile = AthleteProfile(
        sport="Football",
        role="Captain",
        grit=10,
        teamwork=10
    )
    matches = match_opportunities(profile)
    titles = [j.title for j in matches]

    assert "Elite Commander" in titles
    assert "Generalist" in titles
    # Missing Resilience (which comes from Walk-on)
    assert "Gritty Worker" not in titles

def test_match_opportunities_low_scores(mock_jobs):
    """Test that low scores filter out demanding jobs."""
    profile = AthleteProfile(
        sport="Football",
        role="Captain",
        grit=5,
        teamwork=5
    )
    matches = match_opportunities(profile)
    titles = [j.title for j in matches]

    assert "Elite Commander" not in titles # Needs 9/9
    assert "Generalist" in titles

def test_match_opportunities_missing_skills(mock_jobs):
    """Test that missing skills filter out jobs even with high scores."""
    # Tennis Player has Universal skills but not Leadership.
    profile = AthleteProfile(
        sport="Tennis",
        role="Player",
        grit=10,
        teamwork=10
    )
    matches = match_opportunities(profile)
    titles = [j.title for j in matches]

    assert "Elite Commander" not in titles # Missing Leadership
    assert "Generalist" in titles

def test_match_opportunities_resilience(mock_jobs):
    """Test that Walk-on matches Gritty Worker."""
    # Walk-on -> Resilience
    profile = AthleteProfile(
        sport="Track",
        role="Walk-on",
        grit=9,
        teamwork=5
    )
    matches = match_opportunities(profile)
    titles = [j.title for j in matches]

    assert "Gritty Worker" in titles
