"""
Unit tests for the Analytics and Reporting features.
"""
import pytest
from src.core.services import get_skill_demand_report, get_compensation_estimate
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

@pytest.mark.parametrize("base, bonus, expected", [
    (100000, 10000, "$100,000 base + $10,000 sign-on"),
    (85000, 0, "$85,000 base"),
    (0, 0, "Compensation not specified"),
    (0, 5000, "$0 base + $5,000 sign-on"),
    (-1000, 1000, ValueError),
    (1000, -1000, ValueError),
    (-50, -50, ValueError),
])
def test_get_compensation_estimate(base, bonus, expected):
    """
    Test the compensation estimation formatting and bounds checking.
    """
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            get_compensation_estimate(base, bonus)
    else:
        assert get_compensation_estimate(base, bonus) == expected
