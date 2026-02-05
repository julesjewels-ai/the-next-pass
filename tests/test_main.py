"""
Unit tests for the CLI entry point main.py.
"""
import argparse
from typing import Dict, List, Any
import pytest
from src.core.models import Job, AthleteProfile
import main

@pytest.fixture
def mock_services(mocker: Any) -> Dict[str, Any]:
    """
    Mocks the service layer functions imported in main.py.
    """
    return {
        "translate": mocker.patch("main.translate_skills"),
        "match": mocker.patch("main.match_careers"),
    }

@pytest.mark.parametrize("sport, role, mock_return, expected_fragments", [
    (
        "Basketball",
        "Captain",
        {"Leadership": "Lead the team"},
        [
            "Resume Translation for Basketball Captain",
            "Athletic Context: \"Leadership\"",
            "Resume Bullet:    \"Lead the team\""
        ]
    ),
    (
        "Football",
        "Player",
        {},
        ["Resume Translation for Football Player"]
    ),
    (
        "Soccer",
        "Goalie",
        {"Focus": "High attention"},
        ["Athletic Context: \"Focus\"", "Resume Bullet:    \"High attention\""]
    )
])
def test_handle_translate(
    mock_services: Dict[str, Any],
    capsys: Any,
    sport: str,
    role: str,
    mock_return: Dict[str, str],
    expected_fragments: List[str]
) -> None:
    """
    Test handle_translate with various inputs.
    Verifies that the service is called with the correct profile
    and that output is formatted correctly.
    """
    # Arrange
    args = argparse.Namespace(sport=sport, role=role)
    mock_services["translate"].return_value = mock_return

    # Act
    main.handle_translate(args)

    # Assert
    captured = capsys.readouterr()
    mock_services["translate"].assert_called_once()

    # Verify the argument passed to service
    call_arg = mock_services["translate"].call_args[0][0]
    assert isinstance(call_arg, AthleteProfile)
    assert call_arg.sport == sport
    assert call_arg.role == role

    # Verify output
    for fragment in expected_fragments:
        assert fragment in captured.out


@pytest.mark.parametrize("grit, teamwork, mock_return, expected_fragments", [
    (
        8,
        9,
        [Job(title="CEO"), Job(title="CTO")],
        ["Career Matches (Grit: 8, Teamwork: 9)", "- CEO", "- CTO"]
    ),
    (
        1,
        1,
        [],
        ["Career Matches (Grit: 1, Teamwork: 1)"]
    ),
    (
        10,
        10,
        [Job(title="Founder")],
        ["Career Matches (Grit: 10, Teamwork: 10)", "- Founder"]
    )
])
def test_handle_match(
    mock_services: Dict[str, Any],
    capsys: Any,
    grit: int,
    teamwork: int,
    mock_return: List[Job],
    expected_fragments: List[str]
) -> None:
    """
    Test handle_match with various scores.
    Verifies that the service is called with correct scores
    and output lists the jobs.
    """
    # Arrange
    args = argparse.Namespace(grit=grit, teamwork=teamwork)
    mock_services["match"].return_value = mock_return

    # Act
    main.handle_match(args)

    # Assert
    captured = capsys.readouterr()
    mock_services["match"].assert_called_once_with(grit, teamwork)

    for fragment in expected_fragments:
        assert fragment in captured.out
