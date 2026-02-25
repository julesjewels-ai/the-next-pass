"""
Unit tests for opportunity matching (skills + soft skills).
"""
import pytest
from src.core.models import AthleteProfile
from src.core.services import match_opportunities
from src.core.data import HIGH_SCORE_THRESHOLD

@pytest.fixture
def high_scores():
    return HIGH_SCORE_THRESHOLD + 1

@pytest.fixture
def low_scores():
    return 0

def test_match_opportunities_universal_match(high_scores):
    """
    Test that a general athlete matches jobs with only universal skills.
    'Sales Development Representative' requires 'Strategic Analysis' (Universal).
    """
    profile = AthleteProfile(sport="Swimming", role="Player")
    # Swimmers get Universal skills.
    # SDR requires Strategic Analysis.

    matches = match_opportunities(profile, grit_score=high_scores, teamwork_score=high_scores)
    titles = [job.title for job in matches]

    assert "Sales Development Representative" in titles

def test_match_opportunities_sport_specific_match(high_scores):
    """
    Test that a Basketball player matches Basketball-specific jobs.
    'Project Coordinator' requires 'Team Collaboration' (Basketball).
    """
    profile = AthleteProfile(sport="Basketball", role="Player")

    matches = match_opportunities(profile, grit_score=high_scores, teamwork_score=high_scores)
    titles = [job.title for job in matches]

    assert "Project Coordinator" in titles
    assert "Sales Development Representative" in titles # Also has Universal

def test_match_opportunities_role_specific_match(high_scores):
    """
    Test that a Captain matches jobs requiring Leadership.
    But we don't have a job that requires ONLY Leadership currently.
    'Customer Success Manager' requires Team Collaboration AND Leadership.
    """
    profile = AthleteProfile(sport="Basketball", role="Captain")

    matches = match_opportunities(profile, grit_score=high_scores, teamwork_score=high_scores)
    titles = [job.title for job in matches]

    assert "Customer Success Manager" in titles

def test_match_opportunities_composite_match(high_scores):
    """
    Test that a Football Captain matches Composite jobs.
    'Operations Manager' requires 'Operational Command' (Football Captain).
    """
    profile = AthleteProfile(sport="Football", role="Captain")

    matches = match_opportunities(profile, grit_score=high_scores, teamwork_score=high_scores)
    titles = [job.title for job in matches]

    assert "Operations Manager (High Intensity)" in titles

def test_match_opportunities_grit_filter(high_scores, low_scores):
    """
    Test that low grit score filters out high grit jobs even if skills match.
    'Operations Manager' requires high grit.
    """
    profile = AthleteProfile(sport="Football", role="Captain")

    matches = match_opportunities(profile, grit_score=low_scores, teamwork_score=high_scores)
    titles = [job.title for job in matches]

    assert "Operations Manager (High Intensity)" not in titles

def test_match_opportunities_teamwork_filter(high_scores, low_scores):
    """
    Test that low teamwork score filters out high teamwork jobs.
    'Customer Success Manager' requires high teamwork.
    """
    profile = AthleteProfile(sport="Basketball", role="Captain")

    matches = match_opportunities(profile, grit_score=high_scores, teamwork_score=low_scores)
    titles = [job.title for job in matches]

    assert "Customer Success Manager" not in titles

def test_match_opportunities_missing_skill(high_scores):
    """
    Test that an athlete without the required skill does NOT match.
    'Project Coordinator' requires 'Team Collaboration' (Basketball).
    A Football player should NOT match it.
    """
    profile = AthleteProfile(sport="Football", role="Player")

    matches = match_opportunities(profile, grit_score=high_scores, teamwork_score=high_scores)
    titles = [job.title for job in matches]

    assert "Project Coordinator" not in titles

def test_match_opportunities_walkon_analyst(high_scores):
    """
    Test that a Walk-on matches 'Supply Chain Analyst'.
    Requires Resilience (Walk-on) and Strategic Analysis (Universal).
    """
    profile = AthleteProfile(sport="Swimming", role="Walk-on")
    matches = match_opportunities(profile, grit_score=high_scores, teamwork_score=high_scores)
    titles = [job.title for job in matches]

    assert "Supply Chain Analyst" in titles

def test_match_opportunities_leadership_program(high_scores):
    """
    Test that a Captain matches 'Leadership Development Program'.
    Requires Leadership (Captain) and Time Management (Universal).
    """
    profile = AthleteProfile(sport="Tennis", role="Captain")
    matches = match_opportunities(profile, grit_score=high_scores, teamwork_score=high_scores)
    titles = [job.title for job in matches]

    assert "Leadership Development Program" in titles

def test_match_opportunities_field_operations(high_scores):
    """
    Test that a Football Walk-on Captain matches 'Field Operations Supervisor'.
    Requires Operational Command (Football Captain) and Resilience (Walk-on).
    This demonstrates handling multiple roles/keywords in the profile.
    """
    # Assuming role can be "Walk-on Captain" or similar
    profile = AthleteProfile(sport="Football", role="Walk-on Captain")
    matches = match_opportunities(profile, grit_score=high_scores, teamwork_score=high_scores)
    titles = [job.title for job in matches]

    assert "Field Operations Supervisor" in titles
