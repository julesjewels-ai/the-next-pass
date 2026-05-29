"""
Unit tests for the financial guidance feature.
"""
import pytest
from src.core.services import get_compensation_estimate

@pytest.mark.parametrize("base_salary, signing_bonus, expected", [
    (0, 0, 'Compensation not specified'),
    (60000, 0, '$60,000 base'),
    (85000, 10000, '$85,000 base + $10,000 sign-on'),
    (100000, 0, '$100,000 base'),
    (150000, 25000, '$150,000 base + $25,000 sign-on'),
])
def test_get_compensation_estimate(base_salary: int, signing_bonus: int, expected: str) -> None:
    """Test get_compensation_estimate formatting."""
    assert get_compensation_estimate(base_salary, signing_bonus) == expected
