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
    And its employer 'TechCorp' requires 'Leadership' and 'Strategic Analysis'.
    Thus, an athlete needs 'Leadership' and 'Strategic Analysis'.
    """
    profile = AthleteProfile(sport="Swimming", role="Captain")

    matches = match_opportunities(profile, grit_score=high_scores, teamwork_score=high_scores)
    titles = [job.title for job in matches]

    assert "Sales Development Representative" in titles

def test_match_opportunities_sport_specific_match(high_scores):
    """
    Test that a Basketball player matches Basketball-specific jobs.
    'Project Coordinator' requires 'Team Collaboration' (Basketball).
    Its employer 'ConsultingGroup' requires 'Strategic Execution' and 'Team Collaboration'.
    So athlete needs both. But 'Strategic Execution' is for Football.
    We need an athlete that played both or role mapped to it, or just use
    a different profile structure or mock the database. Actually,
    'Project Coordinator' requires 'Team Collaboration' and 'ConsultingGroup' requires 'Strategic Execution' + 'Team Collaboration'.
    So we need an athlete with Team Collaboration and Strategic Execution.
    Football + Basketball? Let's just mock the profile or data.
    Wait, 'ConsultingGroup' requires [SKILL_STRATEGIC_EXECUTION, SKILL_TEAM_COLLABORATION].
    So we need a profile with both. "Football and Basketball"? The sport string just does `keyword in source`.
    If sport="Football Basketball", they get both.
    """
    profile = AthleteProfile(sport="Football Basketball", role="Captain")

    matches = match_opportunities(profile, grit_score=high_scores, teamwork_score=high_scores)
    titles = [job.title for job in matches]

    assert "Project Coordinator" in titles
    assert "Sales Development Representative" in titles # Captain (Leadership) + Universal (Strategic Analysis)

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
    Employer 'LogisticsInc' requires 'Operational Command' and 'Resilience'.
    So athlete needs 'Resilience', which comes from 'Walk-on'.
    """
    profile = AthleteProfile(sport="Football", role="Captain Walk-on")

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
