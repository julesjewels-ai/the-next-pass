"""
Unit tests for the Analytics and Reporting features.
"""
import pytest
from src.core.models import AthleteProfile
from src.core.services import get_skill_demand_report, get_skill_gap_analysis
from src.core.data import SKILL_TEAM_COLLABORATION, SKILL_LEADERSHIP, KEY_BASKETBALL

def test_get_skill_demand_report():
    """
    Test that get_skill_demand_report correctly aggregates skill frequencies
    and returns them in descending order.
    """
    demand = get_skill_demand_report()

    # Verify return type
    assert isinstance(demand, dict)

    # Verify that the report contains some known skills from the data layer
    assert SKILL_TEAM_COLLABORATION in demand
    assert SKILL_LEADERSHIP in demand

    # Verify that the results are sorted descending
    counts = list(demand.values())
    assert counts == sorted(counts, reverse=True), "Report should be sorted in descending order of demand"

def test_get_skill_demand_report_empty_db(mocker):
    """
    Test the behavior when the JOBS_DB is empty.
    """
    mocker.patch('src.core.services.JOBS_DB', [])
    demand = get_skill_demand_report()
    assert demand == {}, "Should return an empty dict when there are no jobs"


@pytest.mark.parametrize("sport, role, expected_gaps, missing_skill", [
    (KEY_BASKETBALL, "Player", True, "Strategic Execution"),
    ("Unknown Sport", "Unknown Role", True, "Team Collaboration"),
])
def test_get_skill_gap_analysis(sport, role, expected_gaps, missing_skill):
    """
    Test that get_skill_gap_analysis correctly identifies missing skills.
    """
    profile = AthleteProfile(sport=sport, role=role)
    gaps = get_skill_gap_analysis(profile)

    assert isinstance(gaps, dict)
    if expected_gaps:
        assert missing_skill in gaps, f"Expected missing skill {missing_skill} to be in gaps"

        # Verify that it's sorted descending
        counts = list(gaps.values())
        assert counts == sorted(counts, reverse=True)
