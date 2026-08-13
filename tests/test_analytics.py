"""
Unit tests for the Analytics and Reporting features.
"""
import pytest
from src.core.models import AthleteProfile
from src.core.services import get_skill_demand_report, get_skill_gap_analysis
from src.core.data import SKILL_TEAM_COLLABORATION, SKILL_LEADERSHIP

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


@pytest.mark.parametrize("mock_market_demand, mock_athlete_skills, expected_gaps", [
    (
        {"Strategic Execution": 5, "Team Collaboration": 3},
        {"Team Collaboration": "Description"},
        {"Strategic Execution": 5}
    ),
    (
        {"Strategic Execution": 5, "Team Collaboration": 3},
        {"Strategic Execution": "Description", "Team Collaboration": "Description"},
        {}
    ),
    (
        {},
        {"Team Collaboration": "Description"},
        {}
    )
])
def test_get_skill_gap_analysis(
    mocker,
    mock_market_demand,
    mock_athlete_skills,
    expected_gaps
):
    """
    Test that get_skill_gap_analysis correctly identifies missing skills
    by mocking dependencies.
    """
    mocker.patch(
        'src.core.services.get_skill_demand_report',
        return_value=mock_market_demand
    )
    mocker.patch(
        'src.core.services.translate_skills',
        return_value=mock_athlete_skills
    )

    profile = AthleteProfile(sport="Any", role="Any")
    gaps = get_skill_gap_analysis(profile)

    assert gaps == expected_gaps
