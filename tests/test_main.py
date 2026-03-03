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
    main,
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
        {"Captain": "Leadership", "Playbook": "Strategy"},
        ["Leadership", "Strategy", "Athletic Context:", "Resume Bullet:"]
    ),
    (
        {},
        ["--- Resume Translation"]
    ),
])
def test_handle_translate(
    mock_translate_skills: Mock,
    capsys: CaptureFixture,
    mock_return_value: Dict[str, str],
    expected_substrings: List[str]
) -> None:
    """Test handle_translate with various match scenarios."""
    # Arrange
    args = argparse.Namespace(sport="Football", role="Captain")
    mock_translate_skills.return_value = mock_return_value

    # Act
    handle_translate(args)

    # Assert
    captured = capsys.readouterr()
    for substring in expected_substrings:
        assert substring in captured.out

    # Verify the service was called with correct profile
    mock_translate_skills.assert_called_once()
    call_arg = mock_translate_skills.call_args[0][0]
    assert isinstance(call_arg, AthleteProfile)
    assert call_arg.sport == "Football"
    assert call_arg.role == "Captain"


@pytest.fixture
def mock_match_careers(mocker: MockerFixture) -> Mock:
    """Mock the match_careers service."""
    return mocker.patch("main.match_careers")


@pytest.mark.parametrize("mock_return_value, expected_substrings", [
    (
        [Job(title="Software Engineer", employer="TechCorp", required_skills=["Coding"])],
        ["Software Engineer", "Structure is gone"]
    ),
    (
        [],
        ["Structure is gone"]
    ),
])
def test_handle_match(
    mock_match_careers: Mock,
    capsys: CaptureFixture,
    mock_return_value: List[Job],
    expected_substrings: List[str]
) -> None:
    """Test handle_match with various match scenarios."""
    # Arrange
    args = argparse.Namespace(grit=8, teamwork=9)
    mock_match_careers.return_value = mock_return_value

    # Act
    handle_match(args)

    # Assert
    captured = capsys.readouterr()
    for substring in expected_substrings:
        assert substring in captured.out

    # Verify the service was called with correct arguments
    mock_match_careers.assert_called_once_with(8, 9)


@pytest.fixture
def mock_handle_translate(mocker: MockerFixture) -> Mock:
    return mocker.patch("main.handle_translate")


@pytest.fixture
def mock_handle_match(mocker: MockerFixture) -> Mock:
    return mocker.patch("main.handle_match")


@pytest.fixture
def mock_handle_employers(mocker: MockerFixture) -> Mock:
    return mocker.patch("main.handle_employers")


@pytest.fixture
def mock_handle_opportunities(mocker: MockerFixture) -> Mock:
    return mocker.patch("main.handle_opportunities")


@pytest.fixture
def mock_print_help(mocker: MockerFixture) -> Mock:
    return mocker.patch("argparse.ArgumentParser.print_help")


@pytest.mark.parametrize("argv, expected_handler", [
    (
        ["main.py", "translate", "--sport", "Football"],
        "mock_handle_translate"
    ),
    (
        ["main.py", "match"],
        "mock_handle_match"
    ),
    (
        ["main.py", "employers", "--sport", "Basketball"],
        "mock_handle_employers"
    ),
    (
        ["main.py", "opportunities", "--sport", "Soccer"],
        "mock_handle_opportunities"
    ),
    (
        ["main.py"],
        "mock_print_help"
    ),
    (
        ["main.py", "invalid_command"],
        "mock_print_help"
    ),
])
def test_main_dispatch(
    mocker: MockerFixture,
    mock_handle_translate: Mock,
    mock_handle_match: Mock,
    mock_handle_employers: Mock,
    mock_handle_opportunities: Mock,
    mock_print_help: Mock,
    argv: List[str],
    expected_handler: str,
) -> None:
    """Test the main dispatch logic for CLI commands."""
    mocker.patch("sys.argv", argv)

    # In the case of invalid_command, argparse itself might print help and exit
    # depending on how argparse is set up (it often calls sys.exit(2) on invalid choice).
    # Since our mock of print_help doesn't exit, and argparse handles invalid choices
    # automatically, we should mock sys.exit to avoid test runner exit, OR
    # wrap it in pytest.raises(SystemExit) if argparse throws.
    if "invalid_command" in argv:
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 2
        return

    main()

    handlers = {
        "mock_handle_translate": mock_handle_translate,
        "mock_handle_match": mock_handle_match,
        "mock_handle_employers": mock_handle_employers,
        "mock_handle_opportunities": mock_handle_opportunities,
        "mock_print_help": mock_print_help,
    }

    # Verify the correct handler was called
    for name, handler in handlers.items():
        if name == expected_handler:
            handler.assert_called_once()
        else:
            handler.assert_not_called()
