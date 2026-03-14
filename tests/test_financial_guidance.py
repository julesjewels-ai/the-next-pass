"""
Unit tests for the Financial Guidance features.
"""
import pytest
from src.core.models import Job
from src.core.services import get_compensation_estimate

@pytest.mark.parametrize("base, bonus, expected", [
    (60000, 5000, "$60000 base + $5000 sign-on"),
    (0, 5000, "$0 base + $5000 sign-on"),
    (60000, 0, "$60000 base + $0 sign-on"),
    (0, 0, "Compensation not specified"),
    (100000, 15000, "$100000 base + $15000 sign-on"),
])
def test_get_compensation_estimate(base: int, bonus: int, expected: str) -> None:
    """Test get_compensation_estimate with various combinations of base salary and bonus."""
    job = Job(title="Test Job", required_skills=[], base_salary=base, signing_bonus=bonus)
    result = get_compensation_estimate(job)
    assert result == expected, f"Expected '{expected}' but got '{result}'"
