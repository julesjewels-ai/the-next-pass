"""
Tests for the main CLI application logic.
"""
import argparse
from typing import List, Dict
from unittest.mock import Mock

import pytest
from pytest import CaptureFixture
from pytest_mock import MockerFixture
from src.core.models import Employer, AthleteProfile, Job
from main import (
    handle_employers,
    handle_opportunities,
    handle_translate,
    handle_match,
    main
)

@pytest.fixture
def mock_match_employers(mocker: MockerFixture) -> Mock:
    """Mock the match_employers service."""
    return mocker.patch("main.match_employers")

@pytest.mark.parametrize("mock_return_value, expected_substrings", [
    (
        [Employer(name="TechCorp", industry="Tech", required_skills=["Coding"])],
        ["TechCorp", "(Tech)", "Required Skills: Coding"]
    ),
    (
        [],
        ["No direct matches found", "Keep training"]
    ),
    (
        [
            Employer(name="TechCorp", industry="Tech", required_skills=["Coding"]),
            Employer(name="BizCorp", industry="Business", required_skills=["Strategy"])
        ],
        ["TechCorp", "BizCorp", "Coding", "Strategy"]
    )
])
def test_handle_employers(
    mock_match_employers: Mock,
    capsys: CaptureFixture,
    mock_return_value: List[Employer],
    expected_substrings: List[str]
) -> None:
    """Test handle_employers with various match scenarios."""
    # Arrange
    args = argparse.Namespace(sport="Football", role="Captain")
    mock_match_employers.return_value = mock_return_value

    # Act
    handle_employers(args)

    # Assert
    captured = capsys.readouterr()
    for substring in expected_substrings:
        assert substring in captured.out

    # Verify the service was called with correct profile
    mock_match_employers.assert_called_once()
    call_arg = mock_match_employers.call_args[0][0]
    assert isinstance(call_arg, AthleteProfile)
    assert call_arg.sport == "Football"
    assert call_arg.role == "Captain"


@pytest.fixture
def mock_match_opportunities(mocker: MockerFixture) -> Mock:
    """Mock the match_opportunities service."""
    return mocker.patch("main.match_opportunities")

@pytest.mark.parametrize("mock_return_value, expected_substrings", [
    (
        [Job(title="Software Engineer", employer="TechCorp", required_skills=["Coding"])],
        ["Software Engineer", "(TechCorp)"]
    ),
    (
        [],
        ["No direct matches found", "Expand your skillset"]
    ),
])
def test_handle_opportunities(
    mock_match_opportunities: Mock,
    capsys: CaptureFixture,
    mock_return_value: List[Job],
    expected_substrings: List[str]
) -> None:
    """Test handle_opportunities with various match scenarios."""
    # Arrange
    args = argparse.Namespace(sport="Football", role="Captain", grit=8, teamwork=9)
    mock_match_opportunities.return_value = mock_return_value

    # Act
    handle_opportunities(args)

    # Assert
    captured = capsys.readouterr()
    for substring in expected_substrings:
        assert substring in captured.out

    # Verify the service was called with correct arguments
    mock_match_opportunities.assert_called_once()
    # Call args: (profile, grit, teamwork)
    call_args = mock_match_opportunities.call_args[0]
    profile_arg = call_args[0]
    grit_arg = call_args[1]
    teamwork_arg = call_args[2]

    assert isinstance(profile_arg, AthleteProfile)
    assert profile_arg.sport == "Football"
    assert profile_arg.role == "Captain"
    assert grit_arg == 8
    assert teamwork_arg == 9


@pytest.fixture
def mock_translate_skills(mocker: MockerFixture) -> Mock:
    """Mock the translate_skills service."""
    return mocker.patch("main.translate_skills")


@pytest.mark.parametrize("mock_return_value, expected_substrings", [
    (
        {"Agility": "Adaptive Thinking", "Stamina": "Endurance"},
        ["Adaptive Thinking", "Endurance", "Agility", "Stamina"]
    ),
    (
        {},
        ["Resume Translation"]  # Even empty, it prints the header
    )
])
def test_handle_translate(
    mock_translate_skills: Mock,
    capsys: CaptureFixture,
    mock_return_value: Dict[str, str],
    expected_substrings: List[str]
) -> None:
    """Test handle_translate with various skill sets."""
    # Arrange
    args = argparse.Namespace(sport="Swimming", role="Starter")
    mock_translate_skills.return_value = mock_return_value

    # Act
    handle_translate(args)

    # Assert
    captured = capsys.readouterr()
    for substring in expected_substrings:
        assert substring in captured.out

    # Verify call
    mock_translate_skills.assert_called_once()
    call_arg = mock_translate_skills.call_args[0][0]
    assert isinstance(call_arg, AthleteProfile)
    assert call_arg.sport == "Swimming"
    assert call_arg.role == "Starter"


@pytest.fixture
def mock_match_careers(mocker: MockerFixture) -> Mock:
    """Mock the match_careers service."""
    return mocker.patch("main.match_careers")


@pytest.mark.parametrize("mock_return_value, expected_substrings", [
    (
        [Job(title="Project Manager", min_grit=7, min_teamwork=8)],
        ["Project Manager", "Career Matches"]
    ),
    (
        [],
        ["Career Matches", "Structure is gone"]
    )
])
def test_handle_match(
    mock_match_careers: Mock,
    capsys: CaptureFixture,
    mock_return_value: List[Job],
    expected_substrings: List[str]
) -> None:
    """Test handle_match with various job matches."""
    # Arrange
    args = argparse.Namespace(grit=8, teamwork=9)
    mock_match_careers.return_value = mock_return_value

    # Act
    handle_match(args)

    # Assert
    captured = capsys.readouterr()
    for substring in expected_substrings:
        assert substring in captured.out

    # Verify call
    mock_match_careers.assert_called_once_with(8, 9)


@pytest.mark.parametrize("cli_args, expected_handler_mock", [
    (["main.py", "translate", "--sport", "Football", "--role", "Captain"], "handle_translate"),
    (["main.py", "match", "--grit", "8", "--teamwork", "9"], "handle_match"),
    (["main.py", "employers", "--sport", "Football", "--role", "Captain"], "handle_employers"),
    (["main.py", "opportunities", "--sport", "Football", "--role", "Captain", "--grit", "8", "--teamwork", "9"], "handle_opportunities"),
])
def test_main_dispatch(
    mocker: MockerFixture,
    cli_args: List[str],
    expected_handler_mock: str
) -> None:
    """Test that main() dispatches to the correct handler."""
    # Arrange
    mocker.patch("sys.argv", cli_args)

    # Mock all handlers to verify dispatch
    # Note: main.py imports these, so we must patch them where main.py uses them.
    # However, main.py uses the function objects directly in the command_handlers dict.
    # If we patch 'main.handle_translate', it updates the name in main module.
    # When main() runs, it builds the dict using these updated names.
    mock_handlers = {
        "handle_translate": mocker.patch("main.handle_translate"),
        "handle_match": mocker.patch("main.handle_match"),
        "handle_employers": mocker.patch("main.handle_employers"),
        "handle_opportunities": mocker.patch("main.handle_opportunities"),
    }

    # Act
    main()

    # Assert
    # Verify the expected handler was called
    mock_handlers[expected_handler_mock].assert_called_once()

    # Verify others were not called
    for name, mock in mock_handlers.items():
        if name != expected_handler_mock:
            mock.assert_not_called()


def test_main_help(mocker: MockerFixture, capsys: CaptureFixture) -> None:
    """Test main() with no command prints help."""
    mocker.patch("sys.argv", ["main.py"])

    # Act
    main()

    # Assert
    captured = capsys.readouterr()
    assert "usage:" in captured.out
    assert "The 98%: Career Platform for Student-Athletes" in captured.out
