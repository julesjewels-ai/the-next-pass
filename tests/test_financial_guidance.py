"""
Unit tests for the financial guidance features.
"""
import pytest
from src.core.models import Job
from src.core.services import get_compensation_estimate

@pytest.mark.parametrize("base, bonus, expected", [
    (60000, 5000, "$60000 base + $5000 sign-on"),
    (70000, 0, "$70000 base + $0 sign-on"),
    (0, 10000, "$0 base + $10000 sign-on"),
    (0, 0, "Compensation not specified"),
])
def test_get_compensation_estimate(base: int, bonus: int, expected: str) -> None:
    """Test get_compensation_estimate with different salary and bonus values."""
    job = Job(title="Test Job", base_salary=base, signing_bonus=bonus)
    assert get_compensation_estimate(job) == expected, "Compensation string format is incorrect."
