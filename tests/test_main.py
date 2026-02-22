"""
Tests for the main CLI application logic.
"""
import argparse
from typing import List, Dict, Optional
from unittest.mock import Mock

import pytest
from pytest import CaptureFixture
from pytest_mock import MockerFixture
from src.core.models import Employer, AthleteProfile, Job
from main import handle_employers, handle_translate, handle_match, main

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

@pytest.fixture
def mock_argparse(mocker: MockerFixture) -> Mock:
    """Mock argparse to prevent sys.argv parsing."""
    return mocker.patch("argparse.ArgumentParser.parse_args")

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


@pytest.mark.parametrize("mock_return_value, expected_substrings", [
    (
        {"Leadership": "Led team"},
        ["Leadership", "Led team"]
    ),
    (
        {},
        []  # No output expected if empty, or at least header
    ),
    (
        {"Skill A": "Desc A", "Skill B": "Desc B"},
        ["Skill A", "Desc A", "Skill B", "Desc B"]
    )
])
def test_handle_translate(
    mock_translate_skills: Mock,
    capsys: CaptureFixture,
    mock_return_value: Dict[str, str],
    expected_substrings: List[str]
) -> None:
    """Test handle_translate with various skill sets."""
    args = argparse.Namespace(sport="Basketball", role="Captain")
    mock_translate_skills.return_value = mock_return_value

    handle_translate(args)

    captured = capsys.readouterr()
    # Always check for header
    assert "Resume Translation for Basketball Captain" in captured.out
    for substring in expected_substrings:
        assert substring in captured.out

    mock_translate_skills.assert_called_once()
    call_arg = mock_translate_skills.call_args[0][0]
    assert isinstance(call_arg, AthleteProfile)
    assert call_arg.sport == "Basketball"
    assert call_arg.role == "Captain"


@pytest.mark.parametrize("mock_return_value, expected_substrings", [
    (
        [Job(title="Manager", employer="Corp", min_grit=5, min_teamwork=5, required_skills=[])],
        ["- Manager"]
    ),
    (
        [],
        ["Structure is gone. But your discipline remains."]
    ),
    (
        [
            Job(title="Job A", employer="A", min_grit=1, min_teamwork=1),
            Job(title="Job B", employer="B", min_grit=1, min_teamwork=1)
        ],
        ["- Job A", "- Job B"]
    )
])
def test_handle_match(
    mock_match_careers: Mock,
    capsys: CaptureFixture,
    mock_return_value: List[Job],
    expected_substrings: List[str]
) -> None:
    """Test handle_match with various job lists."""
    args = argparse.Namespace(grit=8, teamwork=9)
    mock_match_careers.return_value = mock_return_value

    handle_match(args)

    captured = capsys.readouterr()
    assert "Career Matches (Grit: 8, Teamwork: 9)" in captured.out
    for substring in expected_substrings:
        assert substring in captured.out

    mock_match_careers.assert_called_once_with(8, 9)


@pytest.mark.parametrize("args_namespace, expected_handler_mock_name", [
    (argparse.Namespace(command='translate', sport='Tennis', role='Player'), 'handle_translate'),
    (argparse.Namespace(command='match', grit=5, teamwork=5), 'handle_match'),
    (argparse.Namespace(command='employers', sport='Soccer', role='Striker'), 'handle_employers'),
    (argparse.Namespace(command=None), None),
])
def test_main_dispatch(
    mocker: MockerFixture,
    mock_argparse: Mock,
    args_namespace: argparse.Namespace,
    expected_handler_mock_name: Optional[str]
) -> None:
    """Test main function dispatch logic."""
    mock_argparse.return_value = args_namespace

    # Mock all handlers
    handler_names = ['handle_translate', 'handle_match', 'handle_employers']
    mock_handlers = {name: mocker.patch(f"main.{name}") for name in handler_names}

    # Mock print_help
    mock_print_help = mocker.patch("argparse.ArgumentParser.print_help")

    main()

    if expected_handler_mock_name:
        mock_handlers[expected_handler_mock_name].assert_called_once_with(args_namespace)
        mock_print_help.assert_not_called()
        # Verify others not called
        for name, mock in mock_handlers.items():
            if name != expected_handler_mock_name:
                mock.assert_not_called()
    else:
        # Expect print_help
        mock_print_help.assert_called_once()
        # Verify no handlers called
        for mock in mock_handlers.values():
            mock.assert_not_called()
