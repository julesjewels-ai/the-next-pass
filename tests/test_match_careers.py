"""
Tests for career matching logic in the service layer.
"""
import pytest
from pytest_mock import MockerFixture
from typing import List

from src.core.models import Job
from src.core.services import match_careers


@pytest.fixture
def mock_jobs_db(mocker: MockerFixture) -> List[Job]:
    """Overrides JOBS_DB with controlled data for boundary testing."""
    jobs = [
        Job(title="Entry Level", min_grit=1, min_teamwork=1),
        Job(title="Mid Level", min_grit=5, min_teamwork=5),
        Job(title="Senior Level", min_grit=8, min_teamwork=8),
        Job(title="Specialist (High Grit)", min_grit=9, min_teamwork=2),
        Job(title="Coordinator (High Teamwork)", min_grit=2, min_teamwork=9),
    ]
    mocker.patch("src.core.services.JOBS_DB", jobs)
    return jobs


@pytest.mark.parametrize("grit, teamwork, expected_titles", [
    # Exact Boundary Matches
    (1, 1, ["Entry Level"]),
    (5, 5, ["Entry Level", "Mid Level"]),
    (8, 8, ["Entry Level", "Mid Level", "Senior Level"]),

    # Off-by-one Failures (Grit)
    (4, 5, ["Entry Level"]),  # Fails Mid Level (grit 5)
    (7, 8, ["Entry Level", "Mid Level"]), # Fails Senior (grit 8)

    # Off-by-one Failures (Teamwork)
    (5, 4, ["Entry Level"]), # Fails Mid Level (teamwork 5)
    (8, 7, ["Entry Level", "Mid Level"]), # Fails Senior (teamwork 8)

    # Mixed High/Low
    (9, 2, ["Entry Level", "Specialist (High Grit)"]),
    (2, 9, ["Entry Level", "Coordinator (High Teamwork)"]),

    # Zero and Negative Inputs (Should filter out everything requiring > 0)
    (0, 0, []),
    (-1, -1, []),

    # Max Values
    (10, 10, [
        "Entry Level", "Mid Level", "Senior Level",
        "Specialist (High Grit)", "Coordinator (High Teamwork)"
    ]),
])
def test_match_careers_boundaries(
    mock_jobs_db: List[Job],
    grit: int,
    teamwork: int,
    expected_titles: List[str]
) -> None:
    """
    Test match_careers with various boundary conditions.
    """
    matches = match_careers(grit, teamwork)
    titles = [job.title for job in matches]

    # Sort for consistent comparison
    assert sorted(titles) == sorted(expected_titles)


def test_match_careers_empty_db(mocker: MockerFixture) -> None:
    """Test that an empty database returns no matches regardless of score."""
    mocker.patch("src.core.services.JOBS_DB", [])
    matches = match_careers(10, 10)
    assert matches == []
