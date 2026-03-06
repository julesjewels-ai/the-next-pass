"""
Unit tests for the Financial Guidance features.
"""
from src.core.models import Job
from src.core.services import get_compensation_estimate

def test_get_compensation_estimate():
    """
    Test that get_compensation_estimate correctly calculates total compensation.
    """
    job = Job(
        title="Software Engineer",
        employer="TechCorp",
        required_skills=["Coding"],
        base_salary=100000,
        signing_bonus=15000
    )

    comp = get_compensation_estimate(job)

    assert comp["base_salary"] == 100000
    assert comp["signing_bonus"] == 15000
    assert comp["total"] == 115000

def test_get_compensation_estimate_zero_bonus():
    """
    Test the behavior when the signing bonus is zero.
    """
    job = Job(
        title="Project Manager",
        employer="BizCorp",
        required_skills=["Management"],
        base_salary=80000,
        signing_bonus=0
    )

    comp = get_compensation_estimate(job)

    assert comp["base_salary"] == 80000
    assert comp["signing_bonus"] == 0
    assert comp["total"] == 80000
