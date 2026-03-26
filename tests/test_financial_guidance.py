import pytest
from src.core.services import get_compensation_estimate

@pytest.mark.parametrize("base_salary, signing_bonus, expected", [
    (100000, 10000, "$100,000 base + $10,000 sign-on"),
    (85000, 0, "$85,000 base"),
    (0, 0, "Compensation not specified"),
])
def test_get_compensation_estimate(base_salary: int, signing_bonus: int, expected: str) -> None:
    """Test that compensation string is formatted correctly."""
    result = get_compensation_estimate(base_salary, signing_bonus)
    assert result == expected
