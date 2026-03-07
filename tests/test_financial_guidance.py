"""
Unit tests for Financial Guidance service.
"""
from src.core.models import Job
from src.core.services import get_compensation_estimate

def test_get_compensation_estimate() -> None:
    """Test that total compensation is correctly calculated."""
    job = Job(
        title="Software Engineer",
        employer="TechCorp",
        required_skills=["Coding"],
        base_salary=100000.0,
        signing_bonus=20000.0
    )
    comp = get_compensation_estimate(job)
    assert comp == 120000.0, "Compensation should be sum of base and signing bonus"

def test_get_compensation_estimate_zero_bonus() -> None:
    """Test compensation calculation with no signing bonus."""
    job = Job(
        title="Junior Developer",
        employer="TechCorp",
        required_skills=["Coding"],
        base_salary=80000.0,
        signing_bonus=0.0
    )
    comp = get_compensation_estimate(job)
    assert comp == 80000.0, "Compensation should equal base salary when bonus is zero"

def test_get_compensation_estimate_zero_salary() -> None:
    """Test compensation calculation with zero base salary (e.g. commission-only role)."""
    job = Job(
        title="Sales Associate",
        employer="SalesCorp",
        required_skills=["Sales"],
        base_salary=0.0,
        signing_bonus=5000.0
    )
    comp = get_compensation_estimate(job)
    assert comp == 5000.0, "Compensation should equal signing bonus when base is zero"
