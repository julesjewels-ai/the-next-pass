import pytest
import argparse
from typing import List
from pytest_mock import MockerFixture
from main import handle_employers
from src.core.models import Employer

@pytest.fixture
def mock_match_employers(mocker: MockerFixture):
    return mocker.patch("main.match_employers")

@pytest.mark.parametrize("matches, expected_outputs", [
    (
        [],
        [
            "--- Employer Matches for Football Captain ---",
            "No direct matches found. Keep training.",
            "Network is net worth."
        ]
    ),
    (
        [Employer(name="TestCorp", industry="Tech", required_skills=["Coding"])],
        [
            "--- Employer Matches for Football Captain ---",
            "- TestCorp (Tech)",
            "Required Skills: Coding",
            "Network is net worth."
        ]
    )
])
def test_handle_employers(
    mock_match_employers,
    capsys: pytest.CaptureFixture,
    matches: List[Employer],
    expected_outputs: List[str]
):
    # Arrange
    args = argparse.Namespace(sport="Football", role="Captain")
    mock_match_employers.return_value = matches

    # Act
    handle_employers(args)

    # Assert
    captured = capsys.readouterr()
    for output in expected_outputs:
        assert output in captured.out
