"""
Unit tests for financial guidance features.
"""
import pytest
from src.core.models import Job
from src.core.services import get_compensation_estimate

@pytest.mark.parametrize("base_salary, signing_bonus, expected", [
    (0, 0, 'Compensation not specified'),
    (60000, 0, '$60000 base'),
    (85000, 10000, '$85000 base + $10000 sign-on'),
])
def test_get_compensation_estimate(base_salary: int, signing_bonus: int, expected: str) -> None:
    """Test get_compensation_estimate with different compensation packages."""
    job = Job(title="Test Job", base_salary=base_salary, signing_bonus=signing_bonus)
    assert get_compensation_estimate(job) == expected
