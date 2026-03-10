"""
Tests for financial guidance services.
"""
import pytest
from src.core.models import Job
from src.core.services import get_compensation_estimate

@pytest.mark.parametrize(
    "base_salary, signing_bonus, expected_output",
    [
        (0, 0, "$0 Base"),
        (60000, 0, "$60,000 Base"),
        (75000, 5000, "$75,000 Base + $5,000 Bonus"),
        (100000, 15000, "$100,000 Base + $15,000 Bonus"),
        (0, 5000, "$0 Base + $5,000 Bonus"),
    ]
)
def test_get_compensation_estimate(
    base_salary: int,
    signing_bonus: int,
    expected_output: str
) -> None:
    """Test formatting of compensation estimates."""
    job = Job(
        title="Test Role",
        employer="Test Corp",
        required_skills=[],
        base_salary=base_salary,
        signing_bonus=signing_bonus
    )
    result = get_compensation_estimate(job)
    assert result == expected_output, f"Expected {expected_output}, got {result}"
