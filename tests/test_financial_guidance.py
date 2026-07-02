"""
Unit tests for the Financial Guidance features.
"""
import pytest
from pydantic import ValidationError
from src.core.services import get_compensation_estimate

@pytest.mark.parametrize("base, bonus, expected", [
    (100000, 15000, "$100,000 base + $15,000 sign-on"),
    (80000, 0, "$80,000 base"),
    (0, 0, "Compensation not specified"),
    (-50000, 0, ValidationError),
    (100000, -10000, ValidationError),
])
def test_get_compensation_estimate(base: int, bonus: int, expected: type | str) -> None:
    """Test get_compensation_estimate with valid and invalid inputs."""
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            get_compensation_estimate(base, bonus)
    else:
        assert isinstance(expected, str)
        result = get_compensation_estimate(base, bonus)
        assert result == expected
