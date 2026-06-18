"""
Unit tests for the financial guidance functionality.
"""
import pytest
from src.core.services import get_compensation_estimate

@pytest.mark.parametrize(
    "base_salary, signing_bonus, expected_output",
    [
        (0, 0, 'Compensation not specified'),
        (60000, 0, '$60,000 base'),
        (60000, 5000, '$60,000 base + $5,000 sign-on'),
        (120000, 10000, '$120,000 base + $10,000 sign-on'),
    ]
)
def test_get_compensation_estimate(base_salary: int, signing_bonus: int, expected_output: str) -> None:
    """Tests the format of estimated compensation strings."""
    assert get_compensation_estimate(base_salary, signing_bonus) == expected_output
