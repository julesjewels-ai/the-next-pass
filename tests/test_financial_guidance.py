"""
Unit tests for Financial Guidance logic.
"""
import pytest
from src.core.services import get_compensation_estimate


@pytest.mark.parametrize("base_salary, signing_bonus, expected", [
    (60000, 5000, "$60,000 base + $5,000 sign-on"),
    (80000, 10000, "$80,000 base + $10,000 sign-on"),
    (50000, 0, "$50,000 base"),
    (0, 0, "Compensation not specified"),
])
def test_get_compensation_estimate(base_salary: int, signing_bonus: int, expected: str) -> None:
    """Test the compensation formatting function with various inputs."""
    result = get_compensation_estimate(base_salary, signing_bonus)
    assert result == expected
