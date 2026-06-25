"""
Unit tests for the Financial Guidance features.
"""
import pytest
from pydantic import ValidationError
from src.core.services import get_compensation_estimate

@pytest.mark.parametrize(
    "base_salary, signing_bonus, expected",
    [
        (0, 0, "Compensation not specified"),
        (100000, 0, "$100,000 base"),
        (120000, 15000, "$120,000 base + $15,000 sign-on"),
        (85000, 5000, "$85,000 base + $5,000 sign-on"),
        (0, 10000, "$0 base + $10,000 sign-on"),
    ]
)
def test_get_compensation_estimate_valid(base_salary: int, signing_bonus: int, expected: str) -> None:
    """Test get_compensation_estimate with valid inputs."""
    result = get_compensation_estimate(base_salary, signing_bonus)
    assert result == expected

@pytest.mark.parametrize(
    "base_salary, signing_bonus",
    [
        (-100000, 0),
        (100000, -5000),
        (-50000, -5000),
    ]
)
def test_get_compensation_estimate_invalid(base_salary: int, signing_bonus: int) -> None:
    """Test get_compensation_estimate validation rules."""
    with pytest.raises(ValidationError):
        get_compensation_estimate(base_salary, signing_bonus)
