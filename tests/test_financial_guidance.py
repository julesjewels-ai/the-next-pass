"""
Unit tests for financial guidance and compensation estimates.
"""
import pytest
from src.core.models import Job
from src.core.services import get_compensation_estimate

@pytest.mark.parametrize("base_salary, signing_bonus, expected", [
    (100000, 10000, "$100000 base + $10000 sign-on"),
    (85000, 0, "$85000 base + $0 sign-on"),
    (0, 5000, "$0 base + $5000 sign-on"),
    (0, 0, "Compensation not specified"),
])
def test_get_compensation_estimate(base_salary: int, signing_bonus: int, expected: str) -> None:
    """Test getting compensation estimate string from Job DTO."""
    job = Job(
        title="Test Job",
        base_salary=base_salary,
        signing_bonus=signing_bonus
    )
    assert get_compensation_estimate(job) == expected
