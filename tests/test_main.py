import pytest
from argparse import Namespace
from src.core.models import AthleteProfile, Employer
from main import handle_employers
from typing import List
from pytest_mock import MockerFixture

@pytest.mark.parametrize("sport, role, mock_matches, expected_outputs", [
    (
        "Football",
        "Captain",
        [
            Employer(name="TechCorp", industry="Tech", required_skills=["Leadership", "Strategy"]),
            Employer(name="LogisticsInc", industry="Logistics", required_skills=["Operations"])
        ],
        [
            "--- Employer Matches for Football Captain ---",
            "- TechCorp (Tech)",
            "  Required Skills: Leadership, Strategy",
            "- LogisticsInc (Logistics)",
            "  Required Skills: Operations",
            "Network is net worth."
        ]
    ),
    (
        "Curling",
        "Sweeper",
        [],
        [
            "--- Employer Matches for Curling Sweeper ---",
            "No direct matches found. Keep training.",
            "Network is net worth."
        ]
    )
])
def test_handle_employers(
    sport: str,
    role: str,
    mock_matches: List[Employer],
    expected_outputs: List[str],
    mocker: MockerFixture,
    capsys: pytest.CaptureFixture
) -> None:
    # Arrange
    args = Namespace(sport=sport, role=role)
    mock_match_employers = mocker.patch('main.match_employers', return_value=mock_matches)

    # Act
    handle_employers(args)

    # Assert
    captured = capsys.readouterr()
    output = captured.out

    # Verify mock was called with correct profile
    mock_match_employers.assert_called_once()
    call_args = mock_match_employers.call_args[0][0]
    assert isinstance(call_args, AthleteProfile)
    assert call_args.sport == sport
    assert call_args.role == role

    # Verify output contains expected strings
    for line in expected_outputs:
        assert line in output
