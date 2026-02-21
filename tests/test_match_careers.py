"""
Tests for career matching logic in the service layer.
Targeting high complexity / critical path logic with extensive parametrization.
"""
from typing import List

import pytest
from pytest_mock import MockerFixture

from src.core.models import Job
from src.core.services import match_careers


@pytest.fixture
def mock_jobs_db(mocker: MockerFixture) -> List[Job]:
    """
    Fixture that overrides src.core.services.JOBS_DB with a controlled set of jobs.
    Returns the list of jobs for verification.
    """
    jobs = [
        Job(title="Entry Level", min_grit=1, min_teamwork=1),
        Job(title="Mid Grit", min_grit=5, min_teamwork=1),
        Job(title="Mid Teamwork", min_grit=1, min_teamwork=5),
        Job(title="Senior Level", min_grit=8, min_teamwork=8),
        Job(title="Impossible Job", min_grit=11, min_teamwork=11),
        Job(title="Zero Barrier", min_grit=0, min_teamwork=0),
    ]
    mocker.patch("src.core.services.JOBS_DB", jobs)
    return jobs


@pytest.mark.parametrize("grit, teamwork, expected_titles", [
    (1, 1, ["Entry Level", "Zero Barrier"]),
    (5, 1, ["Entry Level", "Mid Grit", "Zero Barrier"]),
    (1, 5, ["Entry Level", "Mid Teamwork", "Zero Barrier"]),
    (8, 8, ["Entry Level", "Mid Grit", "Mid Teamwork", "Senior Level", "Zero Barrier"]),
    (10, 10, ["Entry Level", "Mid Grit", "Mid Teamwork", "Senior Level", "Zero Barrier"]),
    (11, 11, ["Entry Level", "Mid Grit", "Mid Teamwork", "Senior Level", "Impossible Job", "Zero Barrier"]),
    (0, 0, ["Zero Barrier"]),
    (-1, -1, []),
    (4, 4, ["Entry Level", "Zero Barrier"]),  # Boundary check: just below 5
    (5, 4, ["Entry Level", "Mid Grit", "Zero Barrier"]),  # Mixed boundary
    (4, 5, ["Entry Level", "Mid Teamwork", "Zero Barrier"]),  # Mixed boundary
])
def test_match_careers_logic(
    mock_jobs_db: List[Job],
    grit: int,
    teamwork: int,
    expected_titles: List[str]
) -> None:
    """
    Test match_careers with various score combinations.
    Focus on boundary conditions and edge cases.
    """
    # Act
    matches = match_careers(grit_score=grit, teamwork_score=teamwork)

    # Assert
    matched_titles = [job.title for job in matches]
    assert set(matched_titles) == set(expected_titles)


def test_match_careers_empty_db(mocker: MockerFixture) -> None:
    """Test that an empty database returns no matches regardless of score."""
    mocker.patch("src.core.services.JOBS_DB", [])
    matches = match_careers(grit_score=10, teamwork_score=10)
    assert matches == []
