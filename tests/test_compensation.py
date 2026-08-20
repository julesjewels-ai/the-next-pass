"""
Unit tests for compensation estimation logic.
"""
import pytest
from pydantic import ValidationError

from src.core.services import get_compensation_estimate


@pytest.mark.parametrize(
    "base_salary, signing_bonus, expected",
    [
        (100000, 10000, "$100,000 base + $10,000 sign-on"),
        (50000, 0, "$50,000 base"),
        (0, 0, "Compensation not specified"),
        (-10, 0, ValidationError),
        (0, -5000, ValidationError),
    ]
)
def test_get_compensation_estimate(base_salary: int, signing_bonus: int, expected: str | type) -> None:
    """Test compensation string formatting and validation bounds."""
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            get_compensation_estimate(base_salary, signing_bonus)  # type: ignore
    else:
        result = get_compensation_estimate(base_salary, signing_bonus)  # type: ignore
        assert result == expected
