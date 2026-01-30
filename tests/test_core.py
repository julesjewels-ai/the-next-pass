"""
Unit tests for core application logic.
"""

from src.core.app import AthleteProfile, translate_skills, match_careers


def test_skill_translation_captain():
    """Test that captains get specific leadership translation."""
    profile = AthleteProfile(sport="Soccer", role="Team Captain")
    result = translate_skills(profile)

    assert "Leadership" in result
    assert "coordinating team activities" in result["Leadership"]


def test_skill_translation_goalkeeper():
    """Test that goalkeepers get risk management translation."""
    profile = AthleteProfile(sport="Soccer", role="Goalkeeper")
    result = translate_skills(profile)

    assert "Risk Management" in result
    assert "decisive decision-making" in result["Risk Management"]


def test_skill_translation_quarterback():
    """Test that quarterbacks get strategic vision translation."""
    profile = AthleteProfile(sport="Football", role="Quarterback")
    result = translate_skills(profile)

    assert "Strategic Vision" in result
    assert "analyzing complex scenarios" in result["Strategic Vision"]


def test_skill_translation_universal():
    """Test that all athletes get time management skills."""
    profile = AthleteProfile(sport="Tennis", role="Player")
    result = translate_skills(profile)

    assert "Time Management" in result
    assert "balancing 30+ hour training" in result["Time Management"]


def test_career_matching_high_grit():
    """Test that high grit scores return operations roles."""
    jobs = match_careers(grit_score=9, teamwork_score=5)
    assert "Operations Manager (High Intensity)" in jobs


def test_career_matching_high_teamwork():
    """Test that high teamwork scores return success roles."""
    jobs = match_careers(grit_score=5, teamwork_score=9)
    assert "Customer Success Manager" in jobs
