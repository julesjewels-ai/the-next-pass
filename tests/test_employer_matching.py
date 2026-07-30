"""
Tests for employer matching logic in the service layer.
"""
import pytest

from src.core.data import SKILL_LEADERSHIP
from src.core.models import AthleteProfile, Employer
from src.core.services import match_employers


@pytest.fixture
def mock_employers(mocker):
    """Overrides SAMPLE_EMPLOYERS with controlled data."""
    employers = [
        Employer(
            name="Match Corp",
            industry="Tech",
            required_skills=[SKILL_LEADERSHIP]
        ),
        Employer(
            name="Mismatch Inc",
            industry="Sales",
            required_skills=["Non Existent Skill"]
        ),
        Employer(
            name="Partial Ltd",
            industry="Ops",
            required_skills=[SKILL_LEADERSHIP, "Missing Skill"]
        )
    ]
    mocker.patch("src.core.services.SAMPLE_EMPLOYERS", employers)
    return employers

def test_match_employers_success(mock_employers):
    """Test that an employer with satisfied requirements is returned."""
    # Captain has Leadership. Universal has Strategic Analysis.
    profile = AthleteProfile(sport="Basketball", role="Captain")
    matches = match_employers(profile)

    # Should match Match Corp (Leadership)
    names = [e.name for e in matches]
    assert "Match Corp" in names
    assert len(matches) == 1

def test_match_employers_partial_failure(mock_employers):
    """Test that partial matches are NOT returned."""
    # Captain has Leadership but not "Missing Skill"
    profile = AthleteProfile(sport="Basketball", role="Captain")
    matches = match_employers(profile)

    names = [e.name for e in matches]
    assert "Partial Ltd" not in names

def test_match_employers_no_match(mock_employers):
    """Test that no matches are returned when skills don't align."""
    # "Player" role (with "Tennis") usually implies just Universal skills.
    # Universal: Time Management, Strategic Analysis.
    # None of the mock employers only require these.
    profile = AthleteProfile(sport="Tennis", role="Player")
    matches = match_employers(profile)

    assert len(matches) == 0

def test_integration_tech_corp():
    """
    Integration test with real SAMPLE_EMPLOYERS.
    TechCorp requires: Leadership, Strategic Analysis.
    - Leadership comes from 'Captain' role.
    - Strategic Analysis is a Universal skill.
    Therefore, any Captain should match TechCorp.
    """
    profile = AthleteProfile(sport="Swimming", role="Captain")
    matches = match_employers(profile)

    names = [e.name for e in matches]
    assert "TechCorp" in names

def test_integration_logistics_fail():
    """
    Integration test with real SAMPLE_EMPLOYERS.
    LogisticsInc requires: Operational Command, Resilience.
    - Operational Command comes from Football + Captain.
    - Resilience comes from Walk-on.
    A Football Captain (Recruited) should NOT match.
    """
    profile = AthleteProfile(sport="Football", role="Captain")
    matches = match_employers(profile)

    names = [e.name for e in matches]
    assert "LogisticsInc" not in names
