"""
Tests for the main CLI application logic.
"""
import sys
from main import main as main_func
import argparse
from typing import List
from unittest.mock import Mock

import pytest
from pytest import CaptureFixture
from pytest_mock import MockerFixture
from src.core.models import Employer, AthleteProfile, Job
from main import handle_employers, handle_opportunities

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

def test_handle_translate(mock_translate_skills: Mock, capsys: CaptureFixture) -> None:
    args = argparse.Namespace(sport="Basketball", role="Point Guard")
    mock_translate_skills.return_value = {"Led team": "Leadership"}

    from main import handle_translate
    handle_translate(args)

    captured = capsys.readouterr()
    assert "Basketball Point Guard" in captured.out
    assert "Leadership" in captured.out

@pytest.fixture
def mock_match_careers(mocker: MockerFixture) -> Mock:
    """Mock the match_careers service."""
    return mocker.patch("main.match_careers")

def test_handle_match(mock_match_careers: Mock, capsys: CaptureFixture) -> None:
    args = argparse.Namespace(grit=5, teamwork=5)
    mock_match_careers.return_value = [Job(title="Analyst", employer="Bank", required_skills=[])]

    from main import handle_match
    handle_match(args)

    captured = capsys.readouterr()
    assert "Analyst" in captured.out




@pytest.mark.parametrize("args, handler_to_mock", [
    (['main.py', 'translate', '--sport', 'Soccer'], 'main.handle_translate'),
    (['main.py', 'match', '--grit', '5', '--teamwork', '5'], 'main.handle_match'),
    (['main.py', 'employers', '--sport', 'Tennis'], 'main.handle_employers'),
    (['main.py', 'opportunities', '--sport', 'Golf', '--grit', '5', '--teamwork', '5'], 'main.handle_opportunities'),
])
def test_main_dispatch_commands(
    mocker: MockerFixture, args: List[str], handler_to_mock: str
) -> None:
    mocker.patch.object(sys, 'argv', args)
    mock_handler = mocker.patch(handler_to_mock)
    main_func()
    assert mock_handler.call_count == 1, f"Expected {handler_to_mock} to be called exactly once for args {args}"


@pytest.mark.parametrize("args, should_exit, expected_output", [
    (['main.py', 'invalid'], True, None),
    (['main.py'], False, "usage:"),
])
def test_main_dispatch_edge_cases(
    mocker: MockerFixture, capsys: CaptureFixture, args: List[str], should_exit: bool, expected_output: str | None
) -> None:
    mocker.patch.object(sys, 'argv', args)
    if should_exit:
        with pytest.raises(SystemExit):
            main_func()
    else:
        main_func()
        captured = capsys.readouterr()
        if expected_output:
            assert expected_output in captured.out, f"Expected output '{expected_output}' not found in '{captured.out}' for args {args}"
