"""
Tests for the main CLI application logic.
"""
import argparse
import sys
from typing import List, Dict
from unittest.mock import Mock

import pytest
from pytest import CaptureFixture
from pytest_mock import MockerFixture
from src.core.models import Employer, AthleteProfile, Job
from main import handle_employers, handle_translate, handle_match, main


# --- Fixtures ---

@pytest.fixture
def mock_match_employers(mocker: MockerFixture) -> Mock:
    """Mock the match_employers service."""
    return mocker.patch("main.match_employers")


@pytest.fixture
def mock_translate_skills(mocker: MockerFixture) -> Mock:
    """Mock the translate_skills service."""
    return mocker.patch("main.translate_skills")


@pytest.fixture
def mock_match_careers(mocker: MockerFixture) -> Mock:
    """Mock the match_careers service."""
    return mocker.patch("main.match_careers")


# --- Handler Tests ---

@pytest.mark.parametrize("mock_return_value, expected_substrings", [
    (
        {"Leadership": "Led team of 50"},
        ["Leadership", "Led team of 50", "Resume Translation"]
    ),
    (
        {},
        ["Resume Translation"]
    ),
])
def test_handle_translate(
    mock_translate_skills: Mock,
    capsys: CaptureFixture,
    mock_return_value: Dict[str, str],
    expected_substrings: List[str]
) -> None:
    """Test handle_translate with various inputs."""
    # Arrange
    args = argparse.Namespace(sport="Football", role="Captain")
    mock_translate_skills.return_value = mock_return_value

    # Act
    handle_translate(args)

    # Assert
    captured = capsys.readouterr()
    for substring in expected_substrings:
        assert substring in captured.out

    # Verify service call
    mock_translate_skills.assert_called_once()
    call_arg = mock_translate_skills.call_args[0][0]
    assert isinstance(call_arg, AthleteProfile)
    assert call_arg.sport == "Football"
    assert call_arg.role == "Captain"


@pytest.mark.parametrize("mock_return_value, expected_substrings", [
    (
        [Job(title="CEO", min_grit=10, min_teamwork=10)],
        ["CEO", "Career Matches"]
    ),
    (
        [],
        ["Career Matches"]
    ),
])
def test_handle_match(
    mock_match_careers: Mock,
    capsys: CaptureFixture,
    mock_return_value: List[Job],
    expected_substrings: List[str]
) -> None:
    """Test handle_match with various inputs."""
    # Arrange
    args = argparse.Namespace(grit=8, teamwork=9)
    mock_match_careers.return_value = mock_return_value

    # Act
    handle_match(args)

    # Assert
    captured = capsys.readouterr()
    for substring in expected_substrings:
        assert substring in captured.out

    # Verify service call
    mock_match_careers.assert_called_once_with(8, 9)


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


# --- Main Dispatch Tests ---

@pytest.mark.parametrize("cli_args, mocked_handler_name", [
    (["main.py", "translate", "--sport", "Football"], "handle_translate"),
    (["main.py", "match", "--grit", "8"], "handle_match"),
    (["main.py", "employers", "--sport", "Football"], "handle_employers"),
])
def test_main_dispatch(
    mocker: MockerFixture,
    cli_args: List[str],
    mocked_handler_name: str
) -> None:
    """Test that main() dispatches to the correct handler based on arguments."""
    # Arrange
    mocker.patch.object(sys, "argv", cli_args)
    mock_handler = mocker.patch(f"main.{mocked_handler_name}")

    # Act
    main()

    # Assert
    mock_handler.assert_called_once()


def test_main_no_args_prints_help(mocker: MockerFixture) -> None:
    """Test that main() prints help when no arguments are provided."""
    # Arrange
    mocker.patch.object(sys, "argv", ["main.py"])
    mock_print_help = mocker.patch("argparse.ArgumentParser.print_help")

    # Act
    main()

    # Assert
    mock_print_help.assert_called_once()
