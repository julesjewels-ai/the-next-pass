"""
Unit tests for the Analytics and Reporting features.
"""
from src.core.data import SKILL_LEADERSHIP, SKILL_TEAM_COLLABORATION
from src.core.models import AthleteProfile
from src.core.services import get_skill_demand_report, get_skill_gap_analysis


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


def test_get_skill_gap_analysis(mocker):
    """
    Test that get_skill_gap_analysis returns the correct missing skills
    based on market demand.
    """
    profile = AthleteProfile(sport="Football", role="Player")

    # Mock translate_skills to return specific skills
    mocker.patch(
        'src.core.services.translate_skills',
        return_value={"Strategic Execution": "Executed complex plans."}
    )

    # Mock get_skill_demand_report to return a known demand
    mocker.patch(
        'src.core.services.get_skill_demand_report',
        return_value={
            "Team Collaboration": 5,
            "Leadership": 4,
            "Strategic Execution": 3,
            "Operational Command": 2
        }
    )

    gap = get_skill_gap_analysis(profile, top_n=2)

    assert gap == ["Team Collaboration", "Leadership"]
    assert "Strategic Execution" not in gap, "Athlete already has this skill"


def test_get_skill_gap_analysis_no_gap(mocker):
    """
    Test behavior when athlete has all demanded skills.
    """
    profile = AthleteProfile(sport="Football", role="Captain")

    mocker.patch(
        'src.core.services.translate_skills',
        return_value={"Team Collaboration": "...", "Leadership": "..."}
    )

    mocker.patch(
        'src.core.services.get_skill_demand_report',
        return_value={"Team Collaboration": 5, "Leadership": 4}
    )

    gap = get_skill_gap_analysis(profile)
    assert gap == []
