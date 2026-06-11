"""
Unit tests for the Financial Guidance features.
"""
import pytest
from src.core.services import get_compensation_estimate

@pytest.mark.parametrize(
    "base_salary, signing_bonus, expected_output",
    [
        (0, 0, "Compensation not specified"),
        (75000, 0, "$75,000 base"),
        (80000, 5000, "$80,000 base + $5,000 sign-on"),
        (100000, 10000, "$100,000 base + $10,000 sign-on"),
        (1500000, 250000, "$1,500,000 base + $250,000 sign-on"),
    ]
)
def test_get_compensation_estimate(base_salary: int, signing_bonus: int, expected_output: str) -> None:
    """Test get_compensation_estimate formatting variations."""
    result = get_compensation_estimate(base_salary, signing_bonus)
    assert result == expected_output, f"Expected {expected_output}, got {result}"
