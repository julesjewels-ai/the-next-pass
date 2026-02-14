"""
Unit tests for core application logic.
"""

from src.core.models import AthleteProfile
from src.core.services import translate_skills, match_careers


def test_skill_translation_captain():
    """Test that captains get specific leadership translation."""
    profile = AthleteProfile(sport="Soccer", role="Team Captain")
    result = translate_skills(profile)

    assert "Leadership" in result
    assert "coordinating team activities" in result["Leadership"]


def test_skill_translation_universal():
    """Test that all athletes get time management skills."""
    profile = AthleteProfile(sport="Tennis", role="Player")
    result = translate_skills(profile)

    assert "Time Management" in result
    assert "balancing 30+ hour training" in result["Time Management"]


def test_skill_translation_basketball():
    """Test that basketball players get team collaboration skills."""
    profile = AthleteProfile(sport="Basketball", role="Point Guard")
    result = translate_skills(profile)

    assert "Team Collaboration" in result
    assert "rapid decision-making" in result["Team Collaboration"]


def test_skill_translation_football():
    """Test that football players get strategic execution skills."""
    profile = AthleteProfile(sport="Football", role="Quarterback")
    result = translate_skills(profile)

    assert "Strategic Execution" in result
    assert "precise coordination" in result["Strategic Execution"]


def test_skill_translation_walkon():
    """Test that walk-ons get resilience skills."""
    profile = AthleteProfile(sport="Track", role="Walk-on")
    result = translate_skills(profile)

    assert "Resilience" in result
    assert "merit-based competition" in result["Resilience"]


def test_career_matching_high_grit():
    """Test that high grit scores return operations roles."""
    jobs = match_careers(grit_score=9, teamwork_score=5)
    # jobs is now List[Job], so we check titles
    titles = [job.title for job in jobs]
    assert "Operations Manager (High Intensity)" in titles


def test_career_matching_high_teamwork():
    """Test that high teamwork scores return success roles."""
    jobs = match_careers(grit_score=5, teamwork_score=9)
    titles = [job.title for job in jobs]
    assert "Customer Success Manager" in titles


def test_skill_translation_composite_football_captain():
    """Test that football captains get specific operational command skills."""
    profile = AthleteProfile(sport="Men's Football", role="Team Captain")
    result = translate_skills(profile)

    assert "Operational Command" in result
    assert "large-scale team maneuvers" in result["Operational Command"]

def test_career_matching_returns_rich_data():
    """Test that matched careers contain enhanced metadata like employer."""
    jobs = match_careers(grit_score=9, teamwork_score=5)

    # Check for Operations Manager which we know requires high grit
    ops_job = next((job for job in jobs if "Operations Manager" in job.title), None)

    assert ops_job is not None
    assert ops_job.employer == "LogisticsInc"
    assert ops_job.min_grit == 9
    assert "Strategic Execution" in ops_job.required_skills
