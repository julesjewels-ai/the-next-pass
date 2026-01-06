"""
Unit tests for core application logic.
"""

import pytest
from src.core.app import CareerPlatform, AthleteProfile

@pytest.fixture
def platform():
    return CareerPlatform()

def test_skill_translation_captain(platform):
    """Test that captains get specific leadership translation."""
    profile = AthleteProfile(sport="Soccer", role="Team Captain")
    result = platform.translate_skills(profile)
    
    assert "Leadership" in result
    assert "coordinating team activities" in result["Leadership"]

def test_skill_translation_universal(platform):
    """Test that all athletes get time management skills."""
    profile = AthleteProfile(sport="Tennis", role="Player")
    result = platform.translate_skills(profile)
    
    assert "Time Management" in result
    assert "balancing 30+ hour training" in result["Time Management"]

def test_career_matching_high_grit(platform):
    """Test that high grit scores return operations roles."""
    jobs = platform.match_careers(grit_score=9, teamwork_score=5)
    assert "Operations Manager (High Intensity)" in jobs

def test_career_matching_high_teamwork(platform):
    """Test that high teamwork scores return success roles."""
    jobs = platform.match_careers(grit_score=5, teamwork_score=9)
    assert "Customer Success Manager" in jobs

def test_loads_skills_from_json(platform):
    """Verify that the skill database is loaded from the JSON file."""
    # Check that _skill_db is a dictionary and not empty
    assert isinstance(platform._skill_db, dict)
    assert len(platform._skill_db) > 0

    # Check for a specific, known key from the JSON file
    assert "Injury Rehab" in platform._skill_db
    assert "overcoming significant setbacks" in platform._skill_db["Injury Rehab"]
