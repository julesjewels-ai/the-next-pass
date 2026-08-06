"""
Unit tests for compensation estimation logic.
"""
import pytest

from src.core.services import get_compensation_estimate


@pytest.mark.parametrize(
    "base_salary, signing_bonus, expected",
    [
        (0, 0, 'Compensation not specified'),
        (100000, 0, '$100,000 base'),
        (125000, 15000, '$125,000 base + $15,000 sign-on'),
        (75500, 5000, '$75,500 base + $5,000 sign-on'),
        (80000, 0, '$80,000 base'),
        (0, 10000, '$0 base + $10,000 sign-on'), # Edge case, though unlikely in practice
    ]
)
def test_get_compensation_estimate(base_salary: int, signing_bonus: int, expected: str):
    """
    Test that get_compensation_estimate correctly formats compensation strings.
    """
    result = get_compensation_estimate(base_salary, signing_bonus)
    assert result == expected, f"Expected {expected}, but got {result}"
