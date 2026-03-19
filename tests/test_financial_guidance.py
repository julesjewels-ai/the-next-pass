"""
Unit tests for Financial Guidance features.
"""
import pytest
from src.core.services import get_compensation_estimate

@pytest.mark.parametrize("base, bonus, expected", [
    (100000, 10000, "$100,000 base + $10,000 sign-on"),
    (80000, 0, "$80,000 base"),
    (0, 0, "Compensation not specified"),
])
def test_get_compensation_estimate(base: int, bonus: int, expected: str) -> None:
    """
    Test that get_compensation_estimate correctly formats compensation.
    """
    result = get_compensation_estimate(base, bonus)
    assert result == expected, f"Expected '{expected}', got '{result}'"
