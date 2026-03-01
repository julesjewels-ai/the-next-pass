"""
Tests for the main CLI application logic.
"""
import argparse
from typing import List
from unittest.mock import Mock

import pytest
from pytest import CaptureFixture
import sys
from pytest_mock import MockerFixture
from src.core.models import Employer, AthleteProfile, Job
from main import handle_employers, handle_opportunities, handle_translate, handle_match, main

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
        assert substring in captured.out, f"Expected '{substring}' to be in output '{captured.out}'"

    # Verify the service was called with correct profile
    mock_match_employers.assert_called_once()
    call_arg = mock_match_employers.call_args[0][0]
    assert isinstance(call_arg, AthleteProfile), f"Expected AthleteProfile, got {type(call_arg)}"
    assert call_arg.sport == "Football", f"Expected sport 'Football', got '{call_arg.sport}'"
    assert call_arg.role == "Captain", f"Expected role 'Captain', got '{call_arg.role}'"


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
        assert substring in captured.out, f"Expected '{substring}' to be in output '{captured.out}'"

    # Verify the service was called with correct arguments
    mock_match_opportunities.assert_called_once()
    # Call args: (profile, grit, teamwork)
    call_args = mock_match_opportunities.call_args[0]
    profile_arg = call_args[0]
    grit_arg = call_args[1]
    teamwork_arg = call_args[2]

    assert isinstance(profile_arg, AthleteProfile), f"Expected AthleteProfile, got {type(profile_arg)}"
    assert profile_arg.sport == "Football", f"Expected sport 'Football', got '{profile_arg.sport}'"
    assert profile_arg.role == "Captain", f"Expected role 'Captain', got '{profile_arg.role}'"
    assert grit_arg == 8, f"Expected grit 8, got {grit_arg}"
    assert teamwork_arg == 9, f"Expected teamwork 9, got {teamwork_arg}"


@pytest.fixture
def mock_translate_skills(mocker: MockerFixture) -> Mock:
    """Mock the translate_skills service."""
    return mocker.patch("main.translate_skills")

@pytest.mark.parametrize("mock_return_value, expected_substrings", [
    (
        {"Communication": "Cross-functional Collaboration"},
        ["Athletic Context: \"Communication\"", "Resume Bullet:    \"Cross-functional Collaboration\""]
    ),
    (
        {},
        ["--- Resume Translation for Football Captain ---"]
    )
])
def test_handle_translate(
    mock_translate_skills: Mock,
    capsys: CaptureFixture,
    mock_return_value: dict,
    expected_substrings: List[str]
) -> None:
    """Test handle_translate with various match scenarios."""
    args = argparse.Namespace(sport="Football", role="Captain")
    mock_translate_skills.return_value = mock_return_value

    handle_translate(args)

    captured = capsys.readouterr()
    for substring in expected_substrings:
        assert substring in captured.out, f"Expected '{substring}' to be in output '{captured.out}'"

    mock_translate_skills.assert_called_once()
    call_arg = mock_translate_skills.call_args[0][0]
    assert isinstance(call_arg, AthleteProfile), f"Expected AthleteProfile, got {type(call_arg)}"
    assert call_arg.sport == "Football", f"Expected sport 'Football', got '{call_arg.sport}'"
    assert call_arg.role == "Captain", f"Expected role 'Captain', got '{call_arg.role}'"


@pytest.fixture
def mock_match_careers(mocker: MockerFixture) -> Mock:
    """Mock the match_careers service."""
    return mocker.patch("main.match_careers")

@pytest.mark.parametrize("mock_return_value, expected_substrings", [
    (
        [Job(title="Software Engineer", employer="TechCorp", required_skills=["Coding"])],
        ["- Software Engineer", "Structure is gone. But your discipline remains."]
    ),
    (
        [],
        ["Structure is gone. But your discipline remains."]
    )
])
def test_handle_match(
    mock_match_careers: Mock,
    capsys: CaptureFixture,
    mock_return_value: List[Job],
    expected_substrings: List[str]
) -> None:
    """Test handle_match with various match scenarios."""
    args = argparse.Namespace(grit=8, teamwork=9)
    mock_match_careers.return_value = mock_return_value

    handle_match(args)

    captured = capsys.readouterr()
    for substring in expected_substrings:
        assert substring in captured.out, f"Expected '{substring}' to be in output '{captured.out}'"

    mock_match_careers.assert_called_once_with(8, 9)


@pytest.mark.parametrize("args, expected_handler", [
    (["main.py", "translate", "--sport", "Football", "--role", "Captain"], "translate"),
    (["main.py", "match", "--grit", "8", "--teamwork", "9"], "match"),
    (["main.py", "employers", "--sport", "Football"], "employers"),
    (["main.py", "opportunities", "--sport", "Football"], "opportunities"),
])
def test_main_dispatch(
    mocker: MockerFixture,
    args: List[str],
    expected_handler: str
) -> None:
    """Test that main dispatches to the correct handler."""
    mocker.patch.object(sys, "argv", args)

    mock_translate = mocker.patch("main.handle_translate")
    mock_match = mocker.patch("main.handle_match")
    mock_employers = mocker.patch("main.handle_employers")
    mock_opportunities = mocker.patch("main.handle_opportunities")

    main()

    if expected_handler == "translate":
        mock_translate.assert_called_once()
    elif expected_handler == "match":
        mock_match.assert_called_once()
    elif expected_handler == "employers":
        mock_employers.assert_called_once()
    elif expected_handler == "opportunities":
        mock_opportunities.assert_called_once()

def test_main_dispatch_help(mocker: MockerFixture, capsys: CaptureFixture) -> None:
    """Test that main prints help when no matching command is found."""
    mocker.patch.object(sys, "argv", ["main.py"])

    # When no command is provided, parse_args will return a Namespace with command=None
    # This should trigger parser.print_help()
    main()

    captured = capsys.readouterr()
    assert "usage:" in captured.out, f"Expected 'usage:' in output '{captured.out}'"
