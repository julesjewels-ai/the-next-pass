"""
Unit tests for the Analytics and Reporting features.
"""
from pytest_mock import MockerFixture

from src.core.data import SKILL_LEADERSHIP, SKILL_TEAM_COLLABORATION
from src.core.services import get_skill_demand_report, get_trait_demand_report


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

def test_get_skill_demand_report_empty_db(mocker: MockerFixture) -> None:
    """
    Test the behavior when the JOBS_DB is empty.
    """
    mocker.patch('src.core.services.JOBS_DB', [])
    demand = get_skill_demand_report()
    assert demand == {}, "Should return an empty dict when there are no jobs"


def test_get_trait_demand_report() -> None:
    """
    Test that get_trait_demand_report correctly calculates average trait requirements.
    """
    demand = get_trait_demand_report()

    # Verify return type
    assert isinstance(demand, dict)
    assert 'grit' in demand
    assert 'teamwork' in demand

    # Verify that the results are positive floats
    assert isinstance(demand['grit'], float)
    assert isinstance(demand['teamwork'], float)
    assert demand['grit'] >= 0.0
    assert demand['teamwork'] >= 0.0


def test_get_trait_demand_report_empty_db(mocker: MockerFixture) -> None:
    """
    Test the behavior of trait demand when the JOBS_DB is empty.
    """
    mocker.patch('src.core.services.JOBS_DB', [])
    demand = get_trait_demand_report()
    assert demand == {'grit': 0.0, 'teamwork': 0.0}, "Should return zeros when there are no jobs"
